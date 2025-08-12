"""CamelCase conversion utilities for domain models."""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from enum import Enum
import re
from typing import Any


def to_camel_case(snake_str: str) -> str:
    """Convert snake_case to camelCase."""
    components = snake_str.split("_")
    return components[0] + "".join(word.capitalize() for word in components[1:])


def to_snake_case(camel_str: str) -> str:
    """Convert camelCase to snake_case."""
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", camel_str)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def dataclass_to_camel_dict(obj: Any) -> dict[str, Any]:
    """Convert dataclass to dict with camelCase keys."""
    if not is_dataclass(obj):
        raise ValueError("Object must be a dataclass")

    def convert_value(value: Any) -> Any:
        if is_dataclass(value):
            return dataclass_to_camel_dict(value)
        if isinstance(value, list):
            return [convert_value(item) for item in value]
        if isinstance(value, dict):
            return {to_camel_case(k): convert_value(v) for k, v in value.items()}
        if isinstance(value, Enum):
            return value.value
        return value

    result = {}
    for field in fields(obj):
        snake_name = field.name
        camel_name = to_camel_case(snake_name)
        value = getattr(obj, snake_name)
        result[camel_name] = convert_value(value)

    return result


def dict_from_camel_case(data: dict[str, Any]) -> dict[str, Any]:
    """Convert dict with camelCase keys to snake_case keys."""

    def convert_value(value: Any) -> Any:
        if isinstance(value, dict):
            return dict_from_camel_case(value)
        if isinstance(value, list):
            return [convert_value(item) for item in value]
        return value

    return {to_snake_case(k): convert_value(v) for k, v in data.items()}
