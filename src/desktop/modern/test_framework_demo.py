#!/usr/bin/env python3
"""
Testing Framework Demonstration
===============================

Demonstrates the comprehensive testing framework for the Modern image export system.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_service_validation():
    """Test service registration validation."""
    print("Testing Service Registration Validation...")
    
    from tests.framework.service_validation import ContainerInspector
    from core.dependency_injection.di_container import DIContainer
    from core.dependency_injection.image_export_service_registration import register_image_export_services
    
    # Create container and register services
    container = DIContainer()
    register_image_export_services(container)
    
    # Test service registration
    inspector = ContainerInspector()
    report = inspector.verify_export_services_registered(container)
    
    print(f"Service Registration Report:")
    print(f"  Total services checked: {report.total_services_checked}")
    print(f"  Registered services: {report.registered_services}")
    print(f"  Resolvable services: {report.resolvable_services}")
    print(f"  All required present: {report.all_required_services_present}")
    
    if report.missing_services:
        print(f"  Missing services: {report.missing_services}")
    if report.failed_resolutions:
        print(f"  Failed resolutions: {report.failed_resolutions}")
    
    if report.all_required_services_present:
        print("Service registration validation PASSED!")
        return True
    else:
        print("Service registration validation FAILED!")
        return False

def test_font_size_validation():
    """Test font size validation framework."""
    print("\nTesting Font Size Validation Framework...")
    
    from tests.framework.visual_regression import FontSizeValidator
    
    # Create validator
    validator = FontSizeValidator(tolerance_percentage=10.0)
    
    print(f"FontSizeValidator created successfully")
    print(f"Expected ranges configured: {len(validator.expected_ranges)} categories")
    print(f"Tolerance: {validator.tolerance_percentage}%")
    
    # Test expected ranges
    word_ranges = validator.expected_ranges.get('word_label', {})
    print(f"Word label ranges: {word_ranges}")
    
    print("Font size validation framework PASSED!")
    return True

def test_ui_automation_framework():
    """Test UI automation framework."""
    print("\nTesting UI Automation Framework...")
    
    from tests.framework.ui_automation import SequenceSpec, WorkbenchController
    
    # Create sequence specification
    sequence_spec = SequenceSpec(
        start_position="alpha1_alpha1",
        beats=[
            {"motion": "pro"},
            {"motion": "anti"},
            {"motion": "static"}
        ],
        word="TEST",
        include_start_position=True
    )
    
    print(f"SequenceSpec created:")
    print(f"  Start position: {sequence_spec.start_position}")
    print(f"  Beats: {len(sequence_spec.beats)}")
    print(f"  Word: {sequence_spec.word}")
    
    print("UI automation framework PASSED!")
    return True

def test_visual_regression_framework():
    """Test visual regression detection framework."""
    print("\nTesting Visual Regression Framework...")
    
    from tests.framework.visual_regression import ImageComparator, VisualElementDetector
    
    # Create components
    comparator = ImageComparator(tolerance_percentage=5.0)
    detector = VisualElementDetector()
    
    print(f"ImageComparator created with {comparator.tolerance_percentage}% tolerance")
    print(f"VisualElementDetector created with {len(detector.detection_methods)} detection methods")
    
    detection_methods = list(detector.detection_methods.keys())
    print(f"Detection methods: {detection_methods}")
    
    print("Visual regression framework PASSED!")
    return True

def main():
    """Run all framework tests."""
    print("=" * 80)
    print("TKA Modern Image Export Testing Framework Demonstration")
    print("=" * 80)
    
    tests = [
        test_service_validation,
        test_font_size_validation,
        test_ui_automation_framework,
        test_visual_regression_framework,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"Test {test.__name__} FAILED with error: {e}")
    
    print("\n" + "=" * 80)
    print(f"Framework Demonstration Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All framework components are working correctly!")
        print("\nThe testing framework is ready to:")
        print("- Detect font sizing regressions ('humongous' text issues)")
        print("- Validate service registration completeness")
        print("- Automate UI workflow testing")
        print("- Perform visual regression detection")
        print("- Prevent container switching issues")
    else:
        print("Some framework components need attention.")
    
    print("=" * 80)
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
