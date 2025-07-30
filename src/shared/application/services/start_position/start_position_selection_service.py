"""
Start Position Selection Service

Handles business logic for start position selection operations.
Extracts command creation and validation logic from presentation components.
"""

import logging

from desktop.modern.core.commands.start_position_commands import SetStartPositionCommand
from desktop.modern.core.interfaces.start_position_services import (
    IStartPositionSelectionService,
)

# Event bus removed - using Qt signals instead

logger = logging.getLogger(__name__)


class StartPositionSelectionService(IStartPositionSelectionService):
    """
    Service for handling start position selection business logic.

    Responsibilities:
    - Validating position selections
    - Creating selection commands
    - Extracting position information
    - Applying business rules for position selection
    """

    def __init__(self):
        """Initialize the start position selection service."""
        logger.debug("StartPositionSelectionService initialized")

    def validate_selection(self, position_key: str) -> bool:
        """
        Validate if a position key is selectable.

        Args:
            position_key: Position key to validate

        Returns:
            True if valid for selection, False otherwise
        """
        try:
            if not position_key:
                logger.warning("Cannot validate empty position key")
                return False

            # Basic validation - position key should have the format "pos_pos"
            if "_" not in position_key:
                logger.warning(f"Invalid position key format: {position_key}")
                return False

            parts = position_key.split("_")
            if len(parts) != 2:
                logger.warning(
                    f"Position key should have exactly two parts: {position_key}"
                )
                return False

            # For start positions, both parts should be the same
            if parts[0] != parts[1]:
                logger.debug(
                    f"Position key is not a start position (parts differ): {position_key}"
                )
                # Note: This might be valid for non-start positions, so not an error

            logger.debug(f"Position key {position_key} validated successfully")
            return True

        except Exception as e:
            logger.error(f"Error validating position key {position_key}: {e}")
            return False

    def create_selection_command(self, position_key: str) -> SetStartPositionCommand:
        """
        Create a command for setting start position.

        Args:
            position_key: Position key to set

        Returns:
            SetStartPositionCommand ready for execution
        """
        try:
            # Event bus removed - using Qt signals instead

            # Create the command without event bus
            command = SetStartPositionCommand(position_key=position_key, event_bus=None)

            logger.debug(f"Created selection command for position: {position_key}")
            return command

        except Exception as e:
            logger.error(f"Error creating selection command for {position_key}: {e}")
            raise

    def extract_end_position_from_key(self, position_key: str) -> str:
        """
        Extract the end position from a position key.

        Args:
            position_key: Position key like "alpha1_alpha1"

        Returns:
            End position part (e.g., "alpha1")
        """
        try:
            if not position_key:
                logger.warning("Cannot extract end position from empty key")
                return ""

            # Position keys are in format "start_end", we want the end part
            if "_" in position_key:
                parts = position_key.split("_")
                if len(parts) >= 2:
                    end_position = parts[1]
                    logger.debug(
                        f"Extracted end position '{end_position}' from '{position_key}'"
                    )
                    return end_position

            # Fallback: if no underscore, assume it's already the position
            logger.debug(f"No underscore in position key, using as-is: {position_key}")
            return position_key

        except Exception as e:
            logger.error(f"Error extracting end position from {position_key}: {e}")
            return position_key  # Safe fallback

    def is_start_position_key(self, position_key: str) -> bool:
        """
        Check if a position key represents a start position.

        Args:
            position_key: Position key to check

        Returns:
            True if it's a start position (format "pos_pos"), False otherwise
        """
        try:
            if not position_key or "_" not in position_key:
                return False

            parts = position_key.split("_")
            if len(parts) != 2:
                return False

            # Start positions have the same start and end position
            return parts[0] == parts[1]

        except Exception as e:
            logger.error(f"Error checking start position key {position_key}: {e}")
            return False

    def normalize_position_key(self, position_key: str) -> str:
        """
        Normalize a position key to ensure consistent format.

        Args:
            position_key: Position key to normalize

        Returns:
            Normalized position key
        """
        try:
            if not position_key:
                return ""

            # Trim whitespace
            position_key = position_key.strip()

            # If it doesn't contain underscore, it might be a single position
            # For start positions, we need to duplicate it
            if "_" not in position_key:
                normalized = f"{position_key}_{position_key}"
                logger.debug(
                    f"Normalized single position '{position_key}' to start position '{normalized}'"
                )
                return normalized

            # Already has underscore, validate format
            parts = position_key.split("_")
            if len(parts) == 2:
                normalized = f"{parts[0].strip()}_{parts[1].strip()}"
                logger.debug(f"Normalized position key to: {normalized}")
                return normalized

            # Invalid format, return as-is
            logger.warning(f"Cannot normalize invalid position key: {position_key}")
            return position_key

        except Exception as e:
            logger.error(f"Error normalizing position key {position_key}: {e}")
            return position_key
