import random

from ..shared.animation_types import Position2D, ShootingStarState, Velocity2D


class ShootingStar:
    """Pure business logic for shooting star - extracted from ShootingStarManager"""

    def __init__(self):
        self.shooting_star: ShootingStarState | None = None
        self._timer = 0
        self._spawn_interval = random.randint(100, 300)

    def update_shooting_star(self) -> None:
        """Update shooting star movement and spawning"""
        if self.shooting_star:
            self._move_shooting_star()
        else:
            self._timer += 1
            if self._timer >= self._spawn_interval:
                self._spawn_shooting_star()

    def _spawn_shooting_star(self) -> None:
        """Spawn a shooting star with initial parameters"""
        start_position_options = [
            (-0.1, random.uniform(0.2, 0.8)),  # Coming from the left
            (1.1, random.uniform(0.2, 0.8)),  # Coming from the right
        ]
        start_x, start_y = random.choice(start_position_options)

        # Ensure the star travels mostly diagonally
        dx = random.uniform(0.3, 0.7) * (-1 if start_x > 0 else 1)
        dy = random.uniform(0.3, 0.6)

        # Normalize direction vector
        normalization_factor = (dx**2 + dy**2) ** 0.5
        dx /= normalization_factor
        dy /= normalization_factor

        self.shooting_star = ShootingStarState(
            position=Position2D(x=start_x, y=start_y),
            velocity=Velocity2D(dx=dx, dy=dy),
            size=random.uniform(5, 10),
            speed=random.uniform(0.08, 0.13),
            tail=[],
            tail_length=30,
            tail_opacity=1.0,
            off_screen=False,
        )
        self._timer = 0
        self._spawn_interval = random.randint(100, 300)

    def _move_shooting_star(self) -> None:
        """Move the shooting star and manage its tail"""
        star = self.shooting_star
        if not star:
            return

        # Calculate movement
        new_x = star.position.x + (star.velocity.dx * star.speed)
        new_y = star.position.y + (star.velocity.dy * star.speed)

        # Add multiple points between previous and new positions
        steps = 25
        prev_x, prev_y = star.position.x, star.position.y
        for i in range(steps):
            interp_x = prev_x + (new_x - prev_x) * (i / steps)
            interp_y = prev_y + (new_y - prev_y) * (i / steps)
            star.tail.append((interp_x, interp_y, star.size))

        # Update position
        star.position.x = new_x
        star.position.y = new_y

        # Check if off-screen
        if star.position.x < -0.1 or star.position.x > 1.1 or star.position.y > 1.1:
            star.off_screen = True

        # Handle tail fading
        if star.off_screen:
            star.tail_opacity -= 0.05
            if star.tail_opacity <= 0:
                self.shooting_star = None

        # Limit tail length
        if len(star.tail) > star.tail_length:
            star.tail.pop(0)

    def get_shooting_star_state(self) -> ShootingStarState | None:
        """Get current shooting star state for rendering"""
        return self.shooting_star
