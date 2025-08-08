#!/usr/bin/env python3
"""
Test script to verify positional continuity in sequence generation.
This script tests that generated sequences have proper positional flow.
"""

from __future__ import annotations

import logging
from pathlib import Path
import sys


# Use the same path setup as the main application
current_file = Path(__file__).resolve()
project_root = current_file.parents[3]  # test -> modern -> desktop -> TKA

# Add the src directory to path
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from desktop.modern.application.services.generation.freeform_generation_service import (
    FreeformGenerationService,
)
from desktop.modern.core.interfaces.generation_services import PropContinuity
from desktop.modern.domain.models.generation_models import GenerationConfig


# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def test_positional_continuity():
    """Test that generated sequences maintain positional continuity."""

    print("Testing Positional Continuity in Sequence Generation")
    print("=" * 60)

    try:
        # Initialize the freeform generation service
        print("1. Initializing freeform generation service...")
        service = FreeformGenerationService()
        print(
            f"   ✅ Service initialized with {len(service.pictograph_options)} pictographs"
        )

        # Create generation config
        config = GenerationConfig(
            length=5,  # Generate 5 beats
            level=1,  # Simple level
            turn_intensity=0,  # No turns
            prop_continuity=PropContinuity.RANDOM,  # Random for now
            letter_types=set(),  # All letter types
        )

        print(
            f"2. Generating sequence with config: length={config.length}, level={config.level}"
        )

        # Generate sequence
        generated_beats = service.generate_sequence(config)

        if not generated_beats:
            print("   ❌ No beats generated!")
            return False

        print(f"   ✅ Generated {len(generated_beats)} beats")

        # Check positional continuity
        print("3. Checking positional continuity...")
        continuity_errors = []

        for i in range(len(generated_beats) - 1):
            current_beat = generated_beats[i]
            next_beat = generated_beats[i + 1]

            current_end = current_beat.end_position
            next_start = next_beat.start_position

            print(f"   Beat {i + 1}: {current_beat.letter} ends at {current_end}")
            print(f"   Beat {i + 2}: {next_beat.letter} starts at {next_start}")

            if current_end != next_start:
                error_msg = f"❌ CONTINUITY BREAK: Beat {i + 1} ends at {current_end} but Beat {i + 2} starts at {next_start}"
                print(f"   {error_msg}")
                continuity_errors.append(error_msg)
            else:
                print(f"   ✅ Continuity maintained: {current_end} → {next_start}")

        # Final beat info
        if generated_beats:
            final_beat = generated_beats[-1]
            print(
                f"   Final beat: {final_beat.letter} ends at {final_beat.end_position}"
            )

        # Summary
        print("\n" + "=" * 60)
        if continuity_errors:
            print("❌ POSITIONAL CONTINUITY TEST FAILED")
            print(f"   Found {len(continuity_errors)} continuity errors:")
            for error in continuity_errors:
                print(f"   - {error}")
            return False
        print("✅ POSITIONAL CONTINUITY TEST PASSED")
        print(f"   All {len(generated_beats)} beats maintain proper positional flow!")

        # Additional test: Check if pictograph data has all required fields for rendering
        print("\n4. Checking pictograph data completeness for rendering...")
        for i, beat in enumerate(generated_beats):
            print(f"   Beat {i + 1} ({beat.letter}):")
            print(f"     - Letter: {beat.letter}")
            print(f"     - Letter Type: {beat.letter_type}")
            print(f"     - Start Position: {beat.start_position}")
            print(f"     - End Position: {beat.end_position}")
            print(
                f"     - Motions: {list(beat.motions.keys()) if beat.motions else 'None'}"
            )
            print(
                f"     - Arrows: {list(beat.arrows.keys()) if beat.arrows else 'None'}"
            )
            print(f"     - Grid Data: {'Present' if beat.grid_data else 'Missing'}")

            # Check if motion data is complete
            if beat.motions:
                for color, motion in beat.motions.items():
                    if motion:
                        print(
                            f"     - {color.title()} Motion: {motion.motion_type} from {motion.start_loc} to {motion.end_loc}"
                        )
                    else:
                        print(f"     - {color.title()} Motion: None")

        return True

    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_positional_continuity()
    sys.exit(0 if success else 1)
