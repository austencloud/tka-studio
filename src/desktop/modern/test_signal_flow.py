#!/usr/bin/env python3
"""
Test script to verify the signal flow between display service and UI components.
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

def test_signal_flow():
    """Test the signal flow from service to UI."""
    app = QApplication(sys.argv)
    
    try:
        # Create DI container and register services
        container = DIContainer()
        register_sequence_card_services(container)
        
        # Create tab with all dependencies
        tab = container.resolve(SequenceCardTab)
        logger.info("✅ Tab created successfully")
        
        # Verify adaptor is properly connected
        logger.info(f"Display adaptor type: {type(tab.display_adaptor).__name__}")
        logger.info(f"Has sequences_loaded signal: {hasattr(tab.display_adaptor, 'sequences_loaded')}")
        logger.info(f"Content component connected: {hasattr(tab.content, 'display_adaptor')}")
        
        # Test signal connection by triggering a display operation
        logger.info("Testing signal flow...")
        
        # Set up a signal receiver to verify the signal is emitted
        sequences_received = []
        def on_sequences_loaded(sequences):
            sequences_received.append(sequences)
            logger.info(f"✅ Signal received! {len(sequences)} sequences loaded")
            app.quit()  # Exit after receiving signal
        
        tab.display_adaptor.sequences_loaded.connect(on_sequences_loaded)
        
        # Show the tab to trigger initialization
        tab.show()
        
        # Set a timeout to exit if no signal is received
        QTimer.singleShot(5000, lambda: (
            logger.error("❌ Timeout: No signal received"),
            app.quit()
        ))
        
        # Run the event loop
        app.exec()
        
        # Check results
        if sequences_received:
            logger.info(f"✅ SUCCESS: Signal flow working! Received {len(sequences_received[0])} sequences")
            return True
        else:
            logger.error("❌ FAILURE: No sequences signal received")
            return False
            
    except Exception as e:
        logger.error(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_signal_flow()
    sys.exit(0 if success else 1)
