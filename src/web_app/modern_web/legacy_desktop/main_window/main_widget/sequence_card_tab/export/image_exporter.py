from __future__ import annotations

# src/main_window/main_widget/sequence_card_tab/export/image_exporter.py
import gc
import io
import json
import os
import time
from datetime import datetime
from typing import TYPE_CHECKING

import numpy as np
import psutil
from PIL import Image, PngImagePlugin
from PyQt6.QtCore import QBuffer, Qt
from PyQt6.QtGui import QImage
from PyQt6.QtWidgets import QApplication

from main_window.main_widget.browse_tab.temp_beat_frame.temp_beat_frame import (
    TempBeatFrame,
)
from main_window.main_widget.metadata_extractor import MetaDataExtractor
from main_window.main_widget.sequence_workbench.legacy_beat_frame.image_export_manager.image_export_manager import (
    ImageExportManager,
)
from utils.path_helpers import (
    get_dictionary_path,
    get_sequence_card_image_exporter_path,
)

if TYPE_CHECKING:
    from ..sequence_card_tab import SequenceCardTab


class SequenceCardImageExporter:
    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        self.sequence_card_tab = sequence_card_tab
        self.main_widget = sequence_card_tab.main_widget
        self.temp_beat_frame = TempBeatFrame(sequence_card_tab)
        self.export_manager = ImageExportManager(
            self.temp_beat_frame, self.temp_beat_frame.__class__
        )
        self.metadata_extractor = MetaDataExtractor()
        self.progress_dialog = None
        self.cancel_requested = False
        self.force_regenerate = False  # Flag to bypass caching and force regeneration

        # Optimized batch processing settings
        self.batch_size = 15  # Process 15 images at a time for better throughput
        self.memory_check_interval = 5  # Check memory every 5 images
        self.max_memory_usage_mb = 2000  # Force GC if memory exceeds 2GB
        self.quality_settings = {
            "png_compression": 1,  # MAXIMUM QUALITY: 0-9, lower is better quality (changed from 6 to 1)
            "high_quality": True,  # Use high quality rendering
        }

    def export_all_images(self, length_filter: int | None = None):
        """
        Dynamically renders sequences from the dictionary with consistent export settings.

        Args:
            length_filter: If specified, only export sequences of this length

        This method:
        1. Loads sequences directly from the dictionary
        2. Applies consistent export settings to all sequences
        3. Organizes sequences by word
        4. Exports them to the dedicated sequence_card_images directory
        5. Uses smart caching to avoid regenerating unchanged images
        6. Processes images in batches to limit memory usage
        7. Implements memory management to prevent out-of-memory errors
        8. Optionally filters by sequence length for selective regeneration
        """
        dictionary_path = get_dictionary_path()
        export_path = get_sequence_card_image_exporter_path()

        # Debug: Print the paths
        print(f"DEBUG: Dictionary path: {dictionary_path}")
        print(f"DEBUG: Export path: {export_path}")
        print(f"DEBUG: Current working directory: {os.getcwd()}")

        # Create the export directory if it doesn't exist
        if not os.path.exists(export_path):
            os.makedirs(export_path)
            print(f"DEBUG: Created export directory: {export_path}")
        else:
            print(f"DEBUG: Export directory already exists: {export_path}")

        print(f"Loading sequences from dictionary: {dictionary_path}")
        print(f"Exporting to: {export_path}")

        # Check if force regeneration is enabled
        if getattr(self, "force_regenerate", False):
            print("DEBUG: Force regeneration enabled - all images will be regenerated")

        # Check if length filtering is enabled
        if length_filter is not None:
            print(
                f"DEBUG: Length filtering enabled - only {length_filter}-beat sequences will be processed"
            )

        # Get all word folders in the dictionary
        word_folders = []
        for item in os.listdir(dictionary_path):
            item_path = os.path.join(dictionary_path, item)
            if os.path.isdir(item_path) and not item.startswith("__"):
                word_folders.append(item)

        # Count total sequences first for progress tracking
        total_sequences = self._count_total_sequences(dictionary_path, word_folders)

        # Check initial memory usage
        self._check_and_manage_memory()

        # Initialize statistics
        processed_sequences = 0
        regenerated_count = 0
        skipped_count = 0
        failed_count = 0

        try:
            # Count total sequences for batch processing
            all_sequences = []
            for word in word_folders:
                word_path = os.path.join(dictionary_path, word)
                for sequence_file in os.listdir(word_path):
                    if sequence_file.endswith(".png") and not sequence_file.startswith(
                        "__"
                    ):
                        all_sequences.append((word, sequence_file))

            total_sequences = len(all_sequences)
            print(f"Total sequences to process: {total_sequences}")

            # Process sequences in batches
            batch_size = self.batch_size
            for batch_start in range(0, total_sequences, batch_size):
                if self.cancel_requested:
                    break

                batch_end = min(batch_start + batch_size, total_sequences)
                print(
                    f"Processing batch {batch_start // batch_size + 1} of {(total_sequences + batch_size - 1) // batch_size} (sequences {batch_start + 1}-{batch_end})"
                )

                # Process the current batch
                (
                    processed_sequences,
                    regenerated_count,
                    skipped_count,
                    failed_count,
                ) = self._process_sequence_batch(
                    word_folders,
                    dictionary_path,
                    export_path,
                    batch_start,
                    batch_end,
                    processed_sequences,
                    total_sequences,
                    regenerated_count,
                    skipped_count,
                    failed_count,
                    length_filter,
                )

                # Force garbage collection between batches
                self._check_and_manage_memory(force_cleanup=True)

                # Process events to keep UI responsive
                QApplication.processEvents()

        except Exception as e:
            print(f"DEBUG: Exception during export: {e}")
        finally:
            # Final memory cleanup
            self._check_and_manage_memory(force_cleanup=True)

            # Debug: Check if any files were actually created
            print("DEBUG: Checking export directory after completion...")
            if os.path.exists(export_path):
                total_files = 0
                for root, dirs, files in os.walk(export_path):
                    png_files = [
                        f
                        for f in files
                        if f.endswith(".png") and not f.startswith("__")
                    ]
                    total_files += len(png_files)
                    if (
                        png_files and len(dirs) < 5
                    ):  # Only print for first few directories
                        print(f"DEBUG: Found {len(png_files)} PNG files in {root}")
                print(
                    f"DEBUG: Total PNG files found in export directory: {total_files}"
                )
            else:
                print(f"DEBUG: Export directory does not exist: {export_path}")

    def export_images_by_length(self, length: int):
        """
        Export images for sequences of a specific length only.

        Args:
            length: The sequence length to export (e.g., 4 for 4-beat sequences)
        """
        print(f"Starting selective export for {length}-beat sequences...")
        self.export_all_images(length_filter=length)

    def get_all_images(self, path: str) -> list[str]:
        images = []
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith((".png", ".jpg", ".jpeg")):
                    images.append(os.path.join(root, file))
        return images

    def qimage_to_pil(self, qimage: QImage, max_dimension: int = 3000) -> Image.Image:
        """
        Convert a QImage to a PIL Image with memory-efficient processing and high quality.

        Args:
            qimage: The QImage to convert
            max_dimension: Maximum width or height for the image (default: 3000px)

        Returns:
            PIL Image object

        This method includes:
        1. Optimized image scaling to maintain quality
        2. Efficient memory management
        3. Error handling for out-of-memory situations
        4. Progressive downsampling if needed
        """
        try:
            # Check if image needs downsampling
            original_width, original_height = qimage.width(), qimage.height()

            # Calculate scaling factor if image is too large
            scale_factor = 1.0
            if original_width > max_dimension or original_height > max_dimension:
                width_factor = (
                    max_dimension / original_width
                    if original_width > max_dimension
                    else 1.0
                )
                height_factor = (
                    max_dimension / original_height
                    if original_height > max_dimension
                    else 1.0
                )
                scale_factor = min(width_factor, height_factor)

                # Log downsampling information
                print(
                    f"Scaling image from {original_width}x{original_height} "
                    + f"to {int(original_width * scale_factor)}x{int(original_height * scale_factor)}"
                )

                # Resize the QImage with high quality
                new_width = int(original_width * scale_factor)
                new_height = int(original_height * scale_factor)
                qimage = qimage.scaled(
                    new_width,
                    new_height,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

            # Convert to ARGB32 format
            qimage = qimage.convertToFormat(QImage.Format.Format_ARGB32)
            width, height = qimage.width(), qimage.height()

            # Get image data
            ptr = qimage.bits()
            ptr.setsize(height * width * 4)

            # Process in chunks to reduce memory pressure
            try:
                # Create numpy array with copy=True to ensure memory safety
                arr = np.array(ptr, copy=True).reshape((height, width, 4))

                # Convert from ARGB to RGBA
                arr = arr[..., [2, 1, 0, 3]]

                # Create PIL image
                pil_image = Image.fromarray(arr, "RGBA")

                # Clear the numpy array to free memory
                arr = None

                return pil_image

            except MemoryError:
                # If we hit a memory error during numpy processing, try a different approach
                print("Memory error during numpy processing, trying alternative method")
                return self._alternative_qimage_to_pil(qimage)

        except MemoryError as e:
            print(f"Memory error during image conversion: {e}")
            print(f"Image dimensions: {qimage.width()}x{qimage.height()}")

            # Try with more conservative downsampling first
            if max_dimension > 2000:
                print("Retrying with moderate downsampling (max dimension: 2000px)")
                return self.qimage_to_pil(qimage, max_dimension=2000)
            elif max_dimension > 1500:
                print("Retrying with stronger downsampling (max dimension: 1500px)")
                return self.qimage_to_pil(qimage, max_dimension=1500)
            elif max_dimension > 1000:
                print("Retrying with aggressive downsampling (max dimension: 1000px)")
                return self.qimage_to_pil(qimage, max_dimension=1000)
            else:
                # If we've already tried aggressive downsampling, create a small error image
                print("Creating fallback error image")
                error_image = Image.new("RGBA", (400, 300), (255, 0, 0, 128))
                return error_image

    def _alternative_qimage_to_pil(self, qimage: QImage) -> Image.Image:
        """Alternative method to convert QImage to PIL Image when memory is constrained."""
        try:
            # Save to a temporary buffer in PNG format (which is lossless)
            buffer = QBuffer()
            buffer.open(QBuffer.OpenModeFlag.ReadWrite)
            qimage.save(buffer, "PNG", quality=100)
            buffer.seek(0)

            # Load from buffer with PIL
            pil_image = Image.open(io.BytesIO(buffer.data().data()))
            return (
                pil_image.copy()
            )  # Return a copy to ensure the buffer can be released
        except Exception as e:
            print(f"Error converting QImage to PIL Image: {e}")
            # Create a small error image
            error_image = Image.new("RGBA", (400, 300), (255, 0, 0, 128))
            return error_image

    def _create_png_info(self, metadata: dict) -> PngImagePlugin.PngInfo:
        info = PngImagePlugin.PngInfo()
        info.add_text("metadata", json.dumps(metadata))
        return info

    def _on_cancel_requested(self):
        """Handle cancel button click in the progress dialog."""
        self.cancel_requested = True

    def _count_total_sequences(self, dictionary_path: str, word_folders: list) -> int:
        """Count the total number of sequences for progress tracking."""
        total = 0
        for word in word_folders:
            word_path = os.path.join(dictionary_path, word)
            sequences = [
                f
                for f in os.listdir(word_path)
                if f.endswith(".png") and not f.startswith("__")
            ]
            total += len(sequences)
        return total

    def _check_and_manage_memory(self, force_cleanup: bool = False) -> float:
        """
        Check current memory usage and perform cleanup if necessary.

        Args:
            force_cleanup: Force garbage collection regardless of memory usage

        Returns:
            Current memory usage in MB
        """
        try:
            # Get current process memory usage
            process = psutil.Process()
            memory_info = process.memory_info()
            memory_mb = memory_info.rss / (1024 * 1024)

            # Check if we need to clean up
            if force_cleanup or memory_mb > self.max_memory_usage_mb:
                # Force garbage collection
                gc.collect()

                # Update memory usage after cleanup
                memory_info = process.memory_info()
                memory_mb = memory_info.rss / (1024 * 1024)

                # Add a small delay to allow the system to stabilize
                time.sleep(0.1)

            return memory_mb

        except Exception:
            return 0.0

    def _needs_regeneration(
        self, source_path: str, output_path: str
    ) -> tuple[bool, str]:
        """
        Determine if an image needs to be regenerated.

        Args:
            source_path: Path to the source sequence file
            output_path: Path to the output image file

        Returns:
            tuple: (needs_regeneration, reason)
        """
        # If force_regenerate flag is set, always regenerate
        if getattr(self, "force_regenerate", False):
            return True, "Force regeneration requested"

        # If output doesn't exist, we need to generate it
        if not os.path.exists(output_path):
            return True, "Output file does not exist"

        # If source is newer than output, we need to regenerate
        source_mtime = os.path.getmtime(source_path)
        output_mtime = os.path.getmtime(output_path)
        if source_mtime > output_mtime:
            return True, "Source file is newer than output file"

        # Check if output has valid metadata
        try:
            # Extract metadata from output
            output_metadata = self.metadata_extractor.extract_metadata_from_file(
                output_path
            )
            if not output_metadata or "sequence" not in output_metadata:
                return True, "Output file has invalid or missing metadata"

            # Extract metadata from source
            source_metadata = self.metadata_extractor.extract_metadata_from_file(
                source_path
            )
            if not source_metadata or "sequence" not in source_metadata:
                return True, "Source file has invalid or missing metadata"

            # Compare sequence data
            if source_metadata["sequence"] != output_metadata["sequence"]:
                return True, "Sequence data has changed"

            # Check for export options in output metadata
            if "export_options" not in output_metadata:
                return True, "Output file missing export options"

            # All checks passed, no need to regenerate
            return False, "Up to date"

        except Exception as e:
            print(f"Error checking if regeneration is needed: {e}")
            return True, f"Error during check: {str(e)}"

    def _process_sequence_batch(
        self,
        word_folders: list,
        dictionary_path: str,
        export_path: str,
        start_index: int,
        end_index: int,
        processed_sequences: int,
        total_sequences: int,
        regenerated_count: int,
        skipped_count: int,
        failed_count: int,
        length_filter: int | None = None,
    ) -> tuple[int, int, int, int]:
        """
        Process a batch of sequences to limit memory usage.

        Args:
            word_folders: List of word folders to process
            dictionary_path: Path to the dictionary
            export_path: Path to export the images
            start_index: Start index of the batch
            end_index: End index of the batch
            processed_sequences: Number of sequences processed so far
            total_sequences: Total number of sequences to process
            regenerated_count: Number of sequences regenerated so far
            skipped_count: Number of sequences skipped so far
            failed_count: Number of sequences failed so far

        Returns:
            tuple: (processed_sequences, regenerated_count, skipped_count, failed_count)
        """
        # Flatten the list of sequences for batch processing
        all_sequences = []
        for word in word_folders:
            word_path = os.path.join(dictionary_path, word)
            for sequence_file in os.listdir(word_path):
                if sequence_file.endswith(".png") and not sequence_file.startswith(
                    "__"
                ):
                    all_sequences.append((word, sequence_file))

        # Process only the current batch
        batch_sequences = all_sequences[start_index:end_index]

        # Process each sequence in the batch
        for word, sequence_file in batch_sequences:
            if self.cancel_requested:
                break

            word_path = os.path.join(dictionary_path, word)
            sequence_path = os.path.join(word_path, sequence_file)

            # Create word-specific folder in the export directory
            word_export_path = os.path.join(export_path, word)
            os.makedirs(word_export_path, exist_ok=True)

            output_path = os.path.join(word_export_path, sequence_file)

            # Debug: Print where we're trying to save
            if processed_sequences < 3:  # Only print for first few to avoid spam
                print(f"DEBUG: Saving {word}/{sequence_file} to: {output_path}")

            # Check memory usage every few images
            if processed_sequences % self.memory_check_interval == 0:
                self._check_and_manage_memory()

            # Process events to keep UI responsive
            QApplication.processEvents()

            # Check if we need to regenerate this image
            needs_regeneration, reason = self._needs_regeneration(
                sequence_path, output_path
            )

            if needs_regeneration:
                # Extract metadata
                metadata = self.metadata_extractor.extract_metadata_from_file(
                    sequence_path
                )
                if metadata and "sequence" in metadata:
                    sequence = metadata["sequence"]

                    # Apply length filter if specified
                    if length_filter is not None:
                        sequence_length = len(
                            [beat for beat in sequence if beat.get("beat") != 0]
                        )
                        if sequence_length != length_filter:
                            # Skip this sequence - doesn't match the length filter
                            skipped_count += 1
                            processed_sequences += 1
                            continue

                    # Set export options with all required metadata visible
                    options = {
                        "add_word": True,  # Show the word
                        "add_user_info": True,  # Show author info
                        "add_difficulty_level": True,  # Show difficulty level
                        "add_date": True,  # Show date
                        "add_note": True,  # Show any notes
                        "add_beat_numbers": True,  # Show beat numbers
                        "add_reversal_symbols": True,  # Show reversal symbols
                        "combined_grids": False,  # Don't use combined grids
                        "include_start_position": True,  # Include start position
                    }

                    try:
                        # Generate the image
                        self.temp_beat_frame.load_sequence(sequence)
                        qimage = (
                            self.export_manager.image_creator.create_sequence_image(
                                sequence,
                                options,
                                dictionary=False,
                                fullscreen_preview=False,
                            )
                        )

                        # Convert to PIL image for better compression
                        pil_image = self.qimage_to_pil(qimage)

                        # Add metadata to the image
                        metadata["export_options"] = options
                        metadata["export_date"] = datetime.now().isoformat()
                        png_info = self._create_png_info(metadata)

                        # Save with optimized compression
                        pil_image.save(
                            output_path,
                            "PNG",
                            compress_level=self.quality_settings["png_compression"],
                            pnginfo=png_info,
                        )

                        # Debug: Verify the file was actually saved
                        if processed_sequences < 3:  # Only check first few
                            if os.path.exists(output_path):
                                file_size = os.path.getsize(output_path)
                                print(
                                    f"DEBUG: Successfully saved {output_path} ({file_size} bytes)"
                                )
                            else:
                                print(
                                    f"DEBUG: ERROR - File not found after save: {output_path}"
                                )

                        regenerated_count += 1

                    except Exception as e:
                        print(f"DEBUG: Exception saving {output_path}: {e}")
                        import traceback

                        traceback.print_exc()
                        failed_count += 1
                else:
                    failed_count += 1
            else:
                # Skip regeneration
                skipped_count += 1

            processed_sequences += 1

        return processed_sequences, regenerated_count, skipped_count, failed_count
