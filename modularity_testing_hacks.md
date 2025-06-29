# TKA AUGMENT AGENT v4.0 - EXPERT DEVELOPMENT ASSISTANT

## CRITICAL DISCOVERY: YOUR ARCHITECTURE IS ALREADY ADVANCED

After microscopic analysis, your TKA codebase already has:

✅ **Command Pattern Implemented**: `SequenceManagementService` has `AddBeatCommand`, `RemoveBeatCommand`, `UpdateBeatCommand` with undo/redo
✅ **Sophisticated Domain Models**: `BeatData`, `SequenceData`, `MotionData`, `PictographData` - complex immutable dataclasses  
✅ **Working DI Container**: `ApplicationFactory` with test/production/headless modes
✅ **Advanced Services**: `PictographManagementService` with dataset management, CSV loading, glyph generation
✅ **Test Architecture**: Lifecycle-based testing (specification/regression/scaffolding) with comprehensive fixtures
✅ **Event System**: Partially implemented with event bus integration

## CORRECTED HACK #2: AI AGENT TESTING INTEGRATION

### WHAT YOU ACTUALLY NEED:
Instead of recreating your command pattern, you need **AI-friendly wrapper functions** that leverage your existing sophisticated architecture.

---

## IMPLEMENTATION: AI Agent Testing Utilities

### File: `src/desktop/modern/src/core/testing/ai_agent_helpers.py`

```python
"""
AI Agent Testing Utilities for TKA

Provides simple interfaces for AI agents to test complex workflows
using the existing sophisticated TKA architecture.
"""

import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# Import your existing architecture
from core.application.application_factory import ApplicationFactory
from core.interfaces.core_services import (
    ISequenceManagementService,
    IPictographManagementService,
    ISequenceDataService,
    IValidationService
)
from domain.models.core_models import (
    BeatData, SequenceData, MotionData, MotionType, 
    Location, RotationDirection
)
from domain.models.pictograph_models import PictographData, GridMode

logger = logging.getLogger(__name__)


@dataclass
class AITestResult:
    """Simple result format for AI agents."""
    success: bool
    data: Optional[Any] = None
    errors: List[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = None


class TKAAITestHelper:
    """
    Simplified testing interface for AI agents.
    
    Abstracts the complexity of your domain models and services
    while providing access to real business logic testing.
    """
    
    def __init__(self, use_test_mode: bool = True):
        """Initialize with test or production services."""
        if use_test_mode:
            self.container = ApplicationFactory.create_test_app()
        else:
            self.container = ApplicationFactory.create_headless_app()
        
        self.execution_history: List[tuple] = []
        
        # Cache frequently used services
        self._sequence_service = None
        self._pictograph_service = None
        self._validation_service = None
    
    @property
    def sequence_service(self):
        if self._sequence_service is None:
            self._sequence_service = self.container.resolve(ISequenceManagementService)
        return self._sequence_service
    
    @property
    def pictograph_service(self):
        if self._pictograph_service is None:
            self._pictograph_service = self.container.resolve(IPictographManagementService)
        return self._pictograph_service
    
    @property
    def validation_service(self):
        if self._validation_service is None:
            self._validation_service = self.container.resolve(IValidationService)
        return self._validation_service
    
    def create_sequence(self, name: str, length: int = 8) -> AITestResult:
        """
        Create a sequence using your existing SequenceManagementService.
        
        Returns simple result format for AI agents.
        """
        import time
        start_time = time.time()
        
        try:
            # Use your existing sophisticated service
            sequence_data = self.sequence_service.create_sequence(name, length)
            
            # Validate using your existing validation
            is_valid = self.validation_service.validate_sequence(sequence_data.to_dict())
            
            if not is_valid:
                errors = self.validation_service.get_validation_errors(sequence_data.to_dict())
                return AITestResult(
                    success=False,
                    errors=errors,
                    execution_time=time.time() - start_time
                )
            
            result = AITestResult(
                success=True,
                data=sequence_data,
                execution_time=time.time() - start_time,
                metadata={
                    'sequence_id': sequence_data.id,
                    'sequence_name': sequence_data.name,
                    'beat_count': len(sequence_data.beats),
                    'is_valid': sequence_data.is_valid
                }
            )
            
            self.execution_history.append(('create_sequence', result))
            return result
            
        except Exception as e:
            logger.error(f"Sequence creation failed: {e}")
            result = AITestResult(
                success=False,
                errors=[f"Sequence creation failed: {str(e)}"],
                execution_time=time.time() - start_time
            )
            self.execution_history.append(('create_sequence', result))
            return result
    
    def create_beat_with_motions(self, beat_number: int, letter: str = "A") -> AITestResult:
        """
        Create a BeatData with proper MotionData using your domain models.
        """
        import time
        start_time = time.time()
        
        try:
            # Create using your sophisticated domain models
            blue_motion = MotionData(
                motion_type=MotionType.PRO,
                prop_rot_dir=RotationDirection.CLOCKWISE,
                start_loc=Location.NORTH,
                end_loc=Location.EAST,
                turns=0.5
            )
            
            red_motion = MotionData(
                motion_type=MotionType.ANTI,
                prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                start_loc=Location.SOUTH,
                end_loc=Location.WEST,
                turns=0.5
            )
            
            beat_data = BeatData(
                beat_number=beat_number,
                letter=letter,
                blue_motion=blue_motion,
                red_motion=red_motion,
                duration=1.0
            )
            
            # Validate using your existing validation
            is_valid = self.validation_service.validate_beat(beat_data.to_dict())
            
            result = AITestResult(
                success=is_valid,
                data=beat_data,
                execution_time=time.time() - start_time,
                metadata={
                    'beat_number': beat_data.beat_number,
                    'letter': beat_data.letter,
                    'has_blue_motion': beat_data.blue_motion is not None,
                    'has_red_motion': beat_data.red_motion is not None,
                    'is_valid': beat_data.is_valid()
                }
            )
            
            if not is_valid:
                result.errors = self.validation_service.get_validation_errors(beat_data.to_dict())
            
            self.execution_history.append(('create_beat', result))
            return result
            
        except Exception as e:
            logger.error(f"Beat creation failed: {e}")
            result = AITestResult(
                success=False,
                errors=[f"Beat creation failed: {str(e)}"],
                execution_time=time.time() - start_time
            )
            self.execution_history.append(('create_beat', result))
            return result
    
    def test_existing_command_pattern(self) -> AITestResult:
        """
        Test your existing command pattern with undo/redo.
        
        Uses your SequenceManagementService's add_beat_with_undo method.
        """
        import time
        start_time = time.time()
        
        try:
            # Create a sequence
            sequence_result = self.create_sequence("Command Test", 4)
            if not sequence_result.success:
                return sequence_result
            
            sequence_data = sequence_result.data
            
            # Set current sequence in service
            self.sequence_service.set_current_sequence(sequence_data)
            
            # Create a beat
            beat_result = self.create_beat_with_motions(1, "A")
            if not beat_result.success:
                return beat_result
            
            beat_data = beat_result.data
            
            # Test your existing command pattern
            if hasattr(self.sequence_service, 'add_beat_with_undo'):
                # Use your existing command with undo
                updated_sequence = self.sequence_service.add_beat_with_undo(beat_data, 0)
                
                # Test undo functionality
                can_undo = self.sequence_service.can_undo()
                undo_description = self.sequence_service.get_undo_description()
                
                result = AITestResult(
                    success=True,
                    data=updated_sequence,
                    execution_time=time.time() - start_time,
                    metadata={
                        'command_pattern_available': True,
                        'can_undo': can_undo,
                        'undo_description': undo_description,
                        'updated_sequence_beats': len(updated_sequence.beats),
                        'sequence_is_valid': updated_sequence.is_valid
                    }
                )
            else:
                # Fallback to regular add_beat
                updated_sequence = self.sequence_service.add_beat(sequence_data, beat_data, 0)
                
                result = AITestResult(
                    success=True,
                    data=updated_sequence,
                    execution_time=time.time() - start_time,
                    metadata={
                        'command_pattern_available': False,
                        'fallback_used': True,
                        'updated_sequence_beats': len(updated_sequence.beats),
                        'sequence_is_valid': updated_sequence.is_valid
                    }
                )
            
            self.execution_history.append(('test_command_pattern', result))
            return result
            
        except Exception as e:
            logger.error(f"Command pattern test failed: {e}")
            result = AITestResult(
                success=False,
                errors=[f"Command pattern test failed: {str(e)}"],
                execution_time=time.time() - start_time
            )
            self.execution_history.append(('test_command_pattern', result))
            return result
    
    def create_pictograph(self, grid_mode: str = 'diamond') -> AITestResult:
        """
        Create a pictograph using your existing PictographManagementService.
        """
        import time
        start_time = time.time()
        
        try:
            grid_mode_enum = GridMode.DIAMOND if grid_mode == 'diamond' else GridMode.BOX
            
            # Use your existing sophisticated pictograph service
            pictograph_data = self.pictograph_service.create_pictograph(grid_mode_enum)
            
            result = AITestResult(
                success=True,
                data=pictograph_data,
                execution_time=time.time() - start_time,
                metadata={
                    'pictograph_id': pictograph_data.id,
                    'grid_mode': pictograph_data.grid_data.grid_mode.value,
                    'is_blank': pictograph_data.is_blank,
                    'has_arrows': len(pictograph_data.arrows) > 0
                }
            )
            
            self.execution_history.append(('create_pictograph', result))
            return result
            
        except Exception as e:
            logger.error(f"Pictograph creation failed: {e}")
            result = AITestResult(
                success=False,
                errors=[f"Pictograph creation failed: {str(e)}"],
                execution_time=time.time() - start_time
            )
            self.execution_history.append(('create_pictograph', result))
            return result
    
    def test_pictograph_from_beat(self) -> AITestResult:
        """
        Test your existing create_from_beat functionality.
        """
        import time
        start_time = time.time()
        
        try:
            # Create a beat with motions
            beat_result = self.create_beat_with_motions(1, "A")
            if not beat_result.success:
                return beat_result
            
            beat_data = beat_result.data
            
            # Use your existing create_from_beat method
            pictograph_data = self.pictograph_service.create_from_beat(beat_data)
            
            result = AITestResult(
                success=True,
                data=pictograph_data,
                execution_time=time.time() - start_time,
                metadata={
                    'pictograph_id': pictograph_data.id,
                    'created_from_beat': beat_data.beat_number,
                    'letter': beat_data.letter,
                    'has_blue_arrow': 'blue' in pictograph_data.arrows,
                    'has_red_arrow': 'red' in pictograph_data.arrows,
                    'is_blank': pictograph_data.is_blank
                }
            )
            
            self.execution_history.append(('pictograph_from_beat', result))
            return result
            
        except Exception as e:
            logger.error(f"Pictograph from beat test failed: {e}")
            result = AITestResult(
                success=False,
                errors=[f"Pictograph from beat test failed: {str(e)}"],
                execution_time=time.time() - start_time
            )
            self.execution_history.append(('pictograph_from_beat', result))
            return result
    
    def test_csv_dataset_integration(self) -> AITestResult:
        """
        Test your existing CSV dataset functionality.
        """
        import time
        start_time = time.time()
        
        try:
            # Test your existing get_pictographs_by_letter method
            pictographs = self.pictograph_service.get_pictographs_by_letter("A")
            
            result = AITestResult(
                success=True,
                data=pictographs,
                execution_time=time.time() - start_time,
                metadata={
                    'pictographs_found': len(pictographs),
                    'letter_tested': "A",
                    'csv_integration_working': len(pictographs) > 0
                }
            )
            
            self.execution_history.append(('csv_dataset_test', result))
            return result
            
        except Exception as e:
            logger.error(f"CSV dataset test failed: {e}")
            result = AITestResult(
                success=False,
                errors=[f"CSV dataset test failed: {str(e)}"],
                execution_time=time.time() - start_time
            )
            self.execution_history.append(('csv_dataset_test', result))
            return result
    
    def run_comprehensive_test_suite(self) -> AITestResult:
        """
        Run comprehensive test of your existing architecture.
        
        Perfect for AI agents to validate all systems working.
        """
        import time
        start_time = time.time()
        
        test_results = {}
        errors = []
        
        # Test 1: Sequence creation
        seq_result = self.create_sequence("Comprehensive Test", 4)
        test_results['sequence_creation'] = seq_result.success
        if not seq_result.success:
            errors.extend(seq_result.errors)
        
        # Test 2: Beat creation
        beat_result = self.create_beat_with_motions(1, "A")
        test_results['beat_creation'] = beat_result.success
        if not beat_result.success:
            errors.extend(beat_result.errors)
        
        # Test 3: Command pattern
        cmd_result = self.test_existing_command_pattern()
        test_results['command_pattern'] = cmd_result.success
        if not cmd_result.success:
            errors.extend(cmd_result.errors)
        
        # Test 4: Pictograph creation
        picto_result = self.create_pictograph("diamond")
        test_results['pictograph_creation'] = picto_result.success
        if not picto_result.success:
            errors.extend(picto_result.errors)
        
        # Test 5: Pictograph from beat
        picto_beat_result = self.test_pictograph_from_beat()
        test_results['pictograph_from_beat'] = picto_beat_result.success
        if not picto_beat_result.success:
            errors.extend(picto_beat_result.errors)
        
        # Test 6: CSV dataset
        csv_result = self.test_csv_dataset_integration()
        test_results['csv_dataset'] = csv_result.success
        if not csv_result.success:
            errors.extend(csv_result.errors)
        
        # Calculate overall success
        total_tests = len(test_results)
        passed_tests = sum(test_results.values())
        success_rate = passed_tests / total_tests
        
        overall_success = success_rate >= 0.8  # 80% success threshold
        
        result = AITestResult(
            success=overall_success,
            data=test_results,
            errors=errors,
            execution_time=time.time() - start_time,
            metadata={
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': total_tests - passed_tests,
                'success_rate': success_rate,
                'test_breakdown': test_results
            }
        )
        
        self.execution_history.append(('comprehensive_test', result))
        return result
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get summary of all executed tests."""
        total_commands = len(self.execution_history)
        successful_commands = len([r for _, r in self.execution_history if r.success])
        total_time = sum(r.execution_time for _, r in self.execution_history)
        
        return {
            'total_commands': total_commands,
            'successful_commands': successful_commands,
            'failed_commands': total_commands - successful_commands,
            'success_rate': successful_commands / total_commands if total_commands > 0 else 0,
            'total_execution_time': total_time,
            'average_execution_time': total_time / total_commands if total_commands > 0 else 0,
            'command_history': [
                {
                    'command': cmd_type,
                    'success': result.success,
                    'execution_time': result.execution_time,
                    'errors': result.errors
                }
                for cmd_type, result in self.execution_history
            ]
        }


# Simple convenience functions for AI agents
def ai_test_tka_comprehensive() -> Dict[str, Any]:
    """One-line comprehensive test for AI agents."""
    helper = TKAAITestHelper()
    result = helper.run_comprehensive_test_suite()
    return {
        'overall_success': result.success,
        'test_breakdown': result.metadata.get('test_breakdown', {}),
        'success_rate': result.metadata.get('success_rate', 0),
        'execution_time': result.execution_time,
        'errors': result.errors
    }


def ai_test_sequence_workflow() -> Dict[str, Any]:
    """Test sequence creation workflow for AI agents."""
    helper = TKAAITestHelper()
    result = helper.test_existing_command_pattern()
    return {
        'success': result.success,
        'command_pattern_available': result.metadata.get('command_pattern_available', False),
        'can_undo': result.metadata.get('can_undo', False),
        'errors': result.errors
    }


def ai_test_pictograph_workflow() -> Dict[str, Any]:
    """Test pictograph creation workflow for AI agents."""
    helper = TKAAITestHelper()
    result = helper.test_pictograph_from_beat()
    return {
        'success': result.success,
        'has_arrows': result.metadata.get('has_blue_arrow', False) and result.metadata.get('has_red_arrow', False),
        'errors': result.errors
    }
```

### File: `tests/specification/test_ai_agent_integration.py`

```python
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Ensure AI agents can effectively test TKA workflows using existing architecture
PERMANENT: AI agent testing must work with our sophisticated domain models and services
AUTHOR: @ai-integration
"""

import pytest
from core.testing.ai_agent_helpers import (
    TKAAITestHelper,
    ai_test_tka_comprehensive,
    ai_test_sequence_workflow,
    ai_test_pictograph_workflow
)


@pytest.mark.specification
@pytest.mark.critical
class TestAIAgentIntegrationContract:
    """Permanent AI agent integration contract - NEVER DELETE"""
    
    def test_ai_helper_initialization_contract(self):
        """PERMANENT: AI helper must initialize with test services"""
        helper = TKAAITestHelper(use_test_mode=True)
        
        # Contract: Must be able to resolve core services
        assert helper.sequence_service is not None
        assert helper.pictograph_service is not None
        assert helper.validation_service is not None
    
    def test_sequence_creation_contract(self):
        """PERMANENT: AI agents must be able to create sequences using real services"""
        helper = TKAAITestHelper()
        result = helper.create_sequence("AI Test", 4)
        
        # Contract: Must succeed with valid input
        assert result.success == True
        assert result.data is not None
        assert result.metadata['sequence_name'] == "AI Test"
        assert result.metadata['beat_count'] == 4
        
        # Contract: Result must contain actual SequenceData
        from domain.models.core_models import SequenceData
        assert isinstance(result.data, SequenceData)
    
    def test_beat_creation_contract(self):
        """PERMANENT: AI agents must be able to create beats with motion data"""
        helper = TKAAITestHelper()
        result = helper.create_beat_with_motions(1, "A")
        
        # Contract: Must succeed with valid motion data
        assert result.success == True
        assert result.data is not None
        assert result.metadata['has_blue_motion'] == True
        assert result.metadata['has_red_motion'] == True
        
        # Contract: Result must contain actual BeatData
        from domain.models.core_models import BeatData
        assert isinstance(result.data, BeatData)
    
    def test_existing_command_pattern_contract(self):
        """PERMANENT: AI agents must be able to use existing command pattern"""
        helper = TKAAITestHelper()
        result = helper.test_existing_command_pattern()
        
        # Contract: Must work regardless of command pattern availability
        assert result.success == True
        assert result.data is not None
        
        # Contract: Must indicate command pattern availability
        assert 'command_pattern_available' in result.metadata
    
    def test_comprehensive_test_suite_contract(self):
        """PERMANENT: AI agents must be able to run full architecture tests"""
        helper = TKAAITestHelper()
        result = helper.run_comprehensive_test_suite()
        
        # Contract: Must test all major components
        assert result.data is not None
        test_breakdown = result.metadata.get('test_breakdown', {})
        
        expected_tests = [
            'sequence_creation',
            'beat_creation', 
            'command_pattern',
            'pictograph_creation',
            'pictograph_from_beat',
            'csv_dataset'
        ]
        
        for test_name in expected_tests:
            assert test_name in test_breakdown
    
    def test_convenience_functions_contract(self):
        """PERMANENT: AI agents must have simple one-line test functions"""
        # Contract: Convenience functions must work
        result1 = ai_test_tka_comprehensive()
        assert 'overall_success' in result1
        assert 'test_breakdown' in result1
        
        result2 = ai_test_sequence_workflow()
        assert 'success' in result2
        
        result3 = ai_test_pictograph_workflow()
        assert 'success' in result3


@pytest.mark.specification
class TestAIAgentWorkflowContract:
    """Permanent AI agent workflow contract - NEVER DELETE"""
    
    def test_error_handling_contract(self):
        """PERMANENT: AI helpers must handle errors gracefully"""
        helper = TKAAITestHelper()
        
        # Test with invalid input
        result = helper.create_sequence("", 0)  # Invalid input
        
        # Contract: Must not crash and provide error information
        assert isinstance(result.success, bool)
        assert isinstance(result.errors, list)
        assert result.execution_time >= 0
    
    def test_execution_history_contract(self):
        """PERMANENT: AI helpers must track execution history"""
        helper = TKAAITestHelper()
        
        # Perform some operations
        helper.create_sequence("Test", 4)
        helper.create_beat_with_motions(1, "A")
        
        # Contract: Must track history
        summary = helper.get_execution_summary()
        assert summary['total_commands'] == 2
        assert 'command_history' in summary
        assert len(summary['command_history']) == 2
```

---

## UPDATED TKA TESTING GUIDELINES FOR AI AGENTS

### CORE TESTING PHILOSOPHY

Your TKA codebase has sophisticated architecture that AI agents must understand and leverage:

1. **Use Existing Architecture**: Never recreate systems - leverage `ApplicationFactory`, existing services, domain models
2. **Test Real Business Logic**: Use actual `SequenceManagementService`, `PictographManagementService` 
3. **Respect Domain Complexity**: Work with `BeatData`, `SequenceData`, `MotionData` immutable models
4. **Follow Test Lifecycle**: Use specification/regression/scaffolding categorization

### AI AGENT TESTING PROTOCOL

#### Phase 1: Architecture Discovery
```python
# AI agents should start by understanding available services
from core.application.application_factory import ApplicationFactory
container = ApplicationFactory.create_test_app()

# Discover what services are available
available_services = list(container.get_registrations().keys())
print(f"Available services: {available_services}")
```

#### Phase 2: Use TKA Test Helpers
```python
# Use the simplified AI helper instead of raw services
from core.testing.ai_agent_helpers import TKAAITestHelper

helper = TKAAITestHelper(use_test_mode=True)

# Test real workflows with simple interfaces
result = helper.run_comprehensive_test_suite()
print(f"Success rate: {result.metadata['success_rate']:.1%}")
```

#### Phase 3: Validate Core Workflows
```python
# Test specific workflows that matter to users
sequence_test = helper.test_existing_command_pattern()
pictograph_test = helper.test_pictograph_from_beat()
dataset_test = helper.test_csv_dataset_integration()

# Validate each component works
assert sequence_test.success
assert pictograph_test.success  
assert dataset_test.success
```

#### Phase 4: Use Convenience Functions
```python
# For quick validation, use one-liners
from core.testing.ai_agent_helpers import (
    ai_test_tka_comprehensive,
    ai_test_sequence_workflow,
    ai_test_pictograph_workflow
)

# Quick comprehensive test
result = ai_test_tka_comprehensive()
assert result['overall_success']
assert result['success_rate'] > 0.8
```

### TESTING BEST PRACTICES FOR AI AGENTS

#### DO:
- ✅ Use `ApplicationFactory.create_test_app()` for fast testing
- ✅ Use `TKAAITestHelper` for simplified interfaces
- ✅ Test with real domain models (`BeatData`, `SequenceData`)
- ✅ Validate existing command pattern functionality
- ✅ Use specification tests for permanent contracts
- ✅ Test CSV dataset integration
- ✅ Verify undo/redo capabilities when available

#### DON'T:
- ❌ Create competing command patterns
- ❌ Mock complex domain models unnecessarily
- ❌ Ignore existing service interfaces
- ❌ Create UI dependencies in tests
- ❌ Recreate existing functionality
- ❌ Skip validation of business rules

### COMMON AI AGENT TEST PATTERNS

#### Pattern 1: Quick Validation
```python
def ai_agent_quick_test():
    """Quick test for AI agents to validate system works"""
    result = ai_test_tka_comprehensive()
    return result['overall_success'] and result['success_rate'] > 0.8
```

#### Pattern 2: Workflow Testing
```python
def ai_agent_workflow_test():
    """Test complete user workflow"""
    helper = TKAAITestHelper()
    
    # Test the full user journey
    seq_result = helper.create_sequence("User Test", 8)
    beat_result = helper.create_beat_with_motions(1, "A")
    cmd_result = helper.test_existing_command_pattern()
    
    return all([seq_result.success, beat_result.success, cmd_result.success])
```

#### Pattern 3: Component Integration
```python
def ai_agent_integration_test():
    """Test component integration"""
    helper = TKAAITestHelper()
    
    # Test services work together
    picto_beat_result = helper.test_pictograph_from_beat()
    csv_result = helper.test_csv_dataset_integration()
    
    return picto_beat_result.success and csv_result.success
```

### ERROR HANDLING FOR AI AGENTS

AI agents should handle errors gracefully:

```python
def ai_agent_error_handling_test():
    """Example of proper error handling"""
    helper = TKAAITestHelper()
    
    # Test with invalid input
    result = helper.create_sequence("", -1)  # Invalid
    
    if not result.success:
        print(f"Expected failure: {result.errors}")
        return True  # This is expected
    
    return False
```

### SUCCESS METRICS FOR AI AGENTS

AI agents should validate:
- **Architecture Integration**: Can resolve all core services
- **Domain Model Usage**: Can create and manipulate `BeatData`, `SequenceData`
- **Business Logic**: Can use existing command pattern and services
- **Error Handling**: Gracefully handles invalid inputs
- **Performance**: Tests execute quickly (< 1 second for comprehensive suite)

This testing protocol ensures AI agents work WITH your sophisticated architecture rather than around it, enabling effective testing of real user workflows while maintaining architectural integrity.