import random
from typing import List

from ..shared.animation_types import BubbleState, Position2D


class BubblePhysics:
    """Pure business logic for bubble physics - extracted from BubblesBackground"""

    def __init__(self, num_bubbles: int = 100):
        self.bubbles: List[BubbleState] = []
        self._initialize_bubbles(num_bubbles)

    def _initialize_bubbles(self, num_bubbles: int) -> None:
        """Create bubbles floating upward with properties"""
        self.bubbles = []
        for _ in range(num_bubbles):
            bubble = BubbleState(
                position=Position2D(x=random.uniform(0, 1), y=random.uniform(0, 1)),
                size=random.uniform(5, 15),
                speed=random.uniform(0.0005, 0.002),
                opacity=random.uniform(0.4, 0.8),
                highlight_factor=random.uniform(0.7, 1.0),
            )
            self.bubbles.append(bubble)

    def update_bubbles(self) -> None:
        """Move bubbles upward and reset when they reach the top"""
        for bubble in self.bubbles:
            bubble.position.y -= bubble.speed
            if bubble.position.y < 0:
                bubble.position.y = 1  # Reset to bottom
                bubble.position.x = random.uniform(0, 1)
                bubble.size = random.uniform(5, 15)
                bubble.highlight_factor = random.uniform(0.7, 1.0)

    def get_bubble_states(self) -> List[BubbleState]:
        """Get current bubble states for rendering"""
        return self.bubbles.copy()

    def reset(self) -> None:
        """Reset all bubbles"""
        self._initialize_bubbles(len(self.bubbles))
