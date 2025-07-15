"""
ConstructTabLayoutManager

Handles UI layout setup, panel creation, and widget management for the construct tab.
Responsible for creating the main layout structure and organizing UI components.
"""

from typing import TYPE_CHECKING, Callable, Optional

from core.dependency_injection.di_container import DIContainer
from core.interfaces.animation_core_interfaces import IAnimationOrchestrator
from presentation.components.option_picker.components.option_picker import OptionPicker
from presentation.components.right_panel_tabs.right_panel_tab_widget import (
    RightPanelTabWidget,
)
from presentation.components.start_position_picker.start_position_picker import (
    PickerMode,
    StartPositionPicker,
)
from presentation.factories.workbench_factory import create_modern_workbench
from PyQt6.QtCore import (
    QEasingCurve,
    QParallelAnimationGroup,
    QPropertyAnimation,
    Qt,
    QTimer,
)
from PyQt6.QtWidgets import (
    QGraphicsOpacityEffect,
    QHBoxLayout,
    QLabel,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

if TYPE_CHECKING:
    from presentation.components.sequence_workbench.sequence_beat_frame.sequence_beat_frame import (
        SequenceBeatFrame,
    )


class ConstructTabLayoutManager:
    """
    Manages the UI layout and panel creation for the construct tab.

    Responsibilities:
    - Setting up the main horizontal layout (50/50 split)
    - Creating workbench panel (left side)
    - Creating picker panel with stacked widget (right side)
    - Managing progress callbacks during initialization
    """

    def __init__(
        self,
        container: DIContainer,
        progress_callback: Optional[Callable[[str, float], None]] = None,
    ):
        self.container = container
        self.progress_callback = progress_callback
        self.workbench = None
        self.picker_stack = None
        self.tab_widget = None  # Tab navigation widget
        self.start_position_picker = None
        self.option_picker = None

        # Animation system for smooth widget transitions
        try:
            self.animation_orchestrator = container.resolve(IAnimationOrchestrator)
        except Exception:
            self.animation_orchestrator = None

        # Transition state tracking
        self._is_transitioning = False

    def setup_ui(self, parent_widget: QWidget) -> None:
        if self.progress_callback:
            self.progress_callback(86, "Setting up layout...")

        main_layout = QHBoxLayout(parent_widget)
        main_layout.setSpacing(8)  # Reduced spacing for more width
        main_layout.setContentsMargins(4, 4, 4, 4)  # Minimal margins for more width

        if self.progress_callback:
            self.progress_callback(86, "Creating workbench...")

        workbench_panel = self._create_workbench_panel()
        main_layout.addWidget(workbench_panel, 1)

        if self.progress_callback:
            self.progress_callback(87, "Creating option picker...")

        picker_panel = self._create_picker_panel_with_progress()
        main_layout.addWidget(picker_panel, 1)

        self._connect_beat_frame_to_graph_editor()

        if self.progress_callback:
            self.progress_callback(89, "Layout complete")

    def _create_workbench_panel(self) -> QWidget:
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(2, 2, 2, 2)  # Minimal margins for more space
        layout.setSpacing(4)  # Reduced spacing
        self.workbench = create_modern_workbench(self.container, panel)
        layout.addWidget(self.workbench.get_widget())
        return panel

    def _create_picker_panel_with_progress(self) -> QWidget:
        if self.progress_callback:
            self.progress_callback(87, "Creating picker panel...")

        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)  # No margins for maximum width
        layout.setSpacing(0)  # No spacing for clean tab integration

        # Create tab navigation widget at the top
        self.tab_widget = RightPanelTabWidget()
        layout.addWidget(self.tab_widget)

        self.picker_stack = QStackedWidget()

        if self.progress_callback:
            self.progress_callback(87, "Loading start positions...")

        start_pos_widget = self._create_start_position_widget()
        self.picker_stack.addWidget(start_pos_widget)

        if self.progress_callback:
            self.progress_callback(88, "Loading option picker...")

        option_widget = self._create_option_picker_widget_with_progress()
        self.picker_stack.addWidget(option_widget)

        if self.progress_callback:
            self.progress_callback(88, "Creating graph editor...")

        graph_editor_widget = self._create_graph_editor_widget()
        self.picker_stack.addWidget(graph_editor_widget)

        if self.progress_callback:
            self.progress_callback(89, "Creating generate controls...")

        generate_widget = self._create_generate_controls_widget()
        self.picker_stack.addWidget(generate_widget)

        if self.progress_callback:
            self.progress_callback(89, "Configuring transitions...")

        self.picker_stack.setCurrentIndex(0)
        layout.addWidget(self.picker_stack)

        # Connect tab widget to update active tab when transitions happen
        if self.tab_widget:
            self._update_tab_active_state(0)  # Start with picker tab active

        return panel

    def _create_start_position_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Get only the 4 services we actually need
        from application.services.pictograph_pool_manager import PictographPoolManager
        from core.interfaces.start_position_services import (
            IStartPositionDataService,
            IStartPositionOrchestrator,
            IStartPositionUIService,
        )

        # Resolve the 4 required services from DI container
        pool_manager = self.container.resolve(PictographPoolManager)
        data_service = self.container.resolve(IStartPositionDataService)
        ui_service = self.container.resolve(IStartPositionUIService)
        orchestrator = self.container.resolve(IStartPositionOrchestrator)

        # Create the simplified start position picker with only 4 dependencies
        self.start_position_picker = StartPositionPicker(
            pool_manager=pool_manager,
            data_service=data_service,
            ui_service=ui_service,
            orchestrator=orchestrator,
            initial_mode=PickerMode.AUTO,  # Start in auto mode for responsive behavior
        )

        layout.addWidget(self.start_position_picker)
        return widget

    def _create_option_picker_widget_with_progress(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        try:

            def option_picker_progress(step: str, progress: float):
                if self.progress_callback:
                    # Map option picker progress to 76-82% range
                    mapped_progress = int(76 + (progress * 6))
                    self.progress_callback(mapped_progress, f"Option picker: {step}")

            # WINDOW MANAGEMENT FIX: Create option picker during splash screen
            # Pool creation happens during splash - no window flashing due to hidden widgets
            # SIZE PROVIDER FIX: Pass widget as parent so option picker can find main window
            self.option_picker = OptionPicker(
                self.container,
                progress_callback=option_picker_progress,
                parent=widget,  # CRITICAL: Pass parent so size provider can find main window
            )
            self.option_picker.initialize()
            layout.addWidget(self.option_picker.widget)

            # WINDOW MANAGEMENT FIX: Make widgets visible after initialization
            # This prevents window flashing during splash screen
            self.option_picker.make_widgets_visible()
        except RuntimeError as e:
            print(f"❌ Failed to create option picker: {e}")
            fallback_label = QLabel("Option picker unavailable")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(fallback_label)
            self.option_picker = None
        return widget

    def _create_graph_editor_widget(self) -> QWidget:
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        try:
            from presentation.components.graph_editor.graph_editor import GraphEditor

            self.graph_editor = GraphEditor(
                graph_service=None,
                parent=None,
                workbench_width=800,
                workbench_height=300,
            )
            layout.addWidget(self.graph_editor)
            if hasattr(self.graph_editor, "beat_modified"):
                self.graph_editor.beat_modified.connect(self._on_graph_beat_modified)
        except Exception as e:
            fallback_label = QLabel(f"Graph editor unavailable: {e}")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback_label.setStyleSheet("color: red; font-size: 14px; padding: 20px;")
            layout.addWidget(fallback_label)
            self.graph_editor = None
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create graph editor: {e}", exc_info=True)
        return widget

    def _create_generate_controls_widget(self) -> QWidget:
        """Create generate controls widget for sequence generation."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        try:
            from presentation.components.generate_tab.generate_panel import (
                GeneratePanel,
            )

            self.generate_panel = GeneratePanel(parent=widget)
            layout.addWidget(self.generate_panel)

            # Connect generate panel signals if needed
            if hasattr(self.generate_panel, "generate_requested"):
                self.generate_panel.generate_requested.connect(
                    self._on_generate_requested
                )

        except Exception as e:
            fallback_label = QLabel(f"Generate controls unavailable: {e}")
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            fallback_label.setStyleSheet(
                "color: orange; font-size: 14px; padding: 20px;"
            )
            layout.addWidget(fallback_label)
            self.generate_panel = None
            import logging

            logger = logging.getLogger(__name__)
            logger.error(f"Failed to create generate controls: {e}", exc_info=True)

        return widget

    def transition_to_option_picker(self):
        """Transition to option picker with smooth fade animation."""
        if self.picker_stack and not self._is_transitioning:
            self._update_tab_active_state(1)  # Option picker
            self._start_fade_to_option_picker()

    def transition_to_start_position_picker(self):
        """Transition to start position picker with smooth fade animation."""
        if self.picker_stack and not self._is_transitioning:
            self._update_tab_active_state(0)  # Start position picker
            self._start_fade_to_start_position_picker()

    def transition_to_graph_editor(self):
        """Transition to graph editor with smooth fade animation."""
        if self.picker_stack and not self._is_transitioning:
            self._update_tab_active_state(2)  # Graph editor
            self._start_fade_to_graph_editor()

    def transition_to_generate_controls(self):
        """Transition to generate controls with smooth fade animation."""
        if self.picker_stack and not self._is_transitioning:
            self._update_tab_active_state(3)  # Generate controls
            self._start_fade_to_generate_controls()

    def _start_fade_to_option_picker(self):
        """Start smooth fade transition to option picker."""
        if self.picker_stack.currentIndex() == 1:
            return  # Already showing option picker

        self._is_transitioning = True

        # Prevent start position picker from updating during transition
        if self.start_position_picker and hasattr(
            self.start_position_picker, "set_transition_mode"
        ):
            self.start_position_picker.set_transition_mode(True)

        # Pre-load option picker content while hidden to avoid redundant fades
        if self.option_picker and hasattr(self.option_picker, "prepare_for_transition"):
            self.option_picker.prepare_for_transition()

        print("🎬 Starting Qt-based fade transition to option picker...")

        # Use the same Qt animation pattern as option picker sections
        self._fade_stack_transition(1, "option picker")

    def _start_fade_to_start_position_picker(self):
        """Start smooth fade transition to start position picker."""
        if self.picker_stack.currentIndex() == 0:
            return  # Already showing start position picker

        self._is_transitioning = True
        print("🎬 Starting Qt-based fade transition to start position picker...")

        # Use the same Qt animation pattern as option picker sections
        self._fade_stack_transition(0, "start position picker")

    def _start_fade_to_graph_editor(self):
        """Start smooth fade transition to graph editor."""
        if self.picker_stack.currentIndex() == 2:
            return  # Already showing graph editor

        self._is_transitioning = True
        print("🎬 Starting Qt-based fade transition to graph editor...")

        # Use the same Qt animation pattern as option picker sections
        self._fade_stack_transition(2, "graph editor")

    def _start_fade_to_generate_controls(self):
        """Start smooth fade transition to generate controls."""
        if self.picker_stack.currentIndex() == 3:
            return  # Already showing generate controls

        self._is_transitioning = True
        print("🎬 Starting Qt-based fade transition to generate controls...")

        # Use the same Qt animation pattern as option picker sections
        self._fade_stack_transition(3, "generate controls")

    def _fade_stack_transition(self, new_index: int, target_name: str):
        """
        Perform stack widget fade transition using legacy-based recursive cleanup.
        Recursively clears graphics effects from all child widgets to prevent QPainter conflicts.
        Based on legacy GraphicsEffectRemover approach that worked successfully.
        """
        try:
            current_widget = self.picker_stack.currentWidget()
            next_widget = self.picker_stack.widget(new_index)

            if (
                not current_widget
                or not next_widget
                or self.picker_stack.currentIndex() == new_index
            ):
                print(
                    f"🎭 [FADE] Skipping transition to {target_name} - invalid widgets or already current"
                )
                self._reset_transition_state()
                return

            print(
                f"🎭 [FADE] Starting fade transition to {target_name} with recursive cleanup"
            )

            # Legacy approach: Clear graphics effects recursively BEFORE starting animation
            self._clear_graphics_effects([current_widget, next_widget])

            # Temporarily disable pictograph updates during transition
            self._disable_pictograph_updates(current_widget, True)

            # Start fade out animation for current widget
            def on_fade_out_finished():
                print(f"🎭 [FADE] Fade out complete, switching to {target_name}")

                # Legacy approach: Clear effects again before switching (critical!)
                self._clear_graphics_effects([current_widget, next_widget])

                # Switch stack
                self.picker_stack.setCurrentIndex(new_index)

                # Re-enable pictograph updates
                self._disable_pictograph_updates(current_widget, False)

                # Start fade in animation for next widget
                self._fade_in_widget(next_widget, target_name)

            # Start fade out animation
            self._fade_out_widget(current_widget, on_fade_out_finished)

        except Exception as e:
            print(f"❌ [FADE] Stack transition failed for {target_name}: {e}")
            self._fallback_transition(new_index, target_name)

    def _fade_out_widget(self, widget, callback):
        """Fade out a widget using QPropertyAnimation with proper QPainter handling."""
        try:
            effect = self._ensure_opacity_effect(widget)
            effect.setOpacity(1.0)  # Ensure it starts visible

            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(200)  # Match option picker timing
            animation.setStartValue(1.0)
            animation.setEndValue(0.0)
            animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

            # Store reference to prevent garbage collection
            self._current_animation = animation

            def on_fade_out_finished():
                # Legacy approach: Recursively clear graphics effects after animation finishes
                self._clear_graphics_effects([widget])
                callback()

            animation.finished.connect(on_fade_out_finished)
            animation.start()

        except Exception as e:
            print(f"❌ [FADE] Fade out animation failed: {e}")
            # Clear effects recursively even on failure
            self._clear_graphics_effects([widget])
            callback()

    def _fade_in_widget(self, widget, target_name: str):
        """Fade in a widget using QPropertyAnimation with proper QPainter handling."""
        try:
            effect = self._ensure_opacity_effect(widget)
            effect.setOpacity(0.0)  # Start invisible

            animation = QPropertyAnimation(effect, b"opacity")
            animation.setDuration(200)  # Match option picker timing
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
            animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

            def on_fade_in_complete():
                print(
                    f"✅ [FADE] Whole-widget fade transition completed to {target_name}"
                )
                # Legacy approach: Recursively clear graphics effects after animation finishes
                self._clear_graphics_effects([widget])
                self._reset_transition_state()

            # Store reference to prevent garbage collection
            self._current_animation = animation

            animation.finished.connect(on_fade_in_complete)
            animation.start()

        except Exception as e:
            print(f"❌ [FADE] Fade in animation failed for {target_name}: {e}")
            # Clear effects recursively even on failure
            self._clear_graphics_effects([widget])
            self._reset_transition_state()

    def _ensure_opacity_effect(self, widget) -> QGraphicsOpacityEffect:
        """Ensure widget has an opacity effect."""
        effect = widget.graphicsEffect()
        if effect and isinstance(effect, QGraphicsOpacityEffect):
            return effect

        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        return effect

    def _clear_graphics_effects(self, widgets):
        """
        Recursively clear graphics effects from widgets and all their children.
        Based on legacy GraphicsEffectRemover approach to prevent QPainter conflicts.
        """
        for widget in widgets:
            if widget and hasattr(widget, "setGraphicsEffect"):
                self._remove_all_graphics_effects_recursive(widget)

    def _remove_all_graphics_effects_recursive(self, widget):
        """
        Recursively remove graphics effects from widget and all child widgets.
        This is the key to preventing QPainter conflicts with complex widgets.
        Based on legacy GraphicsEffectRemover._remove_all_graphics_effects.
        """
        try:
            # Safety check
            if widget is None or not hasattr(widget, "setGraphicsEffect"):
                return

            # Clear effect from the widget itself
            widget.setGraphicsEffect(None)

            # Recursively clear effects from all child widgets
            if hasattr(widget, "findChildren"):
                for child in widget.findChildren(QWidget):
                    if child and child.graphicsEffect():
                        try:
                            child.setGraphicsEffect(None)
                        except (RuntimeError, AttributeError):
                            pass  # Silently ignore already-deleted widgets

        except (RuntimeError, AttributeError):
            pass  # Silently ignore already-deleted widgets or attribute errors

    def _disable_pictograph_updates(self, widget, disable: bool):
        """Temporarily disable pictograph updates to prevent QPainter conflicts."""
        try:
            # For start position picker, disable sizing updates
            if hasattr(widget, "content") and hasattr(widget.content, "apply_sizing"):
                if disable:
                    # Store original method and replace with no-op
                    if not hasattr(widget.content, "_original_apply_sizing"):
                        widget.content._original_apply_sizing = (
                            widget.content.apply_sizing
                        )
                        widget.content.apply_sizing = lambda *args, **kwargs: None
                else:
                    # Restore original method
                    if hasattr(widget.content, "_original_apply_sizing"):
                        widget.content.apply_sizing = (
                            widget.content._original_apply_sizing
                        )
                        delattr(widget.content, "_original_apply_sizing")
        except Exception as e:
            print(f"❌ [FADE] Error managing pictograph updates: {e}")

    def _fallback_transition(self, new_index: int, target_name: str):
        """Fallback to direct transition if animations fail."""
        print(f"🔄 [FALLBACK] Using direct transition to {target_name}")
        self.picker_stack.setCurrentIndex(new_index)
        print(f"✅ [FALLBACK] Direct transition completed to {target_name}")
        QTimer.singleShot(250, self._reset_transition_state)

    def _reset_transition_state(self):
        """Reset the transition state."""
        self._is_transitioning = False
        self._current_animation = None

        # Re-enable start position picker updates
        if self.start_position_picker and hasattr(
            self.start_position_picker, "set_transition_mode"
        ):
            self.start_position_picker.set_transition_mode(False)

    def _connect_beat_frame_to_graph_editor(self):
        if not self.workbench or not self.graph_editor:
            return
        beat_frame_section = getattr(self.workbench, "_beat_frame_section", None)
        if not beat_frame_section:
            return
        beat_frame: "SequenceBeatFrame" = getattr(
            beat_frame_section, "_beat_frame", None
        )
        if not beat_frame:
            return
        beat_frame.beat_selected.connect(self._on_beat_selected_for_graph_editor)

    def _on_beat_selected_for_graph_editor(self, beat_index: int):
        # Removed repetitive debug log
        if not self.graph_editor or not self.workbench:
            print(
                f"⚠️ Missing components - graph_editor: {bool(self.graph_editor)}, workbench: {bool(self.workbench)}"
            )
            return
        current_sequence = self.workbench.get_sequence()
        if not current_sequence:
            print(f"⚠️ No current sequence available")
            return
        # Removed repetitive debug log
        if beat_index == -1:
            start_position_data = getattr(self.workbench, "_start_position_data", None)
            if start_position_data:
                self.graph_editor.set_selected_beat_data(-1, start_position_data)
            else:
                print(f"⚠️ No start position data available")
            return
        if 0 <= beat_index < len(current_sequence.beats):
            beat_data = current_sequence.beats[beat_index]
            # Removed repetitive debug log
            self.graph_editor.set_selected_beat_data(beat_index, beat_data)
        else:
            print(
                f"⚠️ Invalid beat index: {beat_index} (sequence has {len(current_sequence.beats)} beats)"
            )

    def _on_generate_requested(self, generation_config):
        """Handle generation request from generate panel."""
        print(
            f"🤖 [LAYOUT_MANAGER] Generation requested with config: {generation_config}"
        )
        # TODO: Implement sequence generation logic
        # This would typically involve:
        # 1. Calling a generation service with the config
        # 2. Getting the generated sequence
        # 3. Setting it in the workbench
        # 4. Transitioning back to option picker to show the result

    def _on_graph_beat_modified(self, beat_index: int, beat_data):
        print(f"✅ Graph editor modified beat {beat_index}")

    def _update_tab_active_state(self, panel_index: int):
        """Update the tab widget to reflect the current panel."""
        if self.tab_widget:
            # Map panel indices to tab indices
            # 0,1 = Picker tabs, 2 = Graph Editor, 3 = Generate Controls
            if panel_index in [0, 1]:  # Start position picker or option picker
                self.tab_widget.set_active_tab(0)  # Picker tab
            elif panel_index == 2:  # Graph editor
                self.tab_widget.set_active_tab(1)  # Graph editor tab
            elif panel_index == 3:  # Generate controls
                self.tab_widget.set_active_tab(2)  # Generate controls tab
