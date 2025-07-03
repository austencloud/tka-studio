from typing import Dict, Optional, Tuple, TYPE_CHECKING
from enum import Enum
from dataclasses import dataclass
import logging



# Event-driven architecture imports
if TYPE_CHECKING:
    from core.events import IEventBus

try:
    from core.events import (
        IEventBus,
        get_event_bus,
        EventPriority,
    )

    EVENT_SYSTEM_AVAILABLE = True
except ImportError:
    # For tests or when event system is not available
    IEventBus = None
    get_event_bus = None
    EventPriority = None
    EVENT_SYSTEM_AVAILABLE = False

try:
    from core.decorators import handle_service_errors
    from core.monitoring import monitor_performance
    from core.exceptions import ServiceOperationError, ValidationError
except ImportError:
    # For tests, create dummy decorators if imports fail
    def handle_service_errors(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    def monitor_performance(*args, **kwargs):
        def decorator(func):
            return func

        return decorator

    class ServiceOperationError(Exception):
        pass

    class ValidationError(Exception):
        pass


logger = logging.getLogger(__name__)


# ============================================================================
# SHARED ENUMS AND DATA CLASSES
# ============================================================================


class LayoutMode(Enum):
    """Layout modes for different contexts."""

    HORIZONTAL_SCROLL = "horizontal_scroll"
    VERTICAL_SCROLL = "vertical_scroll"
    GRID = "grid"
    FLOW = "flow"
    FIXED = "fixed"


class ScalingMode(Enum):
    """Scaling modes for responsive layouts."""

    FIT_WIDTH = "fit_width"
    FIT_HEIGHT = "fit_height"
    FIT_BOTH = "fit_both"
    MAINTAIN_ASPECT = "maintain_aspect"
    NO_SCALING = "no_scaling"


@dataclass
class LayoutConfig:
    """Configuration for layout calculations."""

    mode: LayoutMode = LayoutMode.HORIZONTAL_SCROLL
    scaling_mode: ScalingMode = ScalingMode.MAINTAIN_ASPECT
    padding: int = 10
    spacing: int = 5
    min_item_size: Tuple[int, int] = (100, 100)
    max_item_size: Tuple[int, int] = (300, 300)
    items_per_row: Optional[int] = None
    maintain_aspect_ratio: bool = True


@dataclass
class LayoutResult:
    """Result of layout calculations."""

    item_positions: Dict[str, Tuple[int, int]]
    item_sizes: Dict[str, Tuple[int, int]]
    total_size: Tuple[int, int]
    scaling_factor: float
    overflow: bool = False
