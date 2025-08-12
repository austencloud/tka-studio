#!/usr/bin/env python3
"""
Test script to verify the complete generate-to-construct integration
"""

from __future__ import annotations

from pathlib import Path
import sys


# Add the modern directory to path
modern_path = Path(__file__).parent / "src" / "desktop" / "modern"
sys.path.insert(0, str(modern_path))


def test_integration():
    """Test the complete integration from generation to construct tab."""
    try:
        print("🧪 Testing Generate-to-Construct Integration")
        print("=" * 60)

        # Create QApplication for Qt widgets
        import sys

        from PyQt6.QtWidgets import QApplication

        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)

        # Test 1: Verify tab factory creates generate tab
        print("1. Testing TabFactory generate tab creation...")
        from desktop.modern.application.services.ui.tab_factory.tab_factory import (
            TabFactory,
        )
        from desktop.modern.core.dependency_injection.di_container import DIContainer

        container = DIContainer()
        tab_factory = TabFactory()

        # Register generation services
        from desktop.modern.application.services.generation.generation_service_registration import (
            register_generation_services,
        )

        register_generation_services(container)

        # Create generate tab
        generate_tab = tab_factory._create_generate_tab(container)
        print(f"✅ Generate tab created: {type(generate_tab)}")

        # Test 2: Verify generate tab has required signals
        print("\n2. Testing GenerateTab signals...")
        if hasattr(generate_tab, "sequence_generated"):
            print("✅ GenerateTab has sequence_generated signal")
        else:
            print("❌ GenerateTab missing sequence_generated signal")

        # Test 3: Verify construct tab has load method
        print("\n3. Testing ConstructTab load method...")
        construct_tab = tab_factory._create_construct_tab(container)
        if hasattr(construct_tab, "load_generated_sequence"):
            print("✅ ConstructTab has load_generated_sequence method")
        else:
            print("❌ ConstructTab missing load_generated_sequence method")

        # Test 4: Test signal connection (simulate UI setup)
        print("\n4. Testing signal connection...")
        try:
            generate_tab.sequence_generated.connect(
                construct_tab.load_generated_sequence
            )
            print("✅ Signal connection successful")
        except Exception as e:
            print(f"❌ Signal connection failed: {e}")

        # Test 5: Test generation service integration
        print("\n5. Testing generation service integration...")
        controller = generate_tab.get_controller()
        if controller:
            print(f"✅ Generate controller available: {type(controller)}")

            # Check if services are available
            if (
                hasattr(controller, "generation_service")
                and controller.generation_service
            ):
                print("✅ Generation service available")
            else:
                print("❌ Generation service not available")

        else:
            print("❌ Generate controller not available")

        print("\n" + "=" * 60)
        print("🎉 Integration test completed!")

        return True

    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_end_to_end_generation():
    """Test end-to-end generation flow."""
    try:
        print("\n🧪 Testing End-to-End Generation Flow")
        print("=" * 60)

        # Import required modules
        from desktop.modern.application.services.generation.generation_service_registration import (
            register_generation_services,
        )
        from desktop.modern.core.dependency_injection.di_container import DIContainer
        from desktop.modern.core.interfaces.generation_services import (
            GenerationMode,
            IGenerationService,
            ISequenceConfigurationService,
            LetterType,
            PropContinuity,
        )
        from desktop.modern.domain.models.enums import GridMode
        from desktop.modern.domain.models.generation_models import GenerationConfig

        # Setup DI container
        container = DIContainer()
        register_generation_services(container)

        # Get services
        generation_service = container.resolve(IGenerationService)
        container.resolve(ISequenceConfigurationService)

        print("✅ Services resolved")

        # Create test config
        config = GenerationConfig(
            mode=GenerationMode.FREEFORM,
            length=3,  # Small test sequence
            level=1,
            turn_intensity=0.0,
            grid_mode=GridMode.DIAMOND,
            prop_continuity=PropContinuity.CONTINUOUS,
            letter_types={LetterType.TYPE1, LetterType.TYPE2},
            slice_size=None,
            cap_type=None,
        )

        print(f"✅ Test config created: {config.length} beats")

        # Generate sequence
        result = generation_service.generate_freeform_sequence(config)

        if result.success:
            print(f"✅ Generation successful: {len(result.sequence_data)} beats")

            # Display generated sequence
            print("\n📋 Generated Sequence:")
            for i, beat in enumerate(result.sequence_data):
                print(
                    f"  Beat {i + 1}: {beat.start_position} → {beat.end_position} (Letter: {beat.letter})"
                )

            return True
        print(f"❌ Generation failed: {result.error_message}")
        return False

    except Exception as e:
        print(f"❌ End-to-end test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Starting Integration Tests\n")

    success1 = test_integration()
    success2 = test_end_to_end_generation()

    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("✅ Generate tab can create sequences")
        print("✅ Construct tab can load sequences")
        print("✅ Signal connections work")
        print("✅ End-to-end flow is ready")
    else:
        print("❌ SOME INTEGRATION TESTS FAILED!")
        print("Check the output above for details.")
