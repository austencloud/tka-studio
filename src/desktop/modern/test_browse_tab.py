"""
Test the Modern Browse Tab Implementation

Simple test to verify the organized filter hub works correctly.
"""

import sys
from pathlib import Path

# Add the src directory to Python path for imports
modern_src = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src))

from PyQt6.QtWidgets import QApplication, QMainWindow
from presentation.tabs.browse.modern_browse_tab import ModernBrowseTab


class TestWindow(QMainWindow):
    """Simple test window for the modern browse tab."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TKA Modern Browse Tab Test")
        self.setGeometry(100, 100, 1200, 800)

        # Create browse tab with test data
        sequences_dir = Path("test_sequences")  # Dummy path
        settings_file = Path("test_settings.json")

        self.browse_tab = ModernBrowseTab(sequences_dir, settings_file)
        self.setCentralWidget(self.browse_tab)

        # Connect signals for testing
        self.browse_tab.sequence_selected.connect(self.on_sequence_selected)
        self.browse_tab.open_in_construct.connect(self.on_open_in_construct)

    def on_sequence_selected(self, sequence_id: str):
        """Handle sequence selection."""
        print(f"🎯 Sequence selected: {sequence_id}")

    def on_open_in_construct(self, sequence_id: str):
        """Handle open in construct."""
        print(f"🔧 Open in construct: {sequence_id}")


def main():
    """Run the test application."""
    app = QApplication(sys.argv)

    # Set dark theme for better visibility
    app.setStyleSheet("""
        QMainWindow {
            background-color: #2b2b2b;
            color: white;
        }
    """)

    window = TestWindow()
    window.show()

    print("🚀 TKA Modern Browse Tab Test Running...")
    print("📊 Features to test:")
    print("   - Quick Access buttons (Favorites, Recent, All)")
    print("   - Organized category sections")
    print("   - Filter functionality")
    print("   - Responsive layout")
    print("   - Navigation between filter and results")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
