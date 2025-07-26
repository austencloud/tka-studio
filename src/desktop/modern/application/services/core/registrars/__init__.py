"""
Service Registrars Package

Contains specialized service registrars following microservices architecture.
Each registrar handles registration for a specific service domain.

Registrars:
- MotionServiceRegistrar: Motion and orientation services
- GraphEditorServiceRegistrar: Graph editor state management
- CoreServiceRegistrar: Core application services
- DataServiceRegistrar: Data management and conversion services
- SequenceServiceRegistrar: Sequence operations and management
- PictographServiceRegistrar: Pictograph management services
- PositioningServiceRegistrar: Arrow and prop positioning services
- OptionPickerServiceRegistrar: Option picker services and components
- WorkbenchServiceRegistrar: Workbench business and presentation services
- LearnServiceRegistrar: Learn Tab services and components
"""

from .animation_service_registrar import AnimationServiceRegistrar
from .core_service_registrar import CoreServiceRegistrar
from .data_service_registrar import DataServiceRegistrar
from .event_system_registrar import EventSystemRegistrar
from .graph_editor_service_registrar import GraphEditorServiceRegistrar
from .learn_service_registrar import LearnServiceRegistrar
from .motion_service_registrar import MotionServiceRegistrar
from .option_picker_service_registrar import OptionPickerServiceRegistrar
from .pictograph_service_registrar import PictographServiceRegistrar
from .positioning_service_registrar import PositioningServiceRegistrar
from .sequence_service_registrar import SequenceServiceRegistrar
from .start_position_service_registrar import StartPositionServiceRegistrar
from .workbench_service_registrar import WorkbenchServiceRegistrar

__all__ = [
    "AnimationServiceRegistrar",
    "MotionServiceRegistrar",
    "GraphEditorServiceRegistrar",
    "DataServiceRegistrar",
    "CoreServiceRegistrar",
    "SequenceServiceRegistrar",
    "PictographServiceRegistrar",
    "EventSystemRegistrar",
    "PositioningServiceRegistrar",
    "OptionPickerServiceRegistrar",
    "WorkbenchServiceRegistrar",
    "StartPositionServiceRegistrar",
    "LearnServiceRegistrar",
]
