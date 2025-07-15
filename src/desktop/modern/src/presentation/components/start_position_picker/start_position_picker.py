"""
Unified Start Position Picker - Single Component with Mode Switching

Consolidates the functionality of Enhanced/Advanced/Basic pickers into a single,
intelligent component that adapts based on mode and container size.

Features:
- Mode-based switching (BASIC: 3 positions, ADVANCED: 16 positions, AUTO: responsive)
- Smooth transitions between modes
- Service-based architecture for business logic
- Single component easier to maintain and port to web
- Responsive layout that adapts to container size
"""

import logging
from enum import Enum
from typing import Callable, List, Optional

from application.services.pictograph_pool_manager import PictographPoolManager
from core.interfaces.start_position_services import (
    IStartPositionDataService,
    IStartPositionOrchestrator,
    IStartPositionSelectionService,
    IStartPositionUIService,
)
from presentation.components.start_position_picker.enhanced_start_position_option import (
    EnhancedStartPositionOption,
)
from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, QSize, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
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

    This component consolidates Enhanced/Advanced/Basic picker functionality
    into a single, maintainable component that's easier to port to web.

    Features:
    - Single component handles both basic and advanced modes
    - Smooth transitions between modes
    - Responsive layout adaptation
    - Simplified service dependencies
    - Easy web translation
    """

    start_position_selected = pyqtSignal(str)
    mode_changed = pyqtSignal(str)

    def __init__(
        self,
        pool_manager: PictographPoolManager,
        data_service: IStartPositionDataService,
        selection_service: IStartPositionSelectionService,
        ui_service: IStartPositionUIService,
        orchestrator: IStartPositionOrchestrator,
        initial_mode: PickerMode = PickerMode.AUTO,
        parent=None,
    ):
        super().__init__(parent)

        # Core dependencies (injected)
        self.pool_manager = pool_manager
        self.data_service = data_service
        self.selection_service = selection_service
        self.ui_service = ui_service
        self.orchestrator = orchestrator

        # State management
        self.current_mode = initial_mode
        self.grid_mode = "diamond"  # diamond/box
        self.position_options: List[EnhancedStartPositionOption] = []
        self._loading_positions = False  # Flag to prevent infinite loops

        # UI components
        self.main_container = None
        self.grid_layout = None
        self.mode_toggle_button = None
        self.back_button = None
        self.variations_button = None
        self.title_label = None
        self.subtitle_label = None

        # Animation
        self.transition_animation = None

        self._setup_ui()
        self._setup_animations()
        self._load_positions_for_current_mode()

        logger.info(
            f"Unified start position picker initialized in {initial_mode.value} mode"
        )

    def _setup_ui(self):
        """Setup the unified UI with adaptive layout."""
        self.setStyleSheet(self._get_glassmorphism_styles())
        self.setObjectName("UnifiedStartPositionPicker")

        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        # Header with mode controls
        header = self._create_adaptive_header()
        layout.addWidget(header)

        # Main content area (single container that adapts)
        self.main_container = QWidget()
        self.grid_layout = QGridLayout(self.main_container)
        self.grid_layout.setSpacing(15)

        # Scroll area for content
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setWidget(self.main_container)
        layout.addWidget(scroll_area, 1)

        # Footer with mode-specific actions
        footer = self._create_adaptive_footer()
        layout.addWidget(footer)

    def _create_adaptive_header(self) -> QWidget:
        """Create header that adapts to current mode."""
        header = QWidget()
        layout = QVBoxLayout(header)
        layout.setSpacing(12)

        # Control bar
        controls = QWidget()
        controls_layout = QHBoxLayout(controls)

        # Back button (shown in advanced mode)
        self.back_button = QPushButton("← Back to Simple")
        self.back_button.setObjectName("BackButton")
        self.back_button.clicked.connect(self._switch_to_basic_mode)
        self.back_button.setVisible(False)
        controls_layout.addWidget(self.back_button)

        controls_layout.addStretch()

        # Mode toggle (grid mode switcher)
        self.mode_toggle_button = QPushButton("⚡ Diamond Grid")
        self.mode_toggle_button.setObjectName("ModeToggleButton")
        self.mode_toggle_button.clicked.connect(self._toggle_grid_mode)
        controls_layout.addWidget(self.mode_toggle_button)

        layout.addWidget(controls)

        # Title section
        title_section = QWidget()
        title_layout = QVBoxLayout(title_section)
        title_layout.setSpacing(8)
        title_layout.setContentsMargins(16, 16, 16, 16)

        # Title
        self.title_label = QLabel("Choose Your Start Position")
        self.title_label.setFont(QFont("Monotype Corsiva", 24, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setObjectName("UnifiedTitle")
        title_layout.addWidget(self.title_label)

        # Subtitle
        self.subtitle_label = QLabel(
            "Select a starting position to begin crafting your sequence"
        )
        self.subtitle_label.setFont(QFont("Monotype Corsiva", 14))
        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle_label.setObjectName("UnifiedSubtitle")
        title_layout.addWidget(self.subtitle_label)

        title_section.setObjectName("TitleSection")
        layout.addWidget(title_section)

        self._update_header_for_mode()
        return header

    def _create_adaptive_footer(self) -> QWidget:
        """Create footer that adapts to current mode."""
        footer = QWidget()
        layout = QHBoxLayout(footer)
        layout.addStretch()

        # Variations button (shown in basic mode)
        self.variations_button = QPushButton("✨ Show All Variations")
        self.variations_button.setObjectName("VariationsButton")
        self.variations_button.clicked.connect(self._switch_to_advanced_mode)
        layout.addWidget(self.variations_button)

        layout.addStretch()
        self._update_footer_for_mode()
        return footer

    def _get_glassmorphism_styles(self) -> str:
        """Consolidated glassmorphism styling."""
        return """
            QWidget#UnifiedStartPositionPicker {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.35),
                    stop:1 rgba(255, 255, 255, 0.25)
                );
                border-radius: 28px;
                border: 2px solid rgba(255, 255, 255, 0.4);
            }
            
            QWidget#TitleSection {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 16px;
            }
            
            QLabel#UnifiedTitle {
                color: black;
                background: transparent;
                font-weight: 700;
            }
            
            QLabel#UnifiedSubtitle {
                color: black;
                background: transparent;
                font-weight: 400;
            }
            
            QPushButton#BackButton {
                background: rgba(239, 68, 68, 0.9);
                color: white;
                border: none;
                border-radius: 16px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 14px;
            }
            
            QPushButton#BackButton:hover {
                background: rgba(239, 68, 68, 1.0);
            }
            
            QPushButton#ModeToggleButton {
                background: rgba(59, 130, 246, 0.9);
                color: white;
                border: none;
                border-radius: 14px;
                padding: 6px 14px;
                font-weight: 600;
                font-size: 12px;
            }
            
            QPushButton#ModeToggleButton:hover {
                background: rgba(59, 130, 246, 1.0);
            }
            
            QPushButton#VariationsButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(99, 102, 241, 0.15),
                    stop:1 rgba(168, 85, 247, 0.1)
                );
                border: 2px solid rgba(255, 255, 255, 0.25);
                border-radius: 16px;
                color: #4c1d95;
                font-weight: 600;
                padding: 12px 24px;
                min-width: 160px;
            }
            
            QPushButton#VariationsButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(99, 102, 241, 0.25),
                    stop:1 rgba(168, 85, 247, 0.2)
                );
                border: 2px solid rgba(255, 255, 255, 0.4);
            }
            
            QScrollArea {
                background: transparent;
                border: none;
                border-radius: 16px;
            }
        """

    def set_mode(self, mode: PickerMode):
        """Change picker mode with smooth transition."""
        # Prevent mode changes while loading to avoid infinite loops
        if self._loading_positions:
            logger.warning(
                f"Ignoring mode change to {mode.value} - currently loading positions"
            )
            return

        if mode != self.current_mode:
            old_mode = self.current_mode
            self.current_mode = mode

            logger.info(f"Switching from {old_mode.value} to {mode.value} mode")
            self._transition_to_mode(old_mode, mode)
            self.mode_changed.emit(mode.value)

    def _transition_to_mode(self, old_mode: PickerMode, new_mode: PickerMode):
        """Smoothly transition between modes."""
        # Update UI elements for new mode
        self._update_header_for_mode()
        self._update_footer_for_mode()

        # Animate content transition
        self._animate_mode_transition(old_mode, new_mode)

    def _animate_mode_transition(self, old_mode: PickerMode, new_mode: PickerMode):
        """Animate the transition between modes."""
        # Skip animation if already loading to prevent infinite loops
        if self._loading_positions:
            logger.warning("Skipping animation - already loading positions")
            return

        # Stop any running animation
        if (
            self.transition_animation
            and self.transition_animation.state() == QPropertyAnimation.State.Running
        ):
            self.transition_animation.stop()

        # Directly load new content without complex animation to avoid loops
        self._complete_mode_transition_simple(new_mode)

    def _complete_mode_transition_simple(self, new_mode: PickerMode):
        """Complete the mode transition by loading new content (simplified version)."""
        # Clear current layout
        self._clear_grid_layout()

        # Load positions for new mode
        self._load_positions_for_current_mode()

    def _fade_options(
        self, target_opacity: float, completion_callback: Callable = None
    ):
        """Fade position options in or out."""
        # Simplified version - just call callback directly to avoid animation loops
        if completion_callback:
            # Use QTimer to call callback after a short delay
            QTimer.singleShot(50, completion_callback)

    def _update_header_for_mode(self):
        """Update header elements based on current mode."""
        if self.current_mode == PickerMode.ADVANCED:
            self.title_label.setText("All Start Positions")
            self.subtitle_label.setText("Choose from 16 available starting positions")
            self.back_button.setVisible(True)
            self.mode_toggle_button.setVisible(True)
        else:
            self.title_label.setText("Choose Your Start Position")
            self.subtitle_label.setText(
                "Select a starting position to begin crafting your sequence"
            )
            self.back_button.setVisible(False)
            self.mode_toggle_button.setVisible(True)

    def _update_footer_for_mode(self):
        """Update footer elements based on current mode."""
        if self.current_mode == PickerMode.ADVANCED:
            self.variations_button.setVisible(False)
        else:
            self.variations_button.setVisible(True)

    def _load_positions_for_current_mode(self):
        """Load position options based on current mode."""
        # Prevent infinite loops with a stronger guard
        if self._loading_positions:
            logger.warning(
                "Already loading positions, skipping to prevent infinite loop"
            )
            return

        self._loading_positions = True

        try:
            logger.debug(
                f"Starting to load positions for {self.current_mode.value} mode"
            )

            # Get position keys for current mode using UI service
            is_advanced = self.current_mode == PickerMode.ADVANCED
            position_keys = self.ui_service.get_positions_for_mode(
                self.grid_mode, is_advanced
            )

            logger.debug(
                f"Loading {len(position_keys)} positions for {self.current_mode.value} mode"
            )

            # Create position options
            self._create_position_options(position_keys)

            # Arrange in grid first
            self._arrange_positions_for_mode()

            # Apply sizing after layout is arranged to avoid interference
            self._apply_sizing_to_all_options()

            logger.info(
                f"Loaded {len(self.position_options)} positions in {self.current_mode.value} mode"
            )

        except Exception as e:
            logger.error(f"Error loading positions for current mode: {e}")
            # Create fallback options
            self._create_fallback_options()
        finally:
            # Use QTimer to reset the flag after a short delay to prevent rapid calls
            QTimer.singleShot(50, self._reset_loading_flag)

    def _reset_loading_flag(self):
        """Reset the loading flag after a delay."""
        self._loading_positions = False

    def _create_position_options(self, position_keys: List[str]):
        """Create position option widgets."""
        # Clear existing options and properly cleanup pool resources
        for option in self.position_options:
            try:
                # Explicitly cleanup pool resources before removing
                if hasattr(option, "_cleanup_pool_resources"):
                    option._cleanup_pool_resources()
                option.setParent(None)
            except Exception as e:
                logger.warning(f"Error cleaning up position option: {e}")
        self.position_options.clear()

        # Create new options
        for position_key in position_keys:
            try:
                option = EnhancedStartPositionOption(
                    position_key=position_key,
                    pool_manager=self.pool_manager,
                    data_service=self.data_service,
                    grid_mode=self.grid_mode,
                    enhanced_styling=True,
                    parent=self,
                )
                option.position_selected.connect(self._handle_position_selection)
                self.position_options.append(option)

            except Exception as e:
                logger.warning(f"Failed to create option for {position_key}: {e}")

    def _create_fallback_options(self):
        """Create fallback options if normal loading fails."""
        fallback_positions = ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]
        logger.warning(f"Creating fallback options: {fallback_positions}")
        self._create_position_options(fallback_positions)

    def _apply_option_sizing(self, option: EnhancedStartPositionOption):
        """Apply appropriate sizing to position option."""
        try:
            # Get main window width for sizing calculation
            main_window = self.window()
            container_width = main_window.width() if main_window else 1000

            # Calculate size using UI service
            is_advanced = self.current_mode == PickerMode.ADVANCED
            size = self.ui_service.calculate_option_size(container_width, is_advanced)

            # Apply the calculated size to the container
            option.setFixedSize(size, size)

            # Update the pictograph size to match the container
            if hasattr(option, "update_pictograph_size"):
                option.update_pictograph_size(size)
                logger.debug(
                    f"Applied sizing: container={size}px, mode={self.current_mode.value}"
                )

            option.show()
            option.setVisible(True)

        except Exception as e:
            logger.warning(f"Failed to apply option sizing: {e}")
            # Fallback sizing
            default_size = 100 if self.current_mode == PickerMode.ADVANCED else 120
            option.setFixedSize(default_size, default_size)

            # Apply fallback pictograph sizing too
            if hasattr(option, "update_pictograph_size"):
                option.update_pictograph_size(default_size)

    def _apply_sizing_to_all_options(self):
        """Apply sizing to all position options after layout is arranged."""
        for option in self.position_options:
            self._apply_option_sizing(option)

    def _arrange_positions_for_mode(self):
        """Arrange position options based on current mode."""
        # Determine layout based on actual mode and position count
        if self.current_mode == PickerMode.ADVANCED:
            self._arrange_advanced_layout()
        elif self.current_mode == PickerMode.BASIC:
            self._arrange_basic_layout()
        else:  # AUTO mode - decide based on position count
            if len(self.position_options) <= 3:
                self._arrange_basic_layout()
            else:
                self._arrange_advanced_layout()

    def _arrange_basic_layout(self):
        """Arrange 3 positions responsively."""
        # Always arrange horizontally in a single row for Simple mode
        # This matches the legacy behavior where 3 positions are displayed horizontally
        for i, option in enumerate(self.position_options):
            self.grid_layout.addWidget(option, 0, i)
            # Ensure widgets are visible and properly sized
            option.show()
            option.setVisible(True)

        # Set column stretch to ensure horizontal distribution
        for i in range(len(self.position_options)):
            self.grid_layout.setColumnStretch(i, 1)

        # Force complete layout recalculation
        self.grid_layout.activate()
        self.grid_layout.update()
        self.main_container.updateGeometry()

        # Process events to ensure layout is applied
        from PyQt6.QtWidgets import QApplication

        QApplication.processEvents()

        logger.debug(
            f"✅ Arranged {len(self.position_options)} positions horizontally in basic mode"
        )

    def _arrange_advanced_layout(self):
        """Arrange positions in 4x4 grid."""
        for i, option in enumerate(self.position_options):
            row, col = divmod(i, 4)
            self.grid_layout.addWidget(option, row, col)

        # Force layout update
        self.grid_layout.update()
        self.main_container.updateGeometry()

        logger.debug(
            f"✅ Arranged {len(self.position_options)} positions in 4x4 advanced grid"
        )

    def _clear_grid_layout(self):
        """Clear all widgets from grid layout and reset its structure."""
        # Remove all widgets from the layout
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item and item.widget():
                item.widget().setParent(None)

        # Reset column stretches to prevent layout conflicts
        for i in range(10):  # Clear up to 10 columns (more than we'll ever use)
            self.grid_layout.setColumnStretch(i, 0)

        # Force the grid layout to completely reset its internal structure
        # This ensures clean transitions between different grid arrangements
        self.grid_layout.invalidate()

        # Clear any cached geometry information
        self.main_container.updateGeometry()
        self.updateGeometry()

        logger.debug("Grid layout cleared and structure reset for mode switching")

    def _handle_position_selection(self, position_key: str):
        """Handle position selection through orchestrator service."""
        try:
            logger.info(f"Position selected: {position_key}")

            success = self.orchestrator.handle_position_selection(position_key)
            if success:
                logger.info(f"✅ Position selection successful: {position_key}")
                self.start_position_selected.emit(position_key)
            else:
                logger.warning(f"⚠️ Position selection failed: {position_key}")
                # Still emit signal for UI consistency
                self.start_position_selected.emit(position_key)

        except Exception as e:
            logger.error(f"Error in position selection: {e}")
            # Fallback - still emit signal
            self.start_position_selected.emit(position_key)

    def _switch_to_basic_mode(self):
        """Switch to basic mode."""
        self.set_mode(PickerMode.BASIC)

    def _switch_to_advanced_mode(self):
        """Switch to advanced mode."""
        self.set_mode(PickerMode.ADVANCED)

    def _toggle_grid_mode(self):
        """Toggle between diamond and box grid modes."""
        old_grid_mode = self.grid_mode
        self.grid_mode = "box" if self.grid_mode == "diamond" else "diamond"

        # Update button text
        self.mode_toggle_button.setText(f"⚡ {self.grid_mode.title()} Grid")

        logger.info(f"Grid mode changed from {old_grid_mode} to {self.grid_mode}")

        # Reload positions for new grid mode with a small delay to avoid conflicts
        QTimer.singleShot(10, self._load_positions_for_current_mode)

    def _setup_animations(self):
        """Setup smooth animations."""
        self.transition_animation = QPropertyAnimation(self, b"windowOpacity")
        self.transition_animation.setDuration(300)
        self.transition_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

    def update_layout_for_size(self, container_size: QSize):
        """Update layout when container size changes."""
        try:
            # Auto-switch modes if in AUTO mode (but only if mode actually needs to change)
            if self.current_mode == PickerMode.AUTO:
                target_mode = None
                if container_size.width() > 1000 and container_size.height() > 600:
                    target_mode = PickerMode.ADVANCED
                else:
                    target_mode = PickerMode.BASIC

                # Only switch if we're not already in the target mode
                if target_mode != self.current_mode:
                    logger.debug(
                        f"Auto-switching from {self.current_mode} to {target_mode}"
                    )
                    self.set_mode(target_mode)
                    return  # Exit early since set_mode will handle the rest

            # Re-apply sizing to all options
            for option in self.position_options:
                self._apply_option_sizing(option)

            # Re-arrange current layout
            self._arrange_positions_for_mode()

        except Exception as e:
            logger.error(f"Error updating layout for size: {e}")

    def get_current_mode(self) -> PickerMode:
        """Get the current picker mode."""
        return self.current_mode

    def get_current_grid_mode(self) -> str:
        """Get the current grid mode."""
        return self.grid_mode

    def showEvent(self, event):
        """Handle show event with proper sizing."""
        super().showEvent(event)

        # Ensure proper sizing when shown
        QTimer.singleShot(100, self._ensure_proper_sizing)

    def _ensure_proper_sizing(self):
        """Ensure all components are properly sized when the widget is shown."""
        try:
            # Force layout update
            self.updateGeometry()
            self.main_container.updateGeometry()

            # Apply sizing to all position options
            for option in self.position_options:
                self._apply_option_sizing(option)

            # Force container visibility
            self.main_container.show()
            self.main_container.setVisible(True)

            logger.debug(
                f"Unified picker sizing ensured - mode: {self.current_mode.value}"
            )

        except Exception as e:
            logger.error(f"Error ensuring proper sizing: {e}")

    def resizeEvent(self, event):
        """Handle resize events to update position option sizes."""
        super().resizeEvent(event)

        # Update sizing for all position options with a slight delay
        QTimer.singleShot(50, self._update_option_sizes)

    def _update_option_sizes(self):
        """Update sizes of all position options."""
        try:
            for option in self.position_options:
                self._apply_option_sizing(option)
        except Exception as e:
            logger.error(f"Error updating option sizes: {e}")

    def sizeHint(self) -> QSize:
        """Provide size hint for the unified picker."""
        if self.current_mode == PickerMode.ADVANCED:
            return QSize(800, 700)  # Larger size for 4x4 grid
        else:
            return QSize(600, 500)  # Smaller size for 3 positions
