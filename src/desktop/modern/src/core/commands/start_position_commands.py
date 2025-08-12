"""
Start Position Commands for Event-Driven Architecture

Commands for handling start position operations with undo/redo support.
These replace the complex signal chains in the original architecture.
"""
from __future__ import annotations

from dataclasses import dataclass
import logging
from typing import Any
import uuid

from desktop.modern.core.commands.command_system import ICommand
from desktop.modern.domain.models.beat_data import BeatData


logger = logging.getLogger(__name__)


@dataclass
class SetStartPositionCommand(ICommand[BeatData]):
    """Command to set sequence start position with undo support"""

    position_key: str
    event_bus: Any  # IEventBus
    _command_id: str = ""
    _previous_position: BeatData | None = None
    _new_beat_data: BeatData | None = None

    def __post_init__(self):
        if not self._command_id:
            self._command_id = str(uuid.uuid4())

    @property
    def command_id(self) -> str:
        return self._command_id

    @property
    def description(self) -> str:
        return f"Set start position to '{self.position_key}'"

    def can_execute(self) -> bool:
        """Check if command can be executed"""
        return bool(self.position_key and self.event_bus)

    def can_undo(self) -> bool:
        """Check if command can be undone"""
        return self._new_beat_data is not None

    def execute(self) -> BeatData:
        """Execute: Set start position and save to persistence"""
        try:
            # Get current state manager to store previous position
            from desktop.modern.core.service_locator import get_sequence_state_manager

            state_manager = get_sequence_state_manager()
            if state_manager:
                self._previous_position = state_manager.get_start_position()

            # Create start position data using existing logic
            self._new_beat_data = self._create_start_position_data()

            if not self._new_beat_data:
                raise ValueError(
                    f"Failed to create start position data for {self.position_key}"
                )

            # Save to persistence
            self._save_to_persistence(self._new_beat_data)

            logger.info(f"✅ Start position set via command: {self.position_key}")
            return self._new_beat_data

        except Exception as e:
            logger.exception(f"❌ Error executing SetStartPositionCommand: {e}")
            raise

    def undo(self) -> BeatData | None:
        """Undo: Restore previous start position"""
        try:
            if self._previous_position:
                # Restore previous position
                self._save_to_persistence(self._previous_position)
                logger.info(
                    f"✅ Start position undone, restored: {self._previous_position.letter}"
                )
                return self._previous_position
            # Clear start position
            self._clear_from_persistence()
            logger.info("✅ Start position undone, cleared")
            return None

        except Exception as e:
            logger.exception(f"❌ Error undoing SetStartPositionCommand: {e}")
            raise

    def extract_end_position_from_position_key(self, position_key: str) -> str:
        """Extract the actual end position from a position key like 'beta5_beta5'"""
        # Position keys are in format "start_end", we want the end part
        if "_" in position_key:
            parts = position_key.split("_")
            if len(parts) == 2:
                return parts[1]  # Return the end position part

        # Fallback: if no underscore, assume it's already the position
        return position_key

    def _create_start_position_data(self) -> BeatData:
        """Create start position data using existing business logic"""
        try:
            # Use existing StartPositionHandler logic
            from desktop.modern.core.service_locator import get_data_conversion_service

            data_converter = get_data_conversion_service()

            if not data_converter:
                raise ValueError("Data conversion service not available")

            # Get the dataset query service
            from desktop.modern.application.services.data.dataset_query import (
                DatasetQuery,
            )
            from desktop.modern.domain.models.glyph_models import GlyphData

            dataset_service = DatasetQuery()

            # Get real start position data from dataset
            start_pos_beat_data = dataset_service.get_start_position_pictograph(
                self.position_key, "diamond"
            )

            if start_pos_beat_data and start_pos_beat_data.has_pictograph:
                # Extract the specific end position from position_key
                specific_end_pos = self.extract_end_position_from_position_key(
                    self.position_key
                )

                # Create proper glyph data with the specific position
                glyph_data = GlyphData(
                    start_position=self.position_key,
                    end_position=specific_end_pos,
                )

                # Update the embedded pictograph data with proper glyph data and position info
                updated_pictograph_data = start_pos_beat_data.pictograph_data.update(
                    glyph_data=glyph_data,
                )

                # Update the beat data with the updated pictograph
                start_pos_beat_data = start_pos_beat_data.update(
                    pictograph_data=updated_pictograph_data
                )

                return start_pos_beat_data

        except Exception as e:
            logger.exception(f"❌ Error creating start position data: {e}")
            raise

    def _save_to_persistence(self, beat_data: BeatData):
        """Save start position to persistence"""
        try:
            from desktop.modern.application.services.sequence.sequence_start_position_manager import (
                SequenceStartPositionManager,
            )

            start_position_manager = SequenceStartPositionManager()
            # Pass the beat data directly - it contains embedded pictograph
            start_position_manager.set_start_position(beat_data)

            logger.debug(f"💾 Start position saved to persistence: {beat_data.letter}")

        except Exception as e:
            logger.exception(f"❌ Error saving start position to persistence: {e}")
            raise

    def _clear_from_persistence(self):
        """Clear start position from persistence"""
        try:
            from desktop.modern.application.services.sequence.sequence_start_position_manager import (
                SequenceStartPositionManager,
            )

            start_position_manager = SequenceStartPositionManager()
            start_position_manager.clear_start_position()

        except Exception as e:
            logger.exception(f"❌ Error clearing start position from persistence: {e}")
            raise


@dataclass
class ClearStartPositionCommand(ICommand[None]):
    """Command to clear start position with undo support"""

    event_bus: Any  # IEventBus
    _command_id: str = ""
    _previous_position: BeatData | None = None

    def __post_init__(self):
        if not self._command_id:
            self._command_id = str(uuid.uuid4())

    @property
    def command_id(self) -> str:
        return self._command_id

    @property
    def description(self) -> str:
        return "Clear start position"

    def can_execute(self) -> bool:
        """Check if command can be executed"""
        return bool(self.event_bus)

    def can_undo(self) -> bool:
        """Check if command can be undone"""
        return self._previous_position is not None

    def execute(self) -> None:
        """Execute: Clear start position"""
        try:
            # Store previous position for undo
            from desktop.modern.core.service_locator import get_sequence_state_manager

            state_manager = get_sequence_state_manager()
            if state_manager:
                self._previous_position = state_manager.get_start_position()

            # Clear from persistence
            from desktop.modern.application.services.sequence.sequence_start_position_manager import (
                SequenceStartPositionManager,
            )

            start_position_manager = SequenceStartPositionManager()
            start_position_manager.clear_start_position()

            return

        except Exception as e:
            logger.exception(f"❌ Error executing ClearStartPositionCommand: {e}")
            raise

    def undo(self) -> None:
        """Undo: Restore previous start position"""
        try:
            if self._previous_position:
                # Restore previous position
                from desktop.modern.application.services.sequence.sequence_start_position_manager import (
                    SequenceStartPositionManager,
                )

                start_position_manager = SequenceStartPositionManager()
                start_position_manager.set_start_position(self._previous_position)

                logger.info(
                    f"✅ Start position clear undone, restored: {self._previous_position.letter}"
                )
            else:
                logger.warning("⚠️ No previous start position to restore")

            return

        except Exception as e:
            logger.exception(f"❌ Error undoing ClearStartPositionCommand: {e}")
            raise
