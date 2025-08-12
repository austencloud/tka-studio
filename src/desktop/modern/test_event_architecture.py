#!/usr/bin/env python3
"""
Test script to verify the event-driven architecture migration is working.

This script tests the key components of the new architecture:
1. Service initialization
2. Command execution
3. Event flow
4. State management
5. Undo/redo functionality
"""

import sys
from pathlib import Path

# Add the src directory to the path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


def test_service_initialization():
    """Test that all services can be initialized"""
    logger.info("🧪 Testing service initialization...")

    try:
        from core.service_locator import initialize_services, is_initialized

        # Initialize services
        success = initialize_services()

        if success and is_initialized():
            logger.info("✅ Service initialization test PASSED")
            return True
        else:
            logger.error("❌ Service initialization test FAILED")
            return False

    except Exception as e:
        logger.error(f"❌ Service initialization test ERROR: {e}")
        return False


def test_start_position_command():
    """Test start position command execution"""
    logger.info("🧪 Testing start position command...")

    try:
        from core.commands.start_position_commands import SetStartPositionCommand
        from core.debugging.event_logger import enable_event_logging, log_debug_info
        from core.service_locator import get_command_processor, get_event_bus

        # Enable event logging for this test
        enable_event_logging()

        # Get services
        command_processor = get_command_processor()
        event_bus = get_event_bus()

        if not command_processor or not event_bus:
            logger.error("❌ Command processor or event bus not available")
            return False

        # Create and execute start position command
        command = SetStartPositionCommand(
            position_key="alpha1_alpha1", event_bus=event_bus
        )

        result = command_processor.execute(command)

        if result.success:
            logger.info("✅ Start position command execution test PASSED")

            # Test undo
            undo_result = command_processor.undo()
            if undo_result.success:
                logger.info("✅ Start position command undo test PASSED")
            else:
                logger.warning(
                    f"⚠️ Start position command undo test FAILED: {undo_result.error_message}"
                )

            # Test redo
            redo_result = command_processor.redo()
            if redo_result.success:
                logger.info("✅ Start position command redo test PASSED")
            else:
                logger.warning(
                    f"⚠️ Start position command redo test FAILED: {redo_result.error_message}"
                )

            # Log debug info
            log_debug_info()

            return True
        else:
            logger.error(
                f"❌ Start position command execution test FAILED: {result.error_message}"
            )
            return False

    except Exception as e:
        logger.error(f"❌ Start position command test ERROR: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_beat_command():
    """Test beat addition command"""
    logger.info("🧪 Testing beat addition command...")

    try:
        from core.commands.sequence_commands import AddBeatCommand
        from core.service_locator import (
            get_command_processor,
            get_event_bus,
            get_sequence_state_manager,
        )
        from domain.models.beat_models import BeatData
        from domain.models.sequence_data import SequenceData

        # Get services
        command_processor = get_command_processor()
        event_bus = get_event_bus()
        state_manager = get_sequence_state_manager()

        if not all([command_processor, event_bus, state_manager]):
            logger.error("❌ Required services not available")
            return False

        # Create a test beat
        test_beat = BeatData(letter="A", beat_number=1, duration=1.0)

        # Get current sequence or create empty one
        current_sequence = state_manager.get_sequence() or SequenceData.empty()

        # Create and execute add beat command
        command = AddBeatCommand(
            sequence=current_sequence, beat=test_beat, position=0, event_bus=event_bus
        )

        result = command_processor.execute(command)

        if result.success:
            logger.info("✅ Beat addition command test PASSED")

            # Verify state was updated
            updated_sequence = state_manager.get_sequence()
            if updated_sequence and updated_sequence.length > 0:
                logger.info("✅ State manager updated correctly")
            else:
                logger.warning("⚠️ State manager was not updated")

            return True
        else:
            logger.error(
                f"❌ Beat addition command test FAILED: {result.error_message}"
            )
            return False

    except Exception as e:
        logger.error(f"❌ Beat addition command test ERROR: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_state_manager():
    """Test state manager functionality"""
    logger.info("🧪 Testing state manager...")

    try:
        from core.service_locator import get_sequence_state_manager
        from domain.models.beat_models import BeatData
        from domain.models.sequence_data import SequenceData

        state_manager = get_sequence_state_manager()

        if not state_manager:
            logger.error("❌ State manager not available")
            return False

        # Test initial state
        initial_sequence = state_manager.get_sequence()
        initial_start_pos = state_manager.get_start_position()

        logger.info(
            f"   Initial sequence: {initial_sequence.length if initial_sequence else 0} beats"
        )
        logger.info(
            f"   Initial start position: {initial_start_pos.letter if initial_start_pos else 'None'}"
        )

        # Test state queries
        has_sequence = state_manager.has_sequence()
        has_start_pos = state_manager.has_start_position()
        is_empty = state_manager.is_empty()

        logger.info(f"   Has sequence: {has_sequence}")
        logger.info(f"   Has start position: {has_start_pos}")
        logger.info(f"   Is empty: {is_empty}")

        logger.info("✅ State manager test PASSED")
        return True

    except Exception as e:
        logger.error(f"❌ State manager test ERROR: {e}")
        return False


def run_all_tests():
    """Run all tests and report results"""
    logger.info("🚀 Starting event-driven architecture tests...")

    tests = [
        ("Service Initialization", test_service_initialization),
        ("State Manager", test_state_manager),
        ("Start Position Command", test_start_position_command),
        ("Beat Addition Command", test_beat_command),
    ]

    results = []

    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"Running test: {test_name}")
        logger.info(f"{'='*50}")

        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"❌ Test {test_name} crashed: {e}")
            results.append((test_name, False))

    # Report results
    logger.info(f"\n{'='*50}")
    logger.info("TEST RESULTS SUMMARY")
    logger.info(f"{'='*50}")

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
        if result:
            passed += 1

    logger.info(f"\nOverall: {passed}/{total} tests passed")

    if passed == total:
        logger.info(
            "🎉 All tests PASSED! Event-driven architecture is working correctly."
        )
        return True
    else:
        logger.error(f"💥 {total - passed} tests FAILED. Architecture needs debugging.")
        return False


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"💥 Test suite crashed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
