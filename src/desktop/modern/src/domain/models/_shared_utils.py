"""
Shared utilities for domain model serialization.

This module contains common functions used across all domain models
to avoid code duplication and ensure consistency.
"""
from __future__ import annotations

from dataclasses import fields, is_dataclass
from enum import Enum
import json
from typing import Any, Union


def process_field_value(value: Any, field_type: Any) -> Any:
    """
    Process field value based on type for deserialization.

    Handles:
    - Optional types (Union[T, None])
    - Nested dataclasses
    - Enums
    - Lists with typed elements

    Args:
        value: The value to process
        field_type: The expected type for the field

    Returns:
        The processed value with correct type
    """
    # Handle Optional types
    if hasattr(field_type, '__origin__') and field_type.__origin__ is Union:
        args = field_type.__args__
        if len(args) == 2 and type(None) in args:
            actual_type = args[0] if args[1] is type(None) else args[1]
            if value is None:
                return None
            return process_field_value(value, actual_type)

    # Handle dataclasses
    if is_dataclass(field_type) and isinstance(value, dict):
        return field_type.from_dict(value)

    # Handle enums
    if isinstance(field_type, type) and issubclass(field_type, Enum):
        return field_type(value)

    # Handle lists
    if hasattr(field_type, '__origin__') and field_type.__origin__ is list:
        if isinstance(value, list):
            list_type = field_type.__args__[0]
            return [process_field_value(item, list_type) for item in value]

    return value


def add_serialization_methods(cls):
    """
    Class decorator to add standard serialization methods to dataclasses.

    Adds:
    - to_dict() - Snake_case dictionary
    - to_camel_dict() - CamelCase dictionary
    - to_json() - JSON serialization
    - from_dict() - Dictionary deserialization
    - from_json() - JSON deserialization

    Usage:
        @add_serialization_methods
        @dataclass(frozen=True)
        class MyModel:
            field: str
    """

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary with snake_case keys."""
        from dataclasses import asdict
        return asdict(self)

    def to_camel_dict(self) -> dict[str, Any]:
        """Convert to dictionary with camelCase keys for JSON APIs."""
        from ..serialization import dataclass_to_camel_dict
        return dataclass_to_camel_dict(self)

    def to_json(self, camel_case: bool = True, **kwargs) -> str:
        """Serialize to JSON string."""
        from ..serialization import domain_model_to_json
        if camel_case:
            return domain_model_to_json(self, **kwargs)
        return json.dumps(self.to_dict(), **kwargs)

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        """Create instance from dictionary."""
        # Handle nested dataclasses and enums
        field_types = {f.name: f.type for f in fields(cls)}

        processed_data = {}
        for key, value in data.items():
            if key in field_types:
                field_type = field_types[key]
                processed_data[key] = process_field_value(value, field_type)
            else:
                processed_data[key] = value

        return cls(**processed_data)

    @classmethod
    def from_json(cls, json_str: str, camel_case: bool = True):
        """Create instance from JSON string."""
        from ..serialization import domain_model_from_json
        if camel_case:
            return domain_model_from_json(json_str, cls)
        data = json.loads(json_str)
        return cls.from_dict(data)

    # Add methods to class
    cls.to_dict = to_dict
    cls.to_camel_dict = to_camel_dict
    cls.to_json = to_json
    cls.from_dict = from_dict
    cls.from_json = from_json

    return cls
