import random
from typing import Optional

from ..shared.animation_types import SantaState


class SantaMovement:
    """Pure business logic for Santa movement - extracted from SantaManager"""

    def __init__(self):
        self.santa: Optional[SantaState] = None
        self._timer = 0
        self._spawn_interval = random.randint(500, 1000)

    def update_santa(self) -> None:
        """Update Santa movement and spawning logic"""
        if self.santa and self.santa.active:
            # Move Santa across the screen
            self.santa.x += self.santa.speed * self.santa.direction

            # Check if Santa has moved off-screen
            if (self.santa.direction == 1 and self.santa.x > 1.2) or (
                self.santa.direction == -1 and self.santa.x < -0.2
            ):
                self.santa.active = False
                self._timer = 0
        else:
            # Increment timer and check if it's time to show Santa
            self._timer += 1
            if self._timer >= self._spawn_interval:
                self._spawn_santa()

    def _spawn_santa(self) -> None:
        """Spawn Santa with random properties"""
        direction = random.choice([-1, 1])
        self.santa = SantaState(
            x=-0.2 if direction == 1 else 1.2,
            y=random.uniform(0.1, 0.3),
            speed=random.uniform(0.003, 0.005),
            direction=direction,
            active=True,
            opacity=0.8,
        )
        self._spawn_interval = random.randint(500, 1000)

    def get_santa_state(self) -> Optional[SantaState]:
        """Get current Santa state for rendering"""
        return self.santa if self.santa and self.santa.active else None

    def reset(self) -> None:
        """Reset Santa to initial state"""
        self.santa = None
        self._timer = 0
        self._spawn_interval = random.randint(500, 1000)
