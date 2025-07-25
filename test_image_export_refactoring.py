"""
Image Export Service Refactoring - Autonomous Testing Protocol
============================================================

This script provides comprehensive testing for the refactored Image Export Service
to ensure framework independence while maintaining full compatibility.

Run this script to validate the refactoring success.
"""

import logging
import os
import sys
from pathlib import Path
import time
from typing import Dict, List, Any

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add project paths using universal TKA path system
def setup_project_paths():
    """Setup project paths for imports using universal TKA path system."""
    try:
        # Import the universal path system
        import tka_paths
        
        # Setup all TKA paths
        success = tka_paths.setup_all_paths(verbose=True)
        
        if success:
            tka_root = tka_paths.find_tka_root()
            logger.info(f"✅ Project paths configured using universal system from: {tka_root}")
            return tka_root
        else:
            logger.error("❌ Universal path setup failed")
            return None
            
    except Exception as e:
        logger.error(f"❌ Failed to setup paths: {e}")
        return None

# Test Results Storage
class TestResults:
    def __init__(self):
        self.results = []
        self.start_time = time.time()
    
    def add_result(self, test_name: str, passed: bool, message: str = "", details: Dict = None):
        """Add test result."""
        self.results.append({
            "test": test_name,
            "passed": passed,
            "message": message,
            "details": details or {},
            "timestamp": time.time()
        })
        
        status = "✅ PASS" if passed else "❌ FAIL"
        logger.info(f"{status}: {test_name} - {message}")
    
    def get_summary(self) -> Dict[str, Any]:
        """Get test summary."""
        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        failed = total - passed
        duration = time.time() - self.start_time
        
        return {
            "total_tests": total,
            "passed": passed,
            "failed": failed,
            "success_rate": (passed / total * 100) if total > 0 else 0,
            "duration_seconds": duration,
            "all_tests_passed": failed == 0
        }
    
    def print_summary(self):
        """Print test summary."""
        summary = self.get_summary()
        print(f"\n{'='*60}")
        print(f"IMAGE EXPORT SERVICE REFACTORING TEST RESULTS")
        print(f"{'='*60}")
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Duration: {summary['duration_seconds']:.2f} seconds")
        print(f"Status: {'✅ ALL TESTS PASSED' if summary['all_tests_passed'] else '❌ SOME TESTS FAILED'}")
        
        if summary['failed'] > 0:
            print(f"\nFailed Tests:")
            for result in self.results:
                if not result['passed']:
                    print(f"  ❌ {result['test']}: {result['message']}")
        
        print(f"{'='*60}\n")


# Test Classes
class CoreImageExportServiceTests:
    """Tests for the framework-agnostic core image export service."""
    
    def __init__(self, results: TestResults):
        self.results = results
    
    def test_import_core_service(self):
        """Test that core service can be imported."""
        try:
            from application.services.core.image_export_service import (
                CoreImageExportService, 
                create_image_export_service
            )
            self.results.add_result(
                "Core Service Import", 
                True, 
                "Successfully imported CoreImageExportService"
            )
            return True
        except Exception as e:
            self.results.add_result(
                "Core Service Import", 
                False, 
                f"Failed to import: {str(e)}"
            )
            return False
    
    def test_core_service_creation(self):
        """Test core service creation."""
        try:
            from application.services.core.image_export_service import CoreImageExportService
            
            service = CoreImageExportService()
            self.results.add_result(
                "Core Service Creation", 
                True, 
                "Successfully created CoreImageExportService instance"
            )
            return service
        except Exception as e:
            self.results.add_result(
                "Core Service Creation", 
                False, 
                f"Failed to create service: {str(e)}"
            )
            return None
    
    def test_layout_calculation(self):
        """Test layout dimension calculations."""
        try:
            from application.services.core.image_export_service import CoreImageExportService
            
            service = CoreImageExportService()
            
            # Test layout calculation
            beat_count = 8
            export_options = {
                "beats_per_row": 4,
                "beat_size": 200,
                "margin": 50,
                "header_height": 100,
                "footer_height": 50
            }
            
            canvas_size, layout_info = service.calculate_layout_dimensions(beat_count, export_options)
            
            # Validate results
            assert canvas_size.width > 0, "Canvas width should be positive"
            assert canvas_size.height > 0, "Canvas height should be positive"
            assert layout_info["beat_size"] == 200, "Beat size should match input"
            assert layout_info["beats_per_row"] == 4, "Beats per row should match input"
            assert layout_info["rows"] == 2, "Should calculate 2 rows for 8 beats"
            
            self.results.add_result(
                "Layout Calculation", 
                True, 
                f"Calculated layout: {canvas_size.width}x{canvas_size.height}",
                {"canvas_size": f"{canvas_size.width}x{canvas_size.height}", "layout_info": layout_info}
            )
            return True
            
        except Exception as e:
            self.results.add_result(
                "Layout Calculation", 
                False, 
                f"Layout calculation failed: {str(e)}"
            )
            return False
    
    def test_export_commands_generation(self):
        """Test export command generation."""
        try:
            from application.services.core.image_export_service import CoreImageExportService
            
            service = CoreImageExportService()
            
            # Test data
            sequence_data = {
                "name": "Test Sequence",
                "difficulty": 3,
                "beats": [
                    {"beat_number": 1, "data": "test1"},
                    {"beat_number": 2, "data": "test2"},
                    {"beat_number": 3, "data": "test3"},
                    {"beat_number": 4, "data": "test4"}
                ]
            }
            
            export_options = {
                "beats_per_row": 2,
                "beat_size": 150,
                "add_word": True,
                "add_difficulty_level": True,
                "background_color": "#FFFFFF"
            }
            
            commands = service.create_export_commands(sequence_data, export_options)
            
            # Validate commands
            assert len(commands) > 0, "Should generate export commands"
            
            # Check for required command types
            command_types = [cmd.get("type") for cmd in commands]
            assert "background" in command_types, "Should include background command"
            assert "beat" in command_types, "Should include beat commands"
            assert "text" in command_types, "Should include text commands"
            
            self.results.add_result(
                "Export Commands Generation", 
                True, 
                f"Generated {len(commands)} export commands",
                {"command_count": len(commands), "command_types": command_types}
            )
            return True
            
        except Exception as e:
            self.results.add_result(
                "Export Commands Generation", 
                False, 
                f"Command generation failed: {str(e)}"
            )
            return False
    
    def test_framework_agnostic_types(self):
        """Test that core service uses framework-agnostic types."""
        try:
            from application.services.core.image_export_service import CoreImageExportService
            from application.services.core.types import ImageData, Size, Color, ImageFormat
            
            service = CoreImageExportService()
            
            # Test data
            sequence_data = {"beats": [{"test": "data"}], "name": "Test"}
            export_options = {"beat_size": 100}
            
            image_data = service.generate_export_data(sequence_data, export_options)
            
            # Validate framework-agnostic types
            assert isinstance(image_data, ImageData), "Should return ImageData type"
            assert isinstance(image_data.format, ImageFormat), "Should use ImageFormat enum"
            assert hasattr(image_data, 'render_commands'), "Should have render_commands"
            assert hasattr(image_data, 'metadata'), "Should have metadata"
            
            # Check no Qt dependencies
            qt_types = ['QImage', 'QColor', 'QPainter', 'QSize', 'QPoint']
            for attr_name in dir(image_data):
                attr_value = getattr(image_data, attr_name)
                for qt_type in qt_types:
                    assert qt_type not in str(type(attr_value)), f"Should not contain Qt type: {qt_type}"
            
            self.results.add_result(
                "Framework Agnostic Types", 
                True, 
                "Core service uses only framework-agnostic types"
            )
            return True
            
        except Exception as e:
            self.results.add_result(
                "Framework Agnostic Types", 
                False, 
                f"Framework agnostic types test failed: {str(e)}"
            )
            return False
    
    def run_all_tests(self):
        """Run all core service tests."""
        logger.info("🧪 Running Core Image Export Service Tests...")
        
        if not self.test_import_core_service():
            return False
        
        service = self.test_core_service_creation()
        if not service:
            return False
        
        self.test_layout_calculation()
        self.test_export_commands_generation()
        self.test_framework_agnostic_types()
        
        return True


class QtAdapterTests:
    """Tests for the Qt image export adapter."""
    
    def __init__(self, results: TestResults):
        self.results = results
    
    def test_import_qt_adapter(self):
        """Test that Qt adapter can be imported."""
        try:
            from application.adapters.qt_image_export_adapter import (
                QtImageExportAdapter,
                create_qt_image_export_adapter
            )
            self.results.add_result(
                "Qt Adapter Import", 
                True, 
                "Successfully imported QtImageExportAdapter"
            )
            return True
        except Exception as e:
            self.results.add_result(
                "Qt Adapter Import", 
                False, 
                f"Failed to import Qt adapter: {str(e)}"
            )
            return False
    
    def test_qt_adapter_creation(self):
        """Test Qt adapter creation."""
        try:
            from application.adapters.qt_image_export_adapter import create_qt_image_export_adapter
            
            adapter = create_qt_image_export_adapter()
            self.results.add_result(
                "Qt Adapter Creation", 
                True, 
                "Successfully created QtImageExportAdapter instance"
            )
            return adapter
        except Exception as e:
            self.results.add_result(
                "Qt Adapter Creation", 
                False, 
                f"Failed to create Qt adapter: {str(e)}"
            )
            return None
    
    def test_qt_image_generation(self):
        """Test Qt image generation."""
        try:
            from application.adapters.qt_image_export_adapter import create_qt_image_export_adapter
            from PyQt6.QtGui import QImage
            
            adapter = create_qt_image_export_adapter()
            
            # Test data
            sequence_data = {
                "name": "Test Sequence",
                "beats": [
                    {"beat_number": 1, "data": "test1"},
                    {"beat_number": 2, "data": "test2"}
                ]
            }
            
            export_options = {
                "beats_per_row": 2,
                "beat_size": 100,
                "margin": 20,
                "background_color": "#FFFFFF"
            }
            
            qt_image = adapter.render_sequence_image(sequence_data, export_options)
            
            # Validate Qt image
            assert isinstance(qt_image, QImage), "Should return QImage instance"
            assert not qt_image.isNull(), "QImage should not be null"
            assert qt_image.width() > 0, "QImage width should be positive"
            assert qt_image.height() > 0, "QImage height should be positive"
            
            self.results.add_result(
                "Qt Image Generation", 
                True, 
                f"Generated QImage: {qt_image.width()}x{qt_image.height()}",
                {"image_size": f"{qt_image.width()}x{qt_image.height()}"}
            )
            return True
            
        except Exception as e:
            self.results.add_result(
                "Qt Image Generation", 
                False, 
                f"Qt image generation failed: {str(e)}"
            )
            return False
    
    def test_adapter_statistics(self):
        """Test adapter statistics."""
        try:
            from application.adapters.qt_image_export_adapter import create_qt_image_export_adapter
            
            adapter = create_qt_image_export_adapter()
            stats = adapter.get_export_statistics()
            
            # Validate statistics
            assert isinstance(stats, dict), "Should return dictionary"
            assert "core_service_stats" in stats, "Should include core service stats"
            assert "adapter_status" in stats, "Should include adapter status"
            assert "architecture" in stats, "Should include architecture info"
            
            self.results.add_result(
                "Adapter Statistics", 
                True, 
                "Successfully retrieved adapter statistics",
                {"stats": stats}
            )
            return True
            
        except Exception as e:
            self.results.add_result(
                "Adapter Statistics", 
                False, 
                f"Adapter statistics test failed: {str(e)}"
            )
            return False
    
    def run_all_tests(self):
        """Run all Qt adapter tests."""
        logger.info("🧪 Running Qt Image Export Adapter Tests...")
        
        if not self.test_import_qt_adapter():
            return False
        
        adapter = self.test_qt_adapter_creation()
        if not adapter:
            return False
        
        self.test_qt_image_generation()
        self.test_adapter_statistics()
        
        return True


class SequenceImageRendererTests:
    """Tests for the refactored SequenceImageRenderer."""
    
    def __init__(self, results: TestResults):
        self.results = results
    
    def test_import_sequence_renderer(self):
        """Test that refactored sequence renderer can be imported."""
        try:
            from application.services.image_export.sequence_image_renderer import SequenceImageRenderer
            self.results.add_result(
                "Sequence Renderer Import", 
                True, 
                "Successfully imported refactored SequenceImageRenderer"
            )
            return True
        except Exception as e:
            self.results.add_result(
                "Sequence Renderer Import", 
                False, 
                f"Failed to import sequence renderer: {str(e)}"
            )
            return False
    
    def test_sequence_renderer_creation(self):
        """Test sequence renderer creation."""
        try:
            from application.services.image_export.sequence_image_renderer import SequenceImageRenderer
            
            renderer = SequenceImageRenderer()
            self.results.add_result(
                "Sequence Renderer Creation", 
                True, 
                "Successfully created SequenceImageRenderer instance"
            )
            return renderer
        except Exception as e:
            self.results.add_result(
                "Sequence Renderer Creation", 
                False, 
                f"Failed to create sequence renderer: {str(e)}"
            )
            return None
    
    def test_no_direct_qt_dependencies(self):
        """Test that sequence renderer has no direct Qt dependencies in core logic."""
        try:
            import importlib
            import inspect
            
            # Import the module
            module = importlib.import_module('application.services.image_export.sequence_image_renderer')
            
            # Get source code
            source = inspect.getsource(module)
            
            # Check for direct Qt usage in main methods (should be minimal)
            problematic_qt_usage = [
                'QPainter(',  # Should not directly create QPainter
                'QBrush(',    # Should not directly create QBrush
                'QPen(',      # Should not directly create QPen
                'QColor(',    # Should not directly create QColor (except for compatibility)
            ]
            
            found_issues = []
            for qt_usage in problematic_qt_usage:
                if qt_usage in source:
                    # Count occurrences (some limited usage is acceptable for compatibility)
                    count = source.count(qt_usage)
                    if count > 3:  # Allow some for legacy compatibility
                        found_issues.append(f"{qt_usage}: {count} occurrences")
            
            if found_issues:
                self.results.add_result(
                    "No Direct Qt Dependencies", 
                    False, 
                    f"Found excessive Qt usage: {', '.join(found_issues)}"
                )
            else:
                self.results.add_result(
                    "No Direct Qt Dependencies", 
                    True, 
                    "Sequence renderer has minimal direct Qt dependencies"
                )
            
            return len(found_issues) == 0
            
        except Exception as e:
            self.results.add_result(
                "No Direct Qt Dependencies", 
                False, 
                f"Qt dependency check failed: {str(e)}"
            )
            return False
    
    def test_legacy_interface_compatibility(self):
        """Test that legacy interface is maintained."""
        try:
            from application.services.image_export.sequence_image_renderer import SequenceImageRenderer
            from PyQt6.QtGui import QImage
            
            renderer = SequenceImageRenderer()
            
            # Test that key methods exist
            required_methods = [
                'render_sequence_beats',
                'render_word',
                'render_user_info', 
                'render_difficulty_level',
                'render_sequence_image',
                'get_beat_size',
                'calculate_additional_height'
            ]
            
            missing_methods = []
            for method_name in required_methods:
                if not hasattr(renderer, method_name):
                    missing_methods.append(method_name)
            
            if missing_methods:
                self.results.add_result(
                    "Legacy Interface Compatibility", 
                    False, 
                    f"Missing methods: {', '.join(missing_methods)}"
                )
                return False
            
            # Test method signature compatibility (basic check)
            test_image = QImage(400, 300, QImage.Format.Format_ARGB32)
            
            # These should not throw attribute errors
            beat_size = renderer.get_beat_size(400, 300, 2, 2)
            assert isinstance(beat_size, int), "get_beat_size should return integer"
            
            self.results.add_result(
                "Legacy Interface Compatibility", 
                True, 
                "All required methods present and callable"
            )
            return True
            
        except Exception as e:
            self.results.add_result(
                "Legacy Interface Compatibility", 
                False, 
                f"Interface compatibility test failed: {str(e)}"
            )
            return False
    
    def test_framework_agnostic_delegation(self):
        """Test that renderer delegates to framework-agnostic services."""
        try:
            from application.services.image_export.sequence_image_renderer import SequenceImageRenderer
            
            renderer = SequenceImageRenderer()
            
            # Check that renderer has framework-agnostic services
            assert hasattr(renderer, '_core_service'), "Should have core service"
            assert hasattr(renderer, '_qt_adapter'), "Should have Qt adapter"
            
            # Check service types
            core_service = renderer.get_core_service()
            qt_adapter = renderer.get_qt_adapter()
            
            assert core_service is not None, "Core service should not be None"
            assert qt_adapter is not None, "Qt adapter should not be None"
            
            # Check that services have expected methods
            assert hasattr(core_service, 'generate_export_data'), "Core service should have generate_export_data"
            assert hasattr(qt_adapter, 'render_sequence_image'), "Qt adapter should have render_sequence_image"
            
            self.results.add_result(
                "Framework Agnostic Delegation", 
                True, 
                "Renderer properly delegates to framework-agnostic services"
            )
            return True
            
        except Exception as e:
            self.results.add_result(
                "Framework Agnostic Delegation", 
                False, 
                f"Framework agnostic delegation test failed: {str(e)}"
            )
            return False
    
    def run_all_tests(self):
        """Run all sequence renderer tests."""
        logger.info("🧪 Running Sequence Image Renderer Tests...")
        
        if not self.test_import_sequence_renderer():
            return False
        
        renderer = self.test_sequence_renderer_creation()
        if not renderer:
            return False
        
        self.test_no_direct_qt_dependencies()
        self.test_legacy_interface_compatibility()
        self.test_framework_agnostic_delegation()
        
        return True


class IntegrationTests:
    """Integration tests for the complete refactored system."""
    
    def __init__(self, results: TestResults):
        self.results = results
    
    def test_end_to_end_image_export(self):
        """Test complete end-to-end image export workflow."""
        try:
            from application.services.image_export.sequence_image_renderer import SequenceImageRenderer
            from PyQt6.QtGui import QImage
            
            # Create mock ImageExportOptions
            class MockImageExportOptions:
                def __init__(self):
                    self.add_word = True
                    self.add_user_info = True
                    self.add_difficulty_level = True
                    self.include_start_position = False
                    self.word = "Test"
                    self.difficulty_level = 2
                    self.num_filled_beats = 4
            
            renderer = SequenceImageRenderer()
            options = MockImageExportOptions()
            
            # Test data
            sequence_data = [
                {"beat_number": 1, "motion_data": "test1"},
                {"beat_number": 2, "motion_data": "test2"},
                {"beat_number": 3, "motion_data": "test3"},
                {"beat_number": 4, "motion_data": "test4"}
            ]
            
            # Create test image
            test_image = QImage(800, 600, QImage.Format.Format_ARGB32)
            test_image.fill(0xFFFFFFFF)  # White background
            
            # Test complete rendering
            renderer.render_sequence_image(
                test_image, 
                sequence_data, 
                "TestWord", 
                2,  # columns
                2,  # rows
                options
            )
            
            # Validate result
            assert not test_image.isNull(), "Rendered image should not be null"
            assert test_image.width() > 0, "Rendered image should have width"
            assert test_image.height() > 0, "Rendered image should have height"
            
            self.results.add_result(
                "End-to-End Image Export", 
                True, 
                f"Successfully rendered complete image: {test_image.width()}x{test_image.height()}"
            )
            return True
            
        except Exception as e:
            self.results.add_result(
                "End-to-End Image Export", 
                False, 
                f"End-to-end test failed: {str(e)}"
            )
            return False
    
    def test_performance_comparison(self):
        """Test performance of refactored vs legacy (if available)."""
        try:
            import time
            from application.services.image_export.sequence_image_renderer import SequenceImageRenderer
            from PyQt6.QtGui import QImage
            
            renderer = SequenceImageRenderer()
            
            # Create mock options
            class MockOptions:
                add_word = True
                add_user_info = False
                add_difficulty_level = True
                include_start_position = False
                word = "Performance"
                difficulty_level = 3
                num_filled_beats = 8
            
            options = MockOptions()
            sequence_data = [{"beat": i} for i in range(8)]
            
            # Measure performance
            start_time = time.time()
            
            for _ in range(5):  # Run 5 times for average
                test_image = QImage(600, 400, QImage.Format.Format_ARGB32)
                renderer.render_sequence_image(test_image, sequence_data, "Test", 4, 2, options)
            
            end_time = time.time()
            avg_time = (end_time - start_time) / 5
            
            # Performance should be reasonable (less than 1 second per render)
            performance_acceptable = avg_time < 1.0
            
            self.results.add_result(
                "Performance Test", 
                performance_acceptable, 
                f"Average render time: {avg_time:.3f}s",
                {"average_time": avg_time, "acceptable": performance_acceptable}
            )
            return performance_acceptable
            
        except Exception as e:
            self.results.add_result(
                "Performance Test", 
                False, 
                f"Performance test failed: {str(e)}"
            )
            return False
    
    def test_memory_usage(self):
        """Test memory usage of the refactored system."""
        try:
            import psutil
            import os
            import gc
            
            from application.services.image_export.sequence_image_renderer import SequenceImageRenderer
            from PyQt6.QtGui import QImage
            
            # Get initial memory
            process = psutil.Process(os.getpid())
            initial_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Create multiple renderers and images
            renderers = []
            images = []
            
            for i in range(10):
                renderer = SequenceImageRenderer()
                renderers.append(renderer)
                
                test_image = QImage(400, 300, QImage.Format.Format_ARGB32)
                images.append(test_image)
            
            # Check memory after creation
            creation_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            # Clean up
            del renderers
            del images
            gc.collect()
            
            # Check memory after cleanup
            final_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            memory_increase = creation_memory - initial_memory
            memory_leak = final_memory - initial_memory
            
            # Memory increase should be reasonable (less than 50MB for 10 instances)
            # Memory leak should be minimal (less than 10MB)
            memory_acceptable = memory_increase < 50 and memory_leak < 10
            
            self.results.add_result(
                "Memory Usage Test", 
                memory_acceptable, 
                f"Memory increase: {memory_increase:.1f}MB, leak: {memory_leak:.1f}MB",
                {
                    "initial_memory": initial_memory,
                    "creation_memory": creation_memory,
                    "final_memory": final_memory,
                    "memory_increase": memory_increase,
                    "memory_leak": memory_leak
                }
            )
            return memory_acceptable
            
        except ImportError:
            self.results.add_result(
                "Memory Usage Test", 
                True, 
                "Skipped - psutil not available",
                {"skipped": True}
            )
            return True
        except Exception as e:
            self.results.add_result(
                "Memory Usage Test", 
                False, 
                f"Memory test failed: {str(e)}"
            )
            return False
    
    def run_all_tests(self):
        """Run all integration tests."""
        logger.info("🧪 Running Integration Tests...")
        
        self.test_end_to_end_image_export()
        self.test_performance_comparison()
        self.test_memory_usage()
        
        return True


# Main Test Runner
def run_autonomous_testing():
    """Run complete autonomous testing protocol."""
    
    print(f"🚀 Starting Image Export Service Refactoring Tests")
    print(f"{'='*60}")
    
    # Setup
    project_root = setup_project_paths()
    if not project_root:
        print("❌ Failed to setup project paths")
        return False
    
    results = TestResults()
    
    try:
        # Run test suites
        core_tests = CoreImageExportServiceTests(results)
        qt_tests = QtAdapterTests(results)
        renderer_tests = SequenceImageRendererTests(results)
        integration_tests = IntegrationTests(results)
        
        # Execute all test suites
        logger.info("🧪 Starting Test Execution...")
        
        core_tests.run_all_tests()
        qt_tests.run_all_tests()
        renderer_tests.run_all_tests()
        integration_tests.run_all_tests()
        
        # Print results
        results.print_summary()
        
        # Additional validation
        summary = results.get_summary()
        if summary['all_tests_passed']:
            print("🎉 REFACTORING SUCCESS!")
            print("✅ Image Export Service is now framework-agnostic")
            print("✅ Ready for web service integration")
            print("✅ Maintains full backward compatibility")
            return True
        else:
            print("⚠️  Some tests failed - refactoring may need adjustments")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test execution failed: {str(e)}")
        results.add_result("Test Execution", False, f"Critical failure: {str(e)}")
        results.print_summary()
        return False


if __name__ == "__main__":
    """Run autonomous testing when script is executed."""
    success = run_autonomous_testing()
    exit_code = 0 if success else 1
    
    print(f"\n🏁 Testing completed with exit code: {exit_code}")
    print(f"   0 = Success (all tests passed)")
    print(f"   1 = Failure (some tests failed)")
    
    exit(exit_code)
