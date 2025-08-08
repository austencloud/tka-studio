#!/usr/bin/env python3
"""
Test the dialog sizing logic without importing the full settings dialog.
"""

import sys
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt


class TestDialog(QDialog):
    """Test dialog that mimics the settings dialog sizing logic."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Test Settings Dialog Sizing")
        self.setModal(True)
        
        # Apply the same sizing logic as the settings dialog
        self._setup_responsive_sizing()
        
        # Create simple content to test
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)
        
        # Add some content
        title = QLabel("Settings Dialog Size Test")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        layout.addWidget(title)
        
        info = QLabel("This dialog uses the same responsive sizing logic as the settings dialog.")
        info.setWordWrap(True)
        info.setStyleSheet("color: white;")
        layout.addWidget(info)
        
        # Size info
        size = self.size()
        size_info = QLabel(f"Dialog size: {size.width()}x{size.height()}")
        size_info.setStyleSheet("color: yellow; font-family: monospace;")
        layout.addWidget(size_info)
        
        # Screen info
        screen = self.screen()
        if screen:
            geometry = screen.availableGeometry()
            screen_info = QLabel(f"Screen size: {geometry.width()}x{geometry.height()}")
            screen_info.setStyleSheet("color: yellow; font-family: monospace;")
            layout.addWidget(screen_info)
            
            # Percentage info
            width_percent = (size.width() / geometry.width()) * 100
            height_percent = (size.height() / geometry.height()) * 100
            percent_info = QLabel(f"Percentage: {width_percent:.1f}% x {height_percent:.1f}%")
            percent_info.setStyleSheet("color: cyan; font-family: monospace;")
            layout.addWidget(percent_info)
        
        layout.addStretch()
        
        # Close button
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
        
        # Apply glassmorphism-like styling
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(20, 20, 30, 0.95),
                    stop:1 rgba(10, 10, 20, 0.95));
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
            }
            QPushButton {
                background: rgba(42, 130, 218, 0.8);
                border: 1px solid rgba(42, 130, 218, 1.0);
                border-radius: 8px;
                color: white;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(42, 130, 218, 1.0);
            }
        """)
        
        self.setWindowFlags(Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
    def _setup_responsive_sizing(self):
        """Apply the same responsive sizing logic as the settings dialog."""
        # Get screen geometry for responsive sizing
        screen = self.screen()
        if screen:
            screen_geometry = screen.availableGeometry()
            # Use 70% of screen width and 60% of screen height for better fit
            dialog_width = int(screen_geometry.width() * 0.70)
            dialog_height = int(screen_geometry.height() * 0.60)
            
            # Set reasonable min/max bounds
            dialog_width = max(900, min(dialog_width, 1600))  # Min 900px, max 1600px
            dialog_height = max(600, min(dialog_height, 1000))  # Min 600px, max 1000px
            
            print(f"Screen size: {screen_geometry.width()}x{screen_geometry.height()}")
            print(f"Calculated dialog size: {dialog_width}x{dialog_height}")
            print(f"Percentage: {(dialog_width/screen_geometry.width())*100:.1f}% x {(dialog_height/screen_geometry.height())*100:.1f}%")
        else:
            # Fallback if screen detection fails
            dialog_width, dialog_height = 1200, 800
            print("Screen detection failed, using fallback size")
            
        self.setFixedSize(dialog_width, dialog_height)


class TestMainWindow(QDialog):
    """Main window to launch the test dialog."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dialog Size Test Launcher")
        self.setGeometry(100, 100, 400, 200)
        
        layout = QVBoxLayout(self)
        
        info = QLabel("Click the button to test the settings dialog sizing:")
        layout.addWidget(info)
        
        test_btn = QPushButton("Open Test Dialog")
        test_btn.clicked.connect(self.open_test_dialog)
        layout.addWidget(test_btn)
        
        layout.addStretch()
        
    def open_test_dialog(self):
        """Open the test dialog."""
        dialog = TestDialog(self)
        dialog.exec()


def main():
    """Main function."""
    app = QApplication(sys.argv)
    
    # Create and show main window
    window = TestMainWindow()
    window.show()
    
    print("Test launcher opened. Click the button to test dialog sizing.")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
