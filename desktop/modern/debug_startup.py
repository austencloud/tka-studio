#!/usr/bin/env python3
"""
TKA Startup Performance Debug Script
Identifies exactly what's causing startup delays.
"""

import sys
import time
from pathlib import Path

# Add the modern src path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

def time_operation(name, operation):
    """Time an operation and print results."""
    start = time.time()
    try:
        result = operation()
        duration = (time.time() - start) * 1000
        print(f"✅ {name}: {duration:.1f}ms")
        return result, duration
    except Exception as e:
        duration = (time.time() - start) * 1000
        print(f"❌ {name}: {duration:.1f}ms - ERROR: {e}")
        return None, duration

def debug_startup():
    """Debug the startup process step by step."""
    print("🔍 TKA Startup Performance Analysis")
    print("=" * 50)
    
    total_start = time.time()
    
    # Test 1: Basic Python imports
    time_operation("Basic Python imports", lambda: __import__('os'))
    
    # Test 2: PyQt6 imports
    time_operation("PyQt6.QtWidgets import", lambda: __import__('PyQt6.QtWidgets'))
    time_operation("PyQt6.QtCore import", lambda: __import__('PyQt6.QtCore'))
    time_operation("PyQt6.QtGui import", lambda: __import__('PyQt6.QtGui'))
    
    # Test 3: QApplication creation
    def create_qapp():
        from PyQt6.QtWidgets import QApplication
        return QApplication(sys.argv)
    
    app, _ = time_operation("QApplication creation", create_qapp)
    
    # Test 4: TKA module imports
    time_operation("ApplicationMode import", 
                  lambda: __import__('core.application.application_factory', fromlist=['ApplicationMode']))
    
    time_operation("SplashScreen import", 
                  lambda: __import__('presentation.components.ui.splash_screen', fromlist=['SplashScreen']))
    
    # Test 5: Splash screen creation
    def create_splash():
        from desktop.modern.presentation.components.ui.splash_screen import SplashScreen
        from PyQt6.QtGui import QGuiApplication
        screens = QGuiApplication.screens()
        target_screen = screens[0] if screens else None
        return SplashScreen(target_screen=target_screen)
    
    splash, splash_time = time_operation("SplashScreen creation", create_splash)
    
    # Test 6: Splash screen display
    if splash:
        def show_splash():
            splash.setWindowOpacity(1.0)  # Skip fade-in
            splash.show()
            app.processEvents()
            return True
        
        time_operation("SplashScreen display", show_splash)
    
    # Test 7: Heavy imports (the real bottleneck)
    time_operation("ApplicationFactory import", 
                  lambda: __import__('core.application.application_factory', fromlist=['ApplicationFactory']))
    
    # Test 8: Container creation (very heavy)
    def create_container():
        from desktop.modern.core.application.application_factory import ApplicationFactory, ApplicationMode
        return ApplicationFactory.create_app(ApplicationMode.PRODUCTION)
    
    container, container_time = time_operation("ApplicationFactory.create_app", create_container)
    
    total_time = (time.time() - total_start) * 1000
    print("=" * 50)
    print(f"🎯 TOTAL STARTUP TIME: {total_time:.1f}ms")
    
    # Analysis
    print("\n📊 ANALYSIS:")
    if splash_time > 500:
        print(f"⚠️  Splash creation is slow ({splash_time:.1f}ms) - check background widget")
    if container_time > 2000:
        print(f"⚠️  Container creation is very slow ({container_time:.1f}ms) - this is the main bottleneck")
    
    print("\n💡 RECOMMENDATIONS:")
    if container_time > splash_time * 4:
        print("✅ Move container creation to background thread (already implemented)")
    if splash_time > 200:
        print("✅ Simplify splash screen creation")
    
    # Clean up
    if splash:
        splash.close()
    if app:
        app.quit()

if __name__ == "__main__":
    debug_startup()
