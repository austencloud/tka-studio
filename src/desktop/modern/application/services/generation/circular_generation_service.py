"""
Circular Generation Service - MODERN ARCHITECTURE

Implements circular sequence generation using modern TKA architecture.
NO MOCKS, NO LEGACY INTEGRATION - Pure modern implementation with real CAP transformations.
"""

import logging
import random
from copy import deepcopy
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from data.mappers.pictograph_mappers import PictographDataMapper
from desktop.modern.core.interfaces.generation_services import (
    CAPType,
    SliceSize,
    PropContinuity,
)
from desktop.modern.domain.models.generation_models import GenerationConfig
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.motion_data import MotionData
from desktop.modern.domain.models.enums import (
    MotionType, RotationDirection, Location, Orientation, GridPosition
)
from .base_sequence_builder import BaseSequenceBuilder
from .turn_intensity_manager import TurnIntensityManager

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class CircularGenerationService(BaseSequenceBuilder):
    """
    Modern circular sequence generation service.
    
    Generates sequences using circular arrangement patterns (CAP) with
    real TKA pictograph data and modern transformation algorithms.
    """

    def __init__(self, container: "DIContainer"):
        super().__init__(container)
        
        # Initialize real pictograph data loader
        self.pictograph_mapper = PictographDataMapper(self._get_data_path())
        self.pictograph_options: List[Dict[str, Any]] = []
        
        # Position transformation mappings for CAP operations
        self.position_mappings = self._initialize_position_mappings()
        
        # Load real pictograph data
        self._load_real_pictograph_data()
        
        logger.info(f"✅ Circular generation service initialized with {len(self.pictograph_options)} real pictographs")

    def _get_data_path(self) -> str:
        """Get the path to the data directory."""
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(current_dir, "..", "..", "..", "..", "..", "data")
        return os.path.abspath(data_path)

    def _load_real_pictograph_data(self) -> None:
        """Load real pictograph data from CSV files."""
        try:
            # Load diamond pictograph data (default for circular)
            diamond_data = self.pictograph_mapper.get_diamond_pictograph_data()
            
            if not diamond_data:
                diamond_data = self.pictograph_mapper.get_box_pictograph_data()
            
            if not diamond_data:
                raise RuntimeError("No pictograph data found in CSV files")
            
            self.pictograph_options = diamond_data
            logger.info(f"✅ Loaded {len(self.pictograph_options)} pictographs for circular generation")
            
        except Exception as e:
            logger.error(f"❌ Failed to load real pictograph data: {e}")
            raise RuntimeError(f"Cannot initialize circular generation without real pictograph data: {e}")

    def _initialize_position_mappings(self) -> Dict[str, Dict[str, str]]:
        """Initialize position transformation mappings for CAP operations."""
        # Real position mappings based on TKA grid system
        return {
            "swapped": {
                "alpha1": "alpha2", "alpha2": "alpha1",
                "alpha3": "alpha4", "alpha4": "alpha3", 
                "alpha5": "alpha6", "alpha6": "alpha5",
                "alpha7": "alpha8", "alpha8": "alpha7",
                "beta1": "beta2", "beta2": "beta1",
                "beta3": "beta4", "beta4": "beta3",
                "beta5": "beta6", "beta6": "beta5",
                "beta7": "beta8", "beta8": "beta7",
                "gamma1": "gamma2", "gamma2": "gamma1",
                "gamma3": "gamma4", "gamma4": "gamma3",
                "gamma5": "gamma6", "gamma6": "gamma5",
                "gamma7": "gamma8", "gamma8": "gamma7",
                "gamma9": "gamma10", "gamma10": "gamma9",
                "gamma11": "gamma12", "gamma12": "gamma11",
            },
            "mirrored": {
                # Vertical mirror transformations
                "alpha1": "alpha1", "alpha2": "alpha2",
                "alpha3": "alpha7", "alpha7": "alpha3",
                "alpha4": "alpha8", "alpha8": "alpha4", 
                "alpha5": "alpha5", "alpha6": "alpha6",
                "beta1": "beta7", "beta7": "beta1",
                "beta2": "beta8", "beta8": "beta2",
                "beta3": "beta3", "beta4": "beta4",
                "beta5": "beta5", "beta6": "beta6",
                "gamma1": "gamma11", "gamma11": "gamma1",
                "gamma2": "gamma12", "gamma12": "gamma2",
                "gamma3": "gamma9", "gamma9": "gamma3",
                "gamma4": "gamma10", "gamma10": "gamma4",
                "gamma5": "gamma7", "gamma7": "gamma5",
                "gamma6": "gamma8", "gamma8": "gamma6",
            },
            "rotated": {
                # 180-degree rotation transformations
                "alpha1": "alpha5", "alpha5": "alpha1",
                "alpha2": "alpha6", "alpha6": "alpha2",
                "alpha3": "alpha7", "alpha7": "alpha3",
                "alpha4": "alpha8", "alpha8": "alpha4",
                "beta1": "beta5", "beta5": "beta1",
                "beta2": "beta6", "beta6": "beta2", 
                "beta3": "beta7", "beta7": "beta3",
                "beta4": "beta8", "beta8": "beta4",
                "gamma1": "gamma7", "gamma7": "gamma1",
                "gamma2": "gamma8", "gamma8": "gamma2",
                "gamma3": "gamma9", "gamma9": "gamma3",
                "gamma4": "gamma10", "gamma10": "gamma4",
                "gamma5": "gamma11", "gamma11": "gamma5",
                "gamma6": "gamma12", "gamma12": "gamma6",
            }
        }

    def generate_sequence(self, config: GenerationConfig) -> List[Dict[str, Any]]:
        """
        Generate a circular sequence using modern architecture and real CAP transformations.
        
        Args:
            config: Generation configuration including CAP type and slice size
            
        Returns:
            List of generated pictograph data
        """
        logger.info(f"🎯 Starting modern circular generation: length={config.length}, CAP={config.cap_type}")
        
        # Initialize sequence
        self.initialize_sequence(config.length, config)
        
        # Determine prop rotation directions for continuous mode
        blue_rot_dir = None
        red_rot_dir = None
        
        if config.prop_continuity == PropContinuity.CONTINUOUS:
            blue_rot_dir = random.choice([RotationDirection.CLOCKWISE, RotationDirection.COUNTER_CLOCKWISE])
            red_rot_dir = random.choice([RotationDirection.CLOCKWISE, RotationDirection.COUNTER_CLOCKWISE])
        
        # Calculate word length based on CAP type and slice size
        word_length = self._calculate_word_length(config.length, config.slice_size, config.cap_type)
        
        logger.info(f"Calculated word length: {word_length} for total length: {config.length}")
        
        # Generate base pattern using real data
        base_pattern = self._generate_base_pattern(
            word_length, config, blue_rot_dir, red_rot_dir
        )
        
        logger.info(f"Generated base pattern with {len(base_pattern)} beats")
        
        # Apply real CAP transformations
        full_pattern = self._apply_real_cap_transformations(
            base_pattern, config.cap_type, config.slice_size
        )
        
        logger.info(f"Applied CAP transformations, full pattern: {len(full_pattern)} beats")
        
        # Add beats to modern workbench one by one
        generated_beats = []
        for i, pictograph_data in enumerate(full_pattern[:config.length]):
            try:
                # Update beat number
                updated_pictograph = pictograph_data.update(beat=i + 1)
                generated_beats.append(updated_pictograph)
                
                # Add to workbench for visual feedback
                self.add_beat_to_modern_workbench(updated_pictograph)
                
                # Process events to show beat appearing
                self._process_events()
                
                logger.info(f"✅ Added circular beat {i+1}: {updated_pictograph.letter}")
                
            except Exception as e:
                logger.error(f"❌ Failed to add circular beat {i}: {e}")
                continue
        
        logger.info(f"🎉 Generated circular sequence with {len(generated_beats)} beats")
        return generated_beats

    def _calculate_word_length(self, total_length: int, slice_size: SliceSize, cap_type: CAPType) -> int:
        """Calculate the word length based on total length, slice size, and CAP type."""
        
        # Base word length calculation
        if slice_size == SliceSize.QUARTERED:
            base_word_length = max(1, total_length // 4)
        else:  # HALVED
            base_word_length = max(1, total_length // 2)
        
        # Adjust for CAP types that need special handling
        if cap_type in [CAPType.MIRRORED_ROTATED, CAPType.MIRRORED_COMPLEMENTARY_ROTATED]:
            # These CAP types apply both mirroring and rotation, so need even smaller base
            base_word_length = max(1, base_word_length // 2)
        
        return base_word_length

    def _generate_base_pattern(
        self,
        word_length: int,
        config: GenerationConfig,
        blue_rot_dir: Optional[RotationDirection],
        red_rot_dir: Optional[RotationDirection],
    ) -> List[PictographData]:
        """Generate the base pattern using real pictograph data."""
        
        base_pattern = []
        
        # Allocate turns for the base pattern
        turn_manager = TurnIntensityManager(
            word_length=word_length,
            level=config.level,
            max_turn_intensity=config.turn_intensity
        )
        turns_blue, turns_red = turn_manager.allocate_turns_for_blue_and_red()
        
        # Generate each beat in the base pattern
        for i in range(word_length):
            try:
                # Get filtered options for this beat
                available_options = self._get_filtered_circular_options(
                    config, blue_rot_dir, red_rot_dir, base_pattern
                )
                
                if not available_options:
                    logger.warning(f"No options available for beat {i}, using any available")
                    available_options = self.pictograph_options
                
                # Select random option
                selected_option = random.choice(available_options)
                
                # Convert to modern pictograph data
                pictograph_data = self._convert_csv_to_modern_pictograph(selected_option, i + 1)
                
                # Apply turns for levels 2 and 3
                if config.level >= 2:
                    pictograph_data = self._apply_turns_to_pictograph(
                        pictograph_data, turns_blue[i], turns_red[i]
                    )
                
                base_pattern.append(pictograph_data)
                
            except Exception as e:
                logger.error(f"Failed to generate base pattern beat {i}: {e}")
                continue
        
        return base_pattern

    def _get_filtered_circular_options(
        self,
        config: GenerationConfig,
        blue_rot_dir: Optional[RotationDirection],
        red_rot_dir: Optional[RotationDirection],
        current_pattern: List[PictographData]
    ) -> List[Dict[str, Any]]:
        """Get filtered options for circular generation."""
        
        options = deepcopy(self.pictograph_options)
        
        # Filter by rotation continuity if specified
        if config.prop_continuity == PropContinuity.CONTINUOUS and (blue_rot_dir or red_rot_dir):
            options = self._filter_by_rotation_continuity(options, blue_rot_dir, red_rot_dir)
        
        # For the last beat in the pattern, filter by expected end position (if implementing)
        # This would require more complex position matching logic
        
        return options

    def _filter_by_rotation_continuity(
        self,
        options: List[Dict[str, Any]], 
        blue_rot_dir: Optional[RotationDirection], 
        red_rot_dir: Optional[RotationDirection]
    ) -> List[Dict[str, Any]]:
        """Filter options by rotation continuity."""
        
        filtered = []
        for opt in options:
            blue_matches = (
                not blue_rot_dir or 
                opt.get('blue_prop_rot_dir', '') == blue_rot_dir.value or
                opt.get('blue_prop_rot_dir', '') == 'no_rot'
            )
            red_matches = (
                not red_rot_dir or 
                opt.get('red_prop_rot_dir', '') == red_rot_dir.value or
                opt.get('red_prop_rot_dir', '') == 'no_rot'
            )
            
            if blue_matches and red_matches:
                filtered.append(opt)
        
        return filtered if filtered else options

    def _apply_real_cap_transformations(
        self,
        base_pattern: List[PictographData],
        cap_type: CAPType,
        slice_size: SliceSize
    ) -> List[PictographData]:
        """Apply real CAP transformations to create the full sequence pattern."""
        
        if not base_pattern:
            return base_pattern
        
        try:
            if cap_type == CAPType.STRICT_ROTATED:
                return self._apply_strict_rotated(base_pattern)
            elif cap_type == CAPType.STRICT_MIRRORED:
                return self._apply_strict_mirrored(base_pattern)
            elif cap_type == CAPType.STRICT_SWAPPED:
                return self._apply_strict_swapped(base_pattern)
            elif cap_type == CAPType.STRICT_COMPLEMENTARY:
                return self._apply_strict_complementary(base_pattern)
            elif cap_type == CAPType.MIRRORED_ROTATED:
                return self._apply_mirrored_rotated(base_pattern)
            elif cap_type == CAPType.MIRRORED_COMPLEMENTARY_ROTATED:
                return self._apply_mirrored_complementary_rotated(base_pattern)
            else:
                logger.warning(f"CAP type {cap_type} not yet implemented, using base pattern")
                return base_pattern + base_pattern  # Simple duplication as fallback
                
        except Exception as e:
            logger.error(f"CAP transformation failed: {e}")
            return base_pattern

    def _apply_strict_rotated(self, pattern: List[PictographData]) -> List[PictographData]:
        """Apply strict rotated CAP transformation using real position mappings."""
        
        rotated_pattern = []
        rotation_map = self.position_mappings["rotated"]
        
        for pictograph in pattern:
            rotated_pictograph = self._transform_pictograph_positions(
                pictograph, rotation_map
            )
            rotated_pattern.append(rotated_pictograph)
        
        return pattern + rotated_pattern

    def _apply_strict_mirrored(self, pattern: List[PictographData]) -> List[PictographData]:
        """Apply strict mirrored CAP transformation using real position mappings."""
        
        mirrored_pattern = []
        mirror_map = self.position_mappings["mirrored"]
        
        for pictograph in pattern:
            mirrored_pictograph = self._transform_pictograph_positions(
                pictograph, mirror_map
            )
            mirrored_pattern.append(mirrored_pictograph)
        
        return pattern + mirrored_pattern

    def _apply_strict_swapped(self, pattern: List[PictographData]) -> List[PictographData]:
        """Apply strict swapped CAP transformation."""
        
        swapped_pattern = []
        
        for pictograph in pattern:
            # Swap blue and red motions
            blue_motion = pictograph.motions.get('blue')
            red_motion = pictograph.motions.get('red')
            
            swapped_pictograph = pictograph.update(motions={
                'blue': red_motion,
                'red': blue_motion
            })
            swapped_pattern.append(swapped_pictograph)
        
        return pattern + swapped_pattern

    def _apply_strict_complementary(self, pattern: List[PictographData]) -> List[PictographData]:
        """Apply strict complementary CAP transformation."""
        
        complementary_pattern = []
        
        # Motion type complements
        motion_complements = {
            MotionType.PRO: MotionType.ANTI,
            MotionType.ANTI: MotionType.PRO,
            MotionType.DASH: MotionType.DASH,
            MotionType.STATIC: MotionType.STATIC,
            MotionType.FLOAT: MotionType.FLOAT
        }
        
        for pictograph in pattern:
            complementary_motions = {}
            
            for color, motion in pictograph.motions.items():
                comp_motion_type = motion_complements.get(motion.motion_type, motion.motion_type)
                comp_motion = motion.update(motion_type=comp_motion_type)
                complementary_motions[color] = comp_motion
            
            comp_pictograph = pictograph.update(motions=complementary_motions)
            complementary_pattern.append(comp_pictograph)
        
        return pattern + complementary_pattern

    def _apply_mirrored_rotated(self, pattern: List[PictographData]) -> List[PictographData]:
        """Apply mirrored rotated CAP transformation (combination transformation)."""
        
        # First apply rotation to get rotated pattern
        rotated_pattern = self._apply_strict_rotated(pattern)
        
        # Then apply mirroring to the entire result
        mirror_map = self.position_mappings["mirrored"]
        
        final_pattern = []
        for pictograph in rotated_pattern:
            mirrored_pictograph = self._transform_pictograph_positions(
                pictograph, mirror_map
            )
            final_pattern.append(mirrored_pictograph)
        
        return final_pattern

    def _apply_mirrored_complementary_rotated(self, pattern: List[PictographData]) -> List[PictographData]:
        """Apply mirrored complementary rotated CAP transformation."""
        
        # Apply mirrored rotated first
        mirrored_rotated = self._apply_mirrored_rotated(pattern)
        
        # Then apply complementary transformation
        return self._apply_strict_complementary(mirrored_rotated)

    def _transform_pictograph_positions(
        self, 
        pictograph: PictographData, 
        position_map: Dict[str, str]
    ) -> PictographData:
        """Transform pictograph positions using the given mapping."""
        
        # Transform start and end positions
        new_start_pos = position_map.get(pictograph.start_position, pictograph.start_position)
        new_end_pos = position_map.get(pictograph.end_position, pictograph.end_position)
        
        return pictograph.update(
            start_position=new_start_pos,
            end_position=new_end_pos
        )

    def _convert_csv_to_modern_pictograph(self, csv_data: Dict[str, Any], beat_number: int) -> PictographData:
        """Convert CSV row data to modern PictographData structure."""
        
        # Create blue motion data
        blue_motion = MotionData(
            motion_type=MotionType(csv_data.get('blue_motion_type', 'static')),
            prop_rot_dir=RotationDirection(csv_data.get('blue_prop_rot_dir', 'no_rot')),
            start_loc=Location(csv_data.get('blue_start_loc', 'n')),
            end_loc=Location(csv_data.get('blue_end_loc', 'n')),
            turns=0,
            start_ori=Orientation.IN,
            end_ori=Orientation.IN
        )
        
        # Create red motion data
        red_motion = MotionData(
            motion_type=MotionType(csv_data.get('red_motion_type', 'static')),
            prop_rot_dir=RotationDirection(csv_data.get('red_prop_rot_dir', 'no_rot')),
            start_loc=Location(csv_data.get('red_start_loc', 'n')),
            end_loc=Location(csv_data.get('red_end_loc', 'n')),
            turns=0,
            start_ori=Orientation.IN,
            end_ori=Orientation.IN
        )
        
        # Create pictograph data
        pictograph_data = PictographData(
            letter=csv_data.get('letter', ''),
            start_position=csv_data.get('start_pos'),
            end_position=csv_data.get('end_pos'),
            beat=beat_number,
            motions={
                'blue': blue_motion,
                'red': red_motion
            },
            metadata={
                'timing': csv_data.get('timing', ''),
                'direction': csv_data.get('direction', ''),
                'generated_by': 'modern_circular_service'
            }
        )
        
        return pictograph_data

    def _apply_turns_to_pictograph(
        self, 
        pictograph_data: PictographData, 
        turn_blue: Any, 
        turn_red: Any
    ) -> PictographData:
        """Apply turns to pictograph motions for levels 2 and 3."""
        
        # Update blue motion with turns
        blue_motion = pictograph_data.motions['blue']
        if turn_blue == "fl":
            blue_motion = blue_motion.to_float_state(
                prefloat_motion_type=blue_motion.motion_type,
                prefloat_prop_rot_dir=blue_motion.prop_rot_dir
            )
        else:
            blue_motion = blue_motion.update(turns=turn_blue)
        
        # Update red motion with turns
        red_motion = pictograph_data.motions['red']
        if turn_red == "fl":
            red_motion = red_motion.to_float_state(
                prefloat_motion_type=red_motion.motion_type,
                prefloat_prop_rot_dir=red_motion.prop_rot_dir
            )
        else:
            red_motion = red_motion.update(turns=turn_red)
        
        # Return updated pictograph
        return pictograph_data.update(motions={
            'blue': blue_motion,
            'red': red_motion
        })

    def _process_events(self) -> None:
        """Process Qt events to update UI during generation."""
        try:
            from PyQt6.QtWidgets import QApplication
            QApplication.processEvents()
        except Exception:
            pass  # Not critical if Qt is not available
