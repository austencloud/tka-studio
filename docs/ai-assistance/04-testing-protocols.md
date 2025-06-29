# 04 - TKA Testing Protocols

## 🧪 SOPHISTICATED TESTING INFRASTRUCTURE

TKA has a mature testing architecture with lifecycle-based organization, comprehensive fixtures, and AI-friendly utilities. AI agents must understand and use this existing infrastructure.

## 📋 TEST LIFECYCLE CATEGORIES

### Specification Tests (PERMANENT)
**Purpose**: Enforce behavioral contracts that must never change
**Location**: `tests/specification/`
**Lifecycle**: NEVER DELETE unless entire feature removed

```python
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Enforce [specific behavioral contract]
PERMANENT: [Why this behavior must always be preserved]
AUTHOR: @username
"""

@pytest.mark.specification
@pytest.mark.critical
class TestDomainModelContract:
    """Permanent domain contract - NEVER DELETE"""
    
    def test_sequence_immutability_contract(self):
        """PERMANENT: Sequence operations must return new instances"""
        sequence = SequenceData(name="Test", beats=[])
        beat = BeatData(beat_number=1, letter="A")
        
        new_sequence = sequence.add_beat(beat)
        
        # Contract: Original must be unchanged
        assert sequence is not new_sequence
        assert len(sequence.beats) == 0
        assert len(new_sequence.beats) == 1
```

### Regression Tests (KEEP UNTIL FEATURE REMOVED)
**Purpose**: Prevent specific bugs from reoccurring
**Location**: `tests/regression/`
**Lifecycle**: Keep until related feature is completely removed

```python
"""
TEST LIFECYCLE: REGRESSION
PURPOSE: Prevent [specific bug] from reoccurring
BUG_REPORT: #issue_number or description
FIXED_DATE: YYYY-MM-DD
AUTHOR: @username
"""

@pytest.mark.regression
class TestBugFix123:
    """Regression test for bug #123 - KEEP until feature removed"""
    
    def test_sequence_creation_crash_fix(self):
        """REGRESSION: Ensure empty name doesn't crash sequence creation"""
        # This test prevents regression of bug #123
        container = ApplicationFactory.create_test_app()
        service = container.resolve(ISequenceManagementService)
        
        # Should not crash, should return validation error
        with pytest.raises(ValidationError):
            service.create_sequence("", 8)
```

### Scaffolding Tests (TEMPORARY)
**Purpose**: Temporary development aids - DELETE after purpose achieved
**Location**: `tests/scaffolding/`
**Lifecycle**: DELETE after DELETE_AFTER date

```python
"""
TEST LIFECYCLE: SCAFFOLDING
PURPOSE: Debug sequence creation performance issue
DELETE_AFTER: 2024-12-31
CREATED: 2024-06-01
AUTHOR: @username
RELATED_ISSUE: #456
"""

@pytest.mark.scaffolding
class TestSequencePerformanceDebug:
    """SCAFFOLDING: Delete after performance issue resolved"""
    
    def test_sequence_creation_timing(self):
        """SCAFFOLDING: Measure sequence creation performance"""
        import time
        
        start = time.time()
        container = ApplicationFactory.create_test_app()
        service = container.resolve(ISequenceManagementService)
        service.create_sequence("Performance Test", 16)
        duration = time.time() - start
        
        print(f"Sequence creation took: {duration:.4f}s")
        # This is temporary debugging - will be deleted
```

## 🎯 AI AGENT TESTING UTILITIES

### `TKAAITestHelper` - Primary Testing Interface
**Location**: `core/testing/ai_agent_helpers.py`

```python
from core.testing.ai_agent_helpers import TKAAITestHelper

# Initialize with test services
helper = TKAAITestHelper(use_test_mode=True)

# Test sequence operations
result = helper.create_sequence("AI Test", 8)
assert result.success
assert result.metadata['sequence_name'] == "AI Test"

# Test beat operations with motion data
beat_result = helper.create_beat_with_motions(1, "A")
assert beat_result.success
assert beat_result.metadata['has_blue_motion']

# Test existing command pattern
cmd_result = helper.test_existing_command_pattern()
assert cmd_result.metadata['command_pattern_available']

# Test pictograph operations
picto_result = helper.create_pictograph("diamond")
assert picto_result.success

# Test CSV dataset integration
csv_result = helper.test_csv_dataset_integration()
assert csv_result.success

# Run comprehensive test suite
comprehensive = helper.run_comprehensive_test_suite()
assert comprehensive.success
assert comprehensive.metadata['success_rate'] > 0.8
```

### Convenience Functions for Quick Testing
```python
from core.testing.ai_agent_helpers import (
    ai_test_tka_comprehensive,
    ai_test_sequence_workflow,
    ai_test_pictograph_workflow
)

# One-line comprehensive test
result = ai_test_tka_comprehensive()
assert result['overall_success']
assert result['success_rate'] > 0.8

# Quick workflow tests
seq_result = ai_test_sequence_workflow()
assert seq_result['success']
assert seq_result['command_pattern_available']

picto_result = ai_test_pictograph_workflow()
assert picto_result['success']
assert picto_result['has_arrows']
```

## 🧰 COMPREHENSIVE TEST FIXTURES

### DI Container Fixtures
**Location**: `tests/fixtures/di_fixtures.py`

```python
# Clean DI container
def test_with_clean_container(clean_di_container):
    container = clean_di_container
    # Test with fresh container
    
# Configured DI container with basic services
def test_with_configured_container(configured_di_container):
    container = configured_di_container
    service = container.resolve(ILayoutService)
    
# Workbench DI container with full service graph
def test_with_workbench_container(workbench_di_container):
    container = workbench_di_container
    # All workbench services available
```

### Domain Model Fixtures
**Location**: `tests/fixtures/domain_fixtures.py`

```python
# Real domain objects for testing
def test_with_beat_data(sample_beat_data):
    beat = sample_beat_data  # Real BeatData with MotionData
    assert beat.is_valid()
    
def test_with_sequence_data(sample_sequence_data):
    sequence = sample_sequence_data  # Real SequenceData with beats
    assert sequence.length > 0
    
def test_with_pictograph_data(sample_pictograph_data):
    pictograph = sample_pictograph_data  # Real PictographData with arrows
    assert not pictograph.is_blank
    
def test_with_motion_data(sample_motion_data):
    motion = sample_motion_data  # Real MotionData with enums
    assert motion.motion_type == MotionType.PRO
```

### Letter Type Fixtures
```python
def test_type1_letters(type1_letters):
    letters = type1_letters  # ["A", "B", "D", "G"]
    # Test Type 1 letter behavior
    
def test_type2_letters(type2_letters):
    letters = type2_letters  # ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"]
    # Test Type 2 letter behavior
```

## 🚀 AI AGENT TESTING PATTERNS

### Pattern 1: Architecture Validation
```python
def test_architecture_integrity():
    """Validate core architecture works"""
    # Use existing utilities
    result = ai_test_tka_comprehensive()
    
    # Check all major components
    assert result['test_breakdown']['sequence_creation']
    assert result['test_breakdown']['beat_creation']
    assert result['test_breakdown']['command_pattern']
    assert result['test_breakdown']['pictograph_creation']
    assert result['test_breakdown']['csv_dataset']
    
    # Ensure high success rate
    assert result['success_rate'] > 0.8
```

### Pattern 2: Workflow Testing
```python
def test_complete_user_workflow():
    """Test end-to-end user workflow"""
    helper = TKAAITestHelper()
    
    # Step 1: Create sequence
    seq_result = helper.create_sequence("Workflow Test", 4)
    assert seq_result.success
    
    # Step 2: Create beats with motions
    beat_result = helper.create_beat_with_motions(1, "A")
    assert beat_result.success
    
    # Step 3: Test command pattern (if available)
    cmd_result = helper.test_existing_command_pattern()
    assert cmd_result.success
    
    # Step 4: Create pictograph from beat
    picto_result = helper.test_pictograph_from_beat()
    assert picto_result.success
```

### Pattern 3: Service Integration Testing
```python
def test_service_integration():
    """Test services work together correctly"""
    container = ApplicationFactory.create_test_app()
    
    # Get multiple services
    sequence_service = container.resolve(ISequenceManagementService)
    pictograph_service = container.resolve(IPictographManagementService)
    validation_service = container.resolve(IValidationService)
    
    # Test integration
    sequence = sequence_service.create_sequence("Integration Test", 4)
    assert validation_service.validate_sequence(sequence.to_dict())
    
    # Test pictograph from sequence data
    beat = BeatData(beat_number=1, letter="A")
    pictograph = pictograph_service.create_from_beat(beat)
    assert not pictograph.is_blank
```

### Pattern 4: Error Handling Testing
```python
def test_error_handling():
    """Test graceful error handling"""
    helper = TKAAITestHelper()
    
    # Test invalid inputs
    invalid_seq = helper.create_sequence("", 0)
    assert not invalid_seq.success
    assert len(invalid_seq.errors) > 0
    
    # Test system continues working after errors
    valid_seq = helper.create_sequence("Valid", 4)
    assert valid_seq.success
```

## 📊 PERFORMANCE TESTING

### Execution Speed Validation
```python
def test_performance_standards():
    """Ensure testing meets performance standards"""
    import time
    
    start = time.time()
    result = ai_test_tka_comprehensive()
    duration = time.time() - start
    
    # Test services should be fast
    assert duration < 1.0  # Under 1 second for comprehensive test
    assert result['overall_success']
```

### Memory Usage Testing
```python
def test_memory_efficiency():
    """Test memory usage is reasonable"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss
    
    # Run comprehensive tests
    helper = TKAAITestHelper()
    helper.run_comprehensive_test_suite()
    
    memory_after = process.memory_info().rss
    memory_increase = memory_after - memory_before
    
    # Memory increase should be reasonable (under 50MB)
    assert memory_increase < 50 * 1024 * 1024
```

## 🔍 TEST DEBUGGING AND ANALYSIS

### Execution History Analysis
```python
def test_execution_analysis():
    """Analyze test execution patterns"""
    helper = TKAAITestHelper()
    
    # Run multiple operations
    helper.create_sequence("Test 1", 4)
    helper.create_beat_with_motions(1, "A")
    helper.create_pictograph("diamond")
    
    # Analyze execution
    summary = helper.get_execution_summary()
    
    assert summary['total_commands'] == 3
    assert summary['successful_commands'] >= 2
    assert summary['average_execution_time'] < 0.1
    
    # Check command history
    history = summary['command_history']
    assert len(history) == 3
    assert all('execution_time' in cmd for cmd in history)
```

### Test Coverage Validation
```python
def test_coverage_validation():
    """Ensure tests cover core functionality"""
    result = ai_test_tka_comprehensive()
    
    # Must test all major components
    required_tests = [
        'sequence_creation',
        'beat_creation',
        'command_pattern',
        'pictograph_creation',
        'pictograph_from_beat',
        'csv_dataset'
    ]
    
    test_breakdown = result['test_breakdown']
    for test_name in required_tests:
        assert test_name in test_breakdown, f"Missing test: {test_name}"
```

## 🚨 TESTING BEST PRACTICES FOR AI AGENTS

### DO:
```python
# ✅ Use existing test infrastructure
helper = TKAAITestHelper(use_test_mode=True)

# ✅ Test with real domain models
beat = BeatData(beat_number=1, letter="A")
assert isinstance(beat, BeatData)

# ✅ Use appropriate test lifecycle
@pytest.mark.specification  # For permanent tests
@pytest.mark.regression     # For bug prevention
@pytest.mark.scaffolding    # For temporary debugging

# ✅ Leverage comprehensive fixtures
def test_with_real_data(sample_sequence_data):
    sequence = sample_sequence_data

# ✅ Test real service integration
container = ApplicationFactory.create_test_app()
service = container.resolve(ISequenceManagementService)
```

### DON'T:
```python
# ❌ Create unnecessary mocks for complex objects
mock_sequence = Mock()  # Use real SequenceData instead

# ❌ Skip using AI test utilities
# Manual service setup when TKAAITestHelper exists

# ❌ Test implementation details
assert service._internal_state == value  # Test contracts, not internals

# ❌ Create permanent tests without proper lifecycle
# Unlabeled tests that might be deleted accidentally

# ❌ Ignore existing fixtures
beat = BeatData()  # Use sample_beat_data fixture instead
```

## 🎯 TEST EXECUTION COMMANDS

### Run Specific Test Categories
```bash
# Run only specification tests (permanent contracts)
pytest tests/specification/ -v

# Run regression tests (bug prevention)
pytest tests/regression/ -v

# Run scaffolding tests (temporary debugging)
pytest tests/scaffolding/ -v

# Run AI agent integration tests
pytest tests/specification/test_ai_agent_integration.py -v
```

### Performance and Health Checks
```bash
# Run test health check
python tests/test_runner.py --health

# Check for expired scaffolding tests
python tests/scripts/test_lifecycle_manager.py --expired

# Generate test report
python tests/scripts/test_lifecycle_manager.py --report
```

## 🎯 KEY TAKEAWAYS FOR AI AGENTS

1. **Use Existing Infrastructure**: TKA has sophisticated testing tools - don't recreate them
2. **Follow Test Lifecycle**: Understand specification/regression/scaffolding categories
3. **Use TKAAITestHelper**: Primary interface for AI agent testing
4. **Test Real Components**: Use actual services and domain models, not mocks
5. **Leverage Fixtures**: Comprehensive fixtures available for all major components
6. **Performance Matters**: Tests should execute quickly (< 1 second for comprehensive)
7. **Validate Architecture**: Use comprehensive test suite to ensure system integrity

**The testing infrastructure is designed to enable effective validation of sophisticated business logic while maintaining fast execution and clear organization.**
