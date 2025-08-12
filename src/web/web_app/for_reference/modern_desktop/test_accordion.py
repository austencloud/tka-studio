"""
Test script for the accordion filter panel.

Run this to test the basic accordion functionality.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

# Add the project root to the path
sys.path.insert(0, "F:/CODE/TKA")

from application.services.browse.dictionary_data_manager import DictionaryDataManager
from desktop.modern.presentation.components.browse.components.accordion_filter_panel import AccordionFilterPanel


class TestWindow(QMainWindow):
    """Test window for the accordion filter panel."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Accordion Filter Panel Test")
        self.setGeometry(100, 100, 600, 800)
        
        # Create a mock dictionary manager
        self.dictionary_manager = DictionaryDataManager()
        
        # Setup UI
        self._setup_ui()
        self._apply_styling()

    def _setup_ui(self):
        """Setup the test UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Create accordion filter panel
        self.accordion_panel = AccordionFilterPanel(self.dictionary_manager)
        self.accordion_panel.filter_selected.connect(self._on_filter_selected)
        
        layout.addWidget(self.accordion_panel)

    def _apply_styling(self):
        """Apply dark theme styling for testing."""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1a1a2e, stop:1 #16213e);
            }
        """)

    def _on_filter_selected(self, filter_type, filter_value):
        """Handle filter selection for testing."""
        print(f"🎯 [TEST] Filter selected: {filter_type.value} = {filter_value}")


def main():
    """Run the test application."""
    app = QApplication(sys.argv)
    
    window = TestWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
