import random

from ..shared.animation_types import SnowflakeState


class SnowflakePhysics:
    """Pure business logic for snowflake physics - extracted from SnowflakeWorker"""

    def __init__(
        self, snowflake_count: int, width: float, height: float, image_count: int
    ):
        self.snowflake_count = snowflake_count
        self.width = width
        self.height = height
        self.image_count = image_count
        self.snowflakes: list[SnowflakeState] = []
        self._initialize_snowflakes()

    def _initialize_snowflakes(self) -> None:
        """Initialize snowflake positions and properties"""
        self.snowflakes = []
        for _ in range(self.snowflake_count):
            snowflake = SnowflakeState(
                x=random.randint(0, int(self.width)),
                y=random.randint(-int(self.height), 0),
                size=random.randint(2, 6),
                speed=random.uniform(0.5, 2.0),
                image_index=random.randint(0, self.image_count - 1),
            )
            self.snowflakes.append(snowflake)

    def update_snowflakes(self) -> None:
        """Update snowflake positions and reset out-of-bounds snowflakes"""
        for snowflake in self.snowflakes:
            snowflake.y += snowflake.speed
            if snowflake.y > self.height:
                snowflake.y = random.randint(-20, 0)
                snowflake.x = random.randint(0, int(self.width))
                snowflake.size = random.randint(2, 6)
                snowflake.speed = random.uniform(0.5, 2.0)
                snowflake.image_index = random.randint(0, self.image_count - 1)

    def get_snowflake_states(self) -> list[SnowflakeState]:
        """Get current snowflake states for rendering"""
        return self.snowflakes.copy()

    def update_bounds(self, width: float, height: float) -> None:
        """Update the bounds for snowflake generation"""
        self.width = width
        self.height = height
        self._initialize_snowflakes()
