#!/usr/bin/env python3
"""
Simple dialog test that mimics the settings dialog sizing without any imports.
"""

import sys
from PyQt6.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QStackedWidget, QListWidget, QWidget, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont


class SimpleSettingsDialog(QDialog):
    """Simple test dialog that mimics the settings dialog sizing."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        
        # Apply responsive sizing
        self._setup_responsive_sizing()
        
        # Create UI
        self._create_ui()
        
        # Apply styling
        self._apply_styling()
        
        # Track measurements
        self.measurements = []
        self.current_tab = "General"
        
    def _setup_responsive_sizing(self):
        """Apply responsive sizing logic."""
        screen = self.screen()
        if screen:
            screen_geometry = screen.availableGeometry()
            # Use 60% width, 50% height
            dialog_width = int(screen_geometry.width() * 0.60)
            dialog_height = int(screen_geometry.height() * 0.50)
            
            # Apply bounds
            dialog_width = max(800, min(dialog_width, 1400))
            dialog_height = max(500, min(dialog_height, 800))
            
            print(f"Screen: {screen_geometry.width()}x{screen_geometry.height()}")
            print(f"Dialog: {dialog_width}x{dialog_height}")
            print(f"Percentage: {(dialog_width/screen_geometry.width())*100:.1f}% x {(dialog_height/screen_geometry.height())*100:.1f}%")
        else:
            dialog_width, dialog_height = 1000, 650
            
        # Use resize with min/max constraints
        self.resize(dialog_width, dialog_height)
        self.setMinimumSize(800, 500)
        self.setMaximumSize(1400, 800)
        
        self.measurements.append(f"Initial: {dialog_width}x{dialog_height}")
        
    def _create_ui(self):
        """Create the dialog UI."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Container
        container = QWidget()
        container.setObjectName("container")
        main_layout.addWidget(container)

        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(16, 16, 16, 16)
        container_layout.setSpacing(12)

        # Header
        header = QLabel("Settings")
        header.setStyleSheet("font-size: 18px; font-weight: bold; color: white;")
        container_layout.addWidget(header)

        # Content area
        content_layout = QHBoxLayout()
        content_layout.setSpacing(16)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(220)
        tabs = ["General", "Prop Type", "Visibility", "Image Export"]
        for tab in tabs:
            self.sidebar.addItem(tab)
        self.sidebar.setCurrentRow(0)
        self.sidebar.currentRowChanged.connect(self._on_tab_changed)
        content_layout.addWidget(self.sidebar)

        # Content area with scroll
        self.content_area = QStackedWidget()
        self.content_area.setMinimumWidth(400)
        
        # Create tabs with different content sizes to test expansion
        for i, tab_name in enumerate(tabs):
            tab_widget = self._create_tab_content(tab_name, i)
            self.content_area.addWidget(tab_widget)
            
        content_layout.addWidget(self.content_area)
        container_layout.addLayout(content_layout)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        test_btn = QPushButton("Test All Tabs")
        test_btn.clicked.connect(self._test_all_tabs)
        button_layout.addWidget(test_btn)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        container_layout.addWidget(QWidget())  # Spacer
        container_layout.addLayout(button_layout)
        
    def _create_tab_content(self, tab_name, index):
        """Create tab content with varying sizes."""
        # Create scroll area for each tab
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QScrollArea.Shape.NoFrame)
        
        # Content widget
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(8)
        
        # Add different amounts of content to test sizing
        layout.addWidget(QLabel(f"{tab_name} Settings"))
        layout.addWidget(QLabel("This tab tests dialog sizing behavior."))
        
        # Add varying content based on tab
        content_items = [5, 10, 15, 8][index]  # Different content amounts
        for i in range(content_items):
            item_label = QLabel(f"Setting item {i+1}: This is a test setting with some description text.")
            item_label.setWordWrap(True)
            layout.addWidget(item_label)
            
        layout.addStretch()
        
        scroll_area.setWidget(content_widget)
        return scroll_area
        
    def _on_tab_changed(self, index):
        """Handle tab changes."""
        tabs = ["General", "Prop Type", "Visibility", "Image Export"]
        if 0 <= index < len(tabs):
            self.current_tab = tabs[index]
            self.content_area.setCurrentIndex(index)
            
            # Measure after tab change
            QTimer.singleShot(100, self._measure_after_tab_change)
            
    def _measure_after_tab_change(self):
        """Measure size after tab change."""
        size = self.size()
        measurement = f"{self.current_tab}: {size.width()}x{size.height()}"
        self.measurements.append(measurement)
        print(f"Tab changed to {measurement}")
        
    def _test_all_tabs(self):
        """Automatically test all tabs."""
        print("\\nTesting all tabs automatically...")
        for i in range(4):
            QTimer.singleShot(i * 1000, lambda idx=i: self.sidebar.setCurrentRow(idx))
        
        # Final analysis
        QTimer.singleShot(5000, self._final_analysis)
        
    def _final_analysis(self):
        """Perform final analysis."""
        print("\\n" + "="*60)
        print("SETTINGS DIALOG SIZE ANALYSIS")
        print("="*60)
        
        size = self.size()
        screen = self.screen()
        
        if screen:
            screen_geometry = screen.availableGeometry()
            width_percent = (size.width() / screen_geometry.width()) * 100
            height_percent = (size.height() / screen_geometry.height()) * 100
            
            print(f"Screen Size: {screen_geometry.width()}x{screen_geometry.height()}")
            print(f"Dialog Size: {size.width()}x{size.height()}")
            print(f"Percentage: {width_percent:.1f}% x {height_percent:.1f}%")
            print(f"Target: 60% x 50%")
            print(f"Width Status: {'✅ GOOD' if 55 <= width_percent <= 65 else '❌ NEEDS ADJUSTMENT'}")
            print(f"Height Status: {'✅ GOOD' if 45 <= height_percent <= 55 else '❌ NEEDS ADJUSTMENT'}")
            print()
            print("Size History:")
            for measurement in self.measurements:
                print(f"  - {measurement}")
            print()
            print(f"Min Size: {self.minimumSize().width()}x{self.minimumSize().height()}")
            print(f"Max Size: {self.maximumSize().width()}x{self.maximumSize().height()}")
            print(f"Current: {size.width()}x{size.height()}")
            
            overall_good = (45 <= height_percent <= 55 and 55 <= width_percent <= 65)
            print(f"\\nOVERALL: {'✅ DIALOG SIZING IS GOOD' if overall_good else '❌ DIALOG SIZING NEEDS ADJUSTMENT'}")
        
    def _apply_styling(self):
        """Apply basic styling."""
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(20, 20, 30, 0.95),
                    stop:1 rgba(10, 10, 20, 0.95));
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 16px;
            }
            QLabel { color: white; }
            QListWidget {
                background: rgba(30, 30, 40, 0.8);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                color: white;
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


def main():
    """Main function."""
    app = QApplication(sys.argv)
    
    print("Starting simple settings dialog test...")
    
    # Create and show dialog
    dialog = SimpleSettingsDialog()
    dialog.show()
    
    # Auto-start testing after a delay
    QTimer.singleShot(1000, dialog._test_all_tabs)
    
    print("Dialog opened. Testing will start automatically in 1 second.")
    print("You can also click 'Test All Tabs' to run the test manually.")
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
