"""
OptionPickerManager

Manages option picker initialization, population, and option selection for the construct tab.
Responsible for coordinating between the option picker component and sequence management.
"""

import time
from typing import Optional

from application.services.data.conversion_utils import (
    extract_end_position_from_position_key,
)
from domain.models.beat_data import BeatData
from domain.models.pictograph_data import PictographData
from domain.models.sequence_data import SequenceData
from presentation.components.option_picker.components.option_picker import OptionPicker
from PyQt6.QtCore import QObject, pyqtSignal


class OptionPickerManager(QObject):
    """
    Manages option picker operations and interactions.

    Responsibilities:
    - Handling option picker population from start positions
    - Managing option selection events
    - Refreshing options based on sequence state
    - Working exclusively with PictographData

    Signals:
    - pictograph_selected: Emitted when a pictograph option is selected
    """

    pictograph_selected = pyqtSignal(object)  # PictographData object

    def __init__(
        self,
        option_picker: Optional[OptionPicker],
    ):
        super().__init__()
        self.option_picker = option_picker

        self._last_refresh_sequence_id = None
        self._last_refresh_length = None

        if self.option_picker:
            self.option_picker.pictograph_selected.connect(
                self._handle_pictograph_selected
            )

    def populate_from_start_position(
        self, position_key: str, start_position_beat_data: BeatData
    ):
        """Populate option picker with valid motion combinations based on start position"""
        if self.option_picker is None:
            return

        try:
            # Create proper modern SequenceData with start position as beat 0
            from domain.models.beat_data import BeatData
            from domain.models.sequence_data import SequenceData

            # Ensure we have a valid end position
            pictograph_data = start_position_beat_data.pictograph_data
            end_position = pictograph_data.end_position
            if not end_position:
                end_position = extract_end_position_from_position_key(position_key)
                # Update the pictograph data with the extracted end position
                pictograph_data = pictograph_data.update(end_position=end_position)

            # Create beat data for the start position (beat 1)
            start_beat = BeatData(
                beat_number=1, pictograph_data=pictograph_data, is_blank=False
            )

            # Create modern sequence data
            sequence_data = SequenceData(
                beats=[start_beat], start_position=position_key
            )

            self.option_picker.load_motion_combinations(sequence_data)

        except Exception as e:
            print(
                f"❌ [OPTION_PICKER_MANAGER] Error populating from start position: {e}"
            )
            import traceback

            traceback.print_exc()

            if self.option_picker is not None:
                try:
                    self.option_picker.refresh_options()
                except Exception as fallback_error:
                    print(
                        f"❌ [OPTION_PICKER_MANAGER] Fallback refresh failed: {fallback_error}"
                    )

    def refresh_from_sequence(self, sequence: SequenceData):
        """Refresh option picker based on current sequence state - PURE Modern IMPLEMENTATION"""
        if not self.option_picker or not sequence or sequence.length == 0:
            return

        start_time = time.perf_counter()

        try:
            self.option_picker.refresh_options_from_modern_sequence(sequence)
            total_time = (time.perf_counter() - start_time) * 1000
        except Exception as e:
            import traceback

            traceback.print_exc()

    def _handle_pictograph_selected(self, pictograph_data: PictographData):
        """Handle pictograph data selection from option picker and forward the signal"""
        self.pictograph_selected.emit(pictograph_data)

    def is_available(self) -> bool:
        """Check if option picker is available and functional"""
        return self.option_picker is not None
