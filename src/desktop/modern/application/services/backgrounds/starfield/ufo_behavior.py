from __future__ import annotations

import math
import random

from PyQt6.QtGui import QPixmap

from desktop.modern.application.services.backgrounds.shared.animation_types import (
    Position2D,
    UFOState,
    Velocity2D,
)

from ..shared.asset_paths import AssetPathResolver


class UFOBehavior:
    """Pure business logic for UFO behavior - extracted from UFOManager"""

    def __init__(self, behavior_mode: str = "wandering"):
        self.behavior_mode = behavior_mode
        self.ufo: UFOState | None = None
        self._pause_timer = 0
        self._appearance_timer = 0
        self._active_duration = 0

        # Load UFO image
        self.asset_resolver = AssetPathResolver()
        self.ufo_image = self.asset_resolver.get_cached_image("backgrounds/ufo.png")
        self.use_image = not self.ufo_image.isNull()

        if not self.use_image:
            print("UFO image not found, using procedural UFO")

        self._init_ufo()

    def _init_ufo(self) -> None:
        """Initialize UFO based on behavior mode"""
        if self.behavior_mode == "wandering":
            self.ufo = UFOState(
                position=Position2D(
                    x=random.uniform(0.1, 0.9), y=random.uniform(0.1, 0.9)
                ),
                velocity=Velocity2D(
                    dx=random.uniform(-0.5, 0.5), dy=random.uniform(-0.5, 0.5)
                ),
                size=random.uniform(40, 60),
                speed=random.uniform(0.003, 0.008),
                active=True,
                paused=False,
                pause_duration=0,
                glow_phase=0,
            )
            self._pause_timer = random.randint(50, 150)
        else:  # flyby mode
            self.ufo = UFOState(
                position=Position2D(x=0, y=0),
                velocity=Velocity2D(dx=0, dy=0),
                size=random.uniform(40, 60),
                speed=random.uniform(0.01, 0.02),
                active=False,
                paused=False,
                pause_duration=0,
                glow_phase=0,
            )
            self._appearance_timer = random.randint(100, 300)

    def update_ufo(self) -> None:
        """Update UFO animation and movement"""
        if not self.ufo:
            return

        # Update glow effect
        self.ufo.glow_phase += 0.05
        if self.ufo.glow_phase > 2 * math.pi:
            self.ufo.glow_phase = 0

        if self.behavior_mode == "wandering":
            self._update_wandering()
        else:
            self._update_flyby()

    def _update_wandering(self) -> None:
        """Update wandering behavior"""
        if not self.ufo:
            return

        if self.ufo.paused:
            self.ufo.pause_duration -= 1
            if self.ufo.pause_duration <= 0:
                self.ufo.paused = False
                self.ufo.velocity.dx = random.uniform(-0.5, 0.5)
                self.ufo.velocity.dy = random.uniform(-0.5, 0.5)
                self._pause_timer = random.randint(100, 200)
        else:
            # Move UFO
            self.ufo.position.x += self.ufo.velocity.dx * self.ufo.speed
            self.ufo.position.y += self.ufo.velocity.dy * self.ufo.speed

            # Boundary bouncing
            if self.ufo.position.x < 0.05 or self.ufo.position.x > 0.95:
                self.ufo.velocity.dx *= -1
                self.ufo.position.x = max(0.05, min(0.95, self.ufo.position.x))
            if self.ufo.position.y < 0.05 or self.ufo.position.y > 0.95:
                self.ufo.velocity.dy *= -1
                self.ufo.position.y = max(0.05, min(0.95, self.ufo.position.y))

            # Pause timing
            self._pause_timer -= 1
            if self._pause_timer <= 0:
                self.ufo.paused = True
                self.ufo.pause_duration = random.randint(100, 300)

    def _update_flyby(self) -> None:
        """Update flyby behavior"""
        if not self.ufo:
            return

        if not self.ufo.active:
            self._appearance_timer -= 1
            if self._appearance_timer <= 0:
                self._set_offscreen_entry()
                self.ufo.active = True
                self._active_duration = random.randint(300, 500)
                self._appearance_timer = random.randint(500, 1000)
        else:
            self._active_duration -= 1
            if self._active_duration <= 0:
                self.ufo.active = False
            else:
                # Move UFO in straight line
                self.ufo.position.x += self.ufo.velocity.dx * self.ufo.speed
                self.ufo.position.y += self.ufo.velocity.dy * self.ufo.speed

                # Check if out of bounds
                if (
                    self.ufo.position.x < -0.1
                    or self.ufo.position.x > 1.1
                    or self.ufo.position.y < -0.1
                    or self.ufo.position.y > 1.1
                ):
                    self.ufo.active = False

    def _set_offscreen_entry(self) -> None:
        """Initialize UFO entry from off-screen"""
        if not self.ufo:
            return

        entry_side = random.choice(["left", "right", "top", "bottom"])

        if entry_side == "left":
            self.ufo.position.x = -0.1
            self.ufo.position.y = random.uniform(0.2, 0.8)
            self.ufo.velocity.dx = random.uniform(0.01, 0.02)
            self.ufo.velocity.dy = 0
        elif entry_side == "right":
            self.ufo.position.x = 1.1
            self.ufo.position.y = random.uniform(0.2, 0.8)
            self.ufo.velocity.dx = -random.uniform(0.01, 0.02)
            self.ufo.velocity.dy = 0
        elif entry_side == "top":
            self.ufo.position.x = random.uniform(0.2, 0.8)
            self.ufo.position.y = -0.1
            self.ufo.velocity.dx = 0
            self.ufo.velocity.dy = random.uniform(0.01, 0.02)
        elif entry_side == "bottom":
            self.ufo.position.x = random.uniform(0.2, 0.8)
            self.ufo.position.y = 1.1
            self.ufo.velocity.dx = 0
            self.ufo.velocity.dy = -random.uniform(0.01, 0.02)

    def get_glow_intensity(self) -> float:
        """Get current glow intensity"""
        if not self.ufo:
            return 0.0
        return (math.sin(self.ufo.glow_phase) + 1) / 2

    def get_ufo_state(self) -> UFOState | None:
        """Get current UFO state for rendering"""
        return self.ufo if self.ufo and self.ufo.active else None

    def set_behavior_mode(self, mode: str) -> None:
        """Change UFO behavior mode at runtime"""
        if mode != self.behavior_mode:
            self.behavior_mode = mode
            self._init_ufo()

    def reset(self) -> None:
        """Reset UFO to initial state"""
        self._init_ufo()

    def get_ufo_image(self) -> QPixmap:
        """Get the UFO image for rendering"""
        return self.ufo_image

    def should_use_image(self) -> bool:
        """Check if UFO should be rendered using image"""
        return self.use_image
