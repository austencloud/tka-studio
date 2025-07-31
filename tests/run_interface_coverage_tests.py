#!/usr/bin/env python3
"""
Interface Coverage Test Runner

This script runs the comprehensive interface coverage test suite and generates
a detailed report showing the TKA application's readiness for web platform migration.

Usage:
    python tests/run_interface_coverage_tests.py
    python tests/run_interface_coverage_tests.py --phase 1
    python tests/run_interface_coverage_tests.py --verbose
    python tests/run_interface_coverage_tests.py --report-only
"""

import argparse
from pathlib import Path
import sys
import time
from typing import Any, Dict

# Add src to path for imports
sys.path.insert(
    0, str(Path(__file__).parent.parent / "src" / "desktop" / "modern" / "src")
)


class InterfaceCoverageTestRunner:
    """Runs comprehensive interface coverage tests and generates reports."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.results: Dict[str, Any] = {}
        self.start_time = time.time()

    def run_phase_1_tests(self) -> Dict[str, Any]:
        """Run Phase 1: Interface Coverage Verification tests."""
        print("🔍 Phase 1: Interface Coverage Verification")
        print("=" * 50)

        phase_results = {
            "phase": 1,
            "name": "Interface Coverage Verification",
            "tests": [],
            "passed": 0,
            "failed": 0,
            "errors": [],
        }

        try:
            # Import and run Phase 1 tests
            from interface_coverage.test_complete_coverage import (
                test_all_services_have_interfaces,
                test_interface_files_exist,
                test_no_abstract_method_errors,
            )

            tests = [
                ("Interface Files Exist", test_interface_files_exist),
                ("Services Have Interfaces", test_all_services_have_interfaces),
                ("No Abstract Method Errors", test_no_abstract_method_errors),
            ]

            for test_name, test_func in tests:
                try:
                    print(f"\n🧪 Running: {test_name}")
                    test_func()
                    phase_results["tests"].append(
                        {"name": test_name, "status": "PASSED"}
                    )
                    phase_results["passed"] += 1
                    print(f"✅ {test_name} - PASSED")
                except AssertionError as e:
                    phase_results["tests"].append(
                        {"name": test_name, "status": "FAILED", "error": str(e)}
                    )
                    phase_results["failed"] += 1
                    phase_results["errors"].append(f"{test_name}: {e}")
                    print(f"❌ {test_name} - FAILED: {e}")
                except Exception as e:
                    phase_results["tests"].append(
                        {"name": test_name, "status": "ERROR", "error": str(e)}
                    )
                    phase_results["failed"] += 1
                    phase_results["errors"].append(f"{test_name}: {e}")
                    print(f"💥 {test_name} - ERROR: {e}")

        except ImportError as e:
            phase_results["errors"].append(f"Failed to import Phase 1 tests: {e}")
            print(f"💥 Failed to import Phase 1 tests: {e}")

        return phase_results

    def run_phase_2_tests(self) -> Dict[str, Any]:
        """Run Phase 2: Interface Quality and Compatibility tests."""
        print("\n📝 Phase 2: Interface Quality and Compatibility")
        print("=" * 50)

        phase_results = {
            "phase": 2,
            "name": "Interface Quality and Compatibility",
            "tests": [],
            "passed": 0,
            "failed": 0,
            "errors": [],
        }

        try:
            from interface_completeness.test_interface_quality import (
                test_all_interfaces_have_web_notes,
                test_interface_file_structure,
                test_interface_method_signatures,
                test_no_qt_imports_in_interfaces,
                test_web_compatible_types,
            )

            tests = [
                ("No Qt Imports", test_no_qt_imports_in_interfaces),
                ("Web Compatible Types", test_web_compatible_types),
                ("Interface File Structure", test_interface_file_structure),
                ("Method Signatures", test_interface_method_signatures),
                ("Web Implementation Notes", test_all_interfaces_have_web_notes),
            ]

            for test_name, test_func in tests:
                try:
                    print(f"\n🧪 Running: {test_name}")
                    test_func()
                    phase_results["tests"].append(
                        {"name": test_name, "status": "PASSED"}
                    )
                    phase_results["passed"] += 1
                    print(f"✅ {test_name} - PASSED")
                except AssertionError as e:
                    phase_results["tests"].append(
                        {"name": test_name, "status": "FAILED", "error": str(e)}
                    )
                    phase_results["failed"] += 1
                    phase_results["errors"].append(f"{test_name}: {e}")
                    print(f"❌ {test_name} - FAILED: {e}")
                except Exception as e:
                    phase_results["tests"].append(
                        {"name": test_name, "status": "ERROR", "error": str(e)}
                    )
                    phase_results["failed"] += 1
                    phase_results["errors"].append(f"{test_name}: {e}")
                    print(f"💥 {test_name} - ERROR: {e}")

        except ImportError as e:
            phase_results["errors"].append(f"Failed to import Phase 2 tests: {e}")
            print(f"💥 Failed to import Phase 2 tests: {e}")

        return phase_results

    def run_phase_3_tests(self) -> Dict[str, Any]:
        """Run Phase 3: Service Implementation and DI tests."""
        print("\n🔧 Phase 3: Service Implementation and DI")
        print("=" * 50)

        phase_results = {
            "phase": 3,
            "name": "Service Implementation and DI",
            "tests": [],
            "passed": 0,
            "failed": 0,
            "errors": [],
        }

        try:
            from service_implementation.test_service_interfaces import (
                test_concrete_services_implement_interfaces,
                test_dependency_injection_compatibility,
                test_interface_inheritance_patterns,
                test_service_registration_system,
            )

            tests = [
                (
                    "Service Interface Implementation",
                    test_concrete_services_implement_interfaces,
                ),
                ("Dependency Injection", test_dependency_injection_compatibility),
                ("Service Registration", test_service_registration_system),
                ("Interface Inheritance", test_interface_inheritance_patterns),
            ]

            for test_name, test_func in tests:
                try:
                    print(f"\n🧪 Running: {test_name}")
                    test_func()
                    phase_results["tests"].append(
                        {"name": test_name, "status": "PASSED"}
                    )
                    phase_results["passed"] += 1
                    print(f"✅ {test_name} - PASSED")
                except AssertionError as e:
                    phase_results["tests"].append(
                        {"name": test_name, "status": "FAILED", "error": str(e)}
                    )
                    phase_results["failed"] += 1
                    phase_results["errors"].append(f"{test_name}: {e}")
                    print(f"❌ {test_name} - FAILED: {e}")
                except Exception as e:
                    phase_results["tests"].append(
                        {"name": test_name, "status": "ERROR", "error": str(e)}
                    )
                    phase_results["failed"] += 1
                    phase_results["errors"].append(f"{test_name}: {e}")
                    print(f"💥 {test_name} - ERROR: {e}")

        except ImportError as e:
            phase_results["errors"].append(f"Failed to import Phase 3 tests: {e}")
            print(f"💥 Failed to import Phase 3 tests: {e}")

        return phase_results

    def run_phase_4_tests(self) -> Dict[str, Any]:
        """Run Phase 4: Cross-Platform Web Compatibility tests."""
        print("\n🌐 Phase 4: Cross-Platform Web Compatibility")
        print("=" * 50)

        phase_results = {
            "phase": 4,
            "name": "Cross-Platform Web Compatibility",
            "tests": [],
            "passed": 0,
            "failed": 0,
            "errors": [],
        }

        try:
            from cross_platform.test_web_compatibility import (
                test_async_compatibility,
                test_browser_api_compatibility,
                test_json_serialization_examples,
                test_serializable_data_types,
                test_web_framework_integration,
            )

            tests = [
                ("JSON Serialization", test_json_serialization_examples),
                ("Serializable Data Types", test_serializable_data_types),
                ("Async Compatibility", test_async_compatibility),
                ("Browser API Compatibility", test_browser_api_compatibility),
                ("Web Framework Integration", test_web_framework_integration),
            ]

            for test_name, test_func in tests:
                try:
                    print(f"\n🧪 Running: {test_name}")
                    test_func()
                    phase_results["tests"].append(
                        {"name": test_name, "status": "PASSED"}
                    )
                    phase_results["passed"] += 1
                    print(f"✅ {test_name} - PASSED")
                except AssertionError as e:
                    phase_results["tests"].append(
                        {"name": test_name, "status": "FAILED", "error": str(e)}
                    )
                    phase_results["failed"] += 1
                    phase_results["errors"].append(f"{test_name}: {e}")
                    print(f"❌ {test_name} - FAILED: {e}")
                except Exception as e:
                    phase_results["tests"].append(
                        {"name": test_name, "status": "ERROR", "error": str(e)}
                    )
                    phase_results["failed"] += 1
                    phase_results["errors"].append(f"{test_name}: {e}")
                    print(f"💥 {test_name} - ERROR: {e}")

        except ImportError as e:
            phase_results["errors"].append(f"Failed to import Phase 4 tests: {e}")
            print(f"💥 Failed to import Phase 4 tests: {e}")

        return phase_results

    def run_phase_5_tests(self) -> Dict[str, Any]:
        """Run Phase 5: Integration and Workflow tests."""
        print("\n🔄 Phase 5: Integration and Workflow Tests")
        print("=" * 50)

        phase_results = {
            "phase": 5,
            "name": "Integration and Workflow Tests",
            "tests": [],
            "passed": 0,
            "failed": 0,
            "errors": [],
        }

        try:
            from integration.test_interface_workflows import (
                test_complete_user_workflows,
                test_data_flow_integration,
                test_interface_coverage_completeness,
                test_mock_web_implementation_scenario,
                test_service_coordination,
            )

            tests = [
                ("User Workflows", test_complete_user_workflows),
                ("Service Coordination", test_service_coordination),
                ("Data Flow Integration", test_data_flow_integration),
                ("Coverage Completeness", test_interface_coverage_completeness),
                ("Mock Web Implementation", test_mock_web_implementation_scenario),
            ]

            for test_name, test_func in tests:
                try:
                    print(f"\n🧪 Running: {test_name}")
                    test_func()
                    phase_results["tests"].append(
                        {"name": test_name, "status": "PASSED"}
                    )
                    phase_results["passed"] += 1
                    print(f"✅ {test_name} - PASSED")
                except AssertionError as e:
                    phase_results["tests"].append(
                        {"name": test_name, "status": "FAILED", "error": str(e)}
                    )
                    phase_results["failed"] += 1
                    phase_results["errors"].append(f"{test_name}: {e}")
                    print(f"❌ {test_name} - FAILED: {e}")
                except Exception as e:
                    phase_results["tests"].append(
                        {"name": test_name, "status": "ERROR", "error": str(e)}
                    )
                    phase_results["failed"] += 1
                    phase_results["errors"].append(f"{test_name}: {e}")
                    print(f"💥 {test_name} - ERROR: {e}")

        except ImportError as e:
            phase_results["errors"].append(f"Failed to import Phase 5 tests: {e}")
            print(f"💥 Failed to import Phase 5 tests: {e}")

        return phase_results

    def run_all_phases(self, specific_phase: int = None) -> Dict[str, Any]:
        """Run all test phases or a specific phase."""
        print("🚀 TKA Interface Coverage Test Suite")
        print("=" * 60)
        print("Testing 100% interface coverage for web platform portability")
        print("=" * 60)

        all_results = {
            "start_time": self.start_time,
            "phases": [],
            "total_tests": 0,
            "total_passed": 0,
            "total_failed": 0,
            "overall_success": False,
        }

        phases = [
            (1, self.run_phase_1_tests),
            (2, self.run_phase_2_tests),
            (3, self.run_phase_3_tests),
            (4, self.run_phase_4_tests),
            (5, self.run_phase_5_tests),
        ]

        for phase_num, phase_func in phases:
            if specific_phase is None or specific_phase == phase_num:
                phase_results = phase_func()
                all_results["phases"].append(phase_results)
                all_results["total_tests"] += len(phase_results["tests"])
                all_results["total_passed"] += phase_results["passed"]
                all_results["total_failed"] += phase_results["failed"]

        all_results["end_time"] = time.time()
        all_results["duration"] = all_results["end_time"] - all_results["start_time"]
        all_results["overall_success"] = all_results["total_failed"] == 0

        return all_results

    def generate_report(self, results: Dict[str, Any]) -> str:
        """Generate a comprehensive test report."""
        report = []
        report.append("🎯 TKA INTERFACE COVERAGE TEST REPORT")
        report.append("=" * 60)
        report.append(f"Test Duration: {results['duration']:.2f} seconds")
        report.append(f"Total Tests: {results['total_tests']}")
        report.append(f"Passed: {results['total_passed']}")
        report.append(f"Failed: {results['total_failed']}")

        if results["overall_success"]:
            report.append(
                "🎉 OVERALL RESULT: SUCCESS - 100% Interface Coverage Achieved!"
            )
        else:
            report.append("⚠️ OVERALL RESULT: Issues Found - See Details Below")

        report.append("")

        # Phase-by-phase results
        for phase in results["phases"]:
            report.append(f"📋 Phase {phase['phase']}: {phase['name']}")
            report.append("-" * 40)
            report.append(
                f"Tests: {len(phase['tests'])} | Passed: {phase['passed']} | Failed: {phase['failed']}"
            )

            if phase["errors"]:
                report.append("❌ Issues Found:")
                for error in phase["errors"]:
                    report.append(f"   - {error}")
            else:
                report.append("✅ All tests passed!")

            report.append("")

        # Summary and next steps
        report.append("📊 SUMMARY")
        report.append("-" * 20)

        if results["overall_success"]:
            report.append("✅ Interface Coverage: 100%")
            report.append("✅ Cross-Platform Compatibility: PASS")
            report.append("✅ DI Integration: PASS")
            report.append("✅ Web Platform Ready: YES")
            report.append("")
            report.append("🚀 NEXT STEPS:")
            report.append("1. Begin web platform implementation")
            report.append("2. Create web-specific service implementations")
            report.append("3. Implement browser-based UI layer")
            report.append("4. Set up web deployment pipeline")
        else:
            report.append("⚠️ Interface Coverage: Needs Improvement")
            report.append("⚠️ Issues Found: See phase details above")
            report.append("")
            report.append("🔧 RECOMMENDED ACTIONS:")
            report.append("1. Fix failing tests in priority order")
            report.append("2. Add missing interface implementations")
            report.append("3. Resolve DI registration issues")
            report.append("4. Re-run tests until 100% pass rate achieved")

        return "\n".join(report)


def main():
    """Main entry point for the test runner."""
    parser = argparse.ArgumentParser(description="Run TKA Interface Coverage Tests")
    parser.add_argument(
        "--phase", type=int, choices=[1, 2, 3, 4, 5], help="Run specific phase only"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "--report-only", action="store_true", help="Generate report from previous run"
    )

    args = parser.parse_args()

    runner = InterfaceCoverageTestRunner(verbose=args.verbose)

    if not args.report_only:
        results = runner.run_all_phases(specific_phase=args.phase)
    else:
        # Load previous results if available
        results = {
            "phases": [],
            "total_tests": 0,
            "total_passed": 0,
            "total_failed": 0,
            "overall_success": False,
        }

    # Generate and display report
    report = runner.generate_report(results)
    print("\n" + report)

    # Save report to file
    report_file = Path("interface_coverage_report.txt")
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n📄 Report saved to: {report_file}")

    # Exit with appropriate code
    sys.exit(0 if results["overall_success"] else 1)


if __name__ == "__main__":
    main()
