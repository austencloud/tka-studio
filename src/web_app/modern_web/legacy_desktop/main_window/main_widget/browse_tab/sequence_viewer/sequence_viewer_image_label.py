from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QSizePolicy

if TYPE_CHECKING:
    from .sequence_viewer import SequenceViewer


class SequenceViewerImageLabel(QLabel):
    def __init__(self, sequence_viewer: SequenceViewer):
        super().__init__(sequence_viewer)
        self.sequence_viewer = sequence_viewer
        self._original_pixmap: QPixmap | None = None

        # Set up logging
        import logging

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # MODERN APPROACH: Let Qt handle scaling automatically
        self.setScaledContents(True)

        # CRITICAL FIX: Use Fixed size policy and fixed maximum size to prevent infinite expansion
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        # Set a FIXED maximum size that never changes - this prevents infinite expansion
        self._setup_fixed_size_constraints()

        self.logger.info("🔧 SequenceViewerImageLabel initialized")

    def _setup_fixed_size_constraints(self):
        """Set up intelligent size constraints that use full width but prevent window expansion."""
        # Calculate the optimal size based on sequence viewer's available space
        optimal_width, max_height = self._calculate_optimal_dimensions()

        self.logger.info("🔧 Setting up intelligent size constraints:")
        self.logger.info(f"   📐 Optimal size: {optimal_width}x{max_height}")

        # Set size constraints that use full width but limit height
        self.setMinimumSize(200, 200)  # Reasonable minimum
        self.setMaximumSize(optimal_width, max_height)  # Prevent expansion

        # Use preferred size instead of fixed size for better layout flexibility
        self.resize(optimal_width, max_height)

        self.logger.info(
            f"   📏 Size constraints set: min=200x200, max={optimal_width}x{max_height}"
        )
        self.logger.info("   ✅ Full width usage with height constraints applied!")

    def _calculate_optimal_dimensions(self) -> tuple[int, int]:
        """Calculate optimal dimensions for the sequence viewer image."""
        try:
            # Get the sequence viewer's available width (it gets 1/3 of browse tab)
            sequence_viewer = self.sequence_viewer

            # Calculate available width with padding
            padding = 20  # Small padding for aesthetics
            available_width = max(200, sequence_viewer.width() - padding)

            # Calculate maximum height to prevent window expansion
            # Use a reasonable percentage of main widget height
            main_widget_height = sequence_viewer.main_widget.height()
            max_height_ratio = 0.6  # Use up to 60% of main widget height
            max_height = max(200, int(main_widget_height * max_height_ratio))

            # For square images, use the smaller dimension to maintain aspect ratio
            # But prioritize using full width if height allows
            optimal_size = min(available_width, max_height)

            self.logger.debug(
                f"Calculated optimal dimensions: width={available_width}, "
                f"max_height={max_height}, optimal_size={optimal_size}"
            )

            return available_width, optimal_size  # Use full width, constrained height

        except Exception as e:
            self.logger.warning(f"Error calculating optimal dimensions: {e}")
            # Fallback to reasonable defaults
            return 400, 400

    def set_pixmap_with_scaling(self, pixmap: QPixmap):
        """MODERN APPROACH: Set pixmap once, let Qt handle scaling."""
        self.logger.info("🖼️ Setting pixmap with scaling:")
        self.logger.info(
            f"   📐 Widget size before: {self.size().width()}x{self.size().height()}"
        )
        self.logger.info(f"   🖼️ Pixmap size: {pixmap.width()}x{pixmap.height()}")

        self._original_pixmap = pixmap

        # Simply set the pixmap - Qt will scale it automatically with setScaledContents(True)
        self.setPixmap(pixmap)

        self.logger.info(
            f"   📐 Widget size after: {self.size().width()}x{self.size().height()}"
        )

    def resizeEvent(self, event):
        """Handle resize events and recalculate size constraints if needed."""
        old_size = event.oldSize()
        new_size = event.size()

        self.logger.debug("🚨 RESIZE EVENT DETECTED:")
        self.logger.debug(f"   📐 Old size: {old_size.width()}x{old_size.height()}")
        self.logger.debug(f"   📐 New size: {new_size.width()}x{new_size.height()}")

        # Only recalculate if this is a significant size change from parent resize
        if old_size.isValid():
            width_change = abs(old_size.width() - new_size.width())
            if width_change > 20:  # Significant change in parent layout
                self.logger.debug(
                    "Significant size change detected - recalculating constraints"
                )
                self._recalculate_size_constraints()

        super().resizeEvent(event)

    def _recalculate_size_constraints(self):
        """Recalculate size constraints when parent layout changes."""
        try:
            optimal_width, max_height = self._calculate_optimal_dimensions()

            # Update maximum size constraints
            self.setMaximumSize(optimal_width, max_height)

            # Resize to new optimal size if current size is significantly different
            current_size = self.size()
            if (
                abs(current_size.width() - optimal_width) > 20
                or abs(current_size.height() - max_height) > 20
            ):
                self.resize(optimal_width, max_height)

            self.logger.debug(
                f"Size constraints recalculated: max={optimal_width}x{max_height}"
            )

        except Exception as e:
            self.logger.warning(f"Error recalculating size constraints: {e}")

    def recalculate_size_for_layout_change(self):
        """Public method to recalculate size when sequence viewer layout changes."""
        self.logger.debug("Recalculating size for layout change")
        self._recalculate_size_constraints()

    def _calculate_available_space(self) -> tuple[int, int]:
        sequence_viewer = self.sequence_viewer
        available_height = int(sequence_viewer.main_widget.height() * 0.65)
        available_width = int(sequence_viewer.main_widget.width() * 1 / 3 * 0.95)

        return available_width, available_height

    def set_pixmap_to_fit(self):
        """LEGACY METHOD - Now handled by modern setScaledContents approach."""
        # This method is kept for compatibility but no longer does manual scaling
        # The modern approach uses setScaledContents(True) to let Qt handle scaling
        if self._original_pixmap:
            self.setPixmap(self._original_pixmap)

    def update_thumbnail(self, index: int):
        if not self.sequence_viewer.state.thumbnails:
            return

        self.set_pixmap_with_scaling(
            QPixmap(self.sequence_viewer.state.thumbnails[index])
        )
        self.sequence_viewer.variation_number_label.update_index(index)

    def _create_ultra_high_quality_scaled_pixmap(
        self, target_width: int, target_height: int
    ) -> QPixmap:
        """Create ultra high-quality scaled pixmap for sequence viewer using advanced techniques."""
        if not self._original_pixmap:
            return QPixmap()

        original_size = self._original_pixmap.size()
        target_size = QSize(target_width, target_height)

        # Calculate scale factor
        scale_factor = min(
            target_width / original_size.width(), target_height / original_size.height()
        )

        # SEQUENCE VIEWER ULTRA QUALITY: Use multi-step scaling for large images
        if scale_factor < 0.6:
            # Multi-step scaling for better quality when scaling down significantly
            intermediate_factor = 0.75  # Scale to 75% first, then to target
            intermediate_size = QSize(
                int(original_size.width() * intermediate_factor),
                int(original_size.height() * intermediate_factor),
            )

            # Step 1: Scale to intermediate size with high quality
            intermediate_pixmap = self._original_pixmap.scaled(
                intermediate_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            # Step 2: Scale to final size with high quality
            final_pixmap = intermediate_pixmap.scaled(
                target_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            return final_pixmap
        else:
            # Single-step high-quality scaling for smaller scale changes
            return self._original_pixmap.scaled(
                target_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
