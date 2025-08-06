"""
Modern Image Export Service

This service provides image export functionality that replicates the legacy system's behavior
while following clean architecture patterns and using modern data types.
"""

from __future__ import annotations

from collections.abc import Callable
import logging
from pathlib import Path
from typing import Any

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage

from desktop.modern.core.interfaces.image_export_services import (
    ExportProgress,
    ExportResult,
    ImageExportOptions,
    ISequenceImageExporter,
    ISequenceImageLayoutCalculator,
    ISequenceImageRenderer,
    ISequenceMetadataExtractor,
)


logger = logging.getLogger(__name__)


class SequenceImageExporter(ISequenceImageExporter):
    """
    Modern implementation of image export service.

    This service replicates the legacy image exporter functionality while using
    clean architecture patterns and modern data types.
    """

    def __init__(
        self,
        image_renderer: ISequenceImageRenderer,
        metadata_extractor: ISequenceMetadataExtractor,
        layout_calculator: ISequenceImageLayoutCalculator,
    ):
        self.image_renderer = image_renderer
        self.metadata_extractor = metadata_extractor
        self.layout_calculator = layout_calculator

        # Legacy-compatible settings
        self.beat_size = 300  # Default beat size in pixels
        self.batch_size = 15  # Process 15 images at a time
        self.quality_settings = {
            "png_compression": 1,  # Maximum quality (0-9, lower is better)
            "high_quality": True,
        }

    def export_sequence_image(
        self,
        sequence_data: list[dict[str, Any]],
        word: str,
        output_path: Path,
        options: ImageExportOptions,
    ) -> ExportResult:
        """Export a single sequence as an image."""
        try:
            logger.debug(f"Exporting sequence image for word '{word}' to {output_path}")

            # Create the image
            image = self.create_sequence_image(sequence_data, word, options)

            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Save the image with legacy-compatible settings
            success = image.save(
                str(output_path), "PNG", self.quality_settings["png_compression"]
            )

            if success:
                logger.debug(f"Successfully exported image to {output_path}")
                return ExportResult(
                    success=True,
                    output_path=output_path,
                    metadata={"word": word, "sequence_length": len(sequence_data)},
                )
            error_msg = f"Failed to save image to {output_path}"
            logger.error(error_msg)
            return ExportResult(success=False, error_message=error_msg)

        except Exception as e:
            error_msg = f"Error exporting sequence image: {e}"
            logger.error(error_msg, exc_info=True)
            return ExportResult(success=False, error_message=error_msg)

    def export_all_sequences(
        self,
        source_directory: Path,
        export_directory: Path,
        options: ImageExportOptions,
        progress_callback: Callable[[ExportProgress], None] | None = None,
    ) -> dict[str, Any]:
        """Export all sequences from a directory."""
        logger.info(
            f"Starting export of all sequences from {source_directory} to {export_directory}"
        )

        # Collect all sequence files
        sequence_files = self._collect_sequence_files(source_directory)
        total_files = len(sequence_files)

        if total_files == 0:
            logger.warning(f"No sequence files found in {source_directory}")
            return {"success": False, "error": "No sequence files found"}

        # Initialize counters
        processed = 0
        successful = 0
        failed = 0
        skipped = 0

        logger.info(f"Found {total_files} sequence files to process")

        # Process files in batches
        for i in range(0, total_files, self.batch_size):
            batch = sequence_files[i : i + self.batch_size]

            for word, sequence_file in batch:
                # Update progress
                if progress_callback:
                    progress = ExportProgress(
                        current=processed,
                        total=total_files,
                        message=f"Processing {word}/{sequence_file.name}",
                    )
                    progress_callback(progress)

                # Process the file
                result = self._process_sequence_file(
                    word, sequence_file, source_directory, export_directory, options
                )

                if result["success"]:
                    successful += 1
                elif result["skipped"]:
                    skipped += 1
                else:
                    failed += 1

                processed += 1

        # Final progress update
        if progress_callback:
            progress = ExportProgress(
                current=total_files, total=total_files, message="Export complete"
            )
            progress_callback(progress)

        results = {
            "success": True,
            "total_files": total_files,
            "processed": processed,
            "successful": successful,
            "failed": failed,
            "skipped": skipped,
        }

        logger.info(f"Export complete: {results}")
        return results

    def _calculate_legacy_compatible_beat_size(
        self, num_beats: int, columns: int
    ) -> int:
        """
        Calculate beat size using legacy-compatible algorithm.

        Legacy calculation: min(width // num_cols, height // 6)
        This ensures exported images match legacy dimensions and font scaling.
        """
        # Estimate typical legacy beat frame dimensions
        # These values are based on analysis of legacy beat frame resizer
        typical_width = 1200  # Typical legacy beat frame width
        typical_height = 800  # Typical legacy beat frame height

        # Apply legacy calculation
        width_constraint = typical_width // columns if columns > 0 else 0
        height_constraint = typical_height // 6

        beat_size = min(width_constraint, height_constraint) if columns > 0 else 0

        # Ensure minimum size for very small calculations
        beat_size = max(beat_size, 100)  # Minimum 100px for readability

        logger.debug(
            f"Calculated legacy-compatible beat size: {beat_size}px for {num_beats} beats, {columns} columns"
        )
        return beat_size

    def create_sequence_image(
        self,
        sequence_data: list[dict[str, Any]],
        word: str,
        options: ImageExportOptions,
    ) -> QImage:
        """Create a QImage from sequence data."""
        logger.debug(
            f"Creating sequence image for word '{word}' with {len(sequence_data)} beats"
        )

        # Calculate layout
        num_beats = len(sequence_data)
        columns, rows = self.layout_calculator.calculate_layout(
            num_beats, options.include_start_position
        )

        # Calculate legacy-compatible beat size
        beat_size = self._calculate_legacy_compatible_beat_size(num_beats, columns)

        # Calculate additional heights for text elements (must be done after beat_size calculation)
        additional_height = self._calculate_additional_height(
            options, num_beats, beat_size
        )

        # Calculate image dimensions
        width, height = self.layout_calculator.calculate_image_dimensions(
            columns, rows, beat_size, additional_height
        )

        # Create the image
        image = QImage(width, height, QImage.Format.Format_ARGB32)
        image.fill(Qt.GlobalColor.white)

        # Note: additional_height_top and additional_height_bottom are set in _calculate_additional_height

        # Add beat_size to options for font scaling calculations
        options.beat_size = beat_size

        # Render sequence beats with calculated beat size
        self.image_renderer.render_sequence_beats(
            image, sequence_data, options, beat_size
        )

        # Render additional elements with legacy scaling
        if options.add_word:
            self.image_renderer.render_word(image, word, options, num_beats)

        if options.add_user_info:
            self.image_renderer.render_user_info(image, options, num_beats)

        if options.add_difficulty_level:
            difficulty_level = self.metadata_extractor.get_difficulty_level(
                sequence_data
            )
            self.image_renderer.render_difficulty_level(
                image, difficulty_level, options
            )

        logger.debug(f"Created image with dimensions {width}x{height}")
        return image

    def _collect_sequence_files(self, source_directory: Path) -> list[tuple[str, Path]]:
        """Collect all sequence files from the source directory."""
        sequence_files = []

        if not source_directory.exists():
            logger.warning(f"Source directory does not exist: {source_directory}")
            return sequence_files

        # Iterate through word directories
        for word_dir in source_directory.iterdir():
            if word_dir.is_dir():
                word = word_dir.name

                # Find sequence files in the word directory
                for file_path in word_dir.iterdir():
                    if file_path.is_file() and file_path.suffix.lower() == ".png":
                        sequence_files.append((word, file_path))

        logger.debug(f"Collected {len(sequence_files)} sequence files")
        return sequence_files

    def _process_sequence_file(
        self,
        word: str,
        sequence_file: Path,
        source_directory: Path,
        export_directory: Path,
        options: ImageExportOptions,
    ) -> dict[str, Any]:
        """Process a single sequence file."""
        try:
            # Create output path
            word_export_dir = export_directory / word
            output_path = word_export_dir / sequence_file.name

            # Check if regeneration is needed
            if output_path.exists() and not self._needs_regeneration(
                sequence_file, output_path
            ):
                return {"success": True, "skipped": True}

            # Extract sequence data
            sequence_data = self.metadata_extractor.extract_sequence_data(sequence_file)
            if not sequence_data:
                logger.warning(f"Could not extract sequence data from {sequence_file}")
                return {"success": False, "skipped": False}

            # Export the image
            result = self.export_sequence_image(
                sequence_data, word, output_path, options
            )
            return {"success": result.success, "skipped": False}

        except Exception as e:
            logger.error(
                f"Error processing sequence file {sequence_file}: {e}", exc_info=True
            )
            return {"success": False, "skipped": False}

    def _needs_regeneration(self, source_file: Path, output_file: Path) -> bool:
        """Check if the output file needs to be regenerated."""
        if not output_file.exists():
            return True

        # Compare modification times
        source_mtime = source_file.stat().st_mtime
        output_mtime = output_file.stat().st_mtime

        return source_mtime > output_mtime

    def _calculate_additional_height(
        self, options: ImageExportOptions, num_beats: int, beat_size: int
    ) -> int:
        """Calculate additional height needed for text elements using legacy logic."""
        # Legacy HeightDeterminer logic - exact replication
        # Calculate beat_scale based on beat_size ratio to reference size
        reference_beat_size = 280  # Reference size (modern default)
        beat_scale = beat_size / reference_beat_size

        if num_beats == 0:
            additional_height_top = 0
            additional_height_bottom = 55 if options.add_user_info else 0
        elif num_beats == 1:
            additional_height_top = 150 if options.add_word else 0
            additional_height_bottom = 55 if options.add_user_info else 0
        elif num_beats == 2:
            additional_height_top = 200 if options.add_word else 0
            additional_height_bottom = 75 if options.add_user_info else 0
        else:
            additional_height_top = 300 if options.add_word else 0
            additional_height_bottom = 150 if options.add_user_info else 0

        # Apply beat scale (legacy behavior)
        additional_height_top = int(additional_height_top * beat_scale)
        additional_height_bottom = int(additional_height_bottom * beat_scale)

        # Store for use in rendering
        options.additional_height_top = additional_height_top
        options.additional_height_bottom = additional_height_bottom

        return additional_height_top + additional_height_bottom
