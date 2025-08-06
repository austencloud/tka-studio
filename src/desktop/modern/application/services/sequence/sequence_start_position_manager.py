"""
SequenceStartPositionManager

Handles start position operations and management.
Responsible for setting, updating, and managing start positions in sequences.
"""

from __future__ import annotations

from abc import ABCMeta
from typing import TYPE_CHECKING, Optional

from PyQt6.QtCore import QObject, pyqtSignal
from shared.application.services.data.modern_to_legacy_converter import (
    ModernToLegacyConverter,
)
from shared.application.services.sequence.sequence_persister import SequencePersister

from desktop.modern.core.interfaces.sequence_data_services import (
    ISequenceStartPositionManager,
)
from desktop.modern.core.interfaces.workbench_services import IWorkbenchStateManager
from desktop.modern.domain.models.beat_data import BeatData


class QObjectABCMeta(type(QObject), ABCMeta):
    """Metaclass that combines QObject's metaclass with ABCMeta."""


if TYPE_CHECKING:
    pass


class SequenceStartPositionManager(
    QObject, ISequenceStartPositionManager, metaclass=QObjectABCMeta
):
    """
    Service for managing start positions in sequences.

    Responsibilities:
    - Setting start positions
    - Converting start position data to legacy format
    - Managing start position persistence
    - Coordinating start position with workbench
    """

    start_position_set = pyqtSignal(object)  # BeatData object
    start_position_updated = pyqtSignal(object)  # BeatData object

    def __init__(
        self,
        workbench_state_manager: IWorkbenchStateManager,
    ):
        super().__init__()
        self.workbench_state_manager = workbench_state_manager
        self.modern_to_legacy_converter = ModernToLegacyConverter()
        self.persistence_service = SequencePersister()

    def set_start_position(self, start_position_beat_data: BeatData):
        """Set the start position - accepts both PictographData and BeatData"""
        # Create start position beat data using factory

        try:
            # Convert start position to legacy format and save as beat 0
            start_pos_legacy_dict = (
                self.modern_to_legacy_converter.convert_start_position_to_legacy_format(
                    start_position_beat_data
                )
            )

            # Load current sequence to preserve existing beats
            sequence = self.persistence_service.load_current_sequence()

            # Find where to insert/replace start position
            if len(sequence) == 1:  # Only metadata
                sequence.append(start_pos_legacy_dict)
            elif len(sequence) > 1 and sequence[1].get("beat") == 0:
                # Replace existing start position
                sequence[1] = start_pos_legacy_dict
            else:
                # Insert start position, shifting existing beats
                sequence.insert(1, start_pos_legacy_dict)

            # Save updated sequence (preserves existing beats)
            self.persistence_service.save_current_sequence(sequence)

            # Set start position in workbench via state manager
            if self.workbench_state_manager:
                self.workbench_state_manager.set_start_position(
                    start_position_beat_data
                )

            # Emit signal
            self.start_position_set.emit(start_position_beat_data)

        except Exception as e:
            print(f"❌ [START_POS_MGR] Failed to set start position: {e}")
            import traceback

            traceback.print_exc()

    def update_start_position_orientation(self, color: str, new_orientation: int):
        """Update start position orientation for a specific color"""
        try:
            # Get current start position via state manager
            start_position_data = self.workbench_state_manager.get_start_position()
            if not start_position_data:
                print("⚠️ No start position data available")
                return

            # Update the appropriate motion based on color
            if color.lower() == "blue" and start_position_data.blue_motion:
                updated_motion = start_position_data.blue_motion.update(
                    start_orientation=new_orientation, end_orientation=new_orientation
                )
                updated_start_position = start_position_data.update(
                    blue_motion=updated_motion
                )
            elif color.lower() == "red" and start_position_data.red_motion:
                updated_motion = start_position_data.red_motion.update(
                    start_orientation=new_orientation, end_orientation=new_orientation
                )
                updated_start_position = start_position_data.update(
                    red_motion=updated_motion
                )
            else:
                print(f"⚠️ Invalid color '{color}' or missing motion data")
                return

            # Update workbench via state manager
            if self.workbench_state_manager:
                self.workbench_state_manager.set_start_position(updated_start_position)

            # Update persistence
            self._update_start_position_in_persistence(updated_start_position)

            # Emit signal
            self.start_position_updated.emit(updated_start_position)

        except Exception as e:
            print(f"❌ Failed to update start position orientation: {e}")
            import traceback

            traceback.print_exc()

    def get_current_start_position(self) -> Optional[BeatData]:
        """Get the current start position from state manager"""
        try:
            return self.workbench_state_manager.get_start_position()
        except Exception as e:
            print(f"❌ Error getting current start position: {e}")
        return None

    def clear_start_position(self):
        """Clear the current start position"""
        try:
            # Clear from workbench via state manager
            if self.workbench_state_manager:
                self.workbench_state_manager.set_start_position(None)

            # Clear from persistence (only if sequence exists and has start position)
            sequence = self.persistence_service.load_current_sequence()
            if len(sequence) > 1 and sequence[1].get("beat") == 0:
                # Remove start position entry
                sequence.pop(1)
                self.persistence_service.save_current_sequence(sequence)

        except Exception as e:
            print(f"❌ [START_POS_MGR] Failed to clear start position: {e}")
            import traceback

            traceback.print_exc()

    def _update_start_position_in_persistence(self, start_position_data: BeatData):
        """Update start position in persistence"""
        try:
            # Convert to legacy format
            start_pos_dict = (
                self.modern_to_legacy_converter.convert_start_position_to_legacy_format(
                    start_position_data
                )
            )

            # Load current sequence
            sequence = self.persistence_service.load_current_sequence()

            # Update start position if it exists
            if len(sequence) > 1 and sequence[1].get("beat") == 0:
                sequence[1] = start_pos_dict
                self.persistence_service.save_current_sequence(sequence)
            else:
                print("⚠️ No start position found in persistence to update")

        except Exception as e:
            print(f"❌ Failed to update start position in persistence: {e}")
            import traceback

            traceback.print_exc()

    def has_start_position(self) -> bool:
        """Check if a start position is currently set"""
        try:
            start_position = self.workbench_state_manager.get_start_position()
            return start_position is not None
        except Exception as e:
            print(f"❌ Error checking start position: {e}")
        return False
