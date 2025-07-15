"""
Enhanced Start Position Option with modern glassmorphism design and smooth animations.

This component represents a single start position choice with contemporary styling,
hover effects, and improved user interaction feedback.
"""

import logging

from application.services.pictograph_pool_manager import PictographPoolManager
from core.interfaces.start_position_services import IStartPositionDataService
from presentation.components.sequence_workbench.sequence_beat_frame.selection_overlay import (
    SelectionOverlay,
)
from PyQt6.QtCore import (
    QEasingCurve,
    QPoint,
    QPropertyAnimation,
    QRectF,
    Qt,
    pyqtSignal,
)
from PyQt6.QtGui import (
    QColor,
    QFont,
    QLinearGradient,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPen,
)
from PyQt6.QtWidgets import QGraphicsDropShadowEffect, QLabel, QVBoxLayout, QWidget

logger = logging.getLogger(__name__)


class StartPositionOption(QWidget):
    """
    Start position option with modern glassmorphism design.

    Features:
    - Modern glassmorphism styling with transparency and blur effects
    - Smooth hover and selection animations
    - Visual feedback for user interactions
    - Responsive sizing and improved accessibility
    - Enhanced visual hierarchy with position labels
    """

    position_selected = pyqtSignal(str)

    def __init__(
        self,
        position_key: str,
        pool_manager: PictographPoolManager,
        data_service: IStartPositionDataService,
        grid_mode: str = "diamond",
        enhanced_styling: bool = True,
        parent=None,
    ):
        super().__init__(parent)
        self.position_key = position_key
        self.grid_mode = grid_mode
        self.enhanced_styling = enhanced_styling
        self.data_service = data_service
        self._pool_manager = pool_manager

        # State management
        self._is_hovered = False
        self._is_selected = False
        self._is_pressed = False

        # Animation properties
        self.hover_animation: QPropertyAnimation = None
        self.click_animation: QPropertyAnimation = None
        self.selection_animation: QPropertyAnimation = None

        # Components
        self._pictograph_component = None
        self._selection_overlay = None
        self.position_label = None

        self._setup_ui()
        self._setup_animations()

    def _setup_ui(self):
        """Set up the enhanced UI with modern styling."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Apply enhanced styling
        if self.enhanced_styling:
            self.setStyleSheet(self._get_enhanced_styles())
            self.setObjectName("EnhancedPositionOption")
        else:
            self.setStyleSheet(self._get_basic_styles())

        # Get pictograph component from pool
        self._pictograph_component = self._pool_manager.checkout_pictograph(parent=self)
        self.pictograph_component = self._pictograph_component  # Keep legacy reference

        if self._pictograph_component:
            # Start with default size - will be updated by parent when sizing is applied
            initial_size = 200 if self.enhanced_styling else 180
            self._pictograph_component.setFixedSize(initial_size, initial_size)

            # Load pictograph data
            pictograph_data = self.data_service.get_position_data(
                self.position_key, self.grid_mode
            )
            if pictograph_data:
                self._pictograph_component.update_from_pictograph_data(pictograph_data)

            layout.addWidget(self._pictograph_component)
        else:
            logger.warning(
                f"Failed to get pictograph component from pool for start position: {self.position_key}"
            )

        # Add position label for enhanced version
        if self.enhanced_styling:
            self.position_label = self._create_position_label()
            layout.addWidget(self.position_label)

        # Selection overlay
        self._selection_overlay = SelectionOverlay(self)

        # Don't set fixed size here - let parent control sizing dynamically
        # Size will be set by the unified picker's _apply_option_sizing method

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Add drop shadow for enhanced version
        if self.enhanced_styling:
            self._add_drop_shadow()

    def _get_enhanced_styles(self) -> str:
        """Return enhanced glassmorphism stylesheet."""
        return """
            QWidget#EnhancedPositionOption {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.25),
                    stop:0.5 rgba(255, 255, 255, 0.18),
                    stop:1 rgba(255, 255, 255, 0.15)
                );
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 20px;
            }
            
            QWidget#EnhancedPositionOption:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.35),
                    stop:0.5 rgba(255, 255, 255, 0.28),
                    stop:1 rgba(255, 255, 255, 0.25)
                );
                border: 2px solid rgba(255, 255, 255, 0.45);
            }
            
            QLabel#PositionLabel {
                background: rgba(255, 255, 255, 0.2);
                border: 1px solid rgba(255, 255, 255, 0.3);
                border-radius: 8px;
                color: #2d3748;
                font-weight: 600;
                padding: 6px 12px;
                margin: 2px;
            }
        """

    def _get_basic_styles(self) -> str:
        """Return basic styling for backward compatibility."""
        return """
            QWidget {
                border: 2px solid rgba(255,255,255,0.25);
                border-radius: 18px;
                background: rgba(255,255,255,0.18);
            }
        """

    def _create_position_label(self) -> QLabel:
        """Create position label with formatted text."""
        # Extract readable position information
        start_pos, end_pos = self.position_key.split("_")
        letter = self._extract_letter_from_position(start_pos)

        # Format label text
        position_text = f"{letter} - {start_pos.replace(letter.lower(), '').replace('alpha', '').replace('beta', '').replace('gamma', '')}"

        label = QLabel(position_text)
        label.setObjectName("PositionLabel")
        label.setFont(QFont("Segoe UI", 10, QFont.Weight.Medium))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        return label

    def _extract_letter_from_position(self, position: str) -> str:
        """Extract Greek letter from position string."""
        if position.startswith("alpha"):
            return "α"
        elif position.startswith("beta"):
            return "β"
        elif position.startswith("gamma"):
            return "Γ"
        return "?"

    def _add_drop_shadow(self):
        """Add subtle drop shadow effect for enhanced depth."""
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 6)
        self.setGraphicsEffect(shadow)

    def _setup_animations(self):
        """Set up smooth animations for interactions."""
        if not self.enhanced_styling:
            return

        # Hover animation
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(200)
        self.hover_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Click animation
        self.click_animation = QPropertyAnimation(self, b"geometry")
        self.click_animation.setDuration(100)
        self.click_animation.setEasingCurve(QEasingCurve.Type.OutQuad)

    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press with enhanced feedback."""
        if event.button() == Qt.MouseButton.LeftButton:
            self._is_pressed = True

            # Trigger click animation for enhanced version
            if self.enhanced_styling and self.click_animation:
                self._animate_click()

            self.position_selected.emit(self.position_key)

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release."""
        self._is_pressed = False
        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        """Handle mouse enter with enhanced hover effects."""
        self._is_hovered = True
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Enhanced hover animation
        if self.enhanced_styling and self.hover_animation and not self._is_pressed:
            self._animate_hover(True)

        # Standard selection overlay
        self.set_highlighted(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave with smooth transition."""
        self._is_hovered = False
        self.setCursor(Qt.CursorShape.ArrowCursor)

        # Enhanced hover animation out
        if self.enhanced_styling and self.hover_animation and not self._is_pressed:
            self._animate_hover(False)

        # Standard selection overlay
        self.set_highlighted(False)
        super().leaveEvent(event)

    def _animate_hover(self, hover_in: bool):
        """Animate hover state with subtle scaling."""
        if not self.hover_animation:
            return

        current_rect = self.geometry()

        if hover_in:
            # Scale up slightly
            target_rect = current_rect.adjusted(-3, -3, 3, 3)
        else:
            # Scale back to normal
            target_rect = current_rect.adjusted(3, 3, -3, -3)

        self.hover_animation.setStartValue(current_rect)
        self.hover_animation.setEndValue(target_rect)
        self.hover_animation.start()

    def _animate_click(self):
        """Animate click feedback with quick scale."""
        if not self.click_animation:
            return

        current_rect = self.geometry()
        click_rect = current_rect.adjusted(2, 2, -2, -2)  # Scale down

        # Animate scale down
        self.click_animation.setStartValue(current_rect)
        self.click_animation.setEndValue(click_rect)
        self.click_animation.finished.connect(self._restore_click_size)
        self.click_animation.start()

    def _restore_click_size(self):
        """Restore size after click animation."""
        if not self.click_animation:
            return

        self.click_animation.finished.disconnect()
        current_rect = self.geometry()
        normal_rect = current_rect.adjusted(-2, -2, 2, 2)  # Scale back up

        self.click_animation.setStartValue(current_rect)
        self.click_animation.setEndValue(normal_rect)
        self.click_animation.start()

    def set_highlighted(self, highlighted: bool) -> None:
        """Set hover state with selection overlay."""
        if self._selection_overlay:
            if highlighted:
                self._selection_overlay.show_hover()
            else:
                self._selection_overlay.hide_hover_only()

    def set_selected(self, selected: bool) -> None:
        """Set selection state with visual feedback."""
        self._is_selected = selected

        if self._selection_overlay:
            if selected:
                self._selection_overlay.show_selection()
            else:
                self._selection_overlay.hide_all()

    def paintEvent(self, event):
        """Custom paint event for additional visual effects."""
        super().paintEvent(event)

        if not self.enhanced_styling:
            return

        # Add subtle highlight gradient for enhanced version
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create highlight gradient
        if self._is_hovered:
            highlight_gradient = QLinearGradient(0, 0, 0, self.height() * 0.4)
            highlight_gradient.setColorAt(0, QColor(255, 255, 255, 40))
            highlight_gradient.setColorAt(1, QColor(255, 255, 255, 0))

            # Create rounded rectangle path
            path = QPainterPath()
            rect_f = QRectF(self.rect().adjusted(2, 2, -2, -2))
            path.addRoundedRect(rect_f, 18, 18)

            # Draw highlight
            painter.fillPath(path, highlight_gradient)

        # Add selection indicator if selected
        if self._is_selected:
            painter.setPen(QPen(QColor(99, 102, 241), 3))
            rect_f = QRectF(self.rect().adjusted(1, 1, -1, -1))
            painter.drawRoundedRect(rect_f, 20, 20)

        painter.end()

    def update_pictograph_size(self, container_size: int):
        """Update the pictograph size to match the container."""
        if self._pictograph_component:
            # Calculate pictograph size (slightly smaller than container to account for margins)
            pictograph_size = max(
                container_size - 40, 80
            )  # Leave 40px for margins/padding
            self._pictograph_component.setFixedSize(pictograph_size, pictograph_size)
            logger.debug(
                f"Updated pictograph size to {pictograph_size}px for position {self.position_key}"
            )

    def closeEvent(self, event):
        """Clean up pool resources when widget is closed."""
        self._cleanup_pool_resources()
        super().closeEvent(event)

    def _cleanup_pool_resources(self):
        """Return pictograph component to pool for reuse."""
        if self._pictograph_component and self._pool_manager:
            try:
                self._pool_manager.checkin_pictograph(self._pictograph_component)
                self._pictograph_component = None
            except Exception as e:
                logger.warning(
                    f"Failed to return start position component to pool: {e}"
                )

    def __del__(self):
        """Ensure cleanup on deletion."""
        self._cleanup_pool_resources()
