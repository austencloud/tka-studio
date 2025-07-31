#!/usr/bin/env python3
"""
Quick verification script to test if generation services are working.
"""

import sys

# Add paths for imports
sys.path.insert(0, "src/desktop/modern")
sys.path.insert(0, "src")


def test_generation_service_registration():
    """Test if generation services are properly registered."""
    print("🔧 Testing generation service registration...")

    try:
        # Create application container
        from desktop.modern.core.application.application_factory import (
            ApplicationFactory,
        )

        container = ApplicationFactory.create_production_app()
        print("✅ Application container created successfully")

        # Try to resolve IGenerationService
        from desktop.modern.core.interfaces.generation_services import (
            IGenerationService,
        )

        service = container.resolve(IGenerationService)

        if service:
            print(f"✅ SUCCESS: IGenerationService resolved! Type: {type(service)}")

            # Test service methods
            if hasattr(service, "generate_freeform_sequence"):
                print("✅ Service has generate_freeform_sequence method")
            if hasattr(service, "generate_circular_sequence"):
                print("✅ Service has generate_circular_sequence method")

            return True
        else:
            print("❌ FAILED: IGenerationService resolved to None")
            return False

    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_generation_config():
    """Test if generation configuration classes work."""
    print("\n🔧 Testing generation configuration...")

    try:
        from desktop.modern.core.interfaces.generation_services import (
            GenerationMode,
            LetterType,
            PropContinuity,
        )
        from desktop.modern.domain.models.generation_models import GenerationConfig

        # Create a test config
        config = GenerationConfig(
            mode=GenerationMode.FREEFORM,
            length=4,
            level=1,
            turn_intensity=1.0,
            prop_continuity=PropContinuity.CONTINUOUS,
            letter_types={LetterType.TYPE1, LetterType.TYPE2},
        )

        print(f"✅ GenerationConfig created successfully: {config.mode}")
        return True

    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all verification tests."""
    print("🎯 Generation Services Verification")
    print("=" * 50)

    tests = [
        test_generation_service_registration,
        test_generation_config,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")

    print("\n" + "=" * 50)
    print(f"🎯 VERIFICATION SUMMARY: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED - GENERATION SERVICES ARE WORKING!")
        return True
    else:
        print("❌ SOME TESTS FAILED - GENERATION SERVICES NEED MORE WORK")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
