"""
Simplified Option Picker Section Widget - Direct Copy of Legacy Success Pattern

This widget directly copies the successful Legacy OptionPickerSectionWidget pattern,
replacing the over-engineered Modern approach with simple Qt QGroupBox management.

Key principles from Legacy:
- Simple QGroupBox with QVBoxLayout
- Natural Qt sizing with setFixedWidth() in resizeEvent
- Simple pictograph frame (QFrame with QGridLayout)
- No manual height calculations or complex business logic
- Direct pictograph addition without orchestration
"""

from typing import TYPE_CHECKING, Callable, Dict, List, Optional

from application.services.option_picker.option_data_service import OptionDataService
from core.dependency_injection.di_container import DIContainer
from domain.models.pictograph_data import PictographData
from presentation.components.option_picker.core.pictograph_option_frame import (
    PictographOptionFrame,
)
from presentation.components.option_picker.types.letter_types import LetterType
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import QGridLayout, QGroupBox, QHBoxLayout, QVBoxLayout

if TYPE_CHECKING:
    from presentation.components.option_picker.core.option_picker_scroll import (
        OptionPickerScroll,
    )


class OptionPickerSection(QGroupBox):
    """
    Simplified option picker section using Legacy success pattern.

    Direct copy of Legacy OptionPickerSectionWidget with minimal changes for Modern compatibility.
    """

    # Signal emitted when a pictograph is selected in this section
    pictograph_selected = pyqtSignal(object)  # PictographData

    SCROLLBAR_WIDTH = 20

    def __init__(
        self,
        letter_type: LetterType,
        scroll_area: "OptionPickerScroll",
        mw_size_provider: Callable[[], QSize],
        container: Optional[DIContainer] = None,
    ):
        super().__init__(None)
        self.option_scroll = scroll_area
        self.letter_type = letter_type
        self.is_groupable = letter_type in [
            LetterType.TYPE4,
            LetterType.TYPE5,
            LetterType.TYPE6,
        ]
        self.mw_size_provider = mw_size_provider
        self.container = container
        self._debug_logged = False  # Only log once per major change

        # Flag to prevent resizing during option loading (Legacy pattern)
        self._loading_options = False

        # Initialize data service
        self._option_data_service: Optional[OptionDataService] = None

    @property
    def option_data_service(self) -> OptionDataService:
        """Lazy-loaded option data service."""
        if self._option_data_service is None:
            if self.container is None:
                # Fallback: get container from global DI
                from core.dependency_injection import get_container

                container = get_container()
            else:
                container = self.container
            self._option_data_service = OptionDataService(container)
        return self._option_data_service

    def setup_components(self) -> None:
        """Setup components exactly like Legacy."""
        from presentation.components.option_picker.core.pictograph_option_frame import (
            PictographOptionFrame,
        )

        self.pictograph_frame = PictographOptionFrame(self)
        self.pictographs: Dict[str, PictographOptionFrame] = (
            {}
        )  # Will hold real pictograph frames
        self.pictograph_frame.setStyleSheet("QFrame {border: none;}")
        self._setup_header()
        self._setup_layout()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Load real pictographs for this letter type
        self._load_pictographs()

    def _load_pictographs(self) -> None:
        """Load real pictographs based on current sequence state - will be populated by load_options_from_sequence."""
        # This method is now just a placeholder - actual loading happens in load_options_from_sequence
        # when we have the current sequence state to determine valid next options
        pass

    def load_options_from_sequence(
        self, pictographs_for_section: List[PictographData]
    ) -> None:
        """Load actual pictographs for this section based on sequence state."""
        try:
            import time

            from core.monitoring import performance_monitor

            with performance_monitor.profile_block(
                f"section_{self.letter_type}_load_total"
            ):
                # Set loading flag to prevent resize events during loading (Legacy pattern)
                self._loading_options = True

                # Clear existing pictographs
                with performance_monitor.profile_block(
                    f"section_{self.letter_type}_clear"
                ):
                    self.clear_pictographs()

                print(
                    f"🎨 [PICTOGRAPH_LOADING] {self.letter_type}: Loading {len(pictographs_for_section)} real options"
                )

                # Batch create all frames first (without adding to layout to avoid redundant resizing)
                with performance_monitor.profile_block(
                    f"section_{self.letter_type}_create_frames"
                ):
                    frames = []
                    for i, pictograph_data in enumerate(pictographs_for_section):
                        frame_start = time.perf_counter()

                        option_frame = PictographOptionFrame(parent=self)
                        create_time = (time.perf_counter() - frame_start) * 1000

                        update_start = time.perf_counter()
                        option_frame.update_pictograph(pictograph_data)
                        update_time = (time.perf_counter() - update_start) * 1000

                        # Connect selection signal
                        option_frame.option_selected.connect(
                            self._on_pictograph_selected
                        )

                        frames.append(option_frame)

                        # Log timing for first frame only to reduce overhead
                        if i == 0:
                            print(
                                f"🔍 [FRAME_TIMING] {self.letter_type}[{i}]: create={create_time:.1f}ms, update={update_time:.1f}ms"
                            )

                # Batch add all frames to layout (minimizes resize events)
                with performance_monitor.profile_block(
                    f"section_{self.letter_type}_add_to_layout"
                ):
                    for frame in frames:
                        self.add_pictograph(frame)

                # Note: Sizing will be applied once at the end by scroll widget (Legacy pattern)
                # No individual frame resizing during loading

                # Clear loading flag
                self._loading_options = False

        except Exception as e:
            # Clear loading flag on error too
            self._loading_options = False
            print(
                f"❌ [PICTOGRAPH_LOADING] Error loading options for {self.letter_type}: {e}"
            )

    def _get_max_pictographs_for_type(self) -> int:
        """Get maximum number of pictographs to load for this letter type."""
        # All sections get exactly 6 pictographs for a total of 36 options
        return 6  # 6 sections × 6 pictographs = 36 total options

    def _on_pictograph_selected(self, pictograph_data: PictographData) -> None:
        """Handle pictograph selection and emit signal upward."""
        print(f"🎯 [SELECTION] Pictograph selected: {pictograph_data.letter}")
        # Emit signal to parent (OptionPickerScroll)
        self.pictograph_selected.emit(pictograph_data)

    def _setup_layout(self) -> None:
        """Setup layout for header + horizontal pictographs."""
        # Main vertical layout for header + pictographs
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Grid layout for pictographs (will be added after header) - allows wrapping
        self.pictographs_layout: QGridLayout = QGridLayout()
        self.pictographs_layout.setSpacing(5)
        self.pictographs_layout.setContentsMargins(0, 0, 0, 0)

        # Add header first, then grid layout for pictographs
        self.layout.addWidget(self.header)
        self.layout.addLayout(self.pictographs_layout)

    def _setup_header(self) -> None:
        """Setup header exactly like Legacy."""
        from presentation.components.option_picker.core.option_picker_section_header import (
            OptionPickerSectionHeader,
        )

        self.header = OptionPickerSectionHeader(self)
        self.header.type_button.clicked.connect(self.toggle_section)

    def toggle_section(self) -> None:
        """Toggle section visibility exactly like Legacy."""
        is_visible = not self.pictograph_frame.isVisible()
        self.pictograph_frame.setVisible(is_visible)

    def clear_pictographs(self) -> None:
        """Clear pictographs from grid layout."""
        for pictograph_frame in self.pictographs.values():
            if hasattr(pictograph_frame, "setVisible"):
                self.pictographs_layout.removeWidget(pictograph_frame)
                pictograph_frame.setVisible(False)
                # Return pictograph to pool instead of deleting
                if hasattr(pictograph_frame, "cleanup"):
                    pictograph_frame.cleanup()
                pictograph_frame.deleteLater()  # Clean up the frame widget
        self.pictographs = {}

    def add_pictograph(self, pictograph_frame: "PictographOptionFrame") -> None:
        """Add pictograph to grid layout with proper positioning."""
        # Generate a simple key for the pictograph
        key = f"pictograph_{len(self.pictographs)}"
        self.pictographs[key] = pictograph_frame

        # Calculate grid position (8 columns like Legacy)
        COLUMN_COUNT = 8
        count = len(self.pictographs)
        row, col = divmod(count - 1, COLUMN_COUNT)

        # Add to the grid layout
        self.pictographs_layout.addWidget(pictograph_frame, row, col)
        pictograph_frame.setVisible(True)

    def add_pictographs_from_pool(self, pictograph_frames: list) -> None:
        """Add multiple pictographs from pool - simplified version."""
        for frame in pictograph_frames:
            self.add_pictograph(frame)

    def _batch_resize_pictograph_frames(self, frames: list):
        """Batch resize all pictograph frames using Legacy sizing strategy."""
        if not frames:
            return

        # Calculate sizing once for all frames (Legacy pattern)
        main_window_size = self.mw_size_provider()
        option_picker_width = self.option_scroll.width()

        # If option picker width is not available, fall back to main window calculation
        if option_picker_width <= 0:
            option_picker_width = main_window_size.width() // 2

        # Apply sizing to all frames at once
        for frame in frames:
            if hasattr(frame, "resize_option_view"):
                frame.resize_option_view(
                    main_window_size, option_picker_width, spacing=3
                )

    def _resize_pictograph_frame(self, pictograph_frame: "PictographOptionFrame"):
        """Resize single pictograph frame - only used for window resize events."""
        if hasattr(pictograph_frame, "resize_option_view"):
            # Get sizing information
            main_window_size = self.mw_size_provider()
            option_picker_width = self.option_scroll.width()

            # If option picker width is not available, fall back to main window calculation
            if option_picker_width <= 0:
                option_picker_width = main_window_size.width() // 2

            # Apply Legacy sizing
            pictograph_frame.resize_option_view(
                main_window_size, option_picker_width, spacing=3
            )

    @property
    def pictograph_frames(self) -> List:
        """Get list of pictograph frames for compatibility with tests."""
        return list(self.pictographs.values())

    def resizeEvent(self, event) -> None:
        """Resize exactly like Legacy - simple and fast."""
        # Skip resizing during option loading (Legacy pattern)
        if self._loading_options:
            return

        # Legacy pattern: Use main window width // 2 (simple calculation)
        width = self.mw_size_provider().width() // 2

        if self.letter_type in [LetterType.TYPE1, LetterType.TYPE2, LetterType.TYPE3]:
            # Individual sections: use full width (Legacy pattern)
            self.setFixedWidth(width)

        elif self.letter_type in [LetterType.TYPE4, LetterType.TYPE5, LetterType.TYPE6]:
            # Grouped sections: Legacy calculation
            COLUMN_COUNT = 8  # Legacy constant
            calculated_width = int((width / COLUMN_COUNT) - 3)  # Legacy spacing

            view_width = (
                calculated_width
                if calculated_width < self.mw_size_provider().height() // 8
                else self.mw_size_provider().height() // 8
            )
            final_width = int(view_width * 8) // 3
            self.setFixedWidth(final_width)

        # Call super once at the end (Legacy pattern)
        super().resizeEvent(event)
