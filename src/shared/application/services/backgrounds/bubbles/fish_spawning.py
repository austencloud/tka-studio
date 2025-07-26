import random
from typing import List

from ..shared.animation_types import FishState, Position2D, Velocity2D


class FishSpawning:
    """Pure business logic for fish spawning - extracted from BubblesBackground"""

    def __init__(self, num_fish_images: int = 7):
        self.fish: List[FishState] = []
        self.num_fish_images = num_fish_images
        self._timer = 0
        self._spawn_interval = random.randint(50, 100)

    def update_fish_spawning(self) -> None:
        """Handle fish spawning timing"""
        self._timer += 1
        if self._timer >= self._spawn_interval:
            self._spawn_fish()
            self._timer = 0
            self._spawn_interval = random.randint(100, 200)

    def _spawn_fish(self) -> None:
        """Spawn a fish from a random side of the screen"""
        start_position_options = [
            (-0.1, random.uniform(0.2, 0.8)),  # Left side
            (1.1, random.uniform(0.2, 0.8)),  # Right side
        ]
        start_x, start_y = random.choice(start_position_options)

        # Bias towards horizontal movement
        dx = random.uniform(0.3, 1) if start_x < 0 else random.uniform(-1, -0.3)
        dy = random.uniform(-0.1, 0.1)  # Smaller vertical movement

        # Normalize diagonal movement
        normalization_factor = (dx**2 + dy**2) ** 0.5
        dx /= normalization_factor
        dy /= normalization_factor

        fish = FishState(
            position=Position2D(x=start_x, y=start_y),
            velocity=Velocity2D(dx=dx, dy=dy),
            size=random.uniform(40, 80),
            speed=random.uniform(0.003, 0.005),
            image_index=random.randint(0, self.num_fish_images - 1),
        )
        self.fish.append(fish)

    def get_active_fish(self) -> List[FishState]:
        """Get currently active fish"""
        return self.fish.copy()

    def remove_offscreen_fish(self) -> None:
        """Remove fish that have swum out of view"""
        self.fish = [
            fish
            for fish in self.fish
            if -0.2 <= fish.position.x <= 1.2 and -0.2 <= fish.position.y <= 1.2
        ]

    def reset(self) -> None:
        """Reset fish spawning"""
        self.fish.clear()
        self._timer = 0
        self._spawn_interval = random.randint(50, 100)
