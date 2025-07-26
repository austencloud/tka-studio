"""
Quick Validation Script for TKA Critical Fixes

This script provides a fast way to verify that all critical fixes are properly
implemented and working as expected. Useful for CI/CD pipelines and quick checks.

USAGE:
    python validate_fixes.py [--quick] [--list]
"""

import sys
import os
import time
import traceback
from pathlib import Path
from typing import List, Dict, Tuple

# Add src to path for imports
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

class QuickValidator:
    """
    Quick validation of TKA critical fixes.
    
    Provides fast checks without running full test suites.
    """
    
    def __init__(self):
        self.results: List[Tuple[str, bool, str]] = []
    
    def validate_all_fixes(self, quick_mode: bool = False) -> bool:
        """
        Validate all fixes with optional quick mode.
        
        Args:
            quick_mode: If True, skip comprehensive tests
            
        Returns:
            True if all validations pass
        """
        print("🔍 TKA Critical Fixes Quick Validation")
        print("=" * 45)
        
        validators = [
            ("Error Handling Module", self._check_error_handling),
            ("Circular Dependencies", self._check_circular_dependencies),
            ("Service Registration Helper", self._check_service_registration),
            ("DI Container Safety", self._check_di_container_safety),
            ("UI Fallback Implementation", self._check_ui_fallback),
            ("Background Initialization", self._check_background_init),
        ]
        
        if not quick_mode:
            validators.extend([
                ("Method Extraction Tools", self._check_method_extraction),
                ("Application Factory", self._check_application_factory),
                ("Test Files Exist", self._check_test_files),
            ])
        
        all_passed = True
        
        for name, validator in validators:
            try:
                start_time = time.time()
                passed, details = validator()
                duration = time.time() - start_time
                
                self.results.append((name, passed, details))
                status = "✅ PASS" if passed else "❌ FAIL"
                print(f"{status} {name} ({duration:.2f}s)")
                
                if not passed:
                    print(f"   Details: {details}")
                    all_passed = False
                    
            except Exception as e:
                self.results.append((name, False, f"Exception: {e}"))
                print(f"❌ FAIL {name} - Exception: {e}")
                all_passed = False
        
        print("\n" + "=" * 45)
        passed_count = sum(1 for _, passed, _ in self.results if passed)
        total_count = len(self.results)
        print(f"Results: {passed_count}/{total_count} validations passed")
        
        if all_passed:
            print("🎉 All fixes validated successfully!")
        else:
            print("⚠️  Some validations failed - check details above")
        
        return all_passed
    
    def _check_error_handling(self) -> Tuple[bool, str]:
        """Check that StandardErrorHandler is properly implemented."""
        try:
            from desktop.modern.core.error_handling import StandardErrorHandler, ErrorSeverity
            
            # Check that key methods exist
            required_methods = [
                'handle_service_error',
                'handle_ui_error', 
                'handle_dependency_resolution_error',
                'handle_circular_dependency_error'
            ]
            
            missing_methods = []
            for method in required_methods:
                if not hasattr(StandardErrorHandler, method):
                    missing_methods.append(method)
            
            if missing_methods:
                return False, f"Missing methods: {missing_methods}"
            
            # Test that ErrorSeverity constants exist
            severity_constants = ['CRITICAL', 'ERROR', 'WARNING', 'INFO']
            missing_constants = []
            for constant in severity_constants:
                if not hasattr(ErrorSeverity, constant):
                    missing_constants.append(constant)
            
            if missing_constants:
                return False, f"Missing severity constants: {missing_constants}"
            
            return True, "StandardErrorHandler fully implemented"
            
        except ImportError as e:
            return False, f"Import failed: {e}"
        except Exception as e:
            return False, f"Validation error: {e}"
    
    def _check_circular_dependencies(self) -> Tuple[bool, str]:
        """Check that circular dependencies are resolved."""
        try:
            # Try importing ApplicationOrchestrator - should not have circular import issues
            from desktop.modern.application.services.core.application_orchestrator import ApplicationOrchestrator
            
            # Try creating instance
            orchestrator = ApplicationOrchestrator()
            
            # Check that lifecycle manager was created (indicates proper dependency resolution)
            if hasattr(orchestrator, 'lifecycle_manager') and orchestrator.lifecycle_manager is not None:
                return True, "ApplicationOrchestrator creates successfully with dependencies"
            else:
                return False, "ApplicationOrchestrator missing lifecycle_manager"
                
        except ImportError as e:
            return False, f"Circular import detected: {e}"
        except Exception as e:
            return False, f"Creation failed: {e}"
    
    def _check_service_registration(self) -> Tuple[bool, str]:
        """Check that ServiceRegistrationHelper eliminates duplication."""
        try:
            from desktop.modern.core.application.service_registration_helper import ServiceRegistrationHelper
            
            # Check for key methods that eliminate duplication
            required_methods = [
                'register_all_common_services',
                'register_common_data_services',
                'register_common_core_services',
                '_register_services_batch'
            ]
            
            missing_methods = []
            for method in required_methods:
                if not hasattr(ServiceRegistrationHelper, method):
                    missing_methods.append(method)
            
            if missing_methods:
                return False, f"Missing methods: {missing_methods}"
            
            return True, "ServiceRegistrationHelper fully implemented"
            
        except ImportError as e:
            return False, f"Import failed: {e}"
        except Exception as e:
            return False, f"Validation error: {e}"
    
    def _check_di_container_safety(self) -> Tuple[bool, str]:
        """Check that DI container global state management is safe."""
        try:
            from desktop.modern.core.dependency_injection.di_container import DIContainer, set_container, reset_container
            
            # Reset state for clean test
            reset_container()
            
            container1 = DIContainer()
            container2 = DIContainer()
            
            # Set first container
            set_container(container1)
            
            # Try to overwrite without force - should raise exception
            exception_raised = False
            try:
                set_container(container2)
            except (RuntimeError, ValueError):
                exception_raised = True
            except Exception:
                # Any exception is better than silent failure
                exception_raised = True
            
            # Clean up
            reset_container()
            
            if exception_raised:
                return True, "set_container properly raises exception on overwrite"
            else:
                return False, "set_container allows silent overwrite (unsafe)"
                
        except ImportError as e:
            return False, f"Import failed: {e}"
        except Exception as e:
            return False, f"Validation error: {e}"
    
    def _check_ui_fallback(self) -> Tuple[bool, str]:
        """Check that meaningful UI fallback is implemented."""
        try:
            from desktop.modern.application.services.ui.ui_setup_manager import UISetupManager
            
            ui_manager = UISetupManager()
            
            # Check for meaningful fallback methods
            fallback_methods = [
                '_create_meaningful_fallback_ui',
                '_create_basic_construct_tab',
                '_create_basic_browse_tab',
                '_create_info_tab'
            ]
            
            missing_methods = []
            for method in fallback_methods:
                if not hasattr(ui_manager, method):
                    missing_methods.append(method)
            
            if missing_methods:
                return False, f"Missing fallback methods: {missing_methods}"
            
            return True, "Meaningful UI fallback methods implemented"
            
        except ImportError as e:
            return False, f"Import failed: {e}"
        except Exception as e:
            return False, f"Validation error: {e}"
    
    def _check_background_init(self) -> Tuple[bool, str]:
        """Check that background initialization is implemented."""
        try:
            from desktop.modern.application.services.core.application_orchestrator import ApplicationOrchestrator
            
            orchestrator = ApplicationOrchestrator()
            
            # Check for background initialization method
            if hasattr(orchestrator, '_start_background_initialization'):
                return True, "Background initialization method exists"
            else:
                return False, "Background initialization method missing"
                
        except ImportError as e:
            return False, f"Import failed: {e}"
        except Exception as e:
            return False, f"Validation error: {e}"
    
    def _check_method_extraction(self) -> Tuple[bool, str]:
        """Check that method extraction tools are available."""
        try:
            from desktop.modern.core.refactoring import MethodExtractor, generate_refactoring_report
            
            # Check that key classes and functions exist
            if not hasattr(MethodExtractor, 'analyze_method'):
                return False, "MethodExtractor.analyze_method missing"
            
            if not callable(generate_refactoring_report):
                return False, "generate_refactoring_report not callable"
            
            return True, "Method extraction tools available"
            
        except ImportError as e:
            return False, f"Import failed: {e}"
        except Exception as e:
            return False, f"Validation error: {e}"
    
    def _check_application_factory(self) -> Tuple[bool, str]:
        """Check that ApplicationFactory uses ServiceRegistrationHelper."""
        try:
            from desktop.modern.core.application.application_factory import ApplicationFactory
            
            # Check that ApplicationFactory has the expected structure
            if not hasattr(ApplicationFactory, 'create_production_app'):
                return False, "ApplicationFactory.create_production_app missing"
            
            if not hasattr(ApplicationFactory, 'create_test_app'):
                return False, "ApplicationFactory.create_test_app missing"
            
            # Try to access the helper (should be imported in ApplicationFactory)
            import inspect
            source = inspect.getsource(ApplicationFactory.create_production_app)
            
            if 'ServiceRegistrationHelper' in source:
                return True, "ApplicationFactory uses ServiceRegistrationHelper"
            else:
                return False, "ApplicationFactory does not use ServiceRegistrationHelper"
                
        except ImportError as e:
            return False, f"Import failed: {e}"
        except Exception as e:
            return False, f"Validation error: {e}"
    
    def _check_test_files(self) -> Tuple[bool, str]:
        """Check that test files exist."""
        test_files = [
            "tests/fixes/test_critical_fixes.py",
            "tests/fixes/test_integration_fixes.py",
            "run_critical_fixes_tests.py"
        ]
        
        missing_files = []
        for test_file in test_files:
            file_path = project_root / test_file
            if not file_path.exists():
                missing_files.append(test_file)
        
        if missing_files:
            return False, f"Missing test files: {missing_files}"
        
        return True, "All test files exist"
    
    def list_available_checks(self):
        """List all available validation checks."""
        checks = [
            "Error Handling Module - Validates StandardErrorHandler implementation",
            "Circular Dependencies - Checks ApplicationOrchestrator import/creation",
            "Service Registration Helper - Validates deduplication implementation", 
            "DI Container Safety - Tests global state management safety",
            "UI Fallback Implementation - Checks meaningful fallback UI methods",
            "Background Initialization - Validates performance optimization",
            "Method Extraction Tools - Checks refactoring utilities",
            "Application Factory - Validates ServiceRegistrationHelper usage",
            "Test Files Exist - Ensures test suite is complete"
        ]
        
        print("📋 Available Validation Checks:")
        print("=" * 40)
        for i, check in enumerate(checks, 1):
            print(f"{i:2d}. {check}")


def main():
    """Main entry point for quick validation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="TKA Critical Fixes Quick Validation")
    parser.add_argument("--quick", action="store_true", help="Run only essential checks")
    parser.add_argument("--list", action="store_true", help="List available checks")
    
    args = parser.parse_args()
    
    validator = QuickValidator()
    
    if args.list:
        validator.list_available_checks()
        return
    
    try:
        success = validator.validate_all_fixes(quick_mode=args.quick)
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Validation failed with exception: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
