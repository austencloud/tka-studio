"""
Unified Start Position Picker - Simplified Component with Sub-Components

Consolidates the functionality of Enhanced/Advanced/Basic pickers into a single,
intelligent component that coordinates sub-components.

Features:
- Mode-based switching (BASIC: 3 positions, ADVANCED: 16 positions, AUTO: responsive)
- Smooth transitions between modes
- Service-based architecture for business logic
- Component-based architecture for maintainability
- Responsive layout that adapts to container size
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
import logging

from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QTimer, pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget


# Event bus removed - using Qt signals instead
EVENT_BUS_AVAILABLE = False

from desktop.modern.core.interfaces.start_position_services import (
    IStartPositionDataService,
    IStartPositionOrchestrator,
    IStartPositionUIService,
)
from desktop.modern.presentation.components.start_position_picker.start_position_picker_content import (
    StartPositionPickerContent,
)
from desktop.modern.presentation.components.start_position_picker.start_position_picker_footer import (
    StartPositionPickerFooter,
)
from desktop.modern.presentation.components.start_position_picker.start_position_picker_header import (
    StartPositionPickerHeader,
)


logger = logging.getLogger(__name__)


class PickerMode(Enum):
    """Picker display modes."""

    BASIC = "basic"  # 3 key positions
    ADVANCED = "advanced"  # 16 positions in 4x4 grid
    AUTO = "auto"  # Responsive mode switching


class StartPositionPicker(QWidget):
    """
    Unified start position picker with intelligent mode switching.

    This component coordinates sub-components (header, content, footer) to provide
    a complete start position selection experience.

    Features:
    - Component-based architecture for maintainability
    - Mode-based switching between basic and advanced modes
    - Smooth transitions between modes
    - Simplified service dependencies (4 instead of 10)
    - Responsive layout adaptation
    """

    start_position_selected = pyqtSignal(str)
    mode_changed = pyqtSignal(str)

    def __init__(
        self,
        data_service: IStartPositionDataService,
        ui_service: IStartPositionUIService,
        orchestrator: IStartPositionOrchestrator,
        initial_mode: PickerMode = PickerMode.AUTO,
        parent=None,
    ):
        super().__init__(parent)

        # Store dependencies (only 3 needed now!)
        self.data_service = data_service
        self.ui_service = ui_service
        self.orchestrator = orchestrator

        # Event bus removed - using Qt signals instead
        self.event_bus = None

        # State management
        self.current_mode = initial_mode
        self.grid_mode = "diamond"  # diamond/box
        self._is_in_transition = (
            False  # Track transition state to prevent sizing updates
        )

        # Sub-components
        self.header = None
        self.content = None
        self.footer = None

        # Animation
        self.transition_animation = None

        self._setup_ui()
        self._setup_animations()
        self._connect_signals()
        self._load_initial_content()

        logger.info(
            f"Unified start position picker initialized in {initial_mode.value} mode"
        )

    def _setup_ui(self):
        """Setup the unified UI with component-based layout."""
        self.setStyleSheet(self._get_glassmorphism_styles())
        self.setObjectName("UnifiedStartPositionPicker")

        # Main layout - match option picker's top-hugging approach
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # No margins like option picker
        layout.setSpacing(0)  # No spacing like option picker

        # Create sub-components
        self.header = StartPositionPickerHeader(self)

        # Try to get animation orchestrator from the orchestrator service
        animation_orchestrator = None
        try:
            # The orchestrator service might have access to animation services
            if hasattr(self.orchestrator, "_container"):
                from desktop.modern.core.interfaces.animation_core_interfaces import (
                    IAnimationOrchestrator,
                )

                animation_orchestrator = self.orchestrator._container.resolve(
                    IAnimationOrchestrator
                )
        except Exception:
            # Animation system not available - continue without it
            pass

        self.content = StartPositionPickerContent(
            self.data_service,
            self.ui_service,
            self,
            animation_orchestrator,
        )
        self.footer = StartPositionPickerFooter(self)

        # Wrap content and footer in containers with margins (header hugs top)
        content_container = QWidget()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(24, 0, 24, 0)  # Side margins only
        content_layout.addWidget(self.content)

        footer_container = QWidget()
        footer_layout = QVBoxLayout(footer_container)
        footer_layout.setContentsMargins(24, 0, 24, 24)  # Side and bottom margins
        footer_layout.addWidget(self.footer)

        # Add components to layout
        layout.addWidget(self.header)  # Header hugs top (no container needed)
        layout.addWidget(content_container, 1)  # Content gets stretch factor
        layout.addWidget(footer_container)

    def _get_glassmorphism_styles(self) -> str:
        """Main container glassmorphism styling - EXACT copy from original."""
        return """
            QWidget#StartPositionPicker {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.35),
                    stop:1 rgba(255, 255, 255, 0.25)
                );
                border-radius: 28px;
                border: 2px solid rgba(255, 255, 255, 0.4);
            }
        """

    @property
    def position_options(self):
        """Get available position options for testing compatibility."""
        if hasattr(self.content, "position_options") and self.content.position_options:
            # Return the actual position options which should have position_key attributes
            return self.content.position_options
        return []

    def _connect_signals(self):
        """Connect sub-component signals."""
        # Header signals
        self.header.back_to_basic_requested.connect(self._switch_to_basic_mode)
        # Use the new grid_mode_changed signal instead of old toggle system
        self.header.grid_mode_changed.connect(self._on_grid_mode_changed)

        # Content signals
        self.content.position_selected.connect(self._handle_position_selection)

        # Footer signals
        self.footer.show_variations_requested.connect(self._switch_to_advanced_mode)
        self.footer.back_to_basic_requested.connect(self._switch_to_basic_mode)

    def _load_initial_content(self):
        """Load initial content based on current mode."""
        is_advanced = self.current_mode == PickerMode.ADVANCED
        self.content.load_positions(self.grid_mode, is_advanced)
        self.header.update_for_mode(self.current_mode, self.grid_mode)
        self.footer.update_for_mode(self.current_mode)

    def set_mode(self, mode: PickerMode):
        """Change picker mode with smooth transition - EXACT logic from original."""
        if mode != self.current_mode:
            old_mode = self.current_mode
            self.current_mode = mode

            logger.info(f"Switching from {old_mode.value} to {mode.value} mode")
            self._transition_to_mode(old_mode, mode)
            self.mode_changed.emit(mode.value)

    def _transition_to_mode(self, old_mode: PickerMode, new_mode: PickerMode):
        """Smoothly transition between modes."""
        # Update sub-components for new mode
        self.header.update_for_mode(new_mode, self.grid_mode)
        self.footer.update_for_mode(new_mode)

        # Clear and reload content
        self.content.clear_grid_layout()

        # Load positions for new mode
        is_advanced = new_mode == PickerMode.ADVANCED
        self.content.load_positions(self.grid_mode, is_advanced)

    def _handle_position_selection(self, position_key: str):
        """Handle position selection through orchestrator service - EXACT logic from original."""
        try:
            logger.info(f"Position selected: {position_key}")

            success = self.orchestrator.handle_position_selection(position_key)
            if success:
                logger.info(f"✅ Position selection successful: {position_key}")

                # Publish event via event bus (modern approach)
                self._publish_start_position_event(position_key)

                # Also emit Qt signal for backward compatibility
                self.start_position_selected.emit(position_key)
            else:
                logger.warning(f"⚠️ Position selection failed: {position_key}")
                # Still emit signal for UI consistency
                self.start_position_selected.emit(position_key)

        except Exception as e:
            logger.exception(f"Error in position selection: {e}")
            # Fallback - still emit signal
            self.start_position_selected.emit(position_key)

    def _publish_start_position_event(self, position_key: str):
        """Publish start position selection event via event bus."""
        if self.event_bus and EVENT_BUS_AVAILABLE:
            try:
                # Get beat data from orchestrator if available
                if hasattr(self.orchestrator, "get_last_created_beat_data"):
                    beat_data_obj = self.orchestrator.get_last_created_beat_data()
                    if beat_data_obj:
                        # Convert beat data to dict for event
                        {
                            "letter": getattr(beat_data_obj, "letter", position_key),
                            "position_key": position_key,
                            "timestamp": str(datetime.now()),
                        }

                # Event bus removed - Qt signal already emitted above
                logger.info(
                    f"📡 Emitted start_position_selected signal for {position_key}"
                )

            except Exception as e:
                logger.exception(f"Failed to publish start position event: {e}")
        else:
            logger.debug("Event bus not available, skipping event publication")

    def _switch_to_basic_mode(self):
        """Switch to basic mode."""
        self.set_mode(PickerMode.BASIC)

    def _switch_to_advanced_mode(self):
        """Switch to advanced mode."""
        self.set_mode(PickerMode.ADVANCED)

    def _on_grid_mode_changed(self, new_mode: str):
        """Handle grid mode change from the PyToggle system."""
        old_grid_mode = self.grid_mode
        self.grid_mode = new_mode

        logger.info(f"Grid mode changed from {old_grid_mode} to {self.grid_mode}")

        # Reload content for new grid mode with a small delay to avoid conflicts
        QTimer.singleShot(10, self._reload_content_for_grid_mode)

    def _reload_content_for_grid_mode(self):
        """Reload content for new grid mode."""
        is_advanced = self.current_mode == PickerMode.ADVANCED
        self.content.load_positions(self.grid_mode, is_advanced)

    def _setup_animations(self):
        """Setup smooth animations - EXACT copy from original."""
        self.transition_animation = QPropertyAnimation(self, b"windowOpacity")
        self.transition_animation.setDuration(300)
        self.transition_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def set_transition_mode(self, in_transition: bool):
        """Set transition mode to prevent sizing updates during fade transitions."""
        self._is_in_transition = in_transition
        logger.debug(f"Start position picker transition mode: {in_transition}")

    def showEvent(self, event):
        """Handle show event with proper sizing - EXACT copy from original."""
        super().showEvent(event)

        # Skip sizing updates during transitions to prevent pictograph flashing
        if self._is_in_transition:
            logger.debug("Skipping showEvent sizing during transition")
            return

        # Ensure proper sizing when shown
        QTimer.singleShot(100, self._ensure_proper_sizing)

    def _ensure_proper_sizing(self):
        """Ensure all components are properly sized when the widget is shown."""
        try:
            # Skip sizing updates during transitions to prevent pictograph flashing
            if self._is_in_transition:
                logger.debug("Skipping sizing update during transition")
                return

            # Force layout update
            self.updateGeometry()

            # Apply sizing to content
            is_advanced = self.current_mode == PickerMode.ADVANCED
            main_window = self.window()
            container_width = main_window.width() if main_window else 1000
            self.content.apply_sizing(container_width, is_advanced)

            logger.debug(
                f"Unified picker sizing ensured - mode: {self.current_mode.value}"
            )

        except Exception as e:
            logger.exception(f"Error ensuring proper sizing: {e}")

    def resizeEvent(self, event):
        """Handle resize events to update position option sizes - EXACT copy from original."""
        super().resizeEvent(event)

        # Update sizing for all position options with a slight delay
        QTimer.singleShot(50, self._update_option_sizes)

    def _update_option_sizes(self):
        """Update sizes of all position options."""
        try:
            is_advanced = self.current_mode == PickerMode.ADVANCED
            container_width = self.width()
            self.content.apply_sizing(container_width, is_advanced)
        except Exception as e:
            logger.exception(f"Error updating option sizes: {e}")
