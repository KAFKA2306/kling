from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Protocol

from api.multi_image_to_video._requests import (
    ImageItem,
    MultiImageToVideoRequest,
)
from models.image_to_video import ImageToVideoRequest
from models.storyboard import ReferenceAsset, VideoStoryboard
from models.text_to_video import TextToVideoRequest


KlingRoute = Literal["text_to_video", "image_to_video", "multi_image_to_video"]


class KlingPostClient(Protocol):
    async def post(
        self,
        endpoint: str,
        json: dict[str, Any] | None = None,
        response_model: type[Any] | None = None,
    ) -> Any: ...


@dataclass(frozen=True)
class KlingStoryboardPlan:
    route: KlingRoute
    endpoint: str
    payload: dict[str, Any]
    storyboard_id: str
    compiler_version: str


class KlingStoryboardCompiler:
    """Compile provider-neutral storyboard IR into the SDK's existing Kling routes.

    The compiler is deliberately fail-closed. A storyboard is never rounded to a
    provider duration, and reference modes that the current request models cannot
    represent are rejected instead of being silently discarded.
    """

    version = "storyboard-kling-v1"
    supported_durations = {5, 10}
    supported_aspect_ratios = {"16:9", "9:16", "1:1"}

    def compile(
        self,
        storyboard: VideoStoryboard,
        *,
        model_name: str = "kling-v1-6",
        mode: str = "std",
        cfg_scale: float = 0.5,
    ) -> KlingStoryboardPlan:
        duration = self._validate_storyboard(storyboard)
        prompt = self._compile_prompt(storyboard)
        negative_prompt = self._compile_negative_prompt(storyboard)
        assets = storyboard.reference_assets

        first_frames = [asset for asset in assets if asset.role == "first_frame"]
        last_frames = [asset for asset in assets if asset.role == "last_frame"]
        reference_images = [asset for asset in assets if asset.role == "reference_image"]
        unsupported = [
            asset
            for asset in assets
            if asset.role in {"reference_video", "reference_audio"}
        ]
        if unsupported:
            roles = sorted({asset.role for asset in unsupported})
            raise ValueError(
                "current Kling storyboard adapter cannot preserve these reference roles: "
                + ", ".join(roles)
            )

        if (first_frames or last_frames) and reference_images:
            raise ValueError("first/last-frame mode cannot be mixed with multi-image reference mode")
        if len(first_frames) > 1 or len(last_frames) > 1:
            raise ValueError("at most one first frame and one last frame are supported")

        if first_frames or last_frames:
            if not first_frames:
                raise ValueError("current Kling image-to-video request requires a first frame")
            request = ImageToVideoRequest(
                model_name=model_name,
                image=first_frames[0].uri,
                image_tail=last_frames[0].uri if last_frames else None,
                prompt=prompt,
                negative_prompt=negative_prompt or None,
                cfg_scale=cfg_scale,
                mode=mode,
                duration=duration,
                external_task_id=storyboard.storyboard_id,
            )
            return self._plan(
                storyboard,
                "image_to_video",
                "/v1/videos/image2video",
                request.model_dump(mode="json", exclude_none=True),
            )

        if reference_images:
            if len(reference_images) > 4:
                raise ValueError("current Kling multi-image request supports at most four images")
            request = MultiImageToVideoRequest(
                model_name=model_name,
                image_list=[ImageItem(image=asset.uri) for asset in reference_images],
                prompt=prompt,
                negative_prompt=negative_prompt or None,
                mode=mode,
                duration=duration,
                aspect_ratio=storyboard.aspect_ratio,
                external_task_id=storyboard.storyboard_id,
            )
            return self._plan(
                storyboard,
                "multi_image_to_video",
                "/v1/videos/multi-image-to-video",
                request.model_dump(mode="json", exclude_none=True),
            )

        request = TextToVideoRequest(
            model_name=model_name,
            prompt=prompt,
            negative_prompt=negative_prompt or None,
            cfg_scale=cfg_scale,
            mode=mode,
            aspect_ratio=storyboard.aspect_ratio,
            duration=duration,
            external_task_id=storyboard.storyboard_id,
        )
        return self._plan(
            storyboard,
            "text_to_video",
            "/v1/videos/text2video",
            request.model_dump(mode="json", exclude_none=True),
        )

    def _validate_storyboard(self, storyboard: VideoStoryboard) -> int:
        if storyboard.duration_seconds != int(storyboard.duration_seconds):
            raise ValueError("Kling request duration must be an integer")
        duration = int(storyboard.duration_seconds)
        if duration not in self.supported_durations:
            raise ValueError("current Kling request models support exact durations of 5 or 10 seconds")
        if storyboard.aspect_ratio not in self.supported_aspect_ratios:
            raise ValueError(
                "current Kling request models support 16:9, 9:16, or 1:1 aspect ratios"
            )
        return duration

    def _compile_prompt(self, storyboard: VideoStoryboard) -> str:
        lines = [f"Global style: {storyboard.global_style}"] if storyboard.global_style else []
        assets = {asset.asset_id: asset for asset in storyboard.reference_assets}
        for shot in sorted(storyboard.shots, key=lambda item: (item.start_sec, item.end_sec, item.shot_id)):
            fields = [
                f"[{shot.start_sec:.3f}-{shot.end_sec:.3f}s] {shot.message}",
            ]
            if shot.composition:
                fields.append(f"composition={shot.composition}")
            if shot.subject_state:
                fields.append(f"subject_state={shot.subject_state}")
            if shot.motion:
                fields.append("motion=" + "; ".join(shot.motion))
            if shot.transition_in:
                fields.append(f"transition_in={shot.transition_in}")
            if shot.typography:
                cues = [
                    "/".join(filter(None, (cue.text, cue.reveal, cue.emphasis)))
                    for cue in shot.typography
                ]
                fields.append("typography=" + "; ".join(cues))
            if shot.style_invariants:
                fields.append("style_invariants=" + "; ".join(shot.style_invariants))
            if shot.reference_asset_ids:
                refs = [assets[asset_id] for asset_id in shot.reference_asset_ids]
                fields.append("references=" + ", ".join(self._describe_asset(ref) for ref in refs))
            lines.append(" | ".join(fields))

        prompt = "\n".join(lines)
        if len(prompt) > 2500:
            raise ValueError("compiled Kling prompt exceeds the current 2500-character request limit")
        return prompt

    @staticmethod
    def _compile_negative_prompt(storyboard: VideoStoryboard) -> str:
        constraints = list(storyboard.negative_constraints)
        for shot in sorted(storyboard.shots, key=lambda item: (item.start_sec, item.end_sec, item.shot_id)):
            constraints.extend(shot.negative_constraints)
        deduped = list(dict.fromkeys(item.strip() for item in constraints if item.strip()))
        negative_prompt = "; ".join(deduped)
        if len(negative_prompt) > 2500:
            raise ValueError("compiled Kling negative prompt exceeds the current 2500-character request limit")
        return negative_prompt

    @staticmethod
    def _describe_asset(asset: ReferenceAsset) -> str:
        return f"{asset.asset_id}:{asset.role}"

    def _plan(
        self,
        storyboard: VideoStoryboard,
        route: KlingRoute,
        endpoint: str,
        payload: dict[str, Any],
    ) -> KlingStoryboardPlan:
        return KlingStoryboardPlan(
            route=route,
            endpoint=endpoint,
            payload=payload,
            storyboard_id=storyboard.storyboard_id,
            compiler_version=self.version,
        )


class KlingStoryboardAdapter:
    def __init__(self, compiler: KlingStoryboardCompiler | None = None) -> None:
        self.compiler = compiler or KlingStoryboardCompiler()

    def compile(self, storyboard: VideoStoryboard, **kwargs: Any) -> KlingStoryboardPlan:
        return self.compiler.compile(storyboard, **kwargs)

    async def submit(
        self,
        client: KlingPostClient,
        storyboard: VideoStoryboard,
        **kwargs: Any,
    ) -> tuple[KlingStoryboardPlan, Any]:
        plan = self.compile(storyboard, **kwargs)
        response = await client.post(plan.endpoint, json=plan.payload)
        return plan, response
