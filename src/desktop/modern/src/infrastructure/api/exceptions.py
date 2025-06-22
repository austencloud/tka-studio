"""
Exception handling for TKA API.
Defines custom exceptions and error response models.
"""

import logging
from typing import Any, Dict, Optional
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class TKAAPIException(Exception):
    """Base exception for TKA API errors."""

    def __init__(
        self,
        message: str,
        error_code: str = "TKA_ERROR",
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)


class ServiceUnavailableError(TKAAPIException):
    """Raised when a required service is unavailable."""

    def __init__(self, service_name: str, details: Optional[Dict[str, Any]] = None):
        message = f"{service_name} service is unavailable"
        super().__init__(message, "SERVICE_UNAVAILABLE", details)
        self.service_name = service_name


class ValidationError(TKAAPIException):
    """Raised when data validation fails."""

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, "VALIDATION_ERROR", details)
        self.field = field


class ConversionError(TKAAPIException):
    """Raised when data conversion between models fails."""

    def __init__(
        self,
        message: str,
        source_type: str,
        target_type: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, "CONVERSION_ERROR", details)
        self.source_type = source_type
        self.target_type = target_type


class ResourceNotFoundError(TKAAPIException):
    """Raised when a requested resource is not found."""

    def __init__(
        self,
        resource_type: str,
        resource_id: str,
        details: Optional[Dict[str, Any]] = None,
    ):
        message = f"{resource_type} with ID '{resource_id}' not found"
        super().__init__(message, "RESOURCE_NOT_FOUND", details)
        self.resource_type = resource_type
        self.resource_id = resource_id


class OperationError(TKAAPIException):
    """Raised when an operation fails."""

    def __init__(
        self, operation: str, message: str, details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            f"Operation '{operation}' failed: {message}", "OPERATION_ERROR", details
        )
        self.operation = operation


# Exception handlers for FastAPI


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle HTTP exceptions with proper logging and response formatting.

    Args:
        request: The FastAPI request object
        exc: The HTTP exception that was raised

    Returns:
        JSONResponse: Formatted error response
    """
    logger.warning(f"HTTP {exc.status_code}: {exc.detail} - Path: {request.url.path}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "path": str(request.url.path),
        },
    )


async def tka_api_exception_handler(
    request: Request, exc: TKAAPIException
) -> JSONResponse:
    """
    Handle TKA API specific exceptions.

    Args:
        request: The FastAPI request object
        exc: The TKA API exception that was raised

    Returns:
        JSONResponse: Formatted error response
    """
    status_code = 400  # Default to bad request

    # Map exception types to HTTP status codes
    if isinstance(exc, ServiceUnavailableError):
        status_code = 503
    elif isinstance(exc, ResourceNotFoundError):
        status_code = 404
    elif isinstance(exc, ValidationError):
        status_code = 422
    elif isinstance(exc, ConversionError):
        status_code = 400
    elif isinstance(exc, OperationError):
        status_code = 500

    logger.error(
        f"TKA API Error {status_code}: {exc.message} - Path: {request.url.path}"
    )

    return JSONResponse(
        status_code=status_code,
        content={
            "error": exc.message,
            "error_code": exc.error_code,
            "status_code": status_code,
            "path": str(request.url.path),
            "details": exc.details,
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle general exceptions with proper logging and response formatting.

    Args:
        request: The FastAPI request object
        exc: The general exception that was raised

    Returns:
        JSONResponse: Formatted error response
    """
    logger.error(
        f"Unhandled exception: {exc} - Path: {request.url.path}", exc_info=True
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "status_code": 500,
            "path": str(request.url.path),
        },
    )


def register_exception_handlers(app):
    """
    Register all exception handlers with the FastAPI app.

    Args:
        app: The FastAPI application instance
    """
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(TKAAPIException, tka_api_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)

    logger.info("Exception handlers registered successfully")
