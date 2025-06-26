from typing import Optional, TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton, QLabel, QHBoxLayout
from PyQt6.QtGui import QFont, QMouseEvent
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from .letter_types import LetterType

if TYPE_CHECKING:
    from .option_picker_section import OptionPickerSection


class LetterTypeTextPainter:
    """Color scheme for letter type text"""

    COLORS = {
        "Shift": "#6F2DA8",
        "Dual": "#00b3ff",
        "Dash": "#26e600",
        "Cross": "#26e600",
        "Static": "#eb7d00",
        "-": "#000000",
    }

    @classmethod
    def get_colored_text(cls, text: str) -> str:
        """Generate colored HTML text"""
        type_words = text.split("-")
        styled_words = [
            f"<span style='color: {cls.COLORS.get(word, 'black')};'>{word}</span>"
            for word in type_words
        ]
        if "-" in text:
            return "-".join(styled_words)
        return "".join(styled_words)


class OptionPickerSectionButton(QPushButton):
    """
    Section button with embedded QLabel for HTML rendering.
    Features oval shape, transparent background, and dynamic sizing.
    """

    clicked = pyqtSignal()

    def __init__(self, section_widget: "OptionPickerSection"):
        super().__init__(section_widget)
        self.section_widget = section_widget
        self.is_expanded = True  # Sections start expanded
        self._base_background_color = (
            "rgba(255, 255, 255, 200)"  # Base background
        )
        self._resizing = False  # Prevent resize loops
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Create embedded label for HTML text
        self.label = QLabel(self)
        self.label.setTextFormat(Qt.TextFormat.RichText)
        self.label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        # Layout: no margins, center alignment
        self._layout = QHBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self._layout)

        # Generate HTML text
        self._paint_text(section_widget.letter_type)

        # Apply initial styling
        self._set_initial_styles()

    def _paint_text(self, letter_type: str) -> None:
        """Generate and set HTML text"""
        html_text = self._generate_html_text(letter_type)
        self.label.setText(html_text)

    def _generate_html_text(self, letter_type: str) -> str:
        """Generate HTML text format"""
        # Map letter types to text format
        type_texts = {
            "Type1": "Type 1 - Dual Shift",
            "Type2": "Type 2 - Shift",
            "Type3": "Type 3 - Cross Shift",
            "Type4": "Type 4 - Dash",
            "Type5": "Type 5 - Dual Dash",
            "Type6": "Type 6 - Static",
        }

        # Get text format
        display_text = type_texts.get(letter_type, letter_type)

        # Apply color scheme to the words
        words = display_text.split()
        styled_words = []

        for word in words:
            if word in ["Dual", "Shift", "Cross", "Dash", "Static"]:
                color = self._get_word_color(word)
                styled_words.append(f"<span style='color: {color};'>{word}</span>")
            elif word in ["Type", "1", "2", "3", "4", "5", "6", "-"]:
                styled_words.append(f"<span style='color: #000000;'>{word}</span>")
            else:
                styled_words.append(word)

        return " ".join(styled_words)

    def _get_word_color(self, word: str) -> str:
        """Get color for each word type"""
        colors = {
            "Dual": "#00b3ff",  # Blue for Dual
            "Shift": "#6F2DA8",  # Purple for Shift
            "Cross": "#26e600",  # Green for Cross
            "Dash": "#26e600",  # Green for Dash
            "Static": "#eb7d00",  # Orange for Static
        }
        return colors.get(word, "#000000")

    def _set_initial_styles(self) -> None:
        """Apply initial styling"""
        # Bold font
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)

        # Apply initial style
        self._update_style()

    def _update_style(self, background_color: Optional[str] = None) -> None:
        """
        Button styling: oval shape, transparent background, no borders.
        """
        background_color = background_color or "rgba(255, 255, 255, 0.3)"

        # Force a substantial border radius for visible rounding
        border_radius = 18

        style = (
            f"QPushButton {{"
            f"  background: {background_color};"
            f"  border: 1px solid rgba(255, 255, 255, 0.4);"
            f"  border-radius: {border_radius}px;"
            f"  font-weight: bold;"
            f"}}"
            f"QPushButton:hover {{"
            f"  background: rgba(255, 255, 255, 0.45);"
            f"  border: 2px solid rgba(255, 255, 255, 0.6);"
            f"  border-radius: {border_radius}px;"
            f"}}"
            f"QPushButton:pressed {{"
            f"  background: rgba(255, 255, 255, 0.55);"
            f"  border: 1px solid rgba(255, 255, 255, 0.7);"
            f"  border-radius: {border_radius}px;"
            f"}}"
        )
        self.setStyleSheet(style)

    # ---------- HOVER / PRESS / RELEASE STATES ----------

    def enterEvent(self, event) -> None:
        """Hover effect with gradient"""
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        gradient = (
            "qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, "
            "stop:0 rgba(200, 200, 200, 1), stop:1 rgba(150, 150, 150, 1))"
        )
        self._update_style(background_color=gradient)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        """Leave effect"""
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self._update_style()
        super().leaveEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Press effect"""
        if event.button() == Qt.MouseButton.LeftButton:
            self._update_style(background_color="#aaaaaa")
            self.clicked.emit()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        """Release effect"""
        self._update_style()
        super().mouseReleaseEvent(event)

    # ---------- RESIZE LOGIC ----------

    def resizeEvent(self, event) -> None:
        """
        Legacy-exact dynamic sizing: font_size * 3 for height.
        """
        if not self._resizing:  # Prevent infinite resize loops
            super().resizeEvent(event)
        
    def resize_to_fit(self):
        """Resize button using legacy calculation."""
        if self._resizing:  # Prevent recursive calls
            return
            
        self._resizing = True
        try:
            # Legacy sizing calculation
            if self.section_widget.mw_size_provider and callable(
                self.section_widget.mw_size_provider
            ):
                parent_height = self.section_widget.mw_size_provider().height()
            else:
                parent_height = 800

            font_size = max(parent_height // 70, 10)
            label_height = max(int(font_size * 3), 20)  # Legacy: font_size * 3
            label_width = max(int(label_height * 6), 100)  # Legacy: height * 6
            
            # Only resize if size actually changed
            current_size = self.size()
            if current_size.width() != label_width or current_size.height() != label_height:
                print(f"🏷️ [HEADER DEBUG] Button resize for {self.section_widget.letter_type}:")
                print(f"   Legacy calculation: font_size({font_size}) * 3 = {label_height}px height")
                print(f"   Button size: {label_width} × {label_height}px")

                # Apply font sizing
                font = self.label.font()
                font.setPointSize(font_size)
                self.label.setFont(font)

                # Button sizing using legacy calculation
                self.setFixedSize(QSize(label_width, label_height))

                # Reapply style for correct border radius
                self._update_style()
        finally:
            self._resizing = False

    def toggle_expansion(self) -> None:
        """Toggle section expansion state and update text"""
        self.is_expanded = not self.is_expanded
        self._paint_text(self.section_widget.letter_type)
