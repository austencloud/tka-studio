#!/usr/bin/env python3
"""
Quick test script to verify sequence card service registration is working.
"""

import sys
import os
from pathlib import Path

# Add the source path
sys.path.insert(0, str(Path(__file__).parent / "src" / "desktop" / "modern" / "src"))


def test_sequence_card_registration():
    """Test that sequence card services can be registered without metaclass conflicts."""
    try:
        print("🔧 Testing sequence card service registration...")

        from core.dependency_injection.di_container import DIContainer
        from core.dependency_injection.sequence_card_service_registration import (
            register_sequence_card_services,
        )

        # Create container and register services
        container = DIContainer()
        register_sequence_card_services(container)

        print(
            "✅ SUCCESS: Sequence card services registered without metaclass conflict!"
        )

        # Test SequenceCardTab resolution
        from presentation.tabs.sequence_card.sequence_card_tab import SequenceCardTab

        tab = container.resolve(SequenceCardTab)

        print("✅ SUCCESS: SequenceCardTab resolved successfully!")
        print(f"✅ Tab type: {type(tab)}")

        # Test individual service resolution
        from core.interfaces.sequence_card_services import (
            ISequenceCardDataService,
            ISequenceCardCacheService,
            ISequenceCardLayoutService,
            ISequenceCardDisplayService,
            ISequenceCardExportService,
            ISequenceCardSettingsService,
        )

        services = {
            "Data Service": ISequenceCardDataService,
            "Cache Service": ISequenceCardCacheService,
            "Layout Service": ISequenceCardLayoutService,
            "Display Service": ISequenceCardDisplayService,
            "Export Service": ISequenceCardExportService,
            "Settings Service": ISequenceCardSettingsService,
        }

        for name, interface in services.items():
            service = container.resolve(interface)
            print(f"✅ {name}: {type(service).__name__}")

        print("\n🎉 ALL TESTS PASSED! Sequence Card Tab is ready for use!")
        return True

    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_sequence_card_registration()
    sys.exit(0 if success else 1)
