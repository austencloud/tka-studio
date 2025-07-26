import random
from typing import List

from ..shared.animation_types import Position2D, SparkleState


class AuroraSparkleAnimation:
    """Pure business logic for aurora sparkle animation - extracted from SparkleManager"""

    def __init__(self, num_sparkles: int = 50):
        self.sparkles: List[SparkleState] = []
        self._create_sparkles(num_sparkles)

    def _create_sparkles(self, num_sparkles: int) -> None:
        """Create initial sparkles with random positions and properties"""
        self.sparkles = []
        for _ in range(num_sparkles):
            sparkle = SparkleState(
                position=Position2D(x=random.uniform(0, 1), y=random.uniform(0, 1)),
                size=random.uniform(2, 4),
                opacity=random.uniform(0.5, 1.0),
                pulse_speed=random.uniform(0.005, 0.015),
            )
            self.sparkles.append(sparkle)

    def update_sparkles(self) -> None:
        """Animate sparkles by updating their opacity"""
        for sparkle in self.sparkles:
            sparkle.opacity += sparkle.pulse_speed
            if sparkle.opacity > 1.0 or sparkle.opacity < 0.5:
                sparkle.pulse_speed *= -1  # Reverse the pulse direction

    def get_sparkle_states(self) -> List[SparkleState]:
        """Get current sparkle states for rendering"""
        return self.sparkles.copy()

    def reset(self) -> None:
        """Reset sparkles to initial state"""
        self._create_sparkles(len(self.sparkles))
