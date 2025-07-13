#!/usr/bin/env python3
"""
Deep Dive Profiling Patches - Comprehensive Instrumentation

This module provides monkey-patching to instrument every major operation
within the TKAMainWindow creation process for granular performance analysis.

Instrumented Components:
- TKAMainWindow.__init__
- ApplicationOrchestrator.initialize_application
- PictographPoolManager.initialize_pool
- UIManager.setup_main_ui
- ConstructTabWidget creation and setup
- All major sub-operations
"""

import sys
from pathlib import Path

# Add the modern src directory to Python path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

from deep_dive_profiler import deep_dive_profiler


def apply_main_window_patches():
    """Apply deep dive profiling patches to TKAMainWindow."""
    try:
        from main import TKAMainWindow
        
        # Patch TKAMainWindow.__init__
        original_init = TKAMainWindow.__init__
        
        def instrumented_init(self, container=None, splash_screen=None, target_screen=None, parallel_mode=False, parallel_geometry=None):
            """Instrumented TKAMainWindow initialization."""
            with deep_dive_profiler.time_operation("TKAMainWindow.__init__", category="orchestrator", critical_path=True):
                
                with deep_dive_profiler.time_operation("QMainWindow super().__init__", category="orchestrator"):
                    super(TKAMainWindow, self).__init__()
                
                with deep_dive_profiler.time_operation("Window hide and property setup", category="orchestrator"):
                    self.hide()
                    self.container = container
                    self.splash = splash_screen
                    self.target_screen = target_screen
                    self.parallel_mode = parallel_mode
                    self.parallel_geometry = parallel_geometry
                
                if self.container:
                    with deep_dive_profiler.time_operation("ApplicationOrchestrator import", category="orchestrator"):
                        from application.services.core.application_orchestrator import ApplicationOrchestrator
                    
                    with deep_dive_profiler.time_operation("ApplicationOrchestrator creation", category="orchestrator", critical_path=True):
                        self.orchestrator = ApplicationOrchestrator(container=self.container)
                    
                    with deep_dive_profiler.time_operation("ApplicationOrchestrator.initialize_application", category="orchestrator", critical_path=True):
                        self.tab_widget = self.orchestrator.initialize_application(
                            self, splash_screen, target_screen, parallel_mode, parallel_geometry
                        )
        
        TKAMainWindow.__init__ = instrumented_init
        print("✅ TKAMainWindow patches applied")
        
    except ImportError as e:
        print(f"⚠️  Could not apply TKAMainWindow patches: {e}")


def apply_orchestrator_patches():
    """Apply deep dive profiling patches to ApplicationOrchestrator."""
    try:
        from application.services.core.application_orchestrator import ApplicationOrchestrator
        
        # Patch ApplicationOrchestrator.initialize_application
        original_initialize = ApplicationOrchestrator.initialize_application
        
        def instrumented_initialize(self, main_window, splash_screen=None, target_screen=None, parallel_mode=False, parallel_geometry=None):
            """Instrumented ApplicationOrchestrator initialization."""
            with deep_dive_profiler.time_operation("Create progress callback", category="orchestrator"):
                progress_callback = self._create_progress_callback(splash_screen)
            
            with deep_dive_profiler.time_operation("Lifecycle manager initialization", category="lifecycle", critical_path=True):
                self.lifecycle_manager.initialize_application(
                    main_window, target_screen, parallel_mode, parallel_geometry, progress_callback
                )
            
            with deep_dive_profiler.time_operation("DI container setup", category="services"):
                from core.dependency_injection.di_container import get_container
                if progress_callback:
                    progress_callback(45, "Configuring dependency injection...")
                self.container = get_container()
            
            with deep_dive_profiler.time_operation("Service registration", category="services", critical_path=True):
                if progress_callback:
                    progress_callback(50, "Registering application services...")
                self.service_manager.register_all_services(self.container)
                if progress_callback:
                    progress_callback(55, "Services configured")
            
            with deep_dive_profiler.time_operation("Pictograph pool initialization", category="pictograph_pool", critical_path=True):
                if progress_callback:
                    progress_callback(57, "Initializing pictograph pool...")
                try:
                    from application.services.pictograph_pool_manager import PictographPoolManager
                    pool_manager = self.container.resolve(PictographPoolManager)
                    pool_manager.initialize_pool()
                    if progress_callback:
                        progress_callback(59, "Pictograph pool initialized")
                except Exception as e:
                    print(f"❌ Failed to initialize pictograph pool: {e}")
                    if progress_callback:
                        progress_callback(59, "Pictograph pool initialization failed")
            
            with deep_dive_profiler.time_operation("UI Manager setup", category="ui_manager", critical_path=True):
                if progress_callback:
                    progress_callback(60, "Initializing user interface...")
                self.tab_widget = self.ui_manager.setup_main_ui(
                    main_window, self.container, progress_callback, self.lifecycle_manager.session_service
                )
            
            with deep_dive_profiler.time_operation("Session restoration", category="session"):
                if progress_callback:
                    progress_callback(85, "Restoring session state...")
                self.lifecycle_manager.trigger_deferred_session_restoration()
            
            with deep_dive_profiler.time_operation("Background setup", category="background"):
                if progress_callback:
                    progress_callback(90, "Setting up background services...")
                self.background_widget = self.background_manager.setup_background(
                    main_window, self.container, progress_callback
                )
            
            with deep_dive_profiler.time_operation("API server startup", category="background"):
                if progress_callback:
                    progress_callback(95, "Starting API server...")
                self.lifecycle_manager.start_api_server(True)
            
            return self.tab_widget
        
        ApplicationOrchestrator.initialize_application = instrumented_initialize
        print("✅ ApplicationOrchestrator patches applied")
        
    except ImportError as e:
        print(f"⚠️  Could not apply ApplicationOrchestrator patches: {e}")


def apply_pictograph_pool_patches():
    """Apply deep dive profiling patches to PictographPoolManager."""
    try:
        from application.services.pictograph_pool_manager import PictographPoolManager
        
        # Patch PictographPoolManager.initialize_pool
        original_initialize_pool = PictographPoolManager.initialize_pool
        
        def instrumented_initialize_pool(self):
            """Instrumented pictograph pool initialization."""
            with deep_dive_profiler.time_operation("Pool manager setup", category="pictograph_pool"):
                # Call original method which will be further instrumented
                return original_initialize_pool(self)
        
        PictographPoolManager.initialize_pool = instrumented_initialize_pool
        print("✅ PictographPoolManager patches applied")
        
    except ImportError as e:
        print(f"⚠️  Could not apply PictographPoolManager patches: {e}")


def apply_ui_manager_patches():
    """Apply deep dive profiling patches to UIManager."""
    try:
        from application.services.ui.ui_manager import UIManager
        
        # Patch UIManager.setup_main_ui
        original_setup_main_ui = UIManager.setup_main_ui
        
        def instrumented_setup_main_ui(self, main_window, container, progress_callback, session_service):
            """Instrumented UI manager setup."""
            with deep_dive_profiler.time_operation("Central widget setup", category="ui_manager"):
                from PyQt6.QtWidgets import QVBoxLayout, QWidget
                central_widget = QWidget()
                central_widget.setStyleSheet("background: transparent;")
                main_window.setCentralWidget(central_widget)
                layout = QVBoxLayout(central_widget)
                layout.setContentsMargins(20, 20, 20, 20)
            
            with deep_dive_profiler.time_operation("Header layout creation", category="ui_manager"):
                header_layout = self.create_header_layout(main_window)
                layout.addLayout(header_layout)
            
            with deep_dive_profiler.time_operation("Tab widget creation", category="ui_manager", critical_path=True):
                tab_widget = self.create_tab_widget()
                layout.addWidget(tab_widget)
            
            with deep_dive_profiler.time_operation("Construct tab loading", category="construct_tab", critical_path=True):
                # This is where the major bottleneck likely occurs
                from application.services.ui.ui_setup_manager import UISetupManager
                ui_setup_manager = UISetupManager(container)
                ui_setup_manager.load_construct_tab(tab_widget, progress_callback)
            
            return tab_widget
        
        UIManager.setup_main_ui = instrumented_setup_main_ui
        print("✅ UIManager patches applied")
        
    except ImportError as e:
        print(f"⚠️  Could not apply UIManager patches: {e}")


def apply_construct_tab_patches():
    """Apply deep dive profiling patches to ConstructTabWidget."""
    try:
        from presentation.tabs.construct.construct_tab_widget import ConstructTabWidget
        
        # Patch ConstructTabWidget.__init__
        original_construct_init = ConstructTabWidget.__init__
        
        def instrumented_construct_init(self, container, progress_callback=None):
            """Instrumented ConstructTabWidget initialization."""
            with deep_dive_profiler.time_operation("ConstructTabWidget base setup", category="construct_tab"):
                # Initialize base widget
                from PyQt6.QtWidgets import QWidget
                super(ConstructTabWidget, self).__init__()
                self.container = container
                self.progress_callback = progress_callback
            
            with deep_dive_profiler.time_operation("ConstructTabWidget UI setup", category="construct_tab", critical_path=True):
                self._setup_ui_with_progress()
        
        ConstructTabWidget.__init__ = instrumented_construct_init
        
        # Patch ConstructTabWidget.setup if it exists
        if hasattr(ConstructTabWidget, 'setup'):
            original_setup = ConstructTabWidget.setup
            
            def instrumented_setup(self):
                """Instrumented ConstructTabWidget setup."""
                with deep_dive_profiler.time_operation("ConstructTabWidget.setup", category="construct_tab", critical_path=True):
                    return original_setup(self)
            
            ConstructTabWidget.setup = instrumented_setup
        
        print("✅ ConstructTabWidget patches applied")
        
    except ImportError as e:
        print(f"⚠️  Could not apply ConstructTabWidget patches: {e}")


def apply_all_deep_dive_patches():
    """Apply all deep dive profiling patches."""
    print("🔬 Applying comprehensive deep dive profiling patches...")
    apply_main_window_patches()
    apply_orchestrator_patches()
    apply_pictograph_pool_patches()
    apply_ui_manager_patches()
    apply_construct_tab_patches()
    print("🎯 All deep dive patches applied")


if __name__ == "__main__":
    apply_all_deep_dive_patches()
