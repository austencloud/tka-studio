"""
Interactive Browse Tab Test

This test opens the browse tab and lets you interact with it manually
to test the organized filter hub functionality.
"""

import sys
import time
from pathlib import Path

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget

# Add the src directory to Python path for imports
modern_src = Path(__file__).parent / "src" / "desktop" / "modern" / "src"
sys.path.insert(0, str(modern_src))

from presentation.tabs.browse.models import FilterType
from presentation.tabs.browse.modern_browse_tab import ModernBrowseTab


class InteractiveBrowseTabTest(QMainWindow):
    """Interactive test window for the browse tab."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("TKA Browse Tab - Interactive Test")
        self.setGeometry(100, 100, 1400, 900)

        # Apply dark theme
        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #1a1a1a;
                color: #ffffff;
            }
            QWidget {
                background-color: #1a1a1a;
                color: #ffffff;
            }
        """
        )

        # Create central widget with layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Add instruction label
        instructions = QLabel(
            """
🎯 Interactive Browse Tab Test
================================================================================
✅ Test the organized filter hub:

1. 📝 Check the header shows "TKA Sequence Library"
2. ⭐ Click "My Favorites" (gold button)
3. 🔥 Click "Recently Added" (red button)  
4. 📊 Click "All Sequences" (teal button)
5. 📂 Try category sections:
   - By Sequence Name (A-D, E-H, etc.)
   - By Length (3, 4, 5, etc.)
   - By Difficulty (Beginner, Intermediate, Advanced)
   - By Start Position (Alpha, Beta, Gamma, Delta)
   - By Author (Demo Author, Test User, etc.)
   - By Grid Style (Diamond, Box)
6. 🔄 Check navigation between filter and results
7. 📱 Try resizing the window
8. 🖱️ Check hover effects on buttons

Watch the console for debug output!
================================================================================
        """
        )
        instructions.setStyleSheet(
            """
            QLabel {
                color: #ffffff;
                background: rgba(0, 0, 0, 0.3);
                padding: 10px;
                border-radius: 8px;
                font-family: 'Consolas', monospace;
                font-size: 10px;
            }
        """
        )
        layout.addWidget(instructions)

        # Create browse tab
        try:
            sequences_dir = Path("test_sequences")
            settings_file = Path("test_settings.json")

            self.browse_tab = ModernBrowseTab(sequences_dir, settings_file)
            layout.addWidget(self.browse_tab)

            # Connect signals for monitoring
            self.browse_tab.sequence_selected.connect(self._on_sequence_selected)
            self.browse_tab.open_in_construct.connect(self._on_open_in_construct)

            # Connect filter selection signal
            filter_panel = self.browse_tab.filter_selection_panel
            filter_panel.filter_selected.connect(self._on_filter_selected)

            print("✅ Browse tab created successfully!")
            print("🎯 Ready for interactive testing!")

        except Exception as e:
            print(f"❌ Failed to create browse tab: {e}")
            import traceback

            traceback.print_exc()

    def _on_sequence_selected(self, sequence_id: str):
        """Handle sequence selection."""
        print(f"🎯 Sequence selected: {sequence_id}")

    def _on_open_in_construct(self, sequence_id: str):
        """Handle open in construct."""
        print(f"🔧 Open in construct: {sequence_id}")

    def _on_filter_selected(self, filter_type: FilterType, filter_value):
        """Handle filter selection."""
        print(
            f"🔍 [FILTER PANEL] Filter selected: {filter_type.value} = {filter_value}"
        )


def main():
    """Run the interactive test."""
    app = QApplication(sys.argv)

    print("🚀 Starting Interactive Browse Tab Test...")
    print("=" * 60)

    window = InteractiveBrowseTabTest()
    window.show()

    print("💡 Instructions:")
    print("  - Test all the buttons and features")
    print("  - Watch console output for debug info")
    print("  - Check visual design and responsiveness")
    print("  - Press Ctrl+C to exit")
    print("=" * 60)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
