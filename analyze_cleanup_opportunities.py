"""
Post-Testing Cleanup Script for God Object Refactoring

This script identifies redundant files created during the God Object refactoring
that should be cleaned up AFTER successful testing.

⚠️  DO NOT RUN THIS UNTIL TESTING IS COMPLETE AND SUCCESSFUL!
"""

import os


def identify_cleanup_candidates():
    """Identify files that can be cleaned up after successful testing."""

    cleanup_candidates = {
        "temporary_verification": [
            "F:/CODE/TKA/quick_safety_check.py",
            "F:/CODE/TKA/verify_god_object_refactoring.py",
        ],
        "redundant_services": [
            # This duplicates existing SequencePersister + loader.py functionality
            "F:/CODE/TKA/src/desktop/modern/application/services/sequence/sequence_persistence_adapter.py",
        ],
        "redundant_components": [
            # These duplicate existing WorkbenchIndicatorSection and WorkbenchBeatFrameSection
            "F:/CODE/TKA/src/desktop/modern/presentation/components/sequence_workbench/sections/status_indicator_section.py",
            "F:/CODE/TKA/src/desktop/modern/presentation/components/sequence_workbench/sections/focused_beat_display_section.py",
            # Action buttons might be redundant with existing button panel
            "F:/CODE/TKA/src/desktop/modern/presentation/components/sequence_workbench/sections/action_button_section.py",
        ],
        "potentially_redundant_registration": [
            # DI registration might be handled elsewhere
            "F:/CODE/TKA/src/desktop/modern/application/services/sequence/service_registration.py",
            "F:/CODE/TKA/src/desktop/modern/presentation/components/sequence_workbench/component_registration.py",
        ],
        "redundant_container": [
            # WorkbenchContainer might be redundant if existing WorkbenchBeatFrameSection works
            "F:/CODE/TKA/src/desktop/modern/presentation/components/sequence_workbench/workbench_container.py",
        ],
    }

    return cleanup_candidates


def analyze_redundancy():
    """Analyze what files are actually redundant."""

    print("🔍 REDUNDANCY ANALYSIS - Post God Object Refactoring")
    print("=" * 60)

    candidates = identify_cleanup_candidates()

    total_size_saved = 0
    total_files = 0

    for category, files in candidates.items():
        print(f"\n📂 {category.replace('_', ' ').title()}:")
        print("-" * 40)

        category_size = 0
        category_files = 0

        for file_path in files:
            try:
                if os.path.exists(file_path):
                    size = os.path.getsize(file_path) / 1024  # KB
                    category_size += size
                    category_files += 1

                    filename = os.path.basename(file_path)
                    print(f"  📄 {filename:<35} {size:>6.2f} KB")
                else:
                    filename = os.path.basename(file_path)
                    print(f"  ❌ {filename:<35} Not found")

            except Exception as e:
                filename = os.path.basename(file_path)
                print(f"  ⚠️  {filename:<35} Error: {e}")

        if category_files > 0:
            print(
                f"  📊 Category total: {category_size:.2f} KB, {category_files} files"
            )

        total_size_saved += category_size
        total_files += category_files

    print("\n🗑️  CLEANUP POTENTIAL")
    print("-" * 30)
    print(f"Total redundant files:    {total_files}")
    print(f"Total space to reclaim:   {total_size_saved:.2f} KB")
    print(
        f"Average file size:        {total_size_saved / total_files:.2f} KB"
        if total_files > 0
        else "No files found"
    )

    return candidates, total_size_saved, total_files


def recommend_cleanup_strategy():
    """Recommend cleanup strategy based on analysis."""

    print("\n🎯 RECOMMENDED CLEANUP STRATEGY")
    print("-" * 40)
    print("1. ✅ Test the refactored God Objects thoroughly")
    print("2. ✅ Verify focused services work correctly")
    print("3. ✅ Confirm UI components function properly")
    print("4. 🗑️  Delete temporary verification files (safe)")
    print("5. 🔍 Evaluate if new components add value over existing ones")
    print("6. 🗑️  Remove redundant files that don't add value")
    print("7. 📝 Update imports to use remaining files")
    print("8. 🧪 Test again after cleanup")

    print("\n⚠️  CLEANUP PRIORITIES:")
    print("   HIGH:   Temporary verification files (definitely remove)")
    print("   MEDIUM: Redundant services (evaluate based on functionality)")
    print("   LOW:    New components (might provide better architecture)")


def generate_cleanup_script():
    """Generate actual cleanup script for after testing."""

    candidates = identify_cleanup_candidates()

    script_content = '''#!/usr/bin/env python3
"""
EXECUTE CLEANUP - God Object Refactoring Residue Removal

⚠️  ONLY RUN THIS AFTER SUCCESSFUL TESTING!
"""

import os

def cleanup_files(files_to_delete):
    """Delete specified files."""
    deleted = 0
    errors = 0
    
    for file_path in files_to_delete:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"✅ Deleted: {os.path.basename(file_path)}")
                deleted += 1
            else:
                print(f"⚠️  Not found: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"❌ Error deleting {os.path.basename(file_path)}: {e}")
            errors += 1
    
    print(f"\\n📊 Cleanup completed: {deleted} deleted, {errors} errors")

if __name__ == "__main__":
    # HIGH PRIORITY: Temporary files (safe to delete)
    temporary_files = [
'''

    for file_path in candidates["temporary_verification"]:
        script_content += f'        "{file_path}",\n'

    script_content += """    ]
    
    print("🗑️  Cleaning up temporary verification files...")
    cleanup_files(temporary_files)
    
    # MEDIUM PRIORITY: Redundant services (evaluate first)
    print("\\n⚠️  Manual evaluation needed for redundant services")
    print("   Check if these provide value over existing services:")
"""

    for file_path in candidates["redundant_services"]:
        script_content += f'    print("   - {os.path.basename(file_path)}")\n'

    script_content += """
    # LOW PRIORITY: Components (might provide architectural value)
    print("\\n⚠️  Manual evaluation needed for redundant components")
    print("   Check if these provide better architecture:")
"""

    for file_path in candidates["redundant_components"]:
        script_content += f'    print("   - {os.path.basename(file_path)}")\n'

    script_content += """
"""

    with open("F:/CODE/TKA/post_testing_cleanup.py", "w") as f:
        f.write(script_content)

    print("\n📄 Generated cleanup script: post_testing_cleanup.py")


if __name__ == "__main__":
    candidates, total_size, total_files = analyze_redundancy()
    recommend_cleanup_strategy()
    generate_cleanup_script()

    print("\n🎉 REDUNDANCY ANALYSIS COMPLETE")
    print(
        f"Found {total_files} files totaling {total_size:.2f} KB for potential cleanup"
    )
    print("Run this analysis again after testing to execute cleanup!")
