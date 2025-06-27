from typing import Optional
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGraphicsView
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QMouseEvent, QPainter

from domain.models.core_models import BeatData
from domain.models.pictograph_models import PictographData
from application.services.core.pictograph_management_service import (
    PictographManagementService,
)
from presentation.components.pictograph.pictograph_scene import (
    PictographScene,
)


class GraphEditorPictographContainer(QWidget):
    arrow_selected = pyqtSignal(str)
    beat_modified = pyqtSignal(BeatData)

    def __init__(self, parent):
        super().__init__(parent)
        self._graph_editor = parent
        self._current_beat: Optional[BeatData] = None
        self._selected_arrow_id: Optional[str] = None
        self._selected_arrow_items = {}  # Track selected arrow visual items
        self._selection_highlight_color = "#FFD700"  # Gold border color

        # Get layout service from parent's container
        container = getattr(parent, "container", None)
        if container:
            self._pictograph_service = PictographManagementService()
        else:
            self._pictograph_service = None

        self._current_pictograph: Optional[PictographData] = None

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        # Match legacy: no margins and no spacing like legacy container
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._pictograph_view = ModernPictographView(self)
        self._pictograph_view.arrow_clicked.connect(self._on_arrow_clicked)

        layout.addWidget(self._pictograph_view)

        # Set initial size - will be updated in resizeEvent to maintain square aspect ratio
        self.setFixedSize(300, 300)

        # Set size policy to Fixed to match legacy behavior
        from PyQt6.QtWidgets import QSizePolicy

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.setStyleSheet(
            """
            GraphEditorPictographContainer {
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                background-color: rgba(0, 0, 0, 0.1);
            }
        """
        )

    def set_beat(self, beat_data: Optional[BeatData]):
        self._current_beat = beat_data
        self._pictograph_view.set_beat(beat_data)

    def refresh_display(self, beat_data: BeatData):
        """Refresh pictograph display with new beat data"""
        self.set_beat(beat_data)

        # Maintain selection if we had one
        if self._selected_arrow_id:
            self._apply_arrow_selection_visual(self._selected_arrow_id)

    def set_selected_arrow(self, arrow_id: str):
        """Set selected arrow and update visual feedback"""
        # Clear previous selection
        self._clear_arrow_selection()

        # Set new selection
        self._selected_arrow_id = arrow_id
        self._apply_arrow_selection_visual(arrow_id)

        self.arrow_selected.emit(arrow_id)

    def _clear_arrow_selection(self):
        """Clear all arrow selection visual feedback"""
        if hasattr(self._pictograph_view, "_scene") and self._pictograph_view._scene:
            for item in self._pictograph_view._scene.items():
                if hasattr(item, "setSelected"):
                    item.setSelected(False)
                if hasattr(item, "clear_selection_highlight"):
                    item.clear_selection_highlight()

    def _apply_arrow_selection_visual(self, arrow_id: str):
        """Apply visual feedback for selected arrow"""
        if (
            not hasattr(self._pictograph_view, "_pictograph_scene")
            or not self._pictograph_view._pictograph_scene
        ):
            return

        for item in self._pictograph_view._pictograph_scene.items():
            if hasattr(item, "arrow_color") and item.arrow_color == arrow_id:
                # Add gold border highlighting
                if hasattr(item, "add_selection_highlight"):
                    item.add_selection_highlight(self._selection_highlight_color)
                elif hasattr(item, "setSelected"):
                    item.setSelected(True)
                break

    def _on_arrow_clicked(self, arrow_id: str):
        self._selected_arrow_id = arrow_id
        self.arrow_selected.emit(arrow_id)

    def resizeEvent(self, event):
        """Handle resize events to maintain perfect square aspect ratio like legacy"""
        super().resizeEvent(event)

        # Get the graph editor's height to maintain square proportions
        if self._graph_editor and hasattr(self._graph_editor, "height"):
            graph_editor_height = self._graph_editor.height()
            if graph_editor_height > 0:
                # Enforce square aspect ratio: width = height = graph_editor_height
                # This matches legacy: self.setFixedSize(self.graph_editor.height(), self.graph_editor.height())
                square_size = graph_editor_height
                self.setFixedSize(square_size, square_size)

                # The pictograph view should fill the container completely (no margins now)
                if self._pictograph_view:
                    # No margins now, so view fills entire container
                    self._pictograph_view.setFixedSize(square_size, square_size)


class ModernPictographView(QGraphicsView):
    arrow_clicked = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self._container = parent
        self._current_beat: Optional[BeatData] = None

        self._setup_view()

    def _setup_view(self):
        # Use Modern's PictographScene instead of basic QGraphicsScene
        self._pictograph_scene = PictographScene()
        self.setScene(self._pictograph_scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)

        # Remove all frames and borders like legacy
        from PyQt6.QtWidgets import QFrame

        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setLineWidth(0)
        self.setMidLineWidth(0)
        self.setStyleSheet("background: transparent; border: none;")

        # Remove all margins like legacy implementation
        self.setContentsMargins(0, 0, 0, 0)
        viewport = self.viewport()
        if viewport:
            viewport.setContentsMargins(0, 0, 0, 0)
        self.setViewportMargins(0, 0, 0, 0)

        # Set alignment like legacy
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Disable scroll bars like legacy
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Enable proper scaling and viewport updates
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setOptimizationFlags(
            QGraphicsView.OptimizationFlag.DontAdjustForAntialiasing
        )

    def set_beat(self, beat_data: Optional[BeatData]):
        self._current_beat = beat_data
        self._render_beat()

        # Ensure proper scaling after rendering
        self._fit_pictograph_to_view()

    def _render_beat(self):
        if not self._current_beat:
            self.scene().clear()
            return

        # Use Modern's native pictograph scene to render the beat
        self._pictograph_scene.update_beat(self._current_beat)

        # Enable arrow selection for graph editor mode
        self._enable_arrow_selection()

    def _fit_pictograph_to_view(self):
        """Fit the pictograph properly within the view container like legacy"""
        if not self._pictograph_scene:
            return

        # Use legacy-style scaling: scene().sceneRect() and viewport().size()
        scene_size = self._pictograph_scene.sceneRect().size()
        view_size = self.viewport().size()

        if scene_size.width() <= 0 or scene_size.height() <= 0:
            return

        # Calculate scale factor like legacy implementation
        scale_factor = min(
            view_size.width() / scene_size.width(),
            view_size.height() / scene_size.height(),
        )

        # Apply scaling like legacy: resetTransform() then scale()
        self.resetTransform()
        self.scale(scale_factor, scale_factor)

        # Ensure the scene is properly positioned to show all content
        # Instead of centerOn(), use setSceneRect to ensure full scene visibility
        self.setSceneRect(self._pictograph_scene.sceneRect())

        # Ensure the view shows the entire scene content
        self.ensureVisible(self._pictograph_scene.sceneRect(), 0, 0)

        # COMPREHENSIVE POSITION DEBUGGING
        self._debug_positioning_data(scene_size, view_size, scale_factor)

    def _debug_positioning_data(self, scene_size, view_size, scale_factor):
        """Data-driven debugging to identify exact positioning issues"""
        print("=" * 80)
        print("🔍 COMPREHENSIVE PICTOGRAPH POSITIONING DEBUG")
        print("=" * 80)

        # 1. Basic scaling information
        print(f"📐 Scene rect: {scene_size.width():.1f}x{scene_size.height():.1f}")
        print(f"📐 View size: {view_size.width()}x{view_size.height()}")
        print(f"📐 Scale factor: {scale_factor:.3f}")

        # 2. View geometry and positioning
        view_geometry = self.geometry()
        print(
            f"📍 View geometry: x={view_geometry.x()}, y={view_geometry.y()}, w={view_geometry.width()}, h={view_geometry.height()}"
        )
        print(f"📍 View bottom edge: {view_geometry.bottom()}")

        # 3. Parent container geometry
        if self._container:
            container_geometry = self._container.geometry()
            print(
                f"📦 Container geometry: x={container_geometry.x()}, y={container_geometry.y()}, w={container_geometry.width()}, h={container_geometry.height()}"
            )
            print(f"📦 Container bottom edge: {container_geometry.bottom()}")

            # Calculate clipping amount
            view_bottom = view_geometry.bottom()
            container_bottom = container_geometry.bottom()
            clipping_amount = view_bottom - container_bottom
            print(
                f"✂️ Clipping analysis: view_bottom={view_bottom}, container_bottom={container_bottom}"
            )
            if clipping_amount > 0:
                print(
                    f"❌ CONTENT CLIPPED: {clipping_amount}px extends beyond container"
                )
            else:
                print(f"✅ NO CLIPPING: {abs(clipping_amount)}px margin available")

        # 4. Scene rect coordinates and viewport visible area
        scene_rect = self._pictograph_scene.sceneRect()
        print(
            f"🎬 Scene rect coords: x={scene_rect.x()}, y={scene_rect.y()}, w={scene_rect.width()}, h={scene_rect.height()}"
        )

        viewport_rect = self.viewport().geometry()
        print(
            f"👁️ Viewport geometry: x={viewport_rect.x()}, y={viewport_rect.y()}, w={viewport_rect.width()}, h={viewport_rect.height()}"
        )

        # 5. Transform matrix analysis
        transform = self.transform()
        print(
            f"🔄 Transform matrix: m11={transform.m11():.3f}, m22={transform.m22():.3f}, dx={transform.dx():.1f}, dy={transform.dy():.1f}"
        )

        # 6. Effective pictograph size after scaling
        effective_width = scene_size.width() * scale_factor
        effective_height = scene_size.height() * scale_factor
        print(
            f"📏 Effective pictograph size: {effective_width:.1f}x{effective_height:.1f}"
        )

        # 7. Positioning within container analysis
        if self._container:
            container_width = container_geometry.width()
            container_height = container_geometry.height()

            # Calculate how much space is used vs available
            width_utilization = (effective_width / container_width) * 100
            height_utilization = (effective_height / container_height) * 100
            print(
                f"📊 Space utilization: width={width_utilization:.1f}%, height={height_utilization:.1f}%"
            )

            # Check if pictograph fits within container bounds
            if (
                effective_width <= container_width
                and effective_height <= container_height
            ):
                print("✅ Pictograph fits within container bounds")
            else:
                print("❌ Pictograph exceeds container bounds")
                if effective_width > container_width:
                    print(
                        f"   Width overflow: {effective_width - container_width:.1f}px"
                    )
                if effective_height > container_height:
                    print(
                        f"   Height overflow: {effective_height - container_height:.1f}px"
                    )

        print("=" * 80)

    def resizeEvent(self, event):
        """Handle resize events to maintain proper scaling and square aspect ratio like legacy"""
        super().resizeEvent(event)

        # Enforce square aspect ratio exactly like legacy GE_PictographView:
        # self.setFixedSize(self.graph_editor.height(), self.graph_editor.height())
        if self._container and hasattr(self._container, "_graph_editor"):
            graph_editor = self._container._graph_editor
            if graph_editor and hasattr(graph_editor, "height"):
                graph_editor_height = graph_editor.height()
                if graph_editor_height > 0:
                    # No container margins now, so view matches graph editor height exactly
                    square_size = graph_editor_height
                    self.setFixedSize(square_size, square_size)

        # Re-fit the pictograph when the view is resized (handles all scaling)
        self._fit_pictograph_to_view()

    def _enable_arrow_selection(self):
        """Enable arrow selection for graph editor mode."""
        # Connect to arrow renderers in the pictograph scene
        if hasattr(self._pictograph_scene, "arrow_renderer"):
            arrow_renderer = self._pictograph_scene.arrow_renderer
            if hasattr(arrow_renderer, "arrow_clicked"):
                arrow_renderer.arrow_clicked.connect(self._on_arrow_clicked)

        # Make arrows clickable by enabling mouse events on arrow items
        for item in self._pictograph_scene.items():
            if hasattr(item, "arrow_color"):  # Arrow items should have this attribute
                item.setFlag(item.GraphicsItemFlag.ItemIsSelectable, True)
                item.setAcceptHoverEvents(True)
                # Set cursor for arrow items
                item.setCursor(Qt.CursorShape.PointingHandCursor)

    def _on_arrow_clicked(self, arrow_color: str):
        """Handle arrow click from Modern pictograph scene."""
        self.arrow_clicked.emit(arrow_color)

    def get_selected_arrow_data(self) -> Optional[dict]:
        """Get data for the currently selected arrow."""
        if not self._selected_arrow_id or not self._current_beat:
            return None

        # Get arrow data from beat
        if self._selected_arrow_id == "blue" and self._current_beat.blue_motion:
            return {
                "color": "blue",
                "motion": self._current_beat.blue_motion,
                "orientation": getattr(
                    self._current_beat.blue_motion, "orientation", None
                ),
                "turns": getattr(self._current_beat.blue_motion, "turns", 0.0),
            }
        elif self._selected_arrow_id == "red" and self._current_beat.red_motion:
            return {
                "color": "red",
                "motion": self._current_beat.red_motion,
                "orientation": getattr(
                    self._current_beat.red_motion, "orientation", None
                ),
                "turns": getattr(self._current_beat.red_motion, "turns", 0.0),
            }
        return None

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            # Check if we clicked on an arrow in the scene
            scene_pos = self.mapToScene(event.pos())
            item = self.scene().itemAt(scene_pos, self.transform())

            if item and hasattr(item, "arrow_color"):
                # Clicked on an arrow
                arrow_color = item.arrow_color
                self._on_arrow_clicked(arrow_color)
            else:
                # Clicked elsewhere - could deselect current arrow
                pass

        super().mousePressEvent(event)
