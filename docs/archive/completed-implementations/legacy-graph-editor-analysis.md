# Legacy Graph Editor Functional Analysis

## Overview

This document provides a comprehensive analysis of the legacy graph editor functionality to establish requirements for the modern TKA implementation. The analysis covers all features, interaction patterns, and architectural components.

## Functional Inventory

### Core Editing Capabilities

#### 1. Pictograph Manipulation

- **Beat Display**: Shows current beat's pictograph with full visual representation
- **Arrow Selection**: Click-to-select arrows within the pictograph
- **Visual Feedback**: Selected arrows highlighted with gold border
- **Real-time Updates**: Pictograph updates immediately when adjustments are applied

#### 2. Arrow Editing System

- **Position Adjustment**: WASD keys for fine-tuning arrow positions
- **Rotation Override**: X key to override rotation angles
- **Special Placement Removal**: Z key to remove custom placement entries
- **Prop Placement Override**: C key for prop placement adjustments

#### 3. Adjustment Panel Controls

##### Turns Adjustment

- **Blue/Red Motion Controls**: Separate controls for each motion type
- **Increment/Decrement**: Fine-grained turn value adjustments
- **Visual Display**: Current turn values shown with visual indicators
- **Rotation Direction**: Clockwise/counterclockwise toggle buttons

##### Orientation Picker

- **Start Position Mode**: Orientation controls for start positions
- **Visual Orientation Display**: Current orientation shown graphically
- **Click-to-Change**: Direct orientation selection interface

### User Interaction Patterns

#### 1. Mouse Events

- **Arrow Selection**: Left-click on arrows to select
- **Deselection**: Click empty space to clear selection
- **Visual Feedback**: Immediate cursor change and highlighting
- **Scene Mapping**: Accurate click-to-scene coordinate mapping

#### 2. Keyboard Shortcuts

- **WASD**: Arrow movement (with Shift/Ctrl modifiers for precision)
- **X**: Rotation angle override
- **Z**: Remove special placement entry
- **C**: Prop placement override
- **Modifier Support**: Shift for fine adjustments, Ctrl for coarse adjustments

#### 3. Selection Behavior

- **Global State**: Selected arrow maintained across components
- **Visual Indicators**: Gold border on selected arrows
- **Context Switching**: Selection affects adjustment panel display
- **Clear Selection**: Automatic clearing when appropriate

### Visual Feedback Systems

#### 1. Selection Indicators

- **Arrow Highlighting**: Gold border for selected arrows
- **Cursor Changes**: Wait cursor during operations, pointer for clickable areas
- **Real-time Updates**: Immediate visual feedback for all changes

#### 2. Animation System

- **Slide Animation**: Smooth 300ms slide up/down with OutQuad easing
- **Height Animation**: Dynamic height calculation based on window size
- **Toggle Tab**: Animated repositioning during resize events
- **Placeholder Management**: Smooth space allocation during show/hide

#### 3. Layout Responsiveness

- **Dynamic Sizing**: Height = min(window_height / 3.5, width / 4)
- **Aspect Ratio**: Maintains proper proportions across window sizes
- **Component Scaling**: All child components scale appropriately

### Data Management

#### 1. State Persistence

- **Selected Arrow**: Global state via AppContext
- **Beat Selection**: Current beat maintained across operations
- **Adjustment Values**: Turn values and orientations persisted
- **UI State**: Graph editor visibility and dimensions saved

#### 2. Data Flow Patterns

- **Beat Updates**: Changes propagate to all pictographs with same letter
- **JSON Integration**: Direct updates to special placement data
- **Mirrored Entries**: Automatic handling of symmetrical adjustments
- **Validation**: Data integrity checks before applying changes

#### 3. Undo/Redo Support

- **Command Pattern**: TurnsCommand system for reversible operations
- **State Snapshots**: Before/after states captured for rollback
- **Batch Operations**: Multiple related changes grouped together

## Technical Architecture Review

### Component Structure

#### 1. Main Components

```
LegacyGraphEditor (QFrame)
├── ArrowSelectionManager (selection state)
├── LegacyGraphEditorPictographContainer (pictograph display)
├── LegacyAdjustmentPanel (controls)
├── GraphEditorLayoutManager (layout)
├── GraphEditorToggleTab (show/hide)
└── GraphEditorAnimator (animations)
```

#### 2. Adjustment Panel Structure

```
LegacyAdjustmentPanel
├── TurnsBox (Blue/Red) - for beat editing
│   ├── TurnsWidget (display)
│   ├── TurnsAdjustmentManager (logic)
│   └── RotationDirectionButtons
└── OriPickerBox (Blue/Red) - for start positions
    ├── OriPickerWidget (display)
    └── ClickableOriLabel (interaction)
```

#### 3. Event Handling Hierarchy

```
GE_PictographView
├── GE_PictographViewMouseEventHandler
├── GraphEditorViewKeyEventHandler
└── HotkeyGraphAdjuster
    ├── ArrowMovementManager
    ├── RotAngleOverrideManager
    ├── PropPlacementOverrideManager
    └── SpecialPlacementEntryRemover
```

### Integration Points

#### 1. Sequence Workbench Integration

- **Beat Frame Connection**: Direct access to selected beats
- **Layout Management**: Integrated into workbench layout system
- **Event Coordination**: Synchronized with beat selection events

#### 2. Data Layer Integration

- **JSON Repository**: Direct updates to special placement data
- **Pictograph Collection**: Updates all pictographs with matching letters
- **State Management**: Integration with global application context

#### 3. UI Framework Integration

- **PyQt6 Events**: Native event handling for mouse/keyboard
- **Animation System**: QPropertyAnimation for smooth transitions
- **Layout System**: QStackedLayout for panel switching

## Success Metrics Definition

### Functional Parity Requirements

#### 1. Core Functionality

- [ ] Arrow selection with visual feedback
- [ ] WASD movement with modifier support
- [ ] Turn adjustment with increment/decrement
- [ ] Orientation picker for start positions
- [ ] Real-time pictograph updates
- [ ] Smooth show/hide animations

#### 2. User Experience Standards

- [ ] Response time < 100ms for arrow selection
- [ ] Animation duration 300-400ms for visibility toggle
- [ ] Accurate click detection within 2px tolerance
- [ ] Keyboard shortcuts work in all contexts
- [ ] Visual feedback appears within 50ms

#### 3. Data Integrity Requirements

- [ ] All adjustments persist correctly
- [ ] Undo/redo operations work reliably
- [ ] Mirrored entries update automatically
- [ ] No data loss during rapid operations
- [ ] Validation prevents invalid states

### Performance Benchmarks

#### 1. Rendering Performance

- **Pictograph Update**: < 50ms for complex pictographs
- **Animation Smoothness**: 60fps during transitions
- **Memory Usage**: < 50MB additional for graph editor
- **Startup Time**: < 200ms to initialize components

#### 2. Interaction Responsiveness

- **Click Response**: < 100ms from click to selection
- **Keyboard Input**: < 50ms from keypress to action
- **Adjustment Application**: < 150ms for turn changes
- **Panel Switching**: < 200ms for mode changes

## Modern Implementation Roadmap

### Phase 1: Core Architecture (Weeks 1-2)

**Priority: Critical**

#### Components to Implement

1. **ModernGraphEditor** (main container)

   - Clean architecture with dependency injection
   - Service-based state management
   - Reactive sizing system

2. **GraphEditorPictographContainer** (display)

   - Modern PictographScene integration
   - Arrow selection with signals
   - Responsive sizing

3. **IGraphEditorService** (business logic)
   - Beat selection management
   - Arrow adjustment operations
   - State persistence

#### Success Criteria

- [ ] Basic pictograph display working
- [ ] Arrow selection functional
- [ ] Service layer operational
- [ ] Clean architecture validated

### Phase 2: Interaction System (Weeks 3-4)

**Priority: High**

#### Components to Implement

1. **Arrow Selection System**

   - Click-to-select functionality
   - Visual feedback (highlighting)
   - Global state management

2. **Keyboard Input Handler**

   - WASD movement system
   - Modifier key support
   - Command pattern for undo/redo

3. **Mouse Event System**
   - Accurate scene coordinate mapping
   - Multi-selection support
   - Context menu integration

#### Success Criteria

- [ ] All keyboard shortcuts working
- [ ] Mouse selection accurate
- [ ] Visual feedback immediate
- [ ] Undo/redo operational

### Phase 3: Adjustment Panels (Weeks 5-6)

**Priority: High**

#### Components to Implement

1. **ModernAdjustmentPanel**

   - Turns adjustment controls
   - Orientation picker
   - Responsive layout

2. **Turn Management System**

   - Increment/decrement controls
   - Real-time value display
   - Validation and limits

3. **Orientation System**
   - Visual orientation picker
   - Start position mode
   - Direct selection interface

#### Success Criteria

- [ ] Turn adjustments working
- [ ] Orientation picker functional
- [ ] Real-time updates operational
- [ ] Panel switching smooth

### Phase 4: Animation & Polish (Weeks 7-8)

**Priority: Medium**

#### Components to Implement

1. **Animation System**

   - Smooth slide transitions
   - Height animations
   - Easing curves

2. **Visual Polish**

   - Modern styling
   - Consistent theming
   - Accessibility features

3. **Performance Optimization**
   - Efficient rendering
   - Memory management
   - Responsive interactions

#### Success Criteria

- [ ] Animations smooth and responsive
- [ ] Visual design consistent
- [ ] Performance meets benchmarks
- [ ] Accessibility compliant

## Test Criteria for Feature Parity

### Automated Test Scenarios

#### 1. Core Functionality Tests

```python
def test_arrow_selection():
    # Click on arrow -> arrow becomes selected
    # Click elsewhere -> selection clears
    # Visual feedback appears immediately

def test_keyboard_shortcuts():
    # WASD moves selected arrow
    # X overrides rotation
    # Z removes special placement
    # C handles prop placement

def test_turn_adjustments():
    # Increment/decrement buttons work
    # Values update in real-time
    # Changes persist correctly
```

#### 2. Integration Tests

```python
def test_beat_selection_integration():
    # Selecting beat updates graph editor
    # Graph editor changes affect beat frame
    # State synchronization works

def test_data_persistence():
    # Adjustments save to JSON
    # Mirrored entries update
    # Undo/redo preserves state
```

#### 3. Performance Tests

```python
def test_response_times():
    # Arrow selection < 100ms
    # Keyboard input < 50ms
    # Animation completion < 400ms
    # Pictograph update < 50ms
```

### Manual Test Scenarios

#### 1. User Workflow Tests

- **Scenario A**: Select beat → open graph editor → select arrow → adjust turns → verify changes
- **Scenario B**: Use keyboard shortcuts for rapid adjustments → verify all changes applied
- **Scenario C**: Switch between beats rapidly → verify state management

#### 2. Edge Case Tests

- **Rapid Clicking**: Fast arrow selection changes
- **Keyboard Spam**: Rapid key presses
- **Window Resize**: During animation
- **Data Corruption**: Invalid adjustment values

#### 3. Accessibility Tests

- **Keyboard Navigation**: Tab order and focus
- **Screen Reader**: Proper ARIA labels
- **High Contrast**: Visual elements visible
- **Motor Impairment**: Large click targets

## Architectural Patterns to Preserve vs Modernize

### Patterns to Preserve

#### 1. Component Separation

- **Pictograph Container**: Dedicated display component
- **Adjustment Panel**: Separate control interface
- **Selection Manager**: Centralized selection state
- **Animation System**: Smooth transitions

#### 2. Event-Driven Architecture

- **Signal/Slot Pattern**: Component communication
- **Global State Management**: Selected arrow context
- **Real-time Updates**: Immediate visual feedback
- **Command Pattern**: Undo/redo operations

#### 3. Responsive Design

- **Dynamic Sizing**: Height based on window dimensions
- **Aspect Ratio Maintenance**: Consistent proportions
- **Layout Flexibility**: Adapts to different screen sizes

### Patterns to Modernize

#### 1. Dependency Management

- **Legacy**: Direct component instantiation
- **Modern**: Dependency injection with interfaces
- **Benefit**: Testability and modularity

#### 2. State Management

- **Legacy**: Global AppContext singleton
- **Modern**: Service-based state with reactive patterns
- **Benefit**: Cleaner architecture and better testing

#### 3. Data Access

- **Legacy**: Direct JSON file manipulation
- **Modern**: Repository pattern with domain models
- **Benefit**: Data integrity and abstraction

## Implementation Guidelines

### Service Layer Design

#### 1. IGraphEditorService Interface

```python
class IGraphEditorService(Protocol):
    def set_selected_beat(self, beat: BeatData, index: int) -> None
    def get_selected_beat(self) -> Optional[BeatData]
    def set_arrow_selection(self, arrow_id: str) -> None
    def get_selected_arrow(self) -> Optional[str]
    def apply_turn_adjustment(self, arrow_color: str, turn_value: float) -> bool
    def apply_position_adjustment(self, arrow_id: str, delta_x: int, delta_y: int) -> bool
    def toggle_visibility(self) -> bool
    def get_adjustment_history(self) -> List[AdjustmentCommand]
```

#### 2. State Management Service

```python
class GraphEditorStateService:
    def __init__(self, ui_state_service: IUIStateService):
        self._ui_state_service = ui_state_service
        self._selected_beat: Optional[BeatData] = None
        self._selected_arrow_id: Optional[str] = None
        self._is_visible: bool = False

    def save_state(self) -> None:
        # Persist state through UI state service

    def restore_state(self) -> None:
        # Restore state from persistence
```

### Component Architecture

#### 1. Modern Graph Editor Structure

```
ModernGraphEditor (QFrame)
├── IGraphEditorService (business logic)
├── GraphEditorPictographContainer (display)
├── AdjustmentPanel (controls)
├── ModernToggleTab (visibility)
└── AnimationManager (transitions)
```

#### 2. Reactive Sizing Integration

- **Size Provider**: Use reactive sizing pattern from option picker
- **Callback Registration**: Components register for size updates
- **Unified Sizing**: All components use same reference

#### 3. Clean Architecture Compliance

- **Domain Layer**: BeatData, MotionData (immutable)
- **Application Layer**: GraphEditorService, StateService
- **Infrastructure Layer**: JSON repositories, UI state persistence
- **Presentation Layer**: Qt components, event handlers

### Testing Strategy

#### 1. Unit Testing Approach

```python
class TestGraphEditorService:
    def test_arrow_selection(self, mock_container):
        service = mock_container.resolve(IGraphEditorService)
        service.set_arrow_selection("blue_arrow")
        assert service.get_selected_arrow() == "blue_arrow"

    def test_turn_adjustment(self, mock_container):
        service = mock_container.resolve(IGraphEditorService)
        result = service.apply_turn_adjustment("blue", 0.5)
        assert result is True
```

#### 2. Integration Testing

```python
class TestGraphEditorIntegration:
    def test_beat_selection_flow(self, qtbot_with_container):
        workbench = create_workbench(qtbot_with_container.container)
        graph_editor = workbench.graph_editor

        # Simulate beat selection
        beat_data = create_test_beat()
        graph_editor.set_selected_beat(beat_data, 0)

        # Verify pictograph updates
        assert graph_editor._pictograph_container._current_beat == beat_data
```

#### 3. Performance Testing

```python
class TestGraphEditorPerformance:
    def test_arrow_selection_response_time(self, qtbot):
        start_time = time.time()
        graph_editor.select_arrow("blue_arrow")
        response_time = time.time() - start_time
        assert response_time < 0.1  # 100ms requirement
```

## Risk Mitigation

### High-Risk Areas

#### 1. Animation System

- **Risk**: Jerky or slow animations
- **Mitigation**: Use QPropertyAnimation with proper easing
- **Fallback**: Instant show/hide if performance issues

#### 2. Arrow Selection Accuracy

- **Risk**: Inaccurate click detection
- **Mitigation**: Proper scene coordinate mapping
- **Testing**: Automated click simulation tests

#### 3. State Synchronization

- **Risk**: Inconsistent state between components
- **Mitigation**: Single source of truth via service layer
- **Validation**: State consistency checks

### Medium-Risk Areas

#### 1. Keyboard Shortcut Conflicts

- **Risk**: Shortcuts not working in all contexts
- **Mitigation**: Proper event handling hierarchy
- **Testing**: Context-specific shortcut tests

#### 2. Memory Leaks

- **Risk**: Animation objects not cleaned up
- **Mitigation**: Proper object lifecycle management
- **Monitoring**: Memory usage tests

## Success Validation

### Acceptance Criteria

#### 1. Functional Requirements

- [ ] All legacy features implemented
- [ ] Performance meets or exceeds legacy
- [ ] Visual design consistent with modern TKA
- [ ] Accessibility standards met

#### 2. Technical Requirements

- [ ] Clean architecture principles followed
- [ ] Dependency injection used throughout
- [ ] Comprehensive test coverage (>90%)
- [ ] No memory leaks or performance regressions

#### 3. User Experience Requirements

- [ ] Smooth animations and transitions
- [ ] Responsive to user input
- [ ] Intuitive interaction patterns
- [ ] Consistent with TKA design language

### Delivery Milestones

#### 1. Alpha Release (Week 4)

- Core functionality working
- Basic arrow selection and adjustment
- No animations or polish

#### 2. Beta Release (Week 6)

- All features implemented
- Basic animations working
- Ready for internal testing

#### 3. Release Candidate (Week 8)

- Full feature parity
- Performance optimized
- Complete test coverage

#### 4. Production Release (Week 10)

- User acceptance testing complete
- Documentation finalized
- Ready for deployment

## Conclusion

The legacy graph editor provides a comprehensive set of features that must be preserved in the modern implementation. The roadmap prioritizes core functionality first, followed by interaction systems, adjustment panels, and finally polish. Success will be measured by functional parity, performance benchmarks, and comprehensive test coverage.

The key to success will be maintaining the intuitive user experience of the legacy system while leveraging modern architectural patterns for better maintainability, testability, and extensibility. The reactive sizing pattern developed for the option picker should be applied here as well to ensure consistent behavior across the application.
