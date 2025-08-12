#!/usr/bin/env python3
"""
Test script to determine the correct beat size for modern image export
by simulating legacy beat size calculations.
"""

from __future__ import annotations

from pathlib import Path
import sys


# Add the src directory to the Python path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))


def simulate_legacy_beat_size_calculation():
    """Simulate how legacy calculates beat size"""
    print("=== SIMULATING LEGACY BEAT SIZE CALCULATION ===")

    # Typical legacy beat frame dimensions (estimated from UI)
    # These would vary based on window size and layout
    test_scenarios = [
        {"name": "Small Window", "width": 800, "height": 600, "cols": 4},
        {"name": "Medium Window", "width": 1200, "height": 800, "cols": 4},
        {"name": "Large Window", "width": 1600, "height": 1000, "cols": 4},
        {"name": "2-Beat Sequence", "width": 1200, "height": 800, "cols": 2},
        {"name": "8-Beat Sequence", "width": 1200, "height": 800, "cols": 4},  # 2 rows
        {"name": "16-Beat Sequence", "width": 1200, "height": 800, "cols": 4},  # 4 rows
    ]

    print("Legacy beat size calculation: min(width // num_cols, height // 6)")
    print()

    for scenario in test_scenarios:
        width = scenario["width"]
        height = scenario["height"]
        cols = scenario["cols"]

        # Legacy calculation
        width_constraint = width // cols
        height_constraint = height // 6
        beat_size = min(width_constraint, height_constraint)

        print(f"{scenario['name']}:")
        print(f"  Dimensions: {width}x{height}, Columns: {cols}")
        print(f"  Width constraint: {width} // {cols} = {width_constraint}")
        print(f"  Height constraint: {height} // 6 = {height_constraint}")
        print(
            f"  Beat size: min({width_constraint}, {height_constraint}) = {beat_size}"
        )
        print()

    print("ANALYSIS:")
    print("- Modern system uses fixed beat_size = 300")
    print("- Legacy system typically produces beat sizes between 100-200")
    print("- This explains why modern fonts appear larger!")
    print("- Font sizes scale with beat_size, so larger beats = larger fonts")


def calculate_font_size_differences():
    """Calculate how font sizes differ between legacy and modern"""
    print("\n=== FONT SIZE DIFFERENCES ===")

    # Base font sizes
    word_font_base = 175
    user_info_font_base = 50

    # Typical beat sizes
    legacy_beat_size = 150  # Typical legacy beat size
    modern_beat_size = 300  # Current modern beat size

    # Beat scale is always 1 in both systems

    print("Base font sizes:")
    print(f"  Word font: {word_font_base}pt")
    print(f"  User info font: {user_info_font_base}pt")
    print()

    print("Beat sizes:")
    print(f"  Legacy (typical): {legacy_beat_size}px")
    print(f"  Modern (current): {modern_beat_size}px")
    print(f"  Ratio: {modern_beat_size / legacy_beat_size:.2f}x larger")
    print()

    # For 4+ beat sequences (no scaling applied)
    print("Font sizes for 4+ beat sequences (no beat count scaling):")
    print(f"  Legacy word font: {word_font_base}pt")
    print(f"  Modern word font: {word_font_base}pt")
    print(f"  Legacy user info font: {user_info_font_base}pt")
    print(f"  Modern user info font: {user_info_font_base}pt")
    print("  → Font sizes are the same, but images are larger!")
    print()

    # The issue is not font size per se, but image scale
    print("THE REAL ISSUE:")
    print("- Font sizes (in points) are correct")
    print("- But images are larger due to larger beat_size")
    print("- This makes fonts APPEAR larger relative to other elements")
    print("- Solution: Use legacy-compatible beat_size calculation")


def propose_solution():
    """Propose a solution for the font sizing issue"""
    print("\n=== PROPOSED SOLUTION ===")

    print("1. REPLACE HARDCODED BEAT_SIZE")
    print("   Current: beat_size = 300")
    print("   Proposed: beat_size = calculate_legacy_compatible_beat_size()")
    print()

    print("2. IMPLEMENT LEGACY-COMPATIBLE CALCULATION")
    print("   def calculate_legacy_compatible_beat_size(num_beats):")
    print("       # Estimate typical legacy beat frame dimensions")
    print("       typical_width = 1200")
    print("       typical_height = 800")
    print("       cols = calculate_columns(num_beats)")
    print("       return min(typical_width // cols, typical_height // 6)")
    print()

    print("3. EXPECTED RESULTS")
    print("   - 1-4 beats: beat_size ≈ 133-150px (vs current 300px)")
    print("   - Fonts will appear smaller and match legacy")
    print("   - Image dimensions will be smaller and match legacy")
    print("   - Overall export will be pixel-perfect with legacy")
    print()

    print("4. IMPLEMENTATION STEPS")
    print("   a. Add beat_size calculation to ModernImageExportService")
    print("   b. Pass calculated beat_size to ModernImageRenderer")
    print("   c. Update all hardcoded 300 values to use calculated beat_size")
    print("   d. Test with various sequence lengths")


if __name__ == "__main__":
    print("Analyzing beat size calculation differences...")
    print("=" * 60)

    simulate_legacy_beat_size_calculation()
    calculate_font_size_differences()
    propose_solution()

    print("\n" + "=" * 60)
    print("🔍 ROOT CAUSE IDENTIFIED!")
    print("\nThe font sizing issue is caused by:")
    print("1. Modern system uses beat_size = 300 (hardcoded)")
    print("2. Legacy system uses beat_size ≈ 100-200 (calculated)")
    print("3. Larger beat_size creates larger images")
    print("4. Same font sizes in larger images appear proportionally larger")
    print("\nSolution: Replace hardcoded beat_size with legacy-compatible calculation")
