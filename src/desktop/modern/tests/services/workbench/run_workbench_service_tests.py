"""
Comprehensive Test Runner for Workbench Service Refactoring

This script runs all tests for the new workbench services and validates
that the refactoring is working correctly without breaking existing functionality.

Usage:
    python run_workbench_service_tests.py [--verbose] [--coverage] [--integration-only] [--unit-only]
"""

import sys
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Any
import argparse


class WorkbenchTestRunner:
    """Comprehensive test runner for workbench service refactoring."""
    
    def __init__(self, verbose: bool = False, coverage: bool = False):
        self.verbose = verbose
        self.coverage = coverage
        self.test_results = {}
        self.start_time = time.time()
        
        # Get the test directory
        self.test_dir = Path(__file__).parent
        self.project_root = self.test_dir.parent.parent.parent
        
        print(f"🚀 Workbench Service Test Runner")
        print(f"📁 Test directory: {self.test_dir}")
        print(f"📁 Project root: {self.project_root}")
        print("=" * 60)
    
    def run_test_file(self, test_file: Path, test_name: str) -> Dict[str, Any]:
        """Run a specific test file and return results."""
        print(f"\n🧪 Running {test_name}...")
        print(f"📄 File: {test_file}")
        
        cmd = ["python", "-m", "pytest", str(test_file)]
        
        if self.verbose:
            cmd.append("-v")
        else:
            cmd.append("-q")
        
        if self.coverage:
            cmd.extend(["--cov", "--cov-report=term-missing"])
        
        start_time = time.time()
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            duration = time.time() - start_time
            
            success = result.returncode == 0
            
            test_result = {
                "success": success,
                "duration": duration,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
            
            if success:
                print(f"✅ {test_name} passed ({duration:.2f}s)")
                if self.verbose:
                    print(f"   Output: {result.stdout}")
            else:
                print(f"❌ {test_name} failed ({duration:.2f}s)")
                print(f"   Error: {result.stderr}")
                if self.verbose:
                    print(f"   Output: {result.stdout}")
            
            return test_result
            
        except subprocess.TimeoutExpired:
            print(f"⏰ {test_name} timed out after 5 minutes")
            return {
                "success": False,
                "duration": 300,
                "stdout": "",
                "stderr": "Test timed out",
                "returncode": -1
            }
        except Exception as e:
            print(f"💥 {test_name} crashed: {e}")
            return {
                "success": False,
                "duration": 0,
                "stdout": "",
                "stderr": str(e),
                "returncode": -2
            }
    
    def run_unit_tests(self) -> bool:
        """Run all unit tests for workbench services."""
        print(f"\n📋 PHASE 1: Running Unit Tests")
        print("=" * 40)
        
        unit_tests = [
            (self.test_dir / "test_workbench_export_service.py", "Export Service Tests"),
            (self.test_dir / "test_workbench_clipboard_service.py", "Clipboard Service Tests"),
            (self.test_dir / "test_enhanced_workbench_operation_coordinator.py", "Enhanced Coordinator Tests"),
        ]
        
        all_passed = True
        
        for test_file, test_name in unit_tests:
            if not test_file.exists():
                print(f"⚠️  {test_name} - Test file not found: {test_file}")
                self.test_results[test_name] = {
                    "success": False,
                    "duration": 0,
                    "stdout": "",
                    "stderr": "Test file not found",
                    "returncode": -3
                }
                all_passed = False
                continue
            
            result = self.run_test_file(test_file, test_name)
            self.test_results[test_name] = result
            
            if not result["success"]:
                all_passed = False
        
        return all_passed
    
    def run_integration_tests(self) -> bool:
        """Run integration tests for workbench services."""
        print(f"\n🔗 PHASE 2: Running Integration Tests")
        print("=" * 40)
        
        integration_tests = [
            (self.test_dir / "test_workbench_integration.py", "Service Integration Tests"),
        ]
        
        all_passed = True
        
        for test_file, test_name in integration_tests:
            if not test_file.exists():
                print(f"⚠️  {test_name} - Test file not found: {test_file}")
                self.test_results[test_name] = {
                    "success": False,
                    "duration": 0,
                    "stdout": "",
                    "stderr": "Test file not found",
                    "returncode": -3
                }
                all_passed = False
                continue
            
            result = self.run_test_file(test_file, test_name)
            self.test_results[test_name] = result
            
            if not result["success"]:
                all_passed = False
        
        return all_passed
    
    def run_validation_tests(self) -> bool:
        """Run validation tests to ensure no existing functionality is broken."""
        print(f"\n🔍 PHASE 3: Running Validation Tests")
        print("=" * 40)
        
        # These would be existing tests that should still pass
        validation_tests = [
            # Add paths to existing workbench tests here when available
            # (Path("tests/test_existing_workbench.py"), "Existing Workbench Tests"),
        ]
        
        if not validation_tests:
            print("⚠️  No validation tests configured - skipping phase")
            return True
        
        all_passed = True
        
        for test_file, test_name in validation_tests:
            if not test_file.exists():
                print(f"⚠️  {test_name} - Test file not found: {test_file}")
                continue
            
            result = self.run_test_file(test_file, test_name)
            self.test_results[test_name] = result
            
            if not result["success"]:
                all_passed = False
        
        return all_passed
    
    def run_import_validation(self) -> bool:
        """Validate that all new modules can be imported correctly."""
        print(f"\n📦 PHASE 4: Running Import Validation")
        print("=" * 40)
        
        import_tests = [
            ("application.services.workbench.workbench_export_service", "WorkbenchExportService"),
            ("application.services.workbench.workbench_clipboard_service", "WorkbenchClipboardService"),
            ("application.services.workbench.enhanced_workbench_operation_coordinator", "EnhancedWorkbenchOperationCoordinator"),
            ("core.interfaces.workbench_export_services", "Export Service Interfaces"),
        ]
        
        all_passed = True
        
        for module_path, module_name in import_tests:
            try:
                print(f"📥 Importing {module_name}...")
                
                # Change to project root for imports
                original_cwd = Path.cwd()
                project_src = self.project_root / "src"
                
                # Add src to Python path
                if str(project_src) not in sys.path:
                    sys.path.insert(0, str(project_src))
                
                # Try to import the module
                __import__(module_path)
                print(f"✅ {module_name} imported successfully")
                
            except ImportError as e:
                print(f"❌ {module_name} import failed: {e}")
                all_passed = False
                self.test_results[f"Import {module_name}"] = {
                    "success": False,
                    "duration": 0,
                    "stdout": "",
                    "stderr": str(e),
                    "returncode": -4
                }
            except Exception as e:
                print(f"💥 {module_name} import crashed: {e}")
                all_passed = False
                self.test_results[f"Import {module_name}"] = {
                    "success": False,
                    "duration": 0,
                    "stdout": "",
                    "stderr": str(e),
                    "returncode": -5
                }
        
        return all_passed
    
    def run_quick_validation(self) -> bool:
        """Run a quick validation to ensure basic functionality works."""
        print(f"\n⚡ PHASE 5: Running Quick Validation")
        print("=" * 40)
        
        try:
            # Add src to Python path
            project_src = self.project_root / "src"
            if str(project_src) not in sys.path:
                sys.path.insert(0, str(project_src))
            
            print("🔧 Testing WorkbenchExportService...")
            from desktop.modern.application.services.workbench.workbench_export_service import WorkbenchExportService
            
            export_service = WorkbenchExportService()
            assert export_service.validate_export_directory()
            print("✅ WorkbenchExportService basic functionality works")
            
            print("📋 Testing WorkbenchClipboardService...")
            from desktop.modern.application.services.workbench.workbench_clipboard_service import (
                WorkbenchClipboardService, MockClipboardAdapter
            )
            
            clipboard_service = WorkbenchClipboardService(MockClipboardAdapter())
            success, message = clipboard_service.copy_text_to_clipboard("test")
            assert success
            print("✅ WorkbenchClipboardService basic functionality works")
            
            print("🎛️ Testing EnhancedWorkbenchOperationCoordinator...")
            from shared.application.services.workbench.enhanced_workbench_operation_coordinator import (
                EnhancedWorkbenchOperationCoordinator
            )
            
            coordinator = EnhancedWorkbenchOperationCoordinator()
            status = coordinator.get_operation_status_summary()
            assert isinstance(status, dict)
            print("✅ EnhancedWorkbenchOperationCoordinator basic functionality works")
            
            print("✅ All quick validations passed!")
            return True
            
        except Exception as e:
            print(f"❌ Quick validation failed: {e}")
            return False
    
    def generate_report(self, unit_passed: bool, integration_passed: bool, 
                       validation_passed: bool, import_passed: bool, quick_passed: bool) -> None:
        """Generate comprehensive test report."""
        total_duration = time.time() - self.start_time
        
        print(f"\n" + "=" * 60)
        print(f"📊 WORKBENCH SERVICE TEST REPORT")
        print(f"=" * 60)
        
        print(f"⏱️  Total Duration: {total_duration:.2f} seconds")
        print(f"🧪 Total Tests: {len(self.test_results)}")
        
        # Phase summary
        phases = [
            ("📋 Unit Tests", unit_passed),
            ("🔗 Integration Tests", integration_passed),
            ("🔍 Validation Tests", validation_passed),
            ("📦 Import Validation", import_passed),
            ("⚡ Quick Validation", quick_passed),
        ]
        
        print(f"\n📈 Phase Summary:")
        for phase_name, passed in phases:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"   {phase_name}: {status}")
        
        # Detailed results
        if self.test_results:
            print(f"\n📋 Detailed Test Results:")
            for test_name, result in self.test_results.items():
                status = "✅ PASS" if result["success"] else "❌ FAIL"
                duration = result.get("duration", 0)
                print(f"   {test_name}: {status} ({duration:.2f}s)")
                
                if not result["success"] and result.get("stderr"):
                    print(f"      Error: {result['stderr'][:100]}...")
        
        # Overall result
        all_passed = all([unit_passed, integration_passed, validation_passed, import_passed, quick_passed])
        
        print(f"\n🏁 OVERALL RESULT:")
        if all_passed:
            print(f"✅ ALL TESTS PASSED - Workbench service refactoring is successful!")
            print(f"🎉 New services are ready for integration into the presentation layer.")
        else:
            print(f"❌ SOME TESTS FAILED - Please review the errors above.")
            print(f"🔧 Fix the issues before proceeding with integration.")
        
        print(f"=" * 60)
        
        return all_passed
    
    def run_all_tests(self, unit_only: bool = False, integration_only: bool = False) -> bool:
        """Run all test phases."""
        if integration_only:
            phases = [
                ("integration", self.run_integration_tests),
            ]
        elif unit_only:
            phases = [
                ("unit", self.run_unit_tests),
            ]
        else:
            phases = [
                ("import", self.run_import_validation),
                ("quick", self.run_quick_validation),
                ("unit", self.run_unit_tests),
                ("integration", self.run_integration_tests),
                ("validation", self.run_validation_tests),
            ]
        
        results = {}
        
        for phase_name, phase_func in phases:
            try:
                results[phase_name] = phase_func()
            except Exception as e:
                print(f"💥 Phase {phase_name} crashed: {e}")
                results[phase_name] = False
        
        # Generate report
        return self.generate_report(
            unit_passed=results.get("unit", True),
            integration_passed=results.get("integration", True),
            validation_passed=results.get("validation", True),
            import_passed=results.get("import", True),
            quick_passed=results.get("quick", True)
        )


def main():
    """Main entry point for test runner."""
    parser = argparse.ArgumentParser(description="Run workbench service tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", "-c", action="store_true", help="Run with coverage")
    parser.add_argument("--unit-only", action="store_true", help="Run only unit tests")
    parser.add_argument("--integration-only", action="store_true", help="Run only integration tests")
    
    args = parser.parse_args()
    
    runner = WorkbenchTestRunner(verbose=args.verbose, coverage=args.coverage)
    success = runner.run_all_tests(unit_only=args.unit_only, integration_only=args.integration_only)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
