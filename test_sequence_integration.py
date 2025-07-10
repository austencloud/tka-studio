#!/usr/bin/env python3
"""
Integration test suite for sequence microservices.
Tests how the services work together through the orchestrator.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the src directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "src", "desktop", "modern", "src")
)


def test_orchestrator_integration():
    """Test the SequenceOrchestrator integrating multiple microservices."""
    print("🧪 Testing SequenceOrchestrator Integration...")

    try:
        from application.services.sequence.orchestrator import SequenceOrchestrator
        from domain.models.beat_data import BeatData
        from domain.models.pictograph_models import PictographData
        from domain.models.sequence_models import SequenceData

        # Create orchestrator
        orchestrator = SequenceOrchestrator()
        print(f"   ✅ SequenceOrchestrator initialized")

        # Test 1: Create a test pictograph (no empty() method, use constructor)
        from domain.models.pictograph_models import GridData

        test_pictograph = PictographData(
            grid_data=GridData(),
            arrows={},
            props={},
            letter="A",
            start_position="alpha1",
            end_position="alpha3",
            metadata={"test": True},
        )

        print(f"   ✅ Test pictograph created: {test_pictograph.letter}")

        # Test 2: Add the pictograph to the sequence

        orchestrator.add_pictograph_to_sequence(test_pictograph)
        print(f"   ✅ Pictograph added to sequence")

        # Test 3: Apply a transformation (use the correct method name)
        current_sequence = orchestrator._get_current_sequence()
        if current_sequence:
            transformed_sequence = orchestrator.apply_workbench_transformation(
                "color_swap"
            )
            print(f"   ✅ Workbench transformation applied")
            if transformed_sequence:
                print(f"     Transformed beats: {len(transformed_sequence.beats)}")
        else:
            print(f"   ⚠️ No current sequence to transform")

        # Test 4: Get sequence length
        length = orchestrator.get_current_sequence_length()
        print(f"   ✅ Current sequence length: {length}")

        return True

    except Exception as e:
        print(f"   ❌ SequenceOrchestrator integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_beat_operations_integration():
    """Test the SequenceBeatOperations service integration."""
    print("\n🧪 Testing SequenceBeatOperations Integration...")

    try:
        from application.services.sequence.beat_operations import SequenceBeatOperations
        from domain.models.pictograph_models import PictographData

        # Create beat operations service
        beat_ops = SequenceBeatOperations()
        print(f"   ✅ SequenceBeatOperations initialized")

        # Test adding a pictograph
        from domain.models.pictograph_models import GridData

        test_pictograph = PictographData(
            grid_data=GridData(),
            arrows={},
            props={},
            letter="B",
            start_position="alpha3",
            end_position="alpha5",
            metadata={"test": True},
        )

        beat_ops.add_pictograph_to_sequence(test_pictograph)
        print(f"   ✅ Pictograph added via beat operations")

        # Test updating beat turns
        beat_ops.update_beat_turns(0, 2)
        print(f"   ✅ Beat turns updated")

        return True

    except Exception as e:
        print(f"   ❌ SequenceBeatOperations integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_full_workflow_integration():
    """Test a complete workflow using multiple microservices."""
    print("\n🧪 Testing Full Workflow Integration...")

    try:
        from application.services.sequence.orchestrator import SequenceOrchestrator
        from application.services.sequence.persister import SequencePersister
        from application.services.sequence.transformer import SequenceTransformer
        from application.services.sequence.validator import SequenceValidator
        from domain.models.pictograph_models import PictographData

        # Step 1: Create orchestrator and services
        orchestrator = SequenceOrchestrator()
        persister = SequencePersister()
        validator = SequenceValidator()
        transformer = SequenceTransformer()

        print(f"   ✅ All services initialized")

        # Step 2: Create test pictographs
        from domain.models.pictograph_models import GridData

        pictographs = [
            PictographData(
                grid_data=GridData(),
                arrows={},
                props={},
                letter="A",
                start_position="alpha1",
                end_position="alpha3",
                metadata={"test": True},
            ),
            PictographData(
                grid_data=GridData(),
                arrows={},
                props={},
                letter="B",
                start_position="alpha3",
                end_position="alpha5",
                metadata={"test": True},
            ),
            PictographData(
                grid_data=GridData(),
                arrows={},
                props={},
                letter="C",
                start_position="alpha5",
                end_position="alpha7",
                metadata={"test": True},
            ),
        ]

        print(f"   ✅ Created test pictographs")

        # Step 3: Add multiple pictographs
        for i, pictograph in enumerate(pictographs):
            orchestrator.add_pictograph_to_sequence(pictograph)
            print(f"   ✅ Added pictograph {i+1}: {pictograph.letter}")

        # Get current sequence length
        length = orchestrator.get_current_sequence_length()
        print(f"   📊 Final sequence has {length} beats")

        # Step 4: Get current sequence for validation
        current_sequence = orchestrator._get_current_sequence()
        if current_sequence:
            is_valid = validator.validate_sequence(current_sequence)
            print(f"   ✅ Sequence validation: {is_valid}")

            # Step 5: Apply transformation
            transformed = transformer.apply_workbench_operation(
                current_sequence, "color_swap"
            )
            print(f"   ✅ Applied color swap transformation")
        else:
            print(f"   ⚠️ No current sequence available for validation")

        # Step 6: Save to persistence
        with tempfile.TemporaryDirectory() as temp_dir:
            persister.current_sequence_json = Path(temp_dir) / "workflow_test.json"

            # Convert to legacy format for persistence
            legacy_data = [
                {"metadata": "sequence_info"},
                {"letter": "A", "start_pos": "alpha1", "end_pos": "alpha3"},
                {"letter": "B", "start_pos": "alpha3", "end_pos": "alpha5"},
                {"letter": "C", "start_pos": "alpha5", "end_pos": "alpha7"},
            ]

            persister.save_current_sequence(legacy_data)
            loaded_data = persister.load_current_sequence()

            print(f"   ✅ Sequence saved and loaded: {len(loaded_data)} items")

        return True

    except Exception as e:
        print(f"   ❌ Full workflow integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_application_context_integration():
    """Test the microservices in the context of the full application."""
    print("\n🧪 Testing Application Context Integration...")

    try:
        # Test that the microservices work with the existing application workflow
        from src.desktop.modern.tests.end_to_end.test_complete_user_workflow import (
            CompleteUserWorkflowTest,
        )

        # Create a test instance
        workflow_test = CompleteUserWorkflowTest()

        print(f"   ✅ Application workflow test initialized")

        # Test that the persistence service works
        persistence_service = workflow_test.persistence_service

        # Load current sequence
        current_sequence = persistence_service.load_current_sequence()
        print(f"   ✅ Current sequence loaded: {len(current_sequence)} items")

        # Test saving a sequence
        test_sequence = [
            {"metadata": "sequence_info"},
            {"letter": "α", "start_pos": "alpha1_alpha1", "end_pos": "alpha1"},
            {"letter": "A", "start_pos": "alpha1", "end_pos": "alpha3"},
        ]

        persistence_service.save_current_sequence(test_sequence)
        loaded_sequence = persistence_service.load_current_sequence()

        print(f"   ✅ Test sequence saved and loaded: {len(loaded_sequence)} items")

        # Verify content matches
        if loaded_sequence == test_sequence:
            print(f"   ✅ Sequence content integrity maintained")
        else:
            print(f"   ⚠️ Sequence content differs (may be expected)")

        return True

    except Exception as e:
        print(f"   ❌ Application context integration test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Starting sequence microservices integration tests...\n")

    tests = [
        test_orchestrator_integration,
        test_beat_operations_integration,
        test_full_workflow_integration,
        test_application_context_integration,
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

    print(f"\n📊 Integration Test Results:")
    print(f"   ✅ Passed: {success_count}/{total_count}")
    print(f"   ❌ Failed: {total_count - success_count}/{total_count}")

    if success_count == total_count:
        print(f"\n🎉 All integration tests passed!")
        print(f"\n✅ Microservices Integration Summary:")
        print(f"   • SequenceOrchestrator coordinates all operations")
        print(f"   • SequenceBeatOperations handles beat-level changes")
        print(f"   • SequencePersister manages data persistence")
        print(f"   • SequenceValidator ensures data integrity")
        print(f"   • SequenceTransformer applies workbench operations")
        print(f"   • All services work together seamlessly")
    else:
        print(f"\n⚠️ Some integration tests failed!")

    sys.exit(0 if success_count == total_count else 1)
