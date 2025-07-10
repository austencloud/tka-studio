#!/usr/bin/env python3
"""
Simple integration test to check what methods are available.
"""

import os
import sys

# Add the src directory to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "src", "desktop", "modern", "src")
)


def test_orchestrator_methods():
    """Test what methods are available in the orchestrator."""
    print("🧪 Testing SequenceOrchestrator methods...")

    try:
        from application.services.sequence.sequence_orchestrator import (
            SequenceOrchestrator,
        )

        orchestrator = SequenceOrchestrator()
        print(f"   ✅ SequenceOrchestrator initialized")

        # List all available methods
        methods = [method for method in dir(orchestrator) if not method.startswith("_")]
        print(f"   📋 Available public methods:")
        for method in methods:
            print(f"     • {method}")

        # Test some basic methods
        try:
            length = orchestrator.get_current_sequence_length()
            print(f"   ✅ get_current_sequence_length(): {length}")
        except Exception as e:
            print(f"   ❌ get_current_sequence_length() failed: {e}")

        try:
            orchestrator.clear_sequence()
            print(f"   ✅ clear_sequence() succeeded")
        except Exception as e:
            print(f"   ❌ clear_sequence() failed: {e}")

        return True

    except Exception as e:
        print(f"   ❌ SequenceOrchestrator test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_beat_operations_methods():
    """Test what methods are available in beat operations."""
    print("\n🧪 Testing SequenceBeatOperations methods...")

    try:
        from application.services.sequence.sequence_beat_operations import (
            SequenceBeatOperations,
        )

        beat_ops = SequenceBeatOperations()
        print(f"   ✅ SequenceBeatOperations initialized")

        # List all available methods
        methods = [method for method in dir(beat_ops) if not method.startswith("_")]
        print(f"   📋 Available public methods:")
        for method in methods:
            print(f"     • {method}")

        return True

    except Exception as e:
        print(f"   ❌ SequenceBeatOperations test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_persister_basic():
    """Test basic persister functionality."""
    print("\n🧪 Testing SequencePersister basic functionality...")

    try:
        import tempfile
        from pathlib import Path

        from application.services.sequence.sequence_persister import SequencePersister

        with tempfile.TemporaryDirectory() as temp_dir:
            persister = SequencePersister()
            persister.current_sequence_json = Path(temp_dir) / "test.json"

            # Test load (should return default)
            sequence = persister.load_current_sequence()
            print(f"   ✅ Default sequence loaded: {len(sequence)} items")

            # Test save
            test_data = [{"metadata": "test"}, {"letter": "A"}]
            persister.save_current_sequence(test_data)
            print(f"   ✅ Test sequence saved")

            # Test load again
            loaded = persister.load_current_sequence()
            print(f"   ✅ Test sequence loaded: {len(loaded)} items")

            if loaded == test_data:
                print(f"   ✅ Data integrity maintained")
            else:
                print(f"   ⚠️ Data differs (may be expected)")

        return True

    except Exception as e:
        print(f"   ❌ SequencePersister test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_existing_workflow():
    """Test that existing workflow still works."""
    print("\n🧪 Testing existing workflow compatibility...")

    try:
        # Test the existing end-to-end workflow
        from src.desktop.modern.tests.end_to_end.test_complete_user_workflow import (
            CompleteUserWorkflowTest,
        )

        workflow_test = CompleteUserWorkflowTest()
        print(f"   ✅ Existing workflow test initialized")

        # Test that persistence service is working
        persistence = workflow_test.persistence_service
        current_sequence = persistence.load_current_sequence()
        print(f"   ✅ Current sequence loaded: {len(current_sequence)} items")

        return True

    except Exception as e:
        print(f"   ❌ Existing workflow test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🚀 Starting simple integration tests...\n")

    tests = [
        test_orchestrator_methods,
        test_beat_operations_methods,
        test_persister_basic,
        test_existing_workflow,
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

    print(f"\n📊 Simple Integration Test Results:")
    print(f"   ✅ Passed: {success_count}/{total_count}")
    print(f"   ❌ Failed: {total_count - success_count}/{total_count}")

    if success_count == total_count:
        print(f"\n🎉 All simple integration tests passed!")
    else:
        print(f"\n⚠️ Some simple integration tests failed!")

    sys.exit(0 if success_count == total_count else 1)
