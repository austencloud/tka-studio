"""
StartPositionHandler

Manages start position selection, data creation, and related operations for the construct tab.
Responsible for handling start position picker interactions and creating start position data.
"""

from typing import Callable, Optional

from domain.models import BeatData
from PyQt6.QtCore import QObject, pyqtSignal

from .data_conversion_service import DataConversionService


class StartPositionHandler(QObject):
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

    start_position_created = pyqtSignal(str, object)  # position_key, BeatData
    transition_requested = pyqtSignal()  # Request transition to option picker

    def __init__(
        self,
        data_conversion_service: DataConversionService,
        workbench_setter: Optional[Callable[[BeatData], None]] = None,
    ):
        super().__init__()
        self.data_conversion_service = data_conversion_service
        self.workbench_setter = workbench_setter

    def handle_start_position_selected(self, position_key: str):
        """Handle start position selection from the picker"""
        # Removed repetitive debug logs
        print(f"✅ Start position handler: Position selected: {position_key}")

        # Create start position data (separate from sequence like Legacy)
        # Removed repetitive debug logs
        start_position_data = self._create_start_position_data(position_key)
        print(
            f"✅ [START_POS_HANDLER] Created start position data: {start_position_data.letter if start_position_data else 'None'}"
        )

        # Set start position in workbench (this does NOT create a sequence)
        if self.workbench_setter:
            # Removed repetitive debug logs
            self.workbench_setter(start_position_data)
            print(f"✅ [START_POS_HANDLER] Set in workbench")
        else:
            print(f"⚠️ [START_POS_HANDLER] No workbench setter available")

        # Emit signal with the created data
        # Removed repetitive debug logs
        self.start_position_created.emit(position_key, start_position_data)
        print(f"✅ [START_POS_HANDLER] start_position_created signal emitted")

        # Request transition to option picker
        # Removed repetitive debug logs
        self.transition_requested.emit()
        print(f"✅ [START_POS_HANDLER] transition_requested signal emitted")

    def _create_start_position_data(self, position_key: str) -> BeatData:
        """Create start position data from position key using real dataset (separate from sequence beats)"""
        try:
            from application.services.data.dataset_query_service import (
                DatasetQueryService,
            )
            from domain.models import GlyphData

            dataset_service = DatasetQueryService()
            # Get real start position data from dataset
            real_start_position = dataset_service.get_start_position_pictograph(
                position_key, "diamond"
            )

            if real_start_position:
                # Extract the specific end position from position_key (like "gamma13")
                specific_end_pos = (
                    self.data_conversion_service.extract_end_position_from_position_key(
                        position_key
                    )
                )

                # Create proper glyph data with the specific position
                glyph_data = GlyphData(
                    start_position=position_key,  # The selected position key
                    end_position=specific_end_pos,  # The specific end position like "gamma13"
                )

                # Update the beat data with proper glyph data and position info
                beat_data = real_start_position.update(
                    beat_number=0,  # Start position is beat 0 in persistence
                    duration=1.0,  # Standard duration
                    glyph_data=glyph_data,  # Add the position data
                )

                print(
                    f"🎯 Created start position data: {position_key} -> {specific_end_pos}"
                )
                return beat_data
            else:
                print(
                    f"⚠️ No real data found for position {position_key}, using fallback"
                )
                # Fallback start position with proper glyph data
                specific_end_pos = (
                    self.data_conversion_service.extract_end_position_from_position_key(
                        position_key
                    )
                )

                glyph_data = GlyphData(
                    start_position=position_key,
                    end_position=specific_end_pos,
                )

                fallback_beat = BeatData.empty().update(
                    letter=position_key,
                    beat_number=0,
                    duration=1.0,
                    glyph_data=glyph_data,
                    is_blank=False,
                )

                return fallback_beat

        except Exception as e:
            print(f"❌ Error loading real start position data: {e}")
            import traceback

            traceback.print_exc()

            # Fallback to basic beat data with position info
            try:
                specific_end_pos = (
                    self.data_conversion_service.extract_end_position_from_position_key(
                        position_key
                    )
                )
            except Exception:
                specific_end_pos = position_key  # Last resort fallback

            glyph_data = GlyphData(
                start_position=position_key,
                end_position=specific_end_pos,
            )

            fallback_beat = BeatData.empty().update(
                letter=position_key,
                beat_number=0,
                duration=1.0,
                glyph_data=glyph_data,
                is_blank=False,
            )

            return fallback_beat
