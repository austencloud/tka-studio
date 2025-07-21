"""
Sequence Card Test Package

Complete test suite for sequence card tab functionality.
"""

# Export test classes for pytest discovery
from .test_sequence_card_services import (
    TestSequenceCardDataService,
    TestSequenceCardCacheService,
    TestSequenceCardLayoutService,
    TestSequenceCardSettingsService,
    TestSequenceCardExportService,
    TestSequenceCardDisplayService,
    TestSequenceCardServiceIntegration,
)

from .test_sequence_card_ui import (
    TestSequenceCardHeaderComponent,
    TestSequenceCardNavigationComponent, 
    TestSequenceCardContentComponent,
    TestSequenceCardTab,
    TestSequenceCardVisualRegression,
    TestSequenceCardPerformance,
)

from .test_sequence_card_integration import (
    TestSequenceCardServiceRegistration,
    TestSequenceCardTabIntegration,
    TestSequenceCardRealWorldScenarios,
    TestSequenceCardPerformanceIntegration,
)

__all__ = [
    # Service tests
    "TestSequenceCardDataService",
    "TestSequenceCardCacheService", 
    "TestSequenceCardLayoutService",
    "TestSequenceCardSettingsService",
    "TestSequenceCardExportService",
    "TestSequenceCardDisplayService",
    "TestSequenceCardServiceIntegration",
    
    # UI tests
    "TestSequenceCardHeaderComponent",
    "TestSequenceCardNavigationComponent",
    "TestSequenceCardContentComponent", 
    "TestSequenceCardTab",
    "TestSequenceCardVisualRegression",
    "TestSequenceCardPerformance",
    
    # Integration tests
    "TestSequenceCardServiceRegistration",
    "TestSequenceCardTabIntegration",
    "TestSequenceCardRealWorldScenarios", 
    "TestSequenceCardPerformanceIntegration",
]
