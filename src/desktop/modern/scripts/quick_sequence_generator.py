#!/usr/bin/env python3
"""
Quick Sequence Generator

A simple tool to quickly generate sequences and export them as images for testing.
This tool can grab example sequences from metadata or create custom ones.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
import sys


# Add the src directory to the Python path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from PyQt6.QtWidgets import QApplication

from desktop.modern.core.dependency_injection.di_container import DIContainer
from desktop.modern.core.dependency_injection.image_export_service_registration import (
    register_image_export_services,
)
from desktop.modern.core.interfaces.image_export_services import (
    IImageExportService,
    ImageExportOptions,
)


def get_sample_sequences():
    """Get sample sequences for testing"""
    return {
        "simple_4beat": [
            {
                "beat": "1",
                "red_attributes": {
                    "start_loc": "n",
                    "end_loc": "s",
                    "motion_type": "pro",
                    "turns": 0,
                },
                "blue_attributes": {
                    "start_loc": "s",
                    "end_loc": "n",
                    "motion_type": "pro",
                    "turns": 0,
                },
                "start_position": "alpha",
                "end_position": "alpha",
            },
            {
                "beat": "2",
                "red_attributes": {
                    "start_loc": "s",
                    "end_loc": "e",
                    "motion_type": "anti",
                    "turns": 1,
                },
                "blue_attributes": {
                    "start_loc": "n",
                    "end_loc": "w",
                    "motion_type": "anti",
                    "turns": 1,
                },
                "start_position": "alpha",
                "end_position": "beta",
            },
            {
                "beat": "3",
                "red_attributes": {
                    "start_loc": "e",
                    "end_loc": "w",
                    "motion_type": "pro",
                    "turns": 0,
                },
                "blue_attributes": {
                    "start_loc": "w",
                    "end_loc": "e",
                    "motion_type": "pro",
                    "turns": 0,
                },
                "start_position": "beta",
                "end_position": "gamma",
            },
            {
                "beat": "4",
                "red_attributes": {
                    "start_loc": "w",
                    "end_loc": "n",
                    "motion_type": "anti",
                    "turns": 1,
                },
                "blue_attributes": {
                    "start_loc": "e",
                    "end_loc": "s",
                    "motion_type": "anti",
                    "turns": 1,
                },
                "start_position": "gamma",
                "end_position": "alpha",
            },
        ],
        "simple_2beat": [
            {
                "beat": "1",
                "red_attributes": {
                    "start_loc": "n",
                    "end_loc": "s",
                    "motion_type": "pro",
                    "turns": 0,
                },
                "blue_attributes": {
                    "start_loc": "s",
                    "end_loc": "n",
                    "motion_type": "pro",
                    "turns": 0,
                },
                "start_position": "alpha",
                "end_position": "alpha",
            },
            {
                "beat": "2",
                "red_attributes": {
                    "start_loc": "s",
                    "end_loc": "n",
                    "motion_type": "pro",
                    "turns": 0,
                },
                "blue_attributes": {
                    "start_loc": "n",
                    "end_loc": "s",
                    "motion_type": "pro",
                    "turns": 0,
                },
                "start_position": "alpha",
                "end_position": "alpha",
            },
        ],
        "single_beat": [
            {
                "beat": "1",
                "red_attributes": {
                    "start_loc": "n",
                    "end_loc": "s",
                    "motion_type": "pro",
                    "turns": 0,
                },
                "blue_attributes": {
                    "start_loc": "s",
                    "end_loc": "n",
                    "motion_type": "pro",
                    "turns": 0,
                },
                "start_position": "alpha",
                "end_position": "alpha",
            }
        ],
        "complex_8beat": [
            {
                "beat": str(i + 1),
                "red_attributes": {
                    "start_loc": ["n", "s", "e", "w"][i % 4],
                    "end_loc": ["s", "n", "w", "e"][i % 4],
                    "motion_type": ["pro", "anti"][i % 2],
                    "turns": i % 2,
                },
                "blue_attributes": {
                    "start_loc": ["s", "n", "w", "e"][i % 4],
                    "end_loc": ["n", "s", "e", "w"][i % 4],
                    "motion_type": ["anti", "pro"][i % 2],
                    "turns": (i + 1) % 2,
                },
                "start_position": ["alpha", "beta", "gamma"][i % 3],
                "end_position": ["beta", "gamma", "alpha"][i % 3],
            }
            for i in range(8)
        ],
    }


def create_export_options(preset="full"):
    """Create export options with different presets"""
    presets = {
        "full": ImageExportOptions(
            add_word=True,
            add_user_info=True,
            add_difficulty_level=True,
            add_beat_numbers=True,
            add_reversal_symbols=True,
            include_start_position=True,
            user_name="Test User",
            export_date=datetime.now().strftime("%m-%d-%Y"),
            notes="Full export with all elements",
        ),
        "minimal": ImageExportOptions(
            add_word=False,
            add_user_info=False,
            add_difficulty_level=False,
            add_beat_numbers=True,
            add_reversal_symbols=False,
            include_start_position=False,
            user_name="",
            export_date="",
            notes="",
        ),
        "text_only": ImageExportOptions(
            add_word=True,
            add_user_info=True,
            add_difficulty_level=False,
            add_beat_numbers=False,
            add_reversal_symbols=False,
            include_start_position=False,
            user_name="Quick Test",
            export_date=datetime.now().strftime("%m-%d-%Y"),
            notes="Text elements only",
        ),
        "beats_only": ImageExportOptions(
            add_word=False,
            add_user_info=False,
            add_difficulty_level=False,
            add_beat_numbers=True,
            add_reversal_symbols=True,
            include_start_position=True,
            user_name="",
            export_date="",
            notes="",
        ),
    }
    return presets.get(preset, presets["full"])


def generate_quick_sequence(
    sequence_name="simple_4beat", word="QUICK", preset="full", output_name=None
):
    """Generate a quick sequence image for testing"""
    print(f"=== GENERATING QUICK SEQUENCE: {sequence_name.upper()} ===")

    QApplication(sys.argv)

    # Setup export service
    container = DIContainer()
    register_image_export_services(container)
    export_service = container.resolve(IImageExportService)

    # Get sample sequences
    sequences = get_sample_sequences()

    if sequence_name not in sequences:
        print(f"❌ Unknown sequence: {sequence_name}")
        print(f"Available sequences: {list(sequences.keys())}")
        return False

    sequence = sequences[sequence_name]
    options = create_export_options(preset)

    print(f"Sequence: {len(sequence)} beats")
    print(f"Word: {word}")
    print(f"Preset: {preset}")
    print(
        f"Options: word={options.add_word}, user_info={options.add_user_info}, beat_numbers={options.add_beat_numbers}"
    )

    try:
        # Create image
        image = export_service.create_sequence_image(sequence, word, options)

        print(f"Generated image: {image.width()}×{image.height()}px")

        # Save image
        output_dir = Path(__file__).parent / "quick_sequences"
        output_dir.mkdir(exist_ok=True)

        if output_name is None:
            output_name = f"{sequence_name}_{word}_{preset}.png"

        output_path = output_dir / output_name
        success = image.save(str(output_path))

        if success:
            print(f"✅ Saved to: {output_path}")
            print(f"📁 Open folder: {output_dir}")
            return True
        print("❌ Failed to save image")
        return False

    except Exception as e:
        print(f"❌ Error generating sequence: {e}")
        import traceback

        traceback.print_exc()
        return False


def generate_comparison_set():
    """Generate a set of images for comparison"""
    print("=== GENERATING COMPARISON SET ===")

    sequences = ["single_beat", "simple_2beat", "simple_4beat", "complex_8beat"]
    presets = ["full", "minimal", "text_only", "beats_only"]

    success_count = 0
    total_count = 0

    for sequence in sequences:
        for preset in presets:
            total_count += 1
            word = f"TEST{len(get_sample_sequences()[sequence])}"
            output_name = f"comparison_{sequence}_{preset}.png"

            print(f"\n--- {sequence} with {preset} preset ---")
            if generate_quick_sequence(sequence, word, preset, output_name):
                success_count += 1

    print("\n=== COMPARISON SET COMPLETE ===")
    print(f"Generated {success_count}/{total_count} images successfully")
    print(f"📁 All images saved to: {Path(__file__).parent / 'quick_sequences'}")


def main():
    """Main function with command line interface"""
    if len(sys.argv) < 2:
        print("Quick Sequence Generator")
        print("=" * 50)
        print("Usage:")
        print("  python quick_sequence_generator.py <command> [options]")
        print()
        print("Commands:")
        print("  single [word] [preset]     - Generate single sequence")
        print("  compare                    - Generate comparison set")
        print("  list                       - List available sequences")
        print()
        print("Available sequences:")
        for name, seq in get_sample_sequences().items():
            print(f"  {name:<15} - {len(seq)} beats")
        print()
        print("Available presets:")
        print("  full        - All elements (word, user info, beat numbers, etc.)")
        print("  minimal     - Just beat numbers")
        print("  text_only   - Word and user info only")
        print("  beats_only  - Beats with numbers and start position")
        print()
        print("Examples:")
        print("  python quick_sequence_generator.py single")
        print("  python quick_sequence_generator.py single simple_2beat HELLO full")
        print("  python quick_sequence_generator.py compare")
        return

    command = sys.argv[1].lower()

    if command == "single":
        sequence_name = sys.argv[2] if len(sys.argv) > 2 else "simple_4beat"
        word = sys.argv[3] if len(sys.argv) > 3 else "QUICK"
        preset = sys.argv[4] if len(sys.argv) > 4 else "full"

        generate_quick_sequence(sequence_name, word, preset)

    elif command == "compare":
        generate_comparison_set()

    elif command == "list":
        print("Available sequences:")
        for name, seq in get_sample_sequences().items():
            print(f"  {name:<15} - {len(seq)} beats")
            for i, beat in enumerate(seq[:2]):  # Show first 2 beats
                red = beat["red_attributes"]
                blue = beat["blue_attributes"]
                print(
                    f"    Beat {i + 1}: R:{red['start_loc']}→{red['end_loc']} B:{blue['start_loc']}→{blue['end_loc']}"
                )
            if len(seq) > 2:
                print(f"    ... and {len(seq) - 2} more beats")
            print()
    else:
        print(f"Unknown command: {command}")
        print("Use 'python quick_sequence_generator.py' for help")


if __name__ == "__main__":
    main()
