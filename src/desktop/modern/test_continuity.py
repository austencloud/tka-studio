#!/usr/bin/env python3
"""
Test script to verify positional continuity in generated sequences
"""

from __future__ import annotations

from pathlib import Path
import sys


# Add the modern directory to path
modern_path = Path(__file__).parent / "src" / "desktop" / "modern"
sys.path.insert(0, str(modern_path))


def test_positional_continuity():
    """Test that generated sequences have proper positional continuity."""
    try:
        print("🧪 Testing Positional Continuity in Generated Sequences")
        print("=" * 60)

        # Import required modules
        from desktop.modern.application.services.generation.core.freeform_generator import (
            FreeformGenerator,
        )
        from desktop.modern.core.interfaces.generation_services import (
            GenerationMode,
            LetterType,
            PropContinuity,
        )
        from desktop.modern.domain.models.enums import GridMode
        from desktop.modern.domain.models.generation_models import GenerationConfig

        print("✅ Imports successful")

        # Create generator
        generator = FreeformGenerator()
        print("✅ Generator created")

        # Test configuration
        config = GenerationConfig(
            mode=GenerationMode.FREEFORM,
            length=8,  # Generate 8 beats to test longer continuity
            level=1,  # Simple level, no turns
            turn_intensity=0.0,
            grid_mode=GridMode.DIAMOND,
            prop_continuity=PropContinuity.CONTINUOUS,
            letter_types={LetterType.TYPE1, LetterType.TYPE2},
            slice_size=None,
            cap_type=None,
        )

        print(
            f"✅ Config created: {config.length} beats, {config.grid_mode.value} mode"
        )

        # Generate sequence
        print("\n🎯 Generating sequence...")
        sequence = generator.generate_sequence(config)

        if not sequence:
            print("❌ No sequence generated!")
            return False

        print(f"✅ Generated {len(sequence)} beats")

        # Analyze positional continuity
        print("\n🔍 Analyzing Positional Continuity:")
        print("-" * 40)

        continuity_errors = 0

        for i, beat in enumerate(sequence):
            beat_num = i + 1
            start_pos = beat.start_position
            end_pos = beat.end_position

            print(f"Beat {beat_num}: {start_pos} → {end_pos} (Letter: {beat.letter})")

            # Check continuity with next beat
            if i < len(sequence) - 1:
                next_beat = sequence[i + 1]
                next_start = next_beat.start_position

                if end_pos != next_start:
                    print(
                        f"  ❌ CONTINUITY ERROR: Beat {beat_num} ends at {end_pos} but Beat {beat_num + 1} starts at {next_start}"
                    )
                    continuity_errors += 1
                else:
                    print(f"  ✅ Continuity OK: {end_pos} → {next_start}")

        print("\n📊 Continuity Analysis Results:")
        print("-" * 40)
        print(f"Total beats: {len(sequence)}")
        print(f"Continuity checks: {len(sequence) - 1}")
        print(f"Continuity errors: {continuity_errors}")

        if continuity_errors == 0:
            print("🎉 PERFECT CONTINUITY! All beats flow logically.")
            return True
        print(f"❌ CONTINUITY ISSUES: {continuity_errors} breaks in the sequence flow.")
        return False

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_start_position_logic():
    """Test that start positions are established correctly."""
    try:
        print("\n🧪 Testing Start Position Logic")
        print("=" * 40)

        from desktop.modern.application.services.generation.core.freeform_generator import (
            FreeformGenerator,
        )
        from desktop.modern.core.interfaces.generation_services import (
            GenerationMode,
            LetterType,
            PropContinuity,
        )
        from desktop.modern.domain.models.enums import GridMode
        from desktop.modern.domain.models.generation_models import GenerationConfig

        generator = FreeformGenerator()

        # Test diamond mode
        config_diamond = GenerationConfig(
            mode=GenerationMode.FREEFORM,
            length=3,
            level=1,
            turn_intensity=0.0,
            grid_mode=GridMode.DIAMOND,
            prop_continuity=PropContinuity.CONTINUOUS,
            letter_types={LetterType.TYPE1},
            slice_size=None,
            cap_type=None,
        )

        print("Testing Diamond mode...")
        sequence_diamond = generator.generate_sequence(config_diamond)
        if sequence_diamond:
            first_beat = sequence_diamond[0]
            print(f"  Diamond sequence starts at: {first_beat.start_position}")
            valid_diamond_starts = ["alpha1", "beta5", "gamma11"]
            if first_beat.start_position in valid_diamond_starts:
                print("  ✅ Valid diamond start position")
            else:
                print(
                    f"  ❌ Invalid diamond start position: {first_beat.start_position}"
                )

        # Test box mode
        config_box = GenerationConfig(
            mode=GenerationMode.FREEFORM,
            length=3,
            level=1,
            turn_intensity=0.0,
            grid_mode=GridMode.BOX,
            prop_continuity=PropContinuity.CONTINUOUS,
            letter_types={LetterType.TYPE1},
            slice_size=None,
            cap_type=None,
        )

        print("Testing Box mode...")
        sequence_box = generator.generate_sequence(config_box)
        if sequence_box:
            first_beat = sequence_box[0]
            print(f"  Box sequence starts at: {first_beat.start_position}")
            valid_box_starts = ["alpha2", "beta6", "gamma12"]
            if first_beat.start_position in valid_box_starts:
                print("  ✅ Valid box start position")
            else:
                print(f"  ❌ Invalid box start position: {first_beat.start_position}")

        return True

    except Exception as e:
        print(f"❌ Start position test failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Starting Continuity Tests\n")

    success1 = test_positional_continuity()
    success2 = test_start_position_logic()

    print("\n" + "=" * 60)
    if success1 and success2:
        print("🎉 ALL TESTS PASSED! Generation has proper continuity.")
    else:
        print("❌ SOME TESTS FAILED! Check the output above.")
