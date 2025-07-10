"""
Data Conversion Service

Pure business service for data conversions, position calculations, and caching utilities.
Moved from presentation layer to follow clean architecture principles.

This service handles:
- Position key extraction and parsing
- End position calculations with caching
- Sequence format conversions (Modern to Legacy)
- Cache management for performance optimization

No UI dependencies - completely testable in isolation.
"""

from typing import Any, Dict, List

from domain.models.beat_data import BeatData
from domain.models.enums import GridPosition, Location
from domain.models.sequence_models import SequenceData


class DataConversionService:
    """
    Pure business service for data conversion operations and caching.

    Responsibilities:
    - Position key extraction and parsing
    - End position calculations with caching
    - Sequence format conversions (Modern to Legacy)
    - Cache management for performance optimization
    """

    def __init__(self):
        # Performance optimization: Cache for position calculations
        self._position_cache = {}
        self._sequence_conversion_cache = {}

    def extract_end_position_from_position_key(self, position_key: str) -> str:
        """Extract the actual end position from a position key like 'beta5_beta5'"""
        # Position keys are in format "start_end", we want the end part
        if "_" in position_key:
            parts = position_key.split("_")
            if len(parts) == 2:
                return parts[1]  # Return the end position part

        # Fallback: if no underscore, assume it's already the position
        return position_key

    def get_cached_end_position(self, beat: BeatData) -> str:
        """Get end position with caching to eliminate redundant calculations"""
        # Create cache key from motion data
        blue_end = (
            beat.blue_motion.end_loc.value
            if beat.blue_motion and beat.blue_motion.end_loc
            else "s"
        )
        red_end = (
            beat.red_motion.end_loc.value
            if beat.red_motion and beat.red_motion.end_loc
            else "s"
        )

        cache_key = f"{blue_end}_{red_end}"

        # Check cache first
        if cache_key in self._position_cache:
            return self._position_cache[cache_key]

        # Calculate and cache the result using canonical positions map with proper enums
        # Based on f:\CODE\TKA\src\desktop\data\positions_maps.py
        position_map = {
            (Location.SOUTH, Location.NORTH): GridPosition.ALPHA1,
            (Location.SOUTHWEST, Location.NORTHEAST): GridPosition.ALPHA2,
            (Location.WEST, Location.EAST): GridPosition.ALPHA3,
            (Location.NORTHWEST, Location.SOUTHEAST): GridPosition.ALPHA4,
            (Location.NORTH, Location.SOUTH): GridPosition.ALPHA5,
            (Location.NORTHEAST, Location.SOUTHWEST): GridPosition.ALPHA6,
            (Location.EAST, Location.WEST): GridPosition.ALPHA7,
            (Location.SOUTHEAST, Location.NORTHWEST): GridPosition.ALPHA8,
            (Location.NORTH, Location.NORTH): GridPosition.BETA1,
            (Location.NORTHEAST, Location.NORTHEAST): GridPosition.BETA2,
            (Location.EAST, Location.EAST): GridPosition.BETA3,
            (Location.SOUTHEAST, Location.SOUTHEAST): GridPosition.BETA4,
            (Location.SOUTH, Location.SOUTH): GridPosition.BETA5,
            (Location.SOUTHWEST, Location.SOUTHWEST): GridPosition.BETA6,
            (Location.WEST, Location.WEST): GridPosition.BETA7,
            (Location.NORTHWEST, Location.NORTHWEST): GridPosition.BETA8,
            (Location.WEST, Location.NORTH): GridPosition.GAMMA1,
            (Location.NORTHWEST, Location.NORTHEAST): GridPosition.GAMMA2,
            (Location.NORTH, Location.EAST): GridPosition.GAMMA3,
            (Location.NORTHEAST, Location.SOUTHEAST): GridPosition.GAMMA4,
            (Location.EAST, Location.SOUTH): GridPosition.GAMMA5,
            (Location.SOUTHEAST, Location.SOUTHWEST): GridPosition.GAMMA6,
            (Location.SOUTH, Location.WEST): GridPosition.GAMMA7,
            (Location.SOUTHWEST, Location.NORTHWEST): GridPosition.GAMMA8,
            (Location.EAST, Location.NORTH): GridPosition.GAMMA9,
            (Location.SOUTHEAST, Location.NORTHEAST): GridPosition.GAMMA10,
            (Location.SOUTH, Location.EAST): GridPosition.GAMMA11,
            (Location.SOUTHWEST, Location.SOUTHEAST): GridPosition.GAMMA12,
            (Location.WEST, Location.SOUTH): GridPosition.GAMMA13,
            (Location.NORTHWEST, Location.SOUTHWEST): GridPosition.GAMMA14,
            (Location.NORTH, Location.WEST): GridPosition.GAMMA15,
            (Location.NORTHEAST, Location.NORTHWEST): GridPosition.GAMMA16,
        }

        # Convert string locations to Location enums for lookup
        try:
            blue_location = Location(blue_end)
            red_location = Location(red_end)
            position_enum = position_map.get(
                (blue_location, red_location), GridPosition.BETA5
            )
            end_pos = position_enum.value
        except ValueError:
            # Fallback if location strings don't match enum values
            end_pos = GridPosition.BETA5.value
        self._position_cache[cache_key] = end_pos
        return end_pos

    def convert_sequence_to_legacy_format(
        self, sequence: SequenceData
    ) -> List[Dict[str, Any]]:
        """Convert Modern SequenceData to Legacy-compatible format for option picker with caching"""
        # Create cache key from sequence hash
        sequence_hash = hash(
            tuple(beat.letter + str(beat.beat_number) for beat in sequence.beats)
        )

        # Check cache first
        if sequence_hash in self._sequence_conversion_cache:
            return self._sequence_conversion_cache[sequence_hash]

        try:
            # Start with metadata entry (Legacy format)
            legacy_sequence = [{"metadata": "sequence_info"}]

            # Convert each beat to Legacy format
            for beat in sequence.beats:
                if beat and not beat.is_blank:
                    beat_dict = beat.to_dict()

                    # Ensure Legacy-compatible structure
                    if "metadata" not in beat_dict:
                        beat_dict["metadata"] = {}

                    # CRITICAL FIX: Use end_pos from metadata if available, otherwise calculate
                    if "end_pos" not in beat_dict:
                        # First try to get end_pos from beat metadata
                        metadata_end_pos = (
                            beat.metadata.get("end_pos") if beat.metadata else None
                        )

                        if metadata_end_pos:
                            # Use the correct end position from metadata
                            beat_dict["end_pos"] = metadata_end_pos
                            print(
                                f"🎯 Using metadata end_pos: {metadata_end_pos} for beat {beat.letter}"
                            )
                        elif beat.blue_motion and beat.red_motion:
                            # Optimized: Use cached position calculation
                            end_pos = self.get_cached_end_position(beat)
                            beat_dict["end_pos"] = end_pos
                            print(
                                f"🎯 Cached end_pos: {end_pos} for beat {beat.letter} from motion data"
                            )
                        else:
                            # Final fallback
                            beat_dict["end_pos"] = "beta5"
                            print(
                                f"⚠️ Using fallback end_pos: beta5 for beat {beat.letter}"
                            )

                    legacy_sequence.append(beat_dict)

            # Cache the result for future use
            self._sequence_conversion_cache[sequence_hash] = legacy_sequence

            # Limit cache size to prevent memory issues
            if len(self._sequence_conversion_cache) > 100:
                # Remove oldest entries (simple FIFO)
                oldest_key = next(iter(self._sequence_conversion_cache))
                del self._sequence_conversion_cache[oldest_key]

            return legacy_sequence

        except Exception as e:
            print(f"❌ Error converting sequence to Legacy format: {e}")
            return [{"metadata": "sequence_info"}]  # Fallback to empty sequence

    def clear_caches(self):
        """Clear all caches to free memory"""
        self._position_cache.clear()
        self._sequence_conversion_cache.clear()
        print("🧹 Data conversion caches cleared")

    def get_cache_stats(self) -> Dict[str, int]:
        """Get statistics about cache usage"""
        return {
            "position_cache_size": len(self._position_cache),
            "sequence_conversion_cache_size": len(self._sequence_conversion_cache),
        }
