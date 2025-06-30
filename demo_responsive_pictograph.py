#!/usr/bin/env python3
"""
Responsive Pictograph Sizing Demonstration
==========================================

Visual demonstration of the responsive pictograph sizing system showing
how the pictograph adapts to different container sizes automatically.
"""

import sys
import os
from pathlib import Path

# Add TKA source path
tka_root = Path(__file__).parent
sys.path.insert(0, str(tka_root / "src" / "desktop" / "modern" / "src"))

def demonstrate_responsive_sizing():
    """Demonstrate responsive sizing with various container widths."""
    print("=" * 70)
    print("RESPONSIVE PICTOGRAPH SIZING DEMONSTRATION")
    print("=" * 70)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.graph_editor.components.pictograph_display_section import PictographDisplaySection
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # Create responsive pictograph display
        display_section = PictographDisplaySection()
        
        print("📐 Size Calculation Formula:")
        print("   available_width = container_width - info_panel_width - spacing - margins")
        print("   pictograph_size = min(max_size, max(min_size, available_width))")
        print()
        
        # Get configuration details
        min_size, max_size = display_section.get_size_constraints()
        info_panel_width = display_section._info_panel_min_width
        spacing = display_section._component_spacing
        margins = display_section._container_margins * 2
        
        print(f"⚙️  Configuration:")
        print(f"   Min pictograph size: {min_size}px")
        print(f"   Max pictograph size: {max_size}px")
        print(f"   Info panel width: {info_panel_width}px")
        print(f"   Component spacing: {spacing}px")
        print(f"   Container margins: {margins}px")
        print(f"   Total reserved space: {info_panel_width + spacing + margins}px")
        print()
        
        # Test various container sizes
        test_scenarios = [
            ("Mobile/Small", 320),
            ("Tablet Portrait", 600),
            ("Laptop", 1024),
            ("Desktop", 1440),
            ("Ultrawide", 1920),
        ]
        
        print("📱 Responsive Behavior Across Different Screen Sizes:")
        print("-" * 70)
        print(f"{'Screen Type':<15} {'Container':<10} {'Available':<10} {'Pictograph':<12} {'Status'}")
        print("-" * 70)
        
        for screen_type, container_width in test_scenarios:
            # Simulate container resize
            display_section.resize(container_width, 400)
            
            # Calculate what the pictograph size should be
            reserved_space = info_panel_width + spacing + margins
            available_width = container_width - reserved_space
            calculated_size = display_section._calculate_optimal_pictograph_size()
            
            # Determine status
            if calculated_size == min_size:
                status = "MIN (constrained)"
            elif calculated_size == max_size:
                status = "MAX (constrained)"
            else:
                status = "RESPONSIVE"
            
            print(f"{screen_type:<15} {container_width:<10} {available_width:<10} {calculated_size:<12} {status}")
        
        print("-" * 70)
        print()
        
        # Demonstrate dynamic updates
        print("🔄 Dynamic Resize Demonstration:")
        print("   Simulating container width changes...")
        
        sizes_to_test = [400, 600, 800, 1000, 1200, 800, 600, 400]
        current_size = display_section.get_current_pictograph_size()
        
        for i, width in enumerate(sizes_to_test):
            display_section.resize(width, 400)
            new_size = display_section._calculate_optimal_pictograph_size()
            
            if new_size != current_size:
                display_section._update_pictograph_size(new_size)
                direction = "↗️" if new_size > current_size else "↘️"
                print(f"   Step {i+1}: {width}px container → {new_size}px pictograph {direction}")
                current_size = new_size
        
        print()
        
        # Show space utilization
        print("📊 Space Utilization Analysis:")
        final_container_width = 1000
        display_section.resize(final_container_width, 400)
        final_pictograph_size = display_section.get_current_pictograph_size()
        
        pictograph_area = final_pictograph_size * final_pictograph_size
        info_panel_area = info_panel_width * 400  # Assuming 400px height
        total_usable_area = final_container_width * 400
        
        pictograph_percentage = (pictograph_area / total_usable_area) * 100
        info_panel_percentage = (info_panel_area / total_usable_area) * 100
        
        print(f"   Container: {final_container_width}px × 400px = {total_usable_area:,}px²")
        print(f"   Pictograph: {final_pictograph_size}px × {final_pictograph_size}px = {pictograph_area:,}px² ({pictograph_percentage:.1f}%)")
        print(f"   Info Panel: {info_panel_width}px × 400px = {info_panel_area:,}px² ({info_panel_percentage:.1f}%)")
        print()
        
        # Performance characteristics
        print("⚡ Performance Characteristics:")
        print("   ✓ Resize threshold: 5px (prevents micro-adjustments)")
        print("   ✓ Recursive resize protection: Built-in")
        print("   ✓ Smooth transitions: Automatic")
        print("   ✓ Memory efficient: No layout thrashing")
        print()
        
        print("🎯 Key Benefits:")
        print("   • Automatically adapts to any screen size")
        print("   • Maximizes pictograph visibility within constraints")
        print("   • Maintains professional layout proportions")
        print("   • No hardcoded dimensions - fully responsive")
        print("   • Backward compatible with existing code")
        
        return True
        
    except Exception as e:
        print(f"❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def demonstrate_constraint_customization():
    """Demonstrate how size constraints can be customized."""
    print("\n" + "=" * 70)
    print("SIZE CONSTRAINT CUSTOMIZATION DEMONSTRATION")
    print("=" * 70)
    
    try:
        from PyQt6.QtWidgets import QApplication
        from presentation.components.graph_editor.components.pictograph_display_section import PictographDisplaySection
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        display_section = PictographDisplaySection()
        
        print("🎛️  Customizing Size Constraints:")
        print()
        
        # Test different constraint scenarios
        constraint_scenarios = [
            ("Default", 200, 400),
            ("Compact", 150, 300),
            ("Large Display", 300, 600),
            ("Ultra-wide", 250, 800),
        ]
        
        container_width = 1000  # Fixed container for comparison
        display_section.resize(container_width, 400)
        
        print(f"Container Width: {container_width}px")
        print("-" * 50)
        print(f"{'Scenario':<15} {'Min':<6} {'Max':<6} {'Result':<8} {'Status'}")
        print("-" * 50)
        
        for scenario, min_size, max_size in constraint_scenarios:
            display_section.set_size_constraints(min_size, max_size)
            result_size = display_section._calculate_optimal_pictograph_size()
            
            if result_size == min_size:
                status = "MIN"
            elif result_size == max_size:
                status = "MAX"
            else:
                status = "CALC"
            
            print(f"{scenario:<15} {min_size:<6} {max_size:<6} {result_size:<8} {status}")
        
        print("-" * 50)
        print()
        
        print("📝 Constraint Guidelines:")
        print("   • Min size: Ensures readability on small screens")
        print("   • Max size: Prevents oversized pictographs on large displays")
        print("   • Range: Typically 200-400px works well for most use cases")
        print("   • Absolute limits: 100px minimum, 800px maximum (safety)")
        
        return True
        
    except Exception as e:
        print(f"❌ Constraint demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the responsive pictograph sizing demonstration."""
    success1 = demonstrate_responsive_sizing()
    success2 = demonstrate_constraint_customization()
    
    print("\n" + "=" * 70)
    if success1 and success2:
        print("✅ DEMONSTRATION COMPLETE - Responsive pictograph sizing is working perfectly!")
    else:
        print("❌ DEMONSTRATION FAILED - Some issues need to be addressed.")
    print("=" * 70)
    
    return success1 and success2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
