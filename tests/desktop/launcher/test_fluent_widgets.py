#!/usr/bin/env python3
"""
Test script to understand PyQt-Fluent-Widgets architecture and capabilities.
This will help us understand the component structure before implementing the launcher.
"""

import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget
from qfluentwidgets import (
    BodyLabel,
    CaptionLabel,
    CardWidget,
    FlowLayout,
    FluentIcon,
    MSFluentWindow,
    NavigationItemPosition,
    PrimaryPushButton,
    PushButton,
    ScrollArea,
    SearchLineEdit,
    Theme,
    TitleLabel,
    TransparentPushButton,
    setTheme,
)


class FluentTestWindow(MSFluentWindow):
    """Test window to explore PyQt-Fluent-Widgets components."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt-Fluent-Widgets Architecture Test")
        self.resize(1000, 700)

        # Set theme
        setTheme(Theme.DARK)

        # Create main interface
        self._create_main_interface()

        # Setup navigation
        self._setup_navigation()

    def _create_main_interface(self):
        """Create the main interface components."""
        # Create main widget
        main_widget = QWidget()
        main_widget.setObjectName("HomeInterface")  # Required for FluentWindow
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Title section
        title_layout = QHBoxLayout()
        title = TitleLabel("TKA Launcher Architecture Test")
        subtitle = CaptionLabel("Exploring PyQt-Fluent-Widgets components")

        title_layout.addWidget(title)
        title_layout.addStretch()
        main_layout.addLayout(title_layout)
        main_layout.addWidget(subtitle)

        # Search section
        search_layout = QHBoxLayout()
        search_label = BodyLabel("Search Applications:")
        self.search_box = SearchLineEdit()
        self.search_box.setPlaceholderText("Type to search applications...")
        self.search_box.setFixedWidth(400)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_box)
        search_layout.addStretch()
        main_layout.addLayout(search_layout)

        # Application cards section
        cards_label = BodyLabel("Available Applications:")
        main_layout.addWidget(cards_label)

        # Scroll area for cards
        scroll_area = ScrollArea()
        scroll_widget = QWidget()
        self.cards_layout = FlowLayout(scroll_widget)

        # Create sample application cards
        self._create_sample_cards()

        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        # Action buttons
        button_layout = QHBoxLayout()

        self.launch_btn = PrimaryPushButton("Launch Selected")
        self.settings_btn = TransparentPushButton("Settings")
        self.refresh_btn = PushButton("Refresh")

        button_layout.addWidget(self.launch_btn)
        button_layout.addWidget(self.settings_btn)
        button_layout.addWidget(self.refresh_btn)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        # Add as main interface to the fluent window
        self.addSubInterface(main_widget, FluentIcon.HOME, "Home")

    def _create_sample_cards(self):
        """Create sample application cards to test the layout."""
        apps = [
            {
                "title": "TKA Desktop (Modern)",
                "desc": "Modern TKA application",
                "icon": "✨",
            },
            {
                "title": "TKA Desktop (Legacy)",
                "desc": "Legacy TKA application",
                "icon": "🏛️",
            },
            {"title": "Web Application", "desc": "TKA web interface", "icon": "🌐"},
            {"title": "Development Tools", "desc": "Developer utilities", "icon": "🔧"},
            {"title": "Settings", "desc": "Application settings", "icon": "⚙️"},
            {"title": "Documentation", "desc": "User documentation", "icon": "📚"},
        ]

        for app in apps:
            card = self._create_app_card(app["title"], app["desc"], app["icon"])
            self.cards_layout.addWidget(card)

    def _create_app_card(self, title: str, description: str, icon: str) -> CardWidget:
        """Create an application card widget."""
        card = CardWidget()
        card.setFixedSize(250, 120)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)

        # Header with icon and title
        header_layout = QHBoxLayout()
        icon_label = TitleLabel(icon)
        title_label = BodyLabel(title)
        title_label.setWordWrap(True)

        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Description
        desc_label = CaptionLabel(description)
        desc_label.setWordWrap(True)

        layout.addLayout(header_layout)
        layout.addWidget(desc_label)
        layout.addStretch()

        # Make card clickable
        card.setObjectName("app_card")
        card.clicked.connect(lambda: self._on_card_clicked(title))

        return card

    def _on_card_clicked(self, app_title: str):
        """Handle card click events."""
        print(f"Card clicked: {app_title}")

    def _setup_navigation(self):
        """Setup navigation panel (if needed)."""
        # Create settings widget
        settings_widget = QWidget()
        settings_widget.setObjectName("SettingsInterface")

        # Add navigation items
        self.addSubInterface(
            settings_widget,
            FluentIcon.SETTING,
            "Settings",
            NavigationItemPosition.BOTTOM,
        )


def test_fluent_widgets():
    """Test PyQt-Fluent-Widgets components and architecture."""
    print("🧪 Testing PyQt-Fluent-Widgets architecture...")

    app = QApplication(sys.argv)

    # Create test window
    window = FluentTestWindow()
    window.show()

    print("✅ Fluent widgets test window created successfully")
    print("📋 Components tested:")
    print("  - FluentWindow (main window)")
    print("  - SearchLineEdit (search functionality)")
    print("  - CardWidget (application cards)")
    print("  - Various labels and buttons")
    print("  - FlowLayout (responsive card layout)")
    print("  - ScrollArea (scrollable content)")

    # Don't run the event loop in test mode
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Test mode - just validate imports and creation
        success = test_fluent_widgets()
        sys.exit(0 if success else 1)
    else:
        # Interactive mode - run the application
        app = QApplication(sys.argv)
        window = FluentTestWindow()
        window.show()
        sys.exit(app.exec_())
