"""
Option Service - Pure Business Logic for Pictograph Option Management

This service contains the core business logic for managing pictograph options
without any Qt dependencies. It implements the IOptionService interface and
uses dependency injection for signal emission.

ARCHITECTURE:
Application Layer → OptionService → PositionMatchingService
Presentation Layer → OptionServiceQtAdapter → OptionService
"""

import logging
from typing import TYPE_CHECKING, Any

from desktop.modern.core.interfaces.option_picker_interfaces import (
    IOptionProvider,
    IOptionServiceSignals,
)
from desktop.modern.domain.models.pictograph_data import PictographData

if TYPE_CHECKING:
    from desktop.modern.domain.models.sequence_data import SequenceData

if TYPE_CHECKING:
    from desktop.modern.domain.models.sequence_data import SequenceData

logger = logging.getLogger(__name__)


class OptionProvider(IOptionProvider):
    """
    Pure business service for managing pictograph options.

    This service contains all the business logic for loading and managing
    pictograph options without any Qt dependencies. Signal emission is
    abstracted through the IOptionServiceSignals interface.
    """

    def __init__(self, signal_emitter: IOptionServiceSignals | None = None):
        """
        Initialize the option service.

        Args:
            signal_emitter: Optional signal emitter for notifications
        """
        self._pictograph_options: list[PictographData] = []
        self._position_service = None
        self._signal_emitter = signal_emitter
        self._initialize_position_service()

    def _initialize_position_service(self):
        """Initialize the position matching service."""
        try:
            from desktop.modern.application.services.positioning.arrows.utilities.pictograph_position_matcher import (
                PictographPositionMatcher,
            )

            self._position_service = PictographPositionMatcher()
            logger.debug("Position matching service initialized")

        except Exception as e:
            logger.error(f"Failed to initialize position service: {e}")
            self._position_service = None

    def load_options_from_sequence(
        self, sequence_data: list[dict[str, Any]]
    ) -> list[PictographData]:
        """
        Load pictograph options based on legacy sequence data.

        Args:
            sequence_data: Legacy sequence data format

        Returns:
            List of pictograph options
        """
        if not self._position_service:
            logger.warning("Position service not available")
            return self._clear_and_return_empty()

        try:
            # Extract end position from legacy sequence data
            if not sequence_data or len(sequence_data) <= 1:
                logger.debug("Empty or invalid sequence data")
                return self._clear_and_return_empty()

            # Get the last beat (skip metadata at index 0)
            last_beat = sequence_data[-1]
            if not isinstance(last_beat, dict) or "end_pos" not in last_beat:
                logger.debug("No valid end position found in sequence")
                return self._clear_and_return_empty()

            end_position = last_beat["end_pos"]
            logger.debug(f"Extracted end position: {end_position}")

            # Get options from position service
            options = self._position_service.get_next_options(end_position)

            # Cache and emit
            self._pictograph_options = options
            if self._signal_emitter:
                self._signal_emitter.emit_options_loaded(options)

            logger.debug(f"Loaded {len(options)} pictograph options from sequence")
            return options

        except Exception as e:
            logger.error(f"Error loading options from sequence: {e}")
            return self._clear_and_return_empty()

    def load_options_from_modern_sequence(
        self, sequence: "SequenceData"
    ) -> list[PictographData]:
        """
        Load pictograph options based on modern sequence data.

        Args:
            sequence: Modern SequenceData object

        Returns:
            List of pictograph options
        """
        if not self._position_service:
            logger.warning("Position service not available")
            return self._clear_and_return_empty()

        try:
            # Extract end position from modern sequence
            if not sequence or not sequence.beats:
                logger.debug("Empty sequence")
                return self._clear_and_return_empty()

            # Get the last beat
            last_beat = sequence.beats[-1]
            if not last_beat:
                logger.debug("No last beat found in modern sequence")
                return self._clear_and_return_empty()

            # Extract end position from glyph_data
            end_position = None
            if last_beat.pictograph_data.end_position:
                end_position = last_beat.pictograph_data.end_position
            elif last_beat.metadata and "end_position" in last_beat.metadata:
                end_position = last_beat.metadata["end_position"]

            if not end_position:
                logger.debug("No valid end position found in modern sequence beat")
                return self._clear_and_return_empty()

            logger.debug(f"Extracted end position from modern sequence: {end_position}")

            # Get options from position service
            options = self._position_service.get_next_options(end_position)

            # Cache and emit
            self._pictograph_options = options
            if self._signal_emitter:
                self._signal_emitter.emit_options_loaded(options)

            logger.debug(
                f"Loaded {len(options)} pictograph options from modern sequence"
            )
            return options

        except Exception as e:
            logger.error(f"Error loading options from modern sequence: {e}")
            return self._clear_and_return_empty()

    def get_current_options(self) -> list[PictographData]:
        """Get the currently loaded pictograph options."""
        return self._pictograph_options.copy()

    def clear_options(self) -> None:
        """Clear all loaded options."""
        self._pictograph_options = []
        if self._signal_emitter:
            self._signal_emitter.emit_options_cleared()
        logger.debug("Cleared all pictograph options")

    def get_option_count(self) -> int:
        """Get the number of currently loaded options."""
        return len(self._pictograph_options)

    def get_option_by_index(self, index: int) -> PictographData | None:
        """Get option by index."""
        if 0 <= index < len(self._pictograph_options):
            return self._pictograph_options[index]
        return None

    def filter_options_by_letter(self, letter: str) -> list[PictographData]:
        """Filter current options by letter."""
        return [opt for opt in self._pictograph_options if opt.letter == letter]

    def get_available_letters(self) -> list[str]:
        """Get list of available letters in current options."""
        letters = {opt.letter for opt in self._pictograph_options if opt.letter}
        return sorted(list(letters))

    def _clear_and_return_empty(self) -> list[PictographData]:
        """Clear options and return empty list."""
        self._pictograph_options = []
        if self._signal_emitter:
            self._signal_emitter.emit_options_cleared()
        return []

    def set_signal_emitter(self, signal_emitter: IOptionServiceSignals) -> None:
        """
        Set the signal emitter for this service.

        Args:
            signal_emitter: Signal emitter implementation
        """
        self._signal_emitter = signal_emitter
