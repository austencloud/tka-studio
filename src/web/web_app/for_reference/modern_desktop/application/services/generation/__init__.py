"""
Generation Services Package

Simplified generation system using practical generators:
- Main generation orchestration (GenerationService)
- Freeform generator (core/freeform_generator.py)
- Circular generator (core/circular_generator.py)
- Data management and filtering (core/data_and_filtering.py)
- Turn application (core/turn_applicator.py)
- Workbench integration (core/workbench_integration.py)

This package provides clean, focused generation functionality without over-engineering.
"""

from __future__ import annotations

from .generation_service import GenerationService
from .generation_service_registration import (
    GenerationServiceRegistrationHelper,
    register_generation_services,
)


__all__ = [
    "GenerationService",
    "GenerationServiceRegistrationHelper",
    "register_generation_services",
]
