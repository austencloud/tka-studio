"""
Middleware configuration for TKA API.
Handles CORS, logging, performance monitoring, and other cross-cutting concerns.
"""

import logging
import time
from typing import Callable
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging HTTP requests and responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Log request details and response information.

        Args:
            request: The incoming HTTP request
            call_next: The next middleware or endpoint handler

        Returns:
            Response: The HTTP response
        """
        start_time = time.time()

        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path} - "
            f"Client: {request.client.host if request.client else 'unknown'}"
        )

        # Process request
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response
        logger.info(
            f"Response: {response.status_code} - "
            f"Time: {process_time:.3f}s - "
            f"Path: {request.url.path}"
        )

        # Add processing time header
        response.headers["X-Process-Time"] = str(process_time)

        return response


class PerformanceMonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware for monitoring API performance."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Monitor request performance and add metrics.

        Args:
            request: The incoming HTTP request
            call_next: The next middleware or endpoint handler

        Returns:
            Response: The HTTP response with performance headers
        """
        start_time = time.time()

        # Process request
        response = await call_next(request)

        # Calculate metrics
        process_time = time.time() - start_time

        # Add performance headers
        response.headers["X-Response-Time"] = f"{process_time:.3f}"
        response.headers["X-API-Version"] = "2.0.0"

        # Log slow requests (>1 second)
        if process_time > 1.0:
            logger.warning(
                f"Slow request detected: {request.method} {request.url.path} - "
                f"Time: {process_time:.3f}s"
            )

        return response


def configure_cors(app: FastAPI) -> None:
    """
    Configure CORS middleware for the FastAPI application.

    Args:
        app: The FastAPI application instance
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["X-Process-Time", "X-Response-Time", "X-API-Version"],
    )

    logger.info("CORS middleware configured")


def configure_request_logging(app: FastAPI) -> None:
    """
    Configure request logging middleware.

    Args:
        app: The FastAPI application instance
    """
    app.add_middleware(RequestLoggingMiddleware)
    logger.info("Request logging middleware configured")


def configure_performance_monitoring(app: FastAPI) -> None:
    """
    Configure performance monitoring middleware.

    Args:
        app: The FastAPI application instance
    """
    app.add_middleware(PerformanceMonitoringMiddleware)
    logger.info("Performance monitoring middleware configured")


def configure_all_middleware(app: FastAPI) -> None:
    """
    Configure all middleware for the FastAPI application.

    Args:
        app: The FastAPI application instance
    """
    # Order matters - add in reverse order of execution
    configure_performance_monitoring(app)
    configure_request_logging(app)
    configure_cors(app)

    logger.info("All middleware configured successfully")
