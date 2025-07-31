"""
Freeform Generation Service - Fixed Implementation

Provides the RotationDeterminer and other utilities that SequenceGenerator needs.
"""

import random
from typing import Optional, Tuple


class RotationDeterminer:
    """
    CRITICAL FIX: Provides rotation direction logic that SequenceGenerator expects.

    Direct port from legacy rotation determination logic.
    """

    @staticmethod
    def get_rotation_dirs(prop_continuity: str) -> Tuple[Optional[str], Optional[str]]:
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


# Additional utilities that might be needed
class PropContinuityManager:
    """Manages prop rotation continuity logic."""

    @staticmethod
    def is_continuous(prop_continuity: str) -> bool:
        """Check if prop continuity is continuous."""
        return prop_continuity == "continuous"

    @staticmethod
    def should_apply_rotation_filter(prop_continuity: str) -> bool:
        """Check if rotation filtering should be applied."""
        return prop_continuity == "continuous"


class LetterTypeMapper:
    """Maps letter types to actual letters."""

    LETTER_TYPE_MAPPINGS = {
        "Type1": [
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
        ],
        "Type2": ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"],
        "Type3": ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"],
        "Type4": ["Φ", "Ψ", "Λ"],
        "Type5": ["Φ-", "Ψ-", "Λ-"],
        "Type6": ["α", "β", "Γ"],
    }

    @staticmethod
    def get_letters_for_types(letter_types: list) -> list:
        """Get all letters for the given letter types."""
        letters = []
        for letter_type in letter_types:
            if isinstance(letter_type, str):
                letters.extend(
                    LetterTypeMapper.LETTER_TYPE_MAPPINGS.get(letter_type, [])
                )
            elif hasattr(letter_type, "value"):
                letters.extend(
                    LetterTypeMapper.LETTER_TYPE_MAPPINGS.get(letter_type.value, [])
                )
        return list(set(letters))  # Remove duplicates
