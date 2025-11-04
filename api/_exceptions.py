"""Base exceptions for Kling API."""


class KlingAPIError(Exception):
    """Base exception for Kling API errors."""
    
    def __init__(self, message: str, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)
