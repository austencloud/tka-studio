"""
Full Screen Viewer Service

Modern implementation of full screen sequence viewing functionality.
Replaces the stub methods in SequenceManager with a dedicated service
following clean architecture principles.
"""

import logging
import tempfile
from pathlib import Path
from typing import Protocol

from desktop.modern.core.interfaces.workbench_services import IFullScreenViewer
from desktop.modern.domain.models.sequence_data import SequenceData

logger = logging.getLogger(__name__)


class IThumbnailGenerator(Protocol):
    """Interface for thumbnail generation services"""

    def generate_sequence_thumbnail(
        self,
        sequence: SequenceData,
        output_path: Path,
        fullscreen_preview: bool = False,
    ) -> Path | None:
        """Generate thumbnail image for sequence"""


class ISequenceStateReader(Protocol):
    """Interface for reading current sequence state from UI"""

    def get_current_sequence(self) -> SequenceData | None:
        """Get the current sequence from workbench UI state"""


class IFullScreenOverlayFactory(Protocol):
    """Interface for creating full screen overlay widgets"""

    def create_overlay(self, parent_widget) -> "IFullScreenOverlay":
        """Create a full screen overlay widget"""


class IFullScreenOverlay(Protocol):
    """Interface for full screen overlay widget"""

    def show_image(self, image_path: Path) -> None:
        """Display image in full screen overlay"""

    def close(self) -> None:
        """Close the overlay"""


class FullScreenViewer(IFullScreenViewer):
    """
    Dedicated full screen viewing service.

    Replaces the stub implementation in SequenceManager with proper
    separation of concerns and dependency injection.
    """

    def __init__(
        self,
        thumbnail_generator: IThumbnailGenerator,
        sequence_state_reader: ISequenceStateReader,
        overlay_factory: IFullScreenOverlayFactory,
        temp_directory: Path | None = None,
    ):
        """
        Initialize the full screen service.

        Args:
            thumbnail_generator: Service for generating sequence thumbnails
            sequence_state_reader: Service for reading current sequence state
            overlay_factory: Factory for creating overlay widgets
            temp_directory: Directory for temporary files (defaults to system temp)
        """
        self._thumbnail_generator = thumbnail_generator
        self._sequence_state_reader = sequence_state_reader
        self._overlay_factory = overlay_factory
        self._temp_directory = temp_directory or Path(tempfile.gettempdir())

        # Current overlay instance (for cleanup)
        self._current_overlay: IFullScreenOverlay | None = None

    def create_sequence_thumbnail(self, sequence: SequenceData) -> bytes:
        """
        Create thumbnail from sequence.

        Args:
            sequence: The sequence to create thumbnail for

        Returns:
            Thumbnail image data as bytes
        """
        try:
            # Validate sequence
            if not sequence or not sequence.beats:
                logger.warning("Cannot create thumbnail: sequence is empty")
                return b""

            if len(sequence.beats) <= 1:  # Only start position
                logger.warning(
                    "Cannot create thumbnail: sequence too short (need >1 beats)"
                )
                return b""

            # Generate thumbnail to temporary file
            temp_path = self._temp_directory / f"fullscreen_thumbnail_{sequence.id}.png"

            thumbnail_path = self._thumbnail_generator.generate_sequence_thumbnail(
                sequence=sequence, output_path=temp_path, fullscreen_preview=True
            )

            if not thumbnail_path or not thumbnail_path.exists():
                logger.error("Thumbnail generation failed: no output file created")
                return b""

            # Read thumbnail data
            thumbnail_data = thumbnail_path.read_bytes()
            logger.info(f"Generated thumbnail: {len(thumbnail_data)} bytes")

            # Clean up temporary file
            try:
                thumbnail_path.unlink()
            except Exception as e:
                logger.warning(f"Failed to clean up temporary thumbnail: {e}")

            return thumbnail_data

        except Exception as e:
            logger.error(f"Failed to create sequence thumbnail: {e}")
            return b""

    def show_full_screen_view(self, sequence: SequenceData) -> None:
        """
        Show sequence in full screen overlay.

        Args:
            sequence: The sequence to display in full screen
        """
        try:
            # Validate sequence
            if not sequence or not sequence.beats:
                logger.warning("Cannot show full screen: sequence is empty")
                self._show_error_message("Please build a sequence first.")
                return

            if len(sequence.beats) <= 1:  # Only start position
                logger.warning("Cannot show full screen: sequence too short")
                self._show_error_message("Please build a sequence first.")
                return

            # Generate thumbnail for display
            temp_path = self._temp_directory / f"fullscreen_display_{sequence.id}.png"

            thumbnail_path = self._thumbnail_generator.generate_sequence_thumbnail(
                sequence=sequence, output_path=temp_path, fullscreen_preview=True
            )

            if not thumbnail_path or not thumbnail_path.exists():
                logger.error("Cannot show full screen: thumbnail generation failed")
                self._show_error_message("Failed to generate sequence preview.")
                return

            # Close any existing overlay
            if self._current_overlay:
                self._current_overlay.close()
                self._current_overlay = None

            # Create and show new overlay
            # Note: We'll need to get the parent widget from somewhere
            # For now, we'll pass None and handle it in the factory
            self._current_overlay = self._overlay_factory.create_overlay(
                parent_widget=None
            )
            self._current_overlay.show_image(thumbnail_path)

            logger.info(f"🖥️ Full screen view displayed for sequence: {sequence.name}")

        except Exception as e:
            logger.error(f"Failed to show full screen view: {e}")
            self._show_error_message(f"Full screen view failed: {e}")

    def _show_error_message(self, message: str) -> None:
        """
        Show error message to user.

        For now, just log the error. In a full implementation,
        this would show a proper UI message.
        """
        logger.error(f"Full screen error: {message}")
        print(f"❌ Full screen error: {message}")

    # Interface implementation methods
    def show_fullscreen(self, content: any = None) -> None:
        """Show content in fullscreen mode."""
        if content is None:
            # Get current sequence from state reader
            content = self._sequence_state_reader.get_current_sequence()

        if content:
            self.show_full_screen_view(content)
        else:
            self._show_error_message("No content to display in fullscreen")

    def hide_fullscreen(self) -> None:
        """Hide fullscreen mode."""
        if self._current_overlay:
            self._current_overlay.close()
            self._current_overlay = None
            logger.info("🖥️ Full screen view hidden")

    def is_fullscreen(self) -> bool:
        """Check if currently in fullscreen mode."""
        return self._current_overlay is not None

    def toggle_fullscreen(self, content: any = None) -> bool:
        """Toggle fullscreen mode."""
        if self.is_fullscreen():
            self.hide_fullscreen()
            return False
        else:
            self.show_fullscreen(content)
            return True
