from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QResizeEvent
from typing import Callable, List


class ModernOptionPickerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._resize_callback = None
        self._sizing_callbacks: List[Callable[[int], None]] = []

    def set_resize_callback(self, callback):
        self._resize_callback = callback

    def add_sizing_callback(self, callback: Callable[[int], None]):
        """Add a callback that receives the option picker width when it changes"""
        self._sizing_callbacks.append(callback)

    def remove_sizing_callback(self, callback: Callable[[int], None]):
        """Remove a sizing callback"""
        if callback in self._sizing_callbacks:
            self._sizing_callbacks.remove(callback)

    def get_usable_width(self) -> int:
        """Get the usable width for pictograph sizing (excluding margins/padding)"""
        # Account for any margins/padding in the option picker
        return max(0, self.width() - 10)  # 10px for margins

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)

        # Call the original resize callback
        if self._resize_callback:
            self._resize_callback()

        # Notify all sizing callbacks with the new usable width
        usable_width = self.get_usable_width()
        for callback in self._sizing_callbacks:
            try:
                callback(usable_width)
            except Exception as e:
                print(f"❌ Error in sizing callback: {e}")
