"""
Professional Graph Editor for TKA
=================================

A visually rich, pictograph-centered graph editor component designed for embedded use
in stack widgets. Features a modern UI with pictograph display and dual adjustment panels.
"""

import logging
from typing import Optional, TYPE_CHECKING
from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
    QSizePolicy,
    QSlider,
    QSpinBox,
    QComboBox,
    QGroupBox,
    QGridLayout,
    QSplitter,
    QColorDialog,
    QStackedWidget,
)
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QPainter, QColor, QPen

from domain.models.core_models import SequenceData, BeatData
from core.interfaces.workbench_services import IGraphEditorService

# Import pictograph rendering components
from presentation.components.pictograph.pictograph_scene import PictographScene

# Import beat view for internal beat display
from presentation.components.workbench.sequence_beat_frame.beat_view import BeatView

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from presentation.components.workbench.workbench import SequenceWorkbench


class PictographDisplayWidget(QWidget):
    """
    Custom widget for displaying pictographs in the graph editor.
    Handles scaling, centering, and fallback display.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 200)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._pixmap: Optional[QPixmap] = None
        self._placeholder_text = "No beat selected"
        self._setup_styling()

    def _setup_styling(self):
        """Apply styling to the pictograph display"""
        self.setStyleSheet(
            """
            PictographDisplayWidget {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
            }
        """
        )

    def set_pictograph(self, pixmap: Optional[QPixmap]):
        """Set the pictograph to display"""
        self._pixmap = pixmap
        self.update()

    def set_placeholder_text(self, text: str):
        """Set the placeholder text when no pictograph is available"""
        self._placeholder_text = text
        self.update()

    def paintEvent(self, event):
        """Custom paint event to draw the pictograph or placeholder"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Fill background
        painter.fillRect(self.rect(), QColor("#ffffff"))

        if self._pixmap and not self._pixmap.isNull():
            # Calculate scaled size maintaining aspect ratio
            widget_size = self.size()
            pixmap_size = self._pixmap.size()

            # Scale to fit within widget while maintaining aspect ratio
            scaled_size = pixmap_size.scaled(
                widget_size, Qt.AspectRatioMode.KeepAspectRatio
            )

            # Center the pixmap
            x = (widget_size.width() - scaled_size.width()) // 2
            y = (widget_size.height() - scaled_size.height()) // 2

            # Draw the scaled pixmap
            scaled_pixmap = self._pixmap.scaled(
                scaled_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            painter.drawPixmap(x, y, scaled_pixmap)
        else:
            # Draw placeholder text
            painter.setPen(QColor("#999999"))
            font = QFont()
            font.setPointSize(14)
            font.setItalic(True)
            painter.setFont(font)
            painter.drawText(
                self.rect(), Qt.AlignmentFlag.AlignCenter, self._placeholder_text
            )


class GraphEditor(QFrame):
    """
    Professional Graph Editor for TKA

    A visually rich, pictograph-centered graph editor component with modern UI design.
    Features pictograph display area and dual adjustment panels for beat and arrow properties.
    """

    # Signals for external communication
    beat_modified = pyqtSignal(int, object)  # beat_index, beat_data
    arrow_selected = pyqtSignal(object)  # arrow_data
    visibility_changed = pyqtSignal(bool)  # is_visible

    def __init__(
        self,
        graph_service: Optional[IGraphEditorService] = None,
        parent: Optional["SequenceWorkbench"] = None,
        workbench_width: int = 800,
        workbench_height: int = 600,
    ):
        super().__init__(parent)
        self._graph_service = graph_service
        self._parent_workbench = parent
        self._current_sequence: Optional[SequenceData] = None
        self._selected_beat_index: Optional[int] = None
        self._selected_beat_data: Optional[BeatData] = None

        # UI Components
        self._pictograph_display: Optional[PictographDisplayWidget] = None
        self._adjustment_stack: Optional[QStackedWidget] = None

        # Beat display component (like legacy graph editor)
        self._beat_display: Optional[BeatView] = None

        # Blue/Red orientation labels (like legacy)
        self._blue_orientation_label: Optional[QLabel] = None
        self._red_orientation_label: Optional[QLabel] = None

        # Blue/Red turn controls (like legacy)
        self._blue_cw_btn: Optional[QPushButton] = None
        self._blue_ccw_btn: Optional[QPushButton] = None
        self._blue_amount_label: Optional[QLabel] = None
        self._red_cw_btn: Optional[QPushButton] = None
        self._red_ccw_btn: Optional[QPushButton] = None
        self._red_amount_label: Optional[QLabel] = None

        # State tracking
        self._blue_turn_amount = 0
        self._red_turn_amount = 0
        self._blue_orientation = "IN"
        self._red_orientation = "IN"

        # Set up the UI
        self._setup_ui()
        self._setup_styling()

        # Set initial size
        self.setMinimumSize(400, 300)
        self.resize(workbench_width, 300)  # Fixed height for embedded mode

        logger.info("Professional graph editor initialized successfully")

    def _setup_ui(self) -> None:
        """Set up the professional user interface with pictograph display and dual panels"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Create vertical splitter for main sections
        main_splitter = QSplitter(Qt.Orientation.Vertical)
        main_splitter.setChildrenCollapsible(False)

        # Top Section: Pictograph Display Area (60% of height)
        pictograph_section = self._create_pictograph_section()
        main_splitter.addWidget(pictograph_section)

        # Bottom Section: Dual Adjustment Panels (40% of height)
        adjustment_section = self._create_adjustment_section()
        main_splitter.addWidget(adjustment_section)

        # Set splitter proportions (60/40 split)
        main_splitter.setSizes([180, 120])  # Proportional to 300px total height

        main_layout.addWidget(main_splitter)

    def _create_pictograph_section(self) -> QWidget:
        """Create the top pictograph display section"""
        section = QGroupBox("Beat Visualization")
        layout = QVBoxLayout(section)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(5)

        # Create horizontal layout for pictograph and beat display
        display_layout = QHBoxLayout()
        display_layout.setSpacing(10)

        # Pictograph display widget (main display)
        self._pictograph_display = PictographDisplayWidget()
        display_layout.addWidget(self._pictograph_display, 3)  # 75% width

        # Beat display widget (shows selected beat like legacy)
        self._beat_display = BeatView(beat_number=1, parent=self)
        self._beat_display.setFixedSize(100, 100)  # Small square like legacy
        self._beat_display.setToolTip("Currently selected beat")
        display_layout.addWidget(self._beat_display, 1)  # 25% width

        layout.addLayout(display_layout, 1)  # Give it stretch

        # Status label below pictograph
        self._pictograph_status = QLabel("No beat selected")
        self._pictograph_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._pictograph_status.setStyleSheet(
            "color: #666; font-style: italic; padding: 5px;"
        )
        layout.addWidget(self._pictograph_status)

        return section

    def _create_adjustment_section(self) -> QWidget:
        """Create the bottom dual adjustment panels section (matches legacy blue/red structure)"""
        section = QWidget()
        layout = QVBoxLayout(section)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Create stacked widget for context-sensitive panels (like legacy)
        self._adjustment_stack = QStackedWidget()

        # Index 0: Orientation Picker Panels (like legacy ORI_WIDGET_INDEX)
        orientation_panel = self._create_dual_orientation_panels()
        self._adjustment_stack.addWidget(orientation_panel)

        # Index 1: Turns Adjustment Panels (like legacy TURNS_WIDGET_INDEX)
        turns_panel = self._create_dual_turns_panels()
        self._adjustment_stack.addWidget(turns_panel)

        # Default to orientation panels
        self._adjustment_stack.setCurrentIndex(0)

        layout.addWidget(self._adjustment_stack)
        return section

    def _create_dual_orientation_panels(self) -> QWidget:
        """Create dual blue/red orientation picker panels (like legacy OriPickerBox)"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Blue orientation picker (like legacy blue OriPickerBox)
        blue_panel = self._create_orientation_picker_panel("blue")
        layout.addWidget(blue_panel, 1)

        # Red orientation picker (like legacy red OriPickerBox)
        red_panel = self._create_orientation_picker_panel("red")
        layout.addWidget(red_panel, 1)

        return container

    def _create_orientation_picker_panel(self, color: str) -> QWidget:
        """Create single orientation picker panel for blue or red (like legacy OriPickerBox)"""
        panel = QGroupBox(f"{color.title()} Orientation")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(8)

        # Current orientation display (like legacy clickable_ori_label)
        orientation_label = QLabel("IN")
        orientation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        orientation_label.setStyleSheet(
            f"""
            QLabel {{
                background-color: rgba(255, 255, 255, 0.9);
                border: 2px solid {'#0066cc' if color == 'blue' else '#cc0000'};
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
                font-size: 16px;
                color: {'#0066cc' if color == 'blue' else '#cc0000'};
                min-height: 30px;
            }}
        """
        )
        layout.addWidget(orientation_label)

        # Orientation buttons (like legacy orientation selection)
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(5)

        orientations = ["IN", "OUT", "CLOCK", "COUNTER"]
        for orientation in orientations:
            btn = QPushButton(orientation)
            btn.setFixedSize(60, 30)
            btn.clicked.connect(
                lambda checked, ori=orientation, c=color: self._set_orientation(c, ori)
            )
            buttons_layout.addWidget(btn)

        layout.addWidget(buttons_widget)

        # Store reference for updates
        if color == "blue":
            self._blue_orientation_label = orientation_label
        else:
            self._red_orientation_label = orientation_label

        # Apply color-specific styling (like legacy blue/red boxes)
        panel.setStyleSheet(
            f"""
            QGroupBox {{
                background-color: rgba({'0, 102, 204' if color == 'blue' else '204, 0, 0'}, 0.1);
                border: 2px solid {'#0066cc' if color == 'blue' else '#cc0000'};
                border-radius: 8px;
                font-weight: bold;
                color: {'#0066cc' if color == 'blue' else '#cc0000'};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background-color: rgba(255, 255, 255, 0.9);
            }}
        """
        )

        return panel

    def _create_dual_turns_panels(self) -> QWidget:
        """Create dual blue/red turns adjustment panels (like legacy TurnsBox)"""
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Blue turns box (like legacy blue TurnsBox)
        blue_panel = self._create_turns_panel("blue")
        layout.addWidget(blue_panel, 1)

        # Red turns box (like legacy red TurnsBox)
        red_panel = self._create_turns_panel("red")
        layout.addWidget(red_panel, 1)

        return container

    def _create_turns_panel(self, color: str) -> QWidget:
        """Create single turns adjustment panel for blue or red (like legacy TurnsBox)"""
        panel = QGroupBox(f"{color.title()} Turns")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(8)

        # Rotation direction buttons (like legacy PropRotDirButton)
        direction_widget = QWidget()
        direction_layout = QHBoxLayout(direction_widget)
        direction_layout.setContentsMargins(0, 0, 0, 0)
        direction_layout.setSpacing(5)

        # Clockwise button
        cw_btn = QPushButton("⟲ CW")
        cw_btn.setCheckable(True)
        cw_btn.setFixedSize(60, 30)
        cw_btn.clicked.connect(lambda: self._set_rotation_direction(color, "CLOCKWISE"))
        direction_layout.addWidget(cw_btn)

        # Counter-clockwise button
        ccw_btn = QPushButton("⟳ CCW")
        ccw_btn.setCheckable(True)
        ccw_btn.setFixedSize(60, 30)
        ccw_btn.clicked.connect(
            lambda: self._set_rotation_direction(color, "COUNTER_CLOCKWISE")
        )
        direction_layout.addWidget(ccw_btn)

        layout.addWidget(direction_widget)

        # Turn amount controls (like legacy turns adjustment)
        amount_widget = QWidget()
        amount_layout = QHBoxLayout(amount_widget)
        amount_layout.setContentsMargins(0, 0, 0, 0)
        amount_layout.setSpacing(5)

        # Decrease button
        dec_btn = QPushButton("-")
        dec_btn.setFixedSize(30, 30)
        dec_btn.clicked.connect(lambda: self._adjust_turn_amount(color, -1))
        amount_layout.addWidget(dec_btn)

        # Turn amount display
        amount_label = QLabel("0")
        amount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        amount_label.setStyleSheet(
            """
            QLabel {
                background-color: rgba(255, 255, 255, 0.9);
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
                min-width: 40px;
            }
        """
        )
        amount_layout.addWidget(amount_label)

        # Increase button
        inc_btn = QPushButton("+")
        inc_btn.setFixedSize(30, 30)
        inc_btn.clicked.connect(lambda: self._adjust_turn_amount(color, 1))
        amount_layout.addWidget(inc_btn)

        layout.addWidget(amount_widget)

        # Store references for updates
        if color == "blue":
            self._blue_cw_btn = cw_btn
            self._blue_ccw_btn = ccw_btn
            self._blue_amount_label = amount_label
        else:
            self._red_cw_btn = cw_btn
            self._red_ccw_btn = ccw_btn
            self._red_amount_label = amount_label

        # Apply color-specific styling (like legacy blue/red boxes)
        panel.setStyleSheet(
            f"""
            QGroupBox {{
                background-color: rgba({'0, 102, 204' if color == 'blue' else '204, 0, 0'}, 0.1);
                border: 2px solid {'#0066cc' if color == 'blue' else '#cc0000'};
                border-radius: 8px;
                font-weight: bold;
                color: {'#0066cc' if color == 'blue' else '#cc0000'};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background-color: rgba(255, 255, 255, 0.9);
            }}
        """
        )

        return panel

    def _setup_styling(self) -> None:
        """Create beat adjustment panel (matches legacy TurnsBox)"""
        panel = QGroupBox("Beat Adjustment")
        layout = QGridLayout(panel)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(8)

        # Turn controls (like legacy turns_widget)
        layout.addWidget(QLabel("Turn Direction:"), 0, 0)

        # Rotation direction buttons (like legacy PropRotDirButton)
        rotation_widget = QWidget()
        rotation_layout = QHBoxLayout(rotation_widget)
        rotation_layout.setContentsMargins(0, 0, 0, 0)
        rotation_layout.setSpacing(10)

        # Clockwise button (like legacy cw_button)
        self._clockwise_button = QPushButton("⟲ Clockwise")
        self._clockwise_button.setCheckable(True)
        self._clockwise_button.clicked.connect(
            lambda: self._set_rotation_direction("CLOCKWISE")
        )
        rotation_layout.addWidget(self._clockwise_button)

        # Counter-clockwise button (like legacy ccw_button)
        self._counter_clockwise_button = QPushButton("⟳ Counter-CW")
        self._counter_clockwise_button.setCheckable(True)
        self._counter_clockwise_button.clicked.connect(
            lambda: self._set_rotation_direction("COUNTER_CLOCKWISE")
        )
        rotation_layout.addWidget(self._counter_clockwise_button)

        layout.addWidget(rotation_widget, 0, 1, 1, 2)

        # Turn amount controls (like legacy turns adjustment)
        layout.addWidget(QLabel("Turn Amount:"), 1, 0)

        # Turn value display and controls
        turn_controls_widget = QWidget()
        turn_controls_layout = QHBoxLayout(turn_controls_widget)
        turn_controls_layout.setContentsMargins(0, 0, 0, 0)
        turn_controls_layout.setSpacing(5)

        # Decrease button
        decrease_btn = QPushButton("-")
        decrease_btn.setFixedSize(30, 30)
        decrease_btn.clicked.connect(self._decrease_turn_amount)
        turn_controls_layout.addWidget(decrease_btn)

        # Turn amount display
        self._turn_amount_label = QLabel("0")
        self._turn_amount_label.setStyleSheet(
            """
            QLabel {
                background-color: #ffffff;
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
                min-width: 40px;
                text-align: center;
            }
        """
        )
        self._turn_amount_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        turn_controls_layout.addWidget(self._turn_amount_label)

        # Increase button
        increase_btn = QPushButton("+")
        increase_btn.setFixedSize(30, 30)
        increase_btn.clicked.connect(self._increase_turn_amount)
        turn_controls_layout.addWidget(increase_btn)

        layout.addWidget(turn_controls_widget, 1, 1, 1, 2)

        # Apply button (like legacy turns adjustment functionality)
        apply_beat_btn = QPushButton("Apply Beat Changes")
        apply_beat_btn.clicked.connect(self._apply_beat_adjustment_changes)
        layout.addWidget(apply_beat_btn, 2, 0, 1, 3)

        return panel

    def _setup_styling(self) -> None:
        """Create the left panel for beat properties"""
        panel = QGroupBox("Beat Properties")
        layout = QGridLayout(panel)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(8)

        # Duration controls
        layout.addWidget(QLabel("Duration:"), 0, 0)

        # Duration slider
        self._duration_slider = QSlider(Qt.Orientation.Horizontal)
        self._duration_slider.setRange(1, 10)
        self._duration_slider.setValue(1)
        self._duration_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._duration_slider.setTickInterval(1)
        self._duration_slider.valueChanged.connect(self._on_duration_slider_changed)
        layout.addWidget(self._duration_slider, 0, 1)

        # Duration spinbox
        self._duration_spinbox = QSpinBox()
        self._duration_spinbox.setRange(1, 10)
        self._duration_spinbox.setValue(1)
        self._duration_spinbox.setSuffix(" beats")
        self._duration_spinbox.valueChanged.connect(self._on_duration_spinbox_changed)
        layout.addWidget(self._duration_spinbox, 0, 2)

        # Motion type dropdown
        layout.addWidget(QLabel("Motion Type:"), 1, 0)
        self._motion_type_combo = QComboBox()
        self._motion_type_combo.addItems(["Static", "Shift", "Dash", "Float"])
        self._motion_type_combo.currentTextChanged.connect(self._on_motion_type_changed)
        layout.addWidget(self._motion_type_combo, 1, 1, 1, 2)

        # Apply button
        apply_beat_btn = QPushButton("Apply Beat Changes")
        apply_beat_btn.clicked.connect(self._apply_beat_changes)
        layout.addWidget(apply_beat_btn, 2, 0, 1, 3)

        return panel

    def _create_arrow_properties_panel(self) -> QWidget:
        """Create the right panel for arrow properties"""
        panel = QGroupBox("Arrow Properties")
        layout = QGridLayout(panel)
        layout.setContentsMargins(10, 15, 10, 10)
        layout.setSpacing(8)

        # Arrow direction
        layout.addWidget(QLabel("Direction:"), 0, 0)
        self._arrow_direction_combo = QComboBox()
        self._arrow_direction_combo.addItems(
            [
                "↑ North",
                "↗ Northeast",
                "→ East",
                "↘ Southeast",
                "↓ South",
                "↙ Southwest",
                "← West",
                "↖ Northwest",
            ]
        )
        self._arrow_direction_combo.currentTextChanged.connect(
            self._on_arrow_direction_changed
        )
        layout.addWidget(self._arrow_direction_combo, 0, 1, 1, 2)

        # Arrow color
        layout.addWidget(QLabel("Color:"), 1, 0)
        self._arrow_color_button = QPushButton()
        self._arrow_color_button.setFixedSize(60, 30)
        self._arrow_color_button.clicked.connect(self._choose_arrow_color)
        self._update_color_button()
        layout.addWidget(self._arrow_color_button, 1, 1)

        # Color preset buttons
        preset_layout = QHBoxLayout()
        preset_colors = [
            ("#0066cc", "Blue"),
            ("#cc0000", "Red"),
            ("#00cc00", "Green"),
            ("#cc6600", "Orange"),
        ]
        for color_hex, color_name in preset_colors:
            preset_btn = QPushButton()
            preset_btn.setFixedSize(25, 25)
            preset_btn.setStyleSheet(
                f"background-color: {color_hex}; border: 1px solid #999;"
            )
            preset_btn.setToolTip(color_name)
            preset_btn.clicked.connect(
                lambda checked, c=color_hex: self._set_preset_color(c)
            )
            preset_layout.addWidget(preset_btn)

        preset_widget = QWidget()
        preset_widget.setLayout(preset_layout)
        layout.addWidget(preset_widget, 1, 2)

        # Arrow style
        layout.addWidget(QLabel("Style:"), 2, 0)
        arrow_style_combo = QComboBox()
        arrow_style_combo.addItems(["Solid", "Dashed", "Dotted", "Thick"])
        layout.addWidget(arrow_style_combo, 2, 1, 1, 2)

        # Apply button
        apply_arrow_btn = QPushButton("Apply Arrow Changes")
        apply_arrow_btn.clicked.connect(self._apply_arrow_changes)
        layout.addWidget(apply_arrow_btn, 3, 0, 1, 3)

        return panel

    def _setup_styling(self) -> None:
        """Apply glassmorphism styling to the graph editor for animated background"""
        self.setStyleSheet(
            """
            /* Main Graph Editor Frame - Glassmorphism */
            GraphEditor {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
            }

            /* Pictograph Display Widget - Glass effect */
            PictographDisplayWidget {
                background: rgba(255, 255, 255, 0.15);
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 12px;
                backdrop-filter: blur(8px);
                -webkit-backdrop-filter: blur(8px);
            }

            /* Group Boxes - Glass panels */
            QGroupBox {
                font-weight: bold;
                font-size: 12px;
                color: rgba(255, 255, 255, 0.9);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                margin-top: 12px;
                padding-top: 8px;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(6px);
                -webkit-backdrop-filter: blur(6px);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 4px;
                color: rgba(255, 255, 255, 0.95);
            }

            /* Buttons - Glass effect */
            QPushButton {
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 11px;
                color: rgba(255, 255, 255, 0.9);
                font-weight: 500;
                min-height: 20px;
                backdrop-filter: blur(4px);
                -webkit-backdrop-filter: blur(4px);
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.25);
                border-color: rgba(255, 255, 255, 0.4);
                color: rgba(255, 255, 255, 1.0);
            }
            QPushButton:pressed {
                background: rgba(255, 255, 255, 0.35);
                border-color: rgba(255, 255, 255, 0.5);
            }
            QPushButton:checked {
                background: rgba(0, 102, 204, 0.3);
                border-color: rgba(0, 102, 204, 0.6);
                color: rgba(255, 255, 255, 1.0);
            }

            /* Labels - Glass text */
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 11px;
                font-weight: 500;
            }

            /* Stacked Widget - Transparent */
            QStackedWidget {
                background: transparent;
                border: none;
            }

            /* Container Widgets - Transparent */
            QWidget {
                background: transparent;
                border: none;
            }
        """
        )

    # Event Handlers
    def _on_duration_slider_changed(self, value: int):
        """Handle duration slider changes"""
        if self._duration_spinbox:
            self._duration_spinbox.blockSignals(True)
            self._duration_spinbox.setValue(value)
            self._duration_spinbox.blockSignals(False)
        logger.info(f"Duration slider changed to {value}")

    def _on_duration_spinbox_changed(self, value: int):
        """Handle duration spinbox changes"""
        if self._duration_slider:
            self._duration_slider.blockSignals(True)
            self._duration_slider.setValue(value)
            self._duration_slider.blockSignals(False)
        logger.info(f"Duration spinbox changed to {value}")

    def _on_motion_type_changed(self, motion_type: str):
        """Handle motion type changes"""
        logger.info(f"Motion type changed to {motion_type}")

    def _on_arrow_direction_changed(self, direction: str):
        """Handle arrow direction changes"""
        logger.info(f"Arrow direction changed to {direction}")

    def _apply_beat_changes(self):
        """Apply beat property changes"""
        if self._selected_beat_data and self._selected_beat_index is not None:
            # Get current values
            duration = self._duration_spinbox.value() if self._duration_spinbox else 1
            motion_type = (
                self._motion_type_combo.currentText()
                if self._motion_type_combo
                else "Static"
            )

            # Create updated beat data
            updated_beat = self._selected_beat_data.update(duration=float(duration))

            # Emit signal for external handling
            self.beat_modified.emit(self._selected_beat_index, updated_beat)

            # Update status
            if self._pictograph_status:
                self._pictograph_status.setText(
                    f"Beat {self._selected_beat_index} updated"
                )

            logger.info(
                f"Beat changes applied: duration={duration}, motion={motion_type}"
            )

    def _apply_arrow_changes(self):
        """Apply arrow property changes"""
        direction = (
            self._arrow_direction_combo.currentText()
            if self._arrow_direction_combo
            else "↑ North"
        )
        color = self._current_arrow_color.name()

        # Create arrow data object
        arrow_data = {
            "direction": direction,
            "color": color,
            "beat_index": self._selected_beat_index,
        }

        # Emit signal for external handling
        self.arrow_selected.emit(arrow_data)

        # Update status
        if self._pictograph_status:
            self._pictograph_status.setText(f"Arrow updated: {direction}")

        logger.info(f"Arrow changes applied: direction={direction}, color={color}")

    def _choose_arrow_color(self):
        """Open color dialog for arrow color selection"""
        color = QColorDialog.getColor(
            self._current_arrow_color, self, "Choose Arrow Color"
        )
        if color.isValid():
            self._current_arrow_color = color
            self._update_color_button()
            logger.info(f"Arrow color changed to {color.name()}")

    def _set_preset_color(self, color_hex: str):
        """Set arrow color from preset"""
        self._current_arrow_color = QColor(color_hex)
        self._update_color_button()
        logger.info(f"Arrow color set to preset {color_hex}")

    def _update_color_button(self):
        """Update the color button appearance"""
        if self._arrow_color_button:
            color_name = self._current_arrow_color.name()
            self._arrow_color_button.setStyleSheet(
                f"background-color: {color_name}; border: 1px solid #999; border-radius: 4px;"
            )
            self._arrow_color_button.setText("")

    # Dual Blue/Red Panel Event Handlers (Legacy-style)
    def _set_orientation(self, color: str, orientation: str):
        """Set orientation for blue or red panel (like legacy ori_setter)"""
        if color == "blue":
            self._blue_orientation = orientation
            if self._blue_orientation_label:
                self._blue_orientation_label.setText(orientation)
        else:
            self._red_orientation = orientation
            if self._red_orientation_label:
                self._red_orientation_label.setText(orientation)

        # Emit signal for external handling
        orientation_data = {
            "color": color,
            "orientation": orientation,
            "type": "orientation_change",
        }
        self.arrow_selected.emit(orientation_data)

        # Update pictograph status
        if self._pictograph_status:
            self._pictograph_status.setText(
                f"{color.title()} orientation: {orientation}"
            )

        logger.info(f"{color.title()} orientation set to: {orientation}")

    def _set_rotation_direction(self, color: str, direction: str):
        """Set rotation direction for blue or red panel (like legacy PropRotDirButton)"""
        if color == "blue":
            # Update blue button states (exclusive selection)
            if self._blue_cw_btn and self._blue_ccw_btn:
                if direction == "CLOCKWISE":
                    self._blue_cw_btn.setChecked(True)
                    self._blue_ccw_btn.setChecked(False)
                elif direction == "COUNTER_CLOCKWISE":
                    self._blue_cw_btn.setChecked(False)
                    self._blue_ccw_btn.setChecked(True)
        else:
            # Update red button states (exclusive selection)
            if self._red_cw_btn and self._red_ccw_btn:
                if direction == "CLOCKWISE":
                    self._red_cw_btn.setChecked(True)
                    self._red_ccw_btn.setChecked(False)
                elif direction == "COUNTER_CLOCKWISE":
                    self._red_cw_btn.setChecked(False)
                    self._red_ccw_btn.setChecked(True)

        # Emit signal for external handling
        rotation_data = {
            "color": color,
            "direction": direction,
            "type": "rotation_direction",
        }
        self.beat_modified.emit(0, rotation_data)  # Use 0 as placeholder beat index

        logger.info(f"{color.title()} rotation direction set to: {direction}")

    def _adjust_turn_amount(self, color: str, delta: int):
        """Adjust turn amount for blue or red panel (like legacy turns adjustment)"""
        if color == "blue":
            self._blue_turn_amount = max(0, self._blue_turn_amount + delta)
            if self._blue_amount_label:
                self._blue_amount_label.setText(str(self._blue_turn_amount))
            amount = self._blue_turn_amount
        else:
            self._red_turn_amount = max(0, self._red_turn_amount + delta)
            if self._red_amount_label:
                self._red_amount_label.setText(str(self._red_turn_amount))
            amount = self._red_turn_amount

        # Emit signal for external handling
        turn_data = {"color": color, "amount": amount, "type": "turn_amount"}
        self.beat_modified.emit(0, turn_data)  # Use 0 as placeholder beat index

        logger.info(f"{color.title()} turn amount adjusted to: {amount}")

    # Public API Methods (maintaining compatibility)
    def set_sequence(self, sequence: Optional[SequenceData]) -> None:
        """Set the sequence data for the graph editor"""
        self._current_sequence = sequence
        if sequence:
            status_text = f"Sequence: {sequence.name} ({len(sequence.beats)} beats)"
            if self._pictograph_status:
                self._pictograph_status.setText(status_text)
        else:
            if self._pictograph_status:
                self._pictograph_status.setText("No sequence loaded")
        logger.info(f"Sequence set: {sequence.name if sequence else 'None'}")

    def set_selected_beat_data(self, beat_index: int, beat_data: BeatData) -> None:
        """Set the selected beat data and update the UI (switches panels based on beat type like legacy)"""
        self._selected_beat_index = beat_index
        self._selected_beat_data = beat_data

        # Switch panels based on beat type (like legacy)
        if self._adjustment_stack:
            if beat_index == -1:
                # Start position: show orientation picker (index 0, like legacy ORI_WIDGET_INDEX)
                self._adjustment_stack.setCurrentIndex(0)
            else:
                # Regular beat: show turns adjustment panels (index 1, like legacy TURNS_WIDGET_INDEX)
                self._adjustment_stack.setCurrentIndex(1)

        if beat_data:
            # Update pictograph status
            if self._pictograph_status:
                if beat_index == -1:
                    self._pictograph_status.setText(
                        f"Start Position: {beat_data.letter}"
                    )
                else:
                    self._pictograph_status.setText(
                        f"Beat {beat_index + 1}: {beat_data.letter}"
                    )

            # Reset turn controls to defaults (like legacy)
            self._blue_turn_amount = 0
            self._red_turn_amount = 0
            if self._blue_amount_label:
                self._blue_amount_label.setText("0")
            if self._red_amount_label:
                self._red_amount_label.setText("0")

            # Reset rotation buttons
            if self._blue_cw_btn:
                self._blue_cw_btn.setChecked(False)
            if self._blue_ccw_btn:
                self._blue_ccw_btn.setChecked(False)
            if self._red_cw_btn:
                self._red_cw_btn.setChecked(False)
            if self._red_ccw_btn:
                self._red_ccw_btn.setChecked(False)

            # Update beat display component (like legacy graph editor)
            if self._beat_display:
                self._beat_display.set_beat_data(beat_data)
                if beat_index == -1:
                    self._beat_display.setToolTip(f"Start Position: {beat_data.letter}")
                    self._beat_display.set_start_text_visible(
                        True
                    )  # Show START text for start position
                    self._beat_display.set_beat_number_visible(
                        False
                    )  # Hide beat number for start position
                else:
                    self._beat_display.setToolTip(
                        f"Beat {beat_index + 1}: {beat_data.letter}"
                    )
                    self._beat_display.set_start_text_visible(
                        False
                    )  # Hide START text for regular beats
                    self._beat_display.set_beat_number_visible(
                        True
                    )  # Show beat number for regular beats

                # Make sure beat display is visible and updated
                self._beat_display.show()
                self._beat_display.update()
                print(
                    f"✅ Beat display updated: {beat_data.letter} (index {beat_index})"
                )

            # TODO: Load and display pictograph for this beat
            # This would integrate with TKA's pictograph system
            if self._pictograph_display:
                self._pictograph_display.set_placeholder_text(
                    f"Beat {beat_index}: {beat_data.letter}"
                )

        else:
            if self._pictograph_status:
                self._pictograph_status.setText("No beat selected")
            if self._pictograph_display:
                self._pictograph_display.set_placeholder_text("No beat selected")

        logger.info(
            f"Beat selected: {beat_index} - {beat_data.letter if beat_data else 'None'}"
        )

    def set_selected_start_position(self, start_position_data) -> None:
        """Set the selected start position data (switches to orientation panels like legacy)"""
        # Switch to orientation adjustment panels (like legacy ORI_WIDGET_INDEX)
        if self._adjustment_stack:
            self._adjustment_stack.setCurrentIndex(0)

        if start_position_data:
            if self._pictograph_status:
                self._pictograph_status.setText("Start position selected")
            if self._pictograph_display:
                self._pictograph_display.set_placeholder_text("Start Position")

            # Reset orientation controls to defaults (like legacy)
            self._blue_orientation = "IN"
            self._red_orientation = "IN"
            if self._blue_orientation_label:
                self._blue_orientation_label.setText("IN")
            if self._red_orientation_label:
                self._red_orientation_label.setText("IN")

        logger.info(f"Start position set: {start_position_data}")

    def toggle_visibility(self) -> None:
        """Toggle graph editor visibility"""
        if self.isVisible():
            self.hide()
        else:
            self.show()
        self.visibility_changed.emit(self.isVisible())

    def get_preferred_height(self) -> int:
        """Get the preferred height for the graph editor"""
        return 300

    def update_workbench_size(self, width: int, height: int) -> None:
        """Update workbench size reference when workbench resizes"""
        pass  # Not needed for embedded mode

    def sync_width_with_workbench(self) -> None:
        """Synchronize graph editor width with parent workbench width"""
        pass  # Not needed for embedded mode
