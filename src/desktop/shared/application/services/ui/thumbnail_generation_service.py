"""
Thumbnail Generation Service

Modern service for generating sequence thumbnails.
Wraps existing thumbnail generation infrastructure with clean interfaces.
"""

import logging
import tempfile
from pathlib import Path

from desktop.modern.core.interfaces.ui_services import IThumbnailGenerationService
from desktop.modern.domain.models.sequence_data import SequenceData

logger = logging.getLogger(__name__)


class ThumbnailGenerationService(IThumbnailGenerationService):
    """
    Service for generating sequence thumbnails.

    Wraps the existing thumbnail generation infrastructure
    with a clean, modern interface.
    """

    def __init__(self, temp_directory: Path | None = None):
        """
        Initialize the thumbnail generation service.

        Args:
            temp_directory: Directory for temporary files (defaults to system temp)
        """
        self._temp_directory = temp_directory or Path(tempfile.gettempdir())

        # Lazy-loaded legacy components
        self._legacy_thumbnail_generator = None
        self._legacy_data_converter = None

    def generate_sequence_thumbnail(
        self,
        sequence: SequenceData,
        output_path: Path,
        fullscreen_preview: bool = False,
    ) -> Path | None:
        """
        Generate a thumbnail image for the given sequence.

        Args:
            sequence: The sequence to generate thumbnail for
            output_path: Where to save the thumbnail image
            fullscreen_preview: Whether this is for fullscreen preview (affects quality/options)

        Returns:
            Path to the generated thumbnail, or None if generation failed
        """
        try:
            # Validate inputs
            if not sequence or not sequence.beats:
                logger.warning("Cannot generate thumbnail: sequence is empty")
                return None

            if len(sequence.beats) <= 1:  # Only start position
                logger.warning("Cannot generate thumbnail: sequence too short")
                return None

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Convert modern sequence to legacy format
            legacy_sequence = self._convert_to_legacy_format(sequence)
            if not legacy_sequence:
                logger.error("Failed to convert sequence to legacy format")
                return None

            # Generate thumbnail using legacy infrastructure
            thumbnail_path = self._generate_with_legacy_system(
                legacy_sequence, output_path, fullscreen_preview
            )

            if thumbnail_path and Path(thumbnail_path).exists():
                logger.info(f"Generated thumbnail: {thumbnail_path}")
                return Path(thumbnail_path)
            else:
                logger.error("Legacy thumbnail generation failed")
                return None

        except Exception as e:
            logger.error(f"Failed to generate sequence thumbnail: {e}")
            return None

    def _convert_to_legacy_format(self, sequence: SequenceData) -> list | None:
        """
        Convert modern SequenceData to legacy format.

        Args:
            sequence: Modern sequence data

        Returns:
            Legacy sequence format, or None if conversion failed
        """
        try:
            # Get or create the data converter
            if not self._legacy_data_converter:
                self._legacy_data_converter = self._get_legacy_data_converter()

            if not self._legacy_data_converter:
                logger.error("No legacy data converter available")
                return None

            # Convert using the existing converter
            legacy_sequence = (
                self._legacy_data_converter.convert_modern_to_legacy_sequence(sequence)
            )

            logger.debug(
                f"Converted sequence to legacy format: {len(legacy_sequence)} entries"
            )
            return legacy_sequence

        except Exception as e:
            logger.error(f"Failed to convert sequence to legacy format: {e}")
            return None

    def _generate_with_legacy_system(
        self, legacy_sequence: list, output_path: Path, fullscreen_preview: bool
    ) -> str | None:
        """
        Generate thumbnail using the legacy thumbnail generation system.

        Args:
            legacy_sequence: Sequence in legacy format
            output_path: Where to save the thumbnail
            fullscreen_preview: Whether this is for fullscreen preview

        Returns:
            Path to generated thumbnail, or None if failed
        """
        try:
            # Get or create the legacy thumbnail generator
            if not self._legacy_thumbnail_generator:
                self._legacy_thumbnail_generator = (
                    self._get_legacy_thumbnail_generator()
                )

            if not self._legacy_thumbnail_generator:
                logger.error("No legacy thumbnail generator available")
                return None

            # Generate thumbnail using legacy system
            # The legacy system expects a directory and generates its own filename
            output_directory = str(output_path.parent)

            thumbnail_path = (
                self._legacy_thumbnail_generator.generate_and_save_thumbnail(
                    sequence=legacy_sequence,
                    structural_variation_number=0,  # Default variation
                    directory=output_directory,
                    dictionary=False,
                    fullscreen_preview=fullscreen_preview,
                )
            )

            if thumbnail_path:
                # Move/rename to our desired output path if needed
                legacy_path = Path(thumbnail_path)
                if legacy_path != output_path and legacy_path.exists():
                    try:
                        legacy_path.rename(output_path)
                        return str(output_path)
                    except Exception as e:
                        logger.warning(f"Could not rename thumbnail: {e}")
                        return str(legacy_path)
                else:
                    return thumbnail_path

            return None

        except Exception as e:
            logger.error(f"Legacy thumbnail generation failed: {e}")
            return None

    def _get_legacy_data_converter(self):
        """Get the legacy data converter instance"""
        try:
            # Try to import and create the legacy data converter
            from shared.application.services.data.modern_to_legacy_converter import (
                ModernToLegacyConverter,
            )

            return ModernToLegacyConverter()
        except ImportError as e:
            logger.warning(f"Could not import legacy data converter: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to create legacy data converter: {e}")
            return None

    def _get_legacy_thumbnail_generator(self):
        """Get the legacy thumbnail generator instance"""
        try:
            # This is a simplified approach - in a full implementation,
            # we'd need to properly initialize the legacy thumbnail generator
            # with all its dependencies (image_creator, etc.)

            # For now, return None and log that we need legacy integration
            logger.warning("Legacy thumbnail generator integration not yet implemented")
            logger.info("TODO: Integrate with legacy thumbnail generation system")
            return

        except Exception as e:
            logger.error(f"Failed to get legacy thumbnail generator: {e}")
            return


class MockThumbnailGenerationService(IThumbnailGenerationService):
    """
    Mock implementation for testing and development.

    Creates placeholder thumbnails instead of real ones.
    """

    def __init__(self, temp_directory: Path | None = None):
        """
        Initialize the mock thumbnail generation service.

        Args:
            temp_directory: Directory for temporary files (defaults to system temp)
        """
        self._temp_directory = temp_directory or Path(tempfile.gettempdir())

    def generate_sequence_thumbnail(
        self,
        sequence: SequenceData,
        output_path: Path,
        fullscreen_preview: bool = False,
    ) -> Path | None:
        """Generate a mock thumbnail for testing"""
        try:
            # Validate inputs
            if not sequence or not sequence.beats:
                return None

            if len(sequence.beats) <= 1:
                return None

            # Create a simple placeholder file without Qt dependencies
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Create a simple text-based placeholder
            placeholder_content = f"Mock Thumbnail\nSequence: {sequence.name}\nBeats: {len(sequence.beats)}"
            if fullscreen_preview:
                placeholder_content += "\n(Fullscreen Preview)"

            # Write placeholder content to file
            with open(output_path, "w") as f:
                f.write(placeholder_content)

            logger.info(f"Generated mock thumbnail: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to generate mock thumbnail: {e}")
            return None
