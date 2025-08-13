#!/usr/bin/env python3
"""
Test script to debug letter type determination.
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

# Set up logging
logging.basicConfig(level=logging.DEBUG, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def test_letter_type_determination():
    """Test letter type determination for specific letters."""

    print("Testing Letter Type Determination")
    print("=" * 40)

    try:
        # Test the classifier directly
        from desktop.modern.domain.models.enums import LetterType
        from desktop.modern.domain.models.letter_type_classifier import (
            LetterTypeClassifier,
        )

        test_letters = ["A", "W", "W-", "Φ", "Φ-", "α", "β", "Γ"]

        print("1. Testing LetterTypeClassifier directly:")
        for letter in test_letters:
            letter_type_str = LetterTypeClassifier.get_letter_type(letter)
            print(f"   {letter} -> {letter_type_str}")

        print("\n2. Testing enum values:")
        for enum_member in LetterType:
            print(f"   {enum_member.name} = '{enum_member.value}'")

        print("\n3. Testing conversion from string to enum:")
        for letter in test_letters:
            letter_type_str = LetterTypeClassifier.get_letter_type(letter)
            print(f"   Letter '{letter}' classified as: '{letter_type_str}'")

            # Try to find matching enum
            letter_type = None
            for enum_member in LetterType:
                if enum_member.value == letter_type_str:
                    letter_type = enum_member
                    break

            if letter_type:
                print(
                    f"     -> Found enum: {letter_type} (value: '{letter_type.value}')"
                )
            else:
                print(f"     -> No matching enum found for '{letter_type_str}'")

        print("\n4. Testing pictograph factory:")
        from desktop.modern.application.services.data.pictograph_factory import (
            PictographFactory,
        )

        factory = PictographFactory()

        # Create a test entry
        test_entry = {
            "letter": "A",
            "start_pos": "alpha1",
            "end_pos": "alpha1",
            "blue_motion_type": "static",
            "red_motion_type": "static",
            "blue_start_loc": "n",
            "red_start_loc": "n",
            "blue_end_loc": "n",
            "red_end_loc": "n",
        }

        pictograph_data = factory.create_pictograph_data_from_entry(
            test_entry, "diamond"
        )
        print(
            f"   Created pictograph for 'A': letter_type = {pictograph_data.letter_type}"
        )

        return True

    except Exception as e:
        print(f"Test failed with exception: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_letter_type_determination()
    sys.exit(0 if success else 1)
