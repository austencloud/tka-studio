"""
StartPositionHandler

Manages start position selection, data creation, and related operations for the construct tab.
Responsible for handling start position picker interactions and creating start position data.
"""

from __future__ import annotations

from PyQt6.QtCore import QObject, pyqtSignal
from shared.application.services.data.conversion_utils import (
    extract_end_position_from_position_key,
)
from shared.application.services.sequence.beat_factory import BeatFactory

from desktop.modern.domain.models.grid_data import GridData
from desktop.modern.domain.models.pictograph_data import PictographData


class StartPositionSelectionHandler(QObject):
    """
    Handles start position selection and data creation.

    Responsibilities:
    - Processing start position selection events
    - Creating start position data from position keys
    - Managing start position to option picker transitions
    - Integrating with the pictograph dataset service

    Signals:
    - start_position_created: Emitted when start position data is created
    - transition_requested: Emitted when transition to option picker is needed
    """

    start_position_created = pyqtSignal(str, object)  # position_key, PictographData
    transition_requested = pyqtSignal()  # Request transition to option picker

    def __init__(self):
        """Initialize start position selection handler using modern state manager architecture."""
        super().__init__()
        # Modern architecture: No direct workbench setter needed
        # Signal flow: handler -> SignalCoordinator -> StartPositionManager -> WorkbenchStateManager

    def handle_start_position_selected(self, position_key: str):
        """Handle start position selection from the picker"""
        # Removed repetitive debug logs

        # Create start position data (separate from sequence like Legacy)
        # Removed repetitive debug logs
        start_position_pictograph_data = self._create_start_position_pictograph_data(
            position_key
        )

        # Create start position beat data using factory (always create it)
        start_position_beat_data = BeatFactory.create_start_position_beat_data(
            start_position_pictograph_data
        )

        # MODERN ARCHITECTURE: No direct workbench setter needed
        # The signal flow will handle workbench updates:
        # start_position_created signal -> SignalCoordinator -> StartPositionManager -> WorkbenchStateManager
        print(
            "🏗️ [START_POS_HANDLER] Using modern signal flow (no direct workbench setter)"
        )

        # Emit signal with the created data
        print(
            f"🎯 [START_POS_HANDLER] Emitting start_position_created signal with position: {position_key}"
        )
        self.start_position_created.emit(position_key, start_position_beat_data)

        # Request transition to option picker
        print("🎯 [START_POS_HANDLER] Emitting transition_requested signal")
        self.transition_requested.emit()

    def _create_start_position_pictograph_data(
        self, position_key: str
    ) -> PictographData:
        """Create start position data from position key using real dataset (separate from sequence beats)"""
        try:
            # Use dependency injection to get shared services
            from shared.application.services.data.dataset_query import IDatasetQuery

            from desktop.modern.core.dependency_injection.di_container import (
                get_container,
            )

            container = get_container()
            dataset_service = container.resolve(IDatasetQuery)
            # Get real start position data from dataset as PictographData
            real_start_position_pictograph = (
                dataset_service.get_start_position_pictograph_data(
                    position_key, "diamond"
                )
            )

            if real_start_position_pictograph:
                # Extract the specific end position from position_key (like "gamma13")
                specific_end_pos = extract_end_position_from_position_key(position_key)

                # Update the pictograph data with correct position information
                pictograph_data = real_start_position_pictograph.update(
                    start_position=position_key,
                    end_position=specific_end_pos,
                    metadata={"source": "start_position_selection"},
                )

                return pictograph_data
            print(f"⚠️ No real data found for position {position_key}, using fallback")
            # Fallback start position as PictographData
            specific_end_pos = extract_end_position_from_position_key(position_key)

            return self._create_fallback_pictograph_data(position_key, specific_end_pos)

        except Exception as e:
            print(f"❌ Error loading real start position data: {e}")
            import traceback

            traceback.print_exc()

            # Fallback to basic pictograph data with position info
            try:
                specific_end_pos = self.extract_end_position_from_position_key(
                    position_key
                )
            except Exception:
                specific_end_pos = position_key  # Last resort fallback

            return self._create_fallback_pictograph_data(position_key, specific_end_pos)

    def _create_fallback_pictograph_data(
        self, position_key: str, specific_end_pos: str
    ) -> PictographData:
        """Create fallback PictographData when dataset lookup fails."""

        return PictographData(
            letter=position_key,
            start_position=position_key,
            end_position=specific_end_pos,
            grid_data=GridData(),  # Default grid data
            arrows={},  # Empty arrows for fallback
            props={},  # Empty props for fallback
            is_blank=False,
            metadata={"source": "fallback_start_position"},
        )
