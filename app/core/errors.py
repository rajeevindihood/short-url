from typing import Any, Dict, Optional, Tuple

import pydantic


class GenericError(Exception):
    """Base class for all CanPe application exceptions"""

    def __init__(
        self, message: str, code: str, http_status=500, data: Optional[Dict] = None
    ):
        self.message = message
        self.http_status = http_status
        self.code = code
        self.data = data

    def get_error_params(self) -> Tuple[int, str, Optional[str], Optional[Any]]:
        """Return params required to generate an HTTP Error response from this error"""
        return self.http_status, self.code, self.message, self.data


class ResourceNotFoundError(GenericError):
    """
    Raised when an expected resource is not found in db/cache/...

    Attributes:
        message: explanation of what resource is not found and for which query params
        resource_cls: the class of the resouce
    """

    def __init__(self, message: str, resource_cls: Optional[Any] = None):
        super().__init__(message, "RESOURCE_NOT_FOUND", 404)
        self.resource_cls = resource_cls


class MalformedDataError(GenericError):
    """
    Raised when an expected resource is not found in db/cache/...

    Attributes:
        message: explanation of what resource is not found and for which query params
        err: a pydantic validation error
    """

    def __init__(self, message: str, err: Optional[pydantic.ValidationError] = None):
        super().__init__(message, "MALFORMED_DATA", 422)
        self.err = err


class ExpiredDataError(GenericError):
    """
    Raised when an expected resource has been deleted or expired

    Attributes:
        message: explanation of what resource is no longer available
        err: a pydantic validation error
    """

    def __init__(self, message: str, err: Optional[pydantic.ValidationError] = None):
        super().__init__(message, "EXPIRED_DATA", 410)
        self.err = err
