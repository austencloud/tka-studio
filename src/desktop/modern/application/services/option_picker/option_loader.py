"""
OptionLoadingService - Microservice for option loading orchestration.

This service extracts complex loading logic from UI components to handle:
- Frame allocation from pool
- Pictograph updates and signal connections
- Batch loading operations
- Performance monitoring integration

Replaces complex orchestration logic previously embedded in OptionPickerSection.
"""

import logging
import time
from collections.abc import Callable
from typing import Any

from desktop.modern.application.services.option_picker.frame_pool_service import (
    FramePoolService,
)
from desktop.modern.core.interfaces.sequence_operation_services import IOptionLoader
from desktop.modern.core.monitoring import performance_monitor
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.presentation.components.option_picker.components.option_pictograph import (
    OptionPictograph,
)
from desktop.modern.presentation.components.option_picker.types.letter_types import (
    LetterType,
)

logger = logging.getLogger(__name__)


class OptionLoader(IOptionLoader):
    """
    Microservice for orchestrating option loading operations.

    Handles all loading concerns:
    - Frame allocation from pool
    - Pictograph content updates
    - Signal connection management
    - Batch loading with performance monitoring
    - Error handling and recovery
    """

    def __init__(self, frame_pool_service: FramePoolService):
        """
        Initialize with injected frame pool service.

        Args:
            frame_pool_service: Service for managing frame pool
        """
        self._frame_pool_service = frame_pool_service

    def load_section_options(
        self,
        letter_type: LetterType,
        pictographs: list[PictographData],
        selection_callback: Callable[[PictographData], None],
    ) -> list["OptionPictograph"]:
        """
        Load pictographs into frames for a section.

        This replaces the complex loading logic previously in
        OptionPickerSection.load_options_from_sequence().

        Args:
            letter_type: Type of letter section being loaded
            pictographs: List of pictograph data to load
            selection_callback: Callback for when option is selected

        Returns:
            List of loaded frames ready for UI display
        """
        frames = []

        try:
            with performance_monitor.profile_block(f"section_{letter_type}_load_total"):
                # Load each pictograph into a frame
                for i, pictograph_data in enumerate(pictographs):
                    with performance_monitor.profile_block(
                        f"section_{letter_type}_frame_{i}"
                    ):
                        frame = self._load_single_option(
                            pictograph_data, selection_callback, i, letter_type
                        )
                        if frame:
                            frames.append(frame)

                logger.debug(f"Loaded {len(frames)} options for {letter_type} section")

        except Exception as e:
            logger.error(f"Error loading options for {letter_type}: {e}")
            # Return frames loaded so far

        return frames

    def _load_single_option(
        self,
        pictograph_data: PictographData,
        selection_callback: Callable[[PictographData], None],
        index: int,
        letter_type: LetterType,
    ) -> "OptionPictograph":
        """
        Load a single pictograph option into a frame.

        Args:
            pictograph_data: Pictograph data to load
            selection_callback: Selection callback to connect
            index: Index for performance logging
            letter_type: Letter type for performance logging

        Returns:
            Loaded frame or None if loading failed
        """
        try:
            # Get frame from pool
            with performance_monitor.profile_block(
                f"section_{letter_type}_checkout_frame"
            ):
                frame = self._frame_pool_service.checkout_frame()
                if not frame:
                    logger.error("Failed to get frame from pool")
                    return None

            # Update pictograph content
            with performance_monitor.profile_block(
                f"section_{letter_type}_update_pictograph"
            ):
                start_time = time.perf_counter()
                frame.update_pictograph(pictograph_data)
                update_time = (time.perf_counter() - start_time) * 1000

            # Connect selection signal
            with performance_monitor.profile_block(
                f"section_{letter_type}_connect_signal"
            ):
                frame.option_selected.connect(selection_callback)

            # Log timing for first frame only to reduce overhead
            if index == 0:
                logger.debug(
                    f"🔍 [FRAME_TIMING] {letter_type}[{index}]: update={update_time:.1f}ms"
                )

            return frame

        except Exception as e:
            logger.error(f"Error loading single option for {letter_type}[{index}]: {e}")
            return None

    def unload_section_options(self, frames: list["OptionPictograph"]) -> None:
        """
        Unload options and return frames to pool.

        Args:
            frames: List of frames to unload
        """
        try:
            for frame in frames:
                # Disconnect signals to prevent memory leaks
                if hasattr(frame, "option_selected"):
                    try:
                        frame.option_selected.disconnect()
                    except Exception:
                        # Signal might already be disconnected
                        pass

                # Return frame to pool
                self._frame_pool_service.checkin_frame(frame)

            logger.debug(f"Unloaded {len(frames)} option frames")

        except Exception as e:
            logger.error(f"Error unloading section options: {e}")

    def batch_load_all_sections(
        self,
        sections_data: dict[LetterType, list[PictographData]],
        selection_callback: Callable[[PictographData], None],
    ) -> dict[LetterType, list["OptionPictograph"]]:
        """
        Load options for all sections in batch.

        Args:
            sections_data: Dictionary mapping letter types to pictograph lists
            selection_callback: Callback for option selection

        Returns:
            Dictionary mapping letter types to loaded frames
        """
        loaded_sections = {}

        try:
            with performance_monitor.profile_block("batch_load_all_sections"):
                for letter_type, pictographs in sections_data.items():
                    frames = self.load_section_options(
                        letter_type, pictographs, selection_callback
                    )
                    loaded_sections[letter_type] = frames

                total_frames = sum(len(frames) for frames in loaded_sections.values())
                logger.debug(
                    f"Batch loaded {total_frames} frames across {len(loaded_sections)} sections"
                )

        except Exception as e:
            logger.error(f"Error in batch loading: {e}")

        return loaded_sections

    def clear_all_sections(
        self, sections_frames: dict[LetterType, list["OptionPictograph"]]
    ) -> None:
        """
        Clear all loaded sections and return frames to pool.

        Args:
            sections_frames: Dictionary mapping letter types to frame lists
        """
        try:
            total_frames = 0

            for letter_type, frames in sections_frames.items():
                self.unload_section_options(frames)
                total_frames += len(frames)

            logger.debug(f"Cleared {total_frames} frames from all sections")

        except Exception as e:
            logger.error(f"Error clearing all sections: {e}")

    def get_loading_statistics(self) -> dict:
        """
        Get loading service statistics.

        Returns:
            Dictionary with loading statistics
        """
        pool_stats = self._frame_pool_service.get_pool_statistics()

        return {
            "frame_pool": pool_stats,
            "service_status": "active",
        }

    def validate_loading_capacity(self, required_frames: int) -> bool:
        """
        Validate if pool has capacity for required frames.

        Args:
            required_frames: Number of frames needed

        Returns:
            True if capacity is available
        """
        if not self._frame_pool_service.is_initialized():
            return False

        pool_size = self._frame_pool_service.get_pool_size()
        return required_frames <= pool_size

    # Interface implementation methods
    def load_options(self, criteria: dict[str, Any]) -> list[Any]:
        """Load options based on criteria (interface implementation)."""
        pictographs = criteria.get("pictographs", [])
        letter_type = criteria.get("letter_type", LetterType.Type1)

        # Use existing load_pictographs method
        self.load_pictographs(pictographs, letter_type)

        # Return loaded pictographs
        return pictographs

    def get_available_options(self, context: str) -> list[Any]:
        """Get available options for context (interface implementation)."""
        # Return empty list for now - would be populated based on context
        return []

    def validate_option_criteria(self, criteria: dict[str, Any]) -> bool:
        """Validate option loading criteria (interface implementation)."""
        try:
            # Check required fields
            if "pictographs" not in criteria:
                return False

            pictographs = criteria["pictographs"]
            if not isinstance(pictographs, list):
                return False

            # Check if we can handle the required frames
            return self.can_handle_load(len(pictographs))
        except Exception:
            return False
