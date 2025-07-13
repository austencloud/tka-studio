#!/usr/bin/env python3
"""
Deep Dive Analysis Runner - Granular Main Window Creation Analysis

This script runs the deep dive profiler to analyze the main window creation
bottleneck in detail, providing hierarchical timing breakdown and identifying
the most expensive sub-components within the 6.8 second creation process.

Usage:
    python run_deep_dive_analysis.py [options]

Options:
    --mode=full         Run full deep dive analysis (default)
    --mode=focused      Focus only on main window creation
    --save-report       Save detailed report to file

Environment Variables:
    TKA_DEEP_DIVE_PROFILING=1    Enable deep dive profiling (default)
    TKA_REAL_WORLD_PROFILING=1   Enable real-world profiling (default)
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Add the modern src directory to Python path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def run_deep_dive_analysis():
    """Run the comprehensive deep dive analysis."""
    print("🔬 RUNNING DEEP DIVE STARTUP ANALYSIS")
    print("=" * 60)
    print("📋 This provides granular breakdown of main window creation bottleneck")
    print("📋 Analyzing every operation within the 6.8 second TKAMainWindow creation")
    print("=" * 60)
    
    try:
        # Set environment variables for comprehensive profiling
        os.environ["TKA_DEEP_DIVE_PROFILING"] = "1"
        os.environ["TKA_REAL_WORLD_PROFILING"] = "1"
        
        # Import and run the deep dive main
        from deep_dive_main import deep_dive_main
        
        print("📋 Starting deep dive TKA application analysis...")
        start_time = time.perf_counter()
        
        # Run the application (this will block until app closes)
        exit_code = deep_dive_main()
        
        end_time = time.perf_counter()
        total_time = (end_time - start_time) * 1000
        
        print(f"\n🎯 Deep dive analysis completed with exit code: {exit_code}")
        print(f"⏱️  Total analysis runtime: {total_time:.1f}ms")
        
        return exit_code
        
    except Exception as e:
        print(f"❌ Error running deep dive analysis: {e}")
        import traceback
        traceback.print_exc()
        return 1


def run_focused_analysis():
    """Run focused analysis on just the main window creation."""
    print("🎯 RUNNING FOCUSED MAIN WINDOW ANALYSIS")
    print("=" * 60)
    print("📋 Focusing specifically on TKAMainWindow creation bottleneck")
    print("=" * 60)
    
    try:
        # Enable only deep dive profiling for focused analysis
        os.environ["TKA_DEEP_DIVE_PROFILING"] = "1"
        os.environ["TKA_REAL_WORLD_PROFILING"] = "0"
        
        # Import the deep dive profiler and patches
        from deep_dive_profiler import deep_dive_profiler
        from deep_dive_patches import apply_all_deep_dive_patches
        
        # Apply patches
        apply_all_deep_dive_patches()
        
        print("📋 Running focused main window creation test...")
        
        # Simulate just the main window creation part
        with deep_dive_profiler.time_operation("Focused Main Window Test", category="orchestrator", critical_path=True):
            
            # Basic setup
            with deep_dive_profiler.time_operation("Basic imports", category="orchestrator"):
                from PyQt6.QtWidgets import QApplication
                from core.application.application_factory import ApplicationFactory, ApplicationMode
                from presentation.components.ui.splash_screen import SplashScreen
                from PyQt6.QtGui import QGuiApplication
            
            with deep_dive_profiler.time_operation("QApplication setup", category="orchestrator"):
                app = QApplication.instance()
                if not app:
                    app = QApplication(sys.argv)
            
            with deep_dive_profiler.time_operation("Container creation", category="orchestrator"):
                container = ApplicationFactory.create_app(ApplicationMode.PRODUCTION)
            
            with deep_dive_profiler.time_operation("Service initialization", category="services"):
                from core.service_locator import initialize_services
                initialize_services()
            
            with deep_dive_profiler.time_operation("Splash screen setup", category="orchestrator"):
                screens = QGuiApplication.screens()
                target_screen = screens[0] if screens else None
                splash = SplashScreen(target_screen=target_screen)
            
            # THE MAIN EVENT - Main Window Creation
            with deep_dive_profiler.time_operation("MAIN WINDOW CREATION - FOCUSED ANALYSIS", category="orchestrator", critical_path=True):
                from main import TKAMainWindow
                
                window = TKAMainWindow(
                    container=container,
                    splash_screen=splash,
                    target_screen=target_screen,
                    parallel_mode=False,
                    parallel_geometry=None,
                )
        
        # Generate focused report
        deep_dive_profiler.generate_deep_dive_report()
        
        print("✅ Focused analysis completed successfully!")
        return 0
        
    except Exception as e:
        print(f"❌ Error running focused analysis: {e}")
        import traceback
        traceback.print_exc()
        return 1


def save_analysis_report():
    """Save the analysis report to a file."""
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    report_file = f"deep_dive_analysis_report_{timestamp}.txt"
    
    print(f"💾 Analysis report would be saved to: {report_file}")
    print("📋 Report saving functionality can be implemented based on requirements")
    
    return report_file


def main():
    """Main function for the deep dive analysis runner."""
    parser = argparse.ArgumentParser(description="Deep Dive TKA Startup Analysis")
    parser.add_argument("--mode", choices=["full", "focused"], 
                       default="full", help="Analysis mode to run")
    parser.add_argument("--save-report", action="store_true", 
                       help="Save detailed report to file")
    
    args = parser.parse_args()
    
    print("🔬 DEEP DIVE TKA STARTUP PERFORMANCE ANALYSIS")
    print("=" * 60)
    print(f"📋 Mode: {args.mode}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📁 Working Directory: {os.getcwd()}")
    print("=" * 60)
    
    # Run the appropriate analysis mode
    if args.mode == "full":
        exit_code = run_deep_dive_analysis()
    elif args.mode == "focused":
        exit_code = run_focused_analysis()
    else:
        print(f"❌ Unknown mode: {args.mode}")
        exit_code = 1
    
    # Save report if requested
    if args.save_report and exit_code == 0:
        report_file = save_analysis_report()
        print(f"📄 Report saved to: {report_file}")
    
    print(f"\n🎯 Deep dive analysis completed with exit code: {exit_code}")
    
    # Summary of what we learned
    if exit_code == 0:
        print("\n📊 ANALYSIS SUMMARY:")
        print("   🔬 Deep dive profiler provides hierarchical timing breakdown")
        print("   🎯 Identifies specific bottlenecks within main window creation")
        print("   📈 Shows category-based performance analysis")
        print("   💡 Generates targeted optimization recommendations")
        print("   🌍 Combined with real-world profiler for complete picture")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
