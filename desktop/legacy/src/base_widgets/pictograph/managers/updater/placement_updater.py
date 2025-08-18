from __future__ import annotations
import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...legacy_pictograph import LegacyPictograph

logger = logging.getLogger(__name__)


class PlacementUpdater:
    def __init__(self, pictograph: "LegacyPictograph") -> None:
        self.pictograph = pictograph

    def update(self) -> None:
        """
        Updates the layout by repositioning props and arrows and refreshing the scene.
        """
        try:
            self.pictograph.managers.prop_placement_manager.update_prop_positions()
            self.pictograph.managers.arrow_placement_manager.update_arrow_placements()
            self.pictograph.update()
            logger.debug("Layout updated successfully.")
        except Exception as e:
            logger.error(f"Error updating layout: {e}", exc_info=True)
