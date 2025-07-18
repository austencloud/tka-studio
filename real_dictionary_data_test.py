"""
Real Dictionary Data Integration Test

This test verifies that the modern browse tab can successfully load and display
real dictionary data from F:\\CODE\\TKA\\data\\dictionary.
"""

import os
import sys
from pathlib import Path

# Add the src directory to the path
src_path = Path(__file__).parent / "src" / "desktop" / "modern" / "src"
sys.path.insert(0, str(src_path))

from presentation.tabs.browse.modern_browse_tab import ModernBrowseTab
from presentation.tabs.browse.services.modern_dictionary_data_manager import (
    ModernDictionaryDataManager,
)
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget


class RealDataTestWindow(QMainWindow):
    """Test window for real dictionary data loading."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔬 Real Dictionary Data Test - TKA Browse Tab")
        self.setGeometry(100, 100, 1400, 900)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add title
        title = QLabel("🔬 Real Dictionary Data Integration Test")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)

        # Add status label
        self.status_label = QLabel("🔄 Initializing dictionary data manager...")
        layout.addWidget(self.status_label)

        # Test the dictionary manager directly first
        self.test_dictionary_manager()

        # Create browse tab with real data
        try:
            # Use dummy paths for sequences_dir and settings_file since we're using dictionary manager
            sequences_dir = Path("F:/CODE/TKA/data/dictionary")
            settings_file = Path("F:/CODE/TKA/settings.json")

            self.browse_tab = ModernBrowseTab(sequences_dir, settings_file)
            layout.addWidget(self.browse_tab)

            # Connect to data loading signals
            self.browse_tab.dictionary_manager.data_loaded.connect(self.on_data_loaded)
            self.browse_tab.dictionary_manager.loading_progress.connect(
                self.on_loading_progress
            )

            self.status_label.setText(
                "✅ Browse tab initialized with real dictionary data"
            )

        except Exception as e:
            self.status_label.setText(f"❌ Error initializing browse tab: {e}")
            import traceback

            traceback.print_exc()

    def test_dictionary_manager(self):
        """Test the dictionary manager directly."""
        print("\n" + "=" * 60)
        print("🔬 TESTING DICTIONARY MANAGER")
        print("=" * 60)

        try:
            # Create dictionary manager
            manager = ModernDictionaryDataManager()

            # Test data directory detection
            print(f"📂 Dictionary directory: {manager.dictionary_dir}")
            print(f"📁 Directory exists: {manager.dictionary_dir.exists()}")

            if manager.dictionary_dir.exists():
                # List some directories to verify
                dirs = list(manager.dictionary_dir.iterdir())[:10]
                print(f"📋 Sample directories: {[d.name for d in dirs if d.is_dir()]}")

            # Load sequences
            print("\n🔄 Loading sequences...")
            manager.load_all_sequences()

            # Get results
            all_records = manager.get_all_records()
            print(f"✅ Loaded {len(all_records)} sequence records")

            # Test distinct values
            authors = manager.get_distinct_authors()
            levels = manager.get_distinct_levels()
            lengths = manager.get_distinct_lengths()

            print(f"👥 Distinct authors: {len(authors)} - {authors[:5]}...")
            print(f"🎚️  Distinct levels: {levels}")
            print(f"📏 Distinct lengths: {lengths}")

            # Test filtering
            if authors:
                author_records = manager.get_records_by_author(authors[0])
                print(f"🔍 Records by author '{authors[0]}': {len(author_records)}")

            if levels:
                level_records = manager.get_records_by_level(levels[0])
                print(f"🔍 Records by level {levels[0]}: {len(level_records)}")

            # Test sample sequence
            if all_records:
                sample = all_records[0]
                print(f"\n📄 Sample sequence: {sample.word}")
                print(f"   - Author: {sample.author}")
                print(f"   - Level: {sample.level}")
                print(f"   - Length: {sample.sequence_length}")
                print(f"   - Thumbnails: {len(sample.thumbnails)}")
                print(f"   - Difficulty: {sample.difficulty_level}")

                # Show thumbnail paths
                if sample.thumbnails:
                    print(f"   - First thumbnail: {sample.thumbnails[0]}")

            # Test errors
            errors = manager.get_loading_errors()
            if errors:
                print(f"\n⚠️  Loading errors: {len(errors)}")
                for error in errors[:3]:
                    print(f"   - {error}")

            self.status_label.setText(
                f"✅ Dictionary manager loaded {len(all_records)} sequences"
            )

        except Exception as e:
            print(f"❌ Dictionary manager test failed: {e}")
            import traceback

            traceback.print_exc()
            self.status_label.setText(f"❌ Dictionary manager test failed: {e}")

    def on_data_loaded(self, count: int):
        """Handle data loading completion."""
        print(f"📊 Data loaded signal received: {count} sequences")
        self.status_label.setText(
            f"✅ Successfully loaded {count} sequences from dictionary"
        )

    def on_loading_progress(self, message: str, current: int, total: int):
        """Handle loading progress updates."""
        progress = int((current / total) * 100) if total > 0 else 0
        print(f"📈 Loading progress: {message} - {progress}%")
        self.status_label.setText(f"🔄 {message} - {progress}%")


def main():
    """Run the real dictionary data test."""
    print("🚀 Starting Real Dictionary Data Integration Test")
    print("=" * 60)

    app = QApplication(sys.argv)

    # Create and show test window
    window = RealDataTestWindow()
    window.show()

    print("\n✅ Test window displayed - check GUI for results")
    print("📋 This test verifies:")
    print("   - Dictionary data manager can find and load real sequences")
    print("   - Modern browse tab integrates with real data")
    print("   - Filter options are populated from actual dictionary data")
    print("   - Error handling works correctly")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
