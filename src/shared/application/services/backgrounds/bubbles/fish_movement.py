from ..shared.animation_types import FishState


class FishMovement:
    """Pure business logic for fish movement - extracted from BubblesBackground"""

    def __init__(self):
        pass

    def update_fish_positions(self, fish_list: list[FishState]) -> None:
        """Update positions of all fish"""
        for fish in fish_list:
            fish.position.x += fish.velocity.dx * fish.speed
            fish.position.y += fish.velocity.dy * fish.speed

    def calculate_fish_direction(self, fish: FishState) -> int:
        """Calculate fish facing direction for rendering"""
        return -1 if fish.velocity.dx < 0 else 1
