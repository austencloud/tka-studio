#!/usr/bin/env python3
"""
TKA Workflow Scenarios Demo

Demonstrates realistic TKA workflows using different application modes,
showing how the same operations work differently in test vs production environments.
"""

import sys
import time
import json
from pathlib import Path
from typing import List, Dict, Any

# Add TKA modern src to path
tka_src_path = Path(__file__).parent.parent / "src" / "desktop" / "modern" / "src"
sys.path.insert(0, str(tka_src_path))

from core.application.application_factory import ApplicationFactory, ApplicationMode
from core.interfaces.core_services import (
    ISequenceDataService,
    ILayoutService,
    ISettingsService,
    ISequenceManagementService,
    IPictographManagementService,
    IUIStateManagementService
)


class TKAWorkflowDemo:
    """Demonstrates realistic TKA workflows across different application modes."""
    
    def __init__(self, mode: str):
        self.mode = mode
        self.container = ApplicationFactory.create_app(mode)
        self.results = {}
        
    def print_workflow_header(self, workflow_name: str):
        """Print workflow header."""
        print(f"\n{'='*60}")
        print(f"  {workflow_name} - {self.mode.upper()} MODE")
        print(f"{'='*60}")
    
    def sequence_creation_workflow(self) -> Dict[str, Any]:
        """Demonstrate sequence creation and management workflow."""
        self.print_workflow_header("SEQUENCE CREATION WORKFLOW")
        
        results = {
            'sequences_created': 0,
            'total_beats': 0,
            'creation_times': [],
            'errors': []
        }
        
        try:
            # Get services
            seq_data_service = self.container.resolve(ISequenceDataService)
            seq_mgmt_service = self.container.resolve(ISequenceManagementService)
            
            print("🎵 Creating multiple sequences with different characteristics...")
            
            # Create different types of sequences
            sequence_configs = [
                {"name": "Basic Sequence", "length": 8},
                {"name": "Standard Sequence", "length": 16},
                {"name": "Extended Sequence", "length": 32},
                {"name": "Complex Sequence", "length": 64}
            ]
            
            for config in sequence_configs:
                start_time = time.time()
                
                # Create sequence using management service
                sequence = seq_mgmt_service.create_sequence(
                    config["name"], 
                    config["length"]
                )
                
                # Save using data service
                seq_data_service.save_sequence({
                    'id': sequence.get('id', f"seq_{results['sequences_created']}"),
                    'name': config["name"],
                    'length': config["length"],
                    'beats': sequence.get('beats', []),
                    'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
                })
                
                creation_time = time.time() - start_time
                results['creation_times'].append(creation_time)
                results['sequences_created'] += 1
                results['total_beats'] += config["length"]
                
                print(f"  ✅ {config['name']}: {config['length']} beats, "
                      f"created in {creation_time:.4f}s")
            
            # Retrieve and display all sequences
            all_sequences = seq_data_service.get_all_sequences()
            print(f"\n📊 Summary:")
            print(f"  - Total sequences created: {len(all_sequences)}")
            print(f"  - Average creation time: {sum(results['creation_times'])/len(results['creation_times']):.4f}s")
            print(f"  - Total beats across all sequences: {results['total_beats']}")
            
            # Test sequence operations
            if all_sequences:
                test_sequence = all_sequences[0]
                print(f"\n🔧 Testing operations on '{test_sequence['name']}':")
                
                # Add beats to sequence
                for i in range(min(4, test_sequence.get('length', 0))):
                    beat_data = {
                        'beat_number': i + 1,
                        'letter': chr(65 + i),  # A, B, C, D
                        'duration': 1.0
                    }
                    seq_mgmt_service.add_beat(test_sequence, beat_data, i)
                    print(f"  ➕ Added beat {i+1}: {beat_data['letter']}")
                
                # Save updated sequence
                seq_data_service.save_sequence(test_sequence)
                print(f"  💾 Sequence updated and saved")
            
        except Exception as e:
            error_msg = f"Sequence workflow error: {e}"
            results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
        
        self.results['sequence_workflow'] = results
        return results
    
    def layout_calculation_workflow(self) -> Dict[str, Any]:
        """Demonstrate layout calculation workflow."""
        self.print_workflow_header("LAYOUT CALCULATION WORKFLOW")
        
        results = {
            'calculations_performed': 0,
            'calculation_times': [],
            'layout_configs': [],
            'errors': []
        }
        
        try:
            layout_service = self.container.resolve(ILayoutService)
            
            print("📐 Performing layout calculations for different scenarios...")
            
            # Test different container sizes (simulating different screen resolutions)
            test_scenarios = [
                {"name": "Mobile", "size": (800, 600)},
                {"name": "Laptop", "size": (1366, 768)},
                {"name": "Desktop", "size": (1920, 1080)},
                {"name": "4K Monitor", "size": (3840, 2160)}
            ]
            
            for scenario in test_scenarios:
                start_time = time.time()
                
                container_size = scenario["size"]
                
                # Calculate optimal grid layout
                grid_16 = layout_service.get_optimal_grid_layout(16, container_size)
                grid_32 = layout_service.get_optimal_grid_layout(32, container_size)
                
                # Calculate component sizes
                window_size = layout_service.get_main_window_size()
                beat_size = layout_service.calculate_component_size("beat_frame", window_size)
                pictograph_size = layout_service.calculate_component_size("pictograph", window_size)
                
                # Calculate responsive scaling
                scaling_factor = layout_service.calculate_responsive_scaling(
                    (1920, 1080), container_size
                )
                
                calc_time = time.time() - start_time
                
                layout_config = {
                    'scenario': scenario["name"],
                    'container_size': container_size,
                    'grid_16_items': grid_16,
                    'grid_32_items': grid_32,
                    'beat_frame_size': (beat_size.width, beat_size.height),
                    'pictograph_size': (pictograph_size.width, pictograph_size.height),
                    'scaling_factor': scaling_factor,
                    'calculation_time': calc_time
                }
                
                results['layout_configs'].append(layout_config)
                results['calculation_times'].append(calc_time)
                results['calculations_performed'] += 1
                
                print(f"  📱 {scenario['name']} ({container_size[0]}x{container_size[1]}):")
                print(f"     Grid 16: {grid_16[0]}x{grid_16[1]}, Grid 32: {grid_32[0]}x{grid_32[1]}")
                print(f"     Beat: {beat_size.width}x{beat_size.height}, Scale: {scaling_factor:.2f}")
                print(f"     Calculated in {calc_time:.4f}s")
            
            # Performance summary
            avg_time = sum(results['calculation_times']) / len(results['calculation_times'])
            print(f"\n⚡ Performance Summary:")
            print(f"  - Total calculations: {results['calculations_performed']}")
            print(f"  - Average calculation time: {avg_time:.4f}s")
            print(f"  - Fastest: {min(results['calculation_times']):.4f}s")
            print(f"  - Slowest: {max(results['calculation_times']):.4f}s")
            
        except Exception as e:
            error_msg = f"Layout workflow error: {e}"
            results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
        
        self.results['layout_workflow'] = results
        return results
    
    def settings_management_workflow(self) -> Dict[str, Any]:
        """Demonstrate settings management workflow."""
        self.print_workflow_header("SETTINGS MANAGEMENT WORKFLOW")
        
        results = {
            'settings_set': 0,
            'settings_retrieved': 0,
            'persistence_tested': False,
            'errors': []
        }
        
        try:
            settings_service = self.container.resolve(ISettingsService)
            ui_state_service = self.container.resolve(IUIStateManagementService)
            
            print("⚙️ Managing application settings and UI state...")
            
            # Set various types of settings
            settings_to_test = {
                'user_preferences': {
                    'theme': 'dark',
                    'auto_save': True,
                    'default_sequence_length': 16,
                    'recent_files': ['seq1.tka', 'seq2.tka', 'seq3.tka']
                },
                'layout_settings': {
                    'window_width': 1920,
                    'window_height': 1080,
                    'layout_ratio': [3, 1],
                    'show_grid': True
                },
                'performance_settings': {
                    'animation_fps': 60,
                    'render_quality': 'high',
                    'cache_size_mb': 256
                }
            }
            
            # Set settings
            for category, settings in settings_to_test.items():
                print(f"\n📝 Setting {category}:")
                for key, value in settings.items():
                    full_key = f"{category}.{key}"
                    settings_service.set_setting(full_key, value)
                    results['settings_set'] += 1
                    print(f"  ✅ {full_key} = {value}")
            
            # Retrieve and verify settings
            print(f"\n🔍 Retrieving and verifying settings:")
            for category, settings in settings_to_test.items():
                for key, expected_value in settings.items():
                    full_key = f"{category}.{key}"
                    retrieved_value = settings_service.get_setting(full_key)
                    results['settings_retrieved'] += 1
                    
                    if retrieved_value == expected_value:
                        print(f"  ✅ {full_key}: {retrieved_value}")
                    else:
                        print(f"  ❌ {full_key}: expected {expected_value}, got {retrieved_value}")
            
            # Test UI state management
            print(f"\n🖥️ Testing UI state management:")
            ui_state_service.set_setting('current_tab', 'sequence_builder')
            ui_state_service.set_setting('sidebar_width', 300)
            
            current_tab = ui_state_service.get_setting('current_tab')
            sidebar_width = ui_state_service.get_setting('sidebar_width')
            
            print(f"  📑 Current tab: {current_tab}")
            print(f"  📏 Sidebar width: {sidebar_width}px")
            
            # Test graph editor toggle
            graph_visible = ui_state_service.toggle_graph_editor()
            print(f"  🎨 Graph editor visible: {graph_visible}")
            
            # Test persistence
            print(f"\n💾 Testing settings persistence:")
            try:
                settings_service.save_settings()
                settings_service.load_settings()
                results['persistence_tested'] = True
                print(f"  ✅ Settings save/load completed successfully")
                
                # Verify settings persist after save/load
                test_value = settings_service.get_setting('user_preferences.theme')
                if test_value == 'dark':
                    print(f"  ✅ Settings persisted correctly: theme = {test_value}")
                else:
                    print(f"  ⚠️ Settings may not have persisted: theme = {test_value}")
                    
            except Exception as e:
                print(f"  ⚠️ Persistence test: {e} (expected in test mode)")
            
        except Exception as e:
            error_msg = f"Settings workflow error: {e}"
            results['errors'].append(error_msg)
            print(f"❌ {error_msg}")
        
        self.results['settings_workflow'] = results
        return results
    
    def run_all_workflows(self) -> Dict[str, Any]:
        """Run all workflow demonstrations."""
        print(f"\n🚀 RUNNING ALL TKA WORKFLOWS IN {self.mode.upper()} MODE")
        print(f"{'='*80}")
        
        start_time = time.time()
        
        # Run each workflow
        self.sequence_creation_workflow()
        self.layout_calculation_workflow()
        self.settings_management_workflow()
        
        total_time = time.time() - start_time
        
        # Summary
        print(f"\n📊 WORKFLOW EXECUTION SUMMARY - {self.mode.upper()} MODE")
        print(f"{'='*60}")
        print(f"⏱️  Total execution time: {total_time:.4f}s")
        print(f"🎵 Sequences created: {self.results.get('sequence_workflow', {}).get('sequences_created', 0)}")
        print(f"📐 Layout calculations: {self.results.get('layout_workflow', {}).get('calculations_performed', 0)}")
        print(f"⚙️  Settings managed: {self.results.get('settings_workflow', {}).get('settings_set', 0)}")
        
        # Error summary
        total_errors = sum(len(workflow.get('errors', [])) for workflow in self.results.values())
        if total_errors > 0:
            print(f"❌ Total errors: {total_errors}")
        else:
            print(f"✅ All workflows completed successfully!")
        
        self.results['summary'] = {
            'mode': self.mode,
            'total_time': total_time,
            'total_errors': total_errors,
            'completed_successfully': total_errors == 0
        }
        
        return self.results


def compare_workflow_performance():
    """Compare workflow performance across different modes."""
    print(f"\n{'='*80}")
    print(f"  CROSS-MODE WORKFLOW PERFORMANCE COMPARISON")
    print(f"{'='*80}")
    
    modes_to_test = [ApplicationMode.TEST, ApplicationMode.HEADLESS]
    
    # Add production mode if available
    try:
        ApplicationFactory.create_app(ApplicationMode.PRODUCTION)
        modes_to_test.append(ApplicationMode.PRODUCTION)
    except Exception:
        print("⚠️ Production mode not available for comparison")
    
    results = {}
    
    for mode in modes_to_test:
        print(f"\n🔄 Running workflows in {mode} mode...")
        try:
            demo = TKAWorkflowDemo(mode)
            results[mode] = demo.run_all_workflows()
        except Exception as e:
            print(f"❌ Failed to run {mode} workflows: {e}")
            results[mode] = None
    
    # Performance comparison table
    print(f"\n📊 PERFORMANCE COMPARISON TABLE")
    print(f"{'='*80}")
    print(f"{'Mode':<12} | {'Time (s)':<10} | {'Sequences':<10} | {'Layouts':<8} | {'Settings':<8} | {'Errors':<6}")
    print(f"{'-'*12} | {'-'*10} | {'-'*10} | {'-'*8} | {'-'*8} | {'-'*6}")
    
    for mode, result in results.items():
        if result is None:
            print(f"{mode:<12} | {'FAILED':<10} | {'-':<10} | {'-':<8} | {'-':<8} | {'-':<6}")
            continue
            
        summary = result.get('summary', {})
        seq_count = result.get('sequence_workflow', {}).get('sequences_created', 0)
        layout_count = result.get('layout_workflow', {}).get('calculations_performed', 0)
        settings_count = result.get('settings_workflow', {}).get('settings_set', 0)
        
        print(f"{mode:<12} | {summary.get('total_time', 0):<10.4f} | "
              f"{seq_count:<10} | {layout_count:<8} | {settings_count:<8} | "
              f"{summary.get('total_errors', 0):<6}")
    
    return results


def main():
    """Main demonstration function."""
    print("TKA WORKFLOW SCENARIOS DEMONSTRATION")
    print("This demo shows realistic TKA workflows across different application modes.")
    
    # Run individual mode demonstrations
    individual_results = {}
    
    for mode in [ApplicationMode.TEST, ApplicationMode.HEADLESS]:
        try:
            demo = TKAWorkflowDemo(mode)
            individual_results[mode] = demo.run_all_workflows()
        except Exception as e:
            print(f"❌ Failed to run {mode} demo: {e}")
    
    # Run cross-mode comparison
    comparison_results = compare_workflow_performance()
    
    return {
        'individual': individual_results,
        'comparison': comparison_results
    }


if __name__ == "__main__":
    results = main()
