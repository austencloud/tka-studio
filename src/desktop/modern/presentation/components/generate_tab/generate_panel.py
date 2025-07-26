"""
Modern Generate Panel with Tasteful Glassmorphism
================================================

A clean, single-card design that fits all controls on one screen
while maintaining the legacy layout structure with subtle glass effects.
"""

from typing import Optional

from desktop.modern.core.interfaces.generation_services import GenerationMode
from desktop.modern.domain.models.generation_models import (
    GenerationConfig,
    GenerationResult,
    GenerationState,
)
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

from .generation_controls import (
    ModernCAPTypeSelector,
    ModernGenerationModeToggle,
    ModernLengthSelector,
    ModernLetterTypeSelector,
    ModernLevelSelector,
    ModernPropContinuityToggle,
    ModernSliceSizeSelector,
    ModernTurnIntensitySelector,
)


class GlassMorphicButton(QPushButton):
    """Clean glassmorphic button with subtle effects."""

    def __init__(
        self, text: str, primary: bool = False, parent: Optional[QWidget] = None
    ):
        super().__init__(text, parent)
        self.primary = primary
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(40)
        self.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        self.setStyleSheet(self._get_button_style())

    def _get_button_style(self):
        if self.primary:
            return """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(70, 130, 255, 0.8),
                        stop:1 rgba(50, 110, 235, 0.9));
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 8px;
                    padding: 8px 20px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(80, 140, 255, 0.9),
                        stop:1 rgba(60, 120, 245, 1.0));
                    border: 1px solid rgba(255, 255, 255, 0.3);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(60, 120, 235, 0.7),
                        stop:1 rgba(40, 100, 215, 0.8));
                }
                QPushButton:disabled {
                    background: rgba(100, 100, 100, 0.3);
                    color: rgba(255, 255, 255, 0.5);
                    border: 1px solid rgba(255, 255, 255, 0.1);
                }
            """
        else:
            return """
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255, 255, 255, 0.15),
                        stop:1 rgba(255, 255, 255, 0.08));
                    color: rgba(255, 255, 255, 0.9);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                    border-radius: 8px;
                    padding: 8px 20px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255, 255, 255, 0.2),
                        stop:1 rgba(255, 255, 255, 0.12));
                    border: 1px solid rgba(255, 255, 255, 0.3);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(255, 255, 255, 0.1),
                        stop:1 rgba(255, 255, 255, 0.05));
                }
            """


class GeneratePanel(QWidget):
    """
    Modern Generate Panel with single glass card container.
    
    Maintains legacy layout structure while adding subtle glassmorphism effects.
    Everything fits on one screen without scrolling.
    """

    generate_requested = pyqtSignal(GenerationConfig)
    auto_complete_requested = pyqtSignal()
    config_changed = pyqtSignal(GenerationConfig)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._current_config = GenerationConfig()
        self._current_state = GenerationState(config=self._current_config)
        self._setup_ui()
        self._connect_signals()
        self._apply_glassmorphism_theme()

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

        # Apply glass styling to container
        glass_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.12),
                    stop:1 rgba(255, 255, 255, 0.08));
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
            }
        """)

        main_layout.addWidget(glass_container)

    def _setup_header(self, layout: QVBoxLayout):
        """Create header section matching legacy customize sequence label."""
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header = QLabel("Customize Your Sequence")
        header_font = QFont("Segoe UI", 16, QFont.Weight.Bold)
        header.setFont(header_font)
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.95);
                padding: 8px;
                background: transparent;
                border: none;
            }
        """)

        header_layout.addWidget(header)
        layout.addLayout(header_layout)

    def _setup_controls_section(self, layout: QVBoxLayout):
        """Setup controls section following legacy vertical layout."""
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(12)
        controls_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create all controls matching legacy order
        self._level_selector = ModernLevelSelector()
        self._length_selector = ModernLengthSelector()
        self._turn_intensity_selector = ModernTurnIntensitySelector()
        self._mode_toggle = ModernGenerationModeToggle()
        self._prop_continuity_toggle = ModernPropContinuityToggle()
        self._letter_type_selector = ModernLetterTypeSelector()
        self._slice_size_selector = ModernSliceSizeSelector()
        self._cap_type_selector = ModernCAPTypeSelector()

        # Add controls in legacy order with equal stretch
        controls_layout.addWidget(self._level_selector, 1)
        controls_layout.addWidget(self._length_selector, 1)
        controls_layout.addWidget(self._turn_intensity_selector, 1)
        controls_layout.addWidget(self._mode_toggle, 1)
        controls_layout.addWidget(self._prop_continuity_toggle, 1)
        controls_layout.addWidget(self._letter_type_selector, 1)
        controls_layout.addWidget(self._slice_size_selector, 1)
        controls_layout.addWidget(self._cap_type_selector, 1)

        layout.addLayout(controls_layout, 16)  # Match legacy proportions

    def _setup_action_buttons(self, layout: QVBoxLayout):
        """Setup action buttons matching legacy layout."""
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setSpacing(40)  # Reasonable spacing between buttons

        self._auto_complete_button = GlassMorphicButton("Auto-Complete", primary=False)
        self._generate_button = GlassMorphicButton("Generate New", primary=True)

        button_layout.addWidget(self._auto_complete_button)
        button_layout.addWidget(self._generate_button)

        layout.addLayout(button_layout, 4)  # Match legacy proportions

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
        self.setStyleSheet("""
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
        """)

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
            self._current_config = self._current_config.with_updates(**kwargs)
            self._current_state = self._current_state.with_config(self._current_config)
            self.config_changed.emit(self._current_config)
        except Exception as e:
            print(f"Configuration error: {e}")

    def _on_generate_clicked(self):
        """Handle generate button click."""
        if self._current_state.is_generating:
            return

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
        self._prop_continuity_toggle.set_value(self._current_config.prop_continuity)

        if self._current_config.letter_types:
            self._letter_type_selector.set_value(self._current_config.letter_types)

        self._slice_size_selector.set_value(self._current_config.slice_size)
        if self._current_config.cap_type:
            self._cap_type_selector.set_value(self._current_config.cap_type)

        # Update visibility based on mode
        self._on_mode_changed(self._current_config.mode)
