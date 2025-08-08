"""Snowflake Worker - Qt Threading Layer

Qt worker for snowflake animation timing - physics logic delegated to SnowflakePhysics service.
"""

from __future__ import annotations

import time

from PyQt6.QtCore import QObject, pyqtSignal
from shared.application.services.backgrounds.snowfall.snowflake_physics import (
    SnowflakePhysics,
)


class SnowflakeWorker(QObject):
    """Qt worker for snowflake animation - delegates physics to SnowflakePhysics service."""

    update_snowflakes = pyqtSignal(list)

    def __init__(self, snowflake_count, width, height, image_count):
        super().__init__()
        self.running = False
        self._physics_service = SnowflakePhysics(
            snowflake_count, width, height, image_count
        )

    def start(self):
        """Start the animation loop."""
        self.running = True
        self.process()

    def stop(self):
        """Stop the animation loop."""
        self.running = False

    def process(self):
        """Main animation loop - delegates physics to service."""
        while self.running:
            # Update physics using service
            self._physics_service.update_snowflakes()

            # Get current states and emit as legacy format for compatibility
            snowflake_states = self._physics_service.get_snowflake_states()
            legacy_format = self._convert_to_legacy_format(snowflake_states)

            self.update_snowflakes.emit(legacy_format)
            time.sleep(0.016)  # ~60 FPS

    def _convert_to_legacy_format(self, snowflake_states):
        """Convert service states to legacy dict format for compatibility."""
        return [
            {
                "x": int(snowflake.x),
                "y": int(snowflake.y),
                "size": snowflake.size,
                "speed": snowflake.speed,
                "image_index": snowflake.image_index,
            }
            for snowflake in snowflake_states
        ]

    def update_bounds(self, width, height):
        """Update bounds - delegate to service."""
        self._physics_service.update_bounds(width, height)
