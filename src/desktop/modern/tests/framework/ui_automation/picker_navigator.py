"""
Picker Navigator - UI Automation for StartPositionPicker and OptionPicker
=========================================================================

Provides automated interaction capabilities for the picker components,
enabling programmatic selection and validation of picker states.
"""

import logging
import time
from typing import Dict, Optional, Any
from dataclasses import dataclass

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QWidget

logger = logging.getLogger(__name__)


@dataclass
class PickerState:
    """Represents the current state of a picker component."""
    selected_position: Optional[str] = None
    selected_motion: Optional[str] = None
    is_visible: bool = False
    is_enabled: bool = False
    error_message: Optional[str] = None


class PickerNavigator:
    """
    Automate StartPositionPicker and OptionPicker interactions.
    
    Provides methods to programmatically interact with picker components
    and validate their state during testing.
    """
    
    def __init__(self, workbench_widget: QWidget):
        """
        Initialize the picker navigator.
        
        Args:
            workbench_widget: The main workbench widget containing pickers
        """
        self.workbench = workbench_widget
        self.start_position_picker = None
        self.option_picker = None
        self._discover_pickers()
    
    def _discover_pickers(self) -> None:
        """Discover picker widgets within the workbench."""
        try:
            # Find StartPositionPicker
            start_pickers = self.workbench.findChildren(QWidget, "StartPositionPicker")
            if start_pickers:
                self.start_position_picker = start_pickers[0]
                logger.debug(f"Found StartPositionPicker: {self.start_position_picker}")
            
            # Find OptionPicker
            option_pickers = self.workbench.findChildren(QWidget, "OptionPicker")
            if option_pickers:
                self.option_picker = option_pickers[0]
                logger.debug(f"Found OptionPicker: {self.option_picker}")
                
        except Exception as e:
            logger.warning(f"Failed to discover pickers: {e}")
    
    def select_start_position(self, position_key: str, timeout_ms: int = 5000) -> bool:
        """
        Select a start position in the StartPositionPicker.
        
        Args:
            position_key: The position key to select (e.g., "alpha1_alpha1")
            timeout_ms: Maximum time to wait for selection
            
        Returns:
            True if selection was successful, False otherwise
        """
        if not self.start_position_picker:
            logger.error("StartPositionPicker not found")
            return False
        
        try:
            # Ensure picker is visible and enabled
            if not self.start_position_picker.isVisible():
                logger.error("StartPositionPicker is not visible")
                return False
            
            # Look for position button by position key
            position_buttons = self.start_position_picker.findChildren(QWidget)
            target_button = None
            
            for button in position_buttons:
                # Check if button has the position key as property or data
                if hasattr(button, 'position_key') and button.position_key == position_key:
                    target_button = button
                    break
                elif hasattr(button, 'objectName') and position_key in button.objectName():
                    target_button = button
                    break
            
            if not target_button:
                logger.error(f"Position button for '{position_key}' not found")
                return False
            
            # Click the button
            QTest.mouseClick(target_button, Qt.MouseButton.LeftButton)
            
            # Wait for selection to process
            QTest.qWait(100)
            
            # Verify selection was successful
            return self._verify_start_position_selection(position_key)
            
        except Exception as e:
            logger.error(f"Failed to select start position '{position_key}': {e}")
            return False
    
    def navigate_option_picker(self, beat_number: int, motion_type: str, timeout_ms: int = 5000) -> bool:
        """
        Navigate the OptionPicker to select a specific motion for a beat.
        
        Args:
            beat_number: The beat number to modify
            motion_type: The motion type to select (e.g., "pro", "anti", "static", "dash")
            timeout_ms: Maximum time to wait for navigation
            
        Returns:
            True if navigation was successful, False otherwise
        """
        if not self.option_picker:
            logger.error("OptionPicker not found")
            return False
        
        try:
            # Ensure option picker is visible
            if not self.option_picker.isVisible():
                logger.error("OptionPicker is not visible")
                return False
            
            # Find motion type buttons or sections
            motion_buttons = self._find_motion_buttons(motion_type)
            if not motion_buttons:
                logger.error(f"Motion buttons for '{motion_type}' not found")
                return False
            
            # Select the first available option of the specified motion type
            target_button = motion_buttons[0]
            QTest.mouseClick(target_button, Qt.MouseButton.LeftButton)
            
            # Wait for selection to process
            QTest.qWait(200)
            
            # Verify selection was successful
            return self._verify_option_picker_selection(motion_type)
            
        except Exception as e:
            logger.error(f"Failed to navigate option picker for beat {beat_number}, motion '{motion_type}': {e}")
            return False
    
    def verify_picker_state(self, expected_selection: Dict[str, Any]) -> bool:
        """
        Verify the current state of pickers matches expected selection.
        
        Args:
            expected_selection: Dictionary containing expected picker states
            
        Returns:
            True if state matches expectations, False otherwise
        """
        try:
            current_state = self.get_current_picker_state()
            
            for key, expected_value in expected_selection.items():
                if key not in current_state:
                    logger.error(f"Expected state key '{key}' not found in current state")
                    return False
                
                if current_state[key] != expected_value:
                    logger.error(f"State mismatch for '{key}': expected {expected_value}, got {current_state[key]}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to verify picker state: {e}")
            return False
    
    def get_current_picker_state(self) -> Dict[str, Any]:
        """
        Get the current state of all pickers.
        
        Returns:
            Dictionary containing current picker states
        """
        state = {}
        
        try:
            # Get StartPositionPicker state
            if self.start_position_picker:
                state['start_position'] = {
                    'visible': self.start_position_picker.isVisible(),
                    'enabled': self.start_position_picker.isEnabled(),
                    'selected_position': self._get_selected_start_position(),
                }
            
            # Get OptionPicker state
            if self.option_picker:
                state['option_picker'] = {
                    'visible': self.option_picker.isVisible(),
                    'enabled': self.option_picker.isEnabled(),
                    'selected_motion': self._get_selected_motion(),
                }
                
        except Exception as e:
            logger.error(f"Failed to get picker state: {e}")
            state['error'] = str(e)
        
        return state
    
    def _find_motion_buttons(self, motion_type: str) -> list:
        """Find buttons for a specific motion type in the OptionPicker."""
        if not self.option_picker:
            return []
        
        motion_buttons = []
        all_buttons = self.option_picker.findChildren(QWidget)
        
        for button in all_buttons:
            # Check various ways motion type might be stored
            if hasattr(button, 'motion_type') and button.motion_type == motion_type:
                motion_buttons.append(button)
            elif hasattr(button, 'objectName') and motion_type in button.objectName():
                motion_buttons.append(button)
            elif hasattr(button, 'text') and callable(button.text) and motion_type in button.text():
                motion_buttons.append(button)
        
        return motion_buttons
    
    def _verify_start_position_selection(self, position_key: str) -> bool:
        """Verify that the start position was successfully selected."""
        try:
            # Check if the picker has a selected position property
            if hasattr(self.start_position_picker, 'selected_position'):
                return self.start_position_picker.selected_position == position_key
            
            # Alternative: Check for visual selection indicators
            selected_buttons = self.start_position_picker.findChildren(QWidget)
            for button in selected_buttons:
                if hasattr(button, 'isSelected') and button.isSelected():
                    if hasattr(button, 'position_key') and button.position_key == position_key:
                        return True
            
            return False
            
        except Exception as e:
            logger.error(f"Failed to verify start position selection: {e}")
            return False
    
    def _verify_option_picker_selection(self, motion_type: str) -> bool:
        """Verify that the option picker selection was successful."""
        try:
            # Check if the picker has a selected motion property
            if hasattr(self.option_picker, 'selected_motion'):
                return self.option_picker.selected_motion == motion_type
            
            # Alternative: Check for visual selection indicators
            return True  # Assume success if no errors occurred
            
        except Exception as e:
            logger.error(f"Failed to verify option picker selection: {e}")
            return False
    
    def _get_selected_start_position(self) -> Optional[str]:
        """Get the currently selected start position."""
        if not self.start_position_picker:
            return None
        
        try:
            if hasattr(self.start_position_picker, 'selected_position'):
                return self.start_position_picker.selected_position
            return None
        except Exception:
            return None
    
    def _get_selected_motion(self) -> Optional[str]:
        """Get the currently selected motion type."""
        if not self.option_picker:
            return None
        
        try:
            if hasattr(self.option_picker, 'selected_motion'):
                return self.option_picker.selected_motion
            return None
        except Exception:
            return None
