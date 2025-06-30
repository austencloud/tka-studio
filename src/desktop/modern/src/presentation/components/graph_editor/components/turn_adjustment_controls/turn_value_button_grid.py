from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton
from typing import Callable

from presentation.components.graph_editor.components.turn_adjustment_controls.styling_helpers import apply_turn_button_styling


class TurnValueButtonGrid(QWidget):
    def __init__(
        self,
        color: str,
        turn_values,
        turn_value_map,
        on_value_selected: Callable[[str], None],
        parent=None,
    ):
        super().__init__(parent)
        self.buttons = {}
        self.turn_values = turn_values
        self.color = color
        self.on_value_selected = on_value_selected
        grid_layout = QGridLayout(self)
        grid_layout.setContentsMargins(0, 0, 0, 0)
        grid_layout.setSpacing(6)
        for i, turn_value in enumerate(turn_values):
            row = i // 4
            col = i % 4
            button = QPushButton(turn_value)
            button.setCheckable(True)
            button.setFixedSize(50, 40)
            button.clicked.connect(
                lambda checked, val=turn_value: self._handle_click(val)
            )
            apply_turn_button_styling(button, color, turn_value)
            grid_layout.addWidget(button, row, col)
            self.buttons[turn_value] = button

    def _handle_click(self, value: str):
        self.set_selected(value)
        if self.on_value_selected:
            self.on_value_selected(value)

    def set_selected(self, value: str):
        for v, btn in self.buttons.items():
            btn.setChecked(v == value)

    def get_selected(self) -> str:
        for v, btn in self.buttons.items():
            if btn.isChecked():
                return v
        return "0"
