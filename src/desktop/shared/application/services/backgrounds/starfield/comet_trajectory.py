import random

from ..shared.animation_types import CometState, Position2D, Velocity2D


class CometTrajectory:
    """Pure business logic for comet movement - extracted from CometManager"""

    def __init__(self):
        self.comet: CometState | None = None
        self._timer = random.randint(300, 600)
        self._max_tail_length = 35

    def update_comet(self) -> None:
        """Update comet animation and movement"""
        if self.comet and self.comet.active:
            self._move_comet()
        else:
            self._timer -= 1
            if self._timer <= 0:
                self._activate_comet()

    def _activate_comet(self) -> None:
        """Activate the comet by setting its initial position and properties"""
        # Choose random starting position from screen edges
        start_position_options = [
            (random.uniform(-0.1, 0), random.uniform(0.1, 0.9)),  # Coming from left
            (random.uniform(1.0, 1.1), random.uniform(0.1, 0.9)),  # Coming from right
            (random.uniform(0.1, 0.9), random.uniform(-0.1, 0)),  # Coming from top
            (random.uniform(0.1, 0.9), random.uniform(1.0, 1.1)),  # Coming from bottom
        ]
        start_x, start_y = random.choice(start_position_options)

        # Calculate direction vector (normalized)
        dx = random.uniform(-0.5, 0.5)
        dy = random.uniform(-0.5, 0.5)
        normalization_factor = (dx**2 + dy**2) ** 0.5
        if normalization_factor > 0:
            dx /= normalization_factor
            dy /= normalization_factor

        # Assign random color for the comet
        comet_color = (
            random.randint(200, 255),  # Red
            random.randint(200, 255),  # Green
            random.randint(150, 255),  # Blue
        )

        self.comet = CometState(
            position=Position2D(x=start_x, y=start_y),
            prev_position=Position2D(x=start_x, y=start_y),
            velocity=Velocity2D(dx=dx, dy=dy),
            size=random.uniform(8, 16),
            speed=random.uniform(0.015, 0.025),
            tail=[],
            color=comet_color,
            active=True,
            fading=False,
            off_screen=False,
        )

        # Reset timer for next comet
        self._timer = random.randint(400, 800)

    def _move_comet(self) -> None:
        """Update comet position and tail animation"""
        if not self.comet:
            return

        # If comet is fading, only fade out the tail
        if self.comet.fading:
            if len(self.comet.tail) > 0:
                self.comet.tail.pop(0)
            else:
                self.comet.active = False
                self._timer = random.randint(300, 600)
            return

        # Normal comet movement
        new_x = self.comet.position.x + self.comet.velocity.dx * self.comet.speed
        new_y = self.comet.position.y + self.comet.velocity.dy * self.comet.speed

        # Add current position to tail
        self.comet.tail.append(
            (self.comet.position.x, self.comet.position.y, self.comet.size)
        )

        # Update position
        self.comet.prev_position = Position2D(
            x=self.comet.position.x, y=self.comet.position.y
        )
        self.comet.position.x = new_x
        self.comet.position.y = new_y

        # Limit tail length
        if len(self.comet.tail) > self._max_tail_length:
            self.comet.tail.pop(0)

        # Check if comet moved off-screen
        if (
            self.comet.position.x < -0.2
            or self.comet.position.x > 1.2
            or self.comet.position.y < -0.2
            or self.comet.position.y > 1.2
        ):
            self.comet.off_screen = True
            self.comet.fading = True

    def get_comet_state(self) -> CometState | None:
        """Get current comet state for rendering"""
        return self.comet if self.comet and self.comet.active else None
