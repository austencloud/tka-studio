#!/usr/bin/env python3
"""
Orchestrator Profiling Patch - Instrument Application Orchestrator for Performance Analysis

This module provides monkey-patching functionality to instrument the ApplicationOrchestrator
with detailed performance profiling without modifying the original source code.

Usage:
    from orchestrator_profiling_patch import apply_profiling_patch
    apply_profiling_patch()
"""

import sys
from pathlib import Path

# Add the modern src directory to Python path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

from enhanced_startup_profiler import profiler


def apply_profiling_patch():
    """Apply profiling instrumentation to the ApplicationOrchestrator."""
    try:
        from application.services.core.application_orchestrator import ApplicationOrchestrator
        from application.services.core.application_initialization_orchestrator import ApplicationInitializationOrchestrator
        from application.services.ui.ui_manager import UIManager
        
        # Patch ApplicationOrchestrator.initialize_application
        original_initialize_application = ApplicationOrchestrator.initialize_application
        
        def instrumented_initialize_application(self, main_window, splash_screen=None, target_screen=None, parallel_mode=False, parallel_geometry=None):
            """Instrumented version of initialize_application."""
            with profiler.time_operation("ApplicationOrchestrator.initialize_application"):
                return original_initialize_application(self, main_window, splash_screen, target_screen, parallel_mode, parallel_geometry)
        
        ApplicationOrchestrator.initialize_application = instrumented_initialize_application
        
        # Patch ApplicationInitializationOrchestrator.initialize_application
        original_lifecycle_init = ApplicationInitializationOrchestrator.initialize_application
        
        def instrumented_lifecycle_init(self, main_window, target_screen=None, parallel_mode=False, parallel_geometry=None, progress_callback=None):
            """Instrumented version of lifecycle initialization."""
            with profiler.time_operation("Lifecycle manager initialization"):
                # Track progress updates if callback exists
                if progress_callback:
                    original_callback = progress_callback
                    
                    def tracked_progress_callback(progress, message):
                        profiler.track_progress_update(progress, message)
                        return original_callback(progress, message)
                    
                    return original_lifecycle_init(self, main_window, target_screen, parallel_mode, parallel_geometry, tracked_progress_callback)
                else:
                    return original_lifecycle_init(self, main_window, target_screen, parallel_mode, parallel_geometry, progress_callback)
        
        ApplicationInitializationOrchestrator.initialize_application = instrumented_lifecycle_init
        
        # Patch UIManager.setup_main_ui
        original_setup_main_ui = UIManager.setup_main_ui
        
        def instrumented_setup_main_ui(self, main_window, container, progress_callback, session_service):
            """Instrumented version of UI setup."""
            with profiler.time_operation("UI Manager - setup_main_ui"):
                # Track progress updates if callback exists
                if progress_callback:
                    original_callback = progress_callback
                    
                    def tracked_progress_callback(progress, message):
                        profiler.track_progress_update(progress, message)
                        return original_callback(progress, message)
                    
                    return original_setup_main_ui(self, main_window, container, tracked_progress_callback, session_service)
                else:
                    return original_setup_main_ui(self, main_window, container, progress_callback, session_service)
        
        UIManager.setup_main_ui = instrumented_setup_main_ui
        
        # Patch individual UI creation methods for more granular timing
        original_create_header_layout = UIManager.create_header_layout
        
        def instrumented_create_header_layout(self, main_window):
            """Instrumented version of header layout creation."""
            with profiler.time_operation("UI Manager - create_header_layout"):
                return original_create_header_layout(self, main_window)
        
        UIManager.create_header_layout = instrumented_create_header_layout
        
        original_create_tab_widget = UIManager.create_tab_widget
        
        def instrumented_create_tab_widget(self):
            """Instrumented version of tab widget creation."""
            with profiler.time_operation("UI Manager - create_tab_widget"):
                return original_create_tab_widget(self)
        
        UIManager.create_tab_widget = instrumented_create_tab_widget
        
        print("✅ Profiling patches applied successfully to ApplicationOrchestrator")
        
    except ImportError as e:
        print(f"⚠️  Could not apply profiling patches: {e}")
    except Exception as e:
        print(f"❌ Error applying profiling patches: {e}")


def apply_construct_tab_profiling_patch():
    """Apply profiling instrumentation to ConstructTabWidget."""
    try:
        from presentation.tabs.construct.construct_tab_widget import ConstructTabWidget
        
        # Patch ConstructTabWidget.__init__
        original_construct_init = ConstructTabWidget.__init__
        
        def instrumented_construct_init(self, container, progress_callback=None):
            """Instrumented version of ConstructTabWidget initialization."""
            with profiler.time_operation("ConstructTabWidget.__init__"):
                return original_construct_init(self, container, progress_callback)
        
        ConstructTabWidget.__init__ = instrumented_construct_init
        
        # Patch ConstructTabWidget.setup
        original_construct_setup = ConstructTabWidget.setup
        
        def instrumented_construct_setup(self):
            """Instrumented version of ConstructTabWidget setup."""
            with profiler.time_operation("ConstructTabWidget.setup"):
                return original_construct_setup(self)
        
        ConstructTabWidget.setup = instrumented_construct_setup
        
        print("✅ Profiling patches applied successfully to ConstructTabWidget")
        
    except ImportError as e:
        print(f"⚠️  Could not apply ConstructTabWidget profiling patches: {e}")
    except Exception as e:
        print(f"❌ Error applying ConstructTabWidget profiling patches: {e}")


def apply_pictograph_pool_profiling_patch():
    """Apply profiling instrumentation to PictographPoolManager."""
    try:
        from application.services.pictograph_pool_manager import PictographPoolManager
        
        # Patch PictographPoolManager.initialize_pool
        original_initialize_pool = PictographPoolManager.initialize_pool
        
        def instrumented_initialize_pool(self):
            """Instrumented version of pictograph pool initialization."""
            with profiler.time_operation("PictographPoolManager.initialize_pool"):
                return original_initialize_pool(self)
        
        PictographPoolManager.initialize_pool = instrumented_initialize_pool
        
        print("✅ Profiling patches applied successfully to PictographPoolManager")
        
    except ImportError as e:
        print(f"⚠️  Could not apply PictographPoolManager profiling patches: {e}")
    except Exception as e:
        print(f"❌ Error applying PictographPoolManager profiling patches: {e}")


def apply_all_profiling_patches():
    """Apply all available profiling patches."""
    print("🔧 Applying comprehensive profiling patches...")
    apply_profiling_patch()
    apply_construct_tab_profiling_patch()
    apply_pictograph_pool_profiling_patch()
    print("🎯 All profiling patches applied")


if __name__ == "__main__":
    apply_all_profiling_patches()
