"""
Simplified Option Picker Widget - Clean UI Layer

Pure Qt presentation component with business logic extracted to services.
Uses dependency injection for clean separation of concerns.

Key principles:
- Pure Qt UI logic only - no business logic
- Clean dependency injection of services
- Qt widget management in presentation layer
- Coordination between UI and services
"""

from typing import TYPE_CHECKING, Callable, Dict, Optional

from application.services.option_picker.option_picker_size_calculator import (
    OptionPickerSizeCalculator,
)
from application.services.option_picker.option_pool_service import OptionPoolService
from application.services.option_picker.sequence_option_service import (
    SequenceOptionService,
)
from application.services.pictograph_pool_manager import PictographPoolManager
from core.interfaces.animation_core_interfaces import IAnimationOrchestrator
from domain.models.pictograph_data import PictographData
from domain.models.sequence_data import SequenceData
from presentation.components.option_picker.components.option_pictograph import (
    OptionPictograph,
)
from presentation.components.option_picker.types.letter_types import LetterType
from PyQt6.QtCore import QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QScrollArea, QVBoxLayout, QWidget

if TYPE_CHECKING:
    from application.services.option_picker.option_configuration_service import (
        OptionConfigurationService,
    )
    from presentation.components.option_picker.components.option_picker_section import (
        OptionPickerSection,
    )


class OptionPickerScroll(QScrollArea):
    """
    Clean UI component for option picker.

    All business logic extracted to injected services.
    """

    # Signal emitted when a pictograph is selected in any section
    pictograph_selected = pyqtSignal(object)  # PictographData

    def __init__(
        self,
        sequence_option_service: SequenceOptionService,
        option_pool_service: OptionPoolService,
        option_sizing_service: OptionPickerSizeCalculator,
        option_config_service: "OptionConfigurationService",
        pictograph_pool_manager: "PictographPoolManager",
        parent=None,
        mw_size_provider: Callable[[], QSize] = None,
        animation_orchestrator: Optional[IAnimationOrchestrator] = None,
    ):
        """Initialize with injected services - no service location."""
        super().__init__(parent)

        # ✅ Clean dependency injection - no service location
        self._sequence_option_service = sequence_option_service
        self._option_pool_service = option_pool_service
        self._option_sizing_service = option_sizing_service
        self._option_config_service = option_config_service
        self._pictograph_pool_manager = pictograph_pool_manager
        self._animation_orchestrator = animation_orchestrator

        self._mw_size_provider = mw_size_provider or self._default_size_provider

        # Qt widget management - presentation layer responsibility
        self._widget_pool: Dict[int, OptionPictograph] = {}
        self._loading_options = False
        self._is_preparing_for_transition = False

        # UI setup
        self._setup_layout()
        self._initialize_widget_pool()
        self._initialize_sections()
        self._setup_ui_properties()

        # Debounced refresh setup
        debounce_delay = self._option_config_service.get_debounce_delay()
        self._refresh_timer = QTimer()
        self._refresh_timer.setSingleShot(True)
        self._refresh_timer.timeout.connect(self._perform_refresh)
        self._pending_sequence_data = None

        # Fade transition state
        self._pending_fade_sequence_data = None
        self._pending_fade_pictograph_frames = None

        # Set initial size
        # self._update_size()

    @property
    def mw_size_provider(self) -> Callable[[], QSize]:
        """Get the main window size provider."""
        return self._mw_size_provider

    @mw_size_provider.setter
    def mw_size_provider(self, value: Callable[[], QSize]):
        """Set the main window size provider and update all sections."""
        self._mw_size_provider = value
        # CRITICAL: Update all existing sections with the new size provider
        if hasattr(self, "sections"):
            for section in self.sections.values():
                section.mw_size_provider = value

    def _default_size_provider(self) -> QSize:
        """Default size provider if none provided."""
        return QSize(800, 600)

    def _setup_layout(self):
        """Setup Qt layout - pure UI logic."""
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

        # FIXED: Ensure container fills the full scroll area width
        from PyQt6.QtWidgets import QSizePolicy

        self.container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )

        self.container.setLayout(self.layout)
        self.setWidget(self.container)

    def _setup_ui_properties(self):
        """Setup Qt-specific UI properties."""
        # Disable scroll bars like Legacy
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Enable scroll bars for content overflow
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Transparency setup
        self.viewport().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def _initialize_widget_pool(self):
        """Initialize Qt widget pool with proper dependency injection."""
        max_widgets = self._option_config_service.get_total_max_pictographs()

        # ✅ Create Qt widgets with injected pictograph components
        for i in range(max_widgets):
            # Get pictograph component from pool service
            pictograph_component = self._pictograph_pool_manager.checkout_pictograph(
                parent=self
            )

            # Create frame with injected dependencies (component + size calculator)
            frame = OptionPictograph(
                parent=self,
                pictograph_component=pictograph_component,
                size_calculator=self._option_sizing_service,
            )
            frame.hide()  # CRITICAL: Hide frames initially to prevent random display
            self._widget_pool[i] = frame

        # Initialize service pool with same IDs
        self._option_pool_service.reset_pool()

    def _initialize_sections(self) -> None:
        """Create and add sections - Qt layout management."""
        from presentation.components.option_picker.components.group_widget import (
            OptionPickerGroupWidget,
        )
        from presentation.components.option_picker.components.option_picker_section import (
            OptionPickerSection,
        )

        self.sections: Dict[LetterType, "OptionPickerSection"] = {}
        groupable_sections = []

        for letter_type in LetterType.ALL_TYPES:
            # Pass services to sections via dependency injection
            section = OptionPickerSection(
                letter_type=letter_type,
                scroll_area=self,
                mw_size_provider=self._mw_size_provider,
                option_pool_service=self._option_pool_service,
                option_config_service=self._option_config_service,
                size_calculator=self._option_sizing_service,
                animation_orchestrator=self._animation_orchestrator,
            )
            self.sections[letter_type] = section
            section.setup_components()

            # Connect Qt signals
            section.pictograph_selected.connect(self._on_pictograph_selected)

            # Organize sections by grouping (business rule from config service)
            if self._option_config_service.is_groupable_type(letter_type):
                groupable_sections.append(section)
            else:
                self.layout.addWidget(section)

        # Group sections if any are groupable
        if groupable_sections:
            group_widget = OptionPickerGroupWidget(self)
            for section in groupable_sections:
                group_widget.add_section_widget(section)

            # FIXED: Remove stretches that center the group widget
            # This allows the group to use the full available width
            self.layout.addWidget(group_widget)

        # Add balanced spacing after all sections are created
        # This creates equal spacing between header and sections, and between each section
        print(
            f"🔧 [INIT] Checking for header widget... hasattr: {hasattr(self, 'header_widget')}, widget: {getattr(self, 'header_widget', None)}"
        )
        if hasattr(self, "header_widget") and self.header_widget:
            print("🔧 [INIT] Calling _add_balanced_spacing...")
            self._add_balanced_spacing()
        else:
            print("🔧 [INIT] No header widget found, skipping balanced spacing")

    def add_header_label(self, header_widget: QWidget) -> None:
        """Add a header label widget at the top of the scroll area with balanced spacing."""
        # Store the header widget for later use in layout balancing
        self.header_widget = header_widget

        # Insert the header at the very top of the layout
        self.layout.insertWidget(0, header_widget)

        # Don't add initial stretch here - let _add_balanced_spacing handle all stretches

        # Call balanced spacing now that we have the header
        print("🔧 [HEADER] Header added, calling _add_balanced_spacing...")
        self._add_balanced_spacing()

    def _add_balanced_spacing(self):
        """Add balanced spacing between header-section pairs."""
        # Create spacing between header-section PAIRS, not individual elements
        # Each header should hug its section, with equal spacing between the pairs
        print("🔧 [SPACING] Setting up header-section pair spacing...")

        # Step 1: Remove all existing stretches
        items_to_remove = []
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            if item and item.spacerItem():
                items_to_remove.append(item)

        print(f"🔧 [SPACING] Removing {len(items_to_remove)} existing stretches...")
        for item in items_to_remove:
            self.layout.removeItem(item)

        # Step 2: Identify all widgets in layout order
        all_widgets = []
        for i in range(self.layout.count()):
            item = self.layout.itemAt(i)
            if item and item.widget():
                all_widgets.append((i, item.widget()))

        print(f"🔧 [SPACING] Found {len(all_widgets)} total widgets in layout")

        # Step 3: Find the last widget in each header-section pair
        # This is where we'll add stretches to separate the pairs
        pair_end_indices = []

        for i, (index, widget) in enumerate(all_widgets):
            # Skip the main header
            if widget == self.header_widget:
                continue

            # Check if this is a section widget (end of a pair)
            if (
                hasattr(widget, "letter_type")
                or "OptionPickerGroupWidget" in str(type(widget))
                or "OptionPickerSection" in str(type(widget))
            ):
                pair_end_indices.append(index)

        print(
            f"🔧 [SPACING] Found {len(pair_end_indices)} header-section pairs ending at indices: {pair_end_indices}"
        )

        # Step 4: Add stretches after each pair (work backwards to preserve indices)
        for pair_end_index in reversed(pair_end_indices):
            self.layout.insertStretch(pair_end_index + 1)
            print(
                f"🔧 [SPACING] Added stretch after pair ending at index {pair_end_index}"
            )

        # Step 5: Add initial stretch after main header to push first pair down
        header_index = -1
        for i, (index, widget) in enumerate(all_widgets):
            if widget == self.header_widget:
                header_index = index
                break

        if header_index >= 0:
            self.layout.insertStretch(header_index + 1)
            print(
                f"🔧 [SPACING] Added initial stretch after main header at index {header_index}"
            )

        print(
            f"🔧 [SPACING] Header-section pair spacing complete! Final layout count: {self.layout.count()}"
        )

    def clear_all_sections(self):
        """Clear all pictographs from all sections - Qt widget management."""
        for section in self.sections.values():
            section.clear_pictographs()

        # Reset service pool
        self._option_pool_service.reset_pool()

    def get_section(self, letter_type: LetterType) -> "OptionPickerSection":
        """Get section by letter type."""
        return self.sections.get(letter_type)

    def get_widget_from_pool(self, pool_id: int) -> Optional[OptionPictograph]:
        """Get Qt widget from pool by service-provided ID."""
        return self._widget_pool.get(pool_id)

    def _update_size(self):
        """Update picker size using service calculation."""
        # FIXED: Use immediate parent width instead of traversing up hierarchy
        if self.parent():
            # Use the immediate parent's width - this ensures we fit within our container
            available_width = self.parent().width()
            print(f"🔍 [SIZING] Using immediate parent width: {available_width}px")
        else:
            # Fallback to main window calculation if no parent
            main_window_size = self._mw_size_provider()
            available_width = main_window_size.width() // 2
            print(f"🔍 [SIZING] No parent, using MW/2: {available_width}px")

        # Validate that we have a reasonable width (not the default 640px)
        if available_width <= 640:
            print(
                f"⚠️ [SIZING] Parent width {available_width}px seems too small, checking main window..."
            )
            main_window_size = self._mw_size_provider()
            if main_window_size.width() > 1000:
                # Use half the main window width as a better estimate
                available_width = main_window_size.width() // 2
                print(f"🔍 [SIZING] Using main window half-width: {available_width}px")

        # The scroll area should fit exactly within its parent's width
        picker_width = available_width

        print(
            f"🔍 [SIZING] Setting scroll area width to: {picker_width}px (parent: {available_width}px)"
        )

        # DEBUG: Check container width vs scroll area width
        container_width = self.container.width() if hasattr(self, "container") else 0
        print(
            f"🔍 [CONTAINER] Container width: {container_width}px vs Scroll area: {picker_width}px"
        )

        # ✅ Apply to Qt widget - constrain to parent width
        self.setFixedWidth(picker_width)

        # FIXED: Ensure container also uses full width
        if hasattr(self, "container"):
            print(
                f"🔍 [CONTAINER] Setting container width to match scroll area: {picker_width}px"
            )
            # Don't use setFixedWidth as it might interfere with scroll area resizing
            # Instead, ensure the container's minimum width matches the scroll area
            self.container.setMinimumWidth(picker_width)

        # MODERN: Update all sections with the new picker width
        self._update_sections_picker_width(picker_width)

    def _update_sections_picker_width(self, picker_width: int) -> None:
        """Update all sections with the current picker width - modern dependency injection."""
        for section in self.sections.values():
            if hasattr(section, "update_option_picker_width"):
                section.update_option_picker_width(picker_width)

    def load_options_from_sequence(self, sequence_data: SequenceData) -> None:
        """Load options with debouncing - UI coordination logic."""
        self._pending_sequence_data = sequence_data

        # Get debounce delay from config service
        delay = self._option_config_service.get_debounce_delay()
        self._refresh_timer.start(delay)

    def prepare_for_transition(self) -> None:
        """Prepare content for widget transition by loading without fade animations."""
        self._is_preparing_for_transition = True
        try:
            # If we have pending sequence data, load it directly without fades
            if self._pending_sequence_data:
                sequence_data = self._pending_sequence_data
                self._pending_sequence_data = None
                self._update_all_sections_directly(sequence_data)
        finally:
            self._is_preparing_for_transition = False

    def _perform_refresh(self) -> None:
        """Perform refresh with whole-picker fade transition (legacy approach)."""
        if self._pending_sequence_data is None:
            return

        sequence_data = self._pending_sequence_data
        self._pending_sequence_data = None

        try:
            # ✅ Set UI loading state
            self._set_loading_state(True)

            # Skip fade animations if preparing for widget transition
            if self._is_preparing_for_transition:
                self._update_all_sections_directly(sequence_data)
                return

            # Check if we have existing content to fade
            existing_sections = [
                section for section in self.sections.values() if section.pictographs
            ]

            if self._animation_orchestrator and existing_sections:

                self._fade_and_update_all_sections(sequence_data)
            else:

                self._update_all_sections_directly(sequence_data)

        except Exception as e:
            print(f"❌ [UI] Error during refresh: {e}")
            import traceback

            traceback.print_exc()

    def _update_all_sections_directly(self, sequence_data: SequenceData) -> None:
        """Update all sections directly without animation (optimized for fade callback)."""
        try:
            # ✅ Use service to get options (pure business logic)
            options_by_type = self._sequence_option_service.get_options_for_sequence(
                sequence_data
            )

            if not options_by_type:
                print("❌ [UI] No options received from service")
                return

            # ✅ Update UI sections with options (bypass individual section animations)
            # Temporarily disable all section animations for performance
            original_orchestrators = {}
            for letter_type, section in self.sections.items():
                original_orchestrators[letter_type] = section._animation_orchestrator
                section._animation_orchestrator = None

            # Update all sections quickly
            for letter_type, section in self.sections.items():
                section_options = options_by_type.get(letter_type, [])
                section.load_options_from_sequence(section_options)

            # Restore animation orchestrators
            for letter_type, section in self.sections.items():
                section._animation_orchestrator = original_orchestrators[letter_type]

            # ✅ Apply sizing using service (defer with longer delay during startup)
            # Use longer delay during sequence restoration to ensure UI is fully initialized
            delay = 500 if self._is_during_startup() else 50
            QTimer.singleShot(delay, self._apply_sizing_to_all_frames)

        except Exception as e:
            print(f"❌ [UI] Error in direct update: {e}")

    def _fade_and_update_all_sections(self, sequence_data: SequenceData) -> None:
        """Fade pictographs only (keeping headers stable) - improved approach."""
        try:
            from PyQt6.QtCore import QParallelAnimationGroup, QPropertyAnimation, QTimer
            from PyQt6.QtWidgets import QGraphicsOpacityEffect

            # Get all pictograph frames (not the whole sections)
            pictograph_frames = []
            for section in self.sections.values():
                if section.pictographs:
                    pictograph_frames.extend(section.pictographs.values())

            if not pictograph_frames:
                self._update_all_sections_directly(sequence_data)
                return

            # Step 1: Create fade out animation group for pictographs only
            fade_out_group = QParallelAnimationGroup(self)

            for frame in pictograph_frames:
                # Ensure opacity effect exists
                if not frame.graphicsEffect():
                    effect = QGraphicsOpacityEffect()
                    effect.setOpacity(1.0)
                    frame.setGraphicsEffect(effect)

                # Create fade out animation
                animation = QPropertyAnimation(frame.graphicsEffect(), b"opacity")
                animation.setDuration(200)  # 200ms like legacy
                animation.setStartValue(1.0)
                animation.setEndValue(0.0)
                fade_out_group.addAnimation(animation)

            # Step 2: When fade out completes, update content and fade in (with tiny buffer)
            def on_fade_out_complete():

                # Add tiny delay to ensure fade out animation fully completes
                # This prevents the freeze/pause issue during fade out
                from PyQt6.QtCore import QTimer

                QTimer.singleShot(10, self._complete_fade_transition)

            # Store sequence data for the delayed callback
            self._pending_fade_sequence_data = sequence_data
            self._pending_fade_pictograph_frames = pictograph_frames

            fade_out_group.finished.connect(on_fade_out_complete)
            fade_out_group.start()

        except Exception as e:
            print(f"❌ [SCROLL] Fade transition failed: {e}")
            # Fallback to direct update
            self._update_all_sections_directly(sequence_data)

    def _complete_fade_transition(self) -> None:
        """Complete the fade transition after ensuring fade out is fully done."""
        try:
            sequence_data = self._pending_fade_sequence_data
            pictograph_frames = self._pending_fade_pictograph_frames

            # Clear graphics effects from old pictographs
            if pictograph_frames:
                for frame in pictograph_frames:
                    if frame.graphicsEffect():
                        frame.setGraphicsEffect(None)

            # Update content
            self._update_all_sections_directly(sequence_data)

            # Start fade in for new pictographs
            self._fade_in_all_pictographs()

        except Exception as e:
            print(f"❌ [SCROLL] Failed to complete fade transition: {e}")
        finally:
            # Clean up pending data
            self._pending_fade_sequence_data = None
            self._pending_fade_pictograph_frames = None

    def _fade_in_all_pictographs(self) -> None:
        """Fade in pictographs only (keeping headers stable) - improved approach."""
        try:
            from PyQt6.QtCore import QParallelAnimationGroup, QPropertyAnimation
            from PyQt6.QtWidgets import QGraphicsOpacityEffect

            # Get all new pictograph frames
            pictograph_frames = []
            for section in self.sections.values():
                if section.pictographs:
                    pictograph_frames.extend(section.pictographs.values())

            if not pictograph_frames:
                self._set_loading_state(False)
                return

            # Create fade in animation group for pictographs only
            fade_in_group = QParallelAnimationGroup(self)

            for frame in pictograph_frames:
                # Ensure opacity effect exists and is set to 0
                if not frame.graphicsEffect():
                    effect = QGraphicsOpacityEffect()
                    effect.setOpacity(0.0)
                    frame.setGraphicsEffect(effect)

                # Create fade in animation
                animation = QPropertyAnimation(frame.graphicsEffect(), b"opacity")
                animation.setDuration(200)  # 200ms like legacy
                animation.setStartValue(0.0)
                animation.setEndValue(1.0)
                fade_in_group.addAnimation(animation)

            def on_fade_in_complete():

                # Clear graphics effects after fade in completes (like legacy)
                for frame in pictograph_frames:
                    if frame.graphicsEffect():
                        frame.setGraphicsEffect(None)

            fade_in_group.finished.connect(on_fade_in_complete)
            fade_in_group.start()

        except Exception as e:
            print(f"❌ [SCROLL] Pictograph fade in failed: {e}")
        finally:
            # ✅ Always clear loading state
            self._set_loading_state(False)

    def _set_loading_state(self, loading: bool):
        """Set loading state for UI - prevents resize events during loading."""
        self._loading_options = loading

        # Propagate to sections
        for section in self.sections.values():
            if hasattr(section, "_loading_options"):
                section._loading_options = loading

    def _apply_sizing_to_all_frames(self):
        """Apply sizing to all frames using service calculations."""
        # Check if UI is properly initialized before applying sizing
        if not self._is_ui_ready_for_sizing():
            print("⏳ [SIZING] UI not ready for sizing, deferring...")
            # Defer sizing until UI is ready
            QTimer.singleShot(100, self._apply_sizing_to_all_frames)
            return

        # Always get main window size for frame sizing
        main_window_size = self._mw_size_provider()

        # FIXED: Use actual widget width like legacy, not calculated width
        picker_width = self.width()

        # Enhanced validation for accurate width
        if not self._is_picker_width_accurate(picker_width, main_window_size):
            print(
                f"⚠️ [SIZING] Option picker width {picker_width}px appears inaccurate, deferring sizing..."
            )
            # Defer sizing until we get an accurate width
            QTimer.singleShot(200, self._apply_sizing_to_all_frames)
            return

        print(f"✅ [SIZING] Using validated option picker width: {picker_width}px")

        # ✅ Use service for size calculation
        layout_config = self._option_config_service.get_layout_config()

        # ✅ Apply to Qt widgets in presentation layer
        for section in self.sections.values():
            for frame in section.pictographs.values():
                if hasattr(frame, "resize_option_view"):
                    frame.resize_option_view(
                        main_window_size, picker_width, spacing=layout_config["spacing"]
                    )

    def _is_ui_ready_for_sizing(self) -> bool:
        """Check if the UI is ready for accurate sizing calculations."""
        try:
            # Check if main window is visible and properly initialized
            main_window = self.window()
            if not main_window:
                return False

            # Check if main window is visible (not during splash screen)
            if not main_window.isVisible():
                return False

            # Check if this widget is visible and has been shown
            if not self.isVisible():
                return False

            # Check if widget has been properly sized (not default/zero size)
            if self.width() <= 0 or self.height() <= 0:
                return False

            return True

        except Exception as e:
            print(f"⚠️ [SIZING] Error checking UI readiness: {e}")
            return False

    def _is_picker_width_accurate(self, picker_width: int, main_window_size) -> bool:
        """Check if the picker width appears accurate and not from premature measurement."""
        try:
            # Width should be positive
            if picker_width <= 0:
                return False

            # Width should be reasonable relative to main window
            main_window_width = main_window_size.width()
            if main_window_width <= 0:
                return False

            # Picker width should be between 20% and 80% of main window width
            # (typical range for option picker in a layout)
            min_expected = main_window_width * 0.2
            max_expected = main_window_width * 0.8

            if not (min_expected <= picker_width <= max_expected):
                print(
                    f"⚠️ [SIZING] Picker width {picker_width}px outside expected range "
                    f"[{min_expected:.0f}-{max_expected:.0f}px] for main window {main_window_width}px"
                )
                return False

            # Additional check: avoid the specific problematic width mentioned (622px)
            # This suggests the widget was measured during an intermediate layout state
            if picker_width == 622:
                print(
                    f"⚠️ [SIZING] Detected problematic width {picker_width}px, likely from startup timing issue"
                )
                return False

            return True

        except Exception as e:
            print(f"⚠️ [SIZING] Error validating picker width: {e}")
            return False

    def _is_during_startup(self) -> bool:
        """Check if we're currently during application startup phase."""
        try:
            # Check if main window is not yet visible (splash screen phase)
            main_window = self.window()
            if not main_window or not main_window.isVisible():
                return True

            # Check if this widget hasn't been properly shown yet
            if not self.isVisible() or self.width() <= 0:
                return True

            return False

        except Exception:
            # If we can't determine, assume we're during startup to be safe
            return True

    def resizeEvent(self, event):
        """Handle Qt resize events."""
        # Skip resizing during option loading
        if self._loading_options:
            return

        super().resizeEvent(event)

        # Debug: Log resize event details
        print(f"🔍 [RESIZE] Option picker resize event: {self.width()}x{self.height()}")

        self._update_size()

    def _on_pictograph_selected(self, pictograph_data: PictographData):
        """Handle pictograph selection - emit Qt signal."""
        self.pictograph_selected.emit(pictograph_data)
