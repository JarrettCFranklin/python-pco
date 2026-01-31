"""Custom exceptions for PCO API wrapper."""


class PCOError(Exception):
    """Base exception for all PCO API errors."""

    pass


class PCOAuthError(PCOError):
    """Exception raised for authentication errors."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class PCOAPIError(PCOError):
    """Exception raised for API errors."""

    def __init__(self, message: str, status_code: int | None = None, response_data: dict | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class PCONotFoundError(PCOAPIError):
    """Exception raised when a resource is not found (404)."""

    def __init__(self, message: str = "Resource not found", response_data: dict | None = None):
        super().__init__(message, status_code=404, response_data=response_data)


class PCORateLimitError(PCOAPIError):
    """Exception raised when rate limit is exceeded."""

    def __init__(self, message: str = "Rate limit exceeded", response_data: dict | None = None):
        super().__init__(message, status_code=429, response_data=response_data)


class PCOValidationError(PCOAPIError):
    """Exception raised for validation errors (400)."""

    def __init__(self, message: str, response_data: dict | None = None):
        super().__init__(message, status_code=400, response_data=response_data)
