#!/usr/bin/env python3
"""
Real-World Startup Performance Audit Runner

This script runs the real-world startup profiler that measures the complete user
experience from process launch to fully interactive GUI, including all Qt event
loop operations, splash screen animations, and asynchronous initialization.

Usage:
    python run_real_world_audit.py [options]

Options:
    --mode=full         Run full real-world application startup (default)
    --mode=comparison   Compare real-world vs original profiler
    --iterations=N      Number of iterations for consistency testing (default: 1)
    --baseline         Also run baseline measurement without profiling

Environment Variables:
    TKA_REAL_WORLD_PROFILING=1    Enable real-world profiling (default)
    TKA_REAL_WORLD_PROFILING=0    Disable real-world profiling
"""

import argparse
import os
import sys
import time
from pathlib import Path

# Add the modern src directory to Python path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))


def run_real_world_audit():
    """Run the real-world application startup with comprehensive profiling."""
    print("🌍 RUNNING REAL-WORLD STARTUP AUDIT")
    print("=" * 60)
    print("📋 This measures the complete user experience from process start to interactive GUI")
    print("📋 Including Qt event loop, splash animations, and async initialization")
    print("=" * 60)
    
    try:
        # Import and run the real-world instrumented main
        from real_world_main import real_world_main
        
        print("📋 Starting real-world TKA application...")
        start_time = time.perf_counter()
        
        # Run the application (this will block until app closes)
        exit_code = real_world_main()
        
        end_time = time.perf_counter()
        total_time = (end_time - start_time) * 1000
        
        print(f"\n🎯 Real-world application completed with exit code: {exit_code}")
        print(f"⏱️  Total wall-clock runtime: {total_time:.1f}ms")
        
        return exit_code
        
    except Exception as e:
        print(f"❌ Error running real-world audit: {e}")
        import traceback
        traceback.print_exc()
        return 1


def run_comparison_audit():
    """Run comparison between real-world and original profiler."""
    print("🔄 RUNNING COMPARISON AUDIT")
    print("=" * 60)
    print("📋 Comparing real-world profiler vs original component profiler")
    print("=" * 60)
    
    results = {}
    
    # Run original profiler
    print("\n1️⃣ RUNNING ORIGINAL PROFILER:")
    print("-" * 40)
    try:
        os.environ["TKA_STARTUP_PROFILING"] = "1"
        os.environ["TKA_REAL_WORLD_PROFILING"] = "0"
        
        from enhanced_startup_profiler import profile_complete_startup
        
        start_time = time.perf_counter()
        profile_complete_startup()
        end_time = time.perf_counter()
        
        results["original"] = (end_time - start_time) * 1000
        print(f"✅ Original profiler completed: {results['original']:.1f}ms")
        
    except Exception as e:
        print(f"❌ Error in original profiler: {e}")
        results["original"] = None
    
    # Small delay between tests
    time.sleep(2)
    
    # Run real-world profiler
    print("\n2️⃣ RUNNING REAL-WORLD PROFILER:")
    print("-" * 40)
    try:
        os.environ["TKA_STARTUP_PROFILING"] = "0"
        os.environ["TKA_REAL_WORLD_PROFILING"] = "1"
        
        # Clear module cache to get fresh profiler
        import importlib
        if 'real_world_startup_profiler' in sys.modules:
            importlib.reload(sys.modules['real_world_startup_profiler'])
        if 'real_world_main' in sys.modules:
            importlib.reload(sys.modules['real_world_main'])
        
        from real_world_main import real_world_main
        
        start_time = time.perf_counter()
        exit_code = real_world_main()
        end_time = time.perf_counter()
        
        results["real_world"] = (end_time - start_time) * 1000
        print(f"✅ Real-world profiler completed: {results['real_world']:.1f}ms (exit: {exit_code})")
        
    except Exception as e:
        print(f"❌ Error in real-world profiler: {e}")
        results["real_world"] = None
    
    # Analyze comparison
    print(f"\n📊 COMPARISON ANALYSIS")
    print("=" * 40)
    
    if results["original"] and results["real_world"]:
        difference = results["real_world"] - results["original"]
        percentage = (difference / results["original"]) * 100
        
        print(f"📈 Original profiler time:   {results['original']:>8.1f}ms")
        print(f"📈 Real-world profiler time: {results['real_world']:>8.1f}ms")
        print(f"📊 Difference:               {difference:>8.1f}ms ({percentage:+.1f}%)")
        
        if abs(percentage) < 10:
            print("✅ Results are consistent - both profilers measure similar timing")
        elif results["real_world"] > results["original"]:
            print("🎯 Real-world profiler captures additional timing not measured by original")
            print("   This likely includes Qt event loop, animations, and async operations")
        else:
            print("⚠️  Unexpected result - real-world profiler faster than original")
    else:
        print("❌ Could not complete comparison - one or both profilers failed")
        return 1
    
    return 0


def run_multiple_iterations(iterations=3):
    """Run multiple iterations of real-world profiling for consistency."""
    print(f"🔄 RUNNING MULTIPLE REAL-WORLD ITERATIONS ({iterations} iterations)")
    print("=" * 60)
    
    results = []
    
    for i in range(iterations):
        print(f"\n📋 REAL-WORLD ITERATION {i+1}/{iterations}")
        print("-" * 40)
        
        try:
            # Ensure profiling is enabled
            os.environ["TKA_REAL_WORLD_PROFILING"] = "1"
            
            # Clear module cache for fresh profiler
            import importlib
            if 'real_world_startup_profiler' in sys.modules:
                importlib.reload(sys.modules['real_world_startup_profiler'])
            if 'real_world_main' in sys.modules:
                importlib.reload(sys.modules['real_world_main'])
            
            from real_world_main import real_world_main
            
            start_time = time.perf_counter()
            exit_code = real_world_main()
            end_time = time.perf_counter()
            
            iteration_time = (end_time - start_time) * 1000
            results.append(iteration_time)
            
            print(f"✅ Iteration {i+1} completed: {iteration_time:.1f}ms (exit: {exit_code})")
            
            # Delay between iterations
            if i < iterations - 1:
                time.sleep(3)
            
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
        
        if max_time - min_time < 1000:
            print("✅ Good consistency between iterations")
        else:
            print("⚠️  High variance detected - results may be inconsistent")
            print("   This could indicate system load or caching effects")
    else:
        print("❌ No successful iterations")
        return 1
    
    return 0


def main():
    """Main function for the real-world audit runner."""
    parser = argparse.ArgumentParser(description="Real-World TKA Startup Performance Audit")
    parser.add_argument("--mode", choices=["full", "comparison", "multiple"], 
                       default="full", help="Audit mode to run")
    parser.add_argument("--iterations", type=int, default=1, 
                       help="Number of iterations for multiple mode")
    parser.add_argument("--baseline", action="store_true", 
                       help="Also run baseline measurement")
    
    args = parser.parse_args()
    
    print("🌍 REAL-WORLD TKA STARTUP PERFORMANCE AUDIT")
    print("=" * 60)
    print(f"📋 Mode: {args.mode}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"📁 Working Directory: {os.getcwd()}")
    print("=" * 60)
    
    # Run the appropriate audit mode
    if args.mode == "full":
        exit_code = run_real_world_audit()
    elif args.mode == "comparison":
        exit_code = run_comparison_audit()
    elif args.mode == "multiple":
        exit_code = run_multiple_iterations(args.iterations)
    else:
        print(f"❌ Unknown mode: {args.mode}")
        exit_code = 1
    
    print(f"\n🎯 Real-world audit completed with exit code: {exit_code}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
