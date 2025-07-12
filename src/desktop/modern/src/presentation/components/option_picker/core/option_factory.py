"""
Simplified Option Factory - Direct Copy of Legacy Success Pattern

This factory directly copies the successful Legacy OptionFactory pattern,
replacing the complex Modern OptionPoolManager with simple object creation.

Key principles from Legacy:
- Simple factory that creates 36 pictograph objects
- No complex orchestration or event processing workarounds
- Direct object creation without business logic interference
- Simple list-based pool management
"""

from typing import Callable, List

from domain.models.pictograph_data import PictographData
from presentation.components.option_picker.core.pictograph_option_frame import (
    PictographOptionFrame,
)
from PyQt6.QtCore import QSize


class OptionFactory:
    """
    Simplified option factory using Legacy success pattern.

    Direct copy of Legacy OptionFactory with minimal changes for Modern compatibility.
    """

    MAX_PICTOGRAPHS = 36

    def __init__(
        self, parent_widget=None, mw_size_provider: Callable[[], QSize] = None
    ) -> None:
        self.parent_widget = parent_widget
        self.mw_size_provider = mw_size_provider or self._default_size_provider
        # Build the option pool upon instantiation like Legacy
        self.option_pool = self.create_options()

    def _default_size_provider(self) -> QSize:
        """Default size provider if none provided."""
        return QSize(800, 600)

    def create_options(self) -> List[PictographOptionFrame]:
        """Create options exactly like Legacy pattern."""
        options: List[PictographOptionFrame] = []
        for i in range(self.MAX_PICTOGRAPHS):
            # Create the real pictograph frame
            frame = PictographOptionFrame(parent=self.parent_widget)
            options.append(frame)
        return options

    def get_available_frame(self) -> PictographOptionFrame:
        """Get an available frame from the pool."""
        for frame in self.option_pool:
            if not frame.isVisible():
                return frame
        # If no available frame, return the first one (reuse)
        return self.option_pool[0] if self.option_pool else None

    def reset_all_frames(self):
        """Reset all frames to hidden state."""
        for frame in self.option_pool:
            frame.hide()
            frame.setVisible(False)
