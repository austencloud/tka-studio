"""
Application lifecycle management for TKA API.
Handles startup and shutdown events.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from .dependencies import initialize_services, cleanup_services

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage the application lifespan with proper startup and shutdown handling.

    Args:
        app: The FastAPI application instance
    """
    # Startup
    logger.info("Starting TKA Desktop Production API...")
    try:
        await startup_event()
        logger.info("TKA Desktop Production API started successfully")
        yield
    except Exception as e:
        logger.error(f"Failed to start API: {e}")
        raise
    finally:
        # Shutdown
        logger.info("Shutting down TKA Desktop Production API...")
        try:
            await shutdown_event()
            logger.info("TKA Desktop Production API shutdown complete")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")


async def startup_event():
    """
    Handle application startup tasks.

    This function is called when the FastAPI application starts up.
    It initializes all required services and dependencies.

    Raises:
        Exception: If startup tasks fail
    """
    try:
        logger.info("Executing startup tasks...")

        # Initialize all services
        initialize_services()

        # Additional startup tasks can be added here
        # - Database connections
        # - Cache initialization
        # - External service health checks
        # - Configuration validation

        logger.info("Startup tasks completed successfully")

    except Exception as e:
        logger.error(f"Startup tasks failed: {e}")
        raise


async def shutdown_event():
    """
    Handle application shutdown tasks.

    This function is called when the FastAPI application shuts down.
    It performs cleanup tasks and closes resources gracefully.
    """
    try:
        logger.info("Executing shutdown tasks...")

        # Cleanup services
        cleanup_services()

        # Additional shutdown tasks can be added here
        # - Database connection cleanup
        # - Cache cleanup
        # - Background task cancellation
        # - Resource deallocation

        logger.info("Shutdown tasks completed successfully")

    except Exception as e:
        logger.error(f"Shutdown tasks failed: {e}")
        # Don't re-raise during shutdown to avoid masking other issues


def configure_lifecycle_events(app: FastAPI) -> None:
    """
    Configure lifecycle events for the FastAPI application.

    This is an alternative to the lifespan context manager for older
    FastAPI versions that don't support the lifespan parameter.

    Args:
        app: The FastAPI application instance
    """

    @app.on_event("startup")
    async def on_startup():
        """Handle startup event."""
        await startup_event()

    @app.on_event("shutdown")
    async def on_shutdown():
        """Handle shutdown event."""
        await shutdown_event()

    logger.info("Lifecycle events configured")
