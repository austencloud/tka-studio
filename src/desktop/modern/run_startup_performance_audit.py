#!/usr/bin/env python3
"""
TKA Startup Performance Audit Runner

This script runs comprehensive performance audits of the TKA application startup sequence.
It provides multiple testing modes and generates detailed reports.

Usage:
    python run_startup_performance_audit.py [options]

Options:
    --mode=full         Run full application startup (default)
    --mode=profiler     Run standalone profiler test
    --mode=multiple     Run multiple iterations for consistency
    --iterations=N      Number of iterations for multiple mode (default: 3)
    --output=FILE       Save results to file
    --no-gui           Run without GUI (profiler mode only)

Environment Variables:
    TKA_STARTUP_PROFILING=1    Enable profiling (default)
    TKA_STARTUP_PROFILING=0    Disable profiling for baseline measurement
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Add the modern src directory to Python path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def run_full_application_audit():
    """Run the full application startup with profiling."""
    print("🚀 RUNNING FULL APPLICATION STARTUP AUDIT")
    print("=" * 60)
    
    try:
        # Import and run the instrumented main
        from instrumented_main import instrumented_main
        
        print("📋 Starting instrumented TKA application...")
        start_time = time.perf_counter()
        
        # Run the application (this will block until app closes)
        exit_code = instrumented_main()
        
        end_time = time.perf_counter()
        total_time = (end_time - start_time) * 1000
        
        print(f"\n🎯 Application completed with exit code: {exit_code}")
        print(f"⏱️  Total runtime: {total_time:.1f}ms")
        
        return exit_code
        
    except Exception as e:
        print(f"❌ Error running full application audit: {e}")
        import traceback
        traceback.print_exc()
        return 1


def run_profiler_only_audit():
    """Run the standalone profiler test without full GUI."""
    print("🔍 RUNNING STANDALONE PROFILER AUDIT")
    print("=" * 60)
    
    try:
        # Import and run the enhanced profiler
        from enhanced_startup_profiler import profile_complete_startup
        
        print("📋 Starting standalone profiler test...")
        profile_complete_startup()
        
        return 0
        
    except Exception as e:
        print(f"❌ Error running profiler audit: {e}")
        import traceback
        traceback.print_exc()
        return 1


def run_multiple_iterations_audit(iterations=3):
    """Run multiple iterations to check consistency."""
    print(f"🔄 RUNNING MULTIPLE ITERATIONS AUDIT ({iterations} iterations)")
    print("=" * 60)
    
    results = []
    
    for i in range(iterations):
        print(f"\n📋 ITERATION {i+1}/{iterations}")
        print("-" * 40)
        
        try:
            # Set environment to enable profiling
            os.environ["TKA_STARTUP_PROFILING"] = "1"
            
            # Import fresh profiler instance
            import importlib
            if 'enhanced_startup_profiler' in sys.modules:
                importlib.reload(sys.modules['enhanced_startup_profiler'])
            
            from enhanced_startup_profiler import profile_complete_startup
            
            start_time = time.perf_counter()
            profile_complete_startup()
            end_time = time.perf_counter()
            
            iteration_time = (end_time - start_time) * 1000
            results.append(iteration_time)
            
            print(f"✅ Iteration {i+1} completed: {iteration_time:.1f}ms")
            
            # Small delay between iterations
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error in iteration {i+1}: {e}")
            results.append(None)
    
    # Analyze results
    print(f"\n📊 MULTIPLE ITERATIONS ANALYSIS")
    print("=" * 40)
    
    valid_results = [r for r in results if r is not None]
    if valid_results:
        avg_time = sum(valid_results) / len(valid_results)
        min_time = min(valid_results)
        max_time = max(valid_results)
        
        print(f"✅ Successful iterations: {len(valid_results)}/{iterations}")
        print(f"⏱️  Average time: {avg_time:.1f}ms")
        print(f"⏱️  Minimum time: {min_time:.1f}ms")
        print(f"⏱️  Maximum time: {max_time:.1f}ms")
        print(f"📊 Variance: {max_time - min_time:.1f}ms")
        
        if max_time - min_time < 500:
            print("✅ Good consistency between iterations")
        else:
            print("⚠️  High variance detected - results may be inconsistent")
    else:
        print("❌ No successful iterations")
        return 1
    
    return 0


def run_baseline_measurement():
    """Run baseline measurement with profiling disabled."""
    print("📏 RUNNING BASELINE MEASUREMENT (NO PROFILING)")
    print("=" * 60)
    
    # Disable profiling
    os.environ["TKA_STARTUP_PROFILING"] = "0"
    
    try:
        # Import and run without profiling
        import importlib
        if 'enhanced_startup_profiler' in sys.modules:
            importlib.reload(sys.modules['enhanced_startup_profiler'])
        
        from enhanced_startup_profiler import profile_complete_startup
        
        print("📋 Running baseline test (profiling disabled)...")
        start_time = time.perf_counter()
        profile_complete_startup()
        end_time = time.perf_counter()
        
        baseline_time = (end_time - start_time) * 1000
        print(f"⏱️  Baseline startup time: {baseline_time:.1f}ms")
        
        return baseline_time
        
    except Exception as e:
        print(f"❌ Error running baseline measurement: {e}")
        return None


def main():
    """Main function for the audit runner."""
    parser = argparse.ArgumentParser(description="TKA Startup Performance Audit Runner")
    parser.add_argument("--mode", choices=["full", "profiler", "multiple", "baseline"], 
                       default="profiler", help="Audit mode to run")
    parser.add_argument("--iterations", type=int, default=3, 
                       help="Number of iterations for multiple mode")
    parser.add_argument("--output", type=str, help="Save results to file")
    parser.add_argument("--no-gui", action="store_true", 
                       help="Run without GUI (profiler mode only)")
    
    args = parser.parse_args()
    
    print("🎯 TKA STARTUP PERFORMANCE AUDIT")
    print("=" * 60)
    print(f"📋 Mode: {args.mode}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📁 Working Directory: {os.getcwd()}")
    print("=" * 60)
    
    # Run the appropriate audit mode
    if args.mode == "full":
        exit_code = run_full_application_audit()
    elif args.mode == "profiler":
        exit_code = run_profiler_only_audit()
    elif args.mode == "multiple":
        exit_code = run_multiple_iterations_audit(args.iterations)
    elif args.mode == "baseline":
        baseline_time = run_baseline_measurement()
        exit_code = 0 if baseline_time is not None else 1
    else:
        print(f"❌ Unknown mode: {args.mode}")
        exit_code = 1
    
    print(f"\n🎯 Audit completed with exit code: {exit_code}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
