"""
Start Position Commands for Event-Driven Architecture

Commands for handling start position operations with undo/redo support.
These replace the complex signal chains in the original architecture.
"""

import logging
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from core.commands.command_system import ICommand
from domain.models.beat_data import BeatData

logger = logging.getLogger(__name__)


@dataclass
class SetStartPositionCommand(ICommand[BeatData]):
    """Command to set sequence start position with undo support"""

    position_key: str
    event_bus: Any  # IEventBus
    _command_id: str = ""
    _previous_position: Optional[BeatData] = None
    _new_position_data: Optional[BeatData] = None

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
        return self._new_position_data is not None

    def execute(self) -> BeatData:
        """Execute: Set start position and save to persistence"""
        try:
            # Get current state manager to store previous position
            from core.service_locator import get_sequence_state_manager

            state_manager = get_sequence_state_manager()
            if state_manager:
                self._previous_position = state_manager.get_start_position()

            # Create start position data using existing logic
            self._new_position_data = self._create_start_position_data()

            if not self._new_position_data:
                raise ValueError(
                    f"Failed to create start position data for {self.position_key}"
                )

            # Save to persistence
            self._save_to_persistence(self._new_position_data)

            logger.info(f"✅ Start position set via command: {self.position_key}")
            return self._new_position_data

        except Exception as e:
            logger.error(f"❌ Error executing SetStartPositionCommand: {e}")
            raise

    def undo(self) -> Optional[BeatData]:
        """Undo: Restore previous start position"""
        try:
            if self._previous_position:
                # Restore previous position
                self._save_to_persistence(self._previous_position)
                logger.info(
                    f"✅ Start position undone, restored: {self._previous_position.letter}"
                )
                return self._previous_position
            else:
                # Clear start position
                self._clear_from_persistence()
                logger.info("✅ Start position undone, cleared")
                return None

        except Exception as e:
            logger.error(f"❌ Error undoing SetStartPositionCommand: {e}")
            raise

    def _create_start_position_data(self) -> BeatData:
        """Create start position data using existing business logic"""
        try:
            # Use existing StartPositionHandler logic
            from core.service_locator import get_data_conversion_service

            data_converter = get_data_conversion_service()

            if not data_converter:
                raise ValueError("Data conversion service not available")

            # Get the dataset query service
            from application.services.data.dataset_quiry import DatasetQuery
            from domain.models.glyph_models import GlyphData

            dataset_service = DatasetQuery()

            # Get real start position data from dataset
            real_start_position = dataset_service.get_start_position_beat_data(
                self.position_key, "diamond"
            )

            if real_start_position:
                # Extract the specific end position from position_key
                specific_end_pos = (
                    data_converter.extract_end_position_from_position_key(
                        self.position_key
                    )
                )

                # Create proper glyph data with the specific position
                glyph_data = GlyphData(
                    start_position=self.position_key,
                    end_position=specific_end_pos,
                )

                # Update the beat data with proper glyph data and position info
                beat_data = real_start_position.update(
                    beat_number=0,  # Start position is beat 0 in persistence
                    duration=1.0,  # Standard duration
                    glyph_data=glyph_data,
                )

                logger.debug(
                    f"🎯 Created start position data: {self.position_key} -> {specific_end_pos}"
                )
                return beat_data
            else:
                # Fallback start position with proper glyph data
                logger.warning(
                    f"⚠️ No real data found for position {self.position_key}, using fallback"
                )

                specific_end_pos = (
                    data_converter.extract_end_position_from_position_key(
                        self.position_key
                    )
                )

                glyph_data = GlyphData(
                    start_position=self.position_key,
                    end_position=specific_end_pos,
                )

                fallback_beat = BeatData.empty().update(
                    letter=self.position_key,
                    beat_number=0,
                    duration=1.0,
                    glyph_data=glyph_data,
                    is_blank=False,
                )

                return fallback_beat

        except Exception as e:
            logger.error(f"❌ Error creating start position data: {e}")
            raise

    def _save_to_persistence(self, start_position_data: BeatData):
        """Save start position to persistence"""
        try:
            from application.services.sequences.sequence_start_position_manager import (
                SequenceStartPositionManager,
            )

            start_position_manager = SequenceStartPositionManager()
            start_position_manager.set_start_position(start_position_data)

            logger.debug(
                f"💾 Start position saved to persistence: {start_position_data.letter}"
            )

        except Exception as e:
            logger.error(f"❌ Error saving start position to persistence: {e}")
            raise

    def _clear_from_persistence(self):
        """Clear start position from persistence"""
        try:
            from application.services.sequences.sequence_start_position_manager import (
                SequenceStartPositionManager,
            )

            start_position_manager = SequenceStartPositionManager()
            start_position_manager.clear_start_position()

            logger.debug("🗑️ Start position cleared from persistence")

        except Exception as e:
            logger.error(f"❌ Error clearing start position from persistence: {e}")
            raise


@dataclass
class ClearStartPositionCommand(ICommand[None]):
    """Command to clear start position with undo support"""

    event_bus: Any  # IEventBus
    _command_id: str = ""
    _previous_position: Optional[BeatData] = None

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
            from core.service_locator import get_sequence_state_manager

            state_manager = get_sequence_state_manager()
            if state_manager:
                self._previous_position = state_manager.get_start_position()

            # Clear from persistence
            from application.services.sequences.sequence_start_position_manager import (
                SequenceStartPositionManager,
            )

            start_position_manager = SequenceStartPositionManager()
            start_position_manager.clear_start_position()

            logger.info("✅ Start position cleared via command")
            return None

        except Exception as e:
            logger.error(f"❌ Error executing ClearStartPositionCommand: {e}")
            raise

    def undo(self) -> None:
        """Undo: Restore previous start position"""
        try:
            if self._previous_position:
                # Restore previous position
                from application.services.sequences.sequence_start_position_manager import (
                    SequenceStartPositionManager,
                )

                start_position_manager = SequenceStartPositionManager()
                start_position_manager.set_start_position(self._previous_position)

                logger.info(
                    f"✅ Start position clear undone, restored: {self._previous_position.letter}"
                )
            else:
                logger.warning("⚠️ No previous start position to restore")

            return None

        except Exception as e:
            logger.error(f"❌ Error undoing ClearStartPositionCommand: {e}")
            raise
