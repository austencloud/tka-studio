from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

from PyQt6.QtCore import QObject, Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy

from ..components.adjustment_panel import AdjustmentPanel
from ..components.pictograph_container import GraphEditorPictographContainer
from ..config import LayoutConfig


logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ..graph_editor import GraphEditor


class GraphEditorLayoutManager(QObject):
    """
    Manages UI layout, styling, and component positioning for the graph editor.

    Responsibilities:
    - UI setup and initialization
    - Component creation and positioning
    - Styling and visual appearance
    - Resize event handling
    - Layout management
    """

    def __init__(self, graph_editor: GraphEditor, parent: Optional[QObject] = None):
        super().__init__(parent)
        self._graph_editor = graph_editor

        # UI components (will be created during setup)
        self._pictograph_container: Optional[GraphEditorPictographContainer] = None
        self._left_adjustment_panel: Optional[AdjustmentPanel] = None
        self._right_adjustment_panel: Optional[AdjustmentPanel] = None

        # Layout
        self._main_layout: Optional[QHBoxLayout] = None

    def setup_ui(self) -> None:
        """Setup enhanced UI combining best practices from legacy, modern, and web versions"""
        self._setup_frame_properties()
        self._apply_styling()
        self._create_layout()
        self._create_components()
        self._arrange_components()
        self._configure_size_policies()

    def _setup_frame_properties(self) -> None:
        """Setup basic frame properties"""
        self._graph_editor.setFrameStyle(QFrame.Shape.NoFrame)
        self._graph_editor.setFixedHeight(0)  # Start collapsed

        # Enable focus for hotkey handling
        self._graph_editor.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def _apply_styling(self) -> None:
        """Apply enhanced styling combining modern frosted glass with web color principles"""
        self._graph_editor.setStyleSheet(
            """
            GraphEditor {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 rgba(255, 255, 255, 0.25),
                    stop: 0.5 rgba(255, 255, 255, 0.15),
                    stop: 1 rgba(255, 255, 255, 0.10)
                );
                border-bottom: none;
                border-radius: 16px 16px 0px 0px;
            }
        """
        )

    def _create_layout(self) -> None:
        """Create the main horizontal layout"""
        self._main_layout = QHBoxLayout(self._graph_editor)
        self._main_layout.setContentsMargins(
            LayoutConfig.MAIN_LAYOUT_MARGINS,
            LayoutConfig.MAIN_LAYOUT_MARGINS,
            LayoutConfig.MAIN_LAYOUT_MARGINS,
            LayoutConfig.MAIN_LAYOUT_MARGINS,
        )
        self._main_layout.setSpacing(LayoutConfig.MAIN_LAYOUT_SPACING)

    def _create_components(self) -> None:
        """Create all UI components"""
        self._left_adjustment_panel = AdjustmentPanel(
            self._graph_editor, side="left", color="blue"
        )

        self._pictograph_container = GraphEditorPictographContainer(self._graph_editor)

        self._right_adjustment_panel = AdjustmentPanel(
            self._graph_editor, side="right", color="red"
        )

        self._graph_editor._adjustment_panel = (
            self._right_adjustment_panel
        )  # Legacy compatibility

    def _arrange_components(self) -> None:
        """Arrange components in the layout"""
        # Web-inspired layout: flex panels on sides, fixed pictograph in center
        self._main_layout.addWidget(
            self._left_adjustment_panel, 1
        )  # flex: 1 equivalent
        self._main_layout.addWidget(self._pictograph_container, 0)  # fixed size
        self._main_layout.addWidget(
            self._right_adjustment_panel, 1
        )  # flex: 1 equivalent

    def _configure_size_policies(self) -> None:
        """Configure size policies for components"""
        self._graph_editor.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

    def update_component_display(self, beat_data=None, sequence_data=None) -> None:
        """
        Update all components with new data.

        Args:
            beat_data: Beat data to update components with
            sequence_data: Sequence data to update components with
        """
        if beat_data:
            if self._pictograph_container:
                self._pictograph_container.set_beat(beat_data)

            if self._left_adjustment_panel:
                self._left_adjustment_panel.set_beat(beat_data)

            if self._right_adjustment_panel:
                self._right_adjustment_panel.set_beat(beat_data)

    def sync_graph_editor_width(self) -> None:
        """Trigger graph editor width synchronization with workbench"""
        logger.debug("Layout manager sync_graph_editor_width called")
        if hasattr(self._graph_editor, "sync_width_with_workbench"):
            self._graph_editor.sync_width_with_workbench()
        else:
            logger.error("Graph editor missing sync_width_with_workbench method!")

    # Property accessors for components
    @property
    def pictograph_container(self) -> Optional[GraphEditorPictographContainer]:
        """Get the pictograph container"""
        return self._pictograph_container

    @property
    def left_adjustment_panel(self) -> Optional[AdjustmentPanel]:
        """Get the left adjustment panel"""
        return self._left_adjustment_panel

    @property
    def right_adjustment_panel(self) -> Optional[AdjustmentPanel]:
        """Get the right adjustment panel"""
        return self._right_adjustment_panel
