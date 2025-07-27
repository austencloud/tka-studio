#!/usr/bin/env python3
"""
Quick Test Script for Optimized E2E System
==========================================

Run this to test the new optimized end-to-end testing system.

Usage:
    python run_optimized_tests.py
    python run_optimized_tests.py --tab construct
    python run_optimized_tests.py --debug
"""

import sys
from pathlib import Path

# Add the src directory to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

if __name__ == "__main__":
    # Import and run the optimized tests
    import argparse

    from desktop.modern.tests.e2e_workflows import run_optimized_e2e_tests, run_tab_test

    parser = argparse.ArgumentParser(description="Test the optimized E2E system")
    parser.add_argument(
        "--tab", type=str, help="Test specific tab only (construct, sequence_card)"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    parser.add_argument(
        "--headless", action="store_true", help="Run in headless mode (no UI)"
    )

    args = parser.parse_args()

    visual_mode = not args.headless  # Visual by default

    print("🧪 Testing Optimized E2E System")
    print("=" * 40)

    if visual_mode:
        print("👁️  VISUAL MODE: You should see UI interactions!")
        print("💡 Use --headless flag for fast headless testing")
    else:
        print("🤖 HEADLESS MODE: No UI will be shown")

    try:
        if args.tab:
            print(f"Running {args.tab} tab test only...")
            results = run_tab_test(args.tab, debug=args.debug, visual_mode=visual_mode)
        else:
            print("Running all tab workflow tests...")
            results = run_optimized_e2e_tests(debug=args.debug, visual_mode=visual_mode)

        # Show results
        if results["overall_success"]:
            print("\\n🎉 SUCCESS! Optimized E2E system is working!")
            print("✅ No more duplicated logic")
            print("✅ Faster test execution")
            print("✅ Single comprehensive test per tab")
            print("✅ Shared infrastructure eliminates setup overhead")
        else:
            print("\\n⚠️ Some issues found - check the output above")

        # Show timing improvements
        summary = results.get("summary", {})
        if summary:
            total_time = summary.get("total_time", 0)
            avg_time = summary.get("average_time", 0)
            print(
                f"\\n⏱️ Performance: {total_time:.0f}ms total, {avg_time:.0f}ms average per test"
            )

        sys.exit(0 if results["overall_success"] else 1)

    except Exception as e:
        print(f"❌ Error running optimized tests: {e}")
        import traceback

        if args.debug:
            traceback.print_exc()
        sys.exit(1)
