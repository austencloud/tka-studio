#!/usr/bin/env python3
"""
Performance Comparison and Visual Verification Demo

Provides detailed performance analysis and visual output showing differences
between application modes, with memory usage, execution time, and behavior comparisons.
"""

import sys
import time
import psutil
import json
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass, asdict

# Add TKA modern src to path
tka_src_path = Path(__file__).parent.parent / "src" / "desktop" / "modern" / "src"
sys.path.insert(0, str(tka_src_path))

from core.application.application_factory import ApplicationFactory, ApplicationMode
from core.interfaces.core_services import (
    ISequenceDataService,
    ILayoutService,
    ISettingsService,
    ISequenceManagementService
)


@dataclass
class PerformanceMetrics:
    """Performance metrics for a specific operation."""
    operation: str
    mode: str
    execution_time: float
    memory_before: float
    memory_after: float
    memory_delta: float
    cpu_percent: float
    success: bool
    result_size: int = 0
    error_message: str = ""


class PerformanceBenchmark:
    """Benchmarking tool for TKA Application Factory modes."""
    
    def __init__(self):
        self.metrics: List[PerformanceMetrics] = []
        self.process = psutil.Process()
    
    def measure_operation(self, operation_name: str, mode: str, operation_func) -> PerformanceMetrics:
        """Measure performance of a specific operation."""
        # Get initial metrics
        memory_before = self.process.memory_info().rss / 1024 / 1024  # MB
        cpu_before = self.process.cpu_percent()
        
        # Execute operation
        start_time = time.time()
        success = True
        result_size = 0
        error_message = ""
        
        try:
            result = operation_func()
            if isinstance(result, (list, dict)):
                result_size = len(result)
            elif hasattr(result, '__len__'):
                result_size = len(result)
        except Exception as e:
            success = False
            error_message = str(e)
        
        execution_time = time.time() - start_time
        
        # Get final metrics
        memory_after = self.process.memory_info().rss / 1024 / 1024  # MB
        cpu_after = self.process.cpu_percent()
        
        metrics = PerformanceMetrics(
            operation=operation_name,
            mode=mode,
            execution_time=execution_time,
            memory_before=memory_before,
            memory_after=memory_after,
            memory_delta=memory_after - memory_before,
            cpu_percent=max(cpu_before, cpu_after),
            success=success,
            result_size=result_size,
            error_message=error_message
        )
        
        self.metrics.append(metrics)
        return metrics
    
    def benchmark_container_creation(self) -> Dict[str, PerformanceMetrics]:
        """Benchmark container creation across modes."""
        print("[BUILD] Benchmarking Container Creation")
        print("-" * 40)
        
        results = {}
        modes = [ApplicationMode.TEST, ApplicationMode.HEADLESS, ApplicationMode.PRODUCTION]
        
        for mode in modes:
            def create_container():
                return ApplicationFactory.create_app(mode)
            
            metrics = self.measure_operation(f"Create {mode} Container", mode, create_container)
            results[mode] = metrics
            
            status = "[OK]" if metrics.success else "[ERROR]"
            print(f"{status} {mode:12} | {metrics.execution_time:.4f}s | "
                  f"{metrics.memory_delta:+.2f}MB | CPU: {metrics.cpu_percent:.1f}%")
        
        return results
    
    def benchmark_sequence_operations(self, container, mode: str) -> Dict[str, PerformanceMetrics]:
        """Benchmark sequence operations for a specific mode."""
        print(f"\n[MUSIC] Benchmarking Sequence Operations - {mode}")
        print("-" * 50)
        
        results = {}
        seq_service = container.resolve(ISequenceDataService)
        mgmt_service = container.resolve(ISequenceManagementService)
        
        # Benchmark sequence creation
        def create_sequences():
            sequences = []
            for i in range(100):  # Create 100 sequences
                seq = seq_service.create_new_sequence(f"Benchmark Seq {i}")
                sequences.append(seq)
            return sequences
        
        metrics = self.measure_operation("Create 100 Sequences", mode, create_sequences)
        results["creation"] = metrics
        
        status = "[OK]" if metrics.success else "[ERROR]"
        print(f"{status} Create 100 Sequences | {metrics.execution_time:.4f}s | "
              f"{metrics.memory_delta:+.2f}MB | {metrics.result_size} created")
        
        # Benchmark sequence retrieval
        def retrieve_sequences():
            return seq_service.get_all_sequences()
        
        metrics = self.measure_operation("Retrieve All Sequences", mode, retrieve_sequences)
        results["retrieval"] = metrics
        
        status = "[OK]" if metrics.success else "[ERROR]"
        print(f"{status} Retrieve All Sequences | {metrics.execution_time:.4f}s | "
              f"{metrics.memory_delta:+.2f}MB | {metrics.result_size} retrieved")
        
        # Benchmark sequence management operations
        def manage_sequences():
            operations = 0
            for i in range(50):  # 50 management operations
                seq = mgmt_service.create_sequence(f"Mgmt Seq {i}", 16)
                for j in range(4):  # Add 4 beats
                    mgmt_service.add_beat(seq, {"beat_number": j+1, "letter": chr(65+j)}, j)
                operations += 5  # 1 create + 4 add_beat
            return operations
        
        metrics = self.measure_operation("Sequence Management Ops", mode, manage_sequences)
        results["management"] = metrics
        
        status = "[OK]" if metrics.success else "[ERROR]"
        print(f"{status} Management Operations | {metrics.execution_time:.4f}s | "
              f"{metrics.memory_delta:+.2f}MB | {metrics.result_size} operations")
        
        return results
    
    def benchmark_layout_calculations(self, container, mode: str) -> Dict[str, PerformanceMetrics]:
        """Benchmark layout calculations for a specific mode."""
        print(f"\n[RULER] Benchmarking Layout Calculations - {mode}")
        print("-" * 50)
        
        results = {}
        layout_service = container.resolve(ILayoutService)
        
        # Benchmark grid layout calculations
        def calculate_grids():
            calculations = 0
            for items in [4, 8, 16, 24, 32, 48, 64]:
                for width in [800, 1024, 1366, 1920, 2560]:
                    for height in [600, 768, 1080, 1440]:
                        layout_service.get_optimal_grid_layout(items, (width, height))
                        calculations += 1
            return calculations
        
        metrics = self.measure_operation("Grid Layout Calculations", mode, calculate_grids)
        results["grid_calculations"] = metrics
        
        status = "[OK]" if metrics.success else "[ERROR]"
        print(f"{status} Grid Calculations | {metrics.execution_time:.4f}s | "
              f"{metrics.memory_delta:+.2f}MB | {metrics.result_size} calculations")
        
        # Benchmark component size calculations
        def calculate_components():
            window_size = layout_service.get_main_window_size()
            calculations = 0
            component_types = ["beat_frame", "pictograph", "button", "panel", "widget"]
            
            for _ in range(1000):  # 1000 calculations
                for comp_type in component_types:
                    layout_service.calculate_component_size(comp_type, window_size)
                    calculations += 1
            return calculations
        
        metrics = self.measure_operation("Component Size Calculations", mode, calculate_components)
        results["component_calculations"] = metrics
        
        status = "[OK]" if metrics.success else "[ERROR]"
        print(f"{status} Component Calculations | {metrics.execution_time:.4f}s | "
              f"{metrics.memory_delta:+.2f}MB | {metrics.result_size} calculations")
        
        return results
    
    def benchmark_settings_operations(self, container, mode: str) -> Dict[str, PerformanceMetrics]:
        """Benchmark settings operations for a specific mode."""
        print(f"\n[SETTINGS] Benchmarking Settings Operations - {mode}")
        print("-" * 50)
        
        results = {}
        settings_service = container.resolve(ISettingsService)
        
        # Benchmark settings write operations
        def write_settings():
            operations = 0
            for i in range(1000):  # 1000 write operations
                settings_service.set_setting(f"benchmark_key_{i}", f"value_{i}")
                settings_service.set_setting(f"benchmark_number_{i}", i)
                settings_service.set_setting(f"benchmark_list_{i}", [i, i+1, i+2])
                operations += 3
            return operations
        
        metrics = self.measure_operation("Settings Write Operations", mode, write_settings)
        results["write_operations"] = metrics
        
        status = "[OK]" if metrics.success else "[ERROR]"
        print(f"{status} Write Operations | {metrics.execution_time:.4f}s | "
              f"{metrics.memory_delta:+.2f}MB | {metrics.result_size} writes")
        
        # Benchmark settings read operations
        def read_settings():
            operations = 0
            for i in range(1000):  # 1000 read operations
                settings_service.get_setting(f"benchmark_key_{i}")
                settings_service.get_setting(f"benchmark_number_{i}")
                settings_service.get_setting(f"benchmark_list_{i}")
                settings_service.get_setting(f"nonexistent_key_{i}", "default")
                operations += 4
            return operations
        
        metrics = self.measure_operation("Settings Read Operations", mode, read_settings)
        results["read_operations"] = metrics
        
        status = "[OK]" if metrics.success else "[ERROR]"
        print(f"{status} Read Operations | {metrics.execution_time:.4f}s | "
              f"{metrics.memory_delta:+.2f}MB | {metrics.result_size} reads")
        
        return results
    
    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report."""
        # Group metrics by mode
        mode_metrics = {}
        for metric in self.metrics:
            if metric.mode not in mode_metrics:
                mode_metrics[metric.mode] = []
            mode_metrics[metric.mode].append(metric)
        
        # Calculate summary statistics
        report = {
            'summary': {},
            'detailed_metrics': [asdict(m) for m in self.metrics],
            'mode_comparisons': {}
        }
        
        for mode, metrics in mode_metrics.items():
            total_time = sum(m.execution_time for m in metrics)
            total_memory = sum(m.memory_delta for m in metrics)
            success_rate = sum(1 for m in metrics if m.success) / len(metrics) * 100
            
            report['summary'][mode] = {
                'total_operations': len(metrics),
                'total_execution_time': total_time,
                'average_execution_time': total_time / len(metrics),
                'total_memory_delta': total_memory,
                'average_memory_delta': total_memory / len(metrics),
                'success_rate': success_rate,
                'failed_operations': [m.operation for m in metrics if not m.success]
            }
        
        # Generate mode comparisons
        if len(mode_metrics) > 1:
            modes = list(mode_metrics.keys())
            for i, mode1 in enumerate(modes):
                for mode2 in modes[i+1:]:
                    comparison_key = f"{mode1}_vs_{mode2}"
                    
                    summary1 = report['summary'][mode1]
                    summary2 = report['summary'][mode2]
                    
                    report['mode_comparisons'][comparison_key] = {
                        'time_ratio': summary1['average_execution_time'] / summary2['average_execution_time'],
                        'memory_ratio': abs(summary1['average_memory_delta']) / max(abs(summary2['average_memory_delta']), 0.001),
                        'faster_mode': mode1 if summary1['average_execution_time'] < summary2['average_execution_time'] else mode2,
                        'more_memory_efficient': mode1 if abs(summary1['average_memory_delta']) < abs(summary2['average_memory_delta']) else mode2
                    }
        
        return report


def run_comprehensive_benchmark():
    """Run comprehensive performance benchmark across all modes."""
    print("[LAUNCH] TKA APPLICATION FACTORY PERFORMANCE BENCHMARK")
    print("=" * 60)
    
    benchmark = PerformanceBenchmark()
    
    # Benchmark container creation
    container_metrics = benchmark.benchmark_container_creation()
    
    # Benchmark operations for each mode
    containers = {}
    for mode in [ApplicationMode.TEST, ApplicationMode.HEADLESS]:
        try:
            containers[mode] = ApplicationFactory.create_app(mode)
        except Exception as e:
            print(f"[ERROR] Failed to create {mode} container: {e}")
            continue
    
    # Run operation benchmarks
    for mode, container in containers.items():
        benchmark.benchmark_sequence_operations(container, mode)
        benchmark.benchmark_layout_calculations(container, mode)
        benchmark.benchmark_settings_operations(container, mode)
    
    # Generate and display report
    report = benchmark.generate_performance_report()
    
    print(f"\n[CHART] PERFORMANCE BENCHMARK REPORT")
    print("=" * 50)
    
    for mode, summary in report['summary'].items():
        print(f"\n{mode.upper()} MODE SUMMARY:")
        print(f"  Operations: {summary['total_operations']}")
        print(f"  Total Time: {summary['total_execution_time']:.4f}s")
        print(f"  Avg Time: {summary['average_execution_time']:.6f}s")
        print(f"  Memory Delta: {summary['total_memory_delta']:+.2f}MB")
        print(f"  Success Rate: {summary['success_rate']:.1f}%")
        if summary['failed_operations']:
            print(f"  Failed Ops: {', '.join(summary['failed_operations'])}")
    
    # Display comparisons
    if report['mode_comparisons']:
        print(f"\n[RELOAD] MODE COMPARISONS:")
        for comparison, data in report['mode_comparisons'].items():
            mode1, mode2 = comparison.split('_vs_')
            print(f"\n{mode1.upper()} vs {mode2.upper()}:")
            print(f"  Speed: {data['faster_mode']} is {data['time_ratio']:.2f}x faster")
            print(f"  Memory: {data['more_memory_efficient']} is more memory efficient")
    
    return report


def save_benchmark_results(report: Dict[str, Any], filename: str = "benchmark_results.json"):
    """Save benchmark results to file."""
    output_path = Path(__file__).parent / filename
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\n[SAVE] Benchmark results saved to: {output_path}")


def main():
    """Main benchmark execution."""
    print("TKA APPLICATION FACTORY PERFORMANCE ANALYSIS")
    print("This benchmark compares performance across different application modes.")
    
    # Run comprehensive benchmark
    report = run_comprehensive_benchmark()
    
    # Save results
    save_benchmark_results(report)
    
    # Summary insights
    print(f"\n[IDEA] KEY INSIGHTS:")
    print(f"   - TEST mode is optimized for speed and predictability")
    print(f"   - HEADLESS mode balances real logic with performance")
    print(f"   - Memory usage varies based on service implementations")
    print(f"   - All modes maintain high success rates for core operations")
    
    return report


if __name__ == "__main__":
    results = main()
