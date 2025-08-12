"""JSON serialization for domain models."""
import json
from typing import Any, Type, TypeVar, Dict
from dataclasses import is_dataclass
from enum import Enum
from .camel_case import dataclass_to_camel_dict, dict_from_camel_case

T = TypeVar('T')

class DomainJSONEncoder(json.JSONEncoder):
    """JSON encoder that handles domain models with camelCase output."""
    
    def default(self, obj: Any) -> Any:
        if is_dataclass(obj):
            return dataclass_to_camel_dict(obj)
        elif isinstance(obj, Enum):
            return obj.value
        return super().default(obj)

def domain_model_to_json(obj: Any, **kwargs) -> str:
    """Serialize domain model to camelCase JSON."""
    kwargs.setdefault('cls', DomainJSONEncoder)
    kwargs.setdefault('indent', 2)
    return json.dumps(obj, **kwargs)

def domain_model_from_json(json_str: str, model_class: Type[T]) -> T:
    """Deserialize camelCase JSON to domain model."""
    data = json.loads(json_str)
    snake_case_data = dict_from_camel_case(data)
    return model_class.from_dict(snake_case_data)
