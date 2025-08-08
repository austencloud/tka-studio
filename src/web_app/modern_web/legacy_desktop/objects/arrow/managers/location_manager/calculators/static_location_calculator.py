from __future__ import annotations

from .base_location_calculator import BaseLocationCalculator


class StaticLocationCalculator(BaseLocationCalculator):
    def calculate_location(self) -> str:
        start_loc = self.arrow.motion.state.start_loc
        # Return empty string if motion state is not yet initialized
        if start_loc is None:
            return ""
        return start_loc
