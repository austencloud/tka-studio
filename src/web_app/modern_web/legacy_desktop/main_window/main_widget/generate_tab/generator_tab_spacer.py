from __future__ import annotations
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QSizePolicy,
    QSpacerItem,
)


class GeneratorTabSpacer(QSpacerItem):
    resized: pyqtSignal = pyqtSignal()

    def __init__(self, width: int, height: int):
        super().__init__(width, height, QSizePolicy.Policy.Minimum)
        self._height = height

    def resizeEvent(self, event):
        self.changeSize(0, self._height)
        self.resized.emit()
