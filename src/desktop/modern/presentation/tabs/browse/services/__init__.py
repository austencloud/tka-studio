# Browse Tab Services - Refactored

# Core services with real business logic
from .browse_service import BrowseService
from .browse_state_service import BrowseStateService
from .modern_dictionary_data_manager import ModernDictionaryDataManager
from .progressive_loading_service import ProgressiveLoadingService

# Specialized services (keep these - they have real logic)
from .sequence_sorter_service import SequenceSorterService
from .thumbnail_factory_service import ThumbnailFactoryService

# Note: Removed thin wrapper services:
# - LayoutManagerService (use PyQt directly)
# - LoadingStateManagerService (use PyQt directly)  
# - NavigationHandlerService (use PyQt directly)
# - SequenceDisplayCoordinatorService (use PyQt directly)

__all__ = [
    "BrowseService",
    "BrowseStateService", 
    "ModernDictionaryDataManager",
    "ProgressiveLoadingService",
    "SequenceSorterService",
    "ThumbnailFactoryService",
]
