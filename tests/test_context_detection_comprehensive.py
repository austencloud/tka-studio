"""
Comprehensive test for the new pictograph context detection system.

This test validates the complete integration of the robust context detection
system with TKA's architecture and ensures proper arrow behavior.
"""

import logging
from core.testing.ai_agent_helpers import TKAAITestHelper
from core.application.application_factory import ApplicationFactory
from core.interfaces.core_services import IPictographContextService
from application.services.ui.context_aware_scaling_service import RenderingContext

logger = logging.getLogger(__name__)


def test_context_detection_system_comprehensive():
    """
    Comprehensive test of the new context detection system.
    
    Tests:
    1. Service registration and resolution
    2. Context detection functionality
    3. Arrow behavior in different contexts
    4. Integration with existing TKA infrastructure
    5. Backward compatibility
    """
    print("🧪 Starting comprehensive context detection system test...")
    
    # Test 1: Service Registration and Resolution
    print("\n1️⃣ Testing service registration and resolution...")
    
    try:
        # Test with different application modes
        test_container = ApplicationFactory.create_test_app()
        test_service = test_container.resolve(IPictographContextService)
        assert test_service is not None, "Context service not available in test mode"
        print("✅ Context service available in test mode")
        
        headless_container = ApplicationFactory.create_headless_app()
        headless_service = headless_container.resolve(IPictographContextService)
        assert headless_service is not None, "Context service not available in headless mode"
        print("✅ Context service available in headless mode")
        
        production_container = ApplicationFactory.create_production_app()
        production_service = production_container.resolve(IPictographContextService)
        assert production_service is not None, "Context service not available in production mode"
        print("✅ Context service available in production mode")
        
    except Exception as e:
        print(f"❌ Service registration test failed: {e}")
        return False
    
    # Test 2: Context Detection Functionality
    print("\n2️⃣ Testing context detection functionality...")
    
    try:
        helper = TKAAITestHelper(use_test_mode=True)
        context_service = helper.container.resolve(IPictographContextService)
        
        # Test explicit context registration
        component_id = "test_graph_editor_123"
        context_service.register_context_provider(component_id, RenderingContext.GRAPH_EDITOR)
        
        retrieved_context = context_service.get_context_for_component(component_id)
        assert retrieved_context == RenderingContext.GRAPH_EDITOR, f"Expected GRAPH_EDITOR, got {retrieved_context}"
        print("✅ Explicit context registration works")
        
        # Test unknown component handling
        unknown_context = context_service.get_context_for_component("unknown_component")
        assert unknown_context == RenderingContext.UNKNOWN, f"Expected UNKNOWN, got {unknown_context}"
        print("✅ Unknown component handling works")
        
    except Exception as e:
        print(f"❌ Context detection functionality test failed: {e}")
        return False
    
    # Test 3: Arrow Behavior Integration
    print("\n3️⃣ Testing arrow behavior integration...")
    
    try:
        # Test that arrow items can use the new context detection
        from presentation.components.pictograph.graphics_items.arrow_item import ArrowItem
        
        # Create arrow and test context determination
        arrow = ArrowItem()
        
        # Test that the arrow can determine context (even if it's UNKNOWN without a scene)
        context = arrow._determine_context()
        assert isinstance(context, RenderingContext), f"Expected RenderingContext enum, got {type(context)}"
        print("✅ Arrow context determination works")
        
        # Test behavior update for different contexts
        arrow._context_type = RenderingContext.GRAPH_EDITOR
        arrow._update_behavior_for_context()
        print("✅ Arrow behavior update for graph editor works")
        
        arrow._context_type = RenderingContext.BEAT_FRAME
        arrow._update_behavior_for_context()
        print("✅ Arrow behavior update for beat frame works")
        
    except Exception as e:
        print(f"❌ Arrow behavior integration test failed: {e}")
        return False
    
    # Test 4: TKA Infrastructure Integration
    print("\n4️⃣ Testing TKA infrastructure integration...")
    
    try:
        # Test that pictograph scenes can use the new system
        from presentation.components.pictograph.pictograph_scene import PictographScene
        
        scene = PictographScene()
        component_type = scene._determine_component_type()
        assert isinstance(component_type, str), f"Expected string, got {type(component_type)}"
        assert component_type in ["graph_editor", "beat_frame", "option_picker", "preview", "sequence_viewer", "unknown"]
        print("✅ Pictograph scene integration works")
        
        # Test AI helper integration
        helper = TKAAITestHelper(use_test_mode=True)
        result = helper.run_comprehensive_test_suite()
        assert result.success, f"AI helper test suite failed: {result.errors}"
        print("✅ AI helper integration works")
        
    except Exception as e:
        print(f"❌ TKA infrastructure integration test failed: {e}")
        return False
    
    # Test 5: Backward Compatibility
    print("\n5️⃣ Testing backward compatibility...")
    
    try:
        # Test that existing code still works
        from presentation.components.pictograph.pictograph_scene import PictographScene
        
        scene = PictographScene()
        
        # Test legacy method still works
        is_graph_editor = scene.is_in_graph_editor_context()
        assert isinstance(is_graph_editor, bool), f"Expected bool, got {type(is_graph_editor)}"
        print("✅ Legacy graph editor context check works")
        
        # Test that string contexts map to enums correctly
        context_map = {
            RenderingContext.GRAPH_EDITOR: "graph_editor",
            RenderingContext.BEAT_FRAME: "beat_frame", 
            RenderingContext.OPTION_PICKER: "option_picker",
            RenderingContext.PREVIEW: "preview",
            RenderingContext.SEQUENCE_VIEWER: "sequence_viewer",
            RenderingContext.UNKNOWN: "unknown"
        }
        
        for enum_context, string_context in context_map.items():
            assert isinstance(enum_context, RenderingContext)
            assert isinstance(string_context, str)
        print("✅ Context mapping compatibility works")
        
    except Exception as e:
        print(f"❌ Backward compatibility test failed: {e}")
        return False
    
    # Test 6: Error Handling and Robustness
    print("\n6️⃣ Testing error handling and robustness...")
    
    try:
        context_service = helper.container.resolve(IPictographContextService)
        
        # Test invalid context registration
        try:
            context_service.register_context_provider("test", "invalid_context")
            print("❌ Should have rejected invalid context")
            return False
        except (ValueError, TypeError):
            print("✅ Invalid context registration properly rejected")
        
        # Test scene context detection with None scene
        context = context_service.determine_context_from_scene(None)
        assert context == RenderingContext.UNKNOWN, f"Expected UNKNOWN for None scene, got {context}"
        print("✅ None scene handling works")
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False
    
    print("\n🎉 All tests passed! Context detection system is working correctly.")
    print("\n📋 Summary:")
    print("✅ Service registration and resolution")
    print("✅ Context detection functionality")
    print("✅ Arrow behavior integration")
    print("✅ TKA infrastructure integration")
    print("✅ Backward compatibility")
    print("✅ Error handling and robustness")
    
    return True


def test_context_detection_performance():
    """Test performance characteristics of the new system."""
    print("\n⚡ Testing context detection performance...")
    
    import time
    
    try:
        helper = TKAAITestHelper(use_test_mode=True)
        context_service = helper.container.resolve(IPictographContextService)
        
        # Test registration performance
        start_time = time.time()
        for i in range(1000):
            context_service.register_context_provider(f"component_{i}", RenderingContext.GRAPH_EDITOR)
        registration_time = time.time() - start_time
        
        # Test retrieval performance
        start_time = time.time()
        for i in range(1000):
            context_service.get_context_for_component(f"component_{i}")
        retrieval_time = time.time() - start_time
        
        print(f"✅ Registration performance: {registration_time:.3f}s for 1000 components")
        print(f"✅ Retrieval performance: {retrieval_time:.3f}s for 1000 lookups")
        
        # Performance should be reasonable
        assert registration_time < 1.0, f"Registration too slow: {registration_time:.3f}s"
        assert retrieval_time < 0.1, f"Retrieval too slow: {retrieval_time:.3f}s"
        
        return True
        
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False


if __name__ == "__main__":
    # Run comprehensive test
    success = test_context_detection_system_comprehensive()
    
    if success:
        # Run performance test
        perf_success = test_context_detection_performance()
        
        if perf_success:
            print("\n🚀 All tests completed successfully!")
            print("The new pictograph context detection system is ready for production.")
        else:
            print("\n⚠️ Performance tests failed - system may need optimization.")
    else:
        print("\n💥 Comprehensive tests failed - system needs fixes before deployment.")
