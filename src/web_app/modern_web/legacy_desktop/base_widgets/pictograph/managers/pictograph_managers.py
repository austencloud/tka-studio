from __future__ import annotations
from typing import TYPE_CHECKING

from base_widgets.pictograph.managers.pictograph_data_copier import dictCopier
from placement_managers.arrow_placement_manager.arrow_placement_manager import (
    ArrowPlacementManager,
)
from placement_managers.prop_placement_manager.prop_placement_manager import (
    PropPlacementManager,
)
from svg_manager.svg_manager import SvgManager

from .getter.pictograph_getter import PictographGetter
from .pictograph_checker import PictographChecker
from .pictograph_initializer import PictographInitializer
from .updater.pictograph_updater import PictographUpdater

if TYPE_CHECKING:
    pass

from dataclasses import dataclass


@dataclass
class PictographManagers:
    """Stores all manager objects to handle logic separately."""

    arrow_placement_manager: "ArrowPlacementManager" = None
    prop_placement_manager: "PropPlacementManager" = None
    check: "PictographChecker" = None
    get: "PictographGetter" = None
    initializer: "PictographInitializer" = None
    updater: "PictographUpdater" = None
    svg_manager: "SvgManager" = None
    data_copier: "dictCopier" = None
