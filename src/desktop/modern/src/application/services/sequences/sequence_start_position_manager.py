"""
SequenceStartPositionManager

Handles start position operations and management.
Responsible for setting, updating, and managing start positions in sequences.
"""

from typing import Callable, Optional

from application.services.data.sequence_data_converter import SequenceDataConverter
from application.services.sequences.sequence_persistence_service import (
    SequencePersistenceService,
)
from domain.models.beat_data import BeatData
from domain.models.pictograph_models import PictographData
from domain.models.sequence_models import SequenceData
from PyQt6.QtCore import QObject, pyqtSignal


class SequenceStartPositionManager(QObject):
    """
    Service for managing start positions in sequences.

    Responsibilities:
    - Setting start positions
    - Converting start position data to legacy format
    - Managing start position persistence
    - Coordinating start position with workbench
    """

    start_position_set = pyqtSignal(object)  # BeatData object
    start_position_updated = pyqtSignal(object)  # BeatData object

    def __init__(
        self,
        workbench_getter: Optional[Callable[[], object]] = None,
        workbench_setter: Optional[Callable[[SequenceData], None]] = None,
        data_converter: SequenceDataConverter = None,
    ):
        super().__init__()
        self.workbench_getter = workbench_getter
        self.workbench_setter = workbench_setter
        self.data_converter = data_converter
        self.persistence_service = SequencePersistenceService()

    def set_start_position(self, start_position_data):
        """Set the start position - accepts both PictographData and BeatData"""
        # Convert PictographData to BeatData if needed for sequence operations
        if isinstance(start_position_data, PictographData):
            print(
                f"🔄 [START_POS_MGR] Converting PictographData to BeatData for sequence operations"
            )
            beat_data = self._convert_pictograph_to_beat_data(start_position_data)
        else:
            beat_data = start_position_data

        print(
            f"🔄 [START_POS_MGR] set_start_position called with: {beat_data.letter if beat_data else 'None'}"
        )

        try:
            if not self.data_converter:
                print(
                    "❌ [START_POS_MGR] No data converter available for start position"
                )
                return

            print(
                f"✅ [START_POS_MGR] Data converter available: {type(self.data_converter)}"
            )

            # Convert start position to legacy format and save as beat 0
            print(f"🔄 [START_POS_MGR] Converting start position to legacy format...")
            start_pos_dict = (
                self.data_converter.convert_start_position_to_legacy_format(beat_data)
            )
            print(f"✅ [START_POS_MGR] Converted to legacy format: {start_pos_dict}")

            # Load current sequence to preserve existing beats
            print(f"🔄 [START_POS_MGR] Loading current sequence...")
            sequence = self.persistence_service.load_current_sequence()
            print(f"✅ [START_POS_MGR] Loaded sequence with {len(sequence)} items")

            # Find where to insert/replace start position
            if len(sequence) == 1:  # Only metadata
                sequence.append(start_pos_dict)
                print(f"✅ [START_POS_MGR] Inserted start position as beat 0")
            elif len(sequence) > 1 and sequence[1].get("beat") == 0:
                # Replace existing start position
                sequence[1] = start_pos_dict
                print(f"✅ [START_POS_MGR] Replaced existing start position")
            else:
                # Insert start position, shifting existing beats
                sequence.insert(1, start_pos_dict)
                print(
                    f"✅ [START_POS_MGR] Inserted start position, preserving {len(sequence) - 2} existing beats"
                )

            # Save updated sequence (preserves existing beats)
            print(
                f"🔄 [START_POS_MGR] Saving updated sequence with {len(sequence)} items..."
            )
            self.persistence_service.save_current_sequence(sequence)
            print(f"✅ [START_POS_MGR] Sequence saved successfully!")

            # Set start position in workbench
            workbench = self.workbench_getter() if self.workbench_getter else None
            if workbench and hasattr(workbench, "set_start_position"):
                workbench.set_start_position(beat_data)
                print(
                    f"✅ [START_POS_MGR] Start position set in workbench: {beat_data.letter}"
                )
            else:
                print(
                    f"⚠️ [START_POS_MGR] No workbench available or no set_start_position method"
                )

            # Emit signal
            self.start_position_set.emit(beat_data)
            print(
                f"✅ [START_POS_MGR] Signal emitted for start position: {beat_data.letter}"
            )

            print(f"✅ [START_POS_MGR] Set start position complete: {beat_data.letter}")

        except Exception as e:
            print(f"❌ [START_POS_MGR] Failed to set start position: {e}")
            import traceback

            traceback.print_exc()

    def update_start_position_orientation(self, color: str, new_orientation: int):
        """Update start position orientation for a specific color"""
        try:
            workbench = self.workbench_getter()
            if not workbench or not hasattr(workbench, "_start_position_data"):
                print("⚠️ No start position data available in workbench")
                return

            start_position_data = workbench._start_position_data
            if not start_position_data:
                print("⚠️ No start position data to update")
                return

            # Update the appropriate motion based on color
            if color.lower() == "blue" and start_position_data.blue_motion:
                updated_motion = start_position_data.blue_motion.update(
                    start_orientation=new_orientation, end_orientation=new_orientation
                )
                updated_start_position = start_position_data.update(
                    blue_motion=updated_motion
                )
            elif color.lower() == "red" and start_position_data.red_motion:
                updated_motion = start_position_data.red_motion.update(
                    start_orientation=new_orientation, end_orientation=new_orientation
                )
                updated_start_position = start_position_data.update(
                    red_motion=updated_motion
                )
            else:
                print(f"⚠️ Invalid color '{color}' or missing motion data")
                return

            # Update workbench
            if hasattr(workbench, "set_start_position"):
                workbench.set_start_position(updated_start_position)

            # Update persistence
            self._update_start_position_in_persistence(updated_start_position)

            # Emit signal
            self.start_position_updated.emit(updated_start_position)

            print(f"✅ Updated start position {color} orientation to {new_orientation}")

        except Exception as e:
            print(f"❌ Failed to update start position orientation: {e}")
            import traceback

            traceback.print_exc()

    def get_current_start_position(self) -> Optional[BeatData]:
        """Get the current start position from workbench"""
        try:
            workbench = self.workbench_getter()
            if workbench and hasattr(workbench, "_start_position_data"):
                return workbench._start_position_data
        except Exception as e:
            print(f"❌ Error getting current start position: {e}")
        return None

    def clear_start_position(self):
        """Clear the current start position"""
        try:
            print("🔄 [START_POS_MGR] Clearing start position...")

            # Clear from workbench
            workbench = self.workbench_getter()
            if workbench and hasattr(workbench, "_start_position_data"):
                workbench._start_position_data = None
                print("✅ [START_POS_MGR] Cleared from workbench")

                # Clear from beat frame if available
                if hasattr(workbench, "_beat_frame_section"):
                    beat_frame_section = workbench._beat_frame_section
                    if beat_frame_section and hasattr(
                        beat_frame_section, "initialize_cleared_start_position"
                    ):
                        beat_frame_section.initialize_cleared_start_position()
                        print("✅ [START_POS_MGR] Cleared from beat frame")

            # Clear from persistence (only if sequence exists and has start position)
            sequence = self.persistence_service.load_current_sequence()
            if len(sequence) > 1 and sequence[1].get("beat") == 0:
                # Remove start position entry
                sequence.pop(1)
                self.persistence_service.save_current_sequence(sequence)
                print("✅ [START_POS_MGR] Cleared start position from persistence")
            else:
                print("ℹ️ [START_POS_MGR] No start position in persistence to clear")

            print("✅ [START_POS_MGR] Start position cleared")

        except Exception as e:
            print(f"❌ [START_POS_MGR] Failed to clear start position: {e}")
            import traceback

            traceback.print_exc()

    def _update_start_position_in_persistence(self, start_position_data: BeatData):
        """Update start position in persistence"""
        try:
            if not self.data_converter:
                print("⚠️ No data converter available for persistence update")
                return

            # Convert to legacy format
            start_pos_dict = (
                self.data_converter.convert_start_position_to_legacy_format(
                    start_position_data
                )
            )

            # Load current sequence
            sequence = self.persistence_service.load_current_sequence()

            # Update start position if it exists
            if len(sequence) > 1 and sequence[1].get("beat") == 0:
                sequence[1] = start_pos_dict
                self.persistence_service.save_current_sequence(sequence)
                print("✅ Updated start position in persistence")
            else:
                print("⚠️ No start position found in persistence to update")

        except Exception as e:
            print(f"❌ Failed to update start position in persistence: {e}")
            import traceback

            traceback.print_exc()

    def load_start_position_from_persistence(self) -> Optional[BeatData]:
        """Load start position from persistence if it exists"""
        try:
            sequence_data = self.persistence_service.load_current_sequence()

            # Look for start position (beat 0)
            for item in sequence_data[1:]:  # Skip metadata
                if item.get("beat") == 0:
                    if self.data_converter:
                        start_position_beat = self.data_converter.convert_legacy_start_position_to_beat_data(
                            item
                        )
                        print(
                            f"✅ Loaded start position from persistence: {item.get('sequence_start_position', 'unknown')}"
                        )
                        return start_position_beat
                    else:
                        print(
                            "⚠️ No data converter available for start position loading"
                        )
                        return None

            print("ℹ️ No start position found in persistence")
            return None

        except Exception as e:
            print(f"❌ Failed to load start position from persistence: {e}")
            import traceback

            traceback.print_exc()
            return None

    def has_start_position(self) -> bool:
        """Check if a start position is currently set"""
        try:
            workbench = self.workbench_getter()
            if workbench and hasattr(workbench, "_start_position_data"):
                return workbench._start_position_data is not None
        except Exception as e:
            print(f"❌ Error checking start position: {e}")
        return False

    def _convert_pictograph_to_beat_data(
        self, pictograph_data: PictographData
    ) -> BeatData:
        """Convert PictographData to BeatData for sequence operations."""
        from domain.models.glyph_models import GlyphData
        from domain.models.motion_models import MotionData

        # Extract motion data from arrows
        blue_motion = None
        red_motion = None

        if pictograph_data.arrows:
            if "blue" in pictograph_data.arrows:
                arrow = pictograph_data.arrows["blue"]
                from domain.models.enums import (
                    Location,
                    MotionType,
                    Orientation,
                    RotationDirection,
                )

                blue_motion = MotionData(
                    motion_type=getattr(arrow, "motion_type", MotionType.STATIC),
                    prop_rot_dir=RotationDirection.CLOCKWISE,  # Default for start positions
                    start_loc=getattr(arrow, "location", Location.NORTH),
                    start_ori=getattr(arrow, "orientation", Orientation.IN),
                    end_loc=getattr(
                        arrow, "location", Location.NORTH
                    ),  # For start positions, end = start
                    end_ori=getattr(arrow, "orientation", Orientation.IN),
                    turns=0.0,  # Start positions have no turns
                )

            if "red" in pictograph_data.arrows:
                arrow = pictograph_data.arrows["red"]
                from domain.models.enums import (
                    Location,
                    MotionType,
                    Orientation,
                    RotationDirection,
                )

                red_motion = MotionData(
                    motion_type=getattr(arrow, "motion_type", MotionType.STATIC),
                    prop_rot_dir=RotationDirection.CLOCKWISE,  # Default for start positions
                    start_loc=getattr(arrow, "location", Location.NORTH),
                    start_ori=getattr(arrow, "orientation", Orientation.IN),
                    end_loc=getattr(
                        arrow, "location", Location.NORTH
                    ),  # For start positions, end = start
                    end_ori=getattr(arrow, "orientation", Orientation.IN),
                    turns=0.0,  # Start positions have no turns
                )

        # Create glyph data
        glyph_data = GlyphData(
            start_position=pictograph_data.start_position,
            end_position=pictograph_data.end_position,
        )

        # Ensure metadata includes start position flag
        metadata = pictograph_data.metadata or {}
        metadata["is_start_position"] = True

        return BeatData(
            letter=pictograph_data.letter,
            beat_number=0,  # Start position is beat 0
            duration=1.0,
            blue_motion=blue_motion,
            red_motion=red_motion,
            glyph_data=glyph_data,
            is_blank=pictograph_data.is_blank,
            metadata=metadata,
        )
