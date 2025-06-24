# Modern Domain Module

# Export models for easy importing
from .models import *

__all__ = [
    # Re-export everything from models
] + getattr(__import__('domain.models', fromlist=['__all__']), '__all__', [])
