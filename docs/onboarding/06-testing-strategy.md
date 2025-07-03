# TKA Testing Strategy - Sophisticated Testing Framework

## 🎯 Overview

TKA uses a **lifecycle-based testing approach** that categorizes tests by purpose and lifespan. This sophisticated framework ensures test maintainability while supporting enterprise-grade development with comprehensive coverage of 80+ services.

## 📚 Test Lifecycle Philosophy

### **Three Test Lifecycles**
```
🔒 SPECIFICATION Tests (PERMANENT)
   └── Behavioral contracts that must never change
   
🛡️ REGRESSION Tests (LONG-TERM)  
   └── Bug prevention tests (delete only when feature removed)
   
🏗️ SCAFFOLDING Tests (TEMPORARY)
   └── Development aids with expiration dates
```

## 🏗️ Test Organization Structure

```
tests/
├── 📋 specification/        # Permanent behavioral contracts
│   ├── application/         # Service contracts & workflows
│   ├── core/               # DI container & framework contracts
│   ├── domain/             # Domain model contracts 
│   ├── presentation/       # UI behavior contracts
│   └── workflows/          # User workflow contracts
├── 🛡️ regression/          # Bug prevention tests
│   └── bugs/              # Specific bug regression tests
├── 🏗️ scaffolding/         # Temporary development tests  
│   └── debug/             # Debug-specific scaffolding
├── 🔧 unit/               # Isolated component tests
├── 🔗 integration/        # Multi-component tests
├── 📄 templates/          # Test templates for each lifecycle
├── 📦 fixtures/           # Shared test fixtures
└── 🛠️ scripts/           # Test utilities and runners
```

## 🎭 Test Lifecycle Decision Tree

### **When Creating a New Test, Ask:**

```
1. Is this testing a PERMANENT business rule or contract?
   ├── YES → Use specification/ + specification_test_template.py
   └── NO → Continue to step 2

2. Is this preventing a SPECIFIC BUG from reoccurring?
   ├── YES → Use regression/bugs/ + regression_test_template.py  
   └── NO → Continue to step 3

3. Is this TEMPORARY debugging/exploration?
   ├── YES → Use scaffolding/debug/ + scaffolding_test_template.py
   └── NO → Continue to step 4

4. Is this testing MULTIPLE COMPONENTS together?
   ├── YES → Use integration/ + appropriate template
   └── NO → Use unit/ + appropriate template
```

## 🔒 Specification Tests (PERMANENT)

### **Purpose: Enforce Behavioral Contracts**
These tests ensure that core behaviors **never accidentally change**:

```python
"""
TEST LIFECYCLE: SPECIFICATION
PURPOSE: Enforce pictograph immutability contract
PERMANENT: Pictograph operations must return new instances for data integrity
AUTHOR: @austencloud
"""

@pytest.mark.specification
@pytest.mark.critical
class TestPictographImmutabilityContract:
    """Permanent domain contract - NEVER DELETE"""

    def test_pictograph_update_returns_new_instance(self):
        """PERMANENT: Pictograph updates must return new instances"""
        original = PictographData(id="test", arrows={}, grid_data=GridData())
        updated = original.update_arrow("blue", position_x=100)
        
        # Contract: Operations must return new instances
        assert original is not updated
        assert original.arrows != updated.arrows
        assert id(original) != id(updated)

    def test_pictograph_original_unchanged_after_update(self):
        """PERMANENT: Original pictographs must remain unchanged"""
        original = PictographData(id="test", arrows={"blue": arrow_data}, grid_data=GridData())
        original_arrow = original.arrows["blue"]
        
        updated = original.update_arrow("blue", position_x=100)
        
        # Contract: Original data must be unchanged
        assert original.arrows["blue"] is original_arrow
        assert original.arrows["blue"].position_x != 100
```

### **Specification Test Categories**
```python
# Domain model contracts
TestSequenceDataContract           # Sequence immutability & consistency
TestMotionDataContract            # Motion validation & constraints
TestPictographDataContract        # Pictograph behavior & updates

# Service interface contracts  
TestArrowPositioningContract      # Positioning mathematical correctness
TestDataServiceContract          # Data access behavior guarantees
TestDIContainerContract          # Dependency injection behavior

# UI behavior contracts
TestGraphEditorContract          # Graph editor interaction patterns
TestOptionPickerContract        # Option picker selection behavior
TestLayoutContract              # Layout and responsive behavior

# Legacy parity contracts
TestLegacyParityContract         # Modern behavior must match legacy exactly
```

### **Writing Specification Tests**
```python
@pytest.mark.specification
@pytest.mark.critical
class TestArrowPositioningContract:
    """Permanent positioning contract - NEVER DELETE"""

    def test_positioning_deterministic_contract(self):
        """PERMANENT: Same input must always produce same output"""
        arrow_data = ArrowData(color="blue", motion_data=motion)
        pictograph_data = PictographData(...)
        
        orchestrator = container.resolve(IArrowPositioningOrchestrator)
        
        # Calculate position multiple times
        position1 = orchestrator.calculate_arrow_position(arrow_data, pictograph_data)
        position2 = orchestrator.calculate_arrow_position(arrow_data, pictograph_data) 
        position3 = orchestrator.calculate_arrow_position(arrow_data, pictograph_data)
        
        # Contract: Must be deterministic
        assert position1 == position2 == position3

    def test_positioning_never_returns_none_contract(self):
        """PERMANENT: Positioning must never return None/invalid values"""
        # Test with various valid inputs
        # Contract: Must always return valid position data
```

## 🛡️ Regression Tests (BUG PREVENTION)

### **Purpose: Prevent Known Bugs from Returning**
```python
"""
TEST LIFECYCLE: REGRESSION
PURPOSE: Prevent arrow positioning crash when motion_data is None
BUG_REPORT: Issue #47 - NoneType error in arrow positioning pipeline
FIXED_DATE: 2025-01-15  
AUTHOR: @austencloud
"""

@pytest.mark.regression
@pytest.mark.bug_prevention
class TestArrowPositioningNoneMotionBug:
    """Prevent regression of positioning crash bug"""

    def test_positioning_handles_none_motion_data(self):
        """REGRESSION: Must handle None motion_data without crashing"""
        # This test prevents bug #47 from returning
        arrow_data = ArrowData(color="blue", motion_data=None)
        pictograph_data = PictographData(...)
        
        orchestrator = container.resolve(IArrowPositioningOrchestrator)
        
        # Should not crash, should return default position
        position = orchestrator.calculate_arrow_position(arrow_data, pictograph_data)
        assert position is not None
        assert len(position) == 3  # x, y, rotation
```

### **Regression Test Categories**
```python
# Crash prevention
TestPositioningCrashPrevention    # Prevent positioning calculation crashes
TestDataLoadingCrashPrevention   # Prevent data loading failures
TestUIInteractionCrashPrevention # Prevent UI interaction crashes

# Performance regression
TestPositioningPerformance        # Ensure positioning stays fast
TestDataLoadingPerformance       # Ensure data loading stays fast
TestMemoryUsageRegression        # Prevent memory leaks

# Data integrity regression  
TestDataCorruptionPrevention     # Prevent data corruption bugs
TestCalculationAccuracy          # Prevent mathematical precision loss
```

## 🏗️ Scaffolding Tests (TEMPORARY)

### **Purpose: Temporary Development Aids**
```python
"""
TEST LIFECYCLE: SCAFFOLDING
PURPOSE: Debug graph editor layout crash during Sprint 2
DELETE_AFTER: 2025-02-01
CREATED: 2025-01-15
AUTHOR: @austencloud
RELATED_ISSUE: #47
"""

@pytest.mark.scaffolding
@pytest.mark.delete_after("2025-02-01")
@pytest.mark.debug
class TestGraphEditorLayoutDebug:
    """DELETE: Debugging graph editor layout issues"""

    def test_widget_sizing_crash_reproduction(self):
        """DELETE: Reproduce widget sizing crash for debugging"""
        # Temporary test to reproduce and debug specific issue
        graph_editor = GraphEditor()
        # Specific steps to reproduce the crash
        # This test should be DELETED after issue is resolved
```

### **Scaffolding Categories**
```python
# Debug scaffolding
TestOptionPickerCrashDebug       # DELETE: Debug option picker crash
TestPositioningBugDebug          # DELETE: Debug positioning calculation bug

# Exploration scaffolding  
TestLegacyBehaviorExploration    # DELETE: Understand legacy behavior
TestNewAlgorithmExploration      # DELETE: Explore new positioning algorithm

# Spike scaffolding
TestGraphEditorAnimationSpike    # DELETE: Proof of concept for animations
TestPerformanceOptimizationSpike # DELETE: Test performance improvements
```

### **Scaffolding Rules**
```python
# ✅ REQUIRED: All scaffolding tests must have DELETE_AFTER date
"""
DELETE_AFTER: 2025-02-01  # REQUIRED
"""

# ✅ REQUIRED: Clear purpose statement
"""
PURPOSE: Debug specific crash during arrow positioning with zero turns
"""

# ⚠️ WARNING: Tests older than 30 days without clear purpose → DELETE IMMEDIATELY

# 🗑️ DELETE: Tests that always pass or always fail

# 🗑️ DELETE: Tests that duplicate existing specification coverage
```

## 🔧 Unit Testing Strategy

### **Service Isolation with Dependency Injection**
```python
@pytest.fixture
def arrow_positioning_service():
    """Isolated arrow positioning service with mock dependencies"""
    container = DIContainer()
    
    # Register mock dependencies
    container.register_singleton(IArrowLocationCalculator, MockLocationCalculator)
    container.register_singleton(IArrowRotationCalculator, MockRotationCalculator)
    container.register_singleton(IArrowAdjustmentCalculator, MockAdjustmentCalculator)
    
    # Register real service under test
    container.register_singleton(IArrowPositioningOrchestrator, ArrowPositioningOrchestrator)
    
    return container.resolve(IArrowPositioningOrchestrator)

def test_arrow_positioning_orchestration(arrow_positioning_service):
    """Test service orchestration logic in isolation"""
    arrow_data = ArrowData(color="blue", motion_data=test_motion)
    pictograph_data = PictographData(...)
    
    position = arrow_positioning_service.calculate_arrow_position(arrow_data, pictograph_data)
    
    # Test orchestration logic, not implementation details
    assert position is not None
    assert len(position) == 3
```

### **Mathematical Function Testing**
```python
class TestDirectionalTupleCalculator:
    """Unit tests for pure mathematical functions"""

    def test_pro_motion_clockwise_rotation_diamond_grid(self):
        """Test specific rotation matrix calculation"""
        calculator = DirectionalTupleCalculator()
        motion = MotionData(motion_type=MotionType.PRO, prop_rot_dir=RotationDirection.CLOCKWISE)
        
        tuples = calculator.generate_directional_tuples(motion, 10, 15)
        
        # Test mathematical precision
        expected = [(10, 15), (-15, 10), (-10, -15), (15, -10)]
        assert tuples == expected

    def test_rotation_matrix_consistency(self):
        """Test that rotation matrices are mathematically consistent"""
        # Test mathematical properties of rotation matrices
        # Ensure they form proper mathematical groups
        # Verify inverse relationships
```

## 🔗 Integration Testing Strategy

### **Service Composition Testing**
```python
@pytest.fixture
def positioning_integration_container():
    """Integration test container with real positioning services"""
    container = ApplicationFactory.create_test_app()
    
    # Use real positioning services but mock data persistence
    container.register_singleton(IDataService, MockDataService)
    
    return container

def test_full_positioning_pipeline(positioning_integration_container):
    """Test complete positioning workflow integration"""
    # Get real services
    pictograph_service = positioning_integration_container.resolve(IPictographManagementService)
    positioning_service = positioning_integration_container.resolve(IArrowPositioningOrchestrator)
    
    # Test full workflow
    beat_data = BeatData(beat_number=1, letter="A", blue_motion=test_motion)
    pictograph = pictograph_service.create_pictograph(beat_data)
    
    arrow_data = pictograph.arrows["blue"]
    position = positioning_service.calculate_arrow_position(arrow_data, pictograph)
    
    # Integration assertions
    assert position is not None
    assert pictograph.arrows["blue"].position_x == position[0]
    assert pictograph.arrows["blue"].position_y == position[1]
```

### **Application Mode Testing**
```python
def test_headless_mode_positioning():
    """Test positioning works in headless application mode"""
    container = ApplicationFactory.create_headless_app()
    
    # Should work without UI components
    positioning_service = container.resolve(IArrowPositioningOrchestrator)
    position = positioning_service.calculate_arrow_position(arrow_data, pictograph_data)
    
    assert position is not None

def test_production_vs_test_mode_consistency():
    """Test that business logic is consistent across application modes"""
    prod_container = ApplicationFactory.create_production_app()
    test_container = ApplicationFactory.create_test_app()
    
    prod_service = prod_container.resolve(IArrowPositioningOrchestrator)
    test_service = test_container.resolve(IArrowPositioningOrchestrator)
    
    # Same input should produce same results regardless of mode
    prod_position = prod_service.calculate_arrow_position(arrow_data, pictograph_data)
    test_position = test_service.calculate_arrow_position(arrow_data, pictograph_data)
    
    assert prod_position == test_position
```

## 🎯 UI Testing Strategy

### **Component Testing with Service Integration**
```python
@pytest.fixture
def graph_editor_with_services():
    """Graph editor component with real services"""
    app = QApplication.instance() or QApplication([])
    container = ApplicationFactory.create_test_app()
    
    return GraphEditor(container=container)

def test_graph_editor_arrow_selection(graph_editor_with_services):
    """Test UI component with service integration"""
    editor = graph_editor_with_services
    
    # Test UI interaction
    editor.select_arrow("blue")
    assert editor.selected_arrow == "blue"
    
    # Test service integration
    assert editor.positioning_service.is_arrow_selected("blue")

def test_graph_editor_positioning_update(graph_editor_with_services):
    """Test UI updates positioning through services"""
    editor = graph_editor_with_services
    
    # Simulate user interaction
    editor.update_arrow_position("blue", 100, 150)
    
    # Verify service was called correctly
    # Verify UI reflects the change
    assert editor.get_arrow_position("blue") == (100, 150)
```

## 📊 Test Data Management

### **Fixture Organization**
```python
# tests/fixtures/domain_fixtures.py
@pytest.fixture
def sample_motion_data():
    """Standard motion data for testing"""
    return MotionData(
        motion_type=MotionType.PRO,
        start_loc=Location.NORTH,
        end_loc=Location.EAST,
        turns=1.0,
        prop_rot_dir=RotationDirection.CLOCKWISE
    )

@pytest.fixture  
def sample_pictograph_data():
    """Standard pictograph data for testing"""
    return PictographData(
        id="test_pictograph",
        arrows={"blue": sample_arrow_data, "red": sample_arrow_data},
        grid_data=GridData(grid_mode=GridMode.DIAMOND)
    )

# tests/fixtures/di_fixtures.py
@pytest.fixture
def test_container():
    """Clean DI container for testing"""
    container = ApplicationFactory.create_test_app()
    yield container
    container.cleanup_all()
```

### **Test Data Validation**
```python
def test_fixture_data_validity():
    """Ensure test fixtures are valid"""
    motion_data = sample_motion_data()
    assert motion_data.motion_type in MotionType
    assert motion_data.start_loc in Location
    
    # Validate test data doesn't accidentally test invalid scenarios
    calculator = ArrowLocationCalculatorService()
    assert calculator.validate_motion_data(motion_data)
```

## 🚀 Test Execution Strategy

### **Test Categories by Speed**
```python
# Fast tests (< 100ms each) - Run frequently
@pytest.mark.fast
class TestDomainModels:
    """Fast unit tests for domain models"""

# Medium tests (< 1s each) - Run before commits  
@pytest.mark.medium
class TestServiceIntegration:
    """Service integration tests"""

# Slow tests (> 1s each) - Run in CI
@pytest.mark.slow  
class TestFullWorkflows:
    """Complete workflow integration tests"""
```

### **Test Execution Commands**
```bash
# Run fast tests only (during development)
pytest -m fast

# Run specification and regression tests (before commits)
pytest tests/specification tests/regression

# Run all tests except scaffolding (CI pipeline)
pytest --ignore=tests/scaffolding

# Run performance tests
pytest -m performance

# Clean up expired scaffolding tests
python tests/scripts/test_lifecycle_manager.py --cleanup-expired
```

## 🔍 Test Quality Metrics

### **Healthy Test Suite Indicators**
```python
✅ All scaffolding tests have DELETE_AFTER dates
✅ No expired scaffolding tests  
✅ Clear purpose documentation for all tests
✅ Appropriate lifecycle categorization
✅ Regular cleanup of obsolete tests
✅ High specification test coverage of behavioral contracts
✅ Fast test execution (most tests < 100ms)
✅ Consistent test data and fixtures
```

### **Warning Signs**
```python
⚠️ Scaffolding tests without DELETE_AFTER dates
⚠️ Tests older than 30 days in scaffolding/
⚠️ Tests with unclear or missing purpose
⚠️ Specification tests that test implementation details  
⚠️ Always-passing or always-failing tests
⚠️ Slow test execution blocking development
⚠️ Tests that duplicate existing coverage
```

## 🎓 Testing Best Practices

### **Focus on Behavioral Contracts**
```python
# ✅ Test the contract, not the implementation
def test_pictograph_immutability_contract(self):
    """Test that pictograph operations return new instances"""
    # Focus on the behavior that must never change

# ❌ Don't test implementation details  
def test_pictograph_uses_specific_internal_method(self):
    """Test that pictograph calls _internal_method"""
    # This breaks when implementation changes
```

### **Use Appropriate Test Lifecycles**
```python
# ✅ Permanent behavioral contracts → specification/
# ✅ Bug prevention → regression/  
# ✅ Temporary debugging → scaffolding/ with DELETE_AFTER
# ✅ Component isolation → unit/
# ✅ Service integration → integration/
```

### **Maintain Test Data Quality**
```python
# ✅ Use realistic test data
# ✅ Validate test data is semantically correct
# ✅ Share common fixtures
# ✅ Keep test data simple and focused
```

This testing strategy ensures that TKA's sophisticated architecture remains stable and maintainable while enabling confident refactoring and feature development.
