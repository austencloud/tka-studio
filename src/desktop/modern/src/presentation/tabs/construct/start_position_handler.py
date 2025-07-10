"""
StartPositionHandler

Manages start position selection, data creation, and related operations for the construct tab.
Responsible for handling start position picker interactions and creating start position data.
"""

from typing import Callable, Optional

from application.services.data.data_conversion_service import DataConversionService
from application.services.data.sequence_data_converter import SequenceDataConverter
from domain.models.beat_data import BeatData
from domain.models.pictograph_models import PictographData
from PyQt6.QtCore import QObject, pyqtSignal


class StartPositionHandler(QObject):
    """
    Handles start position selection and data creation.

    Responsibilities:
    - Processing start position selection events
    - Creating start position data from position keys
    - Managing start position to option picker transitions
    - Integrating with the pictograph dataset service

    Signals:
    - start_position_created: Emitted when start position data is created
    - transition_requested: Emitted when transition to option picker is needed
    """

    start_position_created = pyqtSignal(str, object)  # position_key, PictographData
    transition_requested = pyqtSignal()  # Request transition to option picker

    def __init__(
        self,
        data_conversion_service: DataConversionService,
        workbench_setter: Optional[Callable[[PictographData], None]] = None,
    ):
        super().__init__()
        self.data_conversion_service = data_conversion_service
        self.workbench_setter = workbench_setter

    def handle_start_position_selected(self, position_key: str):
        """Handle start position selection from the picker"""
        # Removed repetitive debug logs
        print(f"✅ Start position handler: Position selected: {position_key}")

        # Create start position data (separate from sequence like Legacy)
        # Removed repetitive debug logs
        start_position_data = self._create_start_position_data(position_key)
        print(
            f"✅ [START_POS_HANDLER] Created start position data: {start_position_data.letter if start_position_data else 'None'}"
        )

        # Set start position in workbench (this does NOT create a sequence)
        if self.workbench_setter:
            # Convert PictographData to BeatData for sequence workbench context
            beat_data = self._convert_pictograph_to_beat_data(start_position_data)
            self.workbench_setter(beat_data)
            print(f"✅ [START_POS_HANDLER] Set in workbench as BeatData")
        else:
            print(f"⚠️ [START_POS_HANDLER] No workbench setter available")

        # Emit signal with the created data
        # Removed repetitive debug logs
        self.start_position_created.emit(position_key, start_position_data)
        print(f"✅ [START_POS_HANDLER] start_position_created signal emitted")

        # Request transition to option picker
        # Removed repetitive debug logs
        self.transition_requested.emit()
        print(f"✅ [START_POS_HANDLER] transition_requested signal emitted")

    def _create_start_position_data(self, position_key: str) -> PictographData:
        """Create start position data from position key using real dataset (separate from sequence beats)"""
        try:
            from application.services.data.dataset_quiry import DatasetQuery

            dataset_service = DatasetQuery()
            # Get real start position data from dataset as PictographData
            real_start_position_pictograph = (
                dataset_service.get_start_position_pictograph_data(
                    position_key, "diamond"
                )
            )

            if real_start_position_pictograph:
                # Extract the specific end position from position_key (like "gamma13")
                specific_end_pos = (
                    self.data_conversion_service.extract_end_position_from_position_key(
                        position_key
                    )
                )

                # Update the pictograph data with correct position information
                pictograph_data = real_start_position_pictograph.update(
                    start_position=position_key,
                    end_position=specific_end_pos,
                    metadata={"source": "start_position_selection"},
                )

                print(
                    f"🎯 Created start position data: {position_key} -> {specific_end_pos}"
                )
                return pictograph_data
            else:
                print(
                    f"⚠️ No real data found for position {position_key}, using fallback"
                )
                # Fallback start position as PictographData
                specific_end_pos = (
                    self.data_conversion_service.extract_end_position_from_position_key(
                        position_key
                    )
                )

                return self._create_fallback_pictograph_data(
                    position_key, specific_end_pos
                )

        except Exception as e:
            print(f"❌ Error loading real start position data: {e}")
            import traceback

            traceback.print_exc()

            # Fallback to basic pictograph data with position info
            try:
                specific_end_pos = (
                    self.data_conversion_service.extract_end_position_from_position_key(
                        position_key
                    )
                )
            except Exception:
                specific_end_pos = position_key  # Last resort fallback

            return self._create_fallback_pictograph_data(position_key, specific_end_pos)

    def _create_fallback_pictograph_data(
        self, position_key: str, specific_end_pos: str
    ) -> PictographData:
        """Create fallback PictographData when dataset lookup fails."""
        from domain.models.pictograph_models import GridData

        return PictographData(
            letter=position_key,
            start_position=position_key,
            end_position=specific_end_pos,
            grid_data=GridData(),  # Default grid data
            arrows={},  # Empty arrows for fallback
            props={},  # Empty props for fallback
            is_blank=False,
            metadata={"source": "fallback_start_position"},
        )

    def _convert_pictograph_to_beat_data(
        self, pictograph_data: PictographData
    ) -> BeatData:
        """Convert PictographData to BeatData for sequence workbench context.

        This creates a proper start position beat with:
        - beat_number = 0 (indicates it occurs before the sequence begins)
        - duration = 0 (not held for any time, just a visual reference point)
        """
        from domain.models.enums import (
            Location,
            MotionType,
            Orientation,
            RotationDirection,
        )
        from domain.models.glyph_models import GlyphData
        from domain.models.motion_models import MotionData

        # Extract motion data from arrows
        blue_motion = None
        red_motion = None

        if pictograph_data.arrows:
            if "blue" in pictograph_data.arrows:
                arrow = pictograph_data.arrows["blue"]
                blue_motion = MotionData(
                    motion_type=getattr(arrow, "motion_type", MotionType.STATIC),
                    prop_rot_dir=RotationDirection.CLOCKWISE,  # Default for start positions
                    start_loc=getattr(arrow, "location", None) or Location.NORTH,
                    start_ori=getattr(arrow, "orientation", None) or Orientation.IN,
                    end_loc=getattr(arrow, "location", None)
                    or Location.NORTH,  # For start positions, end = start
                    end_ori=getattr(arrow, "orientation", None) or Orientation.IN,
                    turns=0.0,  # Start positions have no turns
                )

            if "red" in pictograph_data.arrows:
                arrow = pictograph_data.arrows["red"]
                red_motion = MotionData(
                    motion_type=getattr(arrow, "motion_type", MotionType.STATIC),
                    prop_rot_dir=RotationDirection.CLOCKWISE,  # Default for start positions
                    start_loc=getattr(arrow, "location", None) or Location.NORTH,
                    start_ori=getattr(arrow, "orientation", None) or Orientation.IN,
                    end_loc=getattr(arrow, "location", None)
                    or Location.NORTH,  # For start positions, end = start
                    end_ori=getattr(arrow, "orientation", None) or Orientation.IN,
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
            duration=0.0,  # Start position has no duration (not held for any time)
            blue_motion=blue_motion,
            red_motion=red_motion,
            glyph_data=glyph_data,
            is_blank=pictograph_data.is_blank,
            metadata=metadata,
        )
