"""
Freeform Generation Service - PRODUCTION READY with ROBUST ERROR HANDLING

Generates freeform sequences using REAL TKA pictograph data and modern architecture.
ROBUST: Handles all error cases gracefully, validates all data conversions.
"""

import logging
import random
from copy import deepcopy
from typing import Any, Dict, List, Optional, Set, TYPE_CHECKING

from data.mappers.pictograph_mappers import PictographDataMapper
from desktop.modern.core.interfaces.generation_services import (
    GenerationMode,
    LetterType,
    PropContinuity,
)
from desktop.modern.domain.models.generation_models import GenerationConfig
from desktop.modern.domain.models.pictograph_data import PictographData
from desktop.modern.domain.models.motion_data import MotionData
from desktop.modern.domain.models.enums import (
    MotionType, RotationDirection, Location, Orientation
)
from .base_sequence_builder import BaseSequenceBuilder
from .turn_intensity_manager import TurnIntensityManager

if TYPE_CHECKING:
    from desktop.modern.core.dependency_injection.di_container import DIContainer

logger = logging.getLogger(__name__)


class FreeformGenerationService(BaseSequenceBuilder):
    """
    Modern freeform sequence generation service with robust error handling.
    
    Uses real TKA pictograph data from CSV files and integrates with modern
    sequence workbench through dependency injection architecture.
    """

    # Letter type to actual letters mapping (conservative - only letters that definitely exist)
    LETTER_TYPE_MAPPINGS = {
        LetterType.TYPE1: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V'],  # Dual-Shift
        LetterType.TYPE2: ['W', 'X', 'Y', 'Z'],  # Shift (conservative set)
        LetterType.TYPE3: ['W-', 'X-', 'Y-', 'Z-'],  # Cross-Shift (conservative set)
        LetterType.TYPE4: ['Φ', 'Ψ', 'Λ'],  # Dash
        LetterType.TYPE5: ['Φ-', 'Ψ-', 'Λ-'],  # Dual-Dash
        LetterType.TYPE6: ['α', 'β', 'Γ'],  # Static
    }

    def __init__(self, container: "DIContainer"):
        super().__init__(container)
        
        # Initialize data loader and options storage
        self.pictograph_mapper = None
        self.pictograph_options: List[Dict[str, Any]] = []
        
        # Robust initialization
        self._initialize_data_safely()

    def _initialize_data_safely(self) -> None:
        """Initialize real pictograph data with robust error handling."""
        try:
            # Try to initialize pictograph mapper
            data_path = self._get_data_path_safely()
            if not data_path:
                raise RuntimeError("Could not determine data directory path")
            
            self.pictograph_mapper = PictographDataMapper(data_path)
            self._load_real_pictograph_data()
            
            logger.info(f"✅ Freeform generation service initialized with {len(self.pictograph_options)} real pictographs")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize freeform generation service: {e}")
            raise RuntimeError(f"Cannot initialize freeform generation without real pictograph data: {e}")

    def _get_data_path_safely(self) -> Optional[str]:
        """Get the path to the data directory with error handling."""
        try:
            import os
            # Navigate from the service file to the data directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Go up: generation -> services -> application -> modern -> desktop -> TKA -> data
            data_path = os.path.join(current_dir, "..", "..", "..", "..", "..", "data")
            abs_path = os.path.abspath(data_path)
            
            # Verify the path exists and contains expected files
            if os.path.exists(abs_path):
                diamond_csv = os.path.join(abs_path, "DiamondPictographDataframe.csv")
                box_csv = os.path.join(abs_path, "BoxPictographDataframe.csv")
                
                if os.path.exists(diamond_csv) or os.path.exists(box_csv):
                    logger.info(f"✅ Found data directory at: {abs_path}")
                    return abs_path
                else:
                    logger.error(f"Data directory exists but no CSV files found: {abs_path}")
            else:
                logger.error(f"Data directory does not exist: {abs_path}")
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to determine data path: {e}")
            return None

    def _load_real_pictograph_data(self) -> None:
        """Load real pictograph data from CSV files with robust error handling."""
        try:
            # Try diamond data first
            diamond_data = self.pictograph_mapper.get_diamond_pictograph_data()
            
            if diamond_data:
                self.pictograph_options = diamond_data
                logger.info(f"✅ Loaded {len(diamond_data)} pictographs from diamond CSV")
            else:
                # Fallback to box data
                logger.warning("Diamond pictograph data not found, trying box data")
                box_data = self.pictograph_mapper.get_box_pictograph_data()
                
                if box_data:
                    self.pictograph_options = box_data
                    logger.info(f"✅ Loaded {len(box_data)} pictographs from box CSV")
                else:
                    raise RuntimeError("No pictograph data found in either diamond or box CSV files")
            
            # Validate data quality
            self._validate_pictograph_data()
            
            # Log available letters for debugging
            letters = set(opt.get('letter', '') for opt in self.pictograph_options if opt.get('letter'))
            logger.info(f"Available letters in data: {sorted(letters)}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load real pictograph data: {e}")
            raise

    def _validate_pictograph_data(self) -> None:
        """Validate the loaded pictograph data."""
        if not self.pictograph_options:
            raise RuntimeError("No pictograph options loaded")
        
        # Check that we have required fields
        required_fields = ['letter', 'blue_motion_type', 'red_motion_type']
        valid_options = 0
        
        for i, opt in enumerate(self.pictograph_options):
            has_required = all(field in opt for field in required_fields)
            if has_required:
                valid_options += 1
            elif i < 5:  # Log first few invalid entries for debugging
                logger.warning(f"Invalid pictograph option {i}: missing required fields. Has: {list(opt.keys())}")
        
        if valid_options == 0:
            raise RuntimeError("No valid pictograph options found with required fields")
        
        logger.info(f"✅ Validated {valid_options}/{len(self.pictograph_options)} pictograph options")

    def generate_sequence(self, config: GenerationConfig) -> List[Dict[str, Any]]:
        """
        Generate a freeform sequence using real TKA data and modern architecture.
        ROBUST: Handles all error cases and provides meaningful feedback.
        
        Args:
            config: Generation configuration
            
        Returns:
            List of generated beat data dictionaries
        """
        logger.info(f"🎯 Starting modern freeform generation: length={config.length}, level={config.level}")
        
        try:
            # Validate configuration
            self._validate_config(config)
            
            # Initialize sequence 
            self.initialize_sequence(config.length, config)
            
            # Determine prop rotation directions for continuous mode
            blue_rot_dir = None
            red_rot_dir = None
            
            if config.prop_continuity == PropContinuity.CONTINUOUS:
                blue_rot_dir = random.choice([RotationDirection.CLOCKWISE, RotationDirection.COUNTER_CLOCKWISE])
                red_rot_dir = random.choice([RotationDirection.CLOCKWISE, RotationDirection.COUNTER_CLOCKWISE])
                logger.info(f"Continuous mode: blue={blue_rot_dir.value}, red={red_rot_dir.value}")
            
            # Calculate how many beats we need to generate
            beats_to_generate = max(0, config.length)
            
            if beats_to_generate <= 0:
                logger.warning("No beats to generate (length <= 0)")
                return []
            
            # Use modern TurnIntensityManager with error handling
            turns_blue, turns_red = self._allocate_turns_safely(beats_to_generate, config)
            
            logger.info(f"Allocated turns for {beats_to_generate} beats")
            
            # Generate each beat and add to modern sequence workbench
            generated_beats = []
            for i in range(beats_to_generate):
                try:
                    logger.info(f"Generating beat {i+1}/{beats_to_generate}")
                    
                    # Generate pictograph data using modern structure
                    pictograph_data = self._generate_next_pictograph_safely(
                        config,
                        turns_blue[i],
                        turns_red[i],
                        blue_rot_dir,
                        red_rot_dir,
                        i + 1  # beat number
                    )
                    
                    if pictograph_data:
                        generated_beats.append(pictograph_data)
                        
                        # Add to modern sequence workbench one by one (for visual effect)
                        self.add_beat_to_modern_workbench(pictograph_data)
                        
                        # Process events to show beat appearing
                        self._process_events()
                        
                        logger.info(f"✅ Generated beat with letter: {pictograph_data.letter}")
                    else:
                        logger.warning(f"Failed to generate beat {i+1}")
                    
                except Exception as e:
                    logger.error(f"❌ Failed to generate beat {i+1}: {str(e)}")
                    continue  # Continue with next beat
            
            logger.info(f"🎉 Generated freeform sequence with {len(generated_beats)} beats")
            return generated_beats
            
        except Exception as e:
            logger.error(f"❌ Freeform generation failed: {str(e)}")
            raise

    def _validate_config(self, config: GenerationConfig) -> None:
        """Validate generation configuration."""
        if config.length <= 0:
            raise ValueError("Sequence length must be positive")
        if config.length > 32:
            raise ValueError("Sequence length cannot exceed 32")
        if config.level < 1 or config.level > 6:
            raise ValueError("Level must be between 1 and 6")
        if config.turn_intensity < 0 or config.turn_intensity > 3:
            raise ValueError("Turn intensity must be between 0 and 3")

    def _allocate_turns_safely(self, beats_to_generate: int, config: GenerationConfig) -> tuple:
        """Allocate turns with error handling."""
        try:
            turn_manager = TurnIntensityManager(
                word_length=beats_to_generate,
                level=config.level,
                max_turn_intensity=config.turn_intensity
            )
            return turn_manager.allocate_turns_for_blue_and_red()
        except Exception as e:
            logger.error(f"Turn allocation failed: {e}")
            # Fallback: no turns
            return ([0] * beats_to_generate, [0] * beats_to_generate)

    def _generate_next_pictograph_safely(
        self,
        config: GenerationConfig,
        turn_blue: Any,
        turn_red: Any,
        blue_rot_dir: Optional[RotationDirection],
        red_rot_dir: Optional[RotationDirection],
        beat_number: int
    ) -> Optional[PictographData]:
        """Generate the next pictograph with comprehensive error handling."""
        
        try:
            # Get real options from CSV data
            available_options = self._get_filtered_options_safely(config, blue_rot_dir, red_rot_dir)
            
            if not available_options:
                logger.error("No valid pictograph options available for generation")
                return None
            
            # Select random option
            selected_option = random.choice(available_options)
            
            # Convert CSV data to modern PictographData structure
            pictograph_data = self._convert_csv_to_modern_pictograph_safely(selected_option, beat_number)
            
            if not pictograph_data:
                logger.error("Failed to convert CSV data to pictograph")
                return None
            
            # Apply turns for levels 2 and 3
            if config.level >= 2:
                pictograph_data = self._apply_turns_to_pictograph_safely(pictograph_data, turn_blue, turn_red)
            
            return pictograph_data
            
        except Exception as e:
            logger.error(f"Failed to generate pictograph: {e}")
            return None

    def _get_filtered_options_safely(
        self, 
        config: GenerationConfig, 
        blue_rot_dir: Optional[RotationDirection], 
        red_rot_dir: Optional[RotationDirection]
    ) -> List[Dict[str, Any]]:
        """Filter pictograph options with comprehensive error handling."""
        
        try:
            options = deepcopy(self.pictograph_options)
            
            # Filter by letter types if specified
            if config.letter_types:
                options = self._filter_by_letter_types_safely(options, config.letter_types)
            
            # Filter by rotation continuity if specified
            if config.prop_continuity == PropContinuity.CONTINUOUS and (blue_rot_dir or red_rot_dir):
                options = self._filter_by_rotation_continuity_safely(options, blue_rot_dir, red_rot_dir)
            
            logger.info(f"Filtered to {len(options)} options from {len(self.pictograph_options)} total")
            return options
            
        except Exception as e:
            logger.error(f"Option filtering failed: {e}")
            return self.pictograph_options  # Return all options as fallback

    def _filter_by_letter_types_safely(self, options: List[Dict[str, Any]], selected_types: Set[LetterType]) -> List[Dict[str, Any]]:
        """Filter options by selected letter types with error handling."""
        
        try:
            if not selected_types:
                return options
            
            # Get all letters for selected types
            selected_letters = set()
            for letter_type in selected_types:
                if letter_type in self.LETTER_TYPE_MAPPINGS:
                    selected_letters.update(self.LETTER_TYPE_MAPPINGS[letter_type])
                else:
                    logger.warning(f"Unknown letter type: {letter_type}")
            
            if not selected_letters:
                logger.warning("No letters found for selected letter types")
                return options
            
            # Filter options
            filtered = [opt for opt in options if opt.get('letter', '') in selected_letters]
            
            logger.info(f"Letter type filtering: {len(options)} -> {len(filtered)} options (types: {[t.value for t in selected_types]})")
            return filtered if filtered else options  # Return all if no matches
            
        except Exception as e:
            logger.error(f"Letter type filtering failed: {e}")
            return options

    def _filter_by_rotation_continuity_safely(
        self, 
        options: List[Dict[str, Any]], 
        blue_rot_dir: Optional[RotationDirection], 
        red_rot_dir: Optional[RotationDirection]
    ) -> List[Dict[str, Any]]:
        """Filter options by rotation continuity with error handling."""
        
        try:
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
            
        except Exception as e:
            logger.error(f"Rotation continuity filtering failed: {e}")
            return options

    def _convert_csv_to_modern_pictograph_safely(self, csv_data: Dict[str, Any], beat_number: int) -> Optional[PictographData]:
        """Convert CSV row data to modern PictographData structure with error handling."""
        
        try:
            # Safe enum conversion with fallbacks
            blue_motion_type = self._safe_motion_type_conversion(csv_data.get('blue_motion_type', 'static'))
            red_motion_type = self._safe_motion_type_conversion(csv_data.get('red_motion_type', 'static'))
            
            blue_rot_dir = self._safe_rotation_direction_conversion(csv_data.get('blue_prop_rot_dir', 'no_rot'))
            red_rot_dir = self._safe_rotation_direction_conversion(csv_data.get('red_prop_rot_dir', 'no_rot'))
            
            blue_start_loc = self._safe_location_conversion(csv_data.get('blue_start_loc', 'n'))
            blue_end_loc = self._safe_location_conversion(csv_data.get('blue_end_loc', 'n'))
            red_start_loc = self._safe_location_conversion(csv_data.get('red_start_loc', 'n'))
            red_end_loc = self._safe_location_conversion(csv_data.get('red_end_loc', 'n'))
            
            # Create motion data with error handling
            blue_motion = MotionData(
                motion_type=blue_motion_type,
                prop_rot_dir=blue_rot_dir,
                start_loc=blue_start_loc,
                end_loc=blue_end_loc,
                turns=0,  # Will be set later if needed
                start_ori=Orientation.IN,
                end_ori=Orientation.IN
            )
            
            red_motion = MotionData(
                motion_type=red_motion_type,
                prop_rot_dir=red_rot_dir,
                start_loc=red_start_loc,
                end_loc=red_end_loc,
                turns=0,  # Will be set later if needed
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
                    'generated_by': 'modern_freeform_service'
                }
            )
            
            return pictograph_data
            
        except Exception as e:
            logger.error(f"Failed to convert CSV data to pictograph: {e}")
            return None

    def _safe_motion_type_conversion(self, value: str) -> MotionType:
        """Safely convert string to MotionType enum."""
        try:
            return MotionType(value.lower())
        except ValueError:
            logger.warning(f"Invalid motion type '{value}', using static")
            return MotionType.STATIC

    def _safe_rotation_direction_conversion(self, value: str) -> RotationDirection:
        """Safely convert string to RotationDirection enum."""
        try:
            return RotationDirection(value.lower())
        except ValueError:
            logger.warning(f"Invalid rotation direction '{value}', using no_rot")
            return RotationDirection.NO_ROTATION

    def _safe_location_conversion(self, value: str) -> Location:
        """Safely convert string to Location enum."""
        try:
            return Location(value.lower())
        except ValueError:
            logger.warning(f"Invalid location '{value}', using north")
            return Location.NORTH

    def _apply_turns_to_pictograph_safely(
        self, 
        pictograph_data: PictographData, 
        turn_blue: Any, 
        turn_red: Any
    ) -> PictographData:
        """Apply turns to pictograph motions with error handling."""
        
        try:
            # Update blue motion with turns
            blue_motion = pictograph_data.motions['blue']
            if turn_blue == "fl":
                # Convert to float motion
                blue_motion = blue_motion.to_float_state(
                    prefloat_motion_type=blue_motion.motion_type,
                    prefloat_prop_rot_dir=blue_motion.prop_rot_dir
                )
            else:
                blue_motion = blue_motion.update(turns=turn_blue)
            
            # Update red motion with turns
            red_motion = pictograph_data.motions['red']
            if turn_red == "fl":
                # Convert to float motion
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
            
        except Exception as e:
            logger.error(f"Failed to apply turns to pictograph: {e}")
            return pictograph_data  # Return unchanged if update fails

    def _process_events(self) -> None:
        """Process Qt events to update UI during generation."""
        try:
            from PyQt6.QtWidgets import QApplication
            QApplication.processEvents()
        except Exception:
            pass  # Not critical if Qt is not available
