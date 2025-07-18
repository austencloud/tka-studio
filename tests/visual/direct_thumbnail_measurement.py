"""
Direct Thumbnail Measurement Tool

This tool directly measures the actual QWidget components in the running TKA app
to analyze thumbnail heights and ensure they match their image content.
"""

import sys
import os
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

# Add TKA paths
tka_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(tka_root))
sys.path.insert(0, str(tka_root / "src"))
sys.path.insert(0, str(tka_root / "launcher"))


@dataclass
class ThumbnailMeasurement:
    """Measurement data for a single thumbnail."""
    index: int
    container_width: int
    container_height: int
    image_width: int
    image_height: int
    word_label_height: int
    info_label_height: int
    total_content_height: int
    is_clipped: bool
    aspect_ratio: float
    sequence_word: str
    sequence_length: int


class DirectThumbnailMeasurer:
    """Directly measure thumbnail components in the running app."""
    
    def __init__(self):
        self.tka_root = Path(__file__).parent.parent.parent
        self.results_dir = Path(__file__).parent / "measurement_results"
        self.results_dir.mkdir(exist_ok=True)
        self.measurements = []
        
    def find_browse_panel(self) -> Optional[object]:
        """Find the running browse panel widget."""
        try:
            from PyQt6.QtWidgets import QApplication
            
            app = QApplication.instance()
            if not app:
                print("❌ No QApplication instance found. Is TKA running?")
                return None
                
            # Find all widgets
            all_widgets = app.allWidgets()
            
            # Look for SequenceBrowserPanel
            for widget in all_widgets:
                if widget.__class__.__name__ == "SequenceBrowserPanel":
                    print(f"✅ Found SequenceBrowserPanel: {widget}")
                    return widget
                    
            print("❌ No SequenceBrowserPanel found")
            return None
            
        except Exception as e:
            print(f"❌ Error finding browse panel: {e}")
            return None
    
    def measure_thumbnails(self, browse_panel) -> List[ThumbnailMeasurement]:
        """Measure all thumbnails in the browse panel."""
        measurements = []
        
        try:
            # Get the thumbnail widgets
            if not hasattr(browse_panel, 'thumbnail_widgets'):
                print("❌ Browse panel has no thumbnail_widgets attribute")
                return measurements
                
            thumbnails = browse_panel.thumbnail_widgets
            print(f"📏 Found {len(thumbnails)} thumbnails to measure")
            
            for i, thumbnail in enumerate(thumbnails):
                measurement = self._measure_single_thumbnail(thumbnail, i)
                if measurement:
                    measurements.append(measurement)
                    
        except Exception as e:
            print(f"❌ Error measuring thumbnails: {e}")
            
        return measurements
    
    def _measure_single_thumbnail(self, thumbnail, index: int) -> Optional[ThumbnailMeasurement]:
        """Measure a single thumbnail widget."""
        try:
            from PyQt6.QtWidgets import QLabel, QVBoxLayout
            
            # Get container dimensions
            container_width = thumbnail.width()
            container_height = thumbnail.height()
            
            # Get the layout
            layout = thumbnail.layout()
            if not isinstance(layout, QVBoxLayout):
                print(f"⚠️ Thumbnail {index} has unexpected layout type")
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
                        # Determine what type of label this is
                        style = widget.styleSheet()
                        text = widget.text()
                        
                        if "background: rgba(0, 0, 0, 0.2)" in style:
                            # This is the image label
                            image_label = widget
                        elif "color: white" in style:
                            # This is the word label
                            word_label = widget
                        elif "color: rgba(255, 255, 255, 0.6)" in style:
                            # This is the info label
                            info_label = widget
            
            # Measure components
            word_height = word_label.height() if word_label else 0
            info_height = info_label.height() if info_label else 0
            
            image_width = 0
            image_height = 0
            aspect_ratio = 0.0
            
            if image_label:
                image_width = image_label.width()
                image_height = image_label.height()
                if image_height > 0:
                    aspect_ratio = image_width / image_height
            
            # Calculate total content height
            spacing = layout.spacing()
            margins = layout.contentsMargins()
            total_content_height = (
                word_height + 
                image_height + 
                info_height + 
                (spacing * 2) +  # 2 spaces between 3 components
                margins.top() + 
                margins.bottom()
            )
            
            # Check if content is clipped
            is_clipped = total_content_height > container_height
            
            # Get sequence info
            sequence_word = word_label.text() if word_label else "Unknown"
            sequence_length = 0
            if info_label:
                info_text = info_label.text()
                if "Length:" in info_text:
                    try:
                        length_part = info_text.split("Length:")[1].split("\n")[0].strip()
                        sequence_length = int(length_part)
                    except:
                        pass
            
            measurement = ThumbnailMeasurement(
                index=index,
                container_width=container_width,
                container_height=container_height,
                image_width=image_width,
                image_height=image_height,
                word_label_height=word_height,
                info_label_height=info_height,
                total_content_height=total_content_height,
                is_clipped=is_clipped,
                aspect_ratio=aspect_ratio,
                sequence_word=sequence_word,
                sequence_length=sequence_length
            )
            
            return measurement
            
        except Exception as e:
            print(f"❌ Error measuring thumbnail {index}: {e}")
            return None
    
    def analyze_measurements(self, measurements: List[ThumbnailMeasurement]) -> Dict:
        """Analyze the measurements and create a report."""
        if not measurements:
            return {"error": "No measurements to analyze"}
            
        analysis = {
            "total_thumbnails": len(measurements),
            "clipped_thumbnails": sum(1 for m in measurements if m.is_clipped),
            "measurements": [asdict(m) for m in measurements]
        }
        
        # Calculate statistics
        container_heights = [m.container_height for m in measurements]
        image_heights = [m.image_height for m in measurements]
        content_heights = [m.total_content_height for m in measurements]
        
        analysis["statistics"] = {
            "container_height": {
                "min": min(container_heights),
                "max": max(container_heights),
                "avg": sum(container_heights) / len(container_heights),
                "variation": max(container_heights) - min(container_heights)
            },
            "image_height": {
                "min": min(image_heights),
                "max": max(image_heights),
                "avg": sum(image_heights) / len(image_heights),
                "variation": max(image_heights) - min(image_heights)
            },
            "content_height": {
                "min": min(content_heights),
                "max": max(content_heights),
                "avg": sum(content_heights) / len(content_heights),
                "variation": max(content_heights) - min(content_heights)
            }
        }
        
        # Issues analysis
        issues = []
        clipped_count = analysis["clipped_thumbnails"]
        if clipped_count > 0:
            issues.append(f"{clipped_count} thumbnails have clipped content")
            
        if analysis["statistics"]["container_height"]["variation"] > 50:
            issues.append("High variation in container heights")
            
        if analysis["statistics"]["image_height"]["variation"] > 30:
            issues.append("High variation in image heights")
            
        analysis["issues"] = issues
        
        return analysis
    
    def create_report(self, analysis: Dict) -> str:
        """Create a detailed measurement report."""
        if "error" in analysis:
            return f"❌ {analysis['error']}"
            
        report = []
        report.append("📏 DIRECT THUMBNAIL MEASUREMENT REPORT")
        report.append("=" * 60)
        
        # Summary
        total = analysis["total_thumbnails"]
        clipped = analysis["clipped_thumbnails"]
        report.append(f"Total thumbnails: {total}")
        report.append(f"Clipped thumbnails: {clipped} ({clipped/total*100:.1f}%)")
        
        # Statistics
        stats = analysis["statistics"]
        report.append(f"\n📊 HEIGHT STATISTICS:")
        report.append(f"Container heights: {stats['container_height']['min']}-{stats['container_height']['max']}px (avg: {stats['container_height']['avg']:.1f})")
        report.append(f"Image heights: {stats['image_height']['min']}-{stats['image_height']['max']}px (avg: {stats['image_height']['avg']:.1f})")
        report.append(f"Content heights: {stats['content_height']['min']}-{stats['content_height']['max']}px (avg: {stats['content_height']['avg']:.1f})")
        
        # Issues
        if analysis["issues"]:
            report.append(f"\n⚠️ ISSUES FOUND:")
            for issue in analysis["issues"]:
                report.append(f"  • {issue}")
        else:
            report.append(f"\n✅ No issues found")
            
        # Individual measurements
        report.append(f"\n📋 INDIVIDUAL MEASUREMENTS:")
        for m in analysis["measurements"]:
            status = "❌ CLIPPED" if m["is_clipped"] else "✅ OK"
            report.append(f"  {m['index']:2d}: {m['sequence_word'][:15]:15} | "
                         f"Container: {m['container_width']}x{m['container_height']} | "
                         f"Image: {m['image_width']}x{m['image_height']} | "
                         f"Content: {m['total_content_height']} | {status}")
        
        return "\n".join(report)
    
    def run_measurement(self) -> bool:
        """Run the complete measurement process."""
        print("📏 TKA Direct Thumbnail Measurement")
        print("=" * 50)
        
        # Find the browse panel
        browse_panel = self.find_browse_panel()
        if not browse_panel:
            print("❌ Could not find browse panel. Make sure TKA is running with browse tab open.")
            return False
            
        # Measure thumbnails
        print("📏 Measuring thumbnails...")
        measurements = self.measure_thumbnails(browse_panel)
        
        if not measurements:
            print("❌ No measurements obtained")
            return False
            
        # Analyze measurements
        print("🔍 Analyzing measurements...")
        analysis = self.analyze_measurements(measurements)
        
        # Create report
        report = self.create_report(analysis)
        print(f"\n{report}")
        
        # Save results
        timestamp = int(time.time())
        
        # Save raw data
        data_path = self.results_dir / f"measurements_{timestamp}.json"
        with open(data_path, 'w') as f:
            json.dump(analysis, f, indent=2)
        print(f"💾 Data saved: {data_path}")
        
        # Save report
        report_path = self.results_dir / f"report_{timestamp}.txt"
        with open(report_path, 'w') as f:
            f.write(report)
        print(f"📄 Report saved: {report_path}")
        
        return True


def main():
    """Main function."""
    print("🔧 Direct Thumbnail Measurement Tool")
    print("Make sure TKA app is running with browse tab open and sequences loaded!")
    
    input("Press Enter when ready...")
    
    measurer = DirectThumbnailMeasurer()
    
    success = measurer.run_measurement()
    
    if success:
        print("\n✅ Measurement completed successfully!")
        print(f"📁 Results saved in: {measurer.results_dir}")
    else:
        print("\n❌ Measurement failed")


if __name__ == "__main__":
    main()
