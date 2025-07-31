"""
Orientation Calculator Service

Direct port of legacy orientation calculation logic.
Critical for ensuring beats flow correctly together.
"""

from typing import Any


class OrientationCalculationService:
    """
    CRITICAL FIX: Orientation calculation service that SequenceGenerator needs.

    Direct port of legacy orientation calculation logic.
    Essential for sequence beat flow correctness.
    """

    def calculate_end_ori(self, beat_data: dict[str, Any], color: str) -> str:
        """
        Calculate end orientation for a beat and color.

        This is the main method that legacy system uses.

        Args:
            beat_data: Beat data dictionary in legacy format
            color: "blue" or "red"

        Returns:
            End orientation string ("in", "out", "clock", "counter")
        """
        print(f"🔧 Calculating end orientation for {color}")

        # Get color attributes
        if color.lower() == "blue":
            attrs = beat_data.get("blue_attributes", {})
        elif color.lower() == "red":
            attrs = beat_data.get("red_attributes", {})
        else:
            raise ValueError(f"Invalid color: {color}")

        motion_type = attrs.get("motion_type", "static")
        start_ori = attrs.get("start_ori", "in")
        prop_rot_dir = attrs.get("prop_rot_dir", "cw")
        turns = attrs.get("turns", 0)
        start_loc = attrs.get("start_loc", "n")
        end_loc = attrs.get("end_loc", "n")

        print(
            f"  Motion: {motion_type}, Start: {start_ori}, Rot: {prop_rot_dir}, Turns: {turns}"
        )

        # Calculate based on motion type (exact legacy logic)
        if motion_type == "static":
            end_ori = start_ori  # Static preserves orientation

        elif motion_type == "dash":
            end_ori = self._calculate_dash_end_orientation(
                start_ori, prop_rot_dir, turns, start_loc, end_loc
            )

        elif motion_type == "pro":
            end_ori = self._calculate_pro_end_orientation(
                start_ori, prop_rot_dir, turns, start_loc, end_loc
            )

        elif motion_type == "anti":
            end_ori = self._calculate_anti_end_orientation(
                start_ori, prop_rot_dir, turns, start_loc, end_loc
            )

        elif motion_type == "float":
            end_ori = self._calculate_float_end_orientation(
                start_ori, prop_rot_dir, turns, start_loc, end_loc
            )

        else:
            # Unknown motion type - preserve start orientation
            end_ori = start_ori
            print(f"⚠️ Unknown motion type: {motion_type}, preserving start orientation")

        print(f"✅ Calculated end orientation: {end_ori}")
        return end_ori

    def _calculate_dash_end_orientation(
        self,
        start_ori: str,
        prop_rot_dir: str,
        turns: float,
        start_loc: str,
        end_loc: str,
    ) -> str:
        """Calculate end orientation for dash motion."""
        # Dash logic from legacy system
        if turns == 0:
            return start_ori  # No turns, preserve orientation

        # With turns, orientation flips based on prop rotation
        if prop_rot_dir == "cw":
            return self._flip_orientation(start_ori)
        elif prop_rot_dir == "ccw":
            return self._flip_orientation_ccw(start_ori)
        else:
            return start_ori

    def _calculate_pro_end_orientation(
        self,
        start_ori: str,
        prop_rot_dir: str,
        turns: float,
        start_loc: str,
        end_loc: str,
    ) -> str:
        """Calculate end orientation for pro motion."""
        # Pro motion logic - orientation typically flips
        base_flip = self._flip_orientation(start_ori)

        # Apply turn effects
        if turns > 0:
            if prop_rot_dir == "cw":
                return base_flip
            elif prop_rot_dir == "ccw":
                return self._flip_orientation(base_flip)

        return base_flip

    def _calculate_anti_end_orientation(
        self,
        start_ori: str,
        prop_rot_dir: str,
        turns: float,
        start_loc: str,
        end_loc: str,
    ) -> str:
        """Calculate end orientation for anti motion."""
        # Anti motion logic - similar to pro but different
        base_flip = self._flip_orientation_ccw(start_ori)

        # Apply turn effects
        if turns > 0:
            if prop_rot_dir == "cw":
                return self._flip_orientation(base_flip)
            elif prop_rot_dir == "ccw":
                return base_flip

        return base_flip

    def _calculate_float_end_orientation(
        self,
        start_ori: str,
        prop_rot_dir: str,
        turns: float,
        start_loc: str,
        end_loc: str,
    ) -> str:
        """Calculate end orientation for float motion."""
        # Float motion preserves orientation (no prop rotation during float)
        return start_ori

    def _flip_orientation(self, orientation: str) -> str:
        """Flip orientation clockwise."""
        flip_map = {"in": "out", "out": "in", "clock": "counter", "counter": "clock"}
        return flip_map.get(orientation, orientation)

    def _flip_orientation_ccw(self, orientation: str) -> str:
        """Flip orientation counter-clockwise."""
        flip_map = {"in": "out", "out": "in", "clock": "counter", "counter": "clock"}
        return flip_map.get(orientation, orientation)

    def validate_orientation_continuity(
        self, previous_beat: dict[str, Any], next_beat: dict[str, Any], color: str
    ) -> bool:
        """
        Validate that orientations flow correctly between beats.

        CRITICAL: This ensures sequence beat flow is correct.
        """
        if color.lower() == "blue":
            prev_end = previous_beat.get("blue_attributes", {}).get("end_ori")
            next_start = next_beat.get("blue_attributes", {}).get("start_ori")
        elif color.lower() == "red":
            prev_end = previous_beat.get("red_attributes", {}).get("end_ori")
            next_start = next_beat.get("red_attributes", {}).get("start_ori")
        else:
            return False

        is_continuous = prev_end == next_start
        if not is_continuous:
            print(f"⚠️ Orientation discontinuity in {color}: {prev_end} -> {next_start}")

        return is_continuous


# Global instance for easy access (matches legacy pattern)
orientation_calculator = OrientationCalculationService()
