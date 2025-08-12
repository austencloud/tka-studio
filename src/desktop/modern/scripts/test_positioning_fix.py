#!/usr/bin/env python3
"""
Test script to demonstrate and fix the positioning difference between legacy and modern image export.

The issue: Modern version adds extra margin to beat positioning, causing unwanted extra height.
Legacy: y = row * beat_size + additional_height_top
Modern: y = options.additional_height_top + margin + row * (beat_size + margin)

The modern version incorrectly adds margin to the Y positioning, which creates extra space.
"""

from __future__ import annotations

from pathlib import Path
import sys


# Add the src directory to the Python path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QImage, QPainter
from PyQt6.QtWidgets import QApplication


def demonstrate_positioning_difference():
    """Demonstrate the positioning difference between legacy and modern approaches."""

    # Test parameters
    beat_size = 300
    additional_height_top = 200
    margin = 10
    rows = 2
    cols = 2

    print("=== POSITIONING COMPARISON ===")
    print(f"Beat size: {beat_size}")
    print(f"Additional height top: {additional_height_top}")
    print(f"Margin: {margin}")
    print(f"Grid: {rows}x{cols}")
    print()

    print("LEGACY POSITIONING (correct):")
    for row in range(rows):
        for col in range(cols):
            x = col * beat_size
            y = row * beat_size + additional_height_top
            print(f"  Beat at row {row}, col {col}: x={x}, y={y}")

    print()
    print("MODERN POSITIONING (incorrect - adds extra margin):")
    for row in range(rows):
        for col in range(cols):
            x = margin + col * (beat_size + margin)
            y = additional_height_top + margin + row * (beat_size + margin)
            print(f"  Beat at row {row}, col {col}: x={x}, y={y}")

    print()
    print("FIXED MODERN POSITIONING (should match legacy):")
    for row in range(rows):
        for col in range(cols):
            x = margin + col * (
                beat_size + margin
            )  # X positioning can keep margin for spacing
            y = (
                additional_height_top + row * beat_size
            )  # Y positioning should NOT add margin
            print(f"  Beat at row {row}, col {col}: x={x}, y={y}")

    print()
    print("ANALYSIS:")
    legacy_first_beat_y = additional_height_top
    modern_first_beat_y = additional_height_top + margin
    fixed_first_beat_y = additional_height_top

    print(f"Legacy first beat Y: {legacy_first_beat_y}")
    print(f"Modern first beat Y: {modern_first_beat_y} (extra {margin} pixels!)")
    print(f"Fixed first beat Y: {fixed_first_beat_y}")
    print(
        f"Extra height in modern version: {modern_first_beat_y - legacy_first_beat_y} pixels"
    )


def create_visual_comparison():
    """Create visual comparison images to show the difference."""

    QApplication(sys.argv)

    # Test parameters
    beat_size = 100
    additional_height_top = 150
    margin = 10
    rows = 2
    cols = 2

    # Calculate image dimensions
    width = cols * beat_size + 2 * margin
    height = rows * beat_size + additional_height_top + margin

    # Create legacy-style image
    legacy_image = QImage(width, height, QImage.Format.Format_ARGB32)
    legacy_image.fill(Qt.GlobalColor.white)

    legacy_painter = QPainter(legacy_image)
    legacy_painter.setPen(Qt.GlobalColor.red)
    legacy_painter.setBrush(Qt.GlobalColor.red)

    print("Creating legacy-style positioning image...")
    for row in range(rows):
        for col in range(cols):
            x = col * beat_size
            y = row * beat_size + additional_height_top
            legacy_painter.drawRect(x, y, beat_size - 5, beat_size - 5)
            print(f"  Legacy beat at ({x}, {y})")

    legacy_painter.end()

    # Create modern-style image (with bug)
    modern_image = QImage(width, height, QImage.Format.Format_ARGB32)
    modern_image.fill(Qt.GlobalColor.white)

    modern_painter = QPainter(modern_image)
    modern_painter.setPen(Qt.GlobalColor.blue)
    modern_painter.setBrush(Qt.GlobalColor.blue)

    print("\nCreating modern-style positioning image (with bug)...")
    for row in range(rows):
        for col in range(cols):
            x = margin + col * (beat_size + margin)
            y = (
                additional_height_top + margin + row * (beat_size + margin)
            )  # BUG: extra margin
            modern_painter.drawRect(x, y, beat_size - 5, beat_size - 5)
            print(f"  Modern beat at ({x}, {y})")

    modern_painter.end()

    # Create fixed modern-style image
    fixed_image = QImage(width, height, QImage.Format.Format_ARGB32)
    fixed_image.fill(Qt.GlobalColor.white)

    fixed_painter = QPainter(fixed_image)
    fixed_painter.setPen(Qt.GlobalColor.green)
    fixed_painter.setBrush(Qt.GlobalColor.green)

    print("\nCreating fixed modern-style positioning image...")
    for row in range(rows):
        for col in range(cols):
            x = margin + col * (beat_size + margin)
            y = additional_height_top + row * beat_size  # FIXED: no extra margin
            fixed_painter.drawRect(x, y, beat_size - 5, beat_size - 5)
            print(f"  Fixed beat at ({x}, {y})")

    fixed_painter.end()

    # Save comparison images
    output_dir = Path(__file__).parent / "positioning_comparison"
    output_dir.mkdir(exist_ok=True)

    legacy_image.save(str(output_dir / "legacy_positioning.png"))
    modern_image.save(str(output_dir / "modern_positioning_bug.png"))
    fixed_image.save(str(output_dir / "modern_positioning_fixed.png"))

    print(f"\nComparison images saved to: {output_dir}")
    print("- legacy_positioning.png (red squares)")
    print("- modern_positioning_bug.png (blue squares - shows extra height)")
    print("- modern_positioning_fixed.png (green squares - matches legacy)")


if __name__ == "__main__":
    print("Testing positioning differences between legacy and modern image export...")
    print()

    demonstrate_positioning_difference()
    print()

    try:
        create_visual_comparison()
    except Exception as e:
        print(f"Could not create visual comparison: {e}")
        print("This is normal if running without display.")

    print("\nConclusion:")
    print("The modern image export adds an extra margin to the Y positioning,")
    print("which causes unwanted extra height at the top of exported images.")
    print("The fix is to remove the margin from the Y calculation while keeping")
    print("it for X positioning to maintain proper spacing between beats.")
