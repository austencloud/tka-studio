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
from presentation.components.option_picker.components.pictograph_option_frame import (
    PictographOptionFrame,
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
        self._widget_pool: Dict[int, PictographOptionFrame] = {}
        self._loading_options = False

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
            frame = PictographOptionFrame(
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

    def clear_all_sections(self):
        """Clear all pictographs from all sections - Qt widget management."""
        for section in self.sections.values():
            section.clear_pictographs()

        # Reset service pool
        self._option_pool_service.reset_pool()

    def get_section(self, letter_type: LetterType) -> "OptionPickerSection":
        """Get section by letter type."""
        return self.sections.get(letter_type)

    def get_widget_from_pool(self, pool_id: int) -> Optional[PictographOptionFrame]:
        """Get Qt widget from pool by service-provided ID."""
        return self._widget_pool.get(pool_id)

    def _update_size(self):
        """Update picker size using service calculation."""
        # Get the correct container width by traversing up the parent hierarchy
        available_width = self._get_container_width()

        # ✅ Use service for calculation with available container width
        picker_width = self._option_sizing_service.calculate_picker_width(
            available_width
        )

        # ✅ Apply to Qt widget
        self.setFixedWidth(picker_width)

        # MODERN: Update all sections with the new picker width
        self._update_sections_picker_width(picker_width)

    def _get_container_width(self) -> int:
        """Get the correct container width by traversing parent hierarchy."""
        # Try to find the main container (usually 2-3 levels up)
        current = self.parent()
        container_width = None

        # Traverse up to find a substantial container width
        for _ in range(5):  # Limit traversal to prevent infinite loops
            if current is None:
                break

            width = current.width()
            if width > 400:  # Lower threshold to find container sooner
                container_width = width
                break

            current = current.parent()

        # Fallback to main window calculation if no suitable parent found
        if container_width is None:
            main_window_size = self._mw_size_provider()
            container_width = main_window_size.width() // 2

        # Use nearly the full container width (leave small margin for borders)
        return max(300, int(container_width * 0.98))  # Use 98% of container width

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

    def _perform_refresh(self) -> None:
        """Perform refresh with whole-picker fade transition (legacy approach)."""
        if self._pending_sequence_data is None:
            return

        sequence_data = self._pending_sequence_data
        self._pending_sequence_data = None

        try:
            # ✅ Set UI loading state
            self._set_loading_state(True)

            # Check if we have existing content to fade
            existing_sections = [
                section for section in self.sections.values() if section.pictographs
            ]

            if self._animation_orchestrator and existing_sections:
                print(
                    f"🎭 [SCROLL] Starting whole-picker fade transition with {len(existing_sections)} sections"
                )
                self._fade_and_update_all_sections(sequence_data)
            else:
                print(
                    "🎭 [SCROLL] Direct update (no existing content or no animation orchestrator)"
                )
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

            # ✅ Apply sizing using service (defer to avoid blocking)
            from PyQt6.QtCore import QTimer

            QTimer.singleShot(0, self._apply_sizing_to_all_frames)

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

            print(
                f"🎭 [SCROLL] Fading out {len(pictograph_frames)} pictographs (keeping headers)"
            )

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
                print("🎭 [SCROLL] Fade out complete, updating all sections")

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
                print("🎭 [SCROLL] No pictographs to fade in")
                self._set_loading_state(False)
                return

            print(
                f"🎭 [SCROLL] Fading in {len(pictograph_frames)} pictographs (headers stay)"
            )

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
                print("✅ [SCROLL] Pictograph fade transition completed")

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
        # Always get main window size for frame sizing
        main_window_size = self._mw_size_provider()

        # Use current width if available, otherwise calculate from container
        picker_width = self.width()
        if not picker_width:
            # FIXED: Use parent container width instead of main window width
            if self.parent():
                available_width = self.parent().width()
            else:
                # Fallback to main window calculation if no parent
                available_width = main_window_size.width() // 2

            picker_width = self._option_sizing_service.calculate_picker_width(
                available_width
            )

        # ✅ Use service for size calculation
        layout_config = self._option_config_service.get_layout_config()

        # ✅ Apply to Qt widgets in presentation layer
        for section in self.sections.values():
            for frame in section.pictographs.values():
                if hasattr(frame, "resize_option_view"):
                    frame.resize_option_view(
                        main_window_size, picker_width, spacing=layout_config["spacing"]
                    )

    def resizeEvent(self, event):
        """Handle Qt resize events."""
        # Skip resizing during option loading
        if self._loading_options:
            return

        super().resizeEvent(event)
        self._update_size()

    def _on_pictograph_selected(self, pictograph_data: PictographData):
        """Handle pictograph selection - emit Qt signal."""
        self.pictograph_selected.emit(pictograph_data)
