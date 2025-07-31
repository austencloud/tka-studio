"""
Modern combo box component with glassmorphism styling.
"""

from typing import Any, Optional

from PyQt6.QtCore import QModelIndex, QPointF, Qt
from PyQt6.QtGui import QBrush, QColor, QLinearGradient, QPainter
from PyQt6.QtWidgets import QComboBox, QStyle, QStyledItemDelegate, QStyleOptionViewItem


class ComboBoxDelegate(QStyledItemDelegate):
    """Custom delegate for combo box items."""

    def paint(
        self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex
    ):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background
        if option.state & QStyle.StateFlag.State_Selected:
            gradient = QLinearGradient(
                QPointF(option.rect.topLeft()), QPointF(option.rect.bottomLeft())
            )
            gradient.setColorAt(0, QColor(42, 130, 218, 100))
            gradient.setColorAt(1, QColor(42, 130, 218, 80))
            painter.fillRect(option.rect, QBrush(gradient))
        elif option.state & QStyle.StateFlag.State_MouseOver:
            painter.fillRect(option.rect, QBrush(QColor(255, 255, 255, 30)))

        # Text
        painter.setPen(QColor(255, 255, 255, 220))
        painter.drawText(
            option.rect.adjusted(12, 0, -12, 0),
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            index.data(),
        )


class ComboBox(QComboBox):
    """Modern combo box with glassmorphism styling."""

    def __init__(self, items: Optional[list[str]] = None, parent=None):
        super().__init__(parent)

        if items:
            self.addItems(items)

        # Set custom delegate
        self.setItemDelegate(ComboBoxDelegate())

        self._apply_styling()

    def _apply_styling(self):
        """Apply glassmorphism styling."""
        self.setStyleSheet(
            """
            QComboBox {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 8px 12px;
                color: rgba(255, 255, 255, 0.9);
                font-size: 13px;
                font-weight: 500;
                min-height: 20px;
            }

            QComboBox:hover {
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(255, 255, 255, 0.3);
            }

            QComboBox:focus {
                background: rgba(255, 255, 255, 0.15);
                border: 1px solid rgba(42, 130, 218, 0.6);
            }

            QComboBox::drop-down {
                border: none;
                width: 20px;
            }

            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 6px solid rgba(255, 255, 255, 0.7);
                margin-right: 8px;
            }

            QComboBox QAbstractItemView {
                background: rgba(40, 40, 50, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 4px;
                color: rgba(255, 255, 255, 0.9);
                selection-background-color: rgba(42, 130, 218, 0.3);
                outline: none;
            }

            QComboBox QAbstractItemView::item {
                padding: 8px 12px;
                border-radius: 4px;
                min-height: 20px;
            }

            QComboBox QAbstractItemView::item:hover {
                background: rgba(255, 255, 255, 0.1);
            }

            QComboBox QAbstractItemView::item:selected {
                background: rgba(42, 130, 218, 0.3);
            }
        """
        )

    def set_items(self, items: list[str]):
        """Set combo box items."""
        self.clear()
        self.addItems(items)

    def get_current_data(self) -> Any:
        """Get current item data."""
        return self.currentData()

    def set_current_by_data(self, data: Any):
        """Set current item by data."""
        index = self.findData(data)
        if index >= 0:
            self.setCurrentIndex(index)
