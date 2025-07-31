#!/usr/bin/env python3
"""
SVG Color Variant Generator for TKA Desktop Performance Optimization

This script pre-processes SVG files to generate blue and red color variants,
eliminating the need for runtime color transformation and improving performance
from 5-15ms per arrow to near-zero overhead.

PERFORMANCE IMPACT:
- Eliminates regex-based runtime color processing
- Reduces arrow rendering overhead by 5-15ms per arrow
- Pre-computed variants load directly without transformation

USAGE:
    python scripts/generate_colored_svg_variants.py

OUTPUT STRUCTURE:
    arrows/
    ├── pro/
    │   ├── blue/
    │   │   ├── pro_0.0.svg
    │   │   └── ...
    │   └── red/
    │       ├── pro_0.0.svg
    │       └── ...
"""

import logging
from pathlib import Path
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Color definitions matching the current implementation
COLORS = {
    "blue": "#2E3192",  # Reference blue color
    "red": "#ED1C24",  # Reference red color
}

# Pattern definitions for color transformation (matching current implementation)
COLOR_PATTERNS = [
    # CSS fill property: fill="#color"
    re.compile(r'(fill=")([^"]*)(")'),
    # CSS style attribute: fill: #color;
    re.compile(r"(fill:\s*)([^;]*)(;)"),
    # Class definition: .st0 { fill: #color; }
    re.compile(r"(\.(st0|cls-1)\s*\{[^}]*?fill:\s*)([^;}]*)([^}]*?\})"),
]


class SVGColorVariantGenerator:
    """Generates blue and red color variants of SVG files."""

    def __init__(self, source_dir: Path, output_dir: Path):
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.processed_files = 0
        self.skipped_files = 0
        self.error_files = 0

    def generate_all_variants(self) -> None:
        """Generate color variants for all SVG files in the source directory."""
        logger.info("Starting SVG color variant generation")
        logger.info(f"Source directory: {self.source_dir}")
        logger.info(f"Output directory: {self.output_dir}")

        # Find all SVG files recursively
        svg_files = list(self.source_dir.rglob("*.svg"))
        logger.info(f"Found {len(svg_files)} SVG files to process")

        for svg_file in svg_files:
            try:
                self._process_svg_file(svg_file)
            except Exception as e:
                logger.error(f"Failed to process {svg_file}: {e}")
                self.error_files += 1

        self._log_summary()

    def _process_svg_file(self, svg_file: Path) -> None:
        """Process a single SVG file to generate color variants."""
        # Read the original SVG content
        try:
            with open(svg_file, encoding="utf-8") as f:
                original_content = f.read()
        except Exception as e:
            logger.error(f"Failed to read {svg_file}: {e}")
            self.error_files += 1
            return

        # Calculate relative path from source directory
        relative_path = svg_file.relative_to(self.source_dir)

        # Generate variants for each color
        for color_name, color_value in COLORS.items():
            colored_content = self._apply_color_transformation(
                original_content, color_value
            )
            output_path = self._get_output_path(relative_path, color_name)

            # Create output directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write the colored variant
            try:
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(colored_content)
                logger.debug(f"Generated {color_name} variant: {output_path}")
            except Exception as e:
                logger.error(f"Failed to write {output_path}: {e}")
                self.error_files += 1
                return

        self.processed_files += 1
        if self.processed_files % 10 == 0:
            logger.info(f"Processed {self.processed_files} files...")

    def _apply_color_transformation(self, svg_content: str, target_color: str) -> str:
        """Apply color transformation to SVG content (matching current implementation)."""
        if not svg_content:
            return svg_content

        # Apply color transformation using all patterns
        for pattern in COLOR_PATTERNS:
            svg_content = pattern.sub(
                lambda m: m.group(1) + target_color + m.group(len(m.groups())),
                svg_content,
            )

        return svg_content

    def _get_output_path(self, relative_path: Path, color_name: str) -> Path:
        """Calculate the output path for a colored variant."""
        # Split the relative path into parts
        parts = list(relative_path.parts)

        # Insert color directory after the motion type directory
        # Example: pro/from_radial/pro_0.0.svg -> pro/blue/pro_0.0.svg
        if len(parts) >= 2:
            # Insert color after motion type (pro, anti, static, dash)
            parts.insert(1, color_name)
        else:
            # For files directly in arrows directory
            parts.insert(-1, color_name)

        return self.output_dir / Path(*parts)

    def _log_summary(self) -> None:
        """Log processing summary."""
        total_variants = self.processed_files * len(COLORS)
        logger.info("=" * 60)
        logger.info("SVG Color Variant Generation Complete")
        logger.info("=" * 60)
        logger.info(f"Files processed: {self.processed_files}")
        logger.info(f"Color variants generated: {total_variants}")
        logger.info(f"Files skipped: {self.skipped_files}")
        logger.info(f"Files with errors: {self.error_files}")
        logger.info(f"Output directory: {self.output_dir}")

        if self.error_files == 0:
            logger.info("✅ All files processed successfully!")
        else:
            logger.warning(f"⚠️  {self.error_files} files had errors")


def main():
    """Main entry point for the script."""
    # Find project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    # Define source and output directories
    source_dir = project_root / "src" / "desktop" / "images" / "arrows"
    output_dir = project_root / "src" / "desktop" / "images" / "arrows_colored"

    # Validate source directory exists
    if not source_dir.exists():
        logger.error(f"Source directory does not exist: {source_dir}")
        return 1

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate variants
    generator = SVGColorVariantGenerator(source_dir, output_dir)
    generator.generate_all_variants()

    return 0


if __name__ == "__main__":
    exit(main())
