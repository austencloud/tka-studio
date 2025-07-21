#!/usr/bin/env python3
"""
Automated test execution script for Sequence Card Tab.

This script runs all tests and generates a comprehensive report.
Run this script to validate the complete sequence card tab implementation.
"""

import subprocess
import sys
import json
from pathlib import Path
import time
import os

def run_test_phase(phase_name, test_command, required_passes=None):
    """Run a test phase and return results."""
    print(f"\n{'='*60}")
    print(f"PHASE: {phase_name}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        # Set environment variables for testing
        env = os.environ.copy()
        env['QT_QPA_PLATFORM'] = 'offscreen'  # Headless Qt
        env['PYTHONPATH'] = str(Path(__file__).parent / "src")
        
        result = subprocess.run(
            test_command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent,
            env=env
        )
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"Command: {test_command}")
        print(f"Duration: {duration:.2f}s")
        print(f"Return code: {result.returncode}")
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout[-2000:])  # Last 2000 chars to avoid overwhelming output
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr[-1000:])  # Last 1000 chars
        
        success = result.returncode == 0
        
        # Parse test results for more detailed reporting
        test_count = 0
        passed_count = 0
        failed_count = 0
        
        if "collected" in result.stdout:
            lines = result.stdout.split('\n')
            for line in lines:
                if "passed" in line and "failed" in line:
                    # Parse pytest summary line
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == "passed" and i > 0:
                            try:
                                passed_count = int(parts[i-1])
                            except:
                                pass
                        elif part == "failed" and i > 0:
                            try:
                                failed_count = int(parts[i-1])
                            except:
                                pass
                elif "collected" in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if part == "items" and i > 0:
                            try:
                                test_count = int(parts[i-1])
                            except:
                                pass
        
        return {
            'phase': phase_name,
            'success': success,
            'duration': duration,
            'command': test_command,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'test_count': test_count,
            'passed_count': passed_count,
            'failed_count': failed_count
        }
        
    except Exception as e:
        print(f"Error running {phase_name}: {e}")
        return {
            'phase': phase_name,
            'success': False,
            'duration': 0,
            'error': str(e),
            'test_count': 0,
            'passed_count': 0,
            'failed_count': 0
        }

def check_prerequisites():
    """Check that all prerequisites are met."""
    print("CHECKING PREREQUISITES...")
    print("=" * 40)
    
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 8):
        issues.append(f"Python 3.8+ required, found {sys.version}")
    else:
        print(f"✅ Python version: {sys.version}")
    
    # Check required packages
    required_packages = [
        'pytest', 'pytest-qt', 'PyQt6', 'psutil'
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} installed")
        except ImportError:
            issues.append(f"Missing package: {package}")
            print(f"❌ {package} NOT installed")
    
    # Check project structure
    project_root = Path(__file__).parent
    required_paths = [
        "src/application/services/sequence_card",
        "src/presentation/tabs/sequence_card", 
        "src/core/interfaces/sequence_card_services.py",
        "tests/sequence_card"
    ]
    
    for path in required_paths:
        full_path = project_root / path
        if full_path.exists():
            print(f"✅ {path} exists")
        else:
            issues.append(f"Missing path: {path}")
            print(f"❌ {path} NOT found")
    
    if issues:
        print(f"\n❌ PREREQUISITE ISSUES FOUND:")
        for issue in issues:
            print(f"  - {issue}")
        
        print(f"\nTO FIX ISSUES:")
        print(f"  pip install pytest pytest-qt PyQt6 psutil")
        print(f"  # Ensure you're in the correct directory")
        print(f"  # Current directory: {project_root}")
        
        return False
    
    print(f"\n✅ All prerequisites met!")
    return True

def main():
    """Run all test phases and generate report."""
    
    print("SEQUENCE CARD TAB - AUTOMATED TEST EXECUTION")
    print("=" * 80)
    print("This script validates the complete sequence card tab implementation")
    print("=" * 80)
    
    # Check prerequisites first
    if not check_prerequisites():
        sys.exit(1)
    
    # Test phases in order of dependency
    phases = [
        {
            'name': 'Service Layer Tests (Unit)',
            'command': 'pytest tests/sequence_card/test_sequence_card_services.py -v --tb=short --maxfail=10',
            'critical': True
        },
        {
            'name': 'Service Registration Tests',
            'command': 'pytest tests/sequence_card/test_sequence_card_integration.py::TestSequenceCardServiceRegistration -v --tb=short',
            'critical': True
        },
        {
            'name': 'UI Component Tests',
            'command': 'pytest tests/sequence_card/test_sequence_card_ui.py -v --tb=short --maxfail=5',
            'critical': False  # UI tests can be flaky in CI
        },
        {
            'name': 'Integration Tests',
            'command': 'pytest tests/sequence_card/test_sequence_card_integration.py::TestSequenceCardTabIntegration -v --tb=short',
            'critical': True
        },
        {
            'name': 'Performance Tests',
            'command': 'pytest tests/sequence_card/ -m performance -v --tb=short',
            'critical': False  # Performance tests are advisory
        },
        {
            'name': 'Complete Test Suite with Coverage',
            'command': 'pytest tests/sequence_card/ --cov=src/application/services/sequence_card --cov=src/presentation/tabs/sequence_card --cov-report=term-missing --cov-report=html -v --maxfail=20',
            'critical': False  # Coverage is nice-to-have
        }
    ]
    
    results = []
    critical_failures = []
    
    # Run each phase
    for phase in phases:
        result = run_test_phase(phase['name'], phase['command'])
        results.append(result)
        
        if not result['success']:
            print(f"\n❌ FAILURE: {phase['name']}")
            if phase.get('critical', False):
                critical_failures.append(phase['name'])
        else:
            print(f"\n✅ SUCCESS: {phase['name']}")
            if result['test_count'] > 0:
                print(f"   Tests: {result['passed_count']}/{result['test_count']} passed")
    
    # Generate summary report
    print(f"\n{'='*80}")
    print("FINAL SUMMARY REPORT")
    print(f"{'='*80}")
    
    total_phases = len(results)
    successful_phases = sum(1 for r in results if r['success'])
    total_duration = sum(r.get('duration', 0) for r in results)
    total_tests = sum(r.get('test_count', 0) for r in results)
    total_passed = sum(r.get('passed_count', 0) for r in results)
    total_failed = sum(r.get('failed_count', 0) for r in results)
    
    print(f"Phase Summary:")
    print(f"  Total Phases: {total_phases}")
    print(f"  Successful: {successful_phases}")
    print(f"  Failed: {total_phases - successful_phases}")
    print(f"  Critical Failures: {len(critical_failures)}")
    print(f"  Total Duration: {total_duration:.2f}s")
    
    print(f"\nTest Summary:")
    print(f"  Total Tests: {total_tests}")
    print(f"  Passed: {total_passed}")
    print(f"  Failed: {total_failed}")
    if total_tests > 0:
        print(f"  Success Rate: {total_passed/total_tests*100:.1f}%")
    
    print(f"\nPhase Success Rate: {successful_phases/total_phases*100:.1f}%")
    
    # Detailed results
    print(f"\nDETAILED RESULTS:")
    for result in results:
        status = "✅ PASS" if result['success'] else "❌ FAIL"
        duration = result.get('duration', 0)
        test_info = ""
        if result.get('test_count', 0) > 0:
            test_info = f" | {result['passed_count']}/{result['test_count']} tests"
        print(f"  {status} | {result['phase']} | {duration:.2f}s{test_info}")
    
    # Critical failure details
    if critical_failures:
        print(f"\n❌ CRITICAL FAILURES:")
        for failure in critical_failures:
            print(f"  - {failure}")
    
    # Save results to file
    results_file = Path(__file__).parent / "sequence_card_test_results.json"
    with open(results_file, 'w') as f:
        json.dump({
            'timestamp': time.time(),
            'summary': {
                'total_phases': total_phases,
                'successful_phases': successful_phases,
                'total_tests': total_tests,
                'total_passed': total_passed,
                'total_failed': total_failed,
                'critical_failures': critical_failures,
                'total_duration': total_duration
            },
            'results': results
        }, f, indent=2)
    
    print(f"\nDetailed results saved to: {results_file}")
    
    # Coverage report location
    coverage_dir = Path(__file__).parent / "htmlcov"
    if coverage_dir.exists():
        print(f"Coverage report available at: {coverage_dir / 'index.html'}")
    
    # Final decision
    print(f"\n{'='*80}")
    if critical_failures:
        print(f"❌ CRITICAL FAILURES DETECTED")
        print(f"The following critical test phases failed:")
        for failure in critical_failures:
            print(f"  - {failure}")
        print(f"\nSequence Card Tab implementation needs fixes before deployment.")
        print(f"Review the detailed output above to identify issues.")
        sys.exit(1)
    elif successful_phases == total_phases:
        print(f"🎉 ALL TESTS PASSED!")
        print(f"Sequence Card Tab implementation is fully validated and ready for use.")
        print(f"\nImplementation Summary:")
        print(f"  ✅ All services implemented and tested")
        print(f"  ✅ UI components implemented and tested") 
        print(f"  ✅ Integration working correctly")
        print(f"  ✅ Performance within acceptable limits")
        print(f"  ✅ DI container integration successful")
        print(f"\nThe tab is ready to be used in the main application!")
        sys.exit(0)
    else:
        print(f"⚠️  SOME NON-CRITICAL TESTS FAILED")
        print(f"Core functionality is working, but some optional features may have issues.")
        print(f"Critical components: ✅ PASSED")
        print(f"Optional components: ❌ Some failures")
        print(f"\nSequence Card Tab core implementation is functional.")
        print(f"Consider reviewing non-critical failures for optimal experience.")
        sys.exit(0)

if __name__ == "__main__":
    main()
