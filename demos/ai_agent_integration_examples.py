#!/usr/bin/env python3
"""
AI Agent Integration Examples

Demonstrates how AI agents and external tools can use the TKA Application Factory
for automated testing, batch processing, and integration workflows.
"""

import sys
import time
import json
import random
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

# Add TKA modern src to path
tka_src_path = Path(__file__).parent.parent / "src" / "desktop" / "modern" / "src"
sys.path.insert(0, str(tka_src_path))

from core.application.application_factory import ApplicationFactory, ApplicationMode
from core.interfaces.core_services import (
    ISequenceDataService,
    ILayoutService,
    ISequenceManagementService,
    IPictographManagementService,
    IValidationService
)


@dataclass
class TestResult:
    """Represents a test result."""
    test_name: str
    success: bool
    duration: float
    details: Dict[str, Any]
    error_message: Optional[str] = None


class TKATestAgent:
    """AI Agent for automated TKA testing."""
    
    def __init__(self, mode: str = ApplicationMode.TEST):
        self.mode = mode
        self.container = None
        self.test_results: List[TestResult] = []
        
    def initialize(self) -> bool:
        """Initialize the test agent."""
        try:
            print(f"🤖 Initializing TKA Test Agent in {self.mode} mode...")
            self.container = ApplicationFactory.create_app(self.mode)
            print(f"✅ Agent initialized successfully")
            return True
        except Exception as e:
            print(f"❌ Agent initialization failed: {e}")
            return False
    
    def run_sequence_validation_tests(self) -> List[TestResult]:
        """Run automated sequence validation tests."""
        print(f"\n🧪 Running sequence validation tests...")
        
        test_cases = [
            {"name": "Valid Basic Sequence", "length": 8, "should_pass": True},
            {"name": "Valid Standard Sequence", "length": 16, "should_pass": True},
            {"name": "Valid Extended Sequence", "length": 32, "should_pass": True},
            {"name": "Edge Case - Single Beat", "length": 1, "should_pass": True},
            {"name": "Edge Case - Maximum Length", "length": 64, "should_pass": True},
        ]
        
        results = []
        seq_service = self.container.resolve(ISequenceManagementService)
        validation_service = self.container.resolve(IValidationService)
        
        for test_case in test_cases:
            start_time = time.time()
            
            try:
                # Create sequence
                sequence = seq_service.create_sequence(
                    test_case["name"], 
                    test_case["length"]
                )
                
                # Validate sequence
                is_valid = validation_service.validate_sequence({
                    'name': test_case["name"],
                    'length': test_case["length"],
                    'beats': sequence.get('beats', [])
                })
                
                duration = time.time() - start_time
                success = is_valid == test_case["should_pass"]
                
                result = TestResult(
                    test_name=test_case["name"],
                    success=success,
                    duration=duration,
                    details={
                        'expected_valid': test_case["should_pass"],
                        'actual_valid': is_valid,
                        'sequence_length': test_case["length"],
                        'sequence_id': sequence.get('id', 'unknown')
                    }
                )
                
                status = "✅ PASS" if success else "❌ FAIL"
                print(f"  {status} {test_case['name']}: {duration:.4f}s")
                
            except Exception as e:
                duration = time.time() - start_time
                result = TestResult(
                    test_name=test_case["name"],
                    success=False,
                    duration=duration,
                    details={'error': str(e)},
                    error_message=str(e)
                )
                print(f"  ❌ ERROR {test_case['name']}: {e}")
            
            results.append(result)
            self.test_results.append(result)
        
        return results
    
    def run_layout_performance_tests(self) -> List[TestResult]:
        """Run automated layout performance tests."""
        print(f"\n⚡ Running layout performance tests...")
        
        test_scenarios = [
            {"name": "Mobile Layout", "size": (800, 600), "items": 16},
            {"name": "Tablet Layout", "size": (1024, 768), "items": 24},
            {"name": "Desktop Layout", "size": (1920, 1080), "items": 32},
            {"name": "4K Layout", "size": (3840, 2160), "items": 64},
        ]
        
        results = []
        layout_service = self.container.resolve(ILayoutService)
        
        for scenario in test_scenarios:
            start_time = time.time()
            
            try:
                # Perform multiple layout calculations
                calculations = []
                for _ in range(10):  # Run 10 iterations for average
                    calc_start = time.time()
                    grid_layout = layout_service.get_optimal_grid_layout(
                        scenario["items"], 
                        scenario["size"]
                    )
                    calc_time = time.time() - calc_start
                    calculations.append(calc_time)
                
                duration = time.time() - start_time
                avg_calc_time = sum(calculations) / len(calculations)
                
                # Performance criteria: should complete in reasonable time
                success = avg_calc_time < 0.01  # Less than 10ms per calculation
                
                result = TestResult(
                    test_name=scenario["name"],
                    success=success,
                    duration=duration,
                    details={
                        'container_size': scenario["size"],
                        'item_count': scenario["items"],
                        'avg_calculation_time': avg_calc_time,
                        'total_calculations': len(calculations),
                        'performance_threshold': 0.01
                    }
                )
                
                status = "✅ PASS" if success else "❌ FAIL"
                print(f"  {status} {scenario['name']}: avg {avg_calc_time:.6f}s per calc")
                
            except Exception as e:
                duration = time.time() - start_time
                result = TestResult(
                    test_name=scenario["name"],
                    success=False,
                    duration=duration,
                    details={'error': str(e)},
                    error_message=str(e)
                )
                print(f"  ❌ ERROR {scenario['name']}: {e}")
            
            results.append(result)
            self.test_results.append(result)
        
        return results
    
    def run_data_persistence_tests(self) -> List[TestResult]:
        """Run automated data persistence tests."""
        print(f"\n💾 Running data persistence tests...")
        
        results = []
        seq_data_service = self.container.resolve(ISequenceDataService)
        
        # Test sequence CRUD operations
        test_sequences = [
            {"name": "Test Sequence 1", "beats": 8},
            {"name": "Test Sequence 2", "beats": 16},
            {"name": "Test Sequence 3", "beats": 24},
        ]
        
        created_sequences = []
        
        # CREATE tests
        for seq_config in test_sequences:
            start_time = time.time()
            
            try:
                sequence = seq_data_service.create_new_sequence(seq_config["name"])
                saved = seq_data_service.save_sequence(sequence)
                
                duration = time.time() - start_time
                success = saved and sequence['name'] == seq_config["name"]
                
                if success:
                    created_sequences.append(sequence)
                
                result = TestResult(
                    test_name=f"CREATE {seq_config['name']}",
                    success=success,
                    duration=duration,
                    details={
                        'sequence_name': seq_config["name"],
                        'saved_successfully': saved,
                        'sequence_id': sequence.get('id', 'unknown')
                    }
                )
                
                status = "✅ PASS" if success else "❌ FAIL"
                print(f"  {status} CREATE {seq_config['name']}: {duration:.4f}s")
                
            except Exception as e:
                duration = time.time() - start_time
                result = TestResult(
                    test_name=f"CREATE {seq_config['name']}",
                    success=False,
                    duration=duration,
                    details={'error': str(e)},
                    error_message=str(e)
                )
                print(f"  ❌ ERROR CREATE {seq_config['name']}: {e}")
            
            results.append(result)
            self.test_results.append(result)
        
        # READ tests
        start_time = time.time()
        try:
            all_sequences = seq_data_service.get_all_sequences()
            duration = time.time() - start_time
            
            success = len(all_sequences) >= len(created_sequences)
            
            result = TestResult(
                test_name="READ All Sequences",
                success=success,
                duration=duration,
                details={
                    'sequences_found': len(all_sequences),
                    'sequences_expected': len(created_sequences)
                }
            )
            
            status = "✅ PASS" if success else "❌ FAIL"
            print(f"  {status} READ All Sequences: found {len(all_sequences)}, {duration:.4f}s")
            
        except Exception as e:
            duration = time.time() - start_time
            result = TestResult(
                test_name="READ All Sequences",
                success=False,
                duration=duration,
                details={'error': str(e)},
                error_message=str(e)
            )
            print(f"  ❌ ERROR READ All Sequences: {e}")
        
        results.append(result)
        self.test_results.append(result)
        
        return results
    
    def generate_test_report(self) -> Dict[str, Any]:
        """Generate a comprehensive test report."""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result.success)
        failed_tests = total_tests - passed_tests
        
        total_duration = sum(result.duration for result in self.test_results)
        avg_duration = total_duration / total_tests if total_tests > 0 else 0
        
        report = {
            'summary': {
                'mode': self.mode,
                'total_tests': total_tests,
                'passed': passed_tests,
                'failed': failed_tests,
                'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
                'total_duration': total_duration,
                'average_duration': avg_duration
            },
            'test_results': [
                {
                    'name': result.test_name,
                    'success': result.success,
                    'duration': result.duration,
                    'details': result.details,
                    'error': result.error_message
                }
                for result in self.test_results
            ]
        }
        
        return report


class TKABatchProcessor:
    """AI Agent for batch processing TKA sequences."""
    
    def __init__(self, mode: str = ApplicationMode.HEADLESS):
        self.mode = mode
        self.container = ApplicationFactory.create_app(mode)
        
    def process_sequence_batch(self, sequence_configs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process a batch of sequences."""
        print(f"\n🔄 Processing batch of {len(sequence_configs)} sequences in {self.mode} mode...")
        
        seq_service = self.container.resolve(ISequenceManagementService)
        data_service = self.container.resolve(ISequenceDataService)
        
        results = {
            'processed': 0,
            'successful': 0,
            'failed': 0,
            'total_time': 0,
            'sequences': []
        }
        
        start_time = time.time()
        
        for i, config in enumerate(sequence_configs):
            try:
                print(f"  📝 Processing sequence {i+1}/{len(sequence_configs)}: {config['name']}")
                
                # Create sequence
                sequence = seq_service.create_sequence(config['name'], config.get('length', 16))
                
                # Add beats if specified
                if 'beats' in config:
                    for beat_idx, beat_data in enumerate(config['beats']):
                        seq_service.add_beat(sequence, beat_data, beat_idx)
                
                # Save sequence
                data_service.save_sequence({
                    'id': sequence.get('id', f"batch_{i}"),
                    'name': config['name'],
                    'length': config.get('length', 16),
                    'beats': sequence.get('beats', []),
                    'batch_processed': True
                })
                
                results['sequences'].append({
                    'name': config['name'],
                    'status': 'success',
                    'id': sequence.get('id', f"batch_{i}")
                })
                results['successful'] += 1
                print(f"    ✅ Success")
                
            except Exception as e:
                results['sequences'].append({
                    'name': config['name'],
                    'status': 'failed',
                    'error': str(e)
                })
                results['failed'] += 1
                print(f"    ❌ Failed: {e}")
            
            results['processed'] += 1
        
        results['total_time'] = time.time() - start_time
        
        print(f"\n📊 Batch processing complete:")
        print(f"  - Processed: {results['processed']}")
        print(f"  - Successful: {results['successful']}")
        print(f"  - Failed: {results['failed']}")
        print(f"  - Total time: {results['total_time']:.4f}s")
        print(f"  - Average time per sequence: {results['total_time']/results['processed']:.4f}s")
        
        return results


def demonstrate_ai_agent_testing():
    """Demonstrate AI agent automated testing."""
    print("🤖 AI AGENT AUTOMATED TESTING DEMONSTRATION")
    print("="*60)
    
    # Initialize test agent
    agent = TKATestAgent(ApplicationMode.TEST)
    if not agent.initialize():
        return None
    
    # Run test suites
    validation_results = agent.run_sequence_validation_tests()
    performance_results = agent.run_layout_performance_tests()
    persistence_results = agent.run_data_persistence_tests()
    
    # Generate report
    report = agent.generate_test_report()
    
    print(f"\n📋 TEST EXECUTION REPORT")
    print(f"="*40)
    print(f"Mode: {report['summary']['mode']}")
    print(f"Total Tests: {report['summary']['total_tests']}")
    print(f"Passed: {report['summary']['passed']}")
    print(f"Failed: {report['summary']['failed']}")
    print(f"Success Rate: {report['summary']['success_rate']:.1f}%")
    print(f"Total Duration: {report['summary']['total_duration']:.4f}s")
    print(f"Average Duration: {report['summary']['average_duration']:.4f}s")
    
    return report


def demonstrate_batch_processing():
    """Demonstrate batch processing capabilities."""
    print("\n🔄 BATCH PROCESSING DEMONSTRATION")
    print("="*50)
    
    # Create sample sequence configurations
    sequence_configs = [
        {
            'name': f'Generated Sequence {i+1}',
            'length': random.choice([8, 16, 24, 32]),
            'beats': [
                {
                    'beat_number': j+1,
                    'letter': chr(65 + (j % 26)),
                    'duration': random.choice([0.5, 1.0, 1.5, 2.0])
                }
                for j in range(random.randint(2, 8))
            ]
        }
        for i in range(10)
    ]
    
    # Process batch
    processor = TKABatchProcessor(ApplicationMode.HEADLESS)
    results = processor.process_sequence_batch(sequence_configs)
    
    return results


def main():
    """Main demonstration function."""
    print("TKA AI AGENT INTEGRATION EXAMPLES")
    print("This demo shows how AI agents can use the Application Factory")
    print("for automated testing and batch processing.")
    
    # Run demonstrations
    test_report = demonstrate_ai_agent_testing()
    batch_results = demonstrate_batch_processing()
    
    # Summary
    print(f"\n🎯 INTEGRATION DEMONSTRATION SUMMARY")
    print(f"="*50)
    print(f"✅ Automated Testing: {test_report['summary']['success_rate']:.1f}% success rate" if test_report else "❌ Testing failed")
    print(f"✅ Batch Processing: {batch_results['successful']}/{batch_results['processed']} sequences processed" if batch_results else "❌ Batch processing failed")
    print(f"\n💡 The Application Factory enables AI agents to:")
    print(f"   - Run comprehensive automated tests")
    print(f"   - Process sequences in batch mode")
    print(f"   - Integrate with TKA without UI dependencies")
    print(f"   - Switch between test and production modes seamlessly")
    
    return {
        'test_report': test_report,
        'batch_results': batch_results
    }


if __name__ == "__main__":
    results = main()
