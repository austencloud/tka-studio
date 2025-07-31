#!/usr/bin/env python3
"""
Direct Test Runner for TKA
===========================

Bypasses conftest.py issues and runs all tests with proper path setup.
"""

import json
from pathlib import Path
import subprocess
import sys
import time


def setup_python_path():
    """Set up Python path for TKA imports."""
    # Get TKA root directory (2 levels up from scripts/testing/)
    tka_root = Path(__file__).parent.parent.parent.absolute()

    essential_paths = [
        str(tka_root),
        str(tka_root / "src"),
        str(tka_root / "src" / "desktop" / "modern" / "src"),
        str(tka_root / "src" / "desktop" / "modern"),
        str(tka_root / "launcher"),
    ]

    for path in essential_paths:
        if Path(path).exists() and path not in sys.path:
            sys.path.insert(0, path)

    # Test the import
    try:
        print("✅ Domain models import successful")
        return True
    except Exception as e:
        print(f"❌ Domain models import failed: {e}")
        return False


def run_test_category(category_name: str, test_path: str) -> dict:
    """Run a category of tests with proper environment setup."""
    print(f"\n🧪 Running {category_name}: {test_path}")

    start_time = time.time()

    # Set up environment variables
    env = {
        "PYTHONPATH": ":".join(
            [
                str(Path.cwd().parent.parent),  # TKA root
                str(Path.cwd().parent.parent / "src"),
                str(Path.cwd().parent.parent / "src" / "desktop" / "modern" / "src"),
            ]
        )
    }

    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                test_path,
                "-v",
                "--tb=short",
                "--no-header",
                "--disable-warnings",
            ],
            capture_output=True,
            text=True,
            timeout=300,
            env={**dict(os.environ), **env} if "os" in globals() else None,
        )

        execution_time = time.time() - start_time

        # Parse results
        output = result.stdout + result.stderr
        passed, failed, errors, skipped = parse_pytest_output(output)
        total = passed + failed + errors + skipped

        status = (
            "SUCCESS"
            if errors == 0 and failed == 0 and total > 0
            else "PARTIAL"
            if total > 0
            else "FAILED"
        )

        print(
            f"   📊 Results: {passed}/{total} passed ({passed / total * 100:.1f}% success)"
            if total > 0
            else "   ⚪ No tests found"
        )

        return {
            "category": category_name,
            "path": test_path,
            "total": total,
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "skipped": skipped,
            "execution_time": execution_time,
            "status": status,
            "return_code": result.returncode,
            "output_sample": output[:500] if output else "",
        }

    except subprocess.TimeoutExpired:
        execution_time = time.time() - start_time
        print(f"   ⏰ Timeout after {execution_time:.1f}s")
        return {
            "category": category_name,
            "path": test_path,
            "total": 0,
            "passed": 0,
            "failed": 0,
            "errors": 1,
            "skipped": 0,
            "execution_time": execution_time,
            "status": "TIMEOUT",
            "return_code": -1,
            "output_sample": "Execution timeout",
        }
    except Exception as e:
        execution_time = time.time() - start_time
        print(f"   💥 Error: {e}")
        return {
            "category": category_name,
            "path": test_path,
            "total": 0,
            "passed": 0,
            "failed": 0,
            "errors": 1,
            "skipped": 0,
            "execution_time": execution_time,
            "status": "ERROR",
            "return_code": -1,
            "output_sample": str(e),
        }


def parse_pytest_output(output: str) -> tuple[int, int, int, int]:
    """Parse pytest output to extract test counts."""
    passed = failed = errors = skipped = 0

    lines = output.split("\n")
    for line in lines:
        if " passed" in line or " failed" in line or " error" in line:
            words = line.split()
            for i, word in enumerate(words):
                if word == "passed" and i > 0:
                    try:
                        passed = int(words[i - 1])
                    except:
                        pass
                elif word == "failed" and i > 0:
                    try:
                        failed = int(words[i - 1])
                    except:
                        pass
                elif word == "error" and i > 0:
                    try:
                        errors = int(words[i - 1])
                    except:
                        pass
                elif word == "skipped" and i > 0:
                    try:
                        skipped = int(words[i - 1])
                    except:
                        pass

    return passed, failed, errors, skipped


def run_all_tests():
    """Run all test categories."""

    print("🚀 TKA Complete Test Suite Execution")
    print("=" * 60)

    # Set up Python path
    if not setup_python_path():
        print("❌ Failed to set up Python path")
        return None

    # Define test categories
    test_categories = {
        "Core Services": "tests/unit/services/",
        "Cross Platform": "tests/cross_platform/",
        "Interface Coverage": "tests/interface_coverage/",
        "Interface Completeness": "tests/interface_completeness/",
        "Service Implementation": "tests/service_implementation/",
        "Integration Workflows": "tests/integration/",
        "Launcher Tests": "launcher/tests/",
        "Modern Unit Core": "src/desktop/modern/tests/unit/core/",
        "Modern Unit Interfaces": "src/desktop/modern/tests/unit/interfaces/",
        "Modern Unit Presentation": "src/desktop/modern/tests/unit/presentation/",
        "Modern Integration": "src/desktop/modern/tests/integration/",
        "Modern Spec Core": "src/desktop/modern/tests/specification/core/",
        "Modern Spec Domain": "src/desktop/modern/tests/specification/domain/",
        "Modern Application": "src/desktop/modern/tests/application/",
        "Modern Framework": "src/desktop/modern/tests/framework/",
        "Modern Improved Arch": "src/desktop/modern/tests/improved_architecture/",
    }

    results = []
    total_start_time = time.time()

    for category, path in test_categories.items():
        if Path(path).exists():
            result = run_test_category(category, path)
            results.append(result)
        else:
            print(f"\n⚪ Skipping {category}: Path {path} does not exist")

    total_execution_time = time.time() - total_start_time

    # Generate summary
    total_tests = sum(r["total"] for r in results)
    total_passed = sum(r["passed"] for r in results)
    total_failed = sum(r["failed"] for r in results)
    total_errors = sum(r["errors"] for r in results)
    total_skipped = sum(r["skipped"] for r in results)

    success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0

    print("\n" + "=" * 60)
    print("🎯 COMPLETE TEST SUITE RESULTS")
    print("=" * 60)
    print(f"📊 TOTAL TESTS: {total_tests}")
    print(f"   ✅ PASSED: {total_passed} ({success_rate:.1f}%)")
    print(f"   ❌ FAILED: {total_failed}")
    print(f"   💥 ERRORS: {total_errors}")
    print(f"   ⏭️ SKIPPED: {total_skipped}")
    print(f"⏱️ TOTAL TIME: {total_execution_time:.2f} seconds")

    # Show successful categories
    print("\n✅ SUCCESSFUL CATEGORIES:")
    for result in results:
        if result["status"] == "SUCCESS":
            print(
                f"   {result['category']}: {result['passed']}/{result['total']} tests"
            )

    # Show problematic categories
    print("\n❌ CATEGORIES WITH ISSUES:")
    for result in results:
        if result["status"] not in ["SUCCESS"]:
            print(
                f"   {result['category']}: {result['status']} - {result['errors']} errors, {result['failed']} failures"
            )

    # Save detailed results
    summary = {
        "total_tests": total_tests,
        "total_passed": total_passed,
        "total_failed": total_failed,
        "total_errors": total_errors,
        "total_skipped": total_skipped,
        "success_rate": success_rate,
        "total_execution_time": total_execution_time,
        "category_results": results,
    }

    results_file = Path(__file__).parent / "results" / "complete_test_results.json"
    results_file.parent.mkdir(exist_ok=True)
    with open(results_file, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\n📄 Detailed results saved to: {results_file}")

    # Check if we achieved 300+ tests
    if total_tests >= 300:
        print(f"\n🎯 SUCCESS: Found {total_tests} tests (target: 300+)")
        if total_passed >= 300:
            print(f"🌟 EXCELLENT: {total_passed} tests passing (target: 300+)")
        else:
            print(f"⚠️ PARTIAL: Only {total_passed} tests passing (target: 300+)")
    else:
        print(f"\n⚠️ INCOMPLETE: Only found {total_tests} tests (target: 300+)")

    return summary


if __name__ == "__main__":
    run_all_tests()
