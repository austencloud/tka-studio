#!/usr/bin/env python3
"""
Test script to debug UI rendering issues in sequence card tab.
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from core.dependency_injection.di_container import DIContainer
from core.dependency_injection.sequence_card_service_registration import register_sequence_card_services
from presentation.tabs.sequence_card.sequence_card_tab import SequenceCardTab

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

def test_ui_rendering():
    """Test UI rendering step by step."""
    app = QApplication(sys.argv)
    
    try:
        # Create DI container and register services
        container = DIContainer()
        register_sequence_card_services(container)
        
        # Create tab with all dependencies
        tab = container.resolve(SequenceCardTab)
        logger.info("✅ Tab created successfully")
        
        # Show the tab
        tab.show()
        logger.info("✅ Tab shown")
        
        # Check initial state
        logger.info(f"Tab visible: {tab.isVisible()}")
        logger.info(f"Tab size: {tab.size()}")
        logger.info(f"Content component visible: {tab.content.isVisible()}")
        logger.info(f"Content component size: {tab.content.size()}")
        
        # Trigger a manual display operation with debugging
        logger.info("🔍 Triggering manual display operation...")
        
        # Set up signal to catch when sequences are loaded
        def on_sequences_loaded(sequences):
            logger.info(f"🎯 Sequences loaded: {len(sequences)} sequences")
            
            # Check content component state after loading
            logger.info(f"Content component after loading:")
            logger.info(f"  - Visible: {tab.content.isVisible()}")
            logger.info(f"  - Size: {tab.content.size()}")
            logger.info(f"  - Layout count: {tab.content.content_layout.count()}")
            
            # Check if any child widgets exist
            for i in range(tab.content.content_layout.count()):
                widget = tab.content.content_layout.itemAt(i).widget()
                if widget:
                    logger.info(f"  - Child {i}: {type(widget).__name__}, visible: {widget.isVisible()}, size: {widget.size()}")
            
            # Exit after checking
            QTimer.singleShot(1000, app.quit)
        
        tab.display_adaptor.sequences_loaded.connect(on_sequences_loaded)
        
        # Manually trigger display
        tab.display_adaptor.display_sequences(16, 2)
        
        # Set a timeout
        QTimer.singleShot(10000, lambda: (
            logger.error("❌ Timeout reached"),
            app.quit()
        ))
        
        # Run the event loop
        app.exec()
        
        logger.info("✅ Test completed")
        return True
            
    except Exception as e:
        logger.error(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_ui_rendering()
    sys.exit(0 if success else 1)
