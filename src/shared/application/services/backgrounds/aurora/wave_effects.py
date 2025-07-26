import math


class AuroraWaveEffects:
    """Pure business logic for aurora wave effects - extracted from AuroraBackground"""

    def __init__(self):
        self.wave_phase = 0
        self.gradient_shift = 0
        self.color_shift = 0

    def update_wave_effects(self) -> None:
        """Update wave animation parameters"""
        self.gradient_shift += 0.01
        self.color_shift = (self.color_shift + 2) % 360
        self.wave_phase += 0.02

    def calculate_wave_shift(self, color_index: int, total_colors: int) -> float:
        """Calculate wave shift for gradient positioning"""
        return 0.1 * math.sin(
            self.wave_phase + color_index * 2 * math.pi / total_colors
        )

    def get_color_hue(self, base_hue: int, color_index: int) -> int:
        """Calculate animated color hue"""
        return int((self.color_shift + color_index * 120) % 360)

    def get_current_state(self) -> dict:
        """Get current wave state for debugging"""
        return {
            "wave_phase": self.wave_phase,
            "gradient_shift": self.gradient_shift,
            "color_shift": self.color_shift,
        }

    def reset(self) -> None:
        """Reset wave effects to initial state"""
        self.wave_phase = 0
        self.gradient_shift = 0
        self.color_shift = 0
