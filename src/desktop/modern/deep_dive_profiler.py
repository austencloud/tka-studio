#!/usr/bin/env python3
"""
Deep Dive Startup Profiler - Granular Analysis of Main Window Creation

This profiler provides detailed timing analysis of every operation within the
TKAMainWindow creation process to identify the most expensive sub-components.

Focus Areas:
- TKAMainWindow.__init__ breakdown
- ApplicationOrchestrator.initialize_application sub-operations
- Pictograph pool initialization details
- UI Manager setup_main_ui components
- Construct tab widget creation and setup
"""

import os
import psutil
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Any
from PyQt6.QtCore import QObject

# Add the modern src directory to Python path
modern_src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(modern_src_path))

# Environment variable to enable/disable profiling
PROFILING_ENABLED = os.getenv("TKA_DEEP_DIVE_PROFILING", "1").lower() in ("1", "true", "yes")


@dataclass
class DeepDiveMetric:
    """Detailed performance metric with hierarchical context."""
    
    name: str
    start_time: float
    end_time: float
    duration_ms: float
    memory_before_mb: float
    memory_after_mb: float
    memory_delta_mb: float
    wall_clock_from_start: float
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)
    depth: int = 0
    category: str = "unknown"
    critical_path: bool = False


class DeepDiveProfiler(QObject):
    """
    Deep dive profiler for granular analysis of main window creation.
    
    Provides hierarchical timing analysis with detailed breakdown of
    every operation within the expensive main window creation process.
    """
    
    def __init__(self, enabled: bool = PROFILING_ENABLED):
        super().__init__()
        self.enabled = enabled
        self.process_start_time = time.perf_counter()
        self.metrics: Dict[str, DeepDiveMetric] = {}
        self.operation_stack: List[str] = []
        self.process = psutil.Process()
        
        # Category tracking
        self.categories = {
            "orchestrator": [],
            "lifecycle": [],
            "services": [],
            "pictograph_pool": [],
            "ui_manager": [],
            "construct_tab": [],
            "option_picker": [],
            "session": [],
            "background": []
        }
        
        if self.enabled:
            print("🔬 Deep Dive Profiler ENABLED")
            print("   Granular analysis of main window creation")
        else:
            print("⚪ Deep Dive Profiler DISABLED")
    
    def _get_memory_usage_mb(self) -> float:
        """Get current memory usage in MB."""
        if not self.enabled:
            return 0.0
        try:
            return self.process.memory_info().rss / 1024 / 1024
        except:
            return 0.0
    
    def _get_wall_clock_from_start(self) -> float:
        """Get wall-clock time in milliseconds from process start."""
        return (time.perf_counter() - self.process_start_time) * 1000
    
    def _categorize_operation(self, operation_name: str) -> str:
        """Categorize operation based on name patterns."""
        name_lower = operation_name.lower()
        
        if "orchestrator" in name_lower:
            return "orchestrator"
        elif "lifecycle" in name_lower:
            return "lifecycle"
        elif "service" in name_lower or "registration" in name_lower:
            return "services"
        elif "pictograph" in name_lower and "pool" in name_lower:
            return "pictograph_pool"
        elif "ui" in name_lower and ("manager" in name_lower or "setup" in name_lower):
            return "ui_manager"
        elif "construct" in name_lower and "tab" in name_lower:
            return "construct_tab"
        elif "option" in name_lower and "picker" in name_lower:
            return "option_picker"
        elif "session" in name_lower:
            return "session"
        elif "background" in name_lower:
            return "background"
        else:
            return "unknown"
    
    @contextmanager
    def time_operation(self, operation_name: str, category: str = None, critical_path: bool = False):
        """Context manager for timing operations with hierarchical tracking."""
        if not self.enabled:
            yield
            return
            
        # Determine parent and depth
        parent = self.operation_stack[-1] if self.operation_stack else None
        depth = len(self.operation_stack)
        
        # Auto-categorize if not specified
        if category is None:
            category = self._categorize_operation(operation_name)
        
        # Add to operation stack
        self.operation_stack.append(operation_name)
        
        start_time = time.perf_counter()
        memory_before = self._get_memory_usage_mb()
        wall_clock_start = self._get_wall_clock_from_start()
        
        try:
            yield
        finally:
            end_time = time.perf_counter()
            memory_after = self._get_memory_usage_mb()
            duration_ms = (end_time - start_time) * 1000
            wall_clock_end = self._get_wall_clock_from_start()
            
            # Create metric
            metric = DeepDiveMetric(
                name=operation_name,
                start_time=start_time,
                end_time=end_time,
                duration_ms=duration_ms,
                memory_before_mb=memory_before,
                memory_after_mb=memory_after,
                memory_delta_mb=memory_after - memory_before,
                wall_clock_from_start=wall_clock_start,
                parent=parent,
                depth=depth,
                category=category,
                critical_path=critical_path
            )
            
            self.metrics[operation_name] = metric
            
            # Add to category tracking
            if category in self.categories:
                self.categories[category].append(operation_name)
            
            # Update parent-child relationships
            if parent and parent in self.metrics:
                self.metrics[parent].children.append(operation_name)
            
            # Remove from operation stack
            self.operation_stack.pop()
            
            # Real-time output with hierarchy
            indent = "  " * depth
            memory_info = f" (+{memory_after - memory_before:.1f}MB)" if memory_after - memory_before > 1 else ""
            critical_info = " [CRITICAL PATH]" if critical_path else ""
            category_info = f" [{category.upper()}]" if category != "unknown" else ""
            
            print(f"🔬 {indent}t+{wall_clock_end:.1f}ms: {operation_name}: {duration_ms:.1f}ms{memory_info}{critical_info}{category_info}")
    
    def generate_deep_dive_report(self):
        """Generate comprehensive deep dive analysis report."""
        if not self.enabled:
            return
            
        total_time = self._get_wall_clock_from_start()
        
        print("\n" + "=" * 80)
        print("🔬 DEEP DIVE STARTUP PERFORMANCE ANALYSIS")
        print("=" * 80)
        print(f"🎯 TOTAL ANALYSIS TIME: {total_time:.1f}ms")
        print(f"💾 Final Memory Usage: {self._get_memory_usage_mb():.1f}MB")
        
        # Hierarchical analysis
        self._analyze_hierarchy()
        
        # Category analysis
        self._analyze_categories()
        
        # Critical path analysis
        self._analyze_critical_path()
        
        # Bottleneck identification
        self._identify_bottlenecks()
        
        # Optimization recommendations
        self._generate_deep_dive_recommendations()
    
    def _analyze_hierarchy(self):
        """Analyze timing hierarchy and parent-child relationships."""
        print("\n📊 HIERARCHICAL TIMING ANALYSIS:")
        
        # Find root operations (no parent)
        root_operations = [m for m in self.metrics.values() if m.parent is None]
        
        for root in sorted(root_operations, key=lambda x: x.duration_ms, reverse=True):
            self._print_hierarchy_tree(root, 0)
    
    def _print_hierarchy_tree(self, metric: DeepDiveMetric, depth: int):
        """Print hierarchical tree of operations."""
        indent = "  " * depth
        percentage = (metric.duration_ms / sum(m.duration_ms for m in self.metrics.values())) * 100
        memory_info = f" (+{metric.memory_delta_mb:.1f}MB)" if metric.memory_delta_mb > 1 else ""
        critical_info = " [CRITICAL]" if metric.critical_path else ""
        
        print(f"   {indent}├─ {metric.name}: {metric.duration_ms:.1f}ms ({percentage:.1f}%){memory_info}{critical_info}")
        
        # Print children
        for child_name in metric.children:
            if child_name in self.metrics:
                child_metric = self.metrics[child_name]
                self._print_hierarchy_tree(child_metric, depth + 1)
    
    def _analyze_categories(self):
        """Analyze performance by category."""
        print("\n📈 CATEGORY PERFORMANCE ANALYSIS:")
        
        category_totals = {}
        for category, operations in self.categories.items():
            total_time = sum(self.metrics[op].duration_ms for op in operations if op in self.metrics)
            if total_time > 0:
                category_totals[category] = total_time
        
        # Sort by total time
        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        
        for category, total_time in sorted_categories:
            operations = self.categories[category]
            operation_count = len([op for op in operations if op in self.metrics])
            avg_time = total_time / operation_count if operation_count > 0 else 0
            
            print(f"   {category.upper():<15} {total_time:>8.1f}ms ({operation_count} ops, avg: {avg_time:.1f}ms)")
    
    def _analyze_critical_path(self):
        """Analyze critical path operations."""
        print("\n🎯 CRITICAL PATH ANALYSIS:")
        
        critical_operations = [m for m in self.metrics.values() if m.critical_path]
        if critical_operations:
            total_critical_time = sum(op.duration_ms for op in critical_operations)
            
            print(f"   Total critical path time: {total_critical_time:.1f}ms")
            
            for op in sorted(critical_operations, key=lambda x: x.duration_ms, reverse=True):
                percentage = (op.duration_ms / total_critical_time) * 100
                print(f"   • {op.name}: {op.duration_ms:.1f}ms ({percentage:.1f}%)")
        else:
            print("   No operations marked as critical path")
    
    def _identify_bottlenecks(self):
        """Identify performance bottlenecks."""
        print("\n⚠️  PERFORMANCE BOTTLENECKS:")
        
        # Sort all operations by duration
        sorted_operations = sorted(self.metrics.values(), key=lambda x: x.duration_ms, reverse=True)
        
        # Identify bottlenecks (>500ms or >10% of total time)
        total_time = sum(m.duration_ms for m in self.metrics.values())
        bottlenecks = [
            op for op in sorted_operations 
            if op.duration_ms > 500 or (op.duration_ms / total_time) > 0.1
        ]
        
        if bottlenecks:
            for op in bottlenecks[:10]:  # Top 10 bottlenecks
                percentage = (op.duration_ms / total_time) * 100
                memory_info = f" (+{op.memory_delta_mb:.1f}MB)" if op.memory_delta_mb > 5 else ""
                category_info = f" [{op.category.upper()}]"
                
                print(f"   • {op.name:<50} {op.duration_ms:>8.1f}ms ({percentage:>5.1f}%){memory_info}{category_info}")
        else:
            print("   ✅ No major bottlenecks detected")
    
    def _generate_deep_dive_recommendations(self):
        """Generate specific optimization recommendations based on deep analysis."""
        print("\n💡 DEEP DIVE OPTIMIZATION RECOMMENDATIONS:")
        
        recommendations = []
        
        # Analyze category performance
        category_totals = {}
        for category, operations in self.categories.items():
            total_time = sum(self.metrics[op].duration_ms for op in operations if op in self.metrics)
            if total_time > 0:
                category_totals[category] = total_time
        
        # Generate category-specific recommendations
        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        
        for category, total_time in sorted_categories[:3]:  # Top 3 categories
            if total_time > 1000:  # Categories taking >1 second
                if category == "pictograph_pool":
                    recommendations.append(f"🎯 PICTOGRAPH POOL OPTIMIZATION ({total_time:.1f}ms):")
                    recommendations.append("   • Move pool initialization to background thread")
                    recommendations.append("   • Implement lazy pool creation (create on first use)")
                    recommendations.append("   • Use smaller initial pool size, expand as needed")
                    
                elif category == "construct_tab":
                    recommendations.append(f"🎯 CONSTRUCT TAB OPTIMIZATION ({total_time:.1f}ms):")
                    recommendations.append("   • Defer construct tab creation until first access")
                    recommendations.append("   • Use placeholder widget during initial load")
                    recommendations.append("   • Load option picker components progressively")
                    
                elif category == "ui_manager":
                    recommendations.append(f"🎯 UI MANAGER OPTIMIZATION ({total_time:.1f}ms):")
                    recommendations.append("   • Split UI creation into phases")
                    recommendations.append("   • Show window shell first, load tabs incrementally")
                    recommendations.append("   • Use virtual widgets for heavy components")
        
        if not recommendations:
            recommendations.append("✅ No major category-specific optimizations identified")
        
        for rec in recommendations:
            print(f"   {rec}")


# Global profiler instance
deep_dive_profiler = DeepDiveProfiler()
