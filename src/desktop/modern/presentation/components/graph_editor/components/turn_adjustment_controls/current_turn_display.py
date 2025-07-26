from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt


class CurrentTurnDisplay(QWidget):
    def __init__(self, color: str, initial_value: str = "0", parent=None):
        super().__init__(parent)
        self.label = QLabel(f"{color.upper()}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet(
            f"""
            QLabel {{
                font-size: 14px;
                font-weight: bold;
                color: {'#4A90E2' if color == 'blue' else '#E74C3C'};
                padding: 2px;
            }}
            """
        )
        self.value_label = QLabel(initial_value)
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value_label.setStyleSheet(
            """
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: rgba(255, 255, 255, 0.9);
                background: rgba(255, 255, 255, 0.1);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 8px;
                min-height: 20px;
            }
            """
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addWidget(self.label)
        layout.addWidget(self.value_label)

    def set_value(self, value: str):
        self.value_label.setText(value)

    def get_value(self) -> str:
        return self.value_label.text()
