"""
Quick Safety Check for God Object Refactoring

This script performs basic validation to ensure the refactored services work
before running full integration tests.
"""


def test_focused_services_basic():
    """Test that focused services can be imported and instantiated."""

    print("🧪 BASIC SERVICE VALIDATION")
    print("=" * 50)

    issues_found = []

    # Test 1: Import all focused services
    try:
        from src.desktop.modern.application.services.sequence.beat_creation_service import (
            BeatCreationService,
        )
        from src.desktop.modern.application.services.sequence.beat_operation_coordinator import (
            BeatOperationCoordinator,
        )
        from src.desktop.modern.application.services.sequence.beat_sequence_service import (
            BeatSequenceService,
        )
        from src.desktop.modern.application.services.sequence.sequence_persistence_adapter import (
            SequencePersistenceAdapter,
        )
        from src.desktop.modern.application.services.sequence.sequence_word_calculator import (
            SequenceWordCalculator,
        )

        print("✅ All focused services imported successfully")
    except ImportError as e:
        issues_found.append(f"Import Error: {e}")
        print(f"❌ Import failed: {e}")

    # Test 2: Instantiate focused services
    try:
        beat_creator = BeatCreationService()
        sequence_service = BeatSequenceService()
        word_calculator = SequenceWordCalculator()
        persistence = SequencePersistenceAdapter()
        coordinator = BeatOperationCoordinator()
        print("✅ All focused services instantiated successfully")
    except Exception as e:
        issues_found.append(f"Instantiation Error: {e}")
        print(f"❌ Instantiation failed: {e}")

    # Test 3: Test basic functionality
    try:
        # Test word calculation
        simplified = word_calculator.simplify_repeated_word("ABCABC")
        if simplified != "ABC":
            issues_found.append(
                f"Word calculation failed: expected 'ABC', got '{simplified}'"
            )
        else:
            print("✅ Word calculation works correctly")

        # Test beat number calculation
        next_beat = beat_creator.calculate_next_beat_number(None)
        if next_beat != 1:
            issues_found.append(
                f"Beat number calculation failed: expected 1, got {next_beat}"
            )
        else:
            print("✅ Beat number calculation works correctly")

    except Exception as e:
        issues_found.append(f"Functionality Error: {e}")
        print(f"❌ Functionality test failed: {e}")

    # Test 4: Check backward compatibility
    try:
        from src.desktop.modern.application.services.sequence.sequence_beat_operations import (
            SequenceBeatOperations,
        )

        legacy_adapter = SequenceBeatOperations()
        print("✅ Legacy adapter works correctly")
    except Exception as e:
        issues_found.append(f"Legacy Adapter Error: {e}")
        print(f"❌ Legacy adapter failed: {e}")

    # Summary
    print("\n📊 VALIDATION SUMMARY")
    print("-" * 30)
    if not issues_found:
        print("✅ All basic validations passed!")
        print("🎯 Services are ready for integration testing")
        return True
    else:
        print(f"❌ Found {len(issues_found)} issues:")
        for i, issue in enumerate(issues_found, 1):
            print(f"   {i}. {issue}")
        print("🚨 Fix these issues before integration testing")
        return False


if __name__ == "__main__":
    import os
    import sys

    # Add project root to path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    sys.path.insert(0, project_root)

    success = test_focused_services_basic()
    sys.exit(0 if success else 1)
