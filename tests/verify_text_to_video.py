import asyncio
import os
from dotenv import load_dotenv
from config import KlingConfig
from ..api.text_to_video.text_to_video import TextToVideoAPI

async def main():
    load_dotenv()
    config = KlingConfig(
        api_key=os.getenv("KLING_ACCESS_KEY"),
        secret_key=os.getenv("KLING_SECRET_KEY")
    )

    async with TextToVideoAPI(config) as client:
        task = await client.create(
            prompt="A cat walking in a garden",
            duration=5,
            aspect_ratio="16:9",
            mode="std"
        )
        print(f"Task ID: {task.task_id}")
        print(f"Status: {task.task_status}")

asyncio.run(main())
