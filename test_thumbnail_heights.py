"""
End-to-End Thumbnail Height Test

Tests that thumbnail containers properly expand to accommodate their content
by launching the app, opening the browse tab, and measuring component heights.
"""

import sys
import os
import time
from pathlib import Path
from typing import Dict, List, Optional

# Add TKA paths
tka_root = Path(__file__).parent
sys.path.insert(0, str(tka_root))
sys.path.insert(0, str(tka_root / "src"))
sys.path.insert(0, str(tka_root / "launcher"))


def test_thumbnail_heights():
    """Test that thumbnails expand properly to show all content."""
    print("🧪 Testing Thumbnail Heights")
    print("=" * 50)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import QTimer
        from PyQt6.QtGui import QGuiApplication
        
        # Create application
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
            app.setStyle("Fusion")
        
        # Import and initialize TKA
        from src.desktop.modern.src.core.application.application_factory import ApplicationFactory, ApplicationMode
        from src.desktop.modern.src.core.service_locator import initialize_services
        
        # Create container
        print("🏗️ Creating application container...")
        container = ApplicationFactory.create_app(ApplicationMode.TEST)
        
        # Initialize services
        print("🔧 Initializing services...")
        initialize_services()
        
        # Create main window
        print("🚀 Creating main window...")
        from src.desktop.modern.main import TKAMainWindow
        main_window = TKAMainWindow(container=container)
        main_window.show()
        
        # Wait for app to initialize
        print("⏳ Waiting for application to initialize...")
        app.processEvents()
        time.sleep(3)
        
        # Find the browse tab widget
        print("� Finding browse tab...")
        browse_tab = None
        
        # Look for tab widget first
        for widget in app.allWidgets():
            if hasattr(widget, 'widget') and hasattr(widget, 'count'):
                # This might be a tab widget
                for i in range(widget.count()):
                    tab_text = widget.tabText(i) if hasattr(widget, 'tabText') else ""
                    if 'Browse' in tab_text or 'browse' in tab_text:
                        # Switch to browse tab
                        widget.setCurrentIndex(i)
                        browse_tab = widget.widget(i)
                        break
        
        if not browse_tab:
            print("⚠️ Could not find browse tab, looking for SequenceBrowserPanel directly...")
        
        # Wait for tab to load
        print("⏳ Waiting for browse tab to load...")
        app.processEvents()
        time.sleep(3)
        
        # Find the sequence browser panel
        print("🔍 Finding sequence browser panel...")
        sequence_browser = None
        
        for widget in app.allWidgets():
            if widget.__class__.__name__ == "SequenceBrowserPanel":
                sequence_browser = widget
                break
        
        if not sequence_browser:
            print("❌ Could not find SequenceBrowserPanel")
            return False
        
        print(f"✅ Found SequenceBrowserPanel: {sequence_browser}")
        
        # Wait for sequences to load
        print("⏳ Waiting for sequences to load...")
        app.processEvents()
        time.sleep(3)
        
        # Check if thumbnails exist
        if not hasattr(sequence_browser, 'thumbnail_widgets'):
            print("❌ No thumbnail_widgets attribute found")
            return False
        
        thumbnails = sequence_browser.thumbnail_widgets
        if not thumbnails:
            print("❌ No thumbnails found")
            return False
        
        print(f"📏 Found {len(thumbnails)} thumbnails to measure")
        
        # Measure each thumbnail
        results = []
        clipped_count = 0
        
        for i, thumbnail in enumerate(thumbnails):
            measurement = measure_thumbnail(thumbnail, i)
            if measurement:
                results.append(measurement)
                if measurement['is_clipped']:
                    clipped_count += 1
        
        # Report results
        print(f"\n📊 MEASUREMENT RESULTS")
        print("=" * 50)
        
        for result in results:
            status = "❌ CLIPPED" if result['is_clipped'] else "✅ OK"
            print(f"Thumbnail {result['index']:2d}: {result['sequence_word'][:15]:15} | "
                  f"Container: {result['container_height']:3d}px | "
                  f"Content: {result['content_height']:3d}px | "
                  f"Overflow: {result['overflow']:3d}px | {status}")
        
        print(f"\n📈 SUMMARY")
        print(f"Total thumbnails: {len(results)}")
        print(f"Clipped thumbnails: {clipped_count}")
        print(f"Success rate: {(len(results) - clipped_count) / len(results) * 100:.1f}%")
        
        if clipped_count == 0:
            print("✅ All thumbnails display content properly!")
            test_passed = True
        else:
            print("⚠️ Some thumbnails have clipped content")
            test_passed = False
        
        # Clean up
        main_window.close()
        app.quit()
        
        return test_passed
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


def measure_thumbnail(thumbnail, index: int) -> Optional[Dict]:
    """Measure a single thumbnail's dimensions and content."""
    try:
        from PyQt6.QtWidgets import QLabel, QVBoxLayout
        
        # Get container dimensions
        container_width = thumbnail.width()
        container_height = thumbnail.height()
        
        # Get layout
        layout = thumbnail.layout()
        if not isinstance(layout, QVBoxLayout):
            return None
        
        # Find components
        word_label = None
        image_label = None
        info_label = None
        
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, QLabel):
                    style = widget.styleSheet()
                    
                    if "background: rgba(0, 0, 0, 0.2)" in style:
                        image_label = widget
                    elif "color: white" in style:
                        word_label = widget
                    elif "color: rgba(255, 255, 255, 0.6)" in style:
                        info_label = widget
        
        # Calculate content height
        word_height = word_label.height() if word_label else 0
        image_height = image_label.height() if image_label else 0
        info_height = info_label.height() if info_label else 0
        
        # Add layout spacing and margins
        spacing = layout.spacing() * (layout.count() - 1)
        margins = layout.contentsMargins()
        total_content_height = (
            word_height + image_height + info_height + 
            spacing + margins.top() + margins.bottom()
        )
        
        # Calculate overflow
        overflow = max(0, total_content_height - container_height)
        is_clipped = overflow > 0
        
        # Get sequence word
        sequence_word = word_label.text() if word_label else "Unknown"
        
        return {
            'index': index,
            'sequence_word': sequence_word,
            'container_width': container_width,
            'container_height': container_height,
            'word_height': word_height,
            'image_height': image_height,
            'info_height': info_height,
            'content_height': total_content_height,
            'overflow': overflow,
            'is_clipped': is_clipped
        }
        
    except Exception as e:
        print(f"❌ Error measuring thumbnail {index}: {e}")
        return None


if __name__ == "__main__":
    success = test_thumbnail_heights()
    
    if success:
        print("\n🎉 Test PASSED - All thumbnails display properly!")
        sys.exit(0)
    else:
        print("\n💥 Test FAILED - Some thumbnails are clipped!")
        sys.exit(1)
