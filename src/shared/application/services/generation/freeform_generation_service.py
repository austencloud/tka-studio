"""
Freeform Generation Service - Fixed Implementation

Provides the RotationDeterminer and other utilities that SequenceGenerator needs.
"""

import random


class RotationDeterminer:
    """
    CRITICAL FIX: Provides rotation direction logic that SequenceGenerator expects.

    Direct port from legacy rotation determination logic.
    """

    @staticmethod
    def get_rotation_dirs(prop_continuity: str) -> tuple[str | None, str | None]:
        """
        Get rotation directions based on prop continuity setting.

        This matches the exact interface that SequenceGenerator is calling.

        Args:
            prop_continuity: "continuous" or "random"

        Returns:
            Tuple of (blue_rot_dir, red_rot_dir) or (None, None) for random
        """
        print(f"🔧 Determining rotation directions for continuity: {prop_continuity}")

        if prop_continuity == "continuous":
            # Legacy behavior - select random directions but keep them consistent
            blue_rot_dir = random.choice(["cw", "ccw"])
            red_rot_dir = random.choice(["cw", "ccw"])

            print(f"✅ Continuous rotation: blue={blue_rot_dir}, red={red_rot_dir}")
            return (blue_rot_dir, red_rot_dir)
        else:
            # Random prop continuity - return None to indicate random selection
            print("✅ Random rotation: blue=None, red=None")
            return (None, None)
