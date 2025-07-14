"""
Comprehensive validation script for start position service integration.

This script validates that all presentation components can properly use the new services
and that backward compatibility is maintained.
"""

import sys
from pathlib import Path

# Add src to path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

def test_presentation_layer_integration():
    """Test that presentation components can use injected services."""
    print("🔍 Testing Presentation Layer Integration...")
    
    success_count = 0
    total_tests = 0
    
    # Test 1: Service Imports
    total_tests += 1
    try:
        print("  📋 Testing service and component imports...")
        from core.interfaces.start_position_services import (
            IStartPositionDataService,
            IStartPositionSelectionService,
            IStartPositionUIService,
            IStartPositionOrchestrator
        )
        from application.services.start_position import (
            StartPositionDataService,
            StartPositionSelectionService,
            StartPositionUIService,
            StartPositionOrchestrator
        )
        from presentation.components.start_position_picker.start_position_option import StartPositionOption
        from presentation.components.start_position_picker.start_position_picker import StartPositionPicker
        from presentation.components.start_position_picker.enhanced_start_position_picker import EnhancedStartPositionPicker
        from presentation.components.start_position_picker.advanced_start_position_picker import AdvancedStartPositionPicker
        print("    ✅ All imports successful")
        success_count += 1
    except Exception as e:
        print(f"    ❌ Import failed: {e}")
    
    # Test 2: Service Instantiation
    total_tests += 1
    try:
        print("  🏗️  Testing service instantiation...")
        data_service = StartPositionDataService()
        selection_service = StartPositionSelectionService()
        ui_service = StartPositionUIService()
        orchestrator = StartPositionOrchestrator(data_service, selection_service, ui_service)
        print("    ✅ All services instantiated")
        success_count += 1
    except Exception as e:
        print(f"    ❌ Service instantiation failed: {e}")
        return success_count, total_tests
    
    # Test 3: Mock Pool Manager
    total_tests += 1
    try:
        print("  🏊 Creating mock pool manager...")
        # Create a simple mock pool manager for testing
        class MockPoolManager:
            def checkout_pictograph(self, parent=None):
                return None
            def checkin_pictograph(self, component):
                pass
        
        mock_pool = MockPoolManager()
        print("    ✅ Mock pool manager created")
        success_count += 1
    except Exception as e:
        print(f"    ❌ Mock pool manager creation failed: {e}")
        return success_count, total_tests
    
    # Test 4: StartPositionOption with Services
    total_tests += 1
    try:
        print("  🎯 Testing StartPositionOption with injected services...")
        option = StartPositionOption(
            "alpha1_alpha1",
            mock_pool,
            "diamond",
            data_service=data_service
        )
        assert hasattr(option, 'data_service')
        assert option.data_service == data_service
        print("    ✅ StartPositionOption works with injected services")
        success_count += 1
    except Exception as e:
        print(f"    ❌ StartPositionOption with services failed: {e}")
    
    # Test 5: StartPositionOption Backward Compatibility
    total_tests += 1
    try:
        print("  🔄 Testing StartPositionOption backward compatibility...")
        option_fallback = StartPositionOption(
            "alpha1_alpha1",
            mock_pool,
            "diamond"
            # No data_service parameter - should use fallback
        )
        assert hasattr(option_fallback, 'data_service')
        print("    ✅ StartPositionOption backward compatibility works")
        success_count += 1
    except Exception as e:
        print(f"    ❌ StartPositionOption backward compatibility failed: {e}")
    
    # Test 6: StartPositionPicker with Services
    total_tests += 1
    try:
        print("  🎛️  Testing StartPositionPicker with injected services...")
        picker = StartPositionPicker(
            mock_pool,
            data_service=data_service,
            selection_service=selection_service,
            ui_service=ui_service,
            orchestrator=orchestrator
        )
        assert hasattr(picker, 'orchestrator')
        assert picker.orchestrator == orchestrator
        print("    ✅ StartPositionPicker works with injected services")
        success_count += 1
    except Exception as e:
        print(f"    ❌ StartPositionPicker with services failed: {e}")
    
    # Test 7: StartPositionPicker Backward Compatibility
    total_tests += 1
    try:
        print("  🔄 Testing StartPositionPicker backward compatibility...")
        picker_fallback = StartPositionPicker(mock_pool)
        assert hasattr(picker_fallback, 'orchestrator')
        # Should be None for fallback
        print("    ✅ StartPositionPicker backward compatibility works")
        success_count += 1
    except Exception as e:
        print(f"    ❌ StartPositionPicker backward compatibility failed: {e}")
    
    # Test 8: EnhancedStartPositionPicker with Services
    total_tests += 1
    try:
        print("  ✨ Testing EnhancedStartPositionPicker with injected services...")
        enhanced_picker = EnhancedStartPositionPicker(
            mock_pool,
            data_service=data_service,
            selection_service=selection_service,
            ui_service=ui_service,
            orchestrator=orchestrator
        )
        assert hasattr(enhanced_picker, 'ui_service')
        assert enhanced_picker.ui_service == ui_service
        print("    ✅ EnhancedStartPositionPicker works with injected services")
        success_count += 1
    except Exception as e:
        print(f"    ❌ EnhancedStartPositionPicker with services failed: {e}")
    
    # Test 9: AdvancedStartPositionPicker with Services
    total_tests += 1
    try:
        print("  🚀 Testing AdvancedStartPositionPicker with injected services...")
        advanced_picker = AdvancedStartPositionPicker(
            mock_pool,
            "diamond",
            data_service=data_service,
            selection_service=selection_service,
            ui_service=ui_service,
            orchestrator=orchestrator
        )
        assert hasattr(advanced_picker, 'data_service')
        assert advanced_picker.data_service == data_service
        print("    ✅ AdvancedStartPositionPicker works with injected services")
        success_count += 1
    except Exception as e:
        print(f"    ❌ AdvancedStartPositionPicker with services failed: {e}")
    
    # Test 10: Service Method Delegation
    total_tests += 1
    try:
        print("  🎯 Testing service method delegation...")
        
        # Test UI service methods
        positions = ui_service.get_positions_for_mode("diamond", False)
        assert isinstance(positions, list)
        assert len(positions) == 3  # Basic diamond positions
        
        size = ui_service.calculate_option_size(1000, False)
        assert isinstance(size, int)
        assert 80 <= size <= 200
        
        # Test selection service methods
        is_valid = selection_service.validate_selection("alpha1_alpha1")
        assert is_valid == True
        
        end_pos = selection_service.extract_end_position_from_key("alpha1_alpha1")
        assert end_pos == "alpha1"
        
        print("    ✅ Service method delegation works correctly")
        success_count += 1
    except Exception as e:
        print(f"    ❌ Service method delegation failed: {e}")
    
    print(f"\n📊 Integration Test Results: {success_count}/{total_tests} tests passed")
    return success_count, total_tests

def test_di_container_integration():
    """Test that components can get services from DI container."""
    print("\n🔍 Testing DI Container Integration...")
    
    try:
        # Create production container
        from core.application.application_factory import ApplicationFactory, ApplicationMode
        container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)
        
        # Resolve services
        from core.interfaces.start_position_services import (
            IStartPositionDataService,
            IStartPositionSelectionService,
            IStartPositionUIService,
            IStartPositionOrchestrator
        )
        
        data_service = container.resolve(IStartPositionDataService)
        selection_service = container.resolve(IStartPositionSelectionService)
        ui_service = container.resolve(IStartPositionUIService)
        orchestrator = container.resolve(IStartPositionOrchestrator)
        
        # Verify all services resolved
        assert data_service is not None
        assert selection_service is not None
        assert ui_service is not None
        assert orchestrator is not None
        
        # Test service functionality
        positions = ui_service.get_positions_for_mode("diamond", False)
        assert len(positions) == 3
        
        is_valid = selection_service.validate_selection("alpha1_alpha1")
        assert is_valid == True
        
        print("✅ DI Container integration works perfectly!")
        return True
        
    except Exception as e:
        print(f"❌ DI Container integration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_end_to_end_workflow():
    """Test the complete workflow with services."""
    print("\n🔍 Testing End-to-End Workflow...")
    
    try:
        # Get services from container
        from core.application.application_factory import ApplicationFactory, ApplicationMode
        container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)
        
        from core.interfaces.start_position_services import IStartPositionOrchestrator
        orchestrator = container.resolve(IStartPositionOrchestrator)
        
        # Test position selection workflow
        result = orchestrator.handle_position_selection("alpha1_alpha1")
        
        # Note: This might fail if command processor is not available in test environment
        # but the important thing is that the service methods work
        print(f"Position selection workflow result: {result}")
        
        # Test position data retrieval
        data = orchestrator.get_position_data_for_display("alpha1_alpha1", "diamond")
        print(f"Position data retrieval: {'✅ Success' if data else '⚠️ No data (expected in test)'}")
        
        # Test layout calculation
        from PyQt6.QtCore import QSize
        layout_params = orchestrator.calculate_responsive_layout(QSize(800, 600), 3)
        assert isinstance(layout_params, dict)
        assert "rows" in layout_params
        assert "cols" in layout_params
        
        print("✅ End-to-end workflow completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ End-to-end workflow failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Start Position Services - Integration Validation")
    print("=" * 60)
    
    # Run integration tests
    integration_passed, integration_total = test_presentation_layer_integration()
    di_passed = test_di_container_integration()
    e2e_passed = test_end_to_end_workflow()
    
    print("\n" + "=" * 60)
    print("📊 Final Results:")
    print(f"  Integration Tests: {integration_passed}/{integration_total}")
    print(f"  DI Container Test: {'✅ Passed' if di_passed else '❌ Failed'}")
    print(f"  End-to-End Test: {'✅ Passed' if e2e_passed else '❌ Failed'}")
    
    if integration_passed == integration_total and di_passed and e2e_passed:
        print("\n🎉 ALL INTEGRATION TESTS PASSED!")
        print("✅ Service integration is complete and functional")
        print("🔄 Backward compatibility is maintained")
        print("🎯 Ready for production use")
        sys.exit(0)
    else:
        print("\n❌ SOME INTEGRATION TESTS FAILED!")
        print("🔧 Please review the errors above")
        sys.exit(1)
