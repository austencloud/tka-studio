"""
Simple Thumbnail Height Test

This test connects to a running TKA instance and measures thumbnail heights.
First run TKA manually, then run this test.
"""

import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

# Add TKA paths
tka_root = Path(__file__).parent
sys.path.insert(0, str(tka_root))
sys.path.insert(0, str(tka_root / "src"))


def test_running_app_thumbnails():
    """Test thumbnails in currently running TKA application."""
    print("🧪 Testing Thumbnail Heights in Running TKA")
    print("=" * 50)
    
    try:
        from PyQt6.QtWidgets import QApplication
        
        # Get the existing application instance
        app = QApplication.instance()
        if not app:
            print("❌ No TKA application is running!")
            print("Please start TKA first, then run this test.")
            return False
        
        print("✅ Found running TKA application")
        
        # Find the sequence browser panel
        sequence_browser = None
        for widget in app.allWidgets():
            if widget.__class__.__name__ == "SequenceBrowserPanel":
                sequence_browser = widget
                break
        
        if not sequence_browser:
            print("❌ Could not find SequenceBrowserPanel")
            print("Make sure the Browse tab is open!")
            return False
        
        print(f"✅ Found SequenceBrowserPanel")
        
        # Check if it has thumbnails
        if not hasattr(sequence_browser, 'grid_layout'):
            print("❌ SequenceBrowserPanel has no grid_layout")
            return False
        
        grid = sequence_browser.grid_layout
        thumbnail_count = 0
        
        # Count thumbnails in grid
        for i in range(grid.count()):
            item = grid.itemAt(i)
            if item and item.widget():
                thumbnail_count += 1
        
        if thumbnail_count == 0:
            print("❌ No thumbnails found in grid")
            print("Make sure sequences are loaded!")
            return False
        
        print(f"📏 Found {thumbnail_count} thumbnails to measure")
        
        # Measure each thumbnail
        results = []
        clipped_count = 0
        
        for i in range(grid.count()):
            item = grid.itemAt(i)
            if item and item.widget():
                thumbnail = item.widget()
                measurement = measure_thumbnail_simple(thumbnail, len(results))
                if measurement:
                    results.append(measurement)
                    if measurement['is_clipped']:
                        clipped_count += 1
        
        # Report results
        print(f"\n📊 MEASUREMENT RESULTS")
        print("=" * 60)
        
        for result in results:
            status = "❌ CLIPPED" if result['is_clipped'] else "✅ OK"
            print(f"Thumbnail {result['index']:2d}: Container: {result['container_height']:3d}px | "
                  f"Content: {result['content_height']:3d}px | "
                  f"Overflow: {result['overflow']:3d}px | {status}")
        
        print(f"\n📈 SUMMARY")
        print(f"Total thumbnails: {len(results)}")
        print(f"Clipped thumbnails: {clipped_count}")
        print(f"Success rate: {(len(results) - clipped_count) / len(results) * 100:.1f}%")
        
        if clipped_count == 0:
            print("✅ All thumbnails display content properly!")
            return True
        else:
            print("⚠️ Some thumbnails have clipped content")
            return False
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


def measure_thumbnail_simple(thumbnail, index: int) -> Optional[Dict]:
    """Measure a single thumbnail's dimensions."""
    try:
        from PyQt6.QtWidgets import QLabel, QVBoxLayout
        
        # Get container dimensions
        container_height = thumbnail.height()
        
        # Get layout
        layout = thumbnail.layout()
        if not isinstance(layout, QVBoxLayout):
            return None
        
        # Calculate content height by summing all child widgets
        total_content_height = 0
        
        for i in range(layout.count()):
            item = layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                total_content_height += widget.height()
        
        # Add spacing and margins
        spacing = layout.spacing() * max(0, layout.count() - 1)
        margins = layout.contentsMargins()
        total_content_height += spacing + margins.top() + margins.bottom()
        
        # Calculate overflow
        overflow = max(0, total_content_height - container_height)
        is_clipped = overflow > 0
        
        return {
            'index': index,
            'container_height': container_height,
            'content_height': total_content_height,
            'overflow': overflow,
            'is_clipped': is_clipped
        }
        
    except Exception as e:
        print(f"❌ Error measuring thumbnail {index}: {e}")
        return None


if __name__ == "__main__":
    print("🚀 Simple Thumbnail Height Test")
    print("📝 Make sure TKA is running with Browse tab open!")
    
    input("Press Enter when TKA is ready...")
    
    success = test_running_app_thumbnails()
    
    if success:
        print("\n🎉 Test PASSED - All thumbnails display properly!")
        sys.exit(0)
    else:
        print("\n💥 Test FAILED - Some thumbnails are clipped!")
        sys.exit(1)
