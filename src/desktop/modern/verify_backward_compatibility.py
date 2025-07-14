"""
Step 6: Backward Compatibility Verification

Verify that components work without injected services (backward compatibility).
"""

import inspect
import sys
from pathlib import Path

# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def verify_backward_compatibility():
    """Verify that components work without injected services."""
    print("🔄 Verifying Backward Compatibility...")

    tests_passed = 0
    total_tests = 0

    # Test imports first
    total_tests += 1
    try:
        from presentation.components.start_position_picker.advanced_start_position_picker import (
            AdvancedStartPositionPicker,
        )
        from presentation.components.start_position_picker.enhanced_start_position_picker import (
            EnhancedStartPositionPicker,
        )
        from presentation.components.start_position_picker.start_position_option import (
            StartPositionOption,
        )
        from presentation.components.start_position_picker.start_position_picker import (
            StartPositionPicker,
        )

        print("  ✅ All component imports successful")
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ Component imports failed: {e}")
        return tests_passed, total_tests

    # Test StartPositionOption backward compatibility
    total_tests += 1
    try:
        sig = inspect.signature(StartPositionOption.__init__)
        params = sig.parameters

        # Check if data_service parameter has a default value (None)
        data_service_param = params.get("data_service")
        if data_service_param:
            has_default = data_service_param.default is not inspect.Parameter.empty
            assert has_default, "data_service parameter should have a default value"
            print(
                "  ✅ StartPositionOption has backward compatibility (data_service=None)"
            )
        else:
            print(
                "  ✅ StartPositionOption has backward compatibility (no data_service param)"
            )
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ StartPositionOption backward compatibility failed: {e}")

    # Test StartPositionPicker backward compatibility
    total_tests += 1
    try:
        sig = inspect.signature(StartPositionPicker.__init__)
        params = sig.parameters

        # Check if service parameters have default values
        service_params = [
            "data_service",
            "selection_service",
            "ui_service",
            "orchestrator",
        ]
        backward_compatible = True

        for param_name in service_params:
            if param_name in params:
                param = params[param_name]
                if param.default is inspect.Parameter.empty:
                    backward_compatible = False
                    break

        assert backward_compatible, "Service parameters should have default values"
        print(
            "  ✅ StartPositionPicker has backward compatibility (service params have defaults)"
        )
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ StartPositionPicker backward compatibility failed: {e}")

    # Test EnhancedStartPositionPicker backward compatibility
    total_tests += 1
    try:
        sig = inspect.signature(EnhancedStartPositionPicker.__init__)
        params = sig.parameters

        # Check if service parameters have default values
        service_params = [
            "data_service",
            "selection_service",
            "ui_service",
            "orchestrator",
        ]
        backward_compatible = True

        for param_name in service_params:
            if param_name in params:
                param = params[param_name]
                if param.default is inspect.Parameter.empty:
                    backward_compatible = False
                    break

        assert backward_compatible, "Service parameters should have default values"
        print(
            "  ✅ EnhancedStartPositionPicker has backward compatibility (service params have defaults)"
        )
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ EnhancedStartPositionPicker backward compatibility failed: {e}")

    # Test AdvancedStartPositionPicker backward compatibility
    total_tests += 1
    try:
        sig = inspect.signature(AdvancedStartPositionPicker.__init__)
        params = sig.parameters

        # Check if service parameters have default values
        service_params = [
            "data_service",
            "selection_service",
            "ui_service",
            "orchestrator",
        ]
        backward_compatible = True

        for param_name in service_params:
            if param_name in params:
                param = params[param_name]
                if param.default is inspect.Parameter.empty:
                    backward_compatible = False
                    break

        assert backward_compatible, "Service parameters should have default values"
        print(
            "  ✅ AdvancedStartPositionPicker has backward compatibility (service params have defaults)"
        )
        tests_passed += 1
    except Exception as e:
        print(f"  ❌ AdvancedStartPositionPicker backward compatibility failed: {e}")

    print(f"\n📊 Backward Compatibility: {tests_passed}/{total_tests} tests passed")
    return tests_passed == total_tests


if __name__ == "__main__":
    success = verify_backward_compatibility()
    if success:
        print("🎉 BACKWARD COMPATIBILITY MAINTAINED!")
    else:
        print("❌ BACKWARD COMPATIBILITY ISSUES FOUND!")
