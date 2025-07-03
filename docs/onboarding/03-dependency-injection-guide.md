# TKA Dependency Injection Guide - Enterprise-Grade DI System

## 🎯 Overview

TKA uses a **custom-built, enterprise-grade dependency injection system** with 7 specialized modules. This isn't over-engineering - it's sophisticated infrastructure that enables clean architecture with 80+ services across multiple application modes.

## 🏗️ The 7 DI Modules

```
core/dependency_injection/
├── 🎭 di_container.py              # Main coordinator (the boss)
├── 📋 service_registry.py          # Service registration management  
├── 🔗 service_resolvers.py         # Resolution strategies (Chain of Responsibility)
├── ✅ validation_engine.py         # Protocol compliance & validation
├── ♻️  lifecycle_manager.py        # Service lifecycle & cleanup
├── 🔍 debugging_tools.py           # Performance & debugging utilities
└── ⚙️  config_registration.py      # Configuration object management
```

## 🧠 ELI5: Think of DI Like a Smart Restaurant

### **DIContainer = Head Chef/Manager**
The boss who doesn't cook but coordinates everything:
```python
container = get_container()
service = container.resolve(IMyService)  # "Get me chicken parmesan"
```

### **ServiceRegistry = Recipe Book & Pantry**
Knows what's available and how to make it:
```python
registry.register_singleton(IService, Implementation)  # "Chicken parmesan uses ChickenService"
registry.register_transient(ILogger, FileLogger)       # "Make fresh salads each time"
```

### **ResolverChain = Kitchen Staff**
Different ways to fulfill requests:
1. **SingletonResolver**: "Do we have one already made?"
2. **ConstructorResolver**: "Can we make it fresh from ingredients?"
3. **FactoryResolver**: "Do we have a special machine for this?"

### **ValidationEngine = Health Inspector**
Makes sure everything is safe before opening:
```python
# Checks that ChefService really knows how to cook
# Ensures we can get all ingredients ChefService needs
# Prevents circular dependencies (bread baker needs flour from pizza maker who needs dough from bread baker)
```

### **LifecycleManager = Opening/Closing Crew**
Handles setup and cleanup:
```python
# Turn on ovens when chefs arrive (initialize services)
# Clean up and turn off equipment when closing (cleanup services)
# Handle special events like "wedding party section" (scoped instances)
```

### **DebuggingTools = Restaurant Analytics**
Tracks performance and helps debug:
```python
# "Chicken parmesan takes 12 minutes on average"
# "The pasta station needs ingredients from 5 other stations"
# "Pizza is our most popular dish"
```

### **ConfigRegistration = Menu Setup**
Sets up all the restaurant's rules and policies at opening.

## 🎮 Basic Usage (90% of What You'll Do)

### **Getting Services (The Simple Way)**
```python
# Step 1: Get the container
container = get_container()

# Step 2: Ask for what you need
pictograph_service = container.resolve(IPictographManagementService)
data_service = container.resolve(IDataService)
settings_service = container.resolve(ISettingsService)

# That's it! The DI system handles everything else automatically.
```

### **Application Startup (Once Per App)**
```python
# The application factory sets up everything
container = ApplicationFactory.create_production_app()

# Or for testing
container = ApplicationFactory.create_test_app()

# Now all services are registered and ready to use
```

## 🔧 Advanced Features (When You Need Them)

### **Multiple Service Lifetimes**
```python
# Singleton: One instance for the entire application
container.register_singleton(IDataService, FileDataService)

# Transient: New instance every time you ask
container.register_transient(ILogger, FileLogger)

# Scoped: One instance per "scope" (like web requests)
container.register_scoped(IUserSession, UserSessionService, ServiceScope.SESSION)

# Lazy: Create only when first accessed
container.register_lazy(IExpensiveService, ExpensiveService)
```

### **Factory Functions**
```python
# Custom creation logic
container.register_factory(
    IComplexService,
    lambda: ComplexService(
        config=load_config(),
        cache=create_cache()
    )
)
```

### **Scoped Instances (Advanced)**
```python
# Create scopes for logical groupings
container.create_scope("user_session_123")

# Services registered with SESSION scope get one instance per session
session_service = container.resolve(IUserSessionService)

# Clean up the scope when done
container.dispose_scope("user_session_123")  # Automatic cleanup
```

## 🎯 Service Registration Patterns

### **Interface-First Design**
```python
# 1. Define interface (contract)
class IPictographService(ABC):
    @abstractmethod
    def create_pictograph(self, beat_data: BeatData) -> PictographData:
        pass

# 2. Implement the interface  
class PictographService(IPictographService):
    def create_pictograph(self, beat_data: BeatData) -> PictographData:
        # Implementation here
        
# 3. Register interface → implementation
container.register_singleton(IPictographService, PictographService)

# 4. Resolve by interface
service = container.resolve(IPictographService)  # Gets PictographService instance
```

### **Automatic Constructor Injection**
```python
class ComplexService:
    def __init__(
        self,
        data_service: IDataService,           # Automatically injected
        settings_service: ISettingsService,  # Automatically injected
        logger: ILogger,                     # Automatically injected
    ):
        self.data_service = data_service
        self.settings_service = settings_service
        self.logger = logger
        
# No manual wiring needed! DI container handles it automatically.
```

### **Protocol Validation**
```python
# Define Protocol (contract)
class Drawable(Protocol):
    def draw(self, context: DrawingContext) -> None: ...

# Implementation must fulfill the Protocol
class Arrow:
    def draw(self, context: DrawingContext) -> None:
        # Implementation
        
# Register with automatic validation
container.auto_register(Drawable, Arrow)  # Validates Arrow implements Drawable
```

## 🚨 Multiple Application Modes (The Power Feature)

### **Why This Matters**
TKA can run in 4 different modes with the **same business logic** but **different service implementations**:

```python
# Production: Real file storage + PyQt UI
production_container = ApplicationFactory.create_production_app()

# Test: Mock storage + Mock UI (fast, isolated)
test_container = ApplicationFactory.create_test_app()

# Headless: Real storage + No UI (CI/CD, server)
headless_container = ApplicationFactory.create_headless_app()

# Recording: Real storage + Recording UI (workflow capture)
recording_container = ApplicationFactory.create_recording_app()
```

### **Same Service, Different Implementation**
```python
# Production Mode
container.register_singleton(IDataService, FileBasedDataService)
container.register_singleton(IUIService, PyQtUIService)

# Test Mode  
container.register_singleton(IDataService, InMemoryDataService)
container.register_singleton(IUIService, MockUIService)

# Headless Mode
container.register_singleton(IDataService, FileBasedDataService)
container.register_singleton(IUIService, HeadlessUIService)

# Same business logic, different infrastructure!
```

## 🔍 Debugging & Performance Tools

### **Understanding Service Dependencies**
```python
# Get dependency graph
container = get_container()
dependency_graph = container.get_dependency_graph()

# Show which services depend on what
for service, dependencies in dependency_graph.items():
    print(f"{service} depends on: {dependencies}")
```

### **Performance Monitoring**
```python
# Get performance metrics
metrics = container.get_performance_metrics()
print(f"Total resolutions: {metrics['total_resolutions']}")
print(f"Success rate: {metrics['success_rate']:.1f}%")
print(f"Average resolution time: {metrics['average_resolution_time']:.4f}s")

# Most frequently resolved services
for service_info in metrics['most_resolved_services']:
    print(f"{service_info['service']}: {service_info['count']} times")
```

### **Comprehensive Diagnostics**
```python
# Generate full diagnostic report
report = container.generate_diagnostic_report()
print(report)

# Output includes:
# - Service registration summary
# - Performance metrics  
# - Lifecycle information
# - Potential issues and warnings
```

### **Finding Service Registration Issues**
```python
# Validate all registrations can be resolved
try:
    container.validate_all_registrations()
    print("✅ All services registered correctly")
except DependencyInjectionError as e:
    print(f"❌ Registration issue: {e}")
```

## ⚡ Performance Features

### **Constructor Signature Caching**
The DI system caches expensive reflection operations:
```python
# First resolution: Analyzes constructor, caches signature
service1 = container.resolve(IComplexService)

# Subsequent resolutions: Uses cached signature (much faster)
service2 = container.resolve(IComplexService)

# Get cache statistics
from core.dependency_injection.service_resolvers import ConstructorResolver
stats = ConstructorResolver.get_cache_stats()
print(f"Cache hit rate: {stats['hits'] / (stats['hits'] + stats['misses']) * 100:.1f}%")
```

### **Lazy Loading**
```python
# Register expensive service as lazy
container.register_lazy(IExpensiveService, ExpensiveService)

# Get lazy proxy (doesn't create the service yet)
lazy_service = container.resolve_lazy(IExpensiveService)

# Service is created only when first accessed
result = lazy_service.expensive_operation()  # NOW it creates the service
```

## 🎓 Common Patterns & Best Practices

### **Service Composition Pattern**
```python
class ArrowPositioningOrchestrator:
    def __init__(
        self,
        location_calculator: IArrowLocationCalculator,
        rotation_calculator: IArrowRotationCalculator,  
        adjustment_calculator: IArrowAdjustmentCalculator,
        coordinate_system: IArrowCoordinateSystemService,
    ):
        # Compose complex behavior from simple services
        self.location_calculator = location_calculator
        self.rotation_calculator = rotation_calculator
        self.adjustment_calculator = adjustment_calculator
        self.coordinate_system = coordinate_system
        
    def calculate_arrow_position(self, arrow_data, pictograph_data):
        # Orchestrate the pipeline
        location = self.location_calculator.calculate_location(...)
        rotation = self.rotation_calculator.calculate_rotation(...)
        adjustment = self.adjustment_calculator.calculate_adjustment(...)
        return self._compose_final_position(location, rotation, adjustment)
```

### **Configuration Injection Pattern**
```python
class DataService:
    def __init__(self, config: DataConfig):
        self.config = config
        self.base_path = config.data_directory
        
# Register configuration objects
register_configurations(container)

# DataConfig is automatically injected into services that need it
data_service = container.resolve(IDataService)
```

### **Result Types for Error Handling**
```python
def load_data(self) -> Result[pd.DataFrame, AppError]:
    try:
        data = self._load_csv_file("data.csv")
        return success(data)
    except Exception as e:
        return failure(app_error(ErrorType.DATA_ERROR, f"Failed: {e}"))

# Usage with proper error handling
result = data_service.load_data()
if result.is_success():
    dataframe = result.value
else:
    logger.error(f"Data loading failed: {result.error}")
```

## 🚨 Common Pitfalls & How to Avoid Them

### **Don't Create Services Manually**
```python
# ❌ DON'T DO THIS
data_service = DataService()
pictograph_service = PictographService(data_service)

# ✅ DO THIS  
container = get_container()
pictograph_service = container.resolve(IPictographService)
```

### **Don't Bypass Interfaces**
```python
# ❌ DON'T DO THIS
concrete_service = container.resolve(ConcreteDataService)

# ✅ DO THIS
abstract_service = container.resolve(IDataService)
```

### **Don't Ignore Registration Errors**
```python
# Always validate registrations during development
try:
    container.validate_all_registrations()
except DependencyInjectionError as e:
    print(f"Fix this before proceeding: {e}")
```

### **Don't Create Circular Dependencies**
```python
# ❌ ServiceA depends on ServiceB, ServiceB depends on ServiceA
# The validation engine will catch this, but design around it

# ✅ Extract shared dependencies into a third service
# ServiceA and ServiceB both depend on SharedService
```

## 🎯 When to Use Advanced Features

### **Use Scoped Instances For:**
- User sessions in web-like scenarios
- Request-specific data in API modes
- Temporary resource groups that need coordinated cleanup

### **Use Lazy Loading For:**
- Expensive services that might not be needed
- Services with heavy initialization costs
- Optional features that are conditionally used

### **Use Factory Functions For:**
- Complex service creation logic
- Services that need runtime configuration
- Services with dependencies that aren't registered in DI

### **Use Performance Monitoring For:**
- Understanding resolution bottlenecks
- Optimizing service creation patterns
- Debugging DI-related performance issues

## 🏆 Why This DI System Matters

### **For TKA's Complexity**
- **80+ services** need sophisticated coordination
- **Multiple application modes** require different implementations
- **Mathematical precision** needs clean service composition
- **Enterprise features** (monitoring, validation, lifecycle) enable production use

### **For Long-term Maintainability**
- **Interface-based design** makes testing and changes easier
- **Automatic injection** reduces manual wiring errors
- **Performance monitoring** helps identify optimization opportunities
- **Validation engine** catches configuration issues early

This DI system enables TKA to maintain clean architecture at scale while providing the sophisticated features needed for a world-class application. The complexity is justified by the genuine benefits it provides.
