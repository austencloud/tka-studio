"""
Quick Thumbnail Test

A simple test that can be run while developing to quickly check
thumbnail measurements and identify issues.
"""

import sys
from pathlib import Path

# Add TKA paths
tka_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(tka_root))
sys.path.insert(0, str(tka_root / "src"))


def quick_thumbnail_check():
    """Quick check of thumbnail measurements."""
    try:
        from PyQt6.QtWidgets import QApplication
        
        app = QApplication.instance()
        if not app:
            print("❌ No QApplication found. TKA must be running.")
            return False
            
        # Find browse panel
        browse_panel = None
        for widget in app.allWidgets():
            if widget.__class__.__name__ == "SequenceBrowserPanel":
                browse_panel = widget
                break
                
        if not browse_panel:
            print("❌ No SequenceBrowserPanel found")
            return False
            
        # Quick check
        if not hasattr(browse_panel, 'thumbnail_widgets'):
            print("❌ No thumbnail_widgets found")
            return False
            
        thumbnails = browse_panel.thumbnail_widgets
        print(f"📏 Found {len(thumbnails)} thumbnails")
        
        clipped_count = 0
        total_count = len(thumbnails)
        
        for i, thumbnail in enumerate(thumbnails):
            container_height = thumbnail.height()
            
            # Get layout and calculate content height
            layout = thumbnail.layout()
            if layout:
                total_content = 0
                for j in range(layout.count()):
                    item = layout.itemAt(j)
                    if item and item.widget():
                        total_content += item.widget().height()
                
                # Add spacing and margins
                spacing = layout.spacing() * (layout.count() - 1)
                margins = layout.contentsMargins()
                total_content += spacing + margins.top() + margins.bottom()
                
                is_clipped = total_content > container_height
                if is_clipped:
                    clipped_count += 1
                    
                print(f"  {i:2d}: Container={container_height:3d}px, Content={total_content:3d}px {'❌' if is_clipped else '✅'}")
        
        print(f"\n📊 Summary: {clipped_count}/{total_count} thumbnails clipped ({clipped_count/total_count*100:.1f}%)")
        
        if clipped_count == 0:
            print("✅ All thumbnails display properly!")
        else:
            print("⚠️ Some thumbnails are clipped - content height exceeds container height")
            
        return clipped_count == 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Quick Thumbnail Check")
    print("=" * 30)
    quick_thumbnail_check()
