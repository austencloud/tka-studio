#!/usr/bin/env python3
"""
Dictionary Loading Debug Test

This test will help identify why the ModernDictionaryDataManager
is not loading sequences properly, causing "filtered to 0 sequences".
"""

import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src" / "desktop" / "modern" / "src"))


def test_dictionary_path_resolution():
    """Test if we can find the dictionary directory correctly."""
    print("🔍 Testing dictionary path resolution...")

    # Test 1: Direct path construction
    tka_root = Path(__file__).parent
    data_dir = tka_root / "data"
    dictionary_dir = data_dir / "dictionary"

    print(f"📁 TKA root: {tka_root}")
    print(f"📁 Data dir: {data_dir}")
    print(f"📁 Dictionary dir: {dictionary_dir}")
    print(f"📁 Dictionary exists: {dictionary_dir.exists()}")

    if dictionary_dir.exists():
        sequence_dirs = list(dictionary_dir.iterdir())
        print(f"📁 Found {len(sequence_dirs)} sequence directories")

        # Show first few directories
        for i, seq_dir in enumerate(sequence_dirs[:5]):
            if seq_dir.is_dir():
                print(f"   - {seq_dir.name}")

    return dictionary_dir


def test_modern_dictionary_manager():
    """Test the ModernDictionaryDataManager directly."""
    print("\n🔍 Testing ModernDictionaryDataManager directly...")

    try:
        # Import after path setup
        from presentation.tabs.browse.services.modern_dictionary_data_manager import (
            ModernDictionaryDataManager,
        )

        # Create with explicit path
        tka_root = Path(__file__).parent
        data_dir = tka_root / "data"

        print(f"📁 Creating ModernDictionaryDataManager with: {data_dir}")
        manager = ModernDictionaryDataManager(data_dir)

        print(f"📁 Manager dictionary dir: {manager.dictionary_dir}")
        print(f"📁 Manager dictionary exists: {manager.dictionary_dir.exists()}")

        # Test loading
        print("\n🔄 Testing load_all_sequences()...")
        manager.load_all_sequences()

        records = manager.get_all_records()
        print(f"✅ Loaded {len(records)} sequence records")

        # Show first few records
        for i, record in enumerate(records[:3]):
            print(f"   {i+1}. {record.word} - {len(record.thumbnails)} thumbnails")
            if record.thumbnails:
                print(f"      First thumbnail: {record.thumbnails[0]}")

        return manager

    except Exception as e:
        print(f"❌ Error testing ModernDictionaryDataManager: {e}")
        import traceback

        traceback.print_exc()
        return None


def test_filtering():
    """Test the filtering functionality."""
    print("\n🔍 Testing filtering functionality...")

    try:
        # Import after path setup
        from presentation.tabs.browse.services.modern_dictionary_data_manager import (
            ModernDictionaryDataManager,
        )

        # Create manager
        tka_root = Path(__file__).parent
        data_dir = tka_root / "data"
        manager = ModernDictionaryDataManager(data_dir)

        # Load sequences
        manager.load_all_sequences()
        total_records = len(manager.get_all_records())
        print(f"📊 Total records loaded: {total_records}")

        # Test A-D filter
        ad_records = manager.get_records_by_starting_letters(["A", "B", "C", "D"])
        print(f"📊 A-D records: {len(ad_records)}")

        # Test individual letters
        a_records = manager.get_records_by_starting_letter("A")
        print(f"📊 A records: {len(a_records)}")

        # Show some sample records
        if a_records:
            print("   Sample A records:")
            for record in a_records[:3]:
                print(f"      - {record.word}")

        return manager

    except Exception as e:
        print(f"❌ Error testing filtering: {e}")
        import traceback

        traceback.print_exc()
        return None


def test_browse_tab_initialization():
    """Test the browse tab initialization process."""
    print("\n🔍 Testing browse tab initialization...")

    try:
        # Import PyQt6 for GUI testing
        from PyQt6.QtCore import QTimer
        from PyQt6.QtWidgets import QApplication

        # Create QApplication if it doesn't exist
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)

        # Import after path setup
        from presentation.tabs.browse.modern_browse_tab import ModernBrowseTab

        # Create browse tab
        tka_root = Path(__file__).parent
        sequences_dir = tka_root / "sequences"  # Dummy path
        settings_file = tka_root / "settings.json"

        print(f"📁 Creating ModernBrowseTab with sequences_dir: {sequences_dir}")
        browse_tab = ModernBrowseTab(sequences_dir, settings_file)

        print(f"📁 Browse tab dictionary manager: {browse_tab.dictionary_manager}")
        print(f"📁 Dictionary dir: {browse_tab.dictionary_manager.dictionary_dir}")

        # Test filter application
        print("\n🔄 Testing filter application...")
        from presentation.tabs.browse.models import FilterType

        # Apply A-D filter
        filtered_sequences = browse_tab._apply_dictionary_filter(
            FilterType.STARTING_LETTER, ["A", "B", "C", "D"]
        )
        print(f"✅ Filtered sequences (A-D): {len(filtered_sequences)}")

        # Show first few
        for i, seq in enumerate(filtered_sequences[:3]):
            print(f"   {i+1}. {seq.word} - {len(seq.thumbnails)} thumbnails")
            if seq.thumbnails:
                print(f"      First thumbnail: {seq.thumbnails[0]}")

        return browse_tab

    except Exception as e:
        print(f"❌ Error testing browse tab initialization: {e}")
        import traceback

        traceback.print_exc()
        return None


def test_sequence_data_conversion():
    """Test the conversion from SequenceRecord to SequenceData."""
    print("\n🔍 Testing SequenceRecord to SequenceData conversion...")

    try:
        # Import after path setup
        from presentation.tabs.browse.services.modern_dictionary_data_manager import (
            ModernDictionaryDataManager,
        )

        # Create manager and load data
        tka_root = Path(__file__).parent
        data_dir = tka_root / "data"
        manager = ModernDictionaryDataManager(data_dir)
        manager.load_all_sequences()

        # Get first record
        records = manager.get_all_records()
        if not records:
            print("❌ No records found for conversion test")
            return None

        record = records[0]
        print(f"📊 Testing conversion of record: {record.word}")
        print(f"📊 Record thumbnails: {len(record.thumbnails)}")

        # Test conversion (from ModernBrowseTab._convert_records_to_sequence_data)
        from domain.models.sequence_data import SequenceData

        sequence_data = SequenceData(
            word=record.word,
            thumbnails=record.thumbnails,
            author=record.author,
            level=record.level,
            sequence_length=record.sequence_length,
            date_added=record.date_added,
            grid_mode=record.grid_mode,
            prop_type=record.prop_type,
            is_favorite=record.is_favorite,
            is_circular=record.is_circular,
            starting_position=record.starting_position,
            difficulty_level=record.difficulty_level,
            tags=record.tags,
        )

        print(f"✅ Converted to SequenceData: {sequence_data.word}")
        print(f"✅ SequenceData thumbnails: {len(sequence_data.thumbnails)}")

        return sequence_data

    except Exception as e:
        print(f"❌ Error testing sequence data conversion: {e}")
        import traceback

        traceback.print_exc()
        return None


if __name__ == "__main__":
    print("🚀 Starting Dictionary Loading Debug Test")
    print("=" * 50)

    # Test 1: Path resolution
    dictionary_dir = test_dictionary_path_resolution()

    # Test 2: ModernDictionaryDataManager
    if dictionary_dir and dictionary_dir.exists():
        manager = test_modern_dictionary_manager()

        # Test 3: Filtering
        if manager:
            test_filtering()

            # Test 4: Browse tab initialization
            browse_tab = test_browse_tab_initialization()

            # Test 5: Sequence data conversion
            test_sequence_data_conversion()

    print("\n" + "=" * 50)
    print("🏁 Dictionary Loading Debug Test Complete")
