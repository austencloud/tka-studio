#!/usr/bin/env python3
"""
Systematic TKA Test Analysis
============================

Analyzes tests by category to identify issues and provide comprehensive validation.
"""

import subprocess
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict


@dataclass
class CategoryResult:
    """Test category execution result."""
    category: str
    path: str
    total_tests: int
    passed: int
    failed: int
    errors: int
    skipped: int
    execution_time: float
    status: str  # SUCCESS, PARTIAL, FAILED
    error_details: List[str]


class SystematicTestAnalyzer:
    """Analyzes TKA test suite systematically by category."""
    
    def __init__(self, tka_root: Path):
        self.tka_root = tka_root
        self.results: List[CategoryResult] = []
        
        # Define test categories to analyze
        self.test_categories = {
            "core_services": "tests/unit/services/",
            "cross_platform": "tests/cross_platform/",
            "interface_coverage": "tests/interface_coverage/",
            "integration": "tests/integration/",
            "launcher_tests": "launcher/tests/",
            "modern_desktop_unit_core": "src/desktop/modern/tests/unit/core/",
            "modern_desktop_unit_interfaces": "src/desktop/modern/tests/unit/interfaces/",
            "modern_desktop_unit_presentation": "src/desktop/modern/tests/unit/presentation/",
            "modern_desktop_integration": "src/desktop/modern/tests/integration/",
            "modern_desktop_specification_core": "src/desktop/modern/tests/specification/core/",
            "modern_desktop_specification_domain": "src/desktop/modern/tests/specification/domain/",
            "modern_desktop_application": "src/desktop/modern/tests/application/",
            "modern_desktop_framework": "src/desktop/modern/tests/framework/",
            "modern_desktop_improved_arch": "src/desktop/modern/tests/improved_architecture/",
            "modern_desktop_root": "src/desktop/modern/tests/*.py",
        }
    
    def analyze_category(self, category: str, path: str) -> CategoryResult:
        """Analyze a specific test category."""
        print(f"\n🔍 Analyzing {category}: {path}")
        
        start_time = time.time()
        error_details = []
        
        try:
            # First, try to collect tests in this category
            collect_result = subprocess.run(
                ["python", "-m", "pytest", path, "--collect-only", "-q"],
                cwd=self.tka_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            # Count collected tests
            total_tests = 0
            if "collected" in collect_result.stdout:
                for line in collect_result.stdout.split('\n'):
                    if "collected" in line and "items" in line:
                        try:
                            total_tests = int(line.split()[0])
                        except:
                            pass
            
            if total_tests == 0:
                execution_time = time.time() - start_time
                return CategoryResult(
                    category=category,
                    path=path,
                    total_tests=0,
                    passed=0,
                    failed=0,
                    errors=0,
                    skipped=0,
                    execution_time=execution_time,
                    status="FAILED",
                    error_details=["No tests found in this category"]
                )
            
            # Now run the tests
            run_result = subprocess.run(
                ["python", "-m", "pytest", path, "-v", "--tb=short"],
                cwd=self.tka_root,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes max per category
            )
            
            execution_time = time.time() - start_time
            
            # Parse results
            passed, failed, errors, skipped = self._parse_test_results(run_result.stdout)
            
            # Determine status
            if errors > 0:
                status = "FAILED"
                error_details = self._extract_error_details(run_result.stdout + run_result.stderr)
            elif failed > 0:
                status = "PARTIAL"
                error_details = self._extract_failure_details(run_result.stdout + run_result.stderr)
            else:
                status = "SUCCESS"
            
            return CategoryResult(
                category=category,
                path=path,
                total_tests=total_tests,
                passed=passed,
                failed=failed,
                errors=errors,
                skipped=skipped,
                execution_time=execution_time,
                status=status,
                error_details=error_details[:10]  # Limit to first 10 errors
            )
            
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return CategoryResult(
                category=category,
                path=path,
                total_tests=0,
                passed=0,
                failed=0,
                errors=1,
                skipped=0,
                execution_time=execution_time,
                status="FAILED",
                error_details=["Category execution timeout (>5 minutes)"]
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return CategoryResult(
                category=category,
                path=path,
                total_tests=0,
                passed=0,
                failed=0,
                errors=1,
                skipped=0,
                execution_time=execution_time,
                status="FAILED",
                error_details=[f"Category analysis error: {str(e)}"]
            )
    
    def _parse_test_results(self, output: str) -> Tuple[int, int, int, int]:
        """Parse pytest output to extract test counts."""
        passed = failed = errors = skipped = 0
        
        lines = output.split('\n')
        for line in lines:
            if " passed" in line and " failed" in line:
                # Format: "X passed, Y failed in Z seconds"
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == "passed" and i > 0:
                        try:
                            passed = int(parts[i-1])
                        except:
                            pass
                    elif part == "failed" and i > 0:
                        try:
                            failed = int(parts[i-1])
                        except:
                            pass
                    elif part == "error" and i > 0:
                        try:
                            errors = int(parts[i-1])
                        except:
                            pass
                    elif part == "skipped" and i > 0:
                        try:
                            skipped = int(parts[i-1])
                        except:
                            pass
            elif " passed in " in line:
                # Format: "X passed in Y seconds"
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == "passed" and i > 0:
                        try:
                            passed = int(parts[i-1])
                        except:
                            pass
        
        return passed, failed, errors, skipped
    
    def _extract_error_details(self, output: str) -> List[str]:
        """Extract error details from pytest output."""
        errors = []
        lines = output.split('\n')
        
        for i, line in enumerate(lines):
            if "ERROR" in line and ("collecting" in line or "ImportError" in line or "ModuleNotFoundError" in line):
                errors.append(line.strip())
            elif "ModuleNotFoundError:" in line or "ImportError:" in line:
                errors.append(line.strip())
        
        return errors
    
    def _extract_failure_details(self, output: str) -> List[str]:
        """Extract failure details from pytest output."""
        failures = []
        lines = output.split('\n')
        
        for line in lines:
            if "FAILED" in line:
                failures.append(line.strip())
        
        return failures
    
    def analyze_all_categories(self) -> Dict:
        """Analyze all test categories."""
        print("🚀 Starting Systematic Test Analysis")
        print("=" * 60)
        
        total_start_time = time.time()
        
        for category, path in self.test_categories.items():
            result = self.analyze_category(category, path)
            self.results.append(result)
            
            # Print immediate feedback
            if result.status == "SUCCESS":
                print(f"✅ {category}: {result.passed}/{result.total_tests} passed ({result.execution_time:.2f}s)")
            elif result.status == "PARTIAL":
                print(f"⚠️ {category}: {result.passed}/{result.total_tests} passed, {result.failed} failed ({result.execution_time:.2f}s)")
            else:
                print(f"❌ {category}: FAILED - {result.error_details[0] if result.error_details else 'Unknown error'}")
        
        total_execution_time = time.time() - total_start_time
        
        # Generate summary
        summary = self._generate_summary(total_execution_time)
        return summary
    
    def _generate_summary(self, total_time: float) -> Dict:
        """Generate analysis summary."""
        total_tests = sum(r.total_tests for r in self.results)
        total_passed = sum(r.passed for r in self.results)
        total_failed = sum(r.failed for r in self.results)
        total_errors = sum(r.errors for r in self.results)
        total_skipped = sum(r.skipped for r in self.results)
        
        successful_categories = len([r for r in self.results if r.status == "SUCCESS"])
        partial_categories = len([r for r in self.results if r.status == "PARTIAL"])
        failed_categories = len([r for r in self.results if r.status == "FAILED"])
        
        return {
            "total_categories": len(self.results),
            "successful_categories": successful_categories,
            "partial_categories": partial_categories,
            "failed_categories": failed_categories,
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "total_errors": total_errors,
            "total_skipped": total_skipped,
            "total_execution_time": total_time,
            "success_rate": (total_passed / total_tests * 100) if total_tests > 0 else 0
        }
    
    def generate_detailed_report(self) -> str:
        """Generate detailed analysis report."""
        summary = self._generate_summary(0)
        
        report = []
        report.append("# TKA Test Suite Systematic Analysis Report")
        report.append("=" * 60)
        report.append("")
        
        # Executive Summary
        report.append("## EXECUTIVE SUMMARY")
        report.append(f"- **Total Categories Analyzed**: {summary['total_categories']}")
        report.append(f"- **Successful Categories**: {summary['successful_categories']} ({summary['successful_categories']/summary['total_categories']*100:.1f}%)")
        report.append(f"- **Partial Categories**: {summary['partial_categories']} ({summary['partial_categories']/summary['total_categories']*100:.1f}%)")
        report.append(f"- **Failed Categories**: {summary['failed_categories']} ({summary['failed_categories']/summary['total_categories']*100:.1f}%)")
        report.append("")
        report.append(f"- **Total Tests Found**: {summary['total_tests']}")
        report.append(f"- **Tests Passed**: {summary['total_passed']} ({summary['success_rate']:.1f}%)")
        report.append(f"- **Tests Failed**: {summary['total_failed']}")
        report.append(f"- **Import/Collection Errors**: {summary['total_errors']}")
        report.append(f"- **Tests Skipped**: {summary['total_skipped']}")
        report.append("")
        
        # Category Details
        report.append("## CATEGORY ANALYSIS")
        report.append("")
        
        for result in self.results:
            status_icon = "✅" if result.status == "SUCCESS" else "⚠️" if result.status == "PARTIAL" else "❌"
            report.append(f"### {status_icon} {result.category}")
            report.append(f"- **Path**: `{result.path}`")
            report.append(f"- **Status**: {result.status}")
            report.append(f"- **Tests**: {result.total_tests} total, {result.passed} passed, {result.failed} failed, {result.errors} errors")
            report.append(f"- **Execution Time**: {result.execution_time:.2f} seconds")
            
            if result.error_details:
                report.append("- **Issues**:")
                for error in result.error_details[:5]:  # Show first 5 errors
                    report.append(f"  - {error}")
                if len(result.error_details) > 5:
                    report.append(f"  - ... and {len(result.error_details) - 5} more issues")
            
            report.append("")
        
        return "\n".join(report)
    
    def save_results(self, filename: str = "systematic_test_analysis.json"):
        """Save results to JSON file."""
        data = {
            "results": [asdict(result) for result in self.results],
            "summary": self._generate_summary(0),
            "timestamp": time.time()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"📄 Analysis results saved to: {filename}")


def main():
    """Main analysis function."""
    tka_root = Path(".")
    
    analyzer = SystematicTestAnalyzer(tka_root)
    summary = analyzer.analyze_all_categories()
    
    # Generate and save reports
    report = analyzer.generate_detailed_report()
    
    with open("systematic_test_analysis_report.md", 'w', encoding='utf-8') as f:
        f.write(report)
    
    analyzer.save_results()
    
    # Print final summary
    print("\n" + "=" * 60)
    print("🎯 SYSTEMATIC ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"📊 Categories: {summary['successful_categories']} success, {summary['partial_categories']} partial, {summary['failed_categories']} failed")
    print(f"📊 Tests: {summary['total_passed']}/{summary['total_tests']} passed ({summary['success_rate']:.1f}%)")
    print(f"⏱️ Total Time: {summary['total_execution_time']:.2f} seconds")
    print(f"📄 Reports saved: systematic_test_analysis_report.md, systematic_test_analysis.json")


if __name__ == "__main__":
    main()
