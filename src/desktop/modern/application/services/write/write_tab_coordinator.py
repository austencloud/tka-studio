"""
Write Tab Coordinator

Coordinator service that orchestrates all write tab functionality
including act management, music playback, and UI coordination.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

from desktop.modern.core.interfaces.write_services import (
    ActData,
    IActDataService,
    IActEditingService,
    IActLayoutService,
    IMusicPlayerService,
    IWriteTabCoordinator,
    WriteTabSignals,
)


logger = logging.getLogger(__name__)


class WriteTabCoordinator(IWriteTabCoordinator):
    """
    Coordinator for write tab functionality.

    Orchestrates interactions between act data, music playback,
    editing operations, and UI updates through a centralized service.
    """

    def __init__(
        self,
        act_data_service: IActDataService,
        music_player_service: IMusicPlayerService,
        act_editing_service: IActEditingService,
        act_layout_service: IActLayoutService,
    ):
        """
        Initialize the write tab coordinator.

        Args:
            act_data_service: Service for act data persistence
            music_player_service: Service for music playback
            act_editing_service: Service for act editing operations
            act_layout_service: Service for layout calculations
        """
        self.act_data_service = act_data_service
        self.music_player_service = music_player_service
        self.act_editing_service = act_editing_service
        self.act_layout_service = act_layout_service

        # Current state
        self.current_act: ActData | None = None
        self.current_file_path: Path | None = None
        self.is_modified = False

        # Signals for UI communication
        self._signals = WriteTabSignals()

        logger.info("WriteTabCoordinator initialized")

    def get_signals(self) -> WriteTabSignals:
        """Get the signals object for UI communication."""
        return self._signals

    def create_new_act(self) -> ActData:
        """
        Create a new empty act.

        Returns:
            New ActData instance
        """
        try:
            new_act = ActData(
                name="Untitled Act",
                description="",
                sequences=[],
                metadata={
                    "created_at": self._get_current_timestamp(),
                    "version": "1.0",
                },
            )

            self.current_act = new_act
            self.current_file_path = None
            self.is_modified = True

            logger.info("Created new act")
            self._signals.act_created.emit(new_act)

            return new_act

        except Exception as e:
            logger.exception(f"Failed to create new act: {e}")
            return ActData()  # Return empty act as fallback

    def load_act_from_file(self, file_path: Path) -> bool:
        """
        Load an act from file.

        Args:
            file_path: Path to the act file

        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            act = self.act_data_service.load_act(file_path)
            if act is None:
                logger.error(f"Failed to load act from {file_path}")
                return False

            self.current_act = act
            self.current_file_path = file_path
            self.is_modified = False

            # Load music if specified
            if act.music_file and act.music_file.exists():
                music_loaded = self.music_player_service.load_music(act.music_file)
                if music_loaded:
                    self._signals.music_loaded.emit(str(act.music_file))
                else:
                    logger.warning(f"Failed to load music file: {act.music_file}")

            logger.info(f"Successfully loaded act '{act.name}' from {file_path}")
            self._signals.act_loaded.emit(act)

            return True

        except Exception as e:
            logger.exception(f"Failed to load act from {file_path}: {e}")
            return False

    def save_current_act(self, file_path: Path | None = None) -> bool:
        """
        Save the current act.

        Args:
            file_path: Optional path to save to (uses current path if None)

        Returns:
            True if saved successfully, False otherwise
        """
        try:
            if self.current_act is None:
                logger.error("No act to save")
                return False

            # Determine save path
            save_path = file_path or self.current_file_path
            if save_path is None:
                # Generate default path
                acts_dir = self.act_data_service.get_acts_directory()
                safe_name = self._make_safe_filename(self.current_act.name)
                save_path = acts_dir / f"{safe_name}.json"

            # Update metadata
            self.current_act.metadata["last_saved"] = self._get_current_timestamp()

            # Save the act
            success = self.act_data_service.save_act(self.current_act, save_path)

            if success:
                self.current_file_path = save_path
                self.is_modified = False

                logger.info(
                    f"Successfully saved act '{self.current_act.name}' to {save_path}"
                )
                self._signals.act_saved.emit(str(save_path))

                return True
            logger.error(f"Failed to save act to {save_path}")
            return False

        except Exception as e:
            logger.exception(f"Failed to save current act: {e}")
            return False

    def get_current_act(self) -> ActData | None:
        """Get the currently loaded act."""
        return self.current_act

    def add_sequence_to_current_act(self, sequence_data: dict[str, Any]) -> bool:
        """
        Add a sequence to the current act.

        Args:
            sequence_data: The sequence data to add

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.current_act is None:
                logger.error("No current act to add sequence to")
                return False

            success = self.act_editing_service.add_sequence_to_act(
                self.current_act, sequence_data
            )

            if success:
                self.is_modified = True
                position = len(self.current_act.sequences) - 1

                logger.info(f"Added sequence to current act at position {position}")
                self._signals.sequence_added.emit(position)

                return True
            return False

        except Exception as e:
            logger.exception(f"Failed to add sequence to current act: {e}")
            return False

    def remove_sequence_from_current_act(self, position: int) -> bool:
        """
        Remove a sequence from the current act.

        Args:
            position: Position of the sequence to remove

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.current_act is None:
                logger.error("No current act to remove sequence from")
                return False

            success = self.act_editing_service.remove_sequence_from_act(
                self.current_act, position
            )

            if success:
                self.is_modified = True

                logger.info(f"Removed sequence from current act at position {position}")
                self._signals.sequence_removed.emit(position)

                return True
            return False

        except Exception as e:
            logger.exception(f"Failed to remove sequence from current act: {e}")
            return False

    def move_sequence_in_current_act(
        self, from_position: int, to_position: int
    ) -> bool:
        """
        Move a sequence within the current act.

        Args:
            from_position: Current position
            to_position: New position

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.current_act is None:
                logger.error("No current act to move sequence in")
                return False

            success = self.act_editing_service.move_sequence_in_act(
                self.current_act, from_position, to_position
            )

            if success:
                self.is_modified = True
                logger.info(
                    f"Moved sequence in current act from {from_position} to {to_position}"
                )
                # Note: Could emit a more specific signal here if needed

                return True
            return False

        except Exception as e:
            logger.exception(f"Failed to move sequence in current act: {e}")
            return False

    def update_current_act_info(
        self, name: str | None = None, description: str | None = None
    ) -> bool:
        """
        Update basic info for the current act.

        Args:
            name: New name (optional)
            description: New description (optional)

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.current_act is None:
                logger.error("No current act to update")
                return False

            if name is not None:
                self.current_act.name = name

            if description is not None:
                self.current_act.description = description

            # Update metadata
            metadata_update = {
                "last_modified": self._get_current_timestamp(),
            }

            success = self.act_editing_service.update_act_metadata(
                self.current_act, metadata_update
            )

            if success:
                self.is_modified = True
                logger.info(
                    f"Updated current act info (name: {name}, description updated: {description is not None})"
                )

                return True
            return False

        except Exception as e:
            logger.exception(f"Failed to update current act info: {e}")
            return False

    def load_music_for_current_act(self, music_file_path: Path) -> bool:
        """
        Load music for the current act.

        Args:
            music_file_path: Path to the music file

        Returns:
            True if successful, False otherwise
        """
        try:
            if self.current_act is None:
                logger.error("No current act to load music for")
                return False

            success = self.music_player_service.load_music(music_file_path)

            if success:
                self.current_act.music_file = music_file_path
                self.is_modified = True

                logger.info(f"Loaded music for current act: {music_file_path}")
                self._signals.music_loaded.emit(str(music_file_path))

                return True
            logger.error(f"Failed to load music file: {music_file_path}")
            return False

        except Exception as e:
            logger.exception(f"Failed to load music for current act: {e}")
            return False

    def play_music(self) -> bool:
        """Start music playback."""
        try:
            success = self.music_player_service.play()
            if success:
                self._signals.playback_started.emit()
            return success
        except Exception as e:
            logger.exception(f"Failed to start music playback: {e}")
            return False

    def pause_music(self) -> bool:
        """Pause music playback."""
        try:
            success = self.music_player_service.pause()
            if success:
                self._signals.playback_paused.emit()
            return success
        except Exception as e:
            logger.exception(f"Failed to pause music playback: {e}")
            return False

    def stop_music(self) -> bool:
        """Stop music playback."""
        try:
            success = self.music_player_service.stop()
            if success:
                self._signals.playback_stopped.emit()
            return success
        except Exception as e:
            logger.exception(f"Failed to stop music playback: {e}")
            return False

    def get_music_position(self) -> float:
        """Get current music playback position."""
        try:
            return self.music_player_service.get_position()
        except Exception as e:
            logger.exception(f"Failed to get music position: {e}")
            return 0.0

    def set_music_position(self, position: float) -> bool:
        """Set music playback position."""
        try:
            success = self.music_player_service.set_position(position)
            if success:
                self._signals.position_changed.emit(position)
            return success
        except Exception as e:
            logger.exception(f"Failed to set music position: {e}")
            return False

    def get_music_duration(self) -> float:
        """Get music duration."""
        try:
            return self.music_player_service.get_duration()
        except Exception as e:
            logger.exception(f"Failed to get music duration: {e}")
            return 0.0

    def is_music_playing(self) -> bool:
        """Check if music is currently playing."""
        try:
            return self.music_player_service.is_playing()
        except Exception as e:
            logger.exception(f"Failed to check music playback status: {e}")
            return False

    def get_available_acts(self) -> list[dict[str, Any]]:
        """
        Get list of available acts with metadata.

        Returns:
            List of act info dictionaries
        """
        try:
            act_files = self.act_data_service.get_available_acts()

            acts_info = []
            for file_path in act_files:
                act_info = self.act_data_service.get_act_info(file_path)
                if act_info:
                    act_info["file_path"] = str(file_path)
                    acts_info.append(act_info)

            logger.debug(f"Found {len(acts_info)} available acts")
            return acts_info

        except Exception as e:
            logger.exception(f"Failed to get available acts: {e}")
            return []

    def calculate_grid_layout(self, sequence_count: int) -> tuple[int, int]:
        """Calculate grid layout for sequences."""
        return self.act_layout_service.calculate_grid_dimensions(sequence_count)

    def is_current_act_modified(self) -> bool:
        """Check if the current act has unsaved changes."""
        return self.is_modified

    def get_current_file_path(self) -> Path | None:
        """Get the current act file path."""
        return self.current_file_path

    def _get_current_timestamp(self) -> float:
        """Get current timestamp."""
        import time

        return time.time()

    def _make_safe_filename(self, name: str) -> str:
        """Make a filename safe by removing/replacing invalid characters."""
        import re

        # Replace invalid characters with underscores
        safe_name = re.sub(r'[<>:"/\\|?*]', "_", name)
        # Remove extra whitespace and limit length
        safe_name = safe_name.strip()[:100]  # Max 100 chars
        # Ensure it's not empty
        if not safe_name:
            safe_name = "untitled_act"

        return safe_name

    def cleanup(self) -> None:
        """Clean up coordinator resources."""
        try:
            # Stop music playback
            self.music_player_service.stop()

            # Clean up music player
            if hasattr(self.music_player_service, "cleanup"):
                self.music_player_service.cleanup()

            logger.info("WriteTabCoordinator cleanup completed")

        except Exception as e:
            logger.exception(f"Error during WriteTabCoordinator cleanup: {e}")
