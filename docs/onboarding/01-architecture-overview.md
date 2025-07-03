# TKA Architecture Overview - Clean Architecture at Scale

## 🏗️ The Big Picture

TKA implements **Clean Architecture** with strict separation of concerns across 5 distinct layers. This creates a maintainable, testable, and scalable system that can handle the complex mathematical requirements of kinetic alphabet visualization.

## 📚 Layer Structure

```
src/
├── application/      # Application Services Layer
├── core/            # Core Framework & Infrastructure  
├── domain/          # Business Logic & Models
├── infrastructure/  # External Concerns (Storage, API)
└── presentation/    # UI Components & Controllers
```

## 🔄 Dependency Flow (The Golden Rule)

**Dependencies flow INWARD only:**

```
Presentation → Application → Domain
     ↓              ↓         ↑
Infrastructure → Core -------+
```

- **Presentation** depends on Application
- **Application** depends on Domain  
- **Infrastructure** depends on Domain
- **Core** provides shared utilities to all layers
- **Domain** depends on nothing (pure business logic)

## 🎯 Layer Responsibilities

### **Domain Layer (`domain/`)**
**Pure business logic with zero dependencies**

```
domain/
├── models/          # Business entities (BeatData, SequenceData, etc.)
├── repositories/    # Data access interfaces (no implementations!)
└── services/        # Domain services (business rules)
```

**Key Principles:**
- No framework dependencies (no PyQt, no database code)
- Immutable dataclasses with validation
- Pure business logic and rules
- Interfaces only, no implementations

**Example:**
```python
@dataclass(frozen=True)
class BeatData:
    """Pure domain model - no dependencies"""
    beat_number: int
    blue_motion: Optional[MotionData] = None
    red_motion: Optional[MotionData] = None
    letter: Optional[str] = None
```

### **Application Layer (`application/`)**
**Orchestrates business logic using domain models**

```
application/services/
├── core/            # Application orchestration (8 services)
├── data/            # Data management (9 services) 
├── positioning/     # Mathematical algorithms (31 services)
├── settings/        # Configuration management (9 services)
├── ui/              # UI state management (6 services)
└── [other domains]  # Feature-specific services
```

**Key Principles:**
- Depends on Domain interfaces, never implementations
- Contains no business logic (delegates to Domain)
- Orchestrates complex workflows
- Uses dependency injection for all dependencies

**Example:**
```python
class ArrowPositioningOrchestrator:
    def __init__(
        self,
        location_calculator: IArrowLocationCalculator,
        rotation_calculator: IArrowRotationCalculator,
        adjustment_calculator: IArrowAdjustmentCalculator,
    ):
        # Orchestrates domain services via interfaces
```

### **Core Layer (`core/`)**
**Shared framework components used by all layers**

```
core/
├── dependency_injection/  # Enterprise DI system (7 modules)
├── interfaces/           # Service contracts (10 interface files)
├── types/               # Shared types (Result, Point, etc.)
├── events/              # Event bus system
├── performance/         # Performance monitoring
└── logging/             # Smart logging framework
```

**Key Principles:**
- Framework-level services (DI, events, logging)
- Shared types and utilities
- No business logic
- Used by all other layers

### **Infrastructure Layer (`infrastructure/`)**
**External system integrations and implementations**

```
infrastructure/
├── storage/         # File system, database implementations
├── api/            # FastAPI web interface  
├── cache/          # Caching implementations
└── test_doubles/   # Mock implementations
```

**Key Principles:**
- Implements Domain interfaces
- Contains framework-specific code (PyQt, file I/O)
- Adapts external systems to domain needs
- Swappable implementations (file vs database vs memory)

### **Presentation Layer (`presentation/`)**
**User interface and user experience**

```
presentation/
├── components/     # Reusable UI components
├── tabs/          # Main application tabs
└── factories/     # UI component factories
```

**Key Principles:**
- Pure UI logic (layout, styling, events)
- Delegates all business logic to Application layer
- Framework-specific (PyQt6)
- No direct database or file access

## 🎮 Data Flow Example

Let's trace how "Position an Arrow" flows through the architecture:

### **1. User Interaction (Presentation)**
```python
# presentation/components/graph_editor/adjustment_panel.py
def on_position_changed(self, new_position):
    # UI delegates to application service
    self.graph_editor_service.update_arrow_position(arrow_id, new_position)
```

### **2. Application Orchestration (Application)**
```python
# application/services/core/pictograph_management_service.py
def update_arrow_position(self, arrow_id, position):
    # 1. Get current pictograph (domain model)
    pictograph = self.sequence_service.get_current_pictograph()
    
    # 2. Delegate positioning calculation to domain service
    new_position = self.positioning_orchestrator.calculate_arrow_position(
        pictograph.get_arrow(arrow_id), pictograph
    )
    
    # 3. Update domain model (returns new immutable instance)
    updated_pictograph = pictograph.update_arrow_position(arrow_id, new_position)
    
    # 4. Persist changes via infrastructure
    self.persistence_service.save_pictograph(updated_pictograph)
```

### **3. Mathematical Calculation (Application + Domain)**
```python
# application/services/positioning/arrows/orchestration/arrow_positioning_orchestrator.py
def calculate_arrow_position(self, arrow_data, pictograph_data):
    # Complex mathematical pipeline using domain models
    location = self.location_calculator.calculate_location(motion, pictograph_data)
    rotation = self.rotation_calculator.calculate_rotation(motion, location)
    adjustment = self.adjustment_calculator.calculate_adjustment(arrow_data, pictograph_data)
    return compose_final_position(location, rotation, adjustment)
```

### **4. Data Persistence (Infrastructure)**
```python
# infrastructure/storage/file_based_sequence_data_service.py
def save_pictograph(self, pictograph_data):
    # Infrastructure handles file I/O details
    json_data = self.serializer.serialize(pictograph_data)
    self.file_system.write_file(file_path, json_data)
```

## 🔧 Dependency Injection Integration

Every layer uses **dependency injection** to maintain loose coupling:

### **Service Registration (Application Factory)**
```python
# core/application/application_factory.py
def create_production_app():
    container = DIContainer()
    
    # Infrastructure implementations
    container.register_singleton(ISequenceDataService, FileBasedSequenceDataService)
    
    # Application services
    container.register_singleton(IPictographManagementService, PictographManagementService)
    
    # UI services  
    container.register_singleton(ILayoutService, LayoutManagementService)
    
    return container
```

### **Service Resolution**
```python
# Any layer can resolve dependencies
container = get_container()
pictograph_service = container.resolve(IPictographManagementService)
```

## 🎯 Key Architectural Benefits

### **1. Testability**
Each layer can be tested in isolation:
```python
# Test application layer with mock infrastructure
container.register_singleton(ISequenceDataService, MockSequenceDataService)
pictograph_service = container.resolve(IPictographManagementService)
```

### **2. Multiple Application Modes**
Same business logic, different implementations:
- **Production**: File storage + PyQt UI
- **Test**: Memory storage + Mock UI  
- **Headless**: File storage + No UI
- **Recording**: File storage + Recording UI

### **3. Performance Optimization**
- Services are singletons by default (expensive to create once)
- Complex calculations isolated in specialized services
- Dependency injection enables performance monitoring

### **4. Mathematical Precision**
- Positioning algorithms isolated in pure services
- Domain models ensure data integrity
- Complex geometric calculations don't pollute UI code

## ⚡ Working With This Architecture

### **Adding New Features**
1. **Define domain models** (if needed) in `domain/models/`
2. **Create service interfaces** in `core/interfaces/`
3. **Implement application services** in `application/services/`
4. **Register in DI container** in application factory
5. **Create UI components** in `presentation/`

### **Modifying Existing Features**
1. **Identify the correct layer** (where does this logic belong?)
2. **Find the responsible service** (use DI debugging if needed)
3. **Make changes within layer boundaries** (don't bypass the architecture)
4. **Update tests** (follow test lifecycle patterns)

### **Debugging Issues**
1. **Use DI diagnostic tools** to understand service dependencies
2. **Check layer boundaries** (are dependencies flowing the right direction?)
3. **Verify service registration** (is the right implementation being used?)
4. **Use application modes** (test in headless mode for faster debugging)

## 🏆 Why This Architecture Matters

### **For a Complex Domain Like Kinetic Alphabet**
- **Mathematical precision** requires isolated, testable algorithms
- **Multiple UI contexts** need consistent business logic
- **Complex data relationships** benefit from clean domain models
- **Performance requirements** need optimized service composition

### **For Long-term Maintainability**
- **New developers** can understand one layer at a time
- **Changes are isolated** to appropriate layers
- **Testing is comprehensive** with different service implementations
- **Business logic is protected** from framework changes

This architecture enables TKA to handle genuine complexity while remaining maintainable and extensible. Each sophisticated component has a clear purpose and place in the overall system.
