# TKA Development Workflow - Working with World-Class Architecture

## 🎯 Overview

Working with TKA's sophisticated architecture requires understanding the **development patterns** and **workflows** that make you productive with 80+ services, clean architecture, and enterprise-grade dependency injection.

## 🚀 Daily Development Workflow

### **Step 1: Start With the Right Application Mode**
```bash
# Development (full UI, real persistence)
python main.py

# Fast testing (mock services, in-memory storage) 
python main.py --test

# CI/CD or server work (no UI, real logic)
python main.py --headless

# Workflow recording (capture user interactions)
python main.py --record
```

### **Step 2: Understand Your Task's Layer**
Before writing code, identify which architectural layer your work belongs to:

```python
# 🎨 Presentation Layer: UI, layouts, user interactions
"Add a new button"              → presentation/components/
"Change layout behavior"        → presentation/tabs/
"Modify UI styling"             → presentation/components/

# 🎮 Application Layer: Business workflows, service orchestration  
"Add positioning algorithm"     → application/services/positioning/
"Modify data processing"        → application/services/data/
"Change settings behavior"      → application/services/settings/

# 🧠 Domain Layer: Core business logic, models
"Add new motion type"           → domain/models/
"Modify business rules"         → domain/services/

# 🔧 Infrastructure Layer: External integrations, storage
"Change file format"            → infrastructure/storage/
"Add API endpoint"              → infrastructure/api/
"Modify database access"        → infrastructure/storage/

# ⚙️ Core Layer: Framework utilities, DI, shared types
"Add new service interface"     → core/interfaces/
"Modify dependency injection"   → core/dependency_injection/
"Add shared utilities"          → core/types/
```

### **Step 3: Find the Right Service**
Use the service discovery patterns:

```python
# Method 1: Use DI debugging tools
container = get_container()
registrations = container.get_registrations()
print([svc.__name__ for svc in registrations.keys()])

# Method 2: Follow naming conventions
"I need to manage pictographs"     → IPictographManagementService
"I need to handle positioning"     → IArrowPositioningOrchestrator  
"I need to access data"            → IDataService
"I need to manage settings"        → ISettingsService

# Method 3: Check service categories
"Core application logic"           → application/services/core/
"Mathematical calculations"        → application/services/positioning/
"Data operations"                  → application/services/data/
"UI state management"              → application/services/ui/
```

## 🛠️ Common Development Tasks

### **Adding a New Feature**

#### **1. Small UI Feature (Button, Control)**
```python
# Step 1: Create the UI component (Presentation)
class NewFeatureButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("New Feature", parent)
        self.clicked.connect(self.on_clicked)
    
    def on_clicked(self):
        # Delegate to application service
        container = get_container()
        feature_service = container.resolve(IFeatureService)
        feature_service.execute_feature()

# Step 2: Register in parent widget
# Step 3: No new services needed (use existing ones)
```

#### **2. New Business Logic Feature**
```python
# Step 1: Define interface (Core)
class INewFeatureService(ABC):
    @abstractmethod
    def execute_feature(self) -> Result[FeatureResult, AppError]:
        pass

# Step 2: Implement service (Application)  
class NewFeatureService(INewFeatureService):
    def __init__(self, data_service: IDataService, settings_service: ISettingsService):
        self.data_service = data_service
        self.settings_service = settings_service
    
    def execute_feature(self) -> Result[FeatureResult, AppError]:
        # Implementation using other services

# Step 3: Register in DI container (Application Factory)
container.register_singleton(INewFeatureService, NewFeatureService)

# Step 4: Use in UI (Presentation)
feature_service = container.resolve(INewFeatureService)
result = feature_service.execute_feature()
```

#### **3. New Mathematical Algorithm**
```python
# Step 1: Create calculator service (Application)
class NewAlgorithmCalculator:
    def calculate(self, input_data: AlgorithmInput) -> AlgorithmResult:
        # Pure mathematical function
        return self._apply_algorithm(input_data)

# Step 2: Integrate into orchestrator (if needed)
class ExistingOrchestrator:
    def __init__(self, ..., new_calculator: NewAlgorithmCalculator):
        self.new_calculator = new_calculator
    
    def orchestrate_workflow(self, data):
        # Use new calculator in pipeline
        result = self.new_calculator.calculate(algorithm_input)

# Step 3: Register in DI
container.register_singleton(NewAlgorithmCalculator, NewAlgorithmCalculator)

# Step 4: Add comprehensive tests
```

### **Modifying Existing Features**

#### **1. UI Changes**
```python
# Find the component in presentation layer
# Modify only the UI logic
# Delegate business logic to existing services

class ExistingWidget:
    def modify_behavior(self):
        # Get service via DI (don't create manually)
        service = get_container().resolve(IRelevantService)
        result = service.handle_business_logic()
        
        # Update UI based on result
        self.update_display(result)
```

#### **2. Business Logic Changes**
```python
# Find the responsible service
# Modify only that service
# Maintain interface contracts

class ExistingService:
    def existing_method(self, data):
        # Modify implementation
        # Keep same interface
        # Add error handling if needed
        try:
            result = self._new_logic(data)
            return success(result)
        except Exception as e:
            return failure(app_error(ErrorType.BUSINESS_LOGIC_ERROR, str(e)))
```

#### **3. Data Structure Changes**
```python
# Modify domain models (Domain layer)
@dataclass(frozen=True) 
class ExistingModel:
    existing_field: str
    new_field: Optional[str] = None  # Add new field with default
    
    # Add new methods if needed
    def new_behavior(self) -> str:
        return f"{self.existing_field}:{self.new_field}"

# Update services that use the model
# Add migration logic if needed
# Update tests
```

## 🔍 Debugging Workflow

### **Understanding Service Dependencies**
```python
# When you're lost in the service maze
container = get_container()

# Get full dependency graph
dependency_graph = container.get_dependency_graph()
for service, deps in dependency_graph.items():
    if "pictograph" in service.lower():  # Filter to relevant services
        print(f"{service} depends on: {deps}")

# Get performance metrics
metrics = container.get_performance_metrics()
print("Most used services:", metrics["most_resolved_services"])
```

### **Tracing Service Resolution**
```python
# Enable DI debugging
logging.getLogger("core.dependency_injection").setLevel(logging.DEBUG)

# Resolve service and watch the logs
container = get_container()
service = container.resolve(IPictographManagementService)

# Check resolution path
resolution_path = container.get_debugging_tools().trace_resolution_path(IPictographManagementService)
print("Resolution path:", resolution_path)
```

### **Finding the Right Service for a Bug**
```python
# Method 1: Start from the UI and trace backwards
# UI Component → Service Interface → Service Implementation

# Method 2: Use error messages
# Exception messages often contain service names

# Method 3: Use performance metrics
# See which services are called most frequently

# Method 4: Check recent git history
# See what services were modified recently
```

## 🧪 Testing Workflow

### **Unit Testing Services**
```python
# Test services in isolation using dependency injection
@pytest.fixture
def pictograph_service():
    container = DIContainer()
    # Register mock dependencies
    container.register_singleton(IDataService, MockDataService)
    container.register_singleton(IValidationService, MockValidationService)
    # Register real service under test
    container.register_singleton(IPictographManagementService, PictographManagementService)
    
    return container.resolve(IPictographManagementService)

def test_create_pictograph(pictograph_service):
    beat_data = BeatData(beat_number=1, letter="A")
    result = pictograph_service.create_pictograph(beat_data)
    assert result.is_success()
    assert result.value.id is not None
```

### **Integration Testing**
```python
# Test service combinations using test application mode
def test_positioning_integration():
    container = ApplicationFactory.create_test_app()
    
    # Get real services (but with mock storage)
    positioning_service = container.resolve(IArrowPositioningOrchestrator)
    pictograph_service = container.resolve(IPictographManagementService)
    
    # Test full workflow
    pictograph = pictograph_service.create_pictograph(beat_data)
    position = positioning_service.calculate_arrow_position(arrow_data, pictograph)
    assert position is not None
```

### **UI Testing**
```python
# Test UI components with real services
@pytest.fixture
def graph_editor():
    app = QApplication.instance() or QApplication([])
    container = ApplicationFactory.create_test_app()
    
    return GraphEditor(container=container)

def test_graph_editor_interaction(graph_editor):
    # Test UI interactions
    graph_editor.select_arrow("blue")
    assert graph_editor.selected_arrow == "blue"
```

## ⚡ Performance Optimization Workflow

### **Identifying Bottlenecks**
```python
# Use built-in performance monitoring
container = get_container()
metrics = container.get_performance_metrics()

# Find slow services
print(f"Average resolution time: {metrics['average_resolution_time']:.4f}s")
print(f"Max resolution time: {metrics['max_resolution_time']:.4f}s")

# Check cache performance  
from core.dependency_injection.service_resolvers import ConstructorResolver
cache_stats = ConstructorResolver.get_cache_stats()
hit_rate = cache_stats['hits'] / (cache_stats['hits'] + cache_stats['misses']) * 100
print(f"DI cache hit rate: {hit_rate:.1f}%")
```

### **Optimizing Service Creation**
```python
# Profile service creation
import cProfile
import time

def profile_service_creation():
    container = get_container()
    
    start_time = time.time()
    service = container.resolve(IExpensiveService)
    end_time = time.time()
    
    print(f"Service creation took: {end_time - start_time:.4f}s")

# Use lazy loading for expensive services
container.register_lazy(IExpensiveService, ExpensiveService)
lazy_service = container.resolve_lazy(IExpensiveService)
```

### **Monitoring Mathematical Performance**
```python
# Profile positioning calculations
def profile_positioning():
    positioning_service = container.resolve(IArrowPositioningOrchestrator)
    
    start_time = time.time()
    for i in range(1000):
        position = positioning_service.calculate_arrow_position(arrow_data, pictograph_data)
    end_time = time.time()
    
    print(f"1000 positioning calculations: {end_time - start_time:.4f}s")
    print(f"Average per calculation: {(end_time - start_time) / 1000:.6f}s")
```

## 🎯 Best Practices for Daily Development

### **DO: Follow Dependency Injection Patterns**
```python
# ✅ Always use DI container
container = get_container()
service = container.resolve(IMyService)

# ✅ Define interfaces first
class IMyNewService(ABC):
    @abstractmethod
    def do_something(self) -> Result[Something, AppError]:
        pass

# ✅ Use constructor injection
class MyService:
    def __init__(self, dependency1: IDependency1, dependency2: IDependency2):
        self.dependency1 = dependency1
        self.dependency2 = dependency2
```

### **DON'T: Bypass the Architecture**
```python
# ❌ Don't create services manually
service = MyService()

# ❌ Don't import concrete implementations in UI
from application.services.concrete_service import ConcreteService

# ❌ Don't put business logic in UI
class UIComponent:
    def on_click(self):
        # Don't do complex calculations here
        result = complex_mathematical_calculation()
```

### **DO: Use Result Types for Error Handling**
```python
# ✅ Explicit error handling
def my_operation() -> Result[MyResult, AppError]:
    try:
        result = do_complex_work()
        return success(result)
    except Exception as e:
        return failure(app_error(ErrorType.OPERATION_ERROR, str(e)))

# ✅ Handle results properly
result = my_service.my_operation()
if result.is_success():
    data = result.value
else:
    logger.error(f"Operation failed: {result.error}")
```

### **DO: Test at the Right Level**
```python
# ✅ Unit test individual services
def test_calculation_service():
    calculator = CalculationService()
    result = calculator.calculate(input_data)
    assert result == expected_result

# ✅ Integration test service combinations  
def test_service_workflow():
    container = ApplicationFactory.create_test_app()
    orchestrator = container.resolve(IOrchestrator)
    result = orchestrator.execute_workflow(test_data)
    assert result.is_success()

# ✅ UI test user workflows
def test_user_workflow():
    # Test complete user interactions
    pass
```

## 🎓 Learning Path for New Features

### **Week 1: Understanding the Domain**
1. Learn the service you need to modify
2. Trace its dependencies
3. Understand its role in the larger workflow
4. Run the existing tests

### **Week 2: Making Changes**
1. Write tests for your changes first
2. Modify the service implementation
3. Update dependent services if needed
4. Ensure all tests pass

### **Week 3: Integration**
1. Test your changes in different application modes
2. Verify UI integration works correctly  
3. Check performance impact
4. Update documentation if needed

## 🎯 Troubleshooting Common Issues

### **"I can't find the right service"**
```python
# Use DI debugging
container = get_container()
all_services = container.get_registrations()
relevant_services = [svc for svc in all_services.keys() if "keyword" in svc.__name__.lower()]
print(relevant_services)
```

### **"My service isn't being injected"**
```python
# Check service registration
try:
    service = container.resolve(IMyService)
    print("✅ Service is registered")
except Exception as e:
    print(f"❌ Service registration issue: {e}")

# Validate all registrations
container.validate_all_registrations()
```

### **"I'm getting circular dependency errors"**
```python
# Use validation tools
container.get_debugging_tools().detect_circular_dependencies(MyService, container.get_registry())

# Or check dependency graph
dependency_graph = container.get_dependency_graph()
# Look for cycles in the graph
```

### **"The positioning system is giving wrong results"**
```python
# Enable detailed positioning logs
logger = logging.getLogger('application.services.positioning')
logger.setLevel(logging.DEBUG)

# Test with known good data
# Check each step of the positioning pipeline
# Verify motion type and grid mode are correct
```

This development workflow enables you to work productively with TKA's sophisticated architecture while maintaining the benefits of clean, well-organized code.
