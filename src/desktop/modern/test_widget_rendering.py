#!/usr/bin/env python3
"""
Test script to debug SequenceCardWidget rendering issues.
Focus on individual widget visibility and image loading.
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer

from core.dependency_injection.di_container import DIContainer
from core.dependency_injection.sequence_card_service_registration import register_sequence_card_services
from core.interfaces.sequence_card_services import ISequenceCardDataService
from presentation.tabs.sequence_card.components.content_component import SequenceCardWidget, SequenceCardPageWidget

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

def test_widget_rendering():
    """Test individual widget rendering step by step."""
    app = QApplication(sys.argv)
    
    try:
        # Create DI container and get data
        container = DIContainer()
        register_sequence_card_services(container)
        data_service = container.resolve(ISequenceCardDataService)
        
        # Get path service
        from application.services.sequence_card.path_service import SequenceCardPathService
        path_service = SequenceCardPathService()
        dictionary_path = path_service.get_dictionary_path()
        
        # Get a few sequences for testing
        sequences = data_service.get_sequences_by_length(dictionary_path, 16)[:3]
        logger.info(f"Testing with {len(sequences)} sequences")
        
        # Create a simple test window
        window = QMainWindow()
        window.setWindowTitle("Sequence Card Widget Test")
        window.resize(800, 600)
        
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        window.setCentralWidget(central_widget)
        
        # Test 1: Create individual SequenceCardWidget
        logger.info("=== TEST 1: Individual SequenceCardWidget ===")
        if sequences:
            seq = sequences[0]
            logger.info(f"Creating widget for: {seq.word}")
            
            card_widget = SequenceCardWidget(seq)
            layout.addWidget(card_widget)
            
            # Force show and check properties
            card_widget.show()
            logger.info(f"Widget after show(): visible={card_widget.isVisible()}, size={card_widget.size()}")
            
            # Check if it has content
            if card_widget.pixmap():
                logger.info(f"Widget has pixmap: size={card_widget.pixmap().size()}")
            else:
                logger.info(f"Widget has text: '{card_widget.text()}'")
        
        # Test 2: Create SequenceCardPageWidget
        logger.info("=== TEST 2: SequenceCardPageWidget ===")
        if len(sequences) >= 3:
            from core.interfaces.sequence_card_services import GridDimensions
            grid_dims = GridDimensions(columns=3, rows=1, total_positions=3)
            
            page_widget = SequenceCardPageWidget(sequences[:3], grid_dims)
            layout.addWidget(page_widget)
            
            page_widget.show()
            logger.info(f"Page widget: visible={page_widget.isVisible()}, size={page_widget.size()}")
            
            # Check child widgets
            page_layout = page_widget.layout()
            if page_layout:
                logger.info(f"Page layout has {page_layout.count()} items")
                for i in range(page_layout.count()):
                    item = page_layout.itemAt(i)
                    if item and item.widget():
                        child = item.widget()
                        logger.info(f"  Child {i}: {type(child).__name__}, visible={child.isVisible()}, size={child.size()}")
                        if hasattr(child, 'pixmap') and child.pixmap():
                            logger.info(f"    Has pixmap: {child.pixmap().size()}")
                        elif hasattr(child, 'text'):
                            logger.info(f"    Has text: '{child.text()[:30]}...'")
        
        # Show window and run event loop
        window.show()
        logger.info(f"Main window: visible={window.isVisible()}, size={window.size()}")
        
        # Set timer to exit after inspection
        def check_final_state():
            logger.info("=== FINAL STATE CHECK ===")
            logger.info(f"Window visible: {window.isVisible()}")
            logger.info(f"Central widget visible: {central_widget.isVisible()}")
            
            # Check all child widgets
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    logger.info(f"Layout item {i}: {type(widget).__name__}")
                    logger.info(f"  Visible: {widget.isVisible()}")
                    logger.info(f"  Size: {widget.size()}")
                    logger.info(f"  Geometry: {widget.geometry()}")
                    
                    # If it's a page widget, check its children
                    if hasattr(widget, 'layout') and widget.layout():
                        child_layout = widget.layout()
                        for j in range(child_layout.count()):
                            child_item = child_layout.itemAt(j)
                            if child_item and child_item.widget():
                                child_widget = child_item.widget()
                                logger.info(f"    Child {j}: visible={child_widget.isVisible()}, size={child_widget.size()}")
            
            app.quit()
        
        QTimer.singleShot(3000, check_final_state)
        
        # Run the event loop
        app.exec()
        
        logger.info("✅ Widget rendering test completed")
        return True
            
    except Exception as e:
        logger.error(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_widget_rendering()
    sys.exit(0 if success else 1)
