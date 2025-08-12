#!/usr/bin/env python3
"""
Test script for TKA Modern Write Tab Implementation

Tests the complete write tab functionality including:
1. Service registration and DI resolution
2. Act data management
3. Music player functionality
4. UI components
5. Tab factory integration
"""
from __future__ import annotations

import logging
from pathlib import Path
import sys
import tempfile


# Add TKA to path
tka_root = Path(__file__).parent
sys.path.insert(0, str(tka_root / "src"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_write_service_registration():
    """Test that all write services can be registered and resolved."""
    try:
        from desktop.modern.core.dependency_injection.di_container import DIContainer
        from desktop.modern.core.dependency_injection.write_service_registration import (
            register_write_services,
            validate_write_service_registration,
        )
        from desktop.modern.core.interfaces.write_services import (
            IActDataService,
            IActEditingService,
            IActLayoutService,
            IMusicPlayerService,
            IWriteTabCoordinator,
        )

        container = DIContainer()

        # Register services
        register_write_services(container)

        # Test service resolution
        container.resolve(IActDataService)
        container.resolve(IActEditingService)
        container.resolve(IActLayoutService)
        container.resolve(IMusicPlayerService)
        container.resolve(IWriteTabCoordinator)

        logger.info("✅ All write services resolved successfully")

        # Run comprehensive validation
        validation_result = validate_write_service_registration(container)
        if validation_result:
            logger.info("✅ Write service validation passed")
        else:
            logger.error("❌ Write service validation failed")
            return False

        return True

    except Exception as e:
        logger.exception(f"❌ Write service registration test failed: {e}")
        return False

def test_act_data_operations():
    """Test act data service operations."""
    try:
        from desktop.modern.application.services.write.act_data_service import (
            ActDataService,
        )
        from desktop.modern.core.interfaces.write_services import ActData

        # Create temporary directory for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            service = ActDataService(Path(temp_dir))

            # Create test act
            test_act = ActData(
                name="Test Act",
                description="A test act for validation",
                sequences=[
                    {"beats": [{"timing": 1, "duration": 2}]},
                    {"beats": [{"timing": 2, "duration": 2}]},
                ],
                metadata={"test": True}
            )

            # Test save
            save_path = Path(temp_dir) / "test_act.json"
            save_result = service.save_act(test_act, save_path)
            if not save_result:
                logger.error("❌ Failed to save test act")
                return False

            # Test load
            loaded_act = service.load_act(save_path)
            if not loaded_act:
                logger.error("❌ Failed to load test act")
                return False

            # Verify data integrity
            if loaded_act.name != test_act.name:
                logger.error("❌ Act name mismatch after load")
                return False

            if len(loaded_act.sequences) != len(test_act.sequences):
                logger.error("❌ Sequence count mismatch after load")
                return False

            # Test get available acts
            available_acts = service.get_available_acts()
            if len(available_acts) != 1:
                logger.error("❌ Expected 1 available act, got {len(available_acts)}")
                return False

            # Test act info
            act_info = service.get_act_info(save_path)
            if not act_info or act_info["name"] != "Test Act":
                logger.error("❌ Act info mismatch")
                return False

            logger.info("✅ Act data operations test passed")
            return True

    except Exception as e:
        logger.exception(f"❌ Act data operations test failed: {e}")
        return False

def test_act_editing_operations():
    """Test act editing service operations."""
    try:
        from desktop.modern.application.services.write.act_editing_service import (
            ActEditingService,
        )
        from desktop.modern.core.interfaces.write_services import ActData

        service = ActEditingService()

        # Create test act
        test_act = ActData(name="Edit Test Act")

        # Test add sequence
        test_sequence = {"beats": [{"timing": 1, "duration": 2}]}
        add_result = service.add_sequence_to_act(test_act, test_sequence)
        if not add_result:
            logger.error("❌ Failed to add sequence to act")
            return False

        if len(test_act.sequences) != 1:
            logger.error("❌ Expected 1 sequence after add")
            return False

        # Test add another sequence
        test_sequence2 = {"beats": [{"timing": 2, "duration": 2}]}
        service.add_sequence_to_act(test_act, test_sequence2)

        if len(test_act.sequences) != 2:
            logger.error("❌ Expected 2 sequences after second add")
            return False

        # Test move sequence
        move_result = service.move_sequence_in_act(test_act, 0, 1)
        if not move_result:
            logger.error("❌ Failed to move sequence")
            return False

        # Test remove sequence
        remove_result = service.remove_sequence_from_act(test_act, 0)
        if not remove_result:
            logger.error("❌ Failed to remove sequence")
            return False

        if len(test_act.sequences) != 1:
            logger.error("❌ Expected 1 sequence after removal")
            return False

        # Test duplicate sequence
        duplicate_result = service.duplicate_sequence_in_act(test_act, 0)
        if not duplicate_result:
            logger.error("❌ Failed to duplicate sequence")
            return False

        if len(test_act.sequences) != 2:
            logger.error("❌ Expected 2 sequences after duplicate")
            return False

        # Test update metadata
        metadata_result = service.update_act_metadata(test_act, {"test_key": "test_value"})
        if not metadata_result:
            logger.error("❌ Failed to update metadata")
            return False

        if test_act.metadata.get("test_key") != "test_value":
            logger.error("❌ Metadata not updated correctly")
            return False

        logger.info("✅ Act editing operations test passed")
        return True

    except Exception as e:
        logger.exception(f"❌ Act editing operations test failed: {e}")
        return False

def test_layout_calculations():
    """Test act layout service calculations."""
    try:
        from desktop.modern.application.services.write.act_layout_service import (
            ActLayoutService,
        )

        service = ActLayoutService()

        # Test grid dimensions
        test_cases = [
            (1, (1, 1)),
            (4, (2, 2)),
            (6, (3, 2)),
            (9, (3, 3)),
            (10, (4, 3)),
        ]

        for sequence_count, _expected in test_cases:
            result = service.calculate_grid_dimensions(sequence_count)
            cols, rows = result

            # Verify we can fit all sequences
            if cols * rows < sequence_count:
                logger.error(f"❌ Grid {cols}x{rows} can't fit {sequence_count} sequences")
                return False

        # Test sequence size calculation
        size_result = service.calculate_sequence_size(800, 600, 3, 2)
        width, height = size_result

        if width <= 0 or height <= 0:
            logger.error(f"❌ Invalid sequence size: {width}x{height}")
            return False

        # Test position calculation
        position_result = service.get_sequence_position(5, 3)  # 6th sequence in 3-column grid
        col, row = position_result

        if col != 2 or row != 1:  # Should be 3rd column, 2nd row
            logger.error(f"❌ Wrong position calculation: got ({col}, {row}), expected (2, 1)")
            return False

        logger.info("✅ Layout calculations test passed")
        return True

    except Exception as e:
        logger.exception(f"❌ Layout calculations test failed: {e}")
        return False

def test_music_player_service():
    """Test music player service (without actual audio files)."""
    try:
        from desktop.modern.application.services.write.music_player_service import (
            MusicPlayerService,
        )

        service = MusicPlayerService()

        # Test availability check
        is_available = service.is_available()
        logger.info(f"Music player available: {is_available}")

        # Test supported formats
        formats = service.get_supported_formats()
        logger.info(f"Supported formats: {formats}")

        # Test basic state
        if service.is_playing():
            logger.error("❌ Music player should not be playing initially")
            return False

        duration = service.get_duration()
        if duration != 0.0:
            logger.error("❌ Duration should be 0.0 initially")
            return False

        position = service.get_position()
        if position != 0.0:
            logger.error("❌ Position should be 0.0 initially")
            return False

        logger.info("✅ Music player service test passed")
        return True

    except Exception as e:
        logger.exception(f"❌ Music player service test failed: {e}")
        return False

def test_coordinator_integration():
    """Test write tab coordinator integration."""
    try:
        from desktop.modern.core.dependency_injection.di_container import DIContainer
        from desktop.modern.core.dependency_injection.write_service_registration import (
            register_write_services,
        )
        from desktop.modern.core.interfaces.write_services import IWriteTabCoordinator

        container = DIContainer()
        register_write_services(container)

        coordinator = container.resolve(IWriteTabCoordinator)

        # Test create new act
        new_act = coordinator.create_new_act()
        if not new_act or new_act.name != "Untitled Act":
            logger.error("❌ Failed to create new act")
            return False

        # Test current act tracking
        current_act = coordinator.get_current_act()
        if current_act != new_act:
            logger.error("❌ Current act tracking failed")
            return False

        # Test act info update
        update_result = coordinator.update_current_act_info("Test Coordinator Act", "Test description")
        if not update_result:
            logger.error("❌ Failed to update act info")
            return False

        # Test add sequence
        test_sequence = {"beats": [{"timing": 1, "duration": 2}]}
        add_result = coordinator.add_sequence_to_current_act(test_sequence)
        if not add_result:
            logger.error("❌ Failed to add sequence to current act")
            return False

        # Test modification tracking
        if not coordinator.is_current_act_modified():
            logger.error("❌ Act should be marked as modified")
            return False

        # Test layout calculation
        cols, rows = coordinator.calculate_grid_layout(6)
        if cols <= 0 or rows <= 0:
            logger.error("❌ Invalid grid layout calculation")
            return False

        logger.info("✅ Coordinator integration test passed")
        return True

    except Exception as e:
        logger.exception(f"❌ Coordinator integration test failed: {e}")
        return False

def test_tab_factory_integration():
    """Test that write tab is properly integrated in TabFactory."""
    try:
        from desktop.modern.application.services.ui.tab_factory.tab_factory import (
            TabFactory,
        )

        factory = TabFactory()
        definitions = factory.get_tab_definitions()

        # Check if write tab is defined
        write_tab_found = False
        for defn in definitions:
            if defn.tab_id == "write":
                write_tab_found = True
                if defn.display_name != "✍️ Write":
                    logger.error("❌ Wrong write tab display name")
                    return False
                break

        if not write_tab_found:
            logger.error("❌ Write tab not found in TabFactory definitions")
            return False

        logger.info("✅ TabFactory integration test passed")
        return True

    except Exception as e:
        logger.exception(f"❌ TabFactory integration test failed: {e}")
        return False

def test_menu_bar_integration():
    """Test that write tab is in menu bar configuration."""
    try:
        from desktop.modern.presentation.components.menu_bar.navigation.menu_bar_navigation_widget import (
            MenuBarNavigationWidget,
        )

        menu_bar = MenuBarNavigationWidget()
        available_tabs = menu_bar.get_available_tabs()

        if "write" not in available_tabs:
            logger.error("❌ Write tab not found in menu bar")
            return False

        logger.info("✅ Menu bar integration test passed")
        return True

    except Exception as e:
        logger.exception(f"❌ Menu bar integration test failed: {e}")
        return False

def main():
    """Run all write tab tests."""
    logger.info("🧪 Testing TKA Modern Write Tab Implementation")
    logger.info("=" * 60)

    tests = [
        ("Write Service Registration", test_write_service_registration),
        ("Act Data Operations", test_act_data_operations),
        ("Act Editing Operations", test_act_editing_operations),
        ("Layout Calculations", test_layout_calculations),
        ("Music Player Service", test_music_player_service),
        ("Coordinator Integration", test_coordinator_integration),
        ("TabFactory Integration", test_tab_factory_integration),
        ("Menu Bar Integration", test_menu_bar_integration),
    ]

    results = []
    for test_name, test_func in tests:
        logger.info(f"\n📋 Running: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            logger.info(f"Result: {'PASS' if result else 'FAIL'}")
        except Exception as e:
            logger.exception(f"Test crashed: {e}")
            results.append((test_name, False))
            logger.info("Result: CRASH")

    logger.info("\n" + "=" * 60)
    logger.info("📊 WRITE TAB TEST RESULTS:")

    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"  {status} - {test_name}")
        if result:
            passed += 1

    logger.info(f"\n🎯 Summary: {passed}/{len(tests)} tests passed")

    if passed == len(tests):
        logger.info("🎉 All write tab tests passed! Implementation is ready.")
        return True
    logger.info("⚠️ Some tests failed. Review the issues above.")
    return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
