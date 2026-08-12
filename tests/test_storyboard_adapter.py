from __future__ import annotations

import pytest

from models.storyboard import ReferenceAsset, Shot, VideoStoryboard
from usecases.storyboard import KlingStoryboardAdapter, KlingStoryboardCompiler


def make_storyboard(**overrides) -> VideoStoryboard:
    data = {
        "storyboard_id": "kling-fixture-10s",
        "duration_seconds": 10,
        "aspect_ratio": "16:9",
        "resolution_target": "1080P",
        "global_style": "clean financial explainer",
        "shots": [
            Shot(
                shot_id="s01",
                start_sec=0,
                end_sec=5,
                message="show the market opening",
                motion=["slow push"],
            ),
            Shot(
                shot_id="s02",
                start_sec=5,
                end_sec=10,
                message="show the closing comparison",
                motion=["hold steady"],
            ),
        ],
        "gap_policy": "forbid",
    }
    data.update(overrides)
    return VideoStoryboard(**data)


def test_text_to_video_plan_is_deterministic() -> None:
    compiler = KlingStoryboardCompiler()
    storyboard = make_storyboard()
    first = compiler.compile(storyboard)
    second = compiler.compile(storyboard)

    assert first == second
    assert first.route == "text_to_video"
    assert first.endpoint == "/v1/videos/text2video"
    assert first.payload["duration"] == 10
    assert first.payload["aspect_ratio"] == "16:9"
    assert first.payload["external_task_id"] == storyboard.storyboard_id


def test_first_and_last_frame_compile_to_image_to_video() -> None:
    first = ReferenceAsset(
        asset_id="first",
        kind="image",
        uri="https://example.invalid/first.png",
        role="first_frame",
    )
    last = ReferenceAsset(
        asset_id="last",
        kind="image",
        uri="https://example.invalid/last.png",
        role="last_frame",
    )
    plan = KlingStoryboardCompiler().compile(make_storyboard(reference_assets=[first, last]))

    assert plan.route == "image_to_video"
    assert plan.payload["image"] == str(first.uri)
    assert plan.payload["image_tail"] == str(last.uri)


def test_reference_images_compile_to_multi_image_route() -> None:
    refs = [
        ReferenceAsset(
            asset_id=f"ref-{index}",
            kind="image",
            uri=f"https://example.invalid/ref-{index}.png",
            role="reference_image",
        )
        for index in range(1, 4)
    ]
    plan = KlingStoryboardCompiler().compile(make_storyboard(reference_assets=refs))

    assert plan.route == "multi_image_to_video"
    assert plan.endpoint == "/v1/videos/multi-image-to-video"
    assert [item["image"] for item in plan.payload["image_list"]] == [asset.uri for asset in refs]


def test_provider_incompatible_duration_fails_instead_of_rounding() -> None:
    with pytest.raises(ValueError, match="5 or 10"):
        KlingStoryboardCompiler().compile(
            make_storyboard(
                duration_seconds=12,
                shots=[Shot(shot_id="s01", start_sec=0, end_sec=12, message="one message")],
            )
        )


def test_reference_video_fails_when_current_request_model_cannot_preserve_it() -> None:
    video = ReferenceAsset(
        asset_id="motion",
        kind="video",
        uri="https://example.invalid/motion.mp4",
        role="reference_video",
        provider_asset_id="provider-video-id",
    )
    with pytest.raises(ValueError, match="reference_video"):
        KlingStoryboardCompiler().compile(make_storyboard(reference_assets=[video]))


def test_last_frame_without_first_frame_fails_closed() -> None:
    last = ReferenceAsset(
        asset_id="last",
        kind="image",
        uri="https://example.invalid/last.png",
        role="last_frame",
    )
    with pytest.raises(ValueError, match="requires a first frame"):
        KlingStoryboardCompiler().compile(make_storyboard(reference_assets=[last]))


@pytest.mark.asyncio
async def test_submit_uses_compiled_endpoint_without_real_network() -> None:
    class FakeClient:
        def __init__(self) -> None:
            self.calls = []

        async def post(self, endpoint, json=None, response_model=None):
            self.calls.append((endpoint, json, response_model))
            return {"task_id": "dry-run-task"}

    client = FakeClient()
    plan, response = await KlingStoryboardAdapter().submit(client, make_storyboard())

    assert client.calls == [(plan.endpoint, plan.payload, None)]
    assert response == {"task_id": "dry-run-task"}
