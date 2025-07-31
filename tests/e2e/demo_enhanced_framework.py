#!/usr/bin/env python3
"""
TKA Modern E2E Framework Demo Script

This script demonstrates the enhanced features of the modern E2E testing framework:
- pytest-qt integration
- Performance monitoring
- Builder patterns
- Custom assertions
- Enhanced reporting

Run with: python demo_enhanced_framework.py
"""

from pathlib import Path
import subprocess
import sys


def print_banner():
    """Print demo banner."""
    print("=" * 60)
    print("🚀 TKA MODERN E2E FRAMEWORK DEMO")
    print("=" * 60)
    print("This demo showcases the enhanced testing framework features:")
    print("✅ pytest-qt integration for better Qt testing")
    print("✅ Performance monitoring and reporting")
    print("✅ Builder pattern for flexible test data")
    print("✅ Custom assertions with rich error messages")
    print("✅ Professional test organization and markers")
    print("=" * 60)
    print()


def check_requirements():
    """Check if required packages are installed."""
    print("📋 Checking requirements...")

    required_packages = ["pytest", "pytest-qt", "pytest-html", "pytest-cov", "PyQt6"]

    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package}")

    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("Install with: pip install pytest pytest-qt pytest-html pytest-cov PyQt6")
        return False

    print("✅ All requirements satisfied!")
    return True


def run_smoke_tests():
    """Run smoke tests to verify basic functionality."""
    print("\n🔥 Running smoke tests...")

    cmd = [
        "pytest",
        "tests/e2e/workflows/test_sequence_building.py::TestSequenceBuilding::test_basic_sequence_creation",
        "-v",
        "-m",
        "not slow",
        "--tb=short",
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=Path.cwd())
        if result.returncode == 0:
            print("✅ Smoke tests passed!")
        else:
            print("❌ Smoke tests failed:")
            print(result.stdout)
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running smoke tests: {e}")
        return False


def run_enhanced_features_demo():
    """Run tests demonstrating enhanced features."""
    print("\n🎯 Running enhanced features demo...")

    cmd = [
        "pytest",
        "tests/e2e/workflows/test_sequence_building.py::TestSequenceBuilding::test_enhanced_builder_pattern",
        "tests/e2e/workflows/test_sequence_building.py::TestSequenceBuilding::test_performance_sequence_builder",
        "-v",
        "--tb=short",
        "--capture=no",  # Show all output including performance monitoring
    ]

    try:
        result = subprocess.run(cmd, cwd=Path.cwd())
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running enhanced features: {e}")
        return False


def run_performance_tests():
    """Run performance tests with monitoring."""
    print("\n⚡ Running performance tests with monitoring...")

    cmd = ["pytest", "tests/e2e/workflows/", "-m", "performance", "-v", "--tb=short"]

    try:
        result = subprocess.run(cmd, cwd=Path.cwd())
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running performance tests: {e}")
        return False


def generate_comprehensive_report():
    """Generate comprehensive test report."""
    print("\n📊 Generating comprehensive test report...")

    # Create reports directory
    reports_dir = Path("test_reports")
    reports_dir.mkdir(exist_ok=True)

    cmd = [
        "pytest",
        "tests/e2e/workflows/test_sequence_building.py",
        "--html=test_reports/enhanced_framework_demo.html",
        "--self-contained-html",
        "--tb=short",
        "-v",
    ]

    try:
        result = subprocess.run(cmd, cwd=Path.cwd())
        if result.returncode == 0:
            report_path = Path.cwd() / "test_reports" / "enhanced_framework_demo.html"
            print(f"✅ Report generated: {report_path}")
            print(f"   Open in browser: file://{report_path}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        return False


def show_builder_pattern_examples():
    """Show builder pattern examples."""
    print("\n🏗️  Builder Pattern Examples:")
    print("-" * 40)

    examples = [
        """
# Simple sequence
sequence_spec = simple_sequence(length=3, position="alpha1_alpha1")
        """,
        """
# Performance test sequence  
perf_spec = performance_sequence(length=10)
        """,
        """
# Complex sequence with validation
sequence_spec = (SequenceBuilder()
                .with_start_position("beta5_beta5")
                .with_length(4)
                .with_validation_rules({"valid": True, "min_length": 3})
                .with_metadata({"test_type": "integration"})
                .build())
        """,
        """
# Error case testing
error_spec = (SequenceBuilder()
             .for_error_case_test()
             .with_expected_result("failure")
             .build())
        """,
    ]

    for i, example in enumerate(examples, 1):
        print(f"Example {i}:{example}")


def show_custom_assertions_examples():
    """Show custom assertions examples."""
    print("\n🧪 Custom Assertions Examples:")
    print("-" * 40)

    examples = [
        """
# Domain-specific assertions with rich error messages
assert_tka.sequence_has_length(workbench, 3)
assert_tka.sequence_is_valid(workbench)
assert_tka.options_available(option_picker, min_count=5)
assert_tka.component_loaded(picker, "Start Position Picker")
        """,
        """
# Workflow assertions
assert_sequence_workflow_success(nav_result, seq_result, val_result, 
                                context="my_test")
        """,
        """
# State transition assertions
assert_state_transition(initial_state, final_state, 
                       {"length": 3, "valid": True}, 
                       context="sequence_building")
        """,
    ]

    for i, example in enumerate(examples, 1):
        print(f"Example {i}:{example}")


def main():
    """Main demo function."""
    print_banner()

    # Check requirements
    if not check_requirements():
        return 1

    # Show examples
    show_builder_pattern_examples()
    show_custom_assertions_examples()

    print("\n" + "=" * 60)
    print("🎬 RUNNING LIVE DEMO")
    print("=" * 60)

    # Run demos
    success = True

    # Basic smoke test
    if not run_smoke_tests():
        success = False

    # Enhanced features
    if not run_enhanced_features_demo():
        success = False

    # Performance tests
    if not run_performance_tests():
        success = False

    # Generate report
    if not generate_comprehensive_report():
        success = False

    # Final summary
    print("\n" + "=" * 60)
    if success:
        print("🎉 DEMO COMPLETED SUCCESSFULLY!")
        print("Your modern E2E framework is ready for production use!")
        print("\nNext steps:")
        print("1. Migrate legacy tests using the new patterns")
        print("2. Add more page objects for other UI components")
        print("3. Expand builders for complex test scenarios")
        print("4. Integrate with CI/CD pipeline")
    else:
        print("❌ DEMO HAD ISSUES")
        print("Check the output above for specific failures")

    print("=" * 60)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
