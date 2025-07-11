"""
OptionPickerManager

Manages option picker initialization, population, and option selection for the construct tab.
Responsible for coordinating between the option picker component and sequence management.
"""

import time
from typing import Optional

from application.services.data.data_converter import DataConverter
from domain.models.pictograph_models import PictographData
from domain.models.sequence_models import SequenceData
from presentation.components.option_picker.core.option_picker import OptionPicker
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
        data_conversion_service: DataConverter,
    ):
        super().__init__()
        self.option_picker = option_picker
        self.data_conversion_service = data_conversion_service

        self._last_refresh_sequence_id = None
        self._last_refresh_length = None

        if self.option_picker:
            self.option_picker.pictograph_selected.connect(
                self._handle_pictograph_selected
            )

    def populate_from_start_position(
        self, position_key: str, start_position_data: PictographData
    ):
        """Populate option picker with valid motion combinations based on start position"""
        if self.option_picker is None:
            return

        try:
            print(
                f"🔄 [OPTION_PICKER_MANAGER] Populating from start position: {position_key}"
            )
            print(
                f"📊 [OPTION_PICKER_MANAGER] Start position data: letter={start_position_data.letter}, start_pos={start_position_data.start_position}, end_pos={start_position_data.end_position}"
            )

            # Convert PictographData to legacy format for compatibility
            start_position_dict = {
                "letter": start_position_data.letter,
                "start_pos": start_position_data.start_position,
                "end_pos": start_position_data.end_position,
                # Add other necessary fields from pictograph data
            }

            # Ensure we have a valid end position for option filtering
            if not start_position_dict.get("end_pos"):
                extracted_end_pos = (
                    self.data_conversion_service.extract_end_position_from_position_key(
                        position_key
                    )
                )
                start_position_dict["end_pos"] = extracted_end_pos
                print(
                    f"🔧 [OPTION_PICKER_MANAGER] Extracted end position: {extracted_end_pos}"
                )

            sequence_data = [
                {"metadata": "sequence_info"},
                start_position_dict,
            ]

            print(
                f"📤 [OPTION_PICKER_MANAGER] Loading motion combinations with sequence_data: {sequence_data}"
            )
            self.option_picker.load_motion_combinations(sequence_data)
            print(f"✅ [OPTION_PICKER_MANAGER] Motion combinations loaded successfully")

        except Exception as e:
            print(
                f"❌ [OPTION_PICKER_MANAGER] Error populating from start position: {e}"
            )
            import traceback

            traceback.print_exc()

            if self.option_picker is not None:
                try:
                    print(f"🔄 [OPTION_PICKER_MANAGER] Attempting fallback refresh...")
                    self.option_picker.refresh_options()
                    print(f"✅ [OPTION_PICKER_MANAGER] Fallback refresh completed")
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
            print(f"⚡ Option picker refreshed: {total_time:.1f}ms")
        except Exception as e:
            import traceback

            traceback.print_exc()

    def _handle_pictograph_selected(self, pictograph_data: PictographData):
        """Handle pictograph data selection from option picker and forward the signal"""
        self.pictograph_selected.emit(pictograph_data)

    def is_available(self) -> bool:
        """Check if option picker is available and functional"""
        return self.option_picker is not None
