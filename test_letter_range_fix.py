#!/usr/bin/env python3
"""
Test the letter range parsing fix
"""

import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src" / "desktop" / "modern" / "src"))


def test_letter_range_parsing():
    """Test the letter range parsing fix."""
    print("🔍 Testing letter range parsing...")

    # Test the parsing logic
    filter_value = "A-D"
    if "-" in filter_value and len(filter_value) == 3:
        start_letter, end_letter = filter_value.split("-")
        letters = [chr(i) for i in range(ord(start_letter), ord(end_letter) + 1)]
        print(f"📊 {filter_value} -> {letters}")

    # Test with different ranges
    test_ranges = ["A-D", "E-H", "I-L", "M-P", "Q-T", "U-Z"]
    for range_str in test_ranges:
        if "-" in range_str and len(range_str) == 3:
            start_letter, end_letter = range_str.split("-")
            letters = [chr(i) for i in range(ord(start_letter), ord(end_letter) + 1)]
            print(f"📊 {range_str} -> {letters}")


def test_browse_tab_filtering():
    """Test the browse tab filtering with the fix."""
    print("\n🔍 Testing browse tab filtering with letter ranges...")

    try:
        from presentation.tabs.browse.models import FilterType
        from presentation.tabs.browse.modern_browse_tab import ModernBrowseTab
        from PyQt6.QtWidgets import QApplication

        # Create QApplication if it doesn't exist
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)

        # Create browse tab
        tka_root = Path(__file__).parent
        sequences_dir = tka_root / "sequences"
        settings_file = tka_root / "settings.json"

        browse_tab = ModernBrowseTab(sequences_dir, settings_file)

        # Test the filtering with letter ranges
        test_filters = ["A-D", "E-H", "I-L", "Q-T", "U-Z"]
        for filter_value in test_filters:
            filtered_sequences = browse_tab._apply_dictionary_filter(
                FilterType.STARTING_LETTER, filter_value
            )
            print(f"📊 {filter_value}: {len(filtered_sequences)} sequences")

        # Test "All Letters"
        all_sequences = browse_tab._apply_dictionary_filter(
            FilterType.STARTING_LETTER, "All Letters"
        )
        print(f"📊 All Letters: {len(all_sequences)} sequences")

    except Exception as e:
        print(f"❌ Error testing browse tab filtering: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_letter_range_parsing()
    test_browse_tab_filtering()
