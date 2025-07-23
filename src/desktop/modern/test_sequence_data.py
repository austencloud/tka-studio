#!/usr/bin/env python3
"""
Test script to check sequence data and image paths.
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from core.dependency_injection.di_container import DIContainer
from core.dependency_injection.sequence_card_service_registration import register_sequence_card_services
from core.interfaces.sequence_card_services import ISequenceCardDataService

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger(__name__)

def test_sequence_data():
    """Test sequence data and paths."""
    try:
        # Create DI container and register services
        container = DIContainer()
        register_sequence_card_services(container)
        
        # Get data service
        data_service = container.resolve(ISequenceCardDataService)
        logger.info("✅ Data service created")
        
        # Get path service to find dictionary
        from application.services.sequence_card.path_service import SequenceCardPathService
        path_service = SequenceCardPathService()
        dictionary_path = path_service.get_dictionary_path()
        logger.info(f"Dictionary path: {dictionary_path}")
        
        # Get sequences for length 16
        sequences = data_service.get_sequences_by_length(dictionary_path, 16)
        logger.info(f"Found {len(sequences)} sequences for length 16")
        
        if sequences:
            # Check first few sequences
            for i, seq in enumerate(sequences[:5]):
                logger.info(f"Sequence {i+1}:")
                logger.info(f"  - Word: {seq.word}")
                logger.info(f"  - Length: {seq.length}")
                logger.info(f"  - Path: {seq.path}")
                logger.info(f"  - Path exists: {seq.path.exists()}")
                if seq.path.exists():
                    logger.info(f"  - File size: {seq.path.stat().st_size} bytes")
                else:
                    logger.error(f"  - ❌ File does not exist!")
        
        return True
            
    except Exception as e:
        logger.error(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_sequence_data()
    sys.exit(0 if success else 1)
