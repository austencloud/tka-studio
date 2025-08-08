"""
Accordion Header Component

Clickable header for accordion sections with expand/collapse indicator.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QWidget

from desktop.modern.presentation.styles.mixins import StyleMixin


class AccordionHeader(QFrame, StyleMixin):
    """Clickable header for accordion sections with expand/collapse indicator."""

    # Signal emitted when header is clicked
    clicked = pyqtSignal()

    def __init__(
        self,
        title: str,
        is_expanded: bool = False,
        parent: QWidget | None = None,
    ):
        super().__init__(parent)
        self.title = title
        self.is_expanded = is_expanded
        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self) -> None:
        """Setup the header layout."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        # Title label
        self.title_label = QLabel(self.title)
        self.title_label.setFont(self._get_title_font())
        layout.addWidget(self.title_label)

        # Spacer
        layout.addStretch()

        # Expand/collapse indicator
        self.indicator_label = QLabel()
        self.indicator_label.setFont(self._get_indicator_font())
        self._update_indicator()
        layout.addWidget(self.indicator_label)

    def _get_title_font(self) -> QFont:
        """Get font for the title."""
        font = QFont()
        font.setPointSize(11)
        font.setWeight(QFont.Weight.Medium)
        return font

    def _get_indicator_font(self) -> QFont:
        """Get font for the expand/collapse indicator."""
        font = QFont()
        font.setPointSize(12)
        font.setWeight(QFont.Weight.Bold)
        return font

    def _update_indicator(self) -> None:
        """Update the expand/collapse indicator with smooth transition."""
        if self.is_expanded:
            self.indicator_label.setText("▼")  # Down arrow
        else:
            self.indicator_label.setText("▶")  # Right arrow

        # Add a subtle scale animation for visual feedback
        from PyQt6.QtCore import QEasingCurve, QPropertyAnimation
        from PyQt6.QtWidgets import QGraphicsOpacityEffect

        if not hasattr(self, "_indicator_animation"):
            self._indicator_effect = QGraphicsOpacityEffect()
            self.indicator_label.setGraphicsEffect(self._indicator_effect)

            self._indicator_animation = QPropertyAnimation(
                self._indicator_effect, b"opacity"
            )
            self._indicator_animation.setDuration(150)
            self._indicator_animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        # Quick fade out and in for smooth transition
        self._indicator_animation.setStartValue(1.0)
        self._indicator_animation.setEndValue(0.7)
        self._indicator_animation.finished.connect(
            lambda: self._indicator_animation.setEndValue(1.0)
        )
        self._indicator_animation.start()

    def _apply_styling(self) -> None:
        """Apply glassmorphism styling to the header using standard patterns."""
        self.setStyleSheet(
            """
            AccordionHeader {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                margin: 4px;
                padding: 0px;
            }
            AccordionHeader:hover {
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
            AccordionHeader QLabel {
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
                border: none;
                padding: 0px;
                margin: 0px;
            }
        """
        )

    def set_expanded(self, expanded: bool) -> None:
        """Set the expanded state and update the indicator."""
        self.is_expanded = expanded
        self._update_indicator()

    def mousePressEvent(self, event) -> None:
        """Handle mouse press to emit clicked signal."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

    def enterEvent(self, event) -> None:
        """Handle mouse enter for hover effect."""
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        """Handle mouse leave to reset cursor."""
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event)
