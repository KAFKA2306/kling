from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..client import KlingClient
from ..api.text_to_video._response import TaskResponse


@dataclass(slots=True)
class GenerateTextToVideoUseCase:
    client: KlingClient

    async def execute(self, prompt: str, **kwargs: Any) -> TaskResponse:
        return await self.client.text_to_video.create(prompt=prompt, **kwargs)
