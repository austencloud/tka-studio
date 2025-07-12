"""
Simplified Option Picker Widget - Direct Copy of Legacy Success Pattern

This widget directly copies the successful Legacy OptionScroll pattern,
replacing the over-engineered Modern approach with simple Qt layout management.

Key principles from Legacy:
- Simple QScrollArea with QVBoxLayout
- Individual sections (Types 1-3) added directly to layout
- Grouped sections (Types 4-6) in horizontal layout
- Natural Qt sizing without business logic interference
- No manual height calculations or complex orchestration
"""

from typing import TYPE_CHECKING, Callable, Dict, Optional

from core.dependency_injection.di_container import DIContainer
from domain.models.pictograph_data import PictographData
from domain.models.sequence_data import SequenceData
from presentation.components.option_picker.types.letter_types import LetterType
from PyQt6.QtCore import QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QHBoxLayout, QScrollArea, QVBoxLayout, QWidget

if TYPE_CHECKING:
    from presentation.components.option_picker.core.option_picker_section import (
        OptionPickerSection,
    )


class OptionPickerScroll(QScrollArea):
    """
    Simplified option picker widget using Legacy success pattern.

    Direct copy of Legacy OptionScroll with minimal changes for Modern compatibility.
    """

    # Signal emitted when a pictograph is selected in any section
    pictograph_selected = pyqtSignal(object)  # PictographData

    spacing = 3
    layout: QVBoxLayout
    container: QWidget
    sections: Dict[LetterType, "OptionPickerSection"] = {}

    def __init__(
        self,
        parent=None,
        mw_size_provider: Callable[[], QSize] = None,
        container: Optional[DIContainer] = None,
    ):
        super().__init__(parent)
        self.mw_size_provider = mw_size_provider or self._default_size_provider
        self.container = container

        # Flag to prevent ALL resizing during option loading (Legacy pattern)
        self._loading_options = False

        self._setup_layout()
        self._initialize_sections()
        # Disable scroll bars like Legacy
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Set initial size like Legacy: half the main window width
        self._update_size()

        # Add debouncing for performance optimization
        self._refresh_timer = QTimer()
        self._refresh_timer.setSingleShot(True)
        self._refresh_timer.timeout.connect(self._perform_refresh)
        self._pending_sequence_data = None

    def _default_size_provider(self) -> QSize:
        """Default size provider if none provided."""
        return QSize(800, 600)

    def _setup_layout(self):
        """Setup layout exactly like Legacy OptionScroll."""
        self.setWidgetResizable(True)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: transparent; border: none;")

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.container = QWidget()
        self.container.setAutoFillBackground(True)
        self.container.setStyleSheet("background: transparent;")
        self.container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.container.setLayout(self.layout)
        self.setWidget(self.container)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.viewport().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def _initialize_sections(self) -> None:
        """Create and add sections exactly like Legacy pattern."""
        from presentation.components.option_picker.core.group_widget import (
            OptionPickerGroupWidget,
        )
        from presentation.components.option_picker.core.option_picker_section import (
            OptionPickerSection,
        )

        groupable_sections = []
        for letter_type in LetterType.ALL_TYPES:
            section = OptionPickerSection(
                letter_type, self, self.mw_size_provider, self.container
            )
            self.sections[letter_type] = section
            section.setup_components()

            # Connect section's pictograph selection signal to scroll widget
            section.pictograph_selected.connect(self._on_pictograph_selected)

            if section.is_groupable:
                groupable_sections.append(section)
            else:
                self.layout.addWidget(section)

        if groupable_sections:
            group_widget = OptionPickerGroupWidget(self)
            for section in groupable_sections:
                group_widget.add_section_widget(section)

            group_layout = QHBoxLayout()
            group_layout.addStretch()
            group_layout.addWidget(group_widget)
            group_layout.addStretch()
            self.layout.addLayout(group_layout, 3)

    def clear_all_sections(self):
        """Clear all pictographs from all sections."""
        for section in self.sections.values():
            section.clear_pictographs()

    def get_section(self, letter_type: LetterType) -> "OptionPickerSection":
        """Get section by letter type."""
        return self.sections.get(letter_type)

    def _update_size(self):
        """Update the option picker size like Legacy: half the main window width."""
        main_window_size = self.mw_size_provider()
        option_picker_width = main_window_size.width() // 2

        # Debug logging
        print(
            f"\n🔧 [OPTION_PICKER_SIZING] Main window: {main_window_size.width()}x{main_window_size.height()}"
        )
        print(
            f"🔧 [OPTION_PICKER_SIZING] Calculated option picker width: {option_picker_width}"
        )
        print(f"🔧 [OPTION_PICKER_SIZING] Previous option picker width: {self.width()}")

        # Set fixed width like Legacy option picker
        self.setFixedWidth(option_picker_width)

        print(f"🔧 [OPTION_PICKER_SIZING] New option picker width: {self.width()}")
        print(
            f"🔧 [OPTION_PICKER_SIZING] Expected sections - Individual: {option_picker_width}, Grouped: {option_picker_width // 3} each"
        )

    def resizeEvent(self, event):
        """Handle resize events to maintain proper sizing."""
        # Skip ALL resizing during option loading (Legacy pattern)
        if self._loading_options:
            return

        super().resizeEvent(event)
        # Update our size when parent resizes
        self._update_size()

        # Only update sections on actual window resize, not during option loading
        # This follows Legacy pattern of only resizing on window events

    def _update_grouped_sections(self):
        """Legacy pattern: Let Qt handle section sizing naturally - no manual resizeEvent calls."""
        # Legacy doesn't manually call resizeEvent during option loading
        # Qt will handle section resizing automatically on actual window resize events
        pass

    def load_options_from_sequence(self, sequence_data) -> None:
        """Load actual options based on current sequence state with debouncing."""
        # Store the sequence data and start/restart the timer
        self._pending_sequence_data = sequence_data
        self._refresh_timer.start(50)  # 50ms debounce delay

    def _perform_refresh(self) -> None:
        """Perform the actual refresh with the pending sequence data."""
        if self._pending_sequence_data is None:
            return

        sequence_data = self._pending_sequence_data
        self._pending_sequence_data = None

        try:
            import time

            from core.monitoring import performance_monitor

            start_time = time.perf_counter()

            # Start comprehensive profiling
            with performance_monitor.profile_block("option_picker_refresh_total"):

                # Set loading flag to prevent resizing during option loading (Legacy pattern)
                with performance_monitor.profile_block("set_loading_flags"):
                    self._loading_options = True
                    for section in self.sections.values():
                        if hasattr(section, "_loading_options"):
                            section._loading_options = True

                print(
                    f"🔄 [OPTION_REFRESH] Starting refresh for sequence: {type(sequence_data)}"
                )

                # Get the position matcher service to find valid next options
                with performance_monitor.profile_block("resolve_position_matcher"):
                    from application.services.positioning.arrows.utilities.pictograph_position_matcher import (
                        PictographPositionMatcher,
                    )
                    from core.dependency_injection.di_container import get_container

                    container = get_container()
                    position_matcher = container.resolve(PictographPositionMatcher)

                    if not position_matcher:
                        print(
                            "❌ [OPTION_LOADING] Could not resolve PictographPositionMatcher"
                        )
                        return

                # Extract end position from sequence data
                with performance_monitor.profile_block("extract_end_position"):
                    end_position = self._extract_end_position(sequence_data)
                    if not end_position:
                        print(
                            "❌ [OPTION_LOADING] Could not extract end position from sequence"
                        )
                        return

                # Get all valid next options (should be exactly 36)
                with performance_monitor.profile_block("get_next_options"):
                    all_options = position_matcher.get_next_options(end_position)
                    print(
                        f"🎯 [OPTION_LOADING] Found {len(all_options)} total options for position {end_position}"
                    )

                # Distribute options based on actual letter type of each pictograph
                with performance_monitor.profile_block("group_options_by_type"):
                    from domain.models.letter_type_classifier import (
                        LetterTypeClassifier,
                    )

                    # Group options by their actual letter type
                    options_by_type = {}
                    for option in all_options:
                        letter = option.letter
                        if letter:
                            letter_type = LetterTypeClassifier.get_letter_type(letter)
                            if letter_type not in options_by_type:
                                options_by_type[letter_type] = []
                            options_by_type[letter_type].append(option)

                    print(
                        f"🎯 [OPTION_DISTRIBUTION] Options by type: {[(t, len(opts)) for t, opts in options_by_type.items()]}"
                    )

                # Load options into their corresponding sections
                with performance_monitor.profile_block("load_options_into_sections"):
                    for letter_type, section in self.sections.items():
                        section_options = options_by_type.get(letter_type, [])
                        section.load_options_from_sequence(section_options)

                # Clear loading flags and apply sizing once at the end (Legacy pattern)
                with performance_monitor.profile_block("clear_flags_and_apply_sizing"):
                    # Apply sizing to all frames once at the end (Legacy pattern)
                    self._apply_sizing_to_all_frames()

                    # Clear loading flags after sizing (Legacy pattern)
                    self._loading_options = False
                    for section in self.sections.values():
                        if hasattr(section, "_loading_options"):
                            section._loading_options = False

                # Performance logging
                total_time = (time.perf_counter() - start_time) * 1000
                print(f"✅ [OPTION_REFRESH] Completed in {total_time:.1f}ms")

                # Print performance summary
                try:
                    summary = performance_monitor.get_performance_summary()
                    if summary and "operations" in summary:
                        print("🔍 [PERFORMANCE_BREAKDOWN]:")
                        for op in summary["operations"][-20:]:  # Last 20 operations
                            if "option_picker" in op.get("operation", "").lower():
                                print(
                                    f"   {op['operation']}: {op['duration_ms']:.1f}ms"
                                )
                except Exception as e:
                    print(f"⚠️ [PERFORMANCE] Could not get summary: {e}")

        except Exception as e:
            # Clear loading flags on error too
            self._loading_options = False
            for section in self.sections.values():
                if hasattr(section, "_loading_options"):
                    section._loading_options = False
            print(f"❌ [OPTION_LOADING] Error loading options from sequence: {e}")

    def _apply_sizing_to_all_frames(self):
        """Apply sizing to all frames once at the end (Legacy pattern)."""
        import time

        start_time = time.perf_counter()

        # Calculate sizing once for all frames
        calc_start = time.perf_counter()
        main_window_size = self.mw_size_provider()
        option_picker_width = self.width()

        if option_picker_width <= 0:
            option_picker_width = main_window_size.width() // 2
        calc_time = (time.perf_counter() - calc_start) * 1000
        print(f"🔍 [SIZING_BREAKDOWN] Size calculation: {calc_time:.1f}ms")

        # Apply to all frames in all sections
        apply_start = time.perf_counter()
        frame_count = 0
        for section in self.sections.values():
            for frame in section.pictographs.values():
                if hasattr(frame, "resize_option_view"):
                    frame.resize_option_view(
                        main_window_size, option_picker_width, spacing=3
                    )
                    frame_count += 1
        apply_time = (time.perf_counter() - apply_start) * 1000
        total_time = (time.perf_counter() - start_time) * 1000

        print(
            f"🔍 [SIZING_BREAKDOWN] Applied sizing to {frame_count} frames: {apply_time:.1f}ms"
        )
        print(f"🔍 [SIZING_BREAKDOWN] Total sizing time: {total_time:.1f}ms")

    def _extract_end_position(self, sequence_data: SequenceData) -> str:
        """Extract end position from sequence data."""
        try:
            print(
                f"🔍 [END_POS] Extracting from sequence: length={sequence_data.length if hasattr(sequence_data, 'length') else 'N/A'}"
            )
            print(
                f"🔍 [END_POS] Sequence beats count: {len(sequence_data.beats) if hasattr(sequence_data, 'beats') and sequence_data.beats else 0}"
            )

            # If sequence has no beats, use alpha1
            if not sequence_data or sequence_data.length == 0:
                print(f"🔍 [END_POS] Empty sequence, returning alpha1")
                return "alpha1"  # Default start position

            # If sequence only has start position (no actual beats), use alpha1
            if not sequence_data.beats or len(sequence_data.beats) == 0:
                print(f"🔍 [END_POS] No beats in sequence, returning alpha1")
                return "alpha1"

            # Get the last beat from the beats list
            if sequence_data.beats:
                last_beat = sequence_data.beats[-1]
                print(f"🔍 [END_POS] Last beat type: {type(last_beat)}")
                print(
                    f"🔍 [END_POS] Last beat has pictograph_data: {hasattr(last_beat, 'pictograph_data')}"
                )

                # BeatData objects have pictograph_data with end_pos
                if hasattr(last_beat, "pictograph_data") and last_beat.pictograph_data:
                    end_pos = last_beat.pictograph_data.end_position
                    print(f"🔍 [END_POS] Found end_pos: {end_pos}")
                    return end_pos or "alpha1"
                # Fallback for dict-based data
                elif isinstance(last_beat, dict) and "end_pos" in last_beat:
                    end_pos = last_beat["end_pos"]
                    print(f"🔍 [END_POS] Found dict end_pos: {end_pos}")
                    return end_pos
                elif isinstance(last_beat, dict) and "end_position" in last_beat:
                    end_pos = last_beat["end_position"]
                    print(f"🔍 [END_POS] Found dict end_position: {end_pos}")
                    return end_pos
                else:
                    print(f"🔍 [END_POS] No end position found in beat")

            print(f"🔍 [END_POS] Falling back to alpha1")
            return "alpha1"  # Default fallback

        except Exception as e:
            print(f"❌ [OPTION_LOADING] Error extracting end position: {e}")
            return "alpha1"

    def _on_pictograph_selected(self, pictograph_data: PictographData):
        """Handle pictograph selection from any section and forward signal."""
        print(f"🎯 [SCROLL] Forwarding pictograph selection: {pictograph_data.letter}")
        self.pictograph_selected.emit(pictograph_data)
