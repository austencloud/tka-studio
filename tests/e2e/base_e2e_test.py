"""
Base End-to-End Test Framework for TKA Application

Provides common functionality for all E2E tests including:
- Application setup and teardown
- Component discovery and interaction
- Logging and error handling
- Qt object lifecycle management
"""

import sys
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any, Callable
from abc import ABC, abstractmethod

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from PyQt6.QtCore import QObject
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QTabWidget, QWidget

# Configure logging for E2E tests
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)


class BaseE2ETest(ABC):
    """
    Base class for all end-to-end tests in the TKA application.
    
    Provides common functionality for:
    - Application lifecycle management
    - Component discovery and interaction
    - Error handling and cleanup
    - Logging and debugging support
    """
    
    def __init__(self, test_name: str):
        """Initialize the base E2E test."""
        self.test_name = test_name
        self.app = None
        self.main_window = None
        self.construct_tab = None
        
        # Component references
        self.start_position_picker = None
        self.option_picker = None
        self.workbench = None
        
        # Test state
        self.test_results = []
        self.cleanup_callbacks = []
        
        logger.info(f"INIT: Initializing {test_name} E2E test")
    
    def setup_application(self) -> bool:
        """Setup the TKA application for testing."""
        try:
            logger.info("SETUP: Setting up TKA application...")
            
            # Use the proven application creation method
            from desktop.modern.main import create_application
            
            logger.info("SETUP: Creating application and main window...")
            self.app, self.main_window = create_application()
            
            # Show window and wait for initialization
            self.main_window.show()
            QTest.qWait(3000)  # Wait for full UI initialization
            
            logger.info("SUCCESS: Application setup completed")
            return True
            
        except Exception as e:
            logger.error(f"ERROR: Failed to setup application: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def find_construct_tab(self) -> bool:
        """Find and navigate to the construct tab."""
        try:
            logger.info("NAVIGATE: Finding construct tab...")
            
            # Find tab widget
            tab_widget = self._find_tab_widget()
            if not tab_widget:
                logger.error("ERROR: Could not find tab widget")
                return False
            
            logger.info(f"FOUND: Tab widget with {tab_widget.count()} tabs")
            
            # Find construct tab
            construct_tab_index = self._find_construct_tab_index(tab_widget)
            if construct_tab_index == -1:
                logger.error("ERROR: Could not find construct tab")
                return False
            
            # Switch to construct tab
            tab_widget.setCurrentIndex(construct_tab_index)
            QTest.qWait(500)
            
            # Get construct tab widget
            self.construct_tab = tab_widget.currentWidget()
            logger.info(f"SUCCESS: Found construct tab: {type(self.construct_tab)}")
            
            return True
            
        except Exception as e:
            logger.error(f"ERROR: Failed to find construct tab: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def discover_components(self) -> bool:
        """Discover and catalog all components in the construct tab."""
        try:
            logger.info("DISCOVER: Analyzing construct tab components...")
            
            if not self.construct_tab:
                logger.error("ERROR: No construct tab available")
                return False
            
            # Get all child components
            all_children = self.construct_tab.findChildren(QObject)
            logger.info(f"FOUND: {len(all_children)} total child components")
            
            # Find key components
            self._find_key_components(all_children)
            
            # Report findings
            logger.info("RESULTS: Component discovery results:")
            logger.info(f"   Start Position Picker: {self.start_position_picker is not None}")
            logger.info(f"   Option Picker: {self.option_picker is not None}")
            logger.info(f"   Workbench: {self.workbench is not None}")
            
            return True
            
        except Exception as e:
            logger.error(f"ERROR: Failed to discover components: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _find_tab_widget(self):
        """Find the main tab widget using multiple strategies."""
        # Strategy 1: Direct findChild
        tab_widget = self.main_window.findChild(QTabWidget)
        if tab_widget:
            logger.info("FOUND: Tab widget found via direct findChild")
            return tab_widget
        
        # Strategy 2: Search all children
        all_children = self.main_window.findChildren(QObject)
        for child in all_children:
            if isinstance(child, QTabWidget):
                logger.info(f"FOUND: Tab widget found in children: {child.__class__.__name__}")
                return child
        
        # Strategy 3: Get central widget and search there
        central_widget = self.main_window.centralWidget()
        if central_widget:
            central_children = central_widget.findChildren(QTabWidget)
            if central_children:
                logger.info(f"FOUND: Tab widget in central widget: {central_children[0].__class__.__name__}")
                return central_children[0]
        
        return None
    
    def _find_construct_tab_index(self, tab_widget: QTabWidget) -> int:
        """Find the index of the construct tab."""
        for i in range(tab_widget.count()):
            tab_text = tab_widget.tabText(i)
            logger.info(f"TAB {i}: {tab_text}")
            if "construct" in tab_text.lower() or i == 0:
                return i
        return -1
    
    def _find_key_components(self, all_children: List[QObject]):
        """Find key components using name matching strategies."""
        for widget in all_children:
            widget_name = widget.__class__.__name__.lower()
            
            # Find start position picker (use first match for primary reference)
            if not self.start_position_picker and self._is_start_position_picker(widget_name):
                self.start_position_picker = widget
                logger.info(f"FOUND: Start position picker: {widget.__class__.__name__}")
            
            # Find option picker (use first match for primary reference)
            if not self.option_picker and self._is_option_picker(widget_name):
                self.option_picker = widget
                logger.info(f"FOUND: Option picker: {widget.__class__.__name__}")
            
            # Find workbench (use first match for primary reference)
            if not self.workbench and self._is_workbench(widget_name):
                self.workbench = widget
                logger.info(f"FOUND: Workbench: {widget.__class__.__name__}")
    
    def _is_start_position_picker(self, widget_name: str) -> bool:
        """Check if widget is a start position picker."""
        return (
            "startpositionpicker" in widget_name or
            ("start" in widget_name and "position" in widget_name and "picker" in widget_name)
        )
    
    def _is_option_picker(self, widget_name: str) -> bool:
        """Check if widget is an option picker."""
        return (
            "optionpicker" in widget_name and "section" not in widget_name or
            ("option" in widget_name and "picker" in widget_name and "widget" in widget_name)
        )
    
    def _is_workbench(self, widget_name: str) -> bool:
        """Check if widget is a workbench."""
        return (
            "sequenceworkbench" in widget_name or
            ("sequence" in widget_name and "workbench" in widget_name)
        )
    
    def wait_for_ui(self, milliseconds: int = 500):
        """Wait for UI to update."""
        QTest.qWait(milliseconds)
    
    def add_cleanup_callback(self, callback: Callable):
        """Add a cleanup callback to be executed during teardown."""
        self.cleanup_callbacks.append(callback)
    
    def cleanup(self):
        """Cleanup resources and close application."""
        try:
            logger.info("CLEANUP: Starting test cleanup...")
            
            # Execute cleanup callbacks
            for callback in self.cleanup_callbacks:
                try:
                    callback()
                except Exception as e:
                    logger.warning(f"CLEANUP: Callback failed: {e}")
            
            # Close main window
            if self.main_window:
                self.main_window.close()
                self.main_window = None
            
            # Clear component references
            self.construct_tab = None
            self.start_position_picker = None
            self.option_picker = None
            self.workbench = None
            
            logger.info("CLEANUP: Test cleanup completed")
            
        except Exception as e:
            logger.warning(f"CLEANUP: Error during cleanup: {e}")
    
    def run_test(self) -> bool:
        """Run the complete test workflow."""
        try:
            logger.info(f"START: Starting {self.test_name} test...")
            
            # Setup phase
            if not self.setup_application():
                return False
            
            if not self.find_construct_tab():
                return False
            
            if not self.discover_components():
                return False
            
            # Run test-specific logic
            if not self.execute_test_logic():
                return False
            
            logger.info(f"SUCCESS: {self.test_name} test completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"ERROR: {self.test_name} test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.cleanup()
    
    @abstractmethod
    def execute_test_logic(self) -> bool:
        """
        Execute the test-specific logic.
        
        This method must be implemented by subclasses to define
        the specific test workflow and validations.
        
        Returns:
            bool: True if test passes, False if test fails
        """
        pass
