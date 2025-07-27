#!/usr/bin/env python3
"""
Test Progressive Loading Finalization

This test specifically checks if the progressive loading properly finalizes
with headers and sections after all chunks are loaded.
"""

import sys
import time
from pathlib import Path

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.presentation.tabs.browse.browse_tab import BrowseTab
from desktop.modern.presentation.tabs.browse.models import FilterType


def test_progressive_finalization():
    """Test that progressive loading properly finalizes with headers."""
    app = QApplication(sys.argv)

    # Setup paths
    sequences_dir = Path("data/sequences")
    settings_file = Path("settings.json")

    # Create DI container
    container = DIContainer()

    print("Creating browse tab...")
    browse_tab = BrowseTab(sequences_dir, settings_file, container)
    browse_tab.show()

    print("Browse tab created and shown")

    # Wait for initialization
    time.sleep(1)

    # Get browser panel
    browser_panel = browse_tab.internal_left_stack.widget(1)

    print("\n=== TESTING PROGRESSIVE LOADING FINALIZATION ===")

    # Trigger filter to start progressive loading
    filter_panel = browse_tab.internal_left_stack.widget(0)
    filter_panel.filter_selected.emit("all_sequences", None)

    print("Progressive loading started...")

    # Wait for progressive loading to complete (longer wait)
    def check_finalization():
        print(f"\n=== CHECKING FINALIZATION STATUS ===")

        # Check if loading is complete
        if hasattr(browser_panel, "progressive_loading_service"):
            is_loading = browser_panel.progressive_loading_service.is_loading()
            print(f"Is still loading: {is_loading}")

        # Check grid layout
        if hasattr(browser_panel, "ui_setup") and browser_panel.ui_setup:
            grid_layout = browser_panel.ui_setup.grid_layout
            if grid_layout:
                item_count = grid_layout.count()
                row_count = grid_layout.rowCount()
                print(f"Grid layout item count: {item_count}")
                print(f"Grid layout row count: {row_count}")

                # Check for headers (QLabel widgets)
                header_count = 0
                thumbnail_count = 0
                for i in range(item_count):
                    item = grid_layout.itemAt(i)
                    if item and item.widget():
                        widget = item.widget()
                        widget_type = type(widget).__name__
                        if "Label" in widget_type:
                            header_count += 1
                            print(
                                f"Found header {header_count}: {widget.text() if hasattr(widget, 'text') else 'No text'}"
                            )
                        elif "Frame" in widget_type:
                            thumbnail_count += 1

                print(f"Headers found: {header_count}")
                print(f"Thumbnails found: {thumbnail_count}")

                if header_count > 0:
                    print("✅ SUCCESS: Headers found - finalization worked!")
                else:
                    print(
                        "❌ ISSUE: No headers found - finalization may not have happened"
                    )
            else:
                print("❌ No grid layout found")

        app.quit()

    # Wait 10 seconds for progressive loading to complete
    QTimer.singleShot(10000, check_finalization)

    # Run the application
    app.exec()


if __name__ == "__main__":
    test_progressive_finalization()
