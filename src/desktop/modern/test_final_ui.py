#!/usr/bin/env python3
"""
Final test to verify UI rendering is working correctly.
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

def test_final_ui():
    """Test final UI rendering."""
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
        tab.resize(1200, 800)
        logger.info("✅ Tab shown and resized")
        
        # Set up signal to catch when sequences are loaded
        sequences_loaded = False
        def on_sequences_loaded(sequences):
            nonlocal sequences_loaded
            sequences_loaded = True
            logger.info(f"✅ {len(sequences)} sequences loaded and displayed")
            
            # Check final state after a short delay to allow rendering
            QTimer.singleShot(1000, check_final_state)
        
        def check_final_state():
            logger.info("=== FINAL UI STATE ===")
            logger.info(f"Tab visible: {tab.isVisible()}")
            logger.info(f"Content visible: {tab.content.isVisible()}")
            logger.info(f"Content layout items: {tab.content.content_layout.count()}")
            
            # Check if any widgets are visible
            visible_widgets = 0
            for i in range(tab.content.content_layout.count()):
                item = tab.content.content_layout.itemAt(i)
                if item and item.widget() and item.widget().isVisible():
                    visible_widgets += 1
            
            logger.info(f"Visible layout items: {visible_widgets}")
            
            if sequences_loaded and visible_widgets > 0:
                logger.info("🎉 SUCCESS: UI rendering is working!")
            else:
                logger.error("❌ FAILURE: UI rendering issues detected")
            
            app.quit()
        
        tab.display_adaptor.sequences_loaded.connect(on_sequences_loaded)
        
        # Set a timeout in case something goes wrong
        QTimer.singleShot(10000, lambda: (
            logger.error("❌ Timeout reached"),
            app.quit()
        ))
        
        # Run the event loop
        app.exec()
        
        return sequences_loaded
            
    except Exception as e:
        logger.error(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_final_ui()
    print(f"\n{'='*50}")
    print(f"UI RENDERING TEST: {'PASSED' if success else 'FAILED'}")
    print(f"{'='*50}")
    sys.exit(0 if success else 1)
