"""
Beat Frame Validator - UI Validation for BeatFrame Components
============================================================

Provides validation capabilities for BeatFrame state, pictograph rendering,
and sequence data consistency during testing.
"""

import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt

logger = logging.getLogger(__name__)


@dataclass
class BeatValidationResult:
    """Result of beat validation."""
    is_valid: bool
    beat_index: int
    errors: List[str]
    warnings: List[str]
    pictograph_data: Optional[Dict[str, Any]] = None


@dataclass
class SequenceValidationResult:
    """Result of sequence validation."""
    is_valid: bool
    total_beats: int
    valid_beats: int
    errors: List[str]
    warnings: List[str]
    beat_results: List[BeatValidationResult]


class BeatFrameValidator:
    """
    Validate BeatFrame state and pictograph rendering.
    
    Provides comprehensive validation of beat frame components including
    beat count, pictograph data, visual elements, and sequence consistency.
    """
    
    def __init__(self, beat_frame_widget: QWidget):
        """
        Initialize the beat frame validator.
        
        Args:
            beat_frame_widget: The BeatFrame widget to validate
        """
        self.beat_frame = beat_frame_widget
        self.beat_views = []
        self.start_position_view = None
        self._discover_beat_components()
    
    def _discover_beat_components(self) -> None:
        """Discover beat views and start position view within the beat frame."""
        try:
            # Find all BeatView components
            beat_views = self.beat_frame.findChildren(QWidget, "BeatView")
            self.beat_views = [view for view in beat_views if view.isVisible()]
            
            # Find StartPositionView
            start_views = self.beat_frame.findChildren(QWidget, "StartPositionView")
            if start_views:
                self.start_position_view = start_views[0]
            
            logger.debug(f"Discovered {len(self.beat_views)} beat views and start position view: {self.start_position_view is not None}")
            
        except Exception as e:
            logger.warning(f"Failed to discover beat components: {e}")
    
    def verify_beat_count(self, expected_count: int) -> bool:
        """
        Verify that the beat frame contains the expected number of beats.
        
        Args:
            expected_count: Expected number of beats
            
        Returns:
            True if beat count matches, False otherwise
        """
        try:
            actual_count = len(self.beat_views)
            if actual_count != expected_count:
                logger.error(f"Beat count mismatch: expected {expected_count}, got {actual_count}")
                return False
            
            logger.debug(f"Beat count verification passed: {actual_count} beats")
            return True
            
        except Exception as e:
            logger.error(f"Failed to verify beat count: {e}")
            return False
    
    def validate_pictograph_data(self, beat_index: int, expected_data: Dict[str, Any]) -> bool:
        """
        Validate pictograph data for a specific beat.
        
        Args:
            beat_index: Index of the beat to validate (0-based)
            expected_data: Expected pictograph data
            
        Returns:
            True if pictograph data matches expectations, False otherwise
        """
        try:
            if beat_index >= len(self.beat_views):
                logger.error(f"Beat index {beat_index} out of range (max: {len(self.beat_views) - 1})")
                return False
            
            beat_view = self.beat_views[beat_index]
            actual_data = self._extract_pictograph_data(beat_view)
            
            if not actual_data:
                logger.error(f"No pictograph data found for beat {beat_index}")
                return False
            
            # Validate key fields
            for key, expected_value in expected_data.items():
                if key not in actual_data:
                    logger.error(f"Missing pictograph data key '{key}' for beat {beat_index}")
                    return False
                
                if actual_data[key] != expected_value:
                    logger.error(f"Pictograph data mismatch for beat {beat_index}, key '{key}': expected {expected_value}, got {actual_data[key]}")
                    return False
            
            logger.debug(f"Pictograph data validation passed for beat {beat_index}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate pictograph data for beat {beat_index}: {e}")
            return False
    
    def check_visual_elements_present(self, beat_index: int) -> Dict[str, bool]:
        """
        Check which visual elements are present in a beat.
        
        Args:
            beat_index: Index of the beat to check
            
        Returns:
            Dictionary indicating presence of visual elements
        """
        elements = {
            'pictograph': False,
            'grid': False,
            'props': False,
            'arrows': False,
            'beat_number': False,
            'reversal_symbols': False
        }
        
        try:
            if beat_index >= len(self.beat_views):
                logger.error(f"Beat index {beat_index} out of range")
                return elements
            
            beat_view = self.beat_views[beat_index]
            
            # Check for pictograph scene
            if hasattr(beat_view, 'pictograph_scene') and beat_view.pictograph_scene:
                elements['pictograph'] = True
                
                # Check scene items for visual elements
                scene = beat_view.pictograph_scene
                scene_items = scene.items() if hasattr(scene, 'items') else []
                
                for item in scene_items:
                    item_name = item.objectName() if hasattr(item, 'objectName') else str(type(item))
                    
                    if 'grid' in item_name.lower():
                        elements['grid'] = True
                    elif 'prop' in item_name.lower() or 'staff' in item_name.lower():
                        elements['props'] = True
                    elif 'arrow' in item_name.lower():
                        elements['arrows'] = True
            
            # Check for beat number display
            beat_number_widgets = beat_view.findChildren(QWidget)
            for widget in beat_number_widgets:
                if hasattr(widget, 'text') and callable(widget.text):
                    text = widget.text()
                    if text.isdigit():
                        elements['beat_number'] = True
                        break
            
            # Check for reversal symbols
            reversal_widgets = beat_view.findChildren(QWidget)
            for widget in reversal_widgets:
                widget_name = widget.objectName() if hasattr(widget, 'objectName') else ""
                if 'reversal' in widget_name.lower():
                    elements['reversal_symbols'] = True
                    break
            
        except Exception as e:
            logger.error(f"Failed to check visual elements for beat {beat_index}: {e}")
        
        return elements
    
    def validate_sequence_data_consistency(self) -> SequenceValidationResult:
        """
        Validate consistency between UI display and stored sequence data.
        
        Returns:
            SequenceValidationResult with detailed validation information
        """
        errors = []
        warnings = []
        beat_results = []
        
        try:
            total_beats = len(self.beat_views)
            valid_beats = 0
            
            for i, beat_view in enumerate(self.beat_views):
                beat_result = self._validate_individual_beat(i, beat_view)
                beat_results.append(beat_result)
                
                if beat_result.is_valid:
                    valid_beats += 1
                else:
                    errors.extend([f"Beat {i}: {error}" for error in beat_result.errors])
                    warnings.extend([f"Beat {i}: {warning}" for warning in beat_result.warnings])
            
            # Check start position consistency
            if self.start_position_view:
                start_result = self._validate_start_position()
                if not start_result.is_valid:
                    errors.extend([f"Start Position: {error}" for error in start_result.errors])
            
            is_valid = len(errors) == 0
            
            return SequenceValidationResult(
                is_valid=is_valid,
                total_beats=total_beats,
                valid_beats=valid_beats,
                errors=errors,
                warnings=warnings,
                beat_results=beat_results
            )
            
        except Exception as e:
            logger.error(f"Failed to validate sequence data consistency: {e}")
            return SequenceValidationResult(
                is_valid=False,
                total_beats=0,
                valid_beats=0,
                errors=[f"Validation failed: {e}"],
                warnings=[],
                beat_results=[]
            )
    
    def _extract_pictograph_data(self, beat_view: QWidget) -> Optional[Dict[str, Any]]:
        """Extract pictograph data from a beat view."""
        try:
            # Try to get pictograph data from the beat view
            if hasattr(beat_view, 'pictograph_data'):
                return beat_view.pictograph_data
            
            if hasattr(beat_view, 'beat_data') and beat_view.beat_data:
                return beat_view.beat_data
            
            # Try to extract from scene or other sources
            if hasattr(beat_view, 'pictograph_scene') and beat_view.pictograph_scene:
                scene = beat_view.pictograph_scene
                if hasattr(scene, 'pictograph_data'):
                    return scene.pictograph_data
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to extract pictograph data: {e}")
            return None
    
    def _validate_individual_beat(self, beat_index: int, beat_view: QWidget) -> BeatValidationResult:
        """Validate an individual beat view."""
        errors = []
        warnings = []
        pictograph_data = None
        
        try:
            # Check if beat view is properly initialized
            if not beat_view.isVisible():
                warnings.append("Beat view is not visible")
            
            # Extract and validate pictograph data
            pictograph_data = self._extract_pictograph_data(beat_view)
            if not pictograph_data:
                errors.append("No pictograph data found")
            else:
                # Validate required fields in pictograph data
                required_fields = ['letter', 'start_pos', 'end_pos']
                for field in required_fields:
                    if field not in pictograph_data:
                        errors.append(f"Missing required field: {field}")
            
            # Check visual elements
            visual_elements = self.check_visual_elements_present(beat_index)
            if not visual_elements['pictograph']:
                errors.append("Pictograph not rendered")
            
            # Check for common issues
            if hasattr(beat_view, 'pictograph_scene'):
                scene = beat_view.pictograph_scene
                if scene and hasattr(scene, 'items'):
                    items = scene.items()
                    if len(items) == 0:
                        warnings.append("Pictograph scene has no items")
            
        except Exception as e:
            errors.append(f"Validation error: {e}")
        
        is_valid = len(errors) == 0
        
        return BeatValidationResult(
            is_valid=is_valid,
            beat_index=beat_index,
            errors=errors,
            warnings=warnings,
            pictograph_data=pictograph_data
        )
    
    def _validate_start_position(self) -> BeatValidationResult:
        """Validate the start position view."""
        errors = []
        warnings = []
        
        try:
            if not self.start_position_view.isVisible():
                warnings.append("Start position view is not visible")
            
            # Check for pictograph data
            pictograph_data = self._extract_pictograph_data(self.start_position_view)
            if not pictograph_data:
                errors.append("No start position data found")
            
        except Exception as e:
            errors.append(f"Start position validation error: {e}")
        
        is_valid = len(errors) == 0
        
        return BeatValidationResult(
            is_valid=is_valid,
            beat_index=-1,  # Special index for start position
            errors=errors,
            warnings=warnings,
            pictograph_data=pictograph_data
        )
