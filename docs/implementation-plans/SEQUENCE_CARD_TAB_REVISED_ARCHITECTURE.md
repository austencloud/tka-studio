# REVISED: Sequence Card Tab Architecture Audit & Implementation Plan

## Architecture Audit Against Established Patterns

After researching established patterns (Clean Architecture, Service Layer, Qt Model/View), I've identified several critical improvements needed in my original plan:

### ❌ Issues with Original Plan

1. **Over-Fragmentation**: Splitting into 7+ services is excessive for a Qt desktop app
2. **Qt Anti-Patterns**: Ignored Qt's Model/View paradigm in favor of generic service layer
3. **Premature Abstraction**: Created interfaces before understanding concrete needs
4. **Missing Qt Integration**: No consideration of Qt signals/slots communication pattern
5. **Testing Complexity**: Unit testing Qt widgets is notoriously difficult and often counterproductive

### ✅ Revised Architecture Based on Research

## Modern Qt Architecture Pattern

Based on Qt Model/View documentation and Clean Architecture principles:

```
┌─────────────────────────────────────────┐
│           PRESENTATION LAYER            │ ← Qt-Specific
├─────────────────────────────────────────┤
│  SequenceCardView (QWidget)            │
│  ├─ Header Component (controls)         │
│  ├─ Navigation Sidebar (filters)        │
│  ├─ Content Display (scrollable)        │
│  └─ Status/Progress Components          │
├─────────────────────────────────────────┤
│  SequenceCardModel (QAbstractItemModel)│ ← Qt Model/View
│  ├─ Data Management                     │
│  ├─ Cache Coordination                  │
│  └─ Signal Emissions                    │
├─────────────────────────────────────────┤
│           BUSINESS LAYER                │ ← Platform Agnostic
├─────────────────────────────────────────┤
│  SequenceDataManager                    │
│  ├─ File System Operations              │
│  ├─ Metadata Processing                 │
│  └─ Data Validation                     │
│                                         │
│  SequenceCacheManager                   │
│  ├─ Multi-level LRU Caching             │
│  ├─ Memory Management                   │
│  └─ Performance Tracking                │
│                                         │
│  SequenceExportManager                  │
│  ├─ Image Generation Pipeline           │
│  ├─ Batch Processing                    │
│  └─ Progress Coordination               │
├─────────────────────────────────────────┤
│           INFRASTRUCTURE                │
├─────────────────────────────────────────┤
│  File System • Settings • Image APIs    │
└─────────────────────────────────────────┘
```

## Concrete File Structure

```
src/desktop/modern/src/
├── application/
│   └── services/
│       └── sequence_card/
│           ├── __init__.py
│           ├── sequence_data_manager.py      # File system + metadata
│           ├── sequence_cache_manager.py     # Multi-level caching
│           ├── sequence_export_manager.py    # Export coordination
│           └── sequence_settings_manager.py  # Settings persistence
├── presentation/
│   └── sequence_card/
│       ├── __init__.py
│       ├── sequence_card_view.py            # Main QWidget container
│       ├── sequence_card_model.py           # QAbstractItemModel
│       ├── components/
│       │   ├── __init__.py
│       │   ├── header_component.py          # Controls and progress
│       │   ├── navigation_component.py      # Length/column selection
│       │   ├── content_component.py         # Scrollable display area
│       │   └── status_component.py          # Status messages
│       └── adapters/
│           ├── __init__.py
│           ├── qt_signal_adapter.py         # Qt signals ↔ business logic
│           └── image_cache_adapter.py       # QPixmap ↔ cache data
└── core/
    └── interfaces/
        ├── __init__.py
        ├── sequence_data_interface.py
        ├── sequence_cache_interface.py
        └── sequence_export_interface.py
```

## Revised Implementation Phases

### Phase 1: Core Business Services (Week 1-2)

**Target**: Platform-agnostic business logic

#### Services to Implement:

1. **`SequenceDataManager`**
   - File system scanning and filtering
   - Metadata extraction and validation
   - Data structure normalization

2. **`SequenceCacheManager`**
   - LRU cache implementation
   - Memory management policies
   - Performance metrics collection

3. **`SequenceSettingsManager`**
   - Settings persistence (column count, last length)
   - Configuration validation
   - Change notifications

#### Key Interfaces:

```python
class ISequenceDataManager(Protocol):
    def get_sequences_by_length(self, path: str, length: int) -> List[SequenceData]
    def watch_directory_changes(self, path: str, callback: Callable) -> None
    def extract_metadata(self, image_path: str) -> SequenceMetadata

class ISequenceCacheManager(Protocol):
    def get_cached_image(self, path: str, scale: float) -> Optional[bytes]
    def cache_image(self, path: str, scale: float, data: bytes) -> None
    def get_cache_stats(self) -> CacheStats
    def optimize_memory_usage(self) -> None
```

#### Testing Strategy Phase 1:

- **Unit Tests**: Business logic without Qt dependencies
- **Integration Tests**: Service interactions
- **Performance Tests**: Cache behavior and memory usage
- **File System Tests**: Directory scanning accuracy

### Phase 2: Qt Model Integration (Week 3-4)

**Target**: Qt Model/View implementation

#### Components to Implement:

4. **`SequenceCardModel`** (inherits `QAbstractItemModel`)
   - Integrates with business services
   - Implements Qt model interface
   - Handles data change notifications
   - Manages view state synchronization

5. **Qt Adapters**
   - Signal coordination between Qt and business layers
   - QPixmap conversion from cache data
   - Progress reporting integration

#### Key Qt Integration:

```python
class SequenceCardModel(QAbstractItemModel):
    def __init__(self, data_manager: ISequenceDataManager,
                 cache_manager: ISequenceCacheManager):
        super().__init__()
        self._data_manager = data_manager
        self._cache_manager = cache_manager
        self._sequences: List[SequenceData] = []

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._sequences)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> Any:
        # Delegate to business services
        # Handle Qt-specific data conversion

    def refresh_sequences(self, length: int) -> None:
        # Coordinate with data manager
        # Emit model change signals
```

#### Testing Strategy Phase 2:

- **Qt Model Tests**: Model interface compliance
- **Signal/Slot Tests**: Event propagation
- **Data Binding Tests**: Business service integration
- **Memory Tests**: Qt object lifecycle management

### Phase 3: UI Components (Week 5-6)

**Target**: Modern Qt UI implementation

#### Components to Implement:

6. **`SequenceCardView`** (main container)
7. **`HeaderComponent`** (controls, progress, actions)
8. **`NavigationComponent`** (length/column selection)
9. **`ContentComponent`** (scrollable sequence display)

#### Modern Qt Patterns:

```python
class SequenceCardView(QWidget):
    def __init__(self, data_manager: ISequenceDataManager,
                 cache_manager: ISequenceCacheManager):
        super().__init__()

        # Create model
        self._model = SequenceCardModel(data_manager, cache_manager)

        # Create view components
        self._header = HeaderComponent(self)
        self._navigation = NavigationComponent(self)
        self._content = ContentComponent(self)

        # Connect signals
        self._setup_signal_connections()

    def _setup_signal_connections(self) -> None:
        # Wire Qt signals between components
        self._navigation.length_changed.connect(self._model.refresh_sequences)
        self._model.dataChanged.connect(self._content.refresh_display)
```

#### Testing Strategy Phase 3:

- **Visual Tests**: Screenshot comparison
- **Interaction Tests**: User input handling
- **Layout Tests**: Responsive behavior
- **Integration Tests**: Component communication

### Phase 4: Export System (Week 7-8)

**Target**: Export functionality with progress tracking

#### Components to Implement:

10. **`SequenceExportManager`**
    - Integrates with legacy TempBeatFrame
    - Batch processing with cancellation
    - Progress reporting
    - Quality settings management

#### Testing Strategy Phase 4:

- **Export Tests**: File output validation
- **Performance Tests**: Large dataset exports
- **Quality Tests**: Image comparison
- **Progress Tests**: Cancellation and resumption

### Phase 5: Integration & Polish (Week 9-10)

**Target**: Full system integration and optimization

#### Final Integration:

- Dependency injection setup
- Error handling standardization
- Performance optimization
- Memory leak prevention
- Documentation completion

## Testing Strategy - Pragmatic Approach

### What NOT to Test (Based on Qt Best Practices):

- ❌ Qt widget internal behavior (trust Qt framework)
- ❌ Signal/slot mechanism (Qt's responsibility)
- ❌ Layout calculations (unless custom logic)
- ❌ Paint events (unless custom painting)

### What TO Test:

- ✅ Business logic in isolation
- ✅ Data transformations
- ✅ Cache behavior and performance
- ✅ File system operations
- ✅ Integration between services
- ✅ Model data accuracy
- ✅ Export functionality

### Testing Tools & Approaches:

#### 1. Business Logic Tests (Python unittest):

```python
class TestSequenceDataManager(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.data_manager = SequenceDataManager()

    def test_sequence_filtering_by_length(self):
        # Create test data
        sequences = self.data_manager.get_sequences_by_length(self.temp_dir, 16)
        # Assert accuracy vs legacy behavior

    def test_metadata_extraction_accuracy(self):
        # Compare with legacy MetaDataExtractor
```

#### 2. Qt Model Tests (pytest-qt):

```python
def test_model_data_access(qtmodeltester):
    model = SequenceCardModel(mock_data_manager, mock_cache_manager)
    qtmodeltester.check(model)  # Qt's built-in model validator
```

#### 3. Visual Regression Tests:

```python
def test_sequence_card_layout(qtbot):
    view = SequenceCardView(mock_services)
    qtbot.addWidget(view)

    # Take screenshot
    pixmap = view.grab()
    # Compare with reference image
```

#### 4. Performance Tests:

```python
def test_cache_performance():
    cache_manager = SequenceCacheManager(cache_size=1000)

    # Load test data
    start_time = time.time()
    for i in range(1000):
        cache_manager.get_cached_image(f"test_path_{i}", 1.0)

    # Assert performance targets
    assert time.time() - start_time < 2.0  # Sub-2 second target
```

## Risk Mitigation - Lessons from Research

### 1. **Avoid Microservice Patterns in Desktop Apps**

- **Risk**: Over-engineering with too many services
- **Solution**: Use 3-4 well-defined managers instead of 7+ micro-services

### 2. **Embrace Qt Patterns**

- **Risk**: Fighting Qt's architecture
- **Solution**: Use Model/View pattern as intended by Qt

### 3. **Incremental UI Migration**

- **Risk**: Big-bang UI replacement
- **Solution**: Component-by-component replacement with adapter pattern

### 4. **Memory Management Focus**

- **Risk**: Memory leaks in Qt applications
- **Solution**: Explicit resource management and testing

### 5. **Cache Complexity**

- **Risk**: Cache inconsistency
- **Solution**: Single source of truth with event-driven invalidation

## Success Criteria (Revised)

### Functional Parity Checkpoints:

- [ ] **Week 2**: Business services pass legacy comparison tests
- [ ] **Week 4**: Qt model provides same data as legacy display
- [ ] **Week 6**: UI components match legacy visual appearance
- [ ] **Week 8**: Export produces identical files to legacy
- [ ] **Week 10**: Full integration passes stress tests

### Performance Benchmarks:

- [ ] Sequence loading: <2 seconds for 1000+ sequences (vs legacy)
- [ ] Memory usage: <400MB peak (vs legacy 500MB+)
- [ ] Cache hit rate: >85% for repeated operations
- [ ] UI responsiveness: <50ms for interactions
- [ ] Export speed: Match legacy ±10%

### Code Quality Gates:

- [ ] Business logic: 90%+ test coverage
- [ ] Qt integration: 70%+ test coverage (realistic for Qt apps)
- [ ] Zero memory leaks in 24-hour stress test
- [ ] All Qt model tests pass
- [ ] Visual regression tests pass

## Common Pitfalls Prevention

### 1. **Qt Object Lifecycle Issues**

```python
# ❌ Wrong: Creates memory leaks
def create_temporary_widget():
    widget = QWidget()  # No parent - never cleaned up
    return widget

# ✅ Correct: Proper parent assignment
def create_managed_widget(parent):
    widget = QWidget(parent)  # Parent manages lifecycle
    return widget
```

### 2. **Signal Connection Memory Leaks**

```python
# ❌ Wrong: Lambda captures can create cycles
signal.connect(lambda: self.some_method(large_object))

# ✅ Correct: Use weak references or proper cleanup
signal.connect(self.some_method)
```

### 3. **Model/View Data Consistency**

```python
# ❌ Wrong: Direct data manipulation
self._sequences.append(new_sequence)  # View won't update

# ✅ Correct: Proper model notifications
self.beginInsertRows(QModelIndex(), len(self._sequences), len(self._sequences))
self._sequences.append(new_sequence)
self.endInsertRows()
```

### 4. **Threading Issues with Qt**

```python
# ❌ Wrong: Direct UI updates from worker thread
def worker_thread():
    result = expensive_operation()
    self.label.setText(result)  # Crashes!

# ✅ Correct: Use signals or QMetaObject.invokeMethod
def worker_thread():
    result = expensive_operation()
    self.result_ready.emit(result)  # Thread-safe signal
```

This revised plan addresses the architectural concerns by:

1. **Following Qt patterns** rather than fighting them
2. **Reducing complexity** to manageable components
3. **Focusing on testable business logic** separation
4. **Providing concrete implementation details**
5. **Including realistic testing strategies**
6. **Addressing Qt-specific pitfalls** proactively

The result should be a more maintainable, performant, and Qt-idiomatic solution.
