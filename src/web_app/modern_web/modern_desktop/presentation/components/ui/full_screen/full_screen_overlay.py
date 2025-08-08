"""
Full Screen Overlay Widget

Modern Qt overlay widget for displaying sequence images in full screen.
Based on the legacy FullScreenImageOverlay but with modern architecture patterns.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget


logger = logging.getLogger(__name__)


class FullScreenOverlay(QWidget):
    """
    Modern full screen overlay widget for displaying sequence images.

    Features:
    - Proper aspect ratio preservation
    - Click-anywhere-to-close functionality
    - Smooth scaling with high quality
    - Menu bar height awareness
    - Semi-transparent background
    """

    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialize the full screen overlay.

        Args:
            parent: Parent widget (typically the main window)
        """
        super().__init__(parent)
        self._parent_widget = parent

        self._setup_widget_properties()
        self._setup_image_label()
        self._setup_layout()
        self._setup_geometry()

        logger.info("FullScreenOverlay initialized")

    def _setup_widget_properties(self):
        """Setup basic widget properties"""
        # Make it a top-level window that covers everything
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        # Semi-transparent black background
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.9);")

        # Enable mouse tracking for click-to-close
        self.setMouseTracking(True)

        # Set cursor to indicate clickability
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def _setup_image_label(self):
        """Setup the image display label"""
        self._image_label = QLabel(self)
        self._image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._image_label.setContentsMargins(0, 0, 0, 0)
        self._image_label.setCursor(Qt.CursorShape.PointingHandCursor)

        # Enable mouse events on the label
        self._image_label.setMouseTracking(True)

    def _setup_layout(self):
        """Setup the layout"""
        self._layout = QVBoxLayout(self)
        self._layout.addWidget(self._image_label)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)

    def _setup_geometry(self):
        """Setup initial geometry to cover the parent or screen"""
        if self._parent_widget:
            # Cover the parent widget
            parent_geometry = self._parent_widget.geometry()
            self.setGeometry(parent_geometry)
        else:
            # Cover the primary screen
            from PyQt6.QtGui import QGuiApplication

            screen = QGuiApplication.primaryScreen()
            if screen:
                screen_geometry = screen.geometry()
                self.setGeometry(screen_geometry)

    def show_image(self, image_path: Path) -> None:
        """
        Display an image in the full screen overlay.

        Args:
            image_path: Path to the image file to display
        """
        try:
            if not image_path.exists():
                logger.error(f"Image file not found: {image_path}")
                return

            # Load the image
            pixmap = QPixmap(str(image_path))
            if pixmap.isNull():
                logger.error(f"Failed to load image: {image_path}")
                return

            # Calculate available size (accounting for menu bar)
            available_size = self._calculate_available_size()

            # Scale the image to fit while preserving aspect ratio
            scaled_pixmap = pixmap.scaled(
                available_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            # Set the scaled image
            self._image_label.setPixmap(scaled_pixmap)

            # Show the overlay
            self.show()
            self.raise_()
            self.activateWindow()

            logger.info(f"Displaying image in full screen: {image_path}")

        except Exception as e:
            logger.error(f"Failed to display image: {e}")

    def _calculate_available_size(self):
        """
        Calculate the available size for the image, accounting for menu bar.

        Returns:
            QSize: Available size for image display
        """
        window_size = self.size()

        # Try to get menu bar height from parent
        menu_bar_height = 0
        if self._parent_widget:
            try:
                # Try different ways to get menu bar height
                if hasattr(self._parent_widget, "menuBar"):
                    menu_bar = self._parent_widget.menuBar()
                    if menu_bar and menu_bar.isVisible():
                        menu_bar_height = menu_bar.height()
                elif hasattr(self._parent_widget, "get_widget"):
                    # Legacy widget manager pattern
                    try:
                        menu_bar = self._parent_widget.get_widget("menu_bar")
                        if menu_bar:
                            menu_bar_height = menu_bar.height()
                    except (AttributeError, KeyError):
                        pass
            except Exception as e:
                logger.debug(f"Could not determine menu bar height: {e}")

        # Adjust height for menu bar
        adjusted_height = window_size.height() - menu_bar_height
        window_size.setHeight(adjusted_height)

        return window_size

    def mousePressEvent(self, event):
        """Handle mouse press events - close on any click"""
        try:
            logger.info("Full screen overlay clicked - closing")
            self.close()
        except Exception as e:
            logger.error(f"Error handling mouse press: {e}")
        finally:
            super().mousePressEvent(event)

    def keyPressEvent(self, event):
        """Handle key press events - close on Escape"""
        try:
            if event.key() == Qt.Key.Key_Escape:
                logger.info("Escape key pressed - closing full screen overlay")
                self.close()
            else:
                super().keyPressEvent(event)
        except Exception as e:
            logger.error(f"Error handling key press: {e}")

    def resizeEvent(self, event):
        """Handle resize events - update image scaling"""
        try:
            super().resizeEvent(event)

            # Re-scale the image if we have one
            if self._image_label.pixmap() and not self._image_label.pixmap().isNull():
                # Get the original pixmap and re-scale it
                current_pixmap = self._image_label.pixmap()
                available_size = self._calculate_available_size()

                # Note: This is a simplified approach. In a full implementation,
                # we'd want to keep the original pixmap to avoid quality loss
                scaled_pixmap = current_pixmap.scaled(
                    available_size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )

                self._image_label.setPixmap(scaled_pixmap)

        except Exception as e:
            logger.error(f"Error handling resize: {e}")

    def closeEvent(self, event):
        """Handle close events - cleanup"""
        try:
            logger.info("Full screen overlay closing")
            super().closeEvent(event)
        except Exception as e:
            logger.error(f"Error during close: {e}")


class FullScreenOverlayFactory:
    """
    Factory for creating FullScreenOverlay instances.

    Provides dependency injection and proper widget hierarchy management.
    """

    def __init__(self, main_window_getter=None):
        """
        Initialize the factory.

        Args:
            main_window_getter: Function to get the main window instance
        """
        self._main_window_getter = main_window_getter

    def create_overlay(self, parent_widget=None) -> FullScreenOverlay:
        """
        Create a full screen overlay instance.

        Args:
            parent_widget: Parent widget (if None, will try to get main window)

        Returns:
            FullScreenOverlay instance
        """
        try:
            # Determine parent widget
            if parent_widget is None and self._main_window_getter:
                try:
                    parent_widget = self._main_window_getter()
                except Exception as e:
                    logger.warning(f"Could not get main window: {e}")

            overlay = FullScreenOverlay(parent=parent_widget)
            logger.info("Created FullScreenOverlay with factory")
            return overlay

        except Exception as e:
            logger.error(f"Failed to create FullScreenOverlay: {e}")
            # Return a basic overlay as fallback
            return FullScreenOverlay(parent=None)
