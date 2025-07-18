#!/usr/bin/env python3
"""
Direct Test Execution Analysis
==============================

Directly executes test categories and provides comprehensive analysis.
"""

import subprocess
import time
from pathlib import Path
from typing import Dict, List, Tuple


class DirectTestExecutor:
    """Executes tests directly and analyzes results."""
    
    def __init__(self, tka_root: Path):
        self.tka_root = tka_root
        self.results = {}
        
        # Define test paths that actually exist
        self.test_paths = [
            "tests/unit/services/",
            "tests/cross_platform/",
            "tests/interface_coverage/",
            "tests/interface_completeness/",
            "tests/service_implementation/",
            "tests/integration/",
            "launcher/tests/",
            "src/desktop/modern/tests/unit/core/",
            "src/desktop/modern/tests/unit/interfaces/",
            "src/desktop/modern/tests/unit/presentation/",
            "src/desktop/modern/tests/integration/",
            "src/desktop/modern/tests/specification/core/",
            "src/desktop/modern/tests/specification/domain/",
            "src/desktop/modern/tests/application/",
            "src/desktop/modern/tests/framework/",
            "src/desktop/modern/tests/improved_architecture/",
            "src/desktop/modern/tests/test_*.py",
        ]
    
    def execute_test_path(self, path: str) -> Dict:
        """Execute tests for a specific path."""
        print(f"\n🧪 Executing: {path}")
        
        start_time = time.time()
        
        try:
            # Run the tests
            result = subprocess.run(
                ["python", "-m", "pytest", path, "-v", "--tb=short"],
                cwd=self.tka_root,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            execution_time = time.time() - start_time
            
            # Parse the output
            output = result.stdout + result.stderr
            
            # Extract test counts
            passed, failed, errors, skipped = self._parse_pytest_output(output)
            total = passed + failed + errors + skipped
            
            # Categorize result
            if total == 0:
                status = "NO_TESTS"
            elif errors > 0:
                status = "ERRORS"
            elif failed > 0:
                status = "FAILURES"
            else:
                status = "SUCCESS"
            
            # Extract specific issues
            import_errors = self._extract_import_errors(output)
            collection_errors = self._extract_collection_errors(output)
            test_failures = self._extract_test_failures(output)
            
            result_data = {
                "path": path,
                "status": status,
                "total_tests": total,
                "passed": passed,
                "failed": failed,
                "errors": errors,
                "skipped": skipped,
                "execution_time": execution_time,
                "return_code": result.returncode,
                "import_errors": import_errors,
                "collection_errors": collection_errors,
                "test_failures": test_failures,
                "output_sample": output[:1000] if output else ""
            }
            
            # Print immediate feedback
            if status == "SUCCESS":
                print(f"✅ {passed}/{total} tests passed ({execution_time:.2f}s)")
            elif status == "NO_TESTS":
                print(f"⚪ No tests found")
            elif status == "ERRORS":
                print(f"❌ {errors} errors, {passed} passed ({execution_time:.2f}s)")
                for error in import_errors[:2]:
                    print(f"   📛 {error}")
            elif status == "FAILURES":
                print(f"⚠️ {failed} failures, {passed} passed ({execution_time:.2f}s)")
            
            return result_data
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            print(f"⏰ Timeout after {execution_time:.2f}s")
            return {
                "path": path,
                "status": "TIMEOUT",
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "errors": 1,
                "skipped": 0,
                "execution_time": execution_time,
                "return_code": -1,
                "import_errors": ["Execution timeout"],
                "collection_errors": [],
                "test_failures": [],
                "output_sample": ""
            }
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"💥 Exception: {str(e)}")
            return {
                "path": path,
                "status": "EXCEPTION",
                "total_tests": 0,
                "passed": 0,
                "failed": 0,
                "errors": 1,
                "skipped": 0,
                "execution_time": execution_time,
                "return_code": -1,
                "import_errors": [str(e)],
                "collection_errors": [],
                "test_failures": [],
                "output_sample": ""
            }
    
    def _parse_pytest_output(self, output: str) -> Tuple[int, int, int, int]:
        """Parse pytest output to extract test counts."""
        passed = failed = errors = skipped = 0
        
        # Look for the summary line
        lines = output.split('\n')
        for line in lines:
            if " passed" in line or " failed" in line or " error" in line:
                # Try to extract numbers
                words = line.split()
                for i, word in enumerate(words):
                    if word == "passed" and i > 0:
                        try:
                            passed = int(words[i-1])
                        except:
                            pass
                    elif word == "failed" and i > 0:
                        try:
                            failed = int(words[i-1])
                        except:
                            pass
                    elif word == "error" and i > 0:
                        try:
                            errors = int(words[i-1])
                        except:
                            pass
                    elif word == "skipped" and i > 0:
                        try:
                            skipped = int(words[i-1])
                        except:
                            pass
        
        return passed, failed, errors, skipped
    
    def _extract_import_errors(self, output: str) -> List[str]:
        """Extract import error messages."""
        errors = []
        lines = output.split('\n')
        
        for line in lines:
            if "ModuleNotFoundError:" in line or "ImportError:" in line:
                errors.append(line.strip())
        
        return errors[:5]  # Limit to first 5
    
    def _extract_collection_errors(self, output: str) -> List[str]:
        """Extract collection error messages."""
        errors = []
        lines = output.split('\n')
        
        for line in lines:
            if "ERROR collecting" in line:
                errors.append(line.strip())
        
        return errors[:5]  # Limit to first 5
    
    def _extract_test_failures(self, output: str) -> List[str]:
        """Extract test failure messages."""
        failures = []
        lines = output.split('\n')
        
        for line in lines:
            if "FAILED" in line and "::" in line:
                failures.append(line.strip())
        
        return failures[:5]  # Limit to first 5
    
    def execute_all_paths(self) -> Dict:
        """Execute all test paths and generate summary."""
        print("🚀 Starting Direct Test Execution Analysis")
        print("=" * 60)
        
        total_start_time = time.time()
        
        for path in self.test_paths:
            result = self.execute_test_path(path)
            self.results[path] = result
        
        total_execution_time = time.time() - total_start_time
        
        # Generate summary
        summary = self._generate_summary(total_execution_time)
        
        return summary
    
    def _generate_summary(self, total_time: float) -> Dict:
        """Generate execution summary."""
        total_tests = sum(r["total_tests"] for r in self.results.values())
        total_passed = sum(r["passed"] for r in self.results.values())
        total_failed = sum(r["failed"] for r in self.results.values())
        total_errors = sum(r["errors"] for r in self.results.values())
        total_skipped = sum(r["skipped"] for r in self.results.values())
        
        successful_paths = len([r for r in self.results.values() if r["status"] == "SUCCESS"])
        error_paths = len([r for r in self.results.values() if r["status"] in ["ERRORS", "TIMEOUT", "EXCEPTION"]])
        failure_paths = len([r for r in self.results.values() if r["status"] == "FAILURES"])
        no_test_paths = len([r for r in self.results.values() if r["status"] == "NO_TESTS"])
        
        # Collect all import errors
        all_import_errors = []
        for result in self.results.values():
            all_import_errors.extend(result["import_errors"])
        
        # Collect all collection errors
        all_collection_errors = []
        for result in self.results.values():
            all_collection_errors.extend(result["collection_errors"])
        
        return {
            "total_paths": len(self.results),
            "successful_paths": successful_paths,
            "error_paths": error_paths,
            "failure_paths": failure_paths,
            "no_test_paths": no_test_paths,
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "total_errors": total_errors,
            "total_skipped": total_skipped,
            "total_execution_time": total_time,
            "success_rate": (total_passed / total_tests * 100) if total_tests > 0 else 0,
            "all_import_errors": list(set(all_import_errors)),  # Unique errors
            "all_collection_errors": list(set(all_collection_errors)),
            "detailed_results": self.results
        }
    
    def print_detailed_summary(self, summary: Dict):
        """Print detailed summary of results."""
        print("\n" + "=" * 60)
        print("🎯 DIRECT TEST EXECUTION ANALYSIS COMPLETE")
        print("=" * 60)
        
        print(f"📊 PATHS ANALYZED: {summary['total_paths']}")
        print(f"   ✅ Successful: {summary['successful_paths']}")
        print(f"   ❌ With Errors: {summary['error_paths']}")
        print(f"   ⚠️ With Failures: {summary['failure_paths']}")
        print(f"   ⚪ No Tests: {summary['no_test_paths']}")
        print()
        
        print(f"📊 TEST RESULTS: {summary['total_tests']} total tests")
        print(f"   ✅ Passed: {summary['total_passed']} ({summary['success_rate']:.1f}%)")
        print(f"   ❌ Failed: {summary['total_failed']}")
        print(f"   💥 Errors: {summary['total_errors']}")
        print(f"   ⏭️ Skipped: {summary['total_skipped']}")
        print()
        
        print(f"⏱️ EXECUTION TIME: {summary['total_execution_time']:.2f} seconds")
        print()
        
        # Show import errors
        if summary['all_import_errors']:
            print("🔍 IMPORT ERRORS FOUND:")
            for error in summary['all_import_errors'][:10]:
                print(f"   📛 {error}")
            if len(summary['all_import_errors']) > 10:
                print(f"   ... and {len(summary['all_import_errors']) - 10} more import errors")
            print()
        
        # Show collection errors
        if summary['all_collection_errors']:
            print("🔍 COLLECTION ERRORS FOUND:")
            for error in summary['all_collection_errors'][:5]:
                print(f"   📛 {error}")
            print()
        
        # Show successful paths
        print("✅ SUCCESSFUL TEST PATHS:")
        for path, result in summary['detailed_results'].items():
            if result['status'] == 'SUCCESS':
                print(f"   {path}: {result['passed']} tests passed ({result['execution_time']:.2f}s)")
        print()
        
        # Show problematic paths
        print("❌ PROBLEMATIC TEST PATHS:")
        for path, result in summary['detailed_results'].items():
            if result['status'] not in ['SUCCESS', 'NO_TESTS']:
                print(f"   {path}: {result['status']} - {result['errors']} errors, {result['failed']} failures")


def main():
    """Main execution function."""
    tka_root = Path(".")
    
    executor = DirectTestExecutor(tka_root)
    summary = executor.execute_all_paths()
    executor.print_detailed_summary(summary)
    
    # Save results
    import json
    with open("direct_test_execution_results.json", 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print("📄 Detailed results saved to: direct_test_execution_results.json")


if __name__ == "__main__":
    main()
