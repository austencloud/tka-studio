from __future__ import annotations

from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import (
    QColor,
    QLinearGradient,
    QPainter,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PyQt6.QtWidgets import QWidget

from desktop.modern.application.services.backgrounds.bubbles.bubble_physics import (
    BubblePhysics,
)
from desktop.modern.application.services.backgrounds.bubbles.fish_movement import (
    FishMovement,
)
from desktop.modern.application.services.backgrounds.bubbles.fish_spawning import (
    FishSpawning,
)

from .base_background import BaseBackground


class BubblesBackground(BaseBackground):
    # Class variable to hold cached images
    _cached_fish_images = None

    def __init__(self, parent=None):
        super().__init__(parent)

        # Check if the fish images are already cached
        if BubblesBackground._cached_fish_images is None:
            # Define the backgrounds folder path
            asset_resolver = AssetPathResolver()
            backgrounds_folder = asset_resolver.get_image_path("backgrounds/")

            # Load the fish images and store them in the class variable
            BubblesBackground._cached_fish_images = [
                QPixmap(backgrounds_folder + "Tropical-Fish-Sherbert.png"),
                QPixmap(backgrounds_folder + "Tropical-Fish-Coral.png"),
                QPixmap(backgrounds_folder + "Tropical-Fish-Seafoam.png"),
                QPixmap(backgrounds_folder + "orange_fish.png"),
                QPixmap(backgrounds_folder + "blue_orange_fish.png"),
                QPixmap(backgrounds_folder + "clown_fish.png"),
                QPixmap(backgrounds_folder + "yellow_fish.png"),
            ]

        # Use the cached images in this instance
        self.fish_images = BubblesBackground._cached_fish_images

        # Initialize services instead of local data
        self.bubble_physics = BubblePhysics(100)
        self.fish_spawning = FishSpawning(len(self.fish_images))
        self.fish_movement = FishMovement()

    def animate_background(self):
        # Update using services
        self.bubble_physics.update_bubbles()
        self.fish_spawning.update_fish_spawning()

        # Update fish positions and remove offscreen fish
        active_fish = self.fish_spawning.get_active_fish()
        self.fish_movement.update_fish_positions(active_fish)
        self.fish_spawning.remove_offscreen_fish()

        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create an underwater gradient (light blue at top, deep blue at bottom)
        gradient = QLinearGradient(0, 0, 0, widget.height())
        gradient.setColorAt(0, QColor(100, 150, 255))  # Light blue
        gradient.setColorAt(1, QColor(0, 30, 90))  # Deep blue
        painter.fillRect(widget.rect(), gradient)

        # Draw bubbles using service data
        self._draw_bubbles(painter, widget)

        # Draw fish using service data
        self._draw_fish(painter, widget)

        painter.setOpacity(1.0)  # Reset opacity after drawing

    def _draw_bubbles(self, painter: QPainter, widget: QWidget):
        """Draw bubbles using service data"""
        for bubble in self.bubble_physics.get_bubble_states():
            x = int(bubble.position.x * widget.width())
            y = int(bubble.position.y * widget.height())
            size = int(bubble.size)

            # Set bubble opacity and fill
            painter.setOpacity(bubble.opacity)
            painter.setBrush(QColor(255, 255, 255, int(bubble.opacity * 255)))
            painter.setPen(Qt.PenStyle.NoPen)

            # Draw the main bubble
            painter.drawEllipse(x, y, size, size)

            # Add a reflection highlight to the bubble for realism
            self.draw_bubble_reflection(
                painter,
                QPointF(x + size / 4, y + size / 4),
                size,
                bubble.highlight_factor,
            )

    def draw_bubble_reflection(
        self, painter: QPainter, center: QPointF, size: int, highlight_factor: float
    ):
        """Draws a reflection highlight on the top of the bubble to simulate lighting."""
        highlight_radius = size * 0.4 * highlight_factor
        gradient = QRadialGradient(center, highlight_radius)
        gradient.setColorAt(0, QColor(255, 255, 255, 180))  # Bright reflection
        gradient.setColorAt(1, QColor(255, 255, 255, 0))  # Soft fade out

        painter.setBrush(gradient)
        painter.drawEllipse(center, highlight_radius, highlight_radius)

    def _draw_fish(self, painter: QPainter, widget: QWidget):
        """Draw fish swimming across the screen using the provided fish images."""
        for fish in self.fish_spawning.get_active_fish():
            x = int(fish.position.x * widget.width())
            y = int(fish.position.y * widget.height())
            size = int(fish.size)

            # Ensure full opacity for the fish
            painter.setOpacity(1.0)

            # Get the fish image
            fish_image = self.fish_images[fish.image_index]

            # Scale the fish image to its size using SmoothTransformation
            fish_image = fish_image.scaled(
                size,
                size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )

            # Flip the fish image if it is moving left (dx < 0)
            direction = self.fish_movement.calculate_fish_direction(fish)
            if direction < 0:
                transform = QTransform().scale(-1, 1)  # Mirror horizontally
                fish_image = fish_image.transformed(
                    transform, Qt.TransformationMode.SmoothTransformation
                )

            # Draw the fish at the correct position with no blending
            painter.drawPixmap(x, y, fish_image)
