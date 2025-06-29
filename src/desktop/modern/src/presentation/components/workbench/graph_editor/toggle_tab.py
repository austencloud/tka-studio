from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import (
    pyqtSignal,
    QTimer,
    QPropertyAnimation,
    QEasingCurve,
    QEvent,
    Qt,
)
from PyQt6.QtGui import QFont


class ToggleTab(QWidget):
    toggle_requested = pyqtSignal()

    def __init__(self, parent, positioning_style="left"):
        super().__init__(parent)
        self._graph_editor = parent
        self._animating = False
        self._real_time_sync_active = (
            False  # Flag to disable all positioning during real-time sync
        )
        self._positioning_style = (
            positioning_style  # "left" for legacy-exact bottom-left positioning
        )

        self._setup_ui()
        self._setup_animation()
        # Defer initial positioning until parent is fully initialized
        QTimer.singleShot(0, self._position_tab)

    def _setup_ui(self):
        """Setup the toggle button UI with proper styling and sizing"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create toggle button with proper text and styling
        self._toggle_btn = QPushButton("Graph Editor ▲")
        self._toggle_btn.clicked.connect(self.toggle_requested.emit)
        self._toggle_btn.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self._toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        # Set initial visual state (disconnected)
        self._update_visual_state()

        layout.addWidget(self._toggle_btn)

        # Set proper size to accommodate button content with padding
        # Button has padding: 8px 16px, so we need extra space
        # Width: min-width 120px + padding 32px (16px * 2) + border 4px = 156px
        # Height: min-height 16px + padding 16px (8px * 2) + border 4px = 36px
        self.setMinimumSize(156, 36)
        self.setMaximumSize(180, 42)

        # Ensure button fills the container properly
        self._toggle_btn.setSizePolicy(
            self._toggle_btn.sizePolicy().horizontalPolicy(),
            self._toggle_btn.sizePolicy().verticalPolicy(),
        )

    def _setup_animation(self):
        """Setup smooth position animation system"""
        from PyQt6.QtCore import QPoint

        # Position animation for smooth movement
        self._position_animation = QPropertyAnimation(self, b"pos")
        self._position_animation.setDuration(300)  # Smooth 300ms animation
        self._position_animation.setEasingCurve(QEasingCurve.Type.OutCubic)

        # Connect animation events
        self._position_animation.finished.connect(self._on_animation_finished)

    def _on_animation_finished(self):
        """Handle animation completion"""
        self._animating = False

    def _update_visual_state(self):
        """Update visual styling with permanent purple-blue gradient (legacy-exact)"""
        # Always use the attractive purple-blue gradient regardless of state
        # This matches the legacy behavior where the toggle tab always looks appealing
        self._toggle_btn.setStyleSheet(
            """
            QPushButton {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #6a11cb,
                    stop: 1 #2575fc
                );
                border: 2px solid #555;
                border-radius: 12px 12px 0px 0px;
                color: white;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 12px; bv
                min-width: 120px;
                min-height: 16px;
            }
            QPushButton:hover {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #7a21db,
                    stop: 1 #3585fc
                );
            }
            QPushButton:pressed {
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 1,
                    stop: 0 #5a01bb,
                    stop: 1 #1565ec
                );
            }
        """
        )

    def _position_tab(self):
        """Position the toggle tab initially at the bottom center of workbench"""
        # Find the right parent - should be the workbench
        workbench_parent = self._graph_editor.parent()
        if workbench_parent:
            # Go up to find the actual workbench (graph_section -> workbench)
            while workbench_parent and not hasattr(
                workbench_parent, "_beat_frame_section"
            ):
                workbench_parent = workbench_parent.parent()

        if not workbench_parent:
            # Defer positioning until parent is available
            QTimer.singleShot(100, self._position_tab)
            return

        self.setParent(workbench_parent)

        # Ensure parent has valid dimensions before positioning
        if workbench_parent.width() <= 0 or workbench_parent.height() <= 0:
            # Defer positioning until parent has valid size
            QTimer.singleShot(100, self._position_tab)
            return

        # CRITICAL FIX: Ensure workbench has reasonable size before positioning
        # The workbench starts very small (100x30) and grows later
        if workbench_parent.height() < 200:  # Minimum reasonable workbench height
            print(
                f"🔍 [INIT DEBUG] Workbench too small ({workbench_parent.height()}px), deferring positioning..."
            )
            QTimer.singleShot(100, self._position_tab)
            return

        # Use bottom-left corner positioning (legacy-exact)
        # Position at the very bottom-left corner of the window
        x = 0  # Bottom-left corner positioning
        y = (
            workbench_parent.height() - self.height()
        )  # Bottom edge positioning (legacy-exact)

        # Debug info for initial positioning
        print(
            f"🔍 [INIT DEBUG] Workbench size: {workbench_parent.width()}x{workbench_parent.height()}"
        )
        print(f"🔍 [INIT DEBUG] Toggle tab size: {self.width()}x{self.height()}")
        print(f"🔍 [INIT DEBUG] Calculated position: ({x}, {y})")

        self.move(x, y)
        self.raise_()

        # Ensure button is visible
        self.show()
        print(
            f"🎯 Toggle tab positioned at ({x}, {y}) in parent {type(workbench_parent).__name__}"
        )

    def update_position(self, animate=True):
        """Update position to hug the top of graph editor frame (Legacy-exact behavior)"""
        # Check if graph editor is currently animating - if so, real-time sync handles positioning
        if (
            hasattr(self._graph_editor, "_animation_controller")
            and self._graph_editor._animation_controller.is_animating()
        ):
            print(
                "🚫 [SYNC DEBUG] Blocking toggle tab position update - real-time sync active"
            )
            return

        if not self._graph_editor._parent_workbench:
            return

        # Prevent multiple animations
        if self._animating and animate:
            return

        # Block all positioning if real-time sync is active
        if self._real_time_sync_active:
            print(
                "🚫 [SYNC DEBUG] Blocking position update - real-time sync controls positioning"
            )
            return

        parent = self._graph_editor._parent_workbench

        # Use bottom-left corner positioning (legacy-exact)
        # Position at the very bottom-left corner of the window
        x = 0  # Bottom-left corner positioning

        if self._graph_editor.is_visible():
            # Graph editor is open: position so bottom of toggle aligns with top of graph editor
            # CRITICAL FIX: Use actual graph editor position relative to workbench
            # Get the graph editor's actual position within the workbench coordinate system
            graph_editor_rect = self._graph_editor.geometry()

            # Safety check: ensure graph editor has valid geometry
            if graph_editor_rect.height() <= 0:
                print(
                    f"⚠️ [TOGGLE DEBUG] Graph editor has invalid geometry: {graph_editor_rect}"
                )
                # Fallback to bottom positioning
                y = parent.height() - self.height()
            else:
                # Map the graph editor's top-left corner to workbench coordinates
                workbench_pos = self._graph_editor.mapTo(
                    parent, graph_editor_rect.topLeft()
                )

                print(
                    f"🔍 [TOGGLE DEBUG] Graph editor rect: {graph_editor_rect}, workbench_pos: {workbench_pos}"
                )

                # Toggle tab's bottom edge should align with graph editor's top edge
                # So toggle tab's top edge should be at: graph_editor_top_y - self.height()
                y = workbench_pos.y() - self.height()  # Actual position alignment
            self._toggle_btn.setText("Graph Editor ▼")
        else:
            # Graph editor is closed: position at bottom edge of window
            y = (
                parent.height() - self.height()
            )  # Bottom edge positioning (legacy-exact)
            self._toggle_btn.setText("Graph Editor ▲")

        # Update visual state to show connection
        self._update_visual_state()

        if animate and not self._animating:
            # Animate to new position
            self._animating = True
            from PyQt6.QtCore import QPoint

            self._position_animation.setStartValue(self.pos())
            self._position_animation.setEndValue(QPoint(x, y))
            self._position_animation.start()
        else:
            # Move immediately without animation
            self.move(x, y)

        self.raise_()

    def resizeEvent(self, event):
        """Handle resize events like Legacy toggle tab"""
        super().resizeEvent(event)
        # Update position when the tab itself is resized (no animation during resize)
        self.update_position(animate=False)

    def eventFilter(self, obj, event):
        """Filter events to catch parent window resize"""
        if (
            event.type() == QEvent.Type.Resize
            and obj == self._graph_editor._parent_workbench
        ):
            # Parent window resized, update our position
            QTimer.singleShot(0, lambda: self.update_position(animate=False))
        return super().eventFilter(obj, event)

    def showEvent(self, event):
        """Handle show events to install event filter"""
        super().showEvent(event)
        if self._graph_editor._parent_workbench:
            # Install event filter to catch parent resize events
            self._graph_editor._parent_workbench.installEventFilter(self)

    def hideEvent(self, event):
        """Handle hide events to remove event filter"""
        super().hideEvent(event)
        if self._graph_editor._parent_workbench:
            # Remove event filter when hiding
            self._graph_editor._parent_workbench.removeEventFilter(self)

    def set_real_time_sync_active(self, active: bool):
        """Enable/disable real-time sync mode to prevent positioning conflicts"""
        self._real_time_sync_active = active
        if active:
            print(
                "🔄 [SYNC DEBUG] Real-time sync mode ENABLED - toggle tab positioning disabled"
            )
        else:
            print(
                "🔄 [SYNC DEBUG] Real-time sync mode DISABLED - toggle tab positioning enabled"
            )

    def is_real_time_sync_active(self) -> bool:
        """Check if real-time sync mode is active"""
        return self._real_time_sync_active
