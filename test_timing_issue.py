#!/usr/bin/env python3
"""
Test to verify the timing issue with dictionary loading
"""

import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src" / "desktop" / "modern" / "src"))


def test_loading_timing():
    """Test the timing issue with dictionary loading."""
    print("🔍 Testing dictionary loading timing...")

    try:
        from presentation.tabs.browse.services.modern_dictionary_data_manager import (
            ModernDictionaryDataManager,
        )

        # Create manager
        tka_root = Path(__file__).parent
        data_dir = tka_root / "data"
        manager = ModernDictionaryDataManager(data_dir)

        # Check if data is loaded before calling load_all_sequences
        print(f"📊 Records before loading: {len(manager.get_all_records())}")

        # Apply filter before loading (this simulates the bug)
        print("🔍 Applying filter BEFORE loading...")
        records_before = manager.get_records_by_starting_letters(["A", "B", "C", "D"])
        print(f"📊 A-D records before loading: {len(records_before)}")

        # Now load
        print("🔄 Loading sequences...")
        manager.load_all_sequences()

        # Apply filter after loading
        print("🔍 Applying filter AFTER loading...")
        records_after = manager.get_records_by_starting_letters(["A", "B", "C", "D"])
        print(f"📊 A-D records after loading: {len(records_after)}")

        # Test the has_loaded flag
        print(f"📊 Has loaded flag: {manager._has_loaded}")

    except Exception as e:
        print(f"❌ Error testing timing: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_loading_timing()
