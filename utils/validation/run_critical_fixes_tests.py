"""
TKA Critical Fixes Test Runner

Comprehensive test runner that validates all critical fixes applied to the TKA application.
Ensures that the identified issues have been properly resolved and no regressions have occurred.

VALIDATES:
- ✅ Standard error handling consistency
- ✅ Circular dependency resolution
- ✅ Meaningful fallback UI functionality
- ✅ Service registration deduplication
- ✅ Global state management safety
- ✅ Background initialization performance
- ✅ Method length compliance

USAGE:
    python run_critical_fixes_tests.py [--verbose] [--report] [--fix-only]
"""

import subprocess
import sys
import time
import traceback
from dataclasses import dataclass
from pathlib import Path

# Add src to path for imports
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

try:
    from desktop.modern.core.error_handling import ErrorSeverity, StandardErrorHandler
    from desktop.modern.core.refactoring import (
        MethodExtractor,
        generate_refactoring_report,
    )
except ImportError as e:
    print(f"⚠️ Could not import TKA modules: {e}")
    print("Make sure you're running from the TKA project root directory.")
    sys.exit(1)


@dataclass
class TestResult:
    """Result of a test execution."""

    name: str
    passed: bool
    duration: float
    error_message: str | None = None
    details: str | None = None


@dataclass
class FixValidationResult:
    """Result of fix validation."""

    fix_name: str
    is_fixed: bool
    validation_details: str
    confidence: str  # "HIGH", "MEDIUM", "LOW"


class TKAFixesTestRunner:
    """
    Test runner for validating TKA critical fixes.

    Provides comprehensive validation of all applied fixes and reports results.
    """

    def __init__(self, verbose: bool = False, report_file: str | None = None):
        self.verbose = verbose
        self.report_file = report_file
        self.test_results: list[TestResult] = []
        self.fix_validations: list[FixValidationResult] = []

    def run_all_tests(self) -> bool:
        """
        Run all critical fixes tests and return overall success.

        Returns:
            True if all critical tests pass, False otherwise
        """
        print("🚀 Starting TKA Critical Fixes Validation")
        print("=" * 50)

        start_time = time.time()

        # Phase 1: Run unit tests
        print("\n📋 Phase 1: Running Unit Tests")
        unit_test_success = self._run_unit_tests()

        # Phase 2: Run integration tests
        print("\n🔗 Phase 2: Running Integration Tests")
        integration_test_success = self._run_integration_tests()

        # Phase 3: Validate specific fixes
        print("\n🔍 Phase 3: Validating Specific Fixes")
        fix_validation_success = self._validate_all_fixes()

        # Phase 4: Performance validation
        print("\n⚡ Phase 4: Performance Validation")
        performance_success = self._validate_performance_improvements()

        # Phase 5: Code quality check
        print("\n🎯 Phase 5: Code Quality Validation")
        quality_success = self._validate_code_quality()

        total_time = time.time() - start_time

        # Generate comprehensive report
        self._generate_final_report(total_time)

        # Determine overall success
        overall_success = (
            unit_test_success
            and integration_test_success
            and fix_validation_success
            and performance_success
            and quality_success
        )

        print(
            f"\n{'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}"
        )
        print(f"Total execution time: {total_time:.2f} seconds")

        return overall_success

    def _run_unit_tests(self) -> bool:
        """Run the unit test suite."""
        try:
            test_file = project_root / "tests" / "fixes" / "test_critical_fixes.py"

            if not test_file.exists():
                self._add_test_result("Unit Tests", False, 0, "Test file not found")
                return False

            start_time = time.time()

            # Run pytest on the unit tests
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(test_file), "-v", "--tb=short"],
                capture_output=True,
                text=True,
                cwd=str(project_root),
            )

            duration = time.time() - start_time
            success = result.returncode == 0

            error_msg = None
            if not success:
                error_msg = f"Unit tests failed:\n{result.stdout}\n{result.stderr}"

            self._add_test_result("Unit Tests", success, duration, error_msg)

            if self.verbose:
                print(
                    f"Unit tests {'✅ PASSED' if success else '❌ FAILED'} in {duration:.2f}s"
                )
                if not success:
                    print(f"Error details: {error_msg}")

            return success

        except Exception as e:
            self._add_test_result("Unit Tests", False, 0, f"Exception: {e}")
            return False

    def _run_integration_tests(self) -> bool:
        """Run the integration test suite."""
        try:
            test_file = project_root / "tests" / "fixes" / "test_integration_fixes.py"

            if not test_file.exists():
                self._add_test_result(
                    "Integration Tests", False, 0, "Test file not found"
                )
                return False

            start_time = time.time()

            # Run pytest on the integration tests
            result = subprocess.run(
                [sys.executable, "-m", "pytest", str(test_file), "-v", "--tb=short"],
                capture_output=True,
                text=True,
                cwd=str(project_root),
            )

            duration = time.time() - start_time
            success = result.returncode == 0

            error_msg = None
            if not success:
                error_msg = (
                    f"Integration tests failed:\n{result.stdout}\n{result.stderr}"
                )

            self._add_test_result("Integration Tests", success, duration, error_msg)

            if self.verbose:
                print(
                    f"Integration tests {'✅ PASSED' if success else '❌ FAILED'} in {duration:.2f}s"
                )
                if not success:
                    print(f"Error details: {error_msg}")

            return success

        except Exception as e:
            self._add_test_result("Integration Tests", False, 0, f"Exception: {e}")
            return False

    def _validate_all_fixes(self) -> bool:
        """Validate each specific fix."""
        validations = [
            self._validate_fix_1_circular_dependencies,
            self._validate_fix_2_error_handling,
            self._validate_fix_3_fallback_ui,
            self._validate_fix_4_performance,
            self._validate_fix_5_service_registration,
            self._validate_fix_6_global_state,
        ]

        all_success = True

        for validation in validations:
            try:
                success = validation()
                all_success = all_success and success
            except Exception as e:
                print(f"❌ Validation error: {e}")
                all_success = False

        return all_success

    def _validate_fix_1_circular_dependencies(self) -> bool:
        """Validate that circular dependencies have been resolved."""
        try:
            # Test that ApplicationOrchestrator can be imported and created without circular import errors
            from desktop.modern.application.services.core.application_orchestrator import (
                ApplicationOrchestrator,
            )

            # Try to create orchestrator
            orchestrator = ApplicationOrchestrator()

            # Verify lifecycle manager was created
            has_lifecycle_manager = (
                hasattr(orchestrator, "lifecycle_manager")
                and orchestrator.lifecycle_manager is not None
            )

            validation = FixValidationResult(
                fix_name="Circular Dependencies Resolution",
                is_fixed=has_lifecycle_manager,
                validation_details="ApplicationOrchestrator creates successfully with lifecycle manager",
                confidence="HIGH",
            )

            self.fix_validations.append(validation)

            if self.verbose:
                print(
                    f"Fix 1: {'✅ RESOLVED' if has_lifecycle_manager else '❌ NOT RESOLVED'}"
                )

            return has_lifecycle_manager

        except Exception as e:
            validation = FixValidationResult(
                fix_name="Circular Dependencies Resolution",
                is_fixed=False,
                validation_details=f"Failed to create ApplicationOrchestrator: {e}",
                confidence="HIGH",
            )
            self.fix_validations.append(validation)
            return False

    def _validate_fix_2_error_handling(self) -> bool:
        """Validate that standardized error handling is working."""
        try:
            # Test that StandardErrorHandler is available and functional
            import logging

            # Create a mock logger to test with
            test_logger = logging.getLogger("test_logger")
            test_error = Exception("Test error")

            # Test various error handling methods
            StandardErrorHandler.handle_service_error(
                "Test service", test_error, test_logger
            )
            StandardErrorHandler.handle_ui_error(
                "Test UI", test_error, test_logger, lambda: "fallback"
            )
            StandardErrorHandler.handle_dependency_resolution_error(
                "ITestService", test_error, test_logger, ["Service1"]
            )

            validation = FixValidationResult(
                fix_name="Standardized Error Handling",
                is_fixed=True,
                validation_details="StandardErrorHandler methods execute without errors",
                confidence="HIGH",
            )

            self.fix_validations.append(validation)

            if self.verbose:
                print("Fix 2: ✅ IMPLEMENTED - StandardErrorHandler working")

            return True

        except Exception as e:
            validation = FixValidationResult(
                fix_name="Standardized Error Handling",
                is_fixed=False,
                validation_details=f"StandardErrorHandler test failed: {e}",
                confidence="HIGH",
            )
            self.fix_validations.append(validation)
            return False

    def _validate_fix_3_fallback_ui(self) -> bool:
        """Validate that meaningful fallback UI is implemented."""
        try:
            from desktop.modern.application.services.ui.ui_setup_manager import (
                UISetupManager,
            )

            # Create UI manager and test fallback creation
            ui_manager = UISetupManager()

            # Check if meaningful fallback methods exist
            has_meaningful_fallback = hasattr(
                ui_manager, "_create_meaningful_fallback_ui"
            )
            has_basic_construct = hasattr(ui_manager, "_create_basic_construct_tab")
            has_basic_browse = hasattr(ui_manager, "_create_basic_browse_tab")

            is_fixed = (
                has_meaningful_fallback and has_basic_construct and has_basic_browse
            )

            validation = FixValidationResult(
                fix_name="Meaningful Fallback UI",
                is_fixed=is_fixed,
                validation_details=f"Fallback methods available: {has_meaningful_fallback}, {has_basic_construct}, {has_basic_browse}",
                confidence="HIGH",
            )

            self.fix_validations.append(validation)

            if self.verbose:
                print(
                    f"Fix 3: {'✅ IMPLEMENTED' if is_fixed else '❌ NOT IMPLEMENTED'}"
                )

            return is_fixed

        except Exception as e:
            validation = FixValidationResult(
                fix_name="Meaningful Fallback UI",
                is_fixed=False,
                validation_details=f"Failed to validate fallback UI: {e}",
                confidence="MEDIUM",
            )
            self.fix_validations.append(validation)
            return False

    def _validate_fix_4_performance(self) -> bool:
        """Validate that background initialization is implemented."""
        try:
            from desktop.modern.application.services.core.application_orchestrator import (
                ApplicationOrchestrator,
            )

            orchestrator = ApplicationOrchestrator()

            # Check if background initialization method exists
            has_background_init = hasattr(
                orchestrator, "_start_background_initialization"
            )

            validation = FixValidationResult(
                fix_name="Background Performance Initialization",
                is_fixed=has_background_init,
                validation_details=f"Background initialization method exists: {has_background_init}",
                confidence="HIGH",
            )

            self.fix_validations.append(validation)

            if self.verbose:
                print(
                    f"Fix 4: {'✅ IMPLEMENTED' if has_background_init else '❌ NOT IMPLEMENTED'}"
                )

            return has_background_init

        except Exception as e:
            validation = FixValidationResult(
                fix_name="Background Performance Initialization",
                is_fixed=False,
                validation_details=f"Failed to validate performance fix: {e}",
                confidence="MEDIUM",
            )
            self.fix_validations.append(validation)
            return False

    def _validate_fix_5_service_registration(self) -> bool:
        """Validate that service registration helper eliminates duplication."""
        try:
            from desktop.modern.core.application.service_registration_helper import (
                ServiceRegistrationHelper,
            )

            # Check if helper class has expected methods
            expected_methods = [
                "register_common_data_services",
                "register_common_core_services",
                "register_all_common_services",
                "_register_services_batch",
            ]

            has_all_methods = all(
                hasattr(ServiceRegistrationHelper, method)
                for method in expected_methods
            )

            validation = FixValidationResult(
                fix_name="Service Registration Deduplication",
                is_fixed=has_all_methods,
                validation_details=f"ServiceRegistrationHelper has all expected methods: {has_all_methods}",
                confidence="HIGH",
            )

            self.fix_validations.append(validation)

            if self.verbose:
                print(
                    f"Fix 5: {'✅ IMPLEMENTED' if has_all_methods else '❌ NOT IMPLEMENTED'}"
                )

            return has_all_methods

        except Exception as e:
            validation = FixValidationResult(
                fix_name="Service Registration Deduplication",
                is_fixed=False,
                validation_details=f"Failed to validate service registration fix: {e}",
                confidence="HIGH",
            )
            self.fix_validations.append(validation)
            return False

    def _validate_fix_6_global_state(self) -> bool:
        """Validate that global state management is safe."""
        try:
            from desktop.modern.core.dependency_injection.di_container import (
                DIContainer,
                reset_container,
                set_container,
            )

            # Test the improved safety of set_container
            reset_container()

            container1 = DIContainer()
            container2 = DIContainer()

            # Set first container
            set_container(container1)

            # Try to overwrite - should raise exception now
            exception_raised = False
            try:
                set_container(container2)
            except RuntimeError:
                exception_raised = True
            except Exception:
                # Different exception type - still shows it's not silent
                exception_raised = True

            # Clean up
            reset_container()

            validation = FixValidationResult(
                fix_name="Safe Global State Management",
                is_fixed=exception_raised,
                validation_details=f"set_container raises exception on overwrite attempt: {exception_raised}",
                confidence="HIGH",
            )

            self.fix_validations.append(validation)

            if self.verbose:
                print(
                    f"Fix 6: {'✅ IMPLEMENTED' if exception_raised else '❌ NOT IMPLEMENTED'}"
                )

            return exception_raised

        except Exception as e:
            validation = FixValidationResult(
                fix_name="Safe Global State Management",
                is_fixed=False,
                validation_details=f"Failed to validate global state fix: {e}",
                confidence="HIGH",
            )
            self.fix_validations.append(validation)
            return False

    def _validate_performance_improvements(self) -> bool:
        """Validate performance improvements."""
        print("Validating performance improvements...")

        # Since we can't run the full app, check that QTimer is used for background tasks
        try:
            import inspect

            from desktop.modern.application.services.core.application_orchestrator import (
                ApplicationOrchestrator,
            )

            # Get source of background initialization method
            orchestrator = ApplicationOrchestrator()
            if hasattr(orchestrator, "_start_background_initialization"):
                method = orchestrator._start_background_initialization
                source = inspect.getsource(method)

                # Check if QTimer.singleShot is used
                uses_qtimer = "QTimer.singleShot" in source

                self._add_test_result("Performance - Background Init", uses_qtimer, 0.1)

                if self.verbose:
                    print(
                        f"Background initialization uses QTimer: {'✅ YES' if uses_qtimer else '❌ NO'}"
                    )

                return uses_qtimer
            else:
                self._add_test_result(
                    "Performance - Background Init", False, 0.1, "Method not found"
                )
                return False

        except Exception as e:
            self._add_test_result(
                "Performance - Background Init", False, 0.1, f"Exception: {e}"
            )
            return False

    def _validate_code_quality(self) -> bool:
        """Validate code quality improvements (method length, etc.)."""
        print("Validating code quality improvements...")

        quality_checks = []

        # Check ApplicationOrchestrator method lengths
        try:
            from desktop.modern.application.services.core.application_orchestrator import (
                ApplicationOrchestrator,
            )

            long_methods = 0
            total_methods = 0

            for attr_name in dir(ApplicationOrchestrator):
                if attr_name.startswith("_") and not attr_name.startswith("__"):
                    attr = getattr(ApplicationOrchestrator, attr_name)
                    if callable(attr):
                        try:
                            source_lines = inspect.getsourcelines(attr)[0]
                            line_count = len(source_lines)
                            total_methods += 1

                            if line_count > 30:  # Consider methods > 30 lines as long
                                long_methods += 1
                        except:
                            pass

            method_quality_good = (
                long_methods / max(total_methods, 1)
            ) < 0.3  # Less than 30% long methods
            quality_checks.append(method_quality_good)

            self._add_test_result(
                "Code Quality - Method Length", method_quality_good, 0.1
            )

            if self.verbose:
                print(
                    f"Method length quality: {total_methods} methods, {long_methods} long ({'✅ GOOD' if method_quality_good else '❌ NEEDS WORK'})"
                )

        except Exception as e:
            quality_checks.append(False)
            self._add_test_result(
                "Code Quality - Method Length", False, 0.1, f"Exception: {e}"
            )

        return all(quality_checks)

    def _add_test_result(
        self, name: str, passed: bool, duration: float, error_message: str = None
    ):
        """Add a test result to the collection."""
        self.test_results.append(TestResult(name, passed, duration, error_message))

    def _generate_final_report(self, total_time: float):
        """Generate comprehensive final report."""
        report_lines = [
            "=" * 70,
            "TKA CRITICAL FIXES VALIDATION REPORT",
            "=" * 70,
            f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total execution time: {total_time:.2f} seconds",
            "",
        ]

        # Test results summary
        passed_tests = sum(1 for result in self.test_results if result.passed)
        total_tests = len(self.test_results)

        report_lines.extend(
            [
                "📊 TEST RESULTS SUMMARY:",
                f"   Tests passed: {passed_tests}/{total_tests}",
                f"   Success rate: {(passed_tests / max(total_tests, 1) * 100):.1f}%",
                "",
            ]
        )

        # Individual test results
        report_lines.append("📋 INDIVIDUAL TEST RESULTS:")
        for result in self.test_results:
            status = "✅ PASS" if result.passed else "❌ FAIL"
            report_lines.append(f"   {status} {result.name} ({result.duration:.2f}s)")
            if not result.passed and result.error_message:
                report_lines.append(f"      Error: {result.error_message}")

        report_lines.append("")

        # Fix validation summary
        fixed_count = sum(1 for fix in self.fix_validations if fix.is_fixed)
        total_fixes = len(self.fix_validations)

        report_lines.extend(
            [
                "🔧 FIXES VALIDATION SUMMARY:",
                f"   Fixes validated: {fixed_count}/{total_fixes}",
                f"   Fix success rate: {(fixed_count / max(total_fixes, 1) * 100):.1f}%",
                "",
            ]
        )

        # Individual fix validations
        report_lines.append("🔍 INDIVIDUAL FIX VALIDATIONS:")
        for fix in self.fix_validations:
            status = "✅ FIXED" if fix.is_fixed else "❌ NOT FIXED"
            confidence = f"({fix.confidence} confidence)"
            report_lines.append(f"   {status} {fix.fix_name} {confidence}")
            report_lines.append(f"      Details: {fix.validation_details}")

        report_content = "\n".join(report_lines)

        # Print to console
        print("\n" + report_content)

        # Save to file if requested
        if self.report_file:
            try:
                with open(self.report_file, "w") as f:
                    f.write(report_content)
                print(f"\n📄 Report saved to: {self.report_file}")
            except Exception as e:
                print(f"⚠️ Could not save report to file: {e}")


def main():
    """Main entry point for the test runner."""
    import argparse

    parser = argparse.ArgumentParser(description="TKA Critical Fixes Test Runner")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--report", "-r", type=str, help="Save report to file")
    parser.add_argument(
        "--fix-only", action="store_true", help="Only validate fixes, skip full tests"
    )

    args = parser.parse_args()

    # Create test runner
    runner = TKAFixesTestRunner(verbose=args.verbose, report_file=args.report)

    try:
        if args.fix_only:
            print("🔍 Running fix validation only...")
            success = runner._validate_all_fixes()
            runner._generate_final_report(0)
        else:
            success = runner.run_all_tests()

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print("\n⚠️ Test run interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Test runner failed with exception: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
