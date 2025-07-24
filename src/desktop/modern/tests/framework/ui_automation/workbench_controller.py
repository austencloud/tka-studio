"""
Workbench Controller - Complete Workflow Automation
==================================================

Orchestrates complete workflow automation for testing the Modern image export system,
including sequence creation, UI interactions, and export operations.
"""

import logging
import time
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from pathlib import Path

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QWidget, QApplication

from .picker_navigator import PickerNavigator
from .beat_frame_validator import BeatFrameValidator, SequenceValidationResult

logger = logging.getLogger(__name__)


@dataclass
class SequenceSpec:
    """Specification for creating a test sequence."""
    start_position: str
    beats: List[Dict[str, str]]  # List of beat specifications
    word: str = "TEST"
    include_start_position: bool = True


@dataclass
class WorkflowResult:
    """Result of a complete workflow execution."""
    success: bool
    export_path: Optional[str] = None
    sequence_validation: Optional[SequenceValidationResult] = None
    errors: List[str] = None
    warnings: List[str] = None
    execution_time_ms: int = 0


class WorkbenchController:
    """
    Orchestrate complete workflow automation for testing.
    
    Provides high-level methods to create authentic sequences, trigger exports,
    and validate the entire workflow from UI interaction to final export.
    """
    
    def __init__(self, workbench_widget: QWidget):
        """
        Initialize the workbench controller.
        
        Args:
            workbench_widget: The main workbench widget
        """
        self.workbench = workbench_widget
        self.picker_navigator = PickerNavigator(workbench_widget)
        self.beat_frame_validator = None
        self.export_service = None
        self._discover_components()
    
    def _discover_components(self) -> None:
        """Discover workbench components for automation."""
        try:
            # Find BeatFrame component
            beat_frames = self.workbench.findChildren(QWidget, "BeatFrame")
            if beat_frames:
                self.beat_frame_validator = BeatFrameValidator(beat_frames[0])
            
            # Try to get export service from workbench
            if hasattr(self.workbench, 'export_service'):
                self.export_service = self.workbench.export_service
            elif hasattr(self.workbench, '_export_service'):
                self.export_service = self.workbench._export_service
            
            logger.debug(f"Discovered components - BeatFrame: {self.beat_frame_validator is not None}, ExportService: {self.export_service is not None}")
            
        except Exception as e:
            logger.warning(f"Failed to discover workbench components: {e}")
    
    def create_authentic_sequence(self, sequence_spec: SequenceSpec, timeout_ms: int = 30000) -> bool:
        """
        Create an authentic sequence through UI interactions.
        
        Args:
            sequence_spec: Specification for the sequence to create
            timeout_ms: Maximum time to wait for sequence creation
            
        Returns:
            True if sequence was created successfully, False otherwise
        """
        start_time = time.time()
        
        try:
            logger.info(f"Creating authentic sequence: {sequence_spec.word} with {len(sequence_spec.beats)} beats")
            
            # Step 1: Select start position
            if sequence_spec.include_start_position:
                success = self.picker_navigator.select_start_position(sequence_spec.start_position)
                if not success:
                    logger.error("Failed to select start position")
                    return False
                
                # Wait for start position to be processed
                QTest.qWait(500)
            
            # Step 2: Create beats through option picker
            for i, beat_spec in enumerate(sequence_spec.beats):
                logger.debug(f"Creating beat {i + 1}: {beat_spec}")
                
                # Navigate to the beat (click on beat frame position)
                if not self._select_beat_position(i):
                    logger.error(f"Failed to select beat position {i}")
                    return False
                
                # Select motion type in option picker
                motion_type = beat_spec.get('motion', 'static')
                success = self.picker_navigator.navigate_option_picker(i + 1, motion_type)
                if not success:
                    logger.error(f"Failed to select motion '{motion_type}' for beat {i + 1}")
                    return False
                
                # Wait for beat to be processed
                QTest.qWait(300)
                
                # Check timeout
                if (time.time() - start_time) * 1000 > timeout_ms:
                    logger.error("Sequence creation timed out")
                    return False
            
            # Step 3: Validate the created sequence
            if self.beat_frame_validator:
                validation_result = self.beat_frame_validator.validate_sequence_data_consistency()
                if not validation_result.is_valid:
                    logger.error(f"Sequence validation failed: {validation_result.errors}")
                    return False
            
            logger.info(f"Successfully created authentic sequence in {(time.time() - start_time) * 1000:.0f}ms")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create authentic sequence: {e}")
            return False
    
    def trigger_save_image(self, output_path: Optional[Path] = None, timeout_ms: int = 10000) -> Optional[str]:
        """
        Trigger the save image operation through UI interaction.
        
        Args:
            output_path: Optional specific output path
            timeout_ms: Maximum time to wait for export
            
        Returns:
            Path to exported image if successful, None otherwise
        """
        try:
            logger.info("Triggering save image operation")
            
            # Find save image button
            save_buttons = self.workbench.findChildren(QWidget)
            save_button = None
            
            for button in save_buttons:
                # Check various ways the save button might be identified
                if hasattr(button, 'text') and callable(button.text):
                    text = button.text().lower()
                    if 'save' in text and 'image' in text:
                        save_button = button
                        break
                elif hasattr(button, 'objectName'):
                    name = button.objectName().lower()
                    if 'save' in name and 'image' in name:
                        save_button = button
                        break
            
            if not save_button:
                logger.error("Save image button not found")
                return None
            
            # Click the save button
            QTest.mouseClick(save_button, Qt.MouseButton.LeftButton)
            
            # Wait for export to complete
            QTest.qWait(2000)
            
            # Try to get the export path from the export service
            if self.export_service and hasattr(self.export_service, 'last_export_path'):
                return str(self.export_service.last_export_path)
            
            # Alternative: Check for recently created files in common export directories
            export_dirs = [
                Path("exports"),
                Path("C:/TKA/exports"),
                Path.home() / "Downloads",
            ]
            
            for export_dir in export_dirs:
                if export_dir.exists():
                    png_files = list(export_dir.glob("*.png"))
                    if png_files:
                        # Return the most recently created file
                        latest_file = max(png_files, key=lambda f: f.stat().st_mtime)
                        return str(latest_file)
            
            logger.warning("Could not determine export path")
            return None
            
        except Exception as e:
            logger.error(f"Failed to trigger save image: {e}")
            return None
    
    def validate_ui_data_consistency(self) -> bool:
        """
        Validate consistency between UI display and stored data.
        
        Returns:
            True if UI and data are consistent, False otherwise
        """
        try:
            if not self.beat_frame_validator:
                logger.error("BeatFrameValidator not available")
                return False
            
            validation_result = self.beat_frame_validator.validate_sequence_data_consistency()
            
            if not validation_result.is_valid:
                logger.error(f"UI data consistency validation failed:")
                for error in validation_result.errors:
                    logger.error(f"  - {error}")
                return False
            
            if validation_result.warnings:
                logger.warning("UI data consistency warnings:")
                for warning in validation_result.warnings:
                    logger.warning(f"  - {warning}")
            
            logger.info(f"UI data consistency validation passed: {validation_result.valid_beats}/{validation_result.total_beats} beats valid")
            return True
            
        except Exception as e:
            logger.error(f"Failed to validate UI data consistency: {e}")
            return False
    
    def execute_complete_workflow(self, sequence_spec: SequenceSpec, output_path: Optional[Path] = None) -> WorkflowResult:
        """
        Execute a complete workflow from sequence creation to export validation.
        
        Args:
            sequence_spec: Specification for the sequence to create
            output_path: Optional specific output path for export
            
        Returns:
            WorkflowResult with detailed execution information
        """
        start_time = time.time()
        errors = []
        warnings = []
        
        try:
            logger.info(f"Executing complete workflow for sequence: {sequence_spec.word}")
            
            # Step 1: Create authentic sequence
            sequence_created = self.create_authentic_sequence(sequence_spec)
            if not sequence_created:
                errors.append("Failed to create authentic sequence")
                return WorkflowResult(
                    success=False,
                    errors=errors,
                    execution_time_ms=int((time.time() - start_time) * 1000)
                )
            
            # Step 2: Validate UI data consistency
            ui_consistent = self.validate_ui_data_consistency()
            if not ui_consistent:
                errors.append("UI data consistency validation failed")
            
            # Step 3: Trigger export
            export_path = self.trigger_save_image(output_path)
            if not export_path:
                errors.append("Failed to trigger save image")
            
            # Step 4: Final validation
            sequence_validation = None
            if self.beat_frame_validator:
                sequence_validation = self.beat_frame_validator.validate_sequence_data_consistency()
                if not sequence_validation.is_valid:
                    errors.extend(sequence_validation.errors)
                warnings.extend(sequence_validation.warnings)
            
            success = len(errors) == 0 and export_path is not None
            execution_time = int((time.time() - start_time) * 1000)
            
            logger.info(f"Workflow execution completed in {execution_time}ms - Success: {success}")
            
            return WorkflowResult(
                success=success,
                export_path=export_path,
                sequence_validation=sequence_validation,
                errors=errors,
                warnings=warnings,
                execution_time_ms=execution_time
            )
            
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            errors.append(f"Workflow execution error: {e}")
            
            return WorkflowResult(
                success=False,
                errors=errors,
                execution_time_ms=int((time.time() - start_time) * 1000)
            )
    
    def _select_beat_position(self, beat_index: int) -> bool:
        """Select a specific beat position in the beat frame."""
        try:
            if not self.beat_frame_validator:
                logger.error("BeatFrameValidator not available")
                return False
            
            if beat_index >= len(self.beat_frame_validator.beat_views):
                logger.error(f"Beat index {beat_index} out of range")
                return False
            
            beat_view = self.beat_frame_validator.beat_views[beat_index]
            QTest.mouseClick(beat_view, Qt.MouseButton.LeftButton)
            QTest.qWait(100)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to select beat position {beat_index}: {e}")
            return False
