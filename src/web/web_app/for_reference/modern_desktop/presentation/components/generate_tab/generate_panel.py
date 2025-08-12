"""
Modern Generate Panel with Tasteful Glassmorphism
================================================

A clean, single-card design that fits all controls on one screen
while maintaining the legacy layout structure with subtle glass effects.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from desktop.modern.core.interfaces.generation_services import GenerationMode
from desktop.modern.domain.models.generation_models import (
    GenerationConfig,
    GenerationResult,
    GenerationState,
)
from desktop.modern.presentation.components.generate_tab.selectors import (
    CAPTypeSelector,
    GenerationModeToggle,
    LengthSelector,
    LetterTypeSelector,
    LevelSelector,
    ModernGridModeSelector,
    PropContinuityToggle,
    SliceSizeSelector,
    TurnIntensitySelector,
)


if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

    from .generate_tab_controller import GenerateTabController


class GeneratePanel(QWidget):
    """
    Modern Generate Panel with single glass card container.

    Maintains legacy layout structure while adding subtle glassmorphism effects.
    Everything fits on one screen without scrolling.
    """

    generate_requested = pyqtSignal(GenerationConfig)
    auto_complete_requested = pyqtSignal()
    config_changed = pyqtSignal(GenerationConfig)

    def __init__(
        self,
        container: DIContainer | None = None,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self._container = container
        self._controller: GenerateTabController | None = None

        self._current_config = GenerationConfig()
        self._current_state = GenerationState(config=self._current_config)

        self._setup_ui()
        self._connect_signals()
        self._apply_glassmorphism_theme()

        # Initialize controller if container is provided
        if self._container:
            self._initialize_controller()

    def _setup_ui(self):
        """Setup clean, elegant UI with minimal visual noise."""
        # Main layout with better centering and padding
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(32, 24, 32, 24)  # More padding for centering
        main_layout.setSpacing(0)

        # Single clean container without visual noise
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(
            24, 20, 24, 20
        )  # Inner padding for better centering
        container_layout.setSpacing(8)  # Compact spacing like legacy

        # Minimal header
        self._setup_header(container_layout)

        # Controls section - clean and spacious
        self._setup_controls_section(container_layout)

        # Action buttons - prominent and clear
        self._setup_action_buttons(container_layout)

        # Apply subtle glassmorphism without borders or visual noise
        container.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                border: none;
            }
        """)

        main_layout.addWidget(container)

    def _setup_header(self, layout: QVBoxLayout):
        """Create elegant, readable header."""
        header = QLabel("Customize Your Sequence")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.95);
                font-size: 20px;
                font-weight: 600;
                letter-spacing: 0.5px;
                padding: 0px 0px 12px 0px;
                margin: 0px;
                background: transparent;
                border: none;
            }
        """)
        layout.addWidget(header)

    def _setup_controls_section(self, layout: QVBoxLayout):
        """Setup clean, unified controls without visual noise."""
        # Create all controls
        self._level_selector = LevelSelector()
        self._length_selector = LengthSelector()
        self._turn_intensity_selector = TurnIntensitySelector()
        self._grid_mode_selector = ModernGridModeSelector()
        self._mode_toggle = GenerationModeToggle()
        self._prop_continuity_toggle = PropContinuityToggle()
        self._letter_type_selector = LetterTypeSelector()
        self._slice_size_selector = SliceSizeSelector()
        self._cap_type_selector = CAPTypeSelector()

        # Apply unified styling to all controls
        self._apply_unified_control_styling()

        # Simple, clean layout - no groups, no containers, no visual noise
        controls = [
            self._level_selector,
            self._length_selector,
            self._turn_intensity_selector,
            self._grid_mode_selector,
            self._mode_toggle,
            self._prop_continuity_toggle,
            self._letter_type_selector,
            self._slice_size_selector,
            self._cap_type_selector,
        ]

        for control in controls:
            layout.addWidget(control)

        # Connect mode toggle to update visibility
        self._mode_toggle.mode_changed.connect(self._update_component_visibility)

        # Set initial visibility based on current mode
        self._update_component_visibility(self._mode_toggle.get_mode())

    def _apply_unified_control_styling(self):
        """Apply consistent, elegant styling to all controls."""
        # This method will ensure all controls have consistent appearance
        # Individual controls will be styled in their own files for now
        pass

    def _update_component_visibility(self, mode):
        """Update component visibility based on generation mode"""
        if mode == GenerationMode.FREEFORM:
            # Freeform mode: show letter type selector, hide slice size and CAP type
            self._letter_type_selector.setVisible(True)
            self._slice_size_selector.setVisible(False)
            self._cap_type_selector.setVisible(False)
        else:  # CIRCULAR mode
            # Circular mode: hide letter type selector, show slice size and CAP type
            self._letter_type_selector.setVisible(False)
            self._slice_size_selector.setVisible(True)
            self._cap_type_selector.setVisible(True)

    def _setup_action_buttons(self, layout: QVBoxLayout):
        """Setup clean, prominent action buttons."""
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setSpacing(16)

        # Create clean, readable buttons
        self._auto_complete_button = QPushButton("Auto-Complete")
        self._generate_button = QPushButton("Generate New")

        # Apply clean, unified button styling with larger, more readable text
        button_style = """
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                color: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                font-weight: 500;
                padding: 14px 28px;
                min-width: 140px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
                border-color: rgba(255, 255, 255, 0.3);
                color: white;
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.2);
            }
        """

        accent_button_style = """
            QPushButton {
                background: rgba(70, 130, 255, 0.8);
                border: 1px solid rgba(70, 130, 255, 0.9);
                border-radius: 8px;
                color: white;
                font-size: 16px;
                font-weight: 600;
                padding: 14px 28px;
                min-width: 140px;
            }
            QPushButton:hover {
                background: rgba(80, 140, 255, 0.9);
                border-color: rgba(80, 140, 255, 1.0);
            }
            QPushButton:pressed {
                background: rgba(60, 120, 245, 0.9);
            }
        """

        self._auto_complete_button.setStyleSheet(button_style)
        self._generate_button.setStyleSheet(accent_button_style)

        # Set cursor for better UX
        self._auto_complete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._generate_button.setCursor(Qt.CursorShape.PointingHandCursor)

        button_layout.addWidget(self._auto_complete_button)
        button_layout.addWidget(self._generate_button)

        layout.addLayout(button_layout)

    def _connect_signals(self):
        """Connect all UI signals."""
        # Mode change
        self._mode_toggle.mode_changed.connect(self._on_mode_changed)

        # Parameter changes
        self._length_selector.value_changed.connect(
            lambda v: self._update_config(length=v)
        )
        self._level_selector.value_changed.connect(
            lambda v: self._update_config(level=v)
        )
        self._turn_intensity_selector.value_changed.connect(
            lambda v: self._update_config(turn_intensity=v)
        )
        self._grid_mode_selector.value_changed.connect(
            lambda v: self._update_config(grid_mode=v)
        )
        self._prop_continuity_toggle.value_changed.connect(
            lambda v: self._update_config(prop_continuity=v)
        )

        # Mode-specific controls
        self._letter_type_selector.value_changed.connect(
            lambda v: self._update_config(letter_types=v)
        )
        self._slice_size_selector.value_changed.connect(
            lambda v: self._update_config(slice_size=v)
        )
        self._cap_type_selector.value_changed.connect(
            lambda v: self._update_config(cap_type=v)
        )

        # Action buttons
        self._generate_button.clicked.connect(self._on_generate_clicked)
        self._auto_complete_button.clicked.connect(self._on_auto_complete_clicked)

    def _apply_glassmorphism_theme(self):
        """Apply subtle glassmorphism theme to the entire panel."""
        self.setStyleSheet(
            """
            GeneratePanel {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(20, 20, 30, 0.95),
                    stop:0.5 rgba(30, 30, 45, 0.90),
                    stop:1 rgba(40, 40, 60, 0.95));
            }
            QWidget {
                color: rgba(255, 255, 255, 0.9);
                font-family: "Segoe UI", sans-serif;
            }
        """
        )

    def _on_mode_changed(self, mode: GenerationMode):
        """Handle mode change and show/hide appropriate controls."""
        self._update_config(mode=mode)

        # Show/hide mode-specific controls
        is_freeform = mode == GenerationMode.FREEFORM
        self._letter_type_selector.setVisible(is_freeform)
        self._slice_size_selector.setVisible(not is_freeform)
        self._cap_type_selector.setVisible(not is_freeform)

    def _update_config(self, **kwargs):
        """Update configuration and emit signal."""
        try:
            # DEBUG: Log length changes specifically
            if "length" in kwargs:
                print(f"🔍 [GENERATE_PANEL] Length updated to: {kwargs['length']}")

            self._current_config = self._current_config.with_updates(**kwargs)
            self._current_state = self._current_state.with_config(self._current_config)

            # DEBUG: Log the final config length
            print(
                f"🔍 [GENERATE_PANEL] Current config length: {self._current_config.length}"
            )

            self.config_changed.emit(self._current_config)
        except Exception as e:
            print(f"Configuration error: {e}")

    def _on_generate_clicked(self):
        """Handle generate button click."""
        if self._current_state.is_generating:
            return

        # DEBUG: Log the config being sent when generate is clicked
        print(
            f"🎯 [GENERATE_PANEL] Generate clicked with length: {self._current_config.length}"
        )
        print(f"🎯 [GENERATE_PANEL] Full config: {self._current_config}")

        self._current_state = self._current_state.start_generation()
        self._update_ui_for_generation_state()
        self.generate_requested.emit(self._current_config)

    def _on_auto_complete_clicked(self):
        """Handle auto complete button click."""
        if self._current_state.is_generating:
            return

        self.auto_complete_requested.emit()

    def _update_ui_for_generation_state(self):
        """Update UI based on current generation state."""
        is_generating = self._current_state.is_generating

        self._generate_button.setEnabled(not is_generating)
        self._auto_complete_button.setEnabled(not is_generating)

        if is_generating:
            self._generate_button.setText("Generating...")
        else:
            self._generate_button.setText("Generate New")

    def set_state(self, state: GenerationState):
        """Set panel state and update UI."""
        self._current_state = state
        self._current_config = state.config
        self._update_controls_from_config()
        self._update_ui_for_generation_state()

    def set_generation_result(self, result: GenerationResult):
        """Set generation result and update state."""
        self._current_state = self._current_state.with_result(result)
        self._update_ui_for_generation_state()

        if result.success:
            # Brief success indication
            self._generate_button.setText("Success!")
            # Reset after 2 seconds would be nice, but keeping it simple
        else:
            print(f"Generation failed: {result.error_message}")

    def _update_controls_from_config(self):
        """Update all controls to reflect current config."""
        self._mode_toggle.set_mode(self._current_config.mode)
        self._length_selector.set_value(self._current_config.length)
        self._level_selector.set_value(self._current_config.level)
        self._turn_intensity_selector.set_value(self._current_config.turn_intensity)
        self._grid_mode_selector.set_value(self._current_config.grid_mode)
        self._prop_continuity_toggle.set_value(self._current_config.prop_continuity)

        if self._current_config.letter_types:
            self._letter_type_selector.set_value(self._current_config.letter_types)

        self._slice_size_selector.set_value(self._current_config.slice_size)
        if self._current_config.cap_type:
            self._cap_type_selector.set_value(self._current_config.cap_type)

        # Update visibility based on mode
        self._on_mode_changed(self._current_config.mode)

    def _initialize_controller(self) -> None:
        """Initialize the generation controller."""
        if not self._container:
            return

        try:
            from .generate_tab_controller import GenerateTabController

            self._controller = GenerateTabController(self._container, self)
            self._controller.set_generate_panel(self)

            # Connect controller signals
            self._controller.generation_completed.connect(self._on_generation_completed)
            self._controller.config_changed.connect(self._on_controller_config_changed)

            print("✅ Generation controller initialized")

        except Exception as e:
            print(f"❌ Failed to initialize generation controller: {e!s}")
            # Continue without controller - panel will work in standalone mode

    def _on_generation_completed(self, result: GenerationResult) -> None:
        """Handle generation completion from controller."""
        self.set_generation_result(result)

        if result.success:
            print(f"✅ Generation completed: {len(result.sequence_data or [])} beats")
        else:
            print(f"❌ Generation failed: {result.error_message}")

    def _on_controller_config_changed(self, config: GenerationConfig) -> None:
        """Handle configuration change from controller."""
        self._current_config = config
        self._current_state = self._current_state.with_config(config)
        self._update_controls_from_config()

    def get_controller(self) -> GenerateTabController | None:
        """Get the current controller instance."""
        return self._controller
