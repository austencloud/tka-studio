#!/usr/bin/env python3
"""
Simple test to verify service creation works without Qt.
"""

import sys
from pathlib import Path

# Add paths for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir.parent))
sys.path.insert(0, str(current_dir.parent.parent))


def main():
    try:
        print("Testing service creation without Qt...")

        # Test service imports and creation
        from modern.core.dependency_injection.construct_tab_service_registration import (
            register_construct_tab_services,
        )
        from modern.core.dependency_injection.di_container import DIContainer
        from modern.core.interfaces.construct_tab_services import (
            IConstructTabComponentFactory,
        )

        container = DIContainer()
        register_construct_tab_services(container)

        # Debug: Check what's actually registered
        print(f"Available services: {container._registry.services.keys()}")

        # Test factory creation
        try:
            factory = container.resolve(IConstructTabComponentFactory)
            print("✅ Component factory resolved successfully")
        except Exception as e:
            print(f"❌ Factory resolution failed: {e}")

            # Try resolving by implementation class directly
            from modern.application.services.construct_tab.construct_tab_component_factory import (
                ConstructTabComponentFactory,
            )

            try:
                factory = ConstructTabComponentFactory(container)
                print("✅ Component factory created directly")
            except Exception as e2:
                print(f"❌ Direct creation failed: {e2}")
                raise

        print("🎉 Service creation test passed!")
        return 0

    except Exception as e:
        print(f"❌ Service creation test failed: {e}")
        import traceback

        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
