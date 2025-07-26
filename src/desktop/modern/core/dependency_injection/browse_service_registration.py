"""
Browse Service Registration

Register browse-related services with the dependency injection container.
"""

import logging
from pathlib import Path

from desktop.modern.application.services.browse.sequence_deletion_service import SequenceDeletionService
from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.interfaces.browse_services import ISequenceDeletionService

logger = logging.getLogger(__name__)


def register_browse_services(container: DIContainer, sequences_dir: Path) -> None:
    """
    Register browse services with the DI container.
    
    Args:
        container: The dependency injection container
        sequences_dir: Directory containing sequence files
    """
    logger.info("Registering browse services...")
    
    try:
        # Register deletion service
        container.register_factory(
            ISequenceDeletionService,
            lambda: SequenceDeletionService(sequences_dir)
        )
        
        logger.info("Browse services registration completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to register browse services: {e}", exc_info=True)
        raise
