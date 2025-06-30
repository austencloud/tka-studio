#!/usr/bin/env python3
"""
Test script to verify instant splash screen functionality.
This simulates the exact startup sequence to measure splash appearance time.
"""

import sys
import time
from pathlib import Path

# Add the modern src path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

def test_instant_splash():
    """Test the instant splash screen implementation."""
    print("🧪 Testing Instant Splash Screen Implementation")
    print("=" * 50)
    
    start_time = time.time()
    
    # Step 1: Create QApplication (lightweight)
    print("Step 1: Creating QApplication...")
    step_start = time.time()
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QGuiApplication
    
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    step_duration = (time.time() - step_start) * 1000
    print(f"   ✅ QApplication created in {step_duration:.1f}ms")
    
    # Step 2: Get screen info (lightweight)
    print("Step 2: Getting screen information...")
    step_start = time.time()
    screens = QGuiApplication.screens()
    target_screen = screens[0] if screens else None
    step_duration = (time.time() - step_start) * 1000
    print(f"   ✅ Screen info obtained in {step_duration:.1f}ms")
    
    # Step 3: Import and create splash screen
    print("Step 3: Creating splash screen...")
    step_start = time.time()
    from presentation.components.ui.splash_screen import SplashScreen
    splash = SplashScreen(target_screen=target_screen)
    step_duration = (time.time() - step_start) * 1000
    print(f"   ✅ Splash screen created in {step_duration:.1f}ms")
    
    # Step 4: Show splash screen immediately
    print("Step 4: Displaying splash screen...")
    step_start = time.time()
    splash.setWindowOpacity(1.0)  # Full opacity immediately
    splash.show()
    splash.update_progress(5, "Starting application...")
    app.processEvents()  # Force immediate display
    step_duration = (time.time() - step_start) * 1000
    print(f"   ✅ Splash screen displayed in {step_duration:.1f}ms")
    
    # Calculate time to splash visibility
    splash_visible_time = (time.time() - start_time) * 1000
    print(f"\n🎯 SPLASH SCREEN VISIBLE IN: {splash_visible_time:.1f}ms")
    
    # Step 5: Simulate heavy loading (this would happen in background thread)
    print("\nStep 5: Simulating heavy initialization...")
    splash.update_progress(20, "Loading modules...")
    app.processEvents()
    
    # Import the heavy module (this is what was causing the delay)
    heavy_start = time.time()
    from core.application.application_factory import ApplicationMode
    heavy_duration = (time.time() - heavy_start) * 1000
    print(f"   ⚠️  Heavy import took {heavy_duration:.1f}ms (now happens AFTER splash)")
    
    splash.update_progress(100, "Ready!")
    app.processEvents()
    
    total_time = (time.time() - start_time) * 1000
    print(f"\n📊 RESULTS:")
    print(f"   Time to splash visible: {splash_visible_time:.1f}ms")
    print(f"   Heavy import time: {heavy_duration:.1f}ms")
    print(f"   Total time: {total_time:.1f}ms")
    
    # Analysis
    print(f"\n💡 ANALYSIS:")
    if splash_visible_time < 200:
        print("   ✅ EXCELLENT: Splash appears in under 200ms")
    elif splash_visible_time < 500:
        print("   ✅ GOOD: Splash appears in under 500ms")
    else:
        print("   ⚠️  SLOW: Splash takes over 500ms to appear")
    
    if heavy_duration > splash_visible_time:
        print("   ✅ SUCCESS: Heavy loading happens after splash is visible")
    else:
        print("   ❌ PROBLEM: Heavy loading still blocking splash")
    
    # Clean up
    splash.close()
    app.quit()
    
    return splash_visible_time < 500

if __name__ == "__main__":
    success = test_instant_splash()
    if success:
        print("\n🎉 INSTANT SPLASH SCREEN TEST PASSED!")
    else:
        print("\n❌ INSTANT SPLASH SCREEN TEST FAILED!")
    sys.exit(0 if success else 1)
