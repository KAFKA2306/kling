"""Base models for Kling API."""
from pydantic import BaseModel, ConfigDict


class KlingAPIBaseModel(BaseModel):
    """Base model for all Kling API models."""
    
    model_config = ConfigDict(
        extra="allow",
        populate_by_name=True,
    )
