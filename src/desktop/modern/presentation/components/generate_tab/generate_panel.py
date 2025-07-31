"""
Modern Generate Panel with Tasteful Glassmorphism
================================================

A clean, single-card design that fits all controls on one screen
while maintaining the legacy layout structure with subtle glass effects.
"""

from typing import TYPE_CHECKING, Optional

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFrame,
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
from desktop.modern.presentation.styles.glassmorphism_styles import (
    GlassmorphismStyleGenerator,
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
        container: Optional["DIContainer"] = None,
        parent: Optional[QWidget] = None,
    ):
        super().__init__(parent)
        self._container = container
        self._controller: Optional[GenerateTabController] = None

        self._current_config = GenerationConfig()
        self._current_state = GenerationState(config=self._current_config)

        self._setup_ui()
        self._connect_signals()
        self._apply_glassmorphism_theme()

        # Initialize controller if container is provided
        if self._container:
            self._initialize_controller()

    def _setup_ui(self):
        """Setup UI with single glass container following legacy structure."""
        # Main layout with minimal padding
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)

        # Single glass container for everything
        glass_container = QFrame()
        glass_container.setFrameStyle(QFrame.Shape.StyledPanel)
        container_layout = QVBoxLayout(glass_container)
        container_layout.setContentsMargins(24, 24, 24, 24)
        container_layout.setSpacing(16)

        # Header section
        self._setup_header(container_layout)

        # Controls section - follows legacy layout exactly
        self._setup_controls_section(container_layout)

        # Action buttons section
        self._setup_action_buttons(container_layout)

        # Apply glass styling to container using established system
        glass_container.setStyleSheet(
            GlassmorphismStyleGenerator.create_container_style(
                variant="default", custom_properties={"border-radius": "16px"}
            )
        )

        main_layout.addWidget(glass_container)

    def _setup_header(self, layout: QVBoxLayout):
        """Create header section matching legacy customize sequence label."""
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header = QLabel("Customize Your Sequence")
        header_font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet(
            """
            QLabel {
                color: rgba(255, 255, 255, 0.95);
                padding: 8px;
                background: transparent;
                border: none;
            }
        """
        )

        header_layout.addWidget(header)
        layout.addLayout(header_layout)

    def _setup_controls_section(self, layout: QVBoxLayout):
        """Setup controls section with proper spacing allocation."""
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(20)  # Increased spacing between sections
        controls_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create all controls matching legacy order
        self._level_selector = LevelSelector()
        self._length_selector = LengthSelector()
        self._turn_intensity_selector = TurnIntensitySelector()
        self._grid_mode_selector = ModernGridModeSelector()
        self._mode_toggle = GenerationModeToggle()
        self._prop_continuity_toggle = PropContinuityToggle()
        self._letter_type_selector = LetterTypeSelector()
        self._slice_size_selector = SliceSizeSelector()
        self._cap_type_selector = CAPTypeSelector()

        # Add controls with proper spacing allocation
        # Level selector gets more space since it has 3 large buttons + descriptions
        controls_layout.addWidget(
            self._level_selector, 3
        )  # More space for 3-level layout
        controls_layout.addWidget(self._length_selector, 1)
        controls_layout.addWidget(self._turn_intensity_selector, 1)
        controls_layout.addWidget(self._grid_mode_selector, 1)
        controls_layout.addWidget(self._mode_toggle, 1)
        controls_layout.addWidget(self._prop_continuity_toggle, 1)
        # Letter type selector needs more space for checkboxes
        controls_layout.addWidget(self._letter_type_selector, 2)
        controls_layout.addWidget(self._slice_size_selector, 1)
        controls_layout.addWidget(self._cap_type_selector, 1)

        layout.addLayout(controls_layout, 18)  # Increased from 16 to give more room

    def _setup_action_buttons(self, layout: QVBoxLayout):
        """Setup action buttons with proper spacing."""
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setSpacing(60)  # More space between buttons

        # Create buttons using standard QPushButton
        self._auto_complete_button = QPushButton("Auto-Complete")
        self._generate_button = QPushButton("Generate New")

        # Apply glassmorphism styling using the established system
        self._auto_complete_button.setStyleSheet(
            GlassmorphismStyleGenerator.create_button_style(
                variant="default",
                size="large",
                custom_properties={"min-width": "140px", "min-height": "45px"},
            )
        )

        self._generate_button.setStyleSheet(
            GlassmorphismStyleGenerator.create_button_style(
                variant="accent",
                size="large",
                custom_properties={"min-width": "140px", "min-height": "45px"},
            )
        )

        # Set cursor for better UX
        self._auto_complete_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._generate_button.setCursor(Qt.CursorShape.PointingHandCursor)

        button_layout.addWidget(self._auto_complete_button)
        button_layout.addWidget(self._generate_button)

        layout.addLayout(
            button_layout, 3
        )  # Reduced from 4 to give more space to controls

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
            print(f"❌ Failed to initialize generation controller: {str(e)}")
            # Continue without controller - panel will work in standalone mode

    def set_controller(self, controller: "GenerateTabController") -> None:
        """Set the generation controller manually."""
        self._controller = controller
        controller.set_generate_panel(self)

        # Connect controller signals
        controller.generation_completed.connect(self._on_generation_completed)
        controller.config_changed.connect(self._on_controller_config_changed)

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

    def get_controller(self) -> Optional["GenerateTabController"]:
        """Get the current controller instance."""
        return self._controller
