import math
import random
from typing import List

from ..shared.animation_types import Position2D, StarState


class StarTwinkling:
    """Pure business logic for star twinkling - extracted from StarManager"""

    def __init__(self, num_stars: int = 150):
        self.stars: List[StarState] = []
        self.twinkle_state: List[float] = []
        self._create_stars(num_stars)

    def _create_stars(self, num_stars: int) -> None:
        """Create diverse star population"""
        self.stars = []
        self.twinkle_state = []

        color_options = [
            (255, 255, 255, 255),  # White stars
            (255, 255, 0, 255),  # Yellow stars
            (255, 200, 200, 255),  # Reddish stars
            (200, 200, 255, 255),  # Bluish stars
        ]

        for _ in range(num_stars):
            star = StarState(
                position=Position2D(x=random.random(), y=random.random()),
                size=random.random() * 2 + 1,
                color=random.choice(color_options),
                spikiness=random.choice([0, 1, 2]),  # 0: round, 1: star shape, 2: spiky
                twinkle_speed=random.uniform(0.5, 2.0),
                twinkle_phase=random.uniform(0, 2 * math.pi),
            )
            self.stars.append(star)
            self.twinkle_state.append(random.uniform(0.8, 1.0))

    def update_stars(self) -> None:
        """Update star twinkling animation"""
        for i, star in enumerate(self.stars):
            # Smooth twinkling using sine waves
            star.twinkle_phase += star.twinkle_speed * 0.1
            twinkle_intensity = (math.sin(star.twinkle_phase) + 1) / 2
            self.twinkle_state[i] = 0.6 + (twinkle_intensity * 0.4)  # Range: 0.6 to 1.0

    def get_star_states(self) -> List[StarState]:
        """Get current star states for rendering"""
        return self.stars.copy()

    def get_twinkle_states(self) -> List[float]:
        """Get current twinkle intensities"""
        return self.twinkle_state.copy()

    def reset(self) -> None:
        """Reset stars to initial state"""
        self._create_stars(len(self.stars))
