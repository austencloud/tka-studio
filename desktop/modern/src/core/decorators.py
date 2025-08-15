"""
Core decorators for TKA application services.

Provides common decorators for error handling, performance monitoring,
and service lifecycle management.
"""

from __future__ import annotations

import functools
import logging
from typing import Any, Callable, TypeVar


F = TypeVar("F", bound=Callable[..., Any])

logger = logging.getLogger(__name__)


def handle_service_errors(name_or_func=None):
    """
    Decorator to handle service errors gracefully.

    Can be used with or without parameters:
    @handle_service_errors
    @handle_service_errors("custom_operation_name")

    Catches exceptions in service methods and logs them appropriately,
    preventing crashes while maintaining error visibility.
    """

    def decorator(func: F) -> F:
        # Determine the name to use for logging
        if isinstance(name_or_func, str):
            operation_name = name_or_func
        else:
            operation_name = func.__name__

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.exception(f"Service error in {operation_name}: {e}")
                # Return appropriate default based on return type annotation
                if hasattr(func, "__annotations__"):
                    return_type = func.__annotations__.get("return")
                    if return_type is not None:
                        if return_type == bool:
                            return False
                        elif return_type == list:
                            return []
                        elif return_type == dict:
                            return {}
                        elif return_type == str:
                            return ""
                        elif return_type == int:
                            return 0
                        elif return_type == float:
                            return 0.0
                return None

        return wrapper

    # Handle both @handle_service_errors and @handle_service_errors("name") usage
    if callable(name_or_func):
        # Used as @handle_service_errors (without parentheses)
        return decorator(name_or_func)
    else:
        # Used as @handle_service_errors("name") (with parentheses)
        return decorator


def retry_on_failure(max_retries: int = 3, delay: float = 0.1):
    """
    Decorator to retry function calls on failure.

    Args:
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}: {e}"
                        )
                        import time

                        time.sleep(delay)
                    else:
                        logger.error(
                            f"All {max_retries + 1} attempts failed for {func.__name__}"
                        )

            # Re-raise the last exception if all retries failed
            raise last_exception

        return wrapper

    return decorator


def validate_arguments(**validators):
    """
    Decorator to validate function arguments.

    Args:
        **validators: Mapping of argument names to validation functions
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Get function signature
            import inspect

            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()

            # Validate arguments
            for arg_name, validator in validators.items():
                if arg_name in bound_args.arguments:
                    value = bound_args.arguments[arg_name]
                    if not validator(value):
                        raise ValueError(f"Invalid value for {arg_name}: {value}")

            return func(*args, **kwargs)

        return wrapper

    return decorator


def cache_result(ttl_seconds: int = 300):
    """
    Decorator to cache function results for a specified time.

    Args:
        ttl_seconds: Time to live for cached results in seconds
    """

    def decorator(func: F) -> F:
        cache = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import hashlib
            import pickle
            import time

            # Create cache key from arguments
            key_data = pickle.dumps((args, sorted(kwargs.items())))
            cache_key = hashlib.md5(key_data).hexdigest()

            current_time = time.time()

            # Check if we have a valid cached result
            if cache_key in cache:
                result, timestamp = cache[cache_key]
                if current_time - timestamp < ttl_seconds:
                    return result

            # Compute new result and cache it
            result = func(*args, **kwargs)
            cache[cache_key] = (result, current_time)

            # Clean up old cache entries
            expired_keys = [
                key
                for key, (_, timestamp) in cache.items()
                if current_time - timestamp >= ttl_seconds
            ]
            for key in expired_keys:
                del cache[key]

            return result

        return wrapper

    return decorator


def log_execution_time(func: F) -> F:
    """
    Decorator to log function execution time.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import time

        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            return result
        finally:
            end_time = time.perf_counter()
            execution_time = (end_time - start_time) * 1000  # Convert to milliseconds
            logger.debug(f"{func.__name__} executed in {execution_time:.2f}ms")

    return wrapper


def singleton(cls):
    """
    Decorator to make a class a singleton.
    """
    instances = {}

    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def deprecated(reason: str = ""):
    """
    Decorator to mark functions as deprecated.

    Args:
        reason: Reason for deprecation
    """

    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import warnings

            message = f"{func.__name__} is deprecated"
            if reason:
                message += f": {reason}"
            warnings.warn(message, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper

    return decorator
