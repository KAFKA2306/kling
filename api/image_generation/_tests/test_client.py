"""Tests for the Kling AI Image Generation API client."""

import json
from datetime import datetime
import pytest
import httpx
import respx

from kling.client import KlingClient
from kling.config import KlingConfig
from .. import (
    ImageGenerationRequest,
    ModelName,
    AspectRatio,
    TaskStatus,
    TaskResponse,
    TaskListResponse,
)


@pytest.fixture
def mock_client() -> KlingClient:
    """Create a KlingClient instance with a mock HTTP client."""
    config = KlingConfig(api_key="test-api-key", secret_key="test-secret-key", base_url="https://api.test.kling.ai")
    return KlingClient(config)


@pytest.fixture
def task_response() -> dict:
    """Sample task response data."""
    return {
        "code": 0,
        "message": "success",
        "request_id": "req_1234567890",
        "data": {
            "task_id": "task_1234567890",
            "task_status": "submitted",
            "created_at": int(datetime.now().timestamp() * 1000),
            "updated_at": int(datetime.now().timestamp() * 1000),
        },
    }


@pytest.fixture
def completed_task_response() -> dict:
    """Sample completed task response data."""
    return {
        "code": 0,
        "message": "success",
        "request_id": "req_1234567890",
        "data": {
            "task_id": "task_1234567890",
            "task_status": "succeed",
            "created_at": int(datetime.now().timestamp() * 1000) - 10000,
            "updated_at": int(datetime.now().timestamp() * 1000),
            "task_result": {
                "images": [
                    {
                        "index": 0,
                        "url": "https://example.com/image1.jpg",
                    },
                    {
                        "index": 1,
                        "url": "https://example.com/image2.jpg",
                    },
                ]
            },
        },
    }


@pytest.fixture
def task_list_response() -> dict:
    """Sample task list response data."""
    now = int(datetime.now().timestamp() * 1000)
    return {
        "code": 0,
        "message": "success",
        "request_id": "req_list_1234567890",
        "data": [
            {
                "task_id": "task_1",
                "task_status": "succeed",
                "created_at": now - 20000,
                "updated_at": now - 10000,
                "task_result": {
                    "images": [{"index": 0, "url": "https://example.com/img1.jpg"}]
                },
            },
            {
                "task_id": "task_2",
                "task_status": "processing",
                "created_at": now - 5000,
                "updated_at": now - 1000,
                "task_result": None,
            },
        ],
    }


@pytest.mark.asyncio
async def test_create_image_generation_task(mock_client: KlingClient, task_response: dict):
    """Test creating an image generation task."""
    with respx.mock(base_url=mock_client.base_url) as respx_mock:
        # Mock the API response
        respx_mock.post("/v1/images/generations").mock(
            return_value=httpx.Response(200, json=task_response)
        )
        
        # Call the API
        response = await mock_client.image_generation.create_task(
            prompt="A beautiful sunset over mountains",
            model_name=ModelName.KLING_V1_5,
            aspect_ratio=AspectRatio.RATIO_16_9,
            n=2,
        )
        
        # Verify the response
        assert isinstance(response, TaskResponse)
        assert response.data.task_id == "task_1234567890"
        
        # Verify the request
        assert respx_mock.calls.call_count == 1
        request_data = json.loads(respx_mock.calls[0].request.content)
        assert request_data["model_name"] == "kling-v1-5"
        assert request_data["prompt"] == "A beautiful sunset over mountains"
        assert request_data["aspect_ratio"] == "16:9"
        assert request_data["n"] == 2


@pytest.mark.asyncio
async def test_get_task_status(mock_client: KlingClient, completed_task_response: dict):
    """Test getting task status."""
    with respx.mock(base_url=mock_client.base_url) as respx_mock:
        # Mock the API response
        task_id = "task_1234567890"
        respx_mock.get(f"/v1/images/generations/{task_id}").mock(
            return_value=httpx.Response(200, json=completed_task_response)
        )
        
        # Call the API
        response = await mock_client.image_generation.get_task(task_id)
        
        # Verify the response
        assert isinstance(response, TaskResponse)
        assert response.data.task_id == task_id
        assert response.data.task_status == TaskStatus.SUCCEEDED
        assert len(response.data.task_result.images) == 2
        assert response.data.task_result.images[0].url == "https://example.com/image1.jpg"
        assert response.data.task_result.images[1].url == "https://example.com/image2.jpg"


@pytest.mark.asyncio
async def test_list_tasks(mock_client: KlingClient, task_list_response: dict):
    """Test listing tasks with pagination."""
    with respx.mock(base_url=mock_client.base_url) as respx_mock:
        # Mock the API response
        respx_mock.get("/v1/images/generations").mock(
            return_value=httpx.Response(200, json=task_list_response)
        )
        
        # Call the API
        response = await mock_client.image_generation.list_tasks()
        
        # Verify the response
        assert isinstance(response, TaskListResponse)
        assert len(response.data) == 2
        assert response.data[0].task_id == "task_1"
        assert response.data[0].task_status == TaskStatus.SUCCEEDED
        assert response.data[1].task_id == "task_2"
        assert response.data[1].task_status == TaskStatus.PROCESSING


@pytest.mark.asyncio
async def test_wait_for_task_completion(mock_client: KlingClient):
    """Test waiting for task completion with polling."""
    task_id = "task_1234567890"
    
    # Create responses for different polling attempts
    processing_response = {
        "code": 0,
        "message": "success",
        "request_id": "req_123",
        "data": {
            "task_id": task_id,
            "task_status": "processing",
            "created_at": int(datetime.now().timestamp() * 1000) - 10000,
            "updated_at": int(datetime.now().timestamp() * 1000) - 5000,
        },
    }
    
    completed_response = {
        "code": 0,
        "message": "success",
        "request_id": "req_456",
        "data": {
            "task_id": task_id,
            "task_status": "succeed",
            "created_at": int(datetime.now().timestamp() * 1000) - 10000,
            "updated_at": int(datetime.now().timestamp() * 1000),
            "task_result": {
                "images": [
                    {
                        "index": 0,
                        "url": "https://example.com/image.jpg",
                    }
                ]
            },
        },
    }
    
    with respx.mock(base_url=mock_client.base_url) as respx_mock:
        # First call: processing
        respx_mock.get(f"/v1/images/generations/{task_id}").mock(
            side_effect=[
                httpx.Response(200, json=processing_response),
                httpx.Response(200, json=completed_response),
            ]
        )
        
        # Call with short poll interval and timeout
        response = await mock_client.image_generation.wait_for_task_completion(
            task_id, poll_interval=0.1, timeout=1.0
        )
        
        # Verify the response
        assert response.data.task_status == TaskStatus.SUCCEEDED
        assert len(response.data.task_result.images) == 1
        assert response.data.task_result.images[0].url == "https://example.com/image.jpg"
        
        # Should have made 2 API calls
        assert respx_mock.calls.call_count == 2


@pytest.mark.asyncio
async def test_validation_error_handling(mock_client: KlingClient):
    """Test that validation errors are properly raised."""
    # Create an invalid request (missing required 'prompt' field)
    with pytest.raises(ValueError):
        ImageGenerationRequest()  # type: ignore
    
    # Test with invalid model name
    with pytest.raises(ValueError):
        ImageGenerationRequest(
            model_name="invalid-model",  # type: ignore
            prompt="test",
        )
    
    # Test with invalid aspect ratio
    with pytest.raises(ValueError):
        ImageGenerationRequest(
            prompt="test",
            aspect_ratio="invalid-ratio",  # type: ignore
        )