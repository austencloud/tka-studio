from __future__ import annotations

from collections.abc import Callable

from base_widgets.pictograph.legacy_pictograph import LegacyPictograph
from enums.letter.letter import Letter
from interfaces.json_manager_interface import IJsonManager
from interfaces.settings_manager_interface import ISettingsManager
from main_window.main_widget.fade_manager.fade_manager import FadeManager
from main_window.main_widget.sequence_workbench.legacy_beat_frame.legacy_beat_frame import (
    LegacyBeatFrame,
)
from PyQt6.QtCore import QSize, pyqtSignal
from PyQt6.QtWidgets import QFrame

from .add_to_sequence_manager.add_to_sequence_manager import AddToSequenceManager
from .advanced_start_pos_picker.advanced_start_pos_picker import AdvancedStartPosPicker
from .option_picker.widgets.legacy_option_picker import LegacyOptionPicker
from .start_pos_picker.start_pos_picker import StartPosPicker


class ConstructTab(QFrame):
    start_position_selected = pyqtSignal(object)

    start_pos_picker_index = 0
    advanced_start_pos_picker_index = 1
    option_picker_index = 2

    def __init__(
        self,
        beat_frame: LegacyBeatFrame,
        pictograph_dataset: dict,
        size_provider: Callable[[], QSize],
        fade_to_stack_index: Callable[[int], None],
        fade_manager: FadeManager,
        settings_manager: ISettingsManager,
        json_manager: IJsonManager,
    ) -> None:
        super().__init__()

        self.settings_manager = settings_manager
        self.json_manager = json_manager
        self.beat_frame = beat_frame
        self.pictograph_dataset = pictograph_dataset
        self.mw_size_provider = size_provider
        self.fade_to_stack_index = fade_to_stack_index
        self.fade_manager = fade_manager
        self.last_beat: LegacyPictograph = None
        self.start_position_picked = False

        self.pictograph_cache: dict[Letter, dict[str, LegacyPictograph]] = {
            letter: {} for letter in Letter
        }

        # In ConstructTab:
        self.add_to_sequence_manager = AddToSequenceManager(
            json_manager=self.json_manager,
            beat_frame=self.beat_frame,
            last_beat=lambda: self.last_beat,  # Use a getter function
            settings_manager=self.settings_manager,
        )

        self.option_picker = LegacyOptionPicker(
            add_to_sequence_manager=self.add_to_sequence_manager,
            pictograph_dataset=self.pictograph_dataset,
            beat_frame=self.beat_frame,
            mw_size_provider=self.mw_size_provider,
            fade_manager=self.fade_manager,
        )

        self.start_pos_picker = StartPosPicker(
            self.pictograph_dataset,
            self.beat_frame,
            self.mw_size_provider,
            advanced_transition_handler=self.transition_to_advanced_start_pos_picker,
        )
        self.advanced_start_pos_picker = AdvancedStartPosPicker(
            self.pictograph_dataset, self.beat_frame, self.mw_size_provider
        )

        # Connect signals for automatic transitions
        self._connect_signals()

    def _connect_signals(self) -> None:
        """Connect signals for automatic transitions between pickers."""
        # Connect start position picker signal to transition to option picker
        self.start_pos_picker.start_position_selected.connect(
            self._handle_start_position_selected
        )

        # Connect advanced start position picker signal if it has one
        if hasattr(self.advanced_start_pos_picker, "start_position_selected"):
            self.advanced_start_pos_picker.start_position_selected.connect(
                self._handle_start_position_selected
            )

    def _handle_start_position_selected(self, pictograph: LegacyPictograph) -> None:
        """Handle start position selection and transition to option picker."""
        import logging

        logger = logging.getLogger(__name__)
        logger.info(f"Start position selected: {pictograph}")

        # Mark that a start position has been picked
        self.start_position_picked = True

        # Emit the construct tab's signal
        self.start_position_selected.emit(pictograph)

        # Automatically transition to option picker
        self.transition_to_option_picker()

        # Prepare the option picker with the start position
        if hasattr(self.option_picker, "prepare_from_start_position"):
            self.option_picker.prepare_from_start_position(pictograph)

    def transition_to_option_picker(self):
        """Transition to the option picker view."""
        self.fade_to_stack_index(self.option_picker_index)

    def transition_to_advanced_start_pos_picker(self) -> None:
        """Transition to the advanced start position picker."""
        self.fade_to_stack_index(self.advanced_start_pos_picker_index)
        self.advanced_start_pos_picker.display_variations()

    def transition_to_start_pos_picker(self) -> None:
        """Reset the view back to the start position picker."""
        self.fade_to_stack_index(self.start_pos_picker_index)
