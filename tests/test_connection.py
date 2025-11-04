import asyncio
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
import httpx
import jwt


def generate_jwt_token(access_key: str, secret_key: str) -> str:
    payload = {
        "iss": access_key,
        "exp": int(time.time()) + 1800,
        "nbf": int(time.time()) - 5
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")


async def test_connection():
    load_dotenv()

    access_key = os.getenv("KLING_ACCESS_KEY")
    secret_key = os.getenv("KLING_SECRET_KEY")
    base_url = os.getenv("KLING_BASE_URL", "https://api.klingai.com")

    jwt_token = generate_jwt_token(access_key, secret_key)

    end_time = int(datetime.now().timestamp() * 1000)
    start_time = int((datetime.now() - timedelta(days=1)).timestamp() * 1000)

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(
            f"{base_url}/account/costs",
            headers={"Authorization": f"Bearer {jwt_token}"},
            params={"start_time": start_time, "end_time": end_time}
        )

        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Code: {data.get('code')}")
        print(f"Message: {data.get('message')}")


if __name__ == "__main__":
    asyncio.run(test_connection())
