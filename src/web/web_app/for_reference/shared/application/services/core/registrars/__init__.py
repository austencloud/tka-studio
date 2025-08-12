"""
Service Registrars for Framework-Agnostic Services

This module contains all service registrars that handle dependency injection
for framework-agnostic services that can be used across desktop and web platforms.
"""

from .animation_service_registrar import AnimationServiceRegistrar
from .core_service_registrar import CoreServiceRegistrar
from .data_service_registrar import DataServiceRegistrar
from .generation_service_registrar import GenerationServiceRegistrar
from .graph_editor_service_registrar import GraphEditorServiceRegistrar
from .learn_service_registrar import LearnServiceRegistrar
from .motion_service_registrar import MotionServiceRegistrar
from .sequence_card_service_registrar import SequenceCardServiceRegistrar
from .option_picker_service_registrar import OptionPickerServiceRegistrar
from .pictograph_service_registrar import PictographServiceRegistrar
from .positioning_service_registrar import PositioningServiceRegistrar
from .sequence_service_registrar import SequenceServiceRegistrar
from .start_position_service_registrar import StartPositionServiceRegistrar
from .workbench_service_registrar import WorkbenchServiceRegistrar
from .write_service_registrar import WriteServiceRegistrar

__all__ = [
    "AnimationServiceRegistrar",
    "CoreServiceRegistrar",
    "DataServiceRegistrar",
    "GenerationServiceRegistrar",
    "GraphEditorServiceRegistrar",
    "LearnServiceRegistrar",
    "MotionServiceRegistrar",
    "SequenceCardServiceRegistrar",
    "OptionPickerServiceRegistrar",
    "PictographServiceRegistrar",
    "PositioningServiceRegistrar",
    "SequenceServiceRegistrar",
    "StartPositionServiceRegistrar",
    "WorkbenchServiceRegistrar",
    "WriteServiceRegistrar",
]
