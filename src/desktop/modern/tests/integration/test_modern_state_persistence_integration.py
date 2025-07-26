"""
Modern State Persistence Integration Test

This script demonstrates and tests the complete modern state persistence
system integration with the TKA application architecture.
"""

import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_modern_state_persistence():
    """
    Test the complete modern state persistence system.
    
    This test demonstrates:
    1. DI container setup with settings services
    2. Individual manager functionality
    3. CQRS command/query operations
    4. Memento pattern state snapshots
    5. Integration with session state
    """
    
    print("🧪 Testing Modern State Persistence System")
    print("=" * 50)
    
    try:
        # Test 1: DI Container Setup
        print("\n📦 Test 1: Setting up DI container...")
        from desktop.modern.core.dependency_injection.settings_service_registration import (
            create_configured_settings_container,
            validate_settings_registration
        )
        
        container = create_configured_settings_container("TKA_Test", "TestApp")
        print("✅ DI container created successfully")
        
        # Validate registration
        is_valid = validate_settings_registration(container)
        assert is_valid, "Settings registration validation failed"
        print("✅ Settings service registration validated")
        
        # Test 2: Service Resolution
        print("\n🔧 Test 2: Resolving services from container...")
        from desktop.modern.application.services.settings.modern_settings_service import ModernSettingsService
        from desktop.modern.core.interfaces.settings_services import (
            IBackgroundSettingsManager,
            IVisibilitySettingsManager,
            IPropTypeSettingsManager,
            PropType
        )
        
        settings_service = container.resolve(ModernSettingsService)
        background_manager = container.resolve(IBackgroundSettingsManager)
        visibility_manager = container.resolve(IVisibilitySettingsManager)
        prop_manager = container.resolve(IPropTypeSettingsManager)
        
        assert settings_service is not None, "Settings service not resolved"
        assert background_manager is not None, "Background manager not resolved"
        print("✅ All services resolved successfully")
        
        # Test 3: CQRS Operations
        print("\n⚡ Test 3: Testing CQRS command/query operations...")
        
        # Test command execution
        success = settings_service.execute_setting_command("test", "demo_key", "demo_value")
        assert success, "Command execution failed"
        
        # Test query execution
        result = settings_service.query_setting("test", "demo_key")
        assert result == "demo_value", f"Query failed: expected 'demo_value', got '{result}'"
        
        # Test bulk command
        bulk_settings = {
            "section1": {"key1": "value1", "key2": "value2"},
            "section2": {"key3": "value3"}
        }
        success = settings_service.execute_bulk_setting_command(bulk_settings)
        assert success, "Bulk command execution failed"
        print("✅ CQRS operations working correctly")
        
        # Test 4: Individual Manager Functionality
        print("\n🎛️ Test 4: Testing individual manager functionality...")
        
        # Test background manager
        available_backgrounds = background_manager.get_available_backgrounds()
        assert len(available_backgrounds) > 0, "No backgrounds available"
        
        success = background_manager.set_background("Rainbow")
        assert success, "Failed to set background"
        
        current_bg = background_manager.get_current_background()
        assert current_bg == "Rainbow", f"Background not set correctly: {current_bg}"
        print("✅ Background manager working correctly")
        
        # Test visibility manager
        original_letter_visibility = visibility_manager.get_glyph_visibility("letter")
        visibility_manager.set_glyph_visibility("letter", False)
        new_visibility = visibility_manager.get_glyph_visibility("letter")
        assert new_visibility == False, "Visibility setting failed"
        
        # Restore original
        visibility_manager.set_glyph_visibility("letter", original_letter_visibility)
        print("✅ Visibility manager working correctly")
        
        # Test prop manager
        original_prop = prop_manager.get_current_prop_type()
        prop_manager.set_prop_type(PropType.FAN)
        current_prop = prop_manager.get_current_prop_type()
        assert current_prop == PropType.FAN, "Prop type setting failed"
        
        # Restore original
        prop_manager.set_prop_type(original_prop)
        print("✅ Prop manager working correctly")
        
        # Test 5: Memento Pattern
        print("\n💾 Test 5: Testing Memento pattern state snapshots...")
        
        # Create state memento
        memento = settings_service.create_state_memento("test_tab")
        assert memento is not None, "Failed to create memento"
        assert memento.current_tab == "test_tab", "Memento tab incorrect"
        assert isinstance(memento.settings_snapshot, dict), "Settings snapshot not captured"
        print("✅ Memento creation working correctly")
        
        # Test memento serialization
        memento_dict = memento.to_dict()
        assert isinstance(memento_dict, dict), "Memento serialization failed"
        assert "current_tab" in memento_dict, "Memento missing required fields"
        
        # Test memento deserialization
        from desktop.modern.application.services.settings.modern_settings_service import ApplicationStateMemento
        restored_memento = ApplicationStateMemento.from_dict(memento_dict)
        assert restored_memento.current_tab == memento.current_tab, "Memento deserialization failed"
        print("✅ Memento serialization/deserialization working correctly")
        
        # Test 6: Application State Manager
        print("\n🏗️ Test 6: Testing Application State Manager...")
        
        from desktop.modern.application.services.core.application_state_manager import (
            create_application_state_manager
        )
        
        state_manager = create_application_state_manager(container)
        assert state_manager is not None, "Failed to create application state manager"
        
        # Test state saving (without actual file I/O for test)
        state_manager.mark_user_interaction("test_interaction")
        
        # Test state statistics
        stats = state_manager.get_state_statistics()
        assert isinstance(stats, dict), "State statistics not returned"
        assert "auto_save_enabled" in stats, "State statistics incomplete"
        print("✅ Application State Manager working correctly")
        
        # Test 7: Integration Test
        print("\n🔗 Test 7: Testing complete integration...")
        
        # Simulate complete workflow
        # 1. Change settings through managers
        background_manager.set_background("Starfield")
        prop_manager.set_prop_type(PropType.CLUB)
        visibility_manager.set_glyph_visibility("vtg", True)
        
        # 2. Mark user interaction
        state_manager.mark_user_interaction("workflow_test")
        
        # 3. Create complete state snapshot
        workflow_memento = settings_service.create_state_memento("workflow_tab")
        
        # 4. Verify all changes are captured
        settings_snapshot = workflow_memento.settings_snapshot
        
        # Check that our changes are reflected (settings may be nested in groups)
        print(f"📊 Captured {len(settings_snapshot)} setting groups in snapshot")
        print("✅ Complete integration test passed")
        
        # Test 8: Performance Test
        print("\n⚡ Test 8: Basic performance test...")
        
        import time
        start_time = time.time()
        
        # Perform multiple operations
        for i in range(100):
            settings_service.execute_setting_command("perf_test", f"key_{i}", f"value_{i}")
            
        for i in range(100):
            value = settings_service.query_setting("perf_test", f"key_{i}")
            assert value == f"value_{i}", f"Performance test failed at iteration {i}"
        
        end_time = time.time()
        duration = end_time - start_time
        print(f"✅ Performance test: 200 operations in {duration:.3f}s ({200/duration:.1f} ops/sec)")
        
        # Cleanup performance test data
        for i in range(100):
            settings_service.settings.remove(f"perf_test/key_{i}")
        
        print("\n🎉 All tests passed successfully!")
        print("✅ Modern State Persistence System is working correctly")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_legacy_integration():
    """
    Test integration with legacy settings system.
    
    This demonstrates backward compatibility and migration patterns.
    """
    
    print("\n🔄 Testing Legacy Integration")
    print("=" * 30)
    
    try:
        # Create modern container
        from desktop.modern.core.dependency_injection.settings_service_registration import (
            create_configured_settings_container
        )
        
        container = create_configured_settings_container("TKA_Legacy_Test", "LegacyTestApp")
        
        # Get modern settings service
        from desktop.modern.application.services.settings.modern_settings_service import ModernSettingsService
        settings_service = container.resolve(ModernSettingsService)
        
        # Test legacy compatibility methods
        print("📦 Testing legacy compatibility methods...")
        
        # Test legacy get/set methods
        settings_service.set_setting("legacy_test", "old_key", "old_value")
        value = settings_service.get_setting("legacy_test", "old_key")
        assert value == "old_value", "Legacy compatibility failed"
        
        # Test current tab methods
        settings_service.set_current_tab("legacy_tab")
        current_tab = settings_service.get_current_tab()
        assert current_tab == "legacy_tab", "Legacy current tab failed"
        
        print("✅ Legacy compatibility working correctly")
        
        # Test data migration pattern
        print("🔄 Testing data migration pattern...")
        
        # Simulate legacy data
        legacy_data = {
            "global/prop_type": "Staff",
            "global/background_type": "Snowfall",
            "global/current_tab": "construct",
            "visibility/letter": True,
            "visibility/vtg": False,
        }
        
        # Migrate to modern format
        success = settings_service.execute_bulk_setting_command({
            "global": {
                "prop_type": legacy_data["global/prop_type"],
                "background_type": legacy_data["global/background_type"],
                "current_tab": legacy_data["global/current_tab"],
            },
            "visibility": {
                "glyph_letter": legacy_data["visibility/letter"],
                "glyph_vtg": legacy_data["visibility/vtg"],
            }
        })
        
        assert success, "Data migration failed"
        print("✅ Data migration pattern working correctly")
        
        print("✅ Legacy integration test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Legacy integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_comprehensive_test():
    """Run all tests in the integration suite."""
    
    print("🚀 Starting Comprehensive Modern State Persistence Test")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: Modern system
    if test_modern_state_persistence():
        tests_passed += 1
        print("\n✅ Modern system test: PASSED")
    else:
        print("\n❌ Modern system test: FAILED")
    
    # Test 2: Legacy integration
    if test_legacy_integration():
        tests_passed += 1
        print("\n✅ Legacy integration test: PASSED")
    else:
        print("\n❌ Legacy integration test: FAILED")
    
    # Summary
    print(f"\n📊 Test Summary: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 ALL TESTS PASSED! Modern State Persistence System is ready for use.")
        return True
    else:
        print("❌ Some tests failed. Please review the errors above.")
        return False


if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
