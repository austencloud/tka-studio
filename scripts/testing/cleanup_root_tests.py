#!/usr/bin/env python3
"""
Root Directory Test Cleanup Script
==================================

Systematically clean up test files in the root directory after consolidation.
Removes duplicates and debug scaffolding while preserving any unique valuable tests.
"""

from pathlib import Path


def analyze_root_tests() -> dict[str, str]:
    """Analyze root test files and categorize them."""

    # Files that were migrated and can be safely deleted (duplicates)
    migrated_duplicates = [
        "test_component_pools.py",  # -> tests_new/regression/performance/memory_usage/
        "test_pool_performance.py",  # -> tests_new/regression/performance/memory_usage/
        "test_browse_tab_crashes.py",  # -> tests_new/regression/bugs/
        "test_construct_tab_loading.py",  # -> tests_new/ui/desktop_qt/components/
        "test_start_position_visibility.py",  # -> tests_new/ui/desktop_qt/components/
        "test_view_sizes.py",  # -> tests_new/ui/desktop_qt/layouts/
        "test_step_by_step.py",  # -> tests_new/ui/desktop_qt/interactions/
        "test_browse_import.py",  # -> tests_new/unit/core/utils/
        "test_browse_imports.py",  # -> tests_new/unit/core/utils/
        "test_browse_simple.py",  # -> tests_new/unit/core/utils/
    ]

    # Debug scaffolding files marked for deletion
    debug_scaffolding = [
        "comprehensive_visibility_test.py",
        "dependency_analysis_test.py",
        "simple_visibility_test.py",
        "final_startup_test.py",
    ]

    categorization = {}

    # Categorize migrated duplicates
    for file in migrated_duplicates:
        if Path(file).exists():
            categorization[file] = "migrated_duplicate"

    # Categorize debug scaffolding
    for file in debug_scaffolding:
        if Path(file).exists():
            categorization[file] = "debug_scaffolding"

    return categorization


def cleanup_root_tests(dry_run: bool = False) -> dict[str, list[str]]:
    """Clean up root test files."""

    categorization = analyze_root_tests()
    results = {
        "deleted_duplicates": [],
        "deleted_scaffolding": [],
        "preserved": [],
        "errors": [],
    }

    print("🧹 Root Directory Test Cleanup")
    print("=" * 50)

    for file, category in categorization.items():
        file_path = Path(file)

        if category == "migrated_duplicate":
            print(f"🗑️  Removing duplicate: {file} (migrated to tests_new/)")
            if not dry_run:
                try:
                    file_path.unlink()
                    results["deleted_duplicates"].append(file)
                except Exception as e:
                    results["errors"].append(f"Failed to delete {file}: {e}")
            else:
                print(f"   DRY RUN: Would delete {file}")
                results["deleted_duplicates"].append(file)

        elif category == "debug_scaffolding":
            print(f"🗑️  Removing debug scaffolding: {file}")
            if not dry_run:
                try:
                    file_path.unlink()
                    results["deleted_scaffolding"].append(file)
                except Exception as e:
                    results["errors"].append(f"Failed to delete {file}: {e}")
            else:
                print(f"   DRY RUN: Would delete {file}")
                results["deleted_scaffolding"].append(file)

    # Check for any remaining test files
    remaining_tests = list(Path().glob("test_*.py"))
    if remaining_tests:
        print("\n⚠️  Remaining test files found:")
        for test_file in remaining_tests:
            if test_file.name not in categorization:
                print(f"   📄 {test_file.name} - PRESERVED (not categorized)")
                results["preserved"].append(test_file.name)

    return results


def main():
    """Main cleanup function."""
    import argparse

    parser = argparse.ArgumentParser(description="Clean up root directory test files")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without making changes",
    )

    args = parser.parse_args()

    print(f"🎯 Root Test Cleanup - {'DRY RUN' if args.dry_run else 'LIVE CLEANUP'}")
    print()

    # Analyze current state
    categorization = analyze_root_tests()
    print(f"📊 Found {len(categorization)} test files to process:")

    duplicates = [f for f, c in categorization.items() if c == "migrated_duplicate"]
    scaffolding = [f for f, c in categorization.items() if c == "debug_scaffolding"]

    print(f"   🔄 Migrated duplicates: {len(duplicates)}")
    print(f"   🐛 Debug scaffolding: {len(scaffolding)}")
    print()

    # Perform cleanup
    results = cleanup_root_tests(dry_run=args.dry_run)

    # Report results
    print("\n📋 CLEANUP SUMMARY:")
    print(f"   ✅ Deleted duplicates: {len(results['deleted_duplicates'])}")
    print(f"   ✅ Deleted scaffolding: {len(results['deleted_scaffolding'])}")
    print(f"   📄 Preserved files: {len(results['preserved'])}")
    print(f"   ❌ Errors: {len(results['errors'])}")

    if results["errors"]:
        print("\n❌ ERRORS:")
        for error in results["errors"]:
            print(f"   {error}")

    if results["preserved"]:
        print("\n📄 PRESERVED FILES:")
        for file in results["preserved"]:
            print(f"   {file}")

    print(
        f"\n🎉 Root directory cleanup {'simulation' if args.dry_run else 'completed'}!"
    )


if __name__ == "__main__":
    main()
