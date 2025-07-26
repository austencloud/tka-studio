"""
Debug Pictograph Colors

This test helps debug what colors are actually present in the rendered pictographs.
"""

import pytest
import tempfile
from pathlib import Path
from collections import Counter

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QImage

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.dependency_injection.image_export_service_registration import register_image_export_services
from desktop.modern.core.interfaces.image_export_services import (
    IImageExportService,
    ImageExportOptions
)


class TestDebugPictographColors:
    """Debug pictograph colors to understand what's being rendered."""
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test environment."""
        # Ensure QApplication exists
        if not QApplication.instance():
            self.app = QApplication([])
        else:
            self.app = QApplication.instance()
        
        # Create DI container and register services
        self.container = DIContainer()
        register_image_export_services(self.container)
        
        # Get services
        self.export_service = self.container.resolve(IImageExportService)
        
        # Create temporary directory
        self.temp_dir = Path(tempfile.mkdtemp())
        
        yield
        
        # Cleanup
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_debug_pictograph_colors(self):
        """Debug what colors are actually in the pictograph."""
        sequence_data = [
            {
                "beat": 1,
                "letter": "X",
                "start_pos": "alpha",
                "end_pos": "gamma",
                "blue_attributes": {"motion": "dash", "location": "alpha"},
                "red_attributes": {"motion": "static", "location": "gamma"}
            }
        ]
        
        options = ImageExportOptions(
            add_beat_numbers=True,
            include_start_position=False
        )
        
        image = self.export_service.create_sequence_image(sequence_data, "DEBUG", options)
        
        # Save for inspection
        output_path = self.temp_dir / "debug_colors.png"
        image.save(str(output_path), "PNG", 1)
        print(f"Debug image saved to: {output_path}")
        
        # Analyze all colors in the image
        color_counts = Counter()
        
        # Sample every 5th pixel to get a good representation
        for y in range(0, image.height(), 5):
            for x in range(0, image.width(), 5):
                if x < image.width() and y < image.height():
                    pixel = image.pixelColor(x, y)
                    color_name = pixel.name()
                    color_counts[color_name] += 1
        
        # Print the most common colors
        print("\n🎨 Most common colors in the pictograph:")
        for color, count in color_counts.most_common(20):
            print(f"  {color}: {count} pixels")
        
        # Look for blue-ish and red-ish colors
        blue_ish_colors = []
        red_ish_colors = []
        
        for color in color_counts.keys():
            # Convert hex to RGB to analyze
            if color.startswith('#') and len(color) == 7:
                try:
                    r = int(color[1:3], 16)
                    g = int(color[3:5], 16)
                    b = int(color[5:7], 16)
                    
                    # Check if it's blue-ish (blue component > red and green)
                    if b > r and b > g and b > 100:
                        blue_ish_colors.append((color, r, g, b, color_counts[color]))
                    
                    # Check if it's red-ish (red component > blue and green)
                    if r > b and r > g and r > 100:
                        red_ish_colors.append((color, r, g, b, color_counts[color]))
                        
                except ValueError:
                    pass
        
        print(f"\n🔵 Blue-ish colors found ({len(blue_ish_colors)}):")
        for color, r, g, b, count in blue_ish_colors:
            print(f"  {color} (R:{r}, G:{g}, B:{b}): {count} pixels")
        
        print(f"\n🔴 Red-ish colors found ({len(red_ish_colors)}):")
        for color, r, g, b, count in red_ish_colors:
            print(f"  {color} (R:{r}, G:{g}, B:{b}): {count} pixels")
        
        # Check for any non-white, non-black colors (indicating real content)
        interesting_colors = [
            color for color in color_counts.keys() 
            if color not in ['#ffffff', '#000000', '#c0c0c0', '#808080']
        ]
        
        print(f"\n✨ Interesting colors (not white/black/gray): {len(interesting_colors)}")
        for color in interesting_colors[:10]:  # Show first 10
            print(f"  {color}: {color_counts[color]} pixels")
        
        # The test passes if we have any blue-ish or red-ish colors
        has_arrows = len(blue_ish_colors) > 0 or len(red_ish_colors) > 0
        print(f"\n🏹 Has arrow colors: {has_arrows}")
        
        # Also check if we have a reasonable number of unique colors (indicating real pictographs)
        unique_colors = len(color_counts)
        print(f"🌈 Total unique colors: {unique_colors}")
        
        # Real pictographs should have some variety
        assert unique_colors > 5, f"Expected >5 unique colors, got {unique_colors}"
        
        # Should have some non-basic colors
        assert len(interesting_colors) > 0, "Should have some interesting colors beyond basic white/black/gray"
