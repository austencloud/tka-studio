"""
Comprehensive Test Runner for Microservices Infrastructure

Executes all test phases in sequence and provides detailed reporting
on the validation of the microservices infrastructure implementation.
"""

import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Any
import json


class MicroservicesTestRunner:
    """Comprehensive test runner for the microservices infrastructure."""
    
    def __init__(self, project_root: str = r"f:\CODE\TKA"):
        self.project_root = Path(project_root)
        self.test_dir = self.project_root / "tests"
        self.results = {
            "phase_1_unit": {},
            "phase_2_integration": {},
            "phase_3_performance": {},
            "phase_4_full_system": {},
            "manual_verification": {},
            "overall_summary": {}
        }
        self.start_time = None
        self.end_time = None
    
    def run_pytest_file(self, test_file: str, phase_name: str) -> Dict[str, Any]:
        """Run a specific pytest file and capture results."""
        print(f"\n{'='*60}")
        print(f"Running {phase_name}: {test_file}")
        print(f"{'='*60}")
        
        test_path = self.test_dir / test_file
        
        if not test_path.exists():
            return {
                "status": "SKIPPED",
                "reason": f"Test file not found: {test_path}",
                "tests_run": 0,
                "passed": 0,
                "failed": 0,
                "duration": 0
            }
        
        # Run pytest with detailed output
        cmd = [
            sys.executable, "-m", "pytest",
            str(test_path),
            "-v",
            "--tb=short",
            "--durations=10",
            "--disable-warnings"
        ]
        
        start_time = time.time()
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=300  # 5 minute timeout per test file
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Parse pytest output
            output_lines = result.stdout.split('\n')
            
            # Extract test results
            tests_run = 0
            passed = 0
            failed = 0
            
            for line in output_lines:
                if "passed" in line and "failed" in line:
                    # Parse summary line like "5 passed, 2 failed in 1.23s"
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == "passed":
                            passed = int(parts[i-1])
                        elif part == "failed":
                            failed = int(parts[i-1])
                    tests_run = passed + failed
                elif "passed in" in line and failed == 0:
                    # Parse line like "15 passed in 2.34s"
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == "passed":
                            passed = int(parts[i-1])
                    tests_run = passed
            
            # Determine status
            if result.returncode == 0:
                status = "PASSED"
            elif tests_run == 0:
                status = "NO_TESTS"
            else:
                status = "FAILED"
            
            return {
                "status": status,
                "tests_run": tests_run,
                "passed": passed,
                "failed": failed,
                "duration": duration,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                "status": "TIMEOUT",
                "tests_run": 0,
                "passed": 0,
                "failed": 0,
                "duration": 300,
                "error": "Test execution timed out after 5 minutes"
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "tests_run": 0,
                "passed": 0,
                "failed": 0,
                "duration": 0,
                "error": str(e)
            }
    
    def run_manual_tests(self) -> Dict[str, Any]:
        """Run manual testing suite."""
        print(f"\n{'='*60}")
        print("Running Manual Verification Tests")
        print(f"{'='*60}")
        
        manual_test_path = self.test_dir / "manual_testing_suite.py"
        
        if not manual_test_path.exists():
            return {
                "status": "SKIPPED",
                "reason": "Manual testing suite not found"
            }
        
        cmd = [sys.executable, str(manual_test_path)]
        
        start_time = time.time()
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=self.project_root,
                timeout=180  # 3 minute timeout
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Parse manual test output
            output_lines = result.stdout.split('\n')
            
            passed_tests = 0
            total_tests = 0
            
            for line in output_lines:
                if "✅ PASS" in line:
                    passed_tests += 1
                    total_tests += 1
                elif "❌ FAIL" in line:
                    total_tests += 1
            
            status = "PASSED" if result.returncode == 0 else "FAILED"
            
            return {
                "status": status,
                "tests_run": total_tests,
                "passed": passed_tests,
                "failed": total_tests - passed_tests,
                "duration": duration,
                "stdout": result.stdout,
                "stderr": result.stderr
            }
            
        except subprocess.TimeoutExpired:
            return {
                "status": "TIMEOUT",
                "error": "Manual tests timed out after 3 minutes"
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "error": str(e)
            }
    
    def run_phase_1_unit_tests(self):
        """Run Phase 1: Unit Tests."""
        print(f"\n🧪 PHASE 1: UNIT TESTS")
        print(f"Testing individual microservices components...")
        
        unit_tests = [
            ("test_event_integration.py", "Event Integration Tests"),
            ("test_circuit_breaker.py", "Circuit Breaker Tests"),
            ("test_initialization_saga.py", "Saga Pattern Tests")
        ]
        
        for test_file, test_name in unit_tests:
            result = self.run_pytest_file(test_file, test_name)
            self.results["phase_1_unit"][test_name] = result
            
            # Print immediate feedback
            status_icon = "✅" if result["status"] == "PASSED" else "❌"
            print(f"{status_icon} {test_name}: {result['passed']}/{result['tests_run']} passed")
    
    def run_phase_2_integration_tests(self):
        """Run Phase 2: Integration Tests."""
        print(f"\n🔗 PHASE 2: INTEGRATION TESTS")
        print(f"Testing component interactions and event flows...")
        
        integration_tests = [
            ("test_e2e_event_flow.py", "End-to-End Event Flow Tests"),
            ("test_service_mesh_integration.py", "Service Mesh Integration Tests")
        ]
        
        for test_file, test_name in integration_tests:
            result = self.run_pytest_file(test_file, test_name)
            self.results["phase_2_integration"][test_name] = result
            
            status_icon = "✅" if result["status"] == "PASSED" else "❌"
            print(f"{status_icon} {test_name}: {result['passed']}/{result['tests_run']} passed")
    
    def run_phase_3_performance_tests(self):
        """Run Phase 3: Performance & Load Tests."""
        print(f"\n⚡ PHASE 3: PERFORMANCE & LOAD TESTS")
        print(f"Testing system performance and scalability...")
        
        performance_tests = [
            ("test_performance.py", "Performance & Load Tests")
        ]
        
        for test_file, test_name in performance_tests:
            result = self.run_pytest_file(test_file, test_name)
            self.results["phase_3_performance"][test_name] = result
            
            status_icon = "✅" if result["status"] == "PASSED" else "❌"
            print(f"{status_icon} {test_name}: {result['passed']}/{result['tests_run']} passed")
    
    def run_phase_4_full_system_tests(self):
        """Run Phase 4: Full System Integration Tests."""
        print(f"\n🌐 PHASE 4: FULL SYSTEM INTEGRATION")
        print(f"Testing complete microservices ecosystem...")
        
        system_tests = [
            ("test_full_system_integration.py", "Full System Integration Tests")
        ]
        
        for test_file, test_name in system_tests:
            result = self.run_pytest_file(test_file, test_name)
            self.results["phase_4_full_system"][test_name] = result
            
            status_icon = "✅" if result["status"] == "PASSED" else "❌"
            print(f"{status_icon} {test_name}: {result['passed']}/{result['tests_run']} passed")
    
    def run_manual_verification(self):
        """Run Manual Verification Tests."""
        print(f"\n🔍 MANUAL VERIFICATION")
        print(f"Running manual testing and verification procedures...")
        
        result = self.run_manual_tests()
        self.results["manual_verification"]["Manual Testing Suite"] = result
        
        status_icon = "✅" if result["status"] == "PASSED" else "❌"
        print(f"{status_icon} Manual Testing Suite: {result.get('passed', 0)}/{result.get('tests_run', 0)} passed")
    
    def calculate_overall_results(self):
        """Calculate overall test results."""
        total_tests = 0
        total_passed = 0
        total_failed = 0
        total_duration = 0
        
        all_phases = [
            self.results["phase_1_unit"],
            self.results["phase_2_integration"],
            self.results["phase_3_performance"],
            self.results["phase_4_full_system"],
            self.results["manual_verification"]
        ]
        
        phase_results = []
        
        for phase_data in all_phases:
            phase_tests = 0
            phase_passed = 0
            phase_failed = 0
            phase_duration = 0
            phase_status = "PASSED"
            
            for test_name, test_result in phase_data.items():
                if isinstance(test_result, dict):
                    phase_tests += test_result.get("tests_run", 0)
                    phase_passed += test_result.get("passed", 0)
                    phase_failed += test_result.get("failed", 0)
                    phase_duration += test_result.get("duration", 0)
                    
                    if test_result.get("status") not in ["PASSED", "NO_TESTS"]:
                        phase_status = "FAILED"
            
            phase_results.append({
                "tests_run": phase_tests,
                "passed": phase_passed,
                "failed": phase_failed,
                "duration": phase_duration,
                "status": phase_status
            })
            
            total_tests += phase_tests
            total_passed += phase_passed
            total_failed += phase_failed
            total_duration += phase_duration
        
        overall_status = "PASSED" if total_failed == 0 and total_tests > 0 else "FAILED"
        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        
        self.results["overall_summary"] = {
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "success_rate": success_rate,
            "total_duration": total_duration,
            "overall_status": overall_status,
            "phase_results": phase_results
        }
    
    def print_detailed_report(self):
        """Print detailed test report."""
        print(f"\n{'='*80}")
        print("MICROSERVICES INFRASTRUCTURE TEST REPORT")
        print(f"{'='*80}")
        
        summary = self.results["overall_summary"]
        
        print(f"\n📊 OVERALL SUMMARY")
        print(f"{'─'*40}")
        print(f"Total Tests Run: {summary['total_tests']}")
        print(f"Passed: {summary['total_passed']}")
        print(f"Failed: {summary['total_failed']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Total Duration: {summary['total_duration']:.2f} seconds")
        print(f"Overall Status: {summary['overall_status']}")
        
        # Phase breakdown
        phase_names = [
            "Phase 1: Unit Tests",
            "Phase 2: Integration Tests", 
            "Phase 3: Performance Tests",
            "Phase 4: Full System Tests",
            "Manual Verification"
        ]
        
        print(f"\n📋 PHASE BREAKDOWN")
        print(f"{'─'*40}")
        
        for i, (phase_name, phase_data) in enumerate(zip(phase_names, [
            self.results["phase_1_unit"],
            self.results["phase_2_integration"],
            self.results["phase_3_performance"],
            self.results["phase_4_full_system"],
            self.results["manual_verification"]
        ])):
            phase_summary = summary["phase_results"][i]
            status_icon = "✅" if phase_summary["status"] == "PASSED" else "❌"
            
            print(f"{status_icon} {phase_name}")
            print(f"   Tests: {phase_summary['passed']}/{phase_summary['tests_run']} passed")
            print(f"   Duration: {phase_summary['duration']:.2f}s")
            
            # Show individual test results
            for test_name, test_result in phase_data.items():
                if isinstance(test_result, dict):
                    test_icon = "✅" if test_result.get("status") == "PASSED" else "❌"
                    print(f"   {test_icon} {test_name}: {test_result.get('passed', 0)}/{test_result.get('tests_run', 0)}")
        
        # Success criteria verification
        print(f"\n✅ SUCCESS CRITERIA VERIFICATION")
        print(f"{'─'*40}")
        
        criteria_met = []
        
        # Zero failures requirement
        if summary["total_failed"] == 0:
            criteria_met.append("✅ Zero test failures")
        else:
            criteria_met.append(f"❌ {summary['total_failed']} test failures detected")
        
        # Performance requirements
        performance_result = self.results["phase_3_performance"].get("Performance & Load Tests", {})
        if performance_result.get("status") == "PASSED":
            criteria_met.append("✅ Performance benchmarks met")
        else:
            criteria_met.append("❌ Performance benchmarks not met")
        
        # Integration requirements
        integration_passed = all(
            result.get("status") == "PASSED" 
            for result in self.results["phase_2_integration"].values()
            if isinstance(result, dict)
        )
        
        if integration_passed:
            criteria_met.append("✅ Integration tests passed")
        else:
            criteria_met.append("❌ Integration tests failed")
        
        # Manual verification
        manual_result = self.results["manual_verification"].get("Manual Testing Suite", {})
        if manual_result.get("status") == "PASSED":
            criteria_met.append("✅ Manual verification completed")
        else:
            criteria_met.append("❌ Manual verification failed")
        
        for criterion in criteria_met:
            print(f"   {criterion}")
        
        # Deployment readiness
        print(f"\n🚀 DEPLOYMENT READINESS")
        print(f"{'─'*40}")
        
        if summary["overall_status"] == "PASSED" and summary["total_failed"] == 0:
            print("🎉 READY FOR DEPLOYMENT")
            print("   All tests passed successfully!")
            print("   Microservices infrastructure is validated and ready.")
        else:
            print("⚠️  NOT READY FOR DEPLOYMENT")
            print("   Please address failing tests before deployment.")
            print("   Review detailed results above for specific issues.")
    
    def save_results_json(self):
        """Save test results to JSON file."""
        results_file = self.project_root / "test_results.json"
        
        # Add metadata
        self.results["metadata"] = {
            "test_run_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_duration": self.end_time - self.start_time if self.end_time and self.start_time else 0,
            "python_version": sys.version,
            "project_root": str(self.project_root)
        }
        
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n💾 Test results saved to: {results_file}")
    
    def run_all_tests(self):
        """Run complete test suite."""
        self.start_time = time.time()
        
        print("🚀 TKA MICROSERVICES INFRASTRUCTURE TESTING PROTOCOL")
        print("=" * 60)
        print("Comprehensive validation of microservices architecture")
        print("Leveraging existing TypeSafeEventBus and Command System")
        
        try:
            # Run all test phases
            self.run_phase_1_unit_tests()
            self.run_phase_2_integration_tests()
            self.run_phase_3_performance_tests()
            self.run_phase_4_full_system_tests()
            self.run_manual_verification()
            
            self.end_time = time.time()
            
            # Calculate and display results
            self.calculate_overall_results()
            self.print_detailed_report()
            self.save_results_json()
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Test execution interrupted by user")
            self.end_time = time.time()
        except Exception as e:
            print(f"\n\n❌ Test execution failed: {e}")
            self.end_time = time.time()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="TKA Microservices Infrastructure Test Runner")
    parser.add_argument("--project-root", default=r"f:\CODE\TKA", help="Project root directory")
    parser.add_argument("--phase", choices=["1", "2", "3", "4", "manual", "all"], default="all", 
                       help="Specific test phase to run")
    
    args = parser.parse_args()
    
    runner = MicroservicesTestRunner(args.project_root)
    
    if args.phase == "all":
        runner.run_all_tests()
    elif args.phase == "1":
        runner.run_phase_1_unit_tests()
        runner.calculate_overall_results()
        runner.print_detailed_report()
    elif args.phase == "2":
        runner.run_phase_2_integration_tests()
        runner.calculate_overall_results()
        runner.print_detailed_report()
    elif args.phase == "3":
        runner.run_phase_3_performance_tests()
        runner.calculate_overall_results()
        runner.print_detailed_report()
    elif args.phase == "4":
        runner.run_phase_4_full_system_tests()
        runner.calculate_overall_results()
        runner.print_detailed_report()
    elif args.phase == "manual":
        runner.run_manual_verification()
        runner.calculate_overall_results()
        runner.print_detailed_report()


if __name__ == "__main__":
    main()
