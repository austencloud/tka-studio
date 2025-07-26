import random
from typing import List

from ..shared.animation_types import BlobState, Position2D, Velocity2D


class AuroraBlobAnimation:
    """Pure business logic for aurora blob animation - extracted from BlobManager"""

    def __init__(self, num_blobs: int = 3):
        self.blobs: List[BlobState] = []
        self._create_blobs(num_blobs)

    def _create_blobs(self, num_blobs: int) -> None:
        """Create initial blobs with random positions and properties"""
        self.blobs = []
        for _ in range(num_blobs):
            blob = BlobState(
                position=Position2D(
                    x=random.uniform(0.1, 0.9), y=random.uniform(0.1, 0.9)
                ),
                velocity=Velocity2D(
                    dx=random.uniform(-0.0005, 0.0005),
                    dy=random.uniform(-0.0005, 0.0005),
                ),
                size=random.uniform(100, 200),
                opacity=random.uniform(0.2, 0.5),
                size_delta=random.uniform(-0.1, 0.1),
                opacity_delta=random.uniform(-0.001, 0.001),
            )
            self.blobs.append(blob)

    def update_blobs(self) -> None:
        """Animate blobs by updating their position, size, and opacity"""
        for blob in self.blobs:
            # Update position
            blob.position.x += blob.velocity.dx
            blob.position.y += blob.velocity.dy

            # Update size and opacity
            blob.size += blob.size_delta
            blob.opacity += blob.opacity_delta

            # Boundary collision and direction reversal
            if blob.position.x < 0 or blob.position.x > 1:
                blob.velocity.dx *= -1
            if blob.position.y < 0 or blob.position.y > 1:
                blob.velocity.dy *= -1
            if blob.size < 50 or blob.size > 250:
                blob.size_delta *= -1
            if blob.opacity < 0.1 or blob.opacity > 0.5:
                blob.opacity_delta *= -1

    def get_blob_states(self) -> List[BlobState]:
        """Get current blob states for rendering"""
        return self.blobs.copy()

    def reset(self) -> None:
        """Reset blobs to initial state"""
        self._create_blobs(len(self.blobs))
