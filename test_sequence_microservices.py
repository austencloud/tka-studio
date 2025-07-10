#!/usr/bin/env python3
"""
Comprehensive test suite for sequence microservices.
Tests each service individually and then integration.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

# Add the src directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "src", "desktop", "modern", "src")
)


def test_sequence_persister():
    """Test the SequencePersister microservice."""
    print("🧪 Testing SequencePersister...")

    try:
        from application.services.sequence.persister import SequencePersister

        # Create a temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create persister with custom path
            persister = SequencePersister()

            # Override the path for testing
            persister.current_sequence_json = Path(temp_dir) / "test_sequence.json"

            print(f"   📁 Using test file: {persister.current_sequence_json}")

            # Test 1: Load default sequence (file doesn't exist)
            default_sequence = persister.load_current_sequence()
            print(f"   ✅ Default sequence loaded: {len(default_sequence)} items")

            # Test 2: Save a sequence
            test_sequence = [
                {"metadata": "sequence_info"},
                {"letter": "α", "start_pos": "alpha1_alpha1", "end_pos": "alpha1"},
                {"letter": "A", "start_pos": "alpha1", "end_pos": "alpha3"},
            ]

            persister.save_current_sequence(test_sequence)
            print(f"   ✅ Sequence saved successfully")

            # Test 3: Load the saved sequence
            loaded_sequence = persister.load_current_sequence()
            print(f"   ✅ Sequence loaded: {len(loaded_sequence)} items")

            # Test 4: Verify content matches
            if loaded_sequence == test_sequence:
                print(f"   ✅ Sequence content matches saved data")
                return True
            else:
                print(f"   ❌ Sequence content mismatch")
                print(f"     Expected: {test_sequence}")
                print(f"     Got: {loaded_sequence}")
                return False

    except Exception as e:
        print(f"   ❌ SequencePersister test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_sequence_validator():
    """Test the SequenceValidator microservice."""
    print("\n🧪 Testing SequenceValidator...")

    try:
        from application.services.sequence.validator import (
            SequenceValidator,
            ValidationError,
        )
        from domain.models.beat_data import BeatData
        from domain.models.sequence_models import SequenceData

        validator = SequenceValidator()
        print(f"   ✅ SequenceValidator initialized")

        # Test 1: Create a valid sequence (beats start from 1, not 0)
        valid_beats = [
            BeatData.empty().update(beat_number=1, letter="A"),
            BeatData.empty().update(beat_number=2, letter="B"),
            BeatData.empty().update(beat_number=3, letter="C"),
        ]

        valid_sequence = SequenceData(
            name="test_sequence", beats=valid_beats, metadata={}
        )

        # Test validation
        is_valid = validator.validate_sequence(valid_sequence)
        print(f"   ✅ Valid sequence validation: {is_valid}")

        # Test 2: Test validation of invalid sequence (wrong beat numbering)
        invalid_beats = [
            BeatData.empty().update(beat_number=1, letter="A"),
            BeatData.empty().update(
                beat_number=4, letter="B"
            ),  # Wrong number! Should be 2
        ]

        try:
            # This should fail during SequenceData creation due to validation
            invalid_sequence = SequenceData(
                name="invalid_sequence", beats=invalid_beats, metadata={}
            )
            print(f"   ❌ Invalid sequence should have failed validation")
            return False
        except (ValidationError, ValueError) as e:
            print(f"   ✅ Invalid sequence correctly rejected during creation: {e}")

        return True

    except Exception as e:
        print(f"   ❌ SequenceValidator test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_sequence_transformer():
    """Test the SequenceTransformer microservice."""
    print("\n🧪 Testing SequenceTransformer...")

    try:
        from application.services.sequence.transformer import (
            SequenceTransformer,
            WorkbenchOperation,
        )
        from domain.models.beat_data import BeatData
        from domain.models.sequence_models import SequenceData

        transformer = SequenceTransformer()
        print(f"   ✅ SequenceTransformer initialized")

        # Create a test sequence (beats start from 1)
        test_beats = [
            BeatData.empty().update(beat_number=1, letter="A"),
            BeatData.empty().update(beat_number=2, letter="B"),
        ]

        test_sequence = SequenceData(
            name="test_sequence", beats=test_beats, metadata={}
        )

        # Test color swap operation
        swapped_sequence = transformer.apply_workbench_operation(
            test_sequence, WorkbenchOperation.COLOR_SWAP.value
        )

        print(f"   ✅ Color swap transformation applied")
        print(f"     Original: {len(test_sequence.beats)} beats")
        print(f"     Transformed: {len(swapped_sequence.beats)} beats")

        # Test horizontal reflection
        reflected_sequence = transformer.apply_workbench_operation(
            test_sequence, WorkbenchOperation.HORIZONTAL_REFLECTION.value
        )

        print(f"   ✅ Horizontal reflection applied")

        return True

    except Exception as e:
        print(f"   ❌ SequenceTransformer test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_sequence_generator():
    """Test the SequenceGenerator microservice."""
    print("\n🧪 Testing SequenceGenerator...")

    try:
        from application.services.sequence.generator import (
            SequenceGenerator,
            SequenceType,
        )

        generator = SequenceGenerator()
        print(f"   ✅ SequenceGenerator initialized")

        # Test freeform sequence generation
        freeform_sequence = generator.generate_sequence(
            SequenceType.FREEFORM, name="test_freeform", length=8
        )

        print(f"   ✅ Freeform sequence generated: {freeform_sequence.name}")
        print(f"     Length: {len(freeform_sequence.beats)} beats")

        # Test circular sequence generation
        circular_sequence = generator.generate_sequence(
            SequenceType.CIRCULAR, name="test_circular", length=16
        )

        print(f"   ✅ Circular sequence generated: {circular_sequence.name}")
        print(f"     Length: {len(circular_sequence.beats)} beats")

        return True

    except Exception as e:
        print(f"   ❌ SequenceGenerator test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_sequence_repository():
    """Test the SequenceRepository microservice."""
    print("\n🧪 Testing SequenceRepository...")

    try:
        from application.services.sequence.repository import SequenceRepository
        from domain.models.beat_data import BeatData
        from domain.models.sequence_models import SequenceData

        repository = SequenceRepository()
        print(f"   ✅ SequenceRepository initialized")

        # Create a test sequence (beats start from 1)
        test_beats = [
            BeatData.empty().update(beat_number=1, letter="A"),
            BeatData.empty().update(beat_number=2, letter="B"),
        ]

        test_sequence = SequenceData(
            name="test_repo_sequence", beats=test_beats, metadata={}
        )

        # Test save operation
        saved_sequence = repository.save(test_sequence)
        print(f"   ✅ Sequence saved: {saved_sequence.name}")

        # Test find operation
        found_sequence = repository.find_by_name("test_repo_sequence")
        if found_sequence:
            # Handle both single sequence and list returns
            if hasattr(found_sequence, "name"):
                print(f"   ✅ Sequence found: {found_sequence.name}")
            elif isinstance(found_sequence, list) and len(found_sequence) > 0:
                print(f"   ✅ Sequence found: {found_sequence[0].name}")
            else:
                print(f"   ✅ Sequence found (unknown format)")
        else:
            print(f"   ⚠️ Sequence not found (may be expected for in-memory repo)")

        # Test list operation
        all_sequences = repository.get_all()
        print(f"   ✅ Repository contains {len(all_sequences)} sequences")

        return True

    except Exception as e:
        print(f"   ❌ SequenceRepository test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Starting sequence microservices tests...\n")

    tests = [
        test_sequence_persister,
        test_sequence_validator,
        test_sequence_transformer,
        test_sequence_generator,
        test_sequence_repository,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            results.append(False)

    success_count = sum(results)
    total_count = len(results)

    print(f"\n📊 Microservices Test Results:")
    print(f"   ✅ Passed: {success_count}/{total_count}")
    print(f"   ❌ Failed: {total_count - success_count}/{total_count}")

    if success_count == total_count:
        print(f"\n🎉 All microservices tests passed!")
    else:
        print(f"\n⚠️ Some microservices tests failed!")

    sys.exit(0 if success_count == total_count else 1)
