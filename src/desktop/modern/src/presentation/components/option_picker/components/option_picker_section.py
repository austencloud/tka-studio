"""
Option Picker Section Widget - Clean UI Layer

Pure Qt presentation component for displaying option sections.
All business logic extracted to injected services.

Key principles:
- Pure Qt UI logic only - no business logic
- Clean dependency injection of services
- Qt widget management in presentation layer
- Simple section layout and display
"""

import asyncio
from typing import Callable, Dict, List, Optional

from application.services.option_picker.option_configuration_service import (
    OptionConfigurationService,
)
from application.services.option_picker.option_picker_size_calculator import (
    OptionPickerSizeCalculator,
)
from application.services.option_picker.option_pool_service import OptionPoolService
from core.interfaces.animation_core_interfaces import (
    AnimationConfig,
    EasingType,
    IAnimationOrchestrator,
)
from domain.models.pictograph_data import PictographData
from presentation.components.option_picker.components.option_picker_scroll import (
    OptionPickerScroll,
)
from presentation.components.option_picker.components.option_pictograph import (
    OptionPictograph,
)
from presentation.components.option_picker.types.letter_types import LetterType
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QGridLayout, QGroupBox, QVBoxLayout


class OptionPickerSection(QGroupBox):
    """
    Clean UI component for option picker sections.

    All business logic extracted to injected services.
    """

    # Signal emitted when a pictograph is selected in this section
    pictograph_selected = pyqtSignal(object)  # PictographData

    def __init__(
        self,
        letter_type: LetterType,
        scroll_area,  # Parent scroll area
        mw_size_provider: Optional[
            Callable[[], QSize]
        ] = None,  # Made optional since we use scroll area width
        option_pool_service: OptionPoolService = None,
        option_config_service: OptionConfigurationService = None,
        size_calculator: OptionPickerSizeCalculator = None,
        animation_orchestrator: Optional[IAnimationOrchestrator] = None,
    ):
        """Initialize with injected services - no service location."""
        super().__init__(None)

        # ✅ Clean dependency injection - no service location
        self.letter_type = letter_type
        self.scroll_area: OptionPickerScroll = scroll_area
        self.mw_size_provider = mw_size_provider
        self._option_pool_service = option_pool_service
        self._option_config_service = option_config_service
        self._option_sizing_service = size_calculator
        self._animation_orchestrator = animation_orchestrator

        # Store the current option picker width (updated via signal)

        # UI state management
        self._loading_options = False
        self._ui_initialized = False  # Track if UI components are ready
        self._scroll_area_ready = False  # Track if scroll area has valid dimensions
        self.pictographs: Dict[str, OptionPictograph] = {}

    def update_option_picker_width(self, width: int) -> None:
        """Update the stored option picker width - called by parent scroll area."""
        # Store the width (though we primarily use scroll area width now)
        self.option_picker_width = width

        # ✅ Use service for business rule
        self.is_groupable = self._option_config_service.is_groupable_type(
            self.letter_type
        )

        # Check if scroll area is now ready for sizing
        self._check_scroll_area_readiness()

    def _check_scroll_area_readiness(self) -> None:
        """Check if scroll area has valid dimensions and mark as ready."""
        if not self._ui_initialized:
            return

        if hasattr(self, "scroll_area") and self.scroll_area:
            scroll_width = self.scroll_area.width()
            parent_width = (
                self.scroll_area.parent().width() if self.scroll_area.parent() else 0
            )

            # More robust validation - check if we have a reasonable width that's not the default
            is_reasonable_width = (
                scroll_width > 800
            )  # Should be much larger than 640px default
            is_not_default = scroll_width != 640  # Avoid the default fallback value
            has_parent_width = (
                parent_width > 800
            )  # Parent should also be properly sized

            print(
                f"🔍 [SIZING] {self.letter_type} width check: scroll={scroll_width}px, parent={parent_width}px"
            )
            print(
                f"🔍 [SIZING] {self.letter_type} validation: reasonable={is_reasonable_width}, not_default={is_not_default}, parent_ok={has_parent_width}"
            )

            if is_reasonable_width and is_not_default and has_parent_width:
                if not self._scroll_area_ready:
                    print(
                        f"✅ [SIZING] {self.letter_type} scroll area ready: {scroll_width}px (parent: {parent_width}px)"
                    )
                    self._scroll_area_ready = True
                    # Trigger a resize now that we're ready
                    self._perform_delayed_resize()
            else:
                print(
                    f"⏳ [SIZING] {self.letter_type} scroll area not ready: {scroll_width}px (waiting for proper layout)"
                )

    def _perform_delayed_resize(self) -> None:
        """Perform resize calculation now that scroll area is ready."""
        if not self._scroll_area_ready or not self._ui_initialized:
            return

        scroll_area_width = self.scroll_area.width()
        print(
            f"🔍 [RESIZE] {self.letter_type} performing delayed resize with width: {scroll_area_width}px"
        )

        # Calculate dimensions using only scroll area width
        dimensions = self._option_sizing_service.calculate_section_dimensions(
            letter_type=self.letter_type,
            main_window_width=scroll_area_width,  # Use scroll area width directly
        )

        print(f"📊 [CALC] {self.letter_type} calculated width: {dimensions['width']}px")

        # Apply the calculated width
        self.setFixedWidth(dimensions["width"])

        # Show actual dimensions after Qt applies them
        from PyQt6.QtCore import QTimer

        QTimer.singleShot(10, self._show_actual_dimensions)

    def setup_components(self) -> None:
        """Setup Qt components - pure UI logic."""
        # Create container frame for pictographs
        self.pictograph_frame = QFrame(self)
        self.pictograph_frame.setStyleSheet("QFrame {border: none;}")

        self._setup_header()
        self._setup_layout()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Mark UI as initialized
        self._ui_initialized = True
        self._check_scroll_area_readiness()

    def _setup_layout(self) -> None:
        """Setup Qt layout - pure UI logic."""
        # Main vertical layout for header + pictographs
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Get layout config from service
        layout_config = self._option_config_service.get_layout_config()

        # Grid layout for pictographs
        self.pictographs_layout: QGridLayout = QGridLayout()
        self.pictographs_layout.setSpacing(layout_config["spacing"])
        self.pictographs_layout.setContentsMargins(0, 0, 0, 0)

        # Add header first, then grid layout for pictographs
        self.layout.addWidget(self.header)
        self.layout.addLayout(self.pictographs_layout)

    def _setup_header(self) -> None:
        """Setup section header - Qt UI logic."""
        from presentation.components.option_picker.components.option_picker_section_header import (
            OptionPickerSectionHeader,
        )

        self.header = OptionPickerSectionHeader(self)
        self.header.type_button.clicked.connect(self.toggle_section)

    def toggle_section(self) -> None:
        """Toggle section visibility - Qt UI logic."""
        is_visible = not self.pictograph_frame.isVisible()
        self.pictograph_frame.setVisible(is_visible)

    def load_options_from_sequence(
        self, pictographs_for_section: List[PictographData]
    ) -> None:
        """Load options for this section with modern animation transitions."""
        try:
            # ✅ Set UI loading state
            self._loading_options = True

            # Get existing frames for fade out
            existing_frames = list(self.pictographs.values())

            # Use modern animation system if available, otherwise fall back to direct update
            if self._animation_orchestrator and existing_frames:
                # Modern animated transition (replicates legacy fade_and_update behavior)
                print(
                    f"🎭 [FADE] Starting fade transition for {self.letter_type} with {len(existing_frames)} existing frames"
                )
                # Use simple Qt-based fade animation (no asyncio)
                try:
                    from PyQt6.QtCore import (
                        QParallelAnimationGroup,
                        QPropertyAnimation,
                        QTimer,
                    )
                    from PyQt6.QtWidgets import QGraphicsOpacityEffect

                    print(
                        f"🎭 [FADE] Starting Qt-based fade transition for {self.letter_type}"
                    )

                    # Step 1: Create fade out animations for existing frames
                    fade_out_group = QParallelAnimationGroup(
                        self
                    )  # Parent to this widget to prevent GC
                    animations_added = 0

                    for frame in existing_frames:
                        try:
                            # Create opacity effect if not present
                            if not frame.graphicsEffect():
                                effect = QGraphicsOpacityEffect()
                                effect.setOpacity(1.0)  # Ensure it starts visible
                                frame.setGraphicsEffect(effect)

                            # Create fade out animation
                            animation = QPropertyAnimation(
                                frame.graphicsEffect(), b"opacity"
                            )
                            animation.setDuration(200)  # 200ms
                            animation.setStartValue(1.0)
                            animation.setEndValue(0.0)
                            fade_out_group.addAnimation(animation)
                            animations_added += 1

                        except Exception as e:
                            print(
                                f"❌ [FADE] Failed to create animation for frame: {e}"
                            )

                    print(
                        f"🎭 [FADE] Created {animations_added} fade out animations for {self.letter_type}"
                    )

                    # Step 2: When fade out completes, update content and fade in
                    def on_fade_out_complete():

                        # Update content
                        self.clear_pictographs()
                        self._load_options_directly(pictographs_for_section)

                        # Step 3: Fade in new frames
                        QTimer.singleShot(
                            50, self._fade_in_new_frames
                        )  # Small delay for content update

                    # Store reference to prevent garbage collection
                    self._current_fade_animation = fade_out_group

                    fade_out_group.finished.connect(on_fade_out_complete)

                    # Add debug for animation start/state

                    fade_out_group.start()

                except Exception as e:
                    print(f"❌ [FADE] Qt fade animation failed: {e}")
                    # Fallback to direct update
                    self.clear_pictographs()
                    self._load_options_directly(pictographs_for_section)
            else:
                self._load_options_directly(pictographs_for_section)

        except Exception as e:
            print(f"❌ [UI] Error loading options for {self.letter_type}: {e}")
        finally:
            # ✅ Always clear loading state
            self._loading_options = False

    def _fade_in_new_frames(self):
        """Fade in newly loaded frames."""
        try:
            from PyQt6.QtCore import QParallelAnimationGroup, QPropertyAnimation
            from PyQt6.QtWidgets import QGraphicsOpacityEffect

            new_frames = list(self.pictographs.values())
            if not new_frames:
                print(f"🎭 [FADE] No new frames to fade in for {self.letter_type}")
                return

            print(
                f"🎭 [FADE] Fading in {len(new_frames)} new frames for {self.letter_type}"
            )

            # Create fade in animations for new frames
            fade_in_group = QParallelAnimationGroup(self)  # Parent to prevent GC

            for frame in new_frames:
                # Create opacity effect if not present
                if not frame.graphicsEffect():
                    effect = QGraphicsOpacityEffect()
                    frame.setGraphicsEffect(effect)
                    effect.setOpacity(0.0)  # Start invisible

                # Create fade in animation
                animation = QPropertyAnimation(frame.graphicsEffect(), b"opacity")
                animation.setDuration(200)  # 200ms
                animation.setStartValue(0.0)
                animation.setEndValue(1.0)
                fade_in_group.addAnimation(animation)

            # When fade in completes
            def on_fade_in_complete():
                print(f"✅ [FADE] Fade transition completed for {self.letter_type}")

            fade_in_group.finished.connect(on_fade_in_complete)
            fade_in_group.start()

        except Exception as e:
            print(f"❌ [FADE] Fade in failed for {self.letter_type}: {e}")

    async def _load_with_fade_transition(
        self,
        pictographs_for_section: List[PictographData],
        existing_frames: List[OptionPictograph],
    ) -> None:
        """Load options with smooth fade transition (replicates legacy behavior)."""
        try:
            print(f"🎭 [FADE] _load_with_fade_transition called for {self.letter_type}")
            # Animation config matching legacy timing (200ms)
            config = AnimationConfig(
                duration=0.2, easing=EasingType.EASE_IN_OUT  # 200ms to match legacy
            )

            # Fade out existing frames
            if existing_frames:
                fade_out_tasks = []
                for frame in existing_frames:
                    if frame.isVisible():
                        task = self._animation_orchestrator.fade_target(
                            frame, fade_in=False, config=config
                        )
                        fade_out_tasks.append(task)

                # Wait for all fade outs to complete
                if fade_out_tasks:
                    await asyncio.gather(*fade_out_tasks)

            # Update content (equivalent to legacy callback)
            self._update_pictograph_content(pictographs_for_section)

            # Fade in new frames
            new_frames = list(self.pictographs.values())
            if new_frames:
                fade_in_tasks = []
                for frame in new_frames:
                    if frame.isVisible():
                        task = self._animation_orchestrator.fade_target(
                            frame, fade_in=True, config=config
                        )
                        fade_in_tasks.append(task)

                # Start all fade ins
                if fade_in_tasks:
                    await asyncio.gather(*fade_in_tasks)

        except Exception as e:
            print(
                f"❌ [ANIMATION] Error in fade transition for {self.letter_type}: {e}"
            )
            # Fallback to direct update
            self._load_options_directly(pictographs_for_section)

    def _load_options_directly(
        self, pictographs_for_section: List[PictographData]
    ) -> None:
        """Direct option loading without animation (fallback)."""
        # ✅ Clear existing UI elements
        self.clear_pictographs()
        self._update_pictograph_content(pictographs_for_section)

    def _update_pictograph_content(
        self, pictographs_for_section: List[PictographData]
    ) -> None:
        """Update pictograph content (extracted for reuse in animation and direct modes)."""
        # ✅ Create and setup Qt widgets
        frames = []
        for pictograph_data in pictographs_for_section:
            # Get widget from pool using service
            pool_id = self._option_pool_service.checkout_item()
            if pool_id is not None:
                # Get Qt widget from scroll area's widget pool
                option_frame = self.scroll_area.get_widget_from_pool(pool_id)
                if option_frame:
                    # Setup Qt widget
                    option_frame.update_pictograph(pictograph_data)

                    # CRITICAL: Disconnect any existing connections first to prevent duplicates
                    try:
                        option_frame.option_selected.disconnect(
                            self._on_pictograph_selected
                        )
                    except (TypeError, RuntimeError):
                        # No existing connection - this is fine
                        pass

                    option_frame.option_selected.connect(self._on_pictograph_selected)
                    frames.append(option_frame)

        # ✅ Add Qt widgets to layout
        for frame in frames:
            self.add_pictograph(frame)

    def clear_pictographs(self) -> None:
        """Clear pictographs from Qt layout."""
        for pictograph_frame in self.pictographs.values():
            if hasattr(pictograph_frame, "setVisible"):
                # Remove from Qt layout
                self.pictographs_layout.removeWidget(pictograph_frame)
                pictograph_frame.setVisible(False)

                # Disconnect our specific signal connection safely
                try:
                    pictograph_frame.option_selected.disconnect(
                        self._on_pictograph_selected
                    )
                except (TypeError, RuntimeError):
                    # Signal was already disconnected or never connected - this is fine
                    pass

                # Clean up widget content
                pictograph_frame.clear_pictograph()

                # Return to pool (find pool ID)
                for pool_id, widget in self.scroll_area._widget_pool.items():
                    if widget == pictograph_frame:
                        self._option_pool_service.checkin_item(pool_id)
                        break

        # Clear tracking dictionary
        self.pictographs = {}

    def add_pictograph(self, pictograph_frame: OptionPictograph) -> None:
        """Add pictograph to Qt grid layout."""
        # Generate tracking key
        key = f"pictograph_{len(self.pictographs)}"
        self.pictographs[key] = pictograph_frame

        # ✅ Use service for grid layout calculation
        layout_config = self._option_config_service.get_layout_config()
        column_count = layout_config["column_count"]

        # Calculate grid position
        count = len(self.pictographs)
        row, col = divmod(count - 1, column_count)

        # ✅ Add to Qt grid layout
        self.pictographs_layout.addWidget(pictograph_frame, row, col)
        pictograph_frame.setVisible(True)

    def _on_pictograph_selected(self, pictograph_data: PictographData) -> None:
        """Handle pictograph selection - emit Qt signal."""
        self.pictograph_selected.emit(pictograph_data)

    def resizeEvent(self, event) -> None:
        """Handle Qt resize events with proper initialization checks."""
        # Skip resizing during option loading
        if self._loading_options:
            return

        # NEW: Only proceed if UI is properly initialized and scroll area is ready
        if not self._ui_initialized:
            print(
                f"⏳ [SIZING] {self.letter_type} UI not ready for sizing, deferring..."
            )
            return

        # Check if scroll area is ready, and if not, try to make it ready
        if not self._scroll_area_ready:
            self._check_scroll_area_readiness()
            if not self._scroll_area_ready:
                print(
                    f"⏳ [SIZING] {self.letter_type} scroll area not ready, deferring..."
                )
                return

        # If we get here, everything is ready - perform the resize
        self._perform_delayed_resize()

        # Call parent resize event
        super().resizeEvent(event)

    def _show_actual_dimensions(self) -> None:
        """Show actual widget dimensions after Qt applies them."""
        actual_width = self.width()
        actual_height = self.height()
        print(
            f"✅ [ACTUAL] {self.letter_type} final size: {actual_width}x{actual_height}px"
        )

        # Also show pictograph frame dimensions if available
        if hasattr(self, "pictographs") and self.pictographs:
            first_frame = next(iter(self.pictographs.values()))
            frame_width = first_frame.width()
            frame_height = first_frame.height()
            print(f"✅ [ACTUAL] First pictograph frame: {frame_width}x{frame_height}px")

            # Calculate if 8 frames + spacing fit within section width
            spacing = 3  # From config
            total_frames_width = 8 * frame_width + 7 * spacing
            fits = total_frames_width <= actual_width
            print(
                f"✅ [ACTUAL] 8 frames fit? {fits} (need {total_frames_width}px, have {actual_width}px)"
            )

    @property
    def pictograph_frames(self) -> List[OptionPictograph]:
        """Get list of pictograph frames for compatibility."""
        return list(self.pictographs.values())
