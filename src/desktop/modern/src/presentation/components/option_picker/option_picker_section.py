from typing import List
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt
from .letter_types import LetterType
from .option_picker_section_header import OptionPickerSectionHeader
from .option_picker_section_pictograph_frame import OptionPickerSectionPictographFrame


class OptionPickerSection(QWidget):
    """
    Refactored Option Picker Section following legacy architecture.

    Components:
    - OptionPickerSectionHeader: Handles header and button
    - OptionPickerSectionPictographFrame: Handles pictograph grid

    This matches the legacy structure for proper sizing.
    """

    def __init__(self, letter_type: str, parent=None, mw_size_provider=None):
        super().__init__(parent)
        self.letter_type = letter_type
        self.mw_size_provider = mw_size_provider
        self.is_groupable = letter_type in [
            LetterType.TYPE4,
            LetterType.TYPE5,
            LetterType.TYPE6,
        ]
        self._last_width = None  # Track width to prevent unnecessary resize
        self._resize_in_progress = False  # Prevent resize cascades
        self._debug_logged = False  # Only log once per major change
        self._setup_ui()

    def _setup_ui(self):
        """Setup UI using legacy-style separation of concerns."""
        # Main layout - legacy style: VBoxLayout with 0 margins and spacing
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create header component
        self.header = OptionPickerSectionHeader(self)
        layout.addWidget(self.header)

        # Create pictograph frame component
        self.pictograph_frame = OptionPickerSectionPictographFrame(self)
        layout.addWidget(self.pictograph_frame)

        # Set transparent background
        self.setStyleSheet("background-color: transparent; border: none;")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # For compatibility, alias the frame as pictograph_container
        self.pictograph_container = self.pictograph_frame
        self.pictograph_layout = self.pictograph_frame.layout
        self.pictographs = self.pictograph_frame.pictographs

        # Access header button for compatibility
        self.header_button = self.header.type_button

    def _get_global_pictograph_size(self) -> int:
        """
        Calculate consistent pictograph size using legacy algorithm.
        Matches legacy option_view.py resize logic exactly.
        """
        if self.mw_size_provider:
            main_window_width = self.mw_size_provider().width()
            section_width = self.width() if self.width() > 0 else main_window_width

            # Legacy algorithm: max(mw_width // 16, option_picker.width() // 8)
            size = max(main_window_width // 16, section_width // 8)

            # Legacy border width calculation: max(1, int(size * 0.015))
            border_width = max(1, int(size * 0.015))

            # Legacy spacing (grid spacing from frame)
            spacing = (
                self.pictograph_frame.layout.spacing()
                if hasattr(self, "pictograph_frame")
                else 3
            )

            # Legacy final calculation: size -= 2 * bw + spacing
            final_size = size - (2 * border_width) - spacing

            # Apply reasonable bounds to prevent extreme sizes
            final_size = max(60, min(final_size, 200))

            return final_size
        else:
            return 100  # Fallback size

    def add_pictograph(self, pictograph_frame):
        """Add pictograph using frame component."""
        self.pictograph_frame.add_pictograph(pictograph_frame)
        self._update_size()

        # Log comprehensive metrics only when pictographs are added
        if len(self.pictograph_frame.pictographs) in [1, 4, 8, 16]:  # Key milestones
            self._log_layout_metrics(
                f"After adding pictograph #{len(self.pictograph_frame.pictographs)}"
            )

    def add_pictograph_from_pool(self, pictograph_frame):
        """Add pictograph from pool using frame component."""
        self.pictograph_frame.add_pictograph_from_pool(pictograph_frame)
        self._update_size()

    def clear_pictographs(self):
        """Clear pictographs using frame component."""
        self.pictograph_frame.clear_pictographs()

    def clear_pictographs_pool_style(self):
        """Clear pictographs using pool style."""
        self.pictograph_frame.clear_pictographs_pool_style()

    def _update_size(self):
        """Update section size using legacy-style calculation."""
        try:
            # Get global pictograph size
            pictograph_size = self._get_global_pictograph_size()

            # Resize pictographs
            self.pictograph_frame.resize_pictographs(pictograph_size)

            # Calculate required heights
            header_height = self.header.get_calculated_height()
            pictograph_height = self.pictograph_frame.calculate_required_height(
                pictograph_size
            )

            # Total section height (legacy style: just header + content)
            total_height = header_height + pictograph_height

            # Set minimum height for section
            self.setMinimumHeight(total_height)

            # Force header to correct size - but don't trigger more resizes
            if hasattr(self.header, "type_button"):
                # Directly set size without triggering resize events
                self.header.type_button._resizing = True
                try:
                    calculated_height = self.header.get_calculated_height()
                    self.header.setFixedHeight(calculated_height)

                    # Size the button without triggering resize
                    if hasattr(self, "mw_size_provider") and self.mw_size_provider:
                        parent_height = self.mw_size_provider().height()
                        font_size = max(parent_height // 70, 10)
                        label_height = max(int(font_size * 3), 20)
                        label_width = max(int(label_height * 6), 100)

                        from PyQt6.QtCore import QSize

                        self.header.type_button.setFixedSize(
                            QSize(label_width, label_height)
                        )
                finally:
                    self.header.type_button._resizing = False

            # Update layout without triggering cascading resizes
            self.updateGeometry()

        except Exception as e:
            print(f"⚠️ [ERROR] Size update failed for {self.letter_type}: {e}")

    def _log_layout_metrics(self, context: str):
        """Log comprehensive layout metrics for comparison with legacy."""
        try:
            if self.mw_size_provider:
                main_window_size = self.mw_size_provider()
                print(f"\n📊 [MODERN METRICS] {self.letter_type} - {context}")
                print(
                    f"   Main Window: {main_window_size.width()}x{main_window_size.height()}"
                )
                print(f"   Section: {self.width()}x{self.height()}")
                print(
                    f"   Frame: {self.pictograph_frame.width()}x{self.pictograph_frame.height()}"
                )
                print(f"   Grid spacing: {self.pictograph_frame.layout.spacing()}px")
                print(f"   Pictograph count: {len(self.pictograph_frame.pictographs)}")
                print(f"   Pictograph size: {self._get_global_pictograph_size()}px")

                # Show section width calculation details
                full_width = main_window_size.width()
                expected_section_width = full_width // 2
                print(
                    f"   Section width calculation: {full_width} // 2 = {expected_section_width}px"
                )
                print(f"   Actual section width: {self.width()}px")

                # Calculate grid utilization
                if len(self.pictograph_frame.pictographs) > 0:
                    rows = (len(self.pictograph_frame.pictographs) - 1) // 8 + 1
                    print(f"   Grid layout: {rows} rows x 8 columns")

                    # Calculate expected vs actual widths
                    pictograph_size = self._get_global_pictograph_size()
                    spacing = self.pictograph_frame.layout.spacing()
                    expected_frame_width = (pictograph_size * 8) + (spacing * 7)
                    utilization = (
                        (expected_frame_width / self.pictograph_frame.width() * 100)
                        if self.pictograph_frame.width() > 0
                        else 0
                    )
                    print(f"   Expected frame width: {expected_frame_width}px")
                    print(f"   Actual frame width: {self.pictograph_frame.width()}px")
                    print(f"   Width utilization: {utilization:.1f}%")
                print(f"   ---")
        except Exception as e:
            print(f"⚠️ [ERROR] Metrics logging failed: {e}")

    def resizeEvent(self, event):
        """Handle resize events using legacy approach."""
        if self._resize_in_progress:
            return

        self._resize_in_progress = True
        try:
            if self.mw_size_provider:
                full_width = self.mw_size_provider().width()

                # Calculate section width based on type
                if self.letter_type in [
                    LetterType.TYPE4,
                    LetterType.TYPE5,
                    LetterType.TYPE6,
                ]:
                    # Bottom row sections - use fixed calculation
                    base_width = full_width // 2
                    COLUMN_COUNT = 8
                    calculated_width = int((base_width / COLUMN_COUNT) - 3)

                    view_width = (
                        calculated_width
                        if calculated_width < self.mw_size_provider().height() // 8
                        else self.mw_size_provider().height() // 8
                    )
                    section_width = full_width // 3
                else:
                    # Top sections - use full width like legacy system
                    section_width = full_width

                # Only resize if width actually changed significantly
                if (
                    self._last_width is None
                    or abs(self._last_width - section_width) > 5
                ):
                    self._last_width = section_width
                    self.setFixedWidth(section_width)

                    # Log only on significant width changes for Types 1-3
                    if not self._debug_logged and self.letter_type in [
                        "Type1",
                        "Type2",
                        "Type3",
                    ]:
                        self._log_layout_metrics("On resize width change")
                        self._debug_logged = True

        except Exception as e:
            print(f"⚠️ [ERROR] Resize failed for {self.letter_type}: {e}")
        finally:
            self._resize_in_progress = False

        super().resizeEvent(event)

    def toggle_section(self):
        """Toggle section visibility."""
        is_visible = not self.pictograph_frame.isVisible()
        self.pictograph_frame.setVisible(is_visible)

    # Properties for compatibility with old code
    @property
    def pictographs(self):
        return self.pictograph_frame.pictographs

    @pictographs.setter
    def pictographs(self, value):
        self.pictograph_frame.pictographs = value
