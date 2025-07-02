# Modern Graph Editor Implementation Roadmap - Updated

## Executive Summary

This roadmap has been updated based on comprehensive audit of the current implementation. The primary focus is now on **completing the core data flow** that enables seamless beat selection → panel switching → data modification → real-time propagation across all UI components.

## Current Implementation Status (65% Complete)

### ✅ What's Working (Strong Foundation)

- **Architecture**: Clean service-based architecture with proper DI ✅
- **UI Components**: Frosted glass design, dual panels, toggle tab ✅
- **Basic Functionality**: Beat selection, panel switching, basic controls ✅
- **Animation System**: Smooth sliding animations (400ms OutCubic) ✅

### ❌ Critical Gaps Identified

- **Data Flow**: Changes stored in UI state, not actual beat data ❌
- **Propagation**: No real-time updates to pictographs or beat frame ❌
- **Hotkey System**: Completely missing WASD movement ❌
- **Visual Feedback**: No arrow highlighting or selection indicators ❌

## Priority-Driven Implementation Plan

### 🎯 PHASE 1: Core Data Flow (Week 1) - CRITICAL

**The most important functionality that makes the graph editor valuable**

#### Goal: Beat Selection → Panel Logic → Data Changes → Real Propagation

**Current Problem:**

```python
# Service stores in UI state - NO real data updates
def apply_turn_adjustment(self, arrow_color: str, turn_value: float) -> bool:
    adjustment_key = f"turn_adjustment_{arrow_color}_{self._selected_arrow_id}"
    self.ui_state_service.set_setting(adjustment_key, turn_value)  # ❌ WRONG
    return True
```

**Required Solution:**

```python
def apply_turn_adjustment(self, arrow_color: str, turn_value: float) -> BeatData:
    # 1. Update actual beat data
    if arrow_color == "blue" and self._selected_beat.blue_motion:
        self._selected_beat.blue_motion.turns = turn_value

    # 2. Persist to JSON repository
    self._beat_repository.update_beat(self._selected_beat)

    # 3. Propagate to all UI components
    self._notify_pictograph_updates(self._selected_beat)
    self._notify_beat_frame_updates(self._selected_beat)

    return self._selected_beat
```

#### Deliverables for Week 1:

- [ ] **DataFlowService**: Bridge service to beat repository
- [ ] **Real Beat Data Updates**: Modify actual MotionData objects
- [ ] **JSON Persistence**: Connect to existing beat persistence layer
- [ ] **UI Propagation**: Update graph editor pictograph + beat frame display
- [ ] **Panel Switch Logic**: Perfect start position vs beat detection

#### Success Criteria:

- [ ] Changing turns/orientation immediately updates pictograph
- [ ] Changes persist and reload correctly
- [ ] Beat frame shows updated values
- [ ] Start position triggers orientation picker, beats trigger turns controls

### 🔧 PHASE 2: Hotkey System (Week 2) - HIGH PRIORITY

**Port the powerful WASD movement system that users rely on**

#### Goal: Complete keyboard control system

**Current Problem:**

```python
class GraphEditorHotkeyService:
    """Placeholder service implementation."""  # ❌ Empty placeholder
```

**Required Implementation:**
Port directly from legacy `ArrowMovementManager` with:

- WASD movement with precise adjustment increments
- Shift modifier for 20px adjustments
- Ctrl+Shift for 200px adjustments
- X key for rotation override
- Z key for special placement removal
- C key for prop placement override

#### Deliverables for Week 2:

- [ ] **ArrowMovementService**: Port legacy movement logic
- [ ] **KeyEventHandler**: Comprehensive keyboard input handling
- [ ] **ModifierSupport**: Shift/Ctrl key combinations
- [ ] **SpecialCommands**: X, Z, C key functionality
- [ ] **ResponseTime**: < 100ms for all keyboard inputs

### 🎨 PHASE 3: Visual Feedback System (Week 3) - HIGH PRIORITY

**Make arrow selection obvious and responsive**

#### Goal: Professional visual feedback matching legacy behavior

**Current Problem:**
No visual indication of selected arrows, no cursor changes, no highlighting system.

**Required Features:**

- Gold border highlighting for selected arrows
- Cursor changes (pointer for arrows, wait during operations)
- Real-time visual updates as adjustments are made
- Clear selection indicators

#### Deliverables for Week 3:

- [ ] **ArrowHighlighting**: Gold border system for selected arrows
- [ ] **CursorManagement**: Context-sensitive cursor changes
- [ ] **SelectionIndicators**: Clear visual feedback
- [ ] **ResponsiveUpdates**: < 50ms visual response to selections

### 🧪 PHASE 4: Testing & Integration (Week 4) - MEDIUM PRIORITY

**Ensure reliability and maintainability**

#### Goal: Comprehensive test coverage and integration validation

#### Deliverables for Week 4:

- [ ] **Unit Tests**: >90% coverage for all services
- [ ] **Integration Tests**: Complete workflow testing
- [ ] **Performance Tests**: Response time validation
- [ ] **User Acceptance**: End-to-end workflow validation

## Technical Implementation Details

### Core Data Flow Architecture

```python
# NEW: Complete data flow service
class GraphEditorDataFlowService:
    """Handles the complete beat selection → modification → propagation flow"""

    def __init__(self,
                 beat_repository: IBeatRepository,
                 pictograph_service: IPictographService,
                 beat_frame_service: IBeatFrameService):
        self._beat_repository = beat_repository
        self._pictograph_service = pictograph_service
        self._beat_frame_service = beat_frame_service

    def handle_beat_selection(self, beat_data: BeatData, is_start_position: bool):
        """Core logic: determine which panel to show"""
        if is_start_position:
            return PanelMode.ORIENTATION_PICKER
        else:
            return PanelMode.TURNS_ADJUSTMENT

    def apply_turn_change(self, beat_data: BeatData, arrow_color: str, new_turns: float) -> BeatData:
        """Apply turn change and propagate everywhere"""
        # 1. Update beat data
        updated_beat = self._update_motion_turns(beat_data, arrow_color, new_turns)

        # 2. Persist to storage
        self._beat_repository.save_beat(updated_beat)

        # 3. Update all UI components
        self._pictograph_service.refresh_pictograph(updated_beat)
        self._beat_frame_service.update_beat_display(updated_beat)

        # 4. Handle mirrored entries (for symmetrical sequences)
        self._handle_mirrored_updates(updated_beat)

        return updated_beat

    def apply_orientation_change(self, beat_data: BeatData, arrow_color: str, new_orientation: str) -> BeatData:
        """Apply orientation change and propagate everywhere"""
        # Similar structure to turn changes
        updated_beat = self._update_motion_orientation(beat_data, arrow_color, new_orientation)
        self._beat_repository.save_beat(updated_beat)
        self._pictograph_service.refresh_pictograph(updated_beat)
        self._beat_frame_service.update_beat_display(updated_beat)
        return updated_beat
```

### Panel Switching Logic Enhancement

```python
# ENHANCED: Perfect panel detection
class AdjustmentPanel(QWidget):
    def set_beat(self, beat_data: Optional[BeatData]):
        """Enhanced panel switching with perfect beat type detection"""
        self._current_beat = beat_data

        # Core logic: start position vs regular beat
        if self._is_start_position(beat_data):
            self._show_orientation_picker()
            self._update_orientation_values(beat_data)
        else:
            self._show_turns_controls()
            self._update_turn_values(beat_data)

    def _is_start_position(self, beat_data: BeatData) -> bool:
        """Robust start position detection"""
        if not beat_data:
            return True

        # Check multiple indicators
        return (
            getattr(beat_data, 'is_start_position', False) or
            getattr(beat_data, 'beat_number', 0) == 0 or
            getattr(beat_data, 'sequence_position', 0) == 0
        )
```

### Real-Time Update System

```python
# NEW: Real-time update coordinator
class RealTimeUpdateCoordinator:
    """Ensures all UI components stay synchronized"""

    def __init__(self):
        self._update_listeners = []

    def register_listener(self, component, update_method):
        """Register components that need real-time updates"""
        self._update_listeners.append((component, update_method))

    def broadcast_beat_update(self, updated_beat: BeatData):
        """Notify all registered components of beat changes"""
        for component, update_method in self._update_listeners:
            try:
                update_method(updated_beat)
            except Exception as e:
                print(f"Update failed for {component}: {e}")

    def broadcast_arrow_selection(self, arrow_id: str, beat_data: BeatData):
        """Notify all components of arrow selection changes"""
        for component, update_method in self._update_listeners:
            if hasattr(component, 'handle_arrow_selection'):
                component.handle_arrow_selection(arrow_id, beat_data)
```

## Integration Points with Existing System

### Beat Frame Integration

```python
# CONNECT: Graph editor ↔ Beat frame
class SequenceWorkbench:
    def __init__(self):
        # ... existing setup ...

        # Connect beat frame selection to graph editor
        self.beat_frame.beat_selected.connect(self.graph_editor.set_selected_beat)

        # Connect graph editor changes back to beat frame
        self.graph_editor.beat_modified.connect(self.beat_frame.update_beat_display)
```

### JSON Repository Integration

```python
# CONNECT: Graph editor ↔ Data persistence
class GraphEditorService:
    def __init__(self, beat_repository: IBeatRepository):
        self._beat_repository = beat_repository

    def apply_turn_adjustment(self, arrow_color: str, turn_value: float) -> bool:
        # Get current beat from repository
        current_beat = self._beat_repository.get_beat(self._selected_beat_id)

        # Apply modification
        updated_beat = self._modify_beat_turns(current_beat, arrow_color, turn_value)

        # Save back to repository (triggers JSON update)
        self._beat_repository.save_beat(updated_beat)

        return True
```

## Success Metrics & Validation

### Core Workflow Validation

- [ ] **Beat Selection**: Clicking beat in beat frame immediately shows in graph editor
- [ ] **Panel Switching**: Start position shows orientation picker, beats show turns
- [ ] **Value Changes**: Adjusting turns/orientation immediately updates pictograph
- [ ] **Persistence**: Changes save and reload correctly
- [ ] **Propagation**: Beat frame updates reflect graph editor changes

### Performance Requirements

- [ ] **Beat Selection Response**: < 100ms from click to graph editor update
- [ ] **Panel Switch Time**: < 50ms for orientation ↔ turns switching
- [ ] **Value Change Response**: < 50ms from adjustment to pictograph update
- [ ] **Keyboard Response**: < 100ms for WASD movement commands

### Quality Standards

- [ ] **Data Integrity**: No data loss during rapid operations
- [ ] **UI Consistency**: All components show same data at all times
- [ ] **Error Handling**: Graceful handling of edge cases
- [ ] **Memory Stability**: No leaks during extended use

## Risk Mitigation

### High-Risk Areas

1. **Data Synchronization**: Multiple UI components showing same data

   - **Mitigation**: Single source of truth via repository pattern
   - **Validation**: Automated sync checking in tests

2. **Performance Degradation**: Real-time updates might be slow

   - **Mitigation**: Efficient update batching and debouncing
   - **Fallback**: Async updates for non-critical components

3. **Legacy Integration**: Complex integration with existing beat frame
   - **Mitigation**: Careful signal/slot design with clear interfaces
   - **Testing**: Extensive integration testing

## Updated Timeline

### Week 1: Core Data Flow (CRITICAL)

- Monday-Tuesday: DataFlowService implementation
- Wednesday-Thursday: Real beat data updates and JSON persistence
- Friday: UI propagation and testing

### Week 2: Hotkey System (HIGH)

- Monday-Tuesday: WASD movement system
- Wednesday: Special key commands (X, Z, C)
- Thursday-Friday: Modifier support and testing

### Week 3: Visual Feedback (HIGH)

- Monday-Tuesday: Arrow highlighting system
- Wednesday: Cursor management and selection indicators
- Thursday-Friday: Polish and responsiveness tuning

### Week 4: Testing & Integration (MEDIUM)

- Monday-Tuesday: Comprehensive test suite
- Wednesday: Integration testing with beat frame
- Thursday: Performance validation
- Friday: User acceptance testing

## Conclusion

This updated roadmap prioritizes the **core value proposition** of the graph editor: seamless beat selection and modification with real-time propagation. By focusing on data flow first, we ensure that users get the immediate, intuitive experience that makes the graph editor powerful.

The key insight is that visual polish and advanced features are secondary to the basic workflow of "select beat → modify values → see changes everywhere". Once this core loop works perfectly, the graph editor becomes immediately valuable to users.

# Graph Editor Implementation Guide - Specific Code Changes

## Phase 1: Core Data Flow (Week 1) - CRITICAL

### 1.1 Fix GraphEditorService Data Persistence

**File:** `src/desktop/modern/src/application/services/graph_editor_service.py`

**REPLACE** the placeholder implementations with real data operations:

```python
# CURRENT (lines 89-95) - REPLACE THIS:
def apply_turn_adjustment(self, arrow_color: str, turn_value: float) -> bool:
    if self.ui_state_service:
        adjustment_key = f"turn_adjustment_{arrow_color}_{self._selected_arrow_id}"
        self.ui_state_service.set_setting(adjustment_key, turn_value)
    return True

# WITH THIS:
def apply_turn_adjustment(self, arrow_color: str, turn_value: float) -> bool:
    if not self._selected_beat:
        return False

    # Update actual beat data
    updated = False
    if arrow_color == "blue" and hasattr(self._selected_beat, 'blue_motion') and self._selected_beat.blue_motion:
        self._selected_beat.blue_motion.turns = turn_value
        updated = True
    elif arrow_color == "red" and hasattr(self._selected_beat, 'red_motion') and self._selected_beat.red_motion:
        self._selected_beat.red_motion.turns = turn_value
        updated = True

    if updated:
        # Persist changes (connect to existing persistence layer)
        self._persist_beat_changes(self._selected_beat)

        # Notify UI components of changes
        self._notify_beat_changed(self._selected_beat)

    return updated

# ADD these new methods:
def _persist_beat_changes(self, beat_data: BeatData) -> None:
    """Persist beat changes to JSON repository"""
    # TODO: Connect to existing beat persistence mechanism
    # This should trigger JSON file updates and sequence state changes
    pass

def _notify_beat_changed(self, beat_data: BeatData) -> None:
    """Notify all UI components that beat data has changed"""
    # TODO: Implement signal emission for UI synchronization
    pass
```

### 1.2 Create Data Flow Bridge Service

**File:** `src/desktop/modern/src/application/services/graph_editor_data_flow_service.py` (NEW)

```python
from typing import Optional
from PyQt6.QtCore import QObject, pyqtSignal
from domain.models.core_models import BeatData, SequenceData

class GraphEditorDataFlowService(QObject):
    """Bridges graph editor changes to beat frame and pictograph updates"""

    # Signals for real-time UI updates
    beat_data_updated = pyqtSignal(BeatData, int)  # beat_data, beat_index
    pictograph_refresh_needed = pyqtSignal(BeatData)
    beat_frame_update_needed = pyqtSignal(BeatData, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_sequence: Optional[SequenceData] = None
        self._current_beat_index: Optional[int] = None

    def set_context(self, sequence: SequenceData, beat_index: int):
        """Set current sequence and beat context"""
        self._current_sequence = sequence
        self._current_beat_index = beat_index

    def process_turn_change(self, beat_data: BeatData, arrow_color: str, new_turns: float) -> BeatData:
        """Process turn change and trigger all necessary updates"""
        # 1. Apply the change to beat data
        if arrow_color == "blue" and beat_data.blue_motion:
            beat_data.blue_motion.turns = new_turns
        elif arrow_color == "red" and beat_data.red_motion:
            beat_data.red_motion.turns = new_turns

        # 2. Update sequence if we have context
        if self._current_sequence and self._current_beat_index is not None:
            self._current_sequence.beats[self._current_beat_index] = beat_data

        # 3. Emit signals for UI updates
        self.beat_data_updated.emit(beat_data, self._current_beat_index or 0)
        self.pictograph_refresh_needed.emit(beat_data)
        self.beat_frame_update_needed.emit(beat_data, self._current_beat_index or 0)

        return beat_data

    def process_orientation_change(self, beat_data: BeatData, arrow_color: str, new_orientation: str) -> BeatData:
        """Process orientation change and trigger all necessary updates"""
        # Similar structure to process_turn_change
        # TODO: Implement orientation update logic
        pass

    def determine_panel_mode(self, beat_data: Optional[BeatData]) -> str:
        """Determine whether to show orientation picker or turns controls"""
        if not beat_data:
            return "orientation"

        # Check if this is start position
        is_start = (
            getattr(beat_data, 'is_start_position', False) or
            getattr(beat_data, 'beat_number', 1) == 0 or
            getattr(beat_data, 'sequence_position', 1) == 0
        )

        return "orientation" if is_start else "turns"
```

### 1.3 Connect GraphEditor to Data Flow Service

**File:** `src/desktop/modern/src/presentation/components/workbench/graph_editor/graph_editor.py`

**ADD** data flow service integration to the `__init__` method (around line 40):

```python
def __init__(
    self,
    graph_service: IGraphEditorService,
    parent: Optional["SequenceWorkbench"] = None,
):
    super().__init__(parent)

    self._graph_service = graph_service
    self._parent_workbench = parent

    # ADD: Data flow service for real-time updates
    self._data_flow_service = GraphEditorDataFlowService(self)
    self._connect_data_flow_signals()

    # ... existing initialization code ...

# ADD this new method:
def _connect_data_flow_signals(self):
    """Connect data flow service signals to UI updates"""
    self._data_flow_service.beat_data_updated.connect(self._on_beat_data_updated)
    self._data_flow_service.pictograph_refresh_needed.connect(self._on_pictograph_refresh_needed)

def _on_beat_data_updated(self, beat_data: BeatData, beat_index: int):
    """Handle beat data updates from data flow service"""
    # Update our internal state
    self._selected_beat = beat_data
    self._selected_beat_index = beat_index

    # Update all UI components
    if self._pictograph_container:
        self._pictograph_container.set_beat(beat_data)

    if self._left_adjustment_panel:
        self._left_adjustment_panel.set_beat(beat_data)
    if self._right_adjustment_panel:
        self._right_adjustment_panel.set_beat(beat_data)

def _on_pictograph_refresh_needed(self, beat_data: BeatData):
    """Handle pictograph refresh requests"""
    if self._pictograph_container:
        self._pictograph_container.refresh_display(beat_data)
```

### 1.4 Enhance AdjustmentPanel Panel Switching Logic

**File:** `src/desktop/modern/src/presentation/components/workbench/graph_editor/adjustment_panel.py`

**REPLACE** the `set_beat` method (around line 180) with enhanced logic:

```python
def set_beat(self, beat_data: Optional[BeatData]):
    """Enhanced panel switching with perfect beat type detection"""
    self._current_beat = beat_data

    # Determine panel mode using data flow service logic
    panel_mode = self._determine_panel_mode(beat_data)

    if panel_mode == "orientation":
        self._stacked_widget.setCurrentIndex(0)  # Show orientation picker
        self._update_orientation_picker(beat_data)
        print(f"📍 Showing orientation picker for {self._arrow_color} motion")
    else:
        self._stacked_widget.setCurrentIndex(1)  # Show turn controls
        self._update_turn_controls(beat_data)
        print(f"🔄 Showing turn controls for {self._arrow_color} motion")

def _determine_panel_mode(self, beat_data: Optional[BeatData]) -> str:
    """Determine whether to show orientation picker or turns controls"""
    if not beat_data:
        return "orientation"

    # Multiple ways to detect start position for robustness
    is_start_position = (
        getattr(beat_data, 'is_start_position', False) or
        getattr(beat_data, 'beat_number', 1) == 0 or
        getattr(beat_data, 'sequence_position', 1) == 0 or
        str(getattr(beat_data, 'beat_number', '1')).lower() in ['start', '0', 'start_pos']
    )

    return "orientation" if is_start_position else "turns"

# ENHANCE the _apply_turn method (around line 175) to use data flow:
def _apply_turn(self, arrow_color: str, turn_value: float):
    """Apply turn value using data flow service for proper propagation"""
    if not self._current_beat:
        return

    # Use graph editor's data flow service if available
    if hasattr(self._graph_editor, '_data_flow_service'):
        updated_beat = self._graph_editor._data_flow_service.process_turn_change(
            self._current_beat, arrow_color, turn_value
        )
        self._current_beat = updated_beat
    else:
        # Fallback to direct service call
        if hasattr(self._graph_editor, "_graph_service"):
            success = self._graph_editor._graph_service.apply_turn_adjustment(
                arrow_color, turn_value
            )
            if success:
                self.turn_applied.emit(arrow_color, turn_value)
                if self._current_beat:
                    self.beat_modified.emit(self._current_beat)
```

### 1.5 Connect to Beat Frame Updates

**File:** `src/desktop/modern/src/presentation/components/workbench/workbench.py`

**ADD** graph editor to beat frame connection (find the workbench initialization):

```python
def _setup_components(self):
    # ... existing component setup ...

    # ADD: Connect graph editor data flow to beat frame updates
    if hasattr(self.graph_editor, '_data_flow_service'):
        self.graph_editor._data_flow_service.beat_frame_update_needed.connect(
            self._on_graph_editor_beat_changed
        )

def _on_graph_editor_beat_changed(self, beat_data: BeatData, beat_index: int):
    """Handle beat changes from graph editor and update beat frame"""
    if hasattr(self, 'beat_frame') and self.beat_frame:
        # Update the specific beat in beat frame
        self.beat_frame.update_beat_at_index(beat_index, beat_data)

        # Refresh beat frame display
        self.beat_frame.refresh_display()
```

## Phase 2: Hotkey System (Week 2) - HIGH PRIORITY

### 2.1 Implement Real Hotkey Service

**File:** `src/desktop/modern/src/application/services/graph_editor_hotkey_service.py`

**REPLACE** the entire placeholder with:

```python
from typing import Optional, TYPE_CHECKING
from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtGui import QKeyEvent

if TYPE_CHECKING:
    from core.interfaces.workbench_services import IGraphEditorService

class GraphEditorHotkeyService(QObject):
    """Real hotkey service implementation for graph editor"""

    # Signals for hotkey actions
    arrow_moved = pyqtSignal(str, int, int)  # arrow_id, delta_x, delta_y
    rotation_override_requested = pyqtSignal(str)  # arrow_id
    special_placement_removal_requested = pyqtSignal(str)  # arrow_id
    prop_placement_override_requested = pyqtSignal(str)  # arrow_id

    def __init__(self, graph_service: "IGraphEditorService", parent=None):
        super().__init__(parent)
        self.graph_service = graph_service

        # Movement increment settings (from legacy)
        self.base_increment = 5
        self.shift_increment = 20
        self.ctrl_shift_increment = 200

    def handle_key_event(self, event: QKeyEvent) -> bool:
        """Handle keyboard events and return True if handled"""
        key = event.key()
        modifiers = event.modifiers()

        # Check if we have a selected arrow
        selected_arrow = self.graph_service.get_selected_arrow() if hasattr(self.graph_service, 'get_selected_arrow') else None
        if not selected_arrow:
            return False

        # WASD movement
        if key in [Qt.Key.Key_W, Qt.Key.Key_A, Qt.Key.Key_S, Qt.Key.Key_D]:
            return self._handle_arrow_movement(key, modifiers, selected_arrow)

        # Special commands
        elif key == Qt.Key.Key_X:
            self.rotation_override_requested.emit(selected_arrow)
            return True
        elif key == Qt.Key.Key_Z:
            self.special_placement_removal_requested.emit(selected_arrow)
            return True
        elif key == Qt.Key.Key_C:
            self.prop_placement_override_requested.emit(selected_arrow)
            return True

        return False

    def _handle_arrow_movement(self, key: Qt.Key, modifiers: Qt.KeyboardModifier, arrow_id: str) -> bool:
        """Handle WASD arrow movement with modifier support"""
        # Calculate increment based on modifiers
        increment = self.base_increment
        if modifiers & Qt.KeyboardModifier.ShiftModifier:
            if modifiers & Qt.KeyboardModifier.ControlModifier:
                increment = self.ctrl_shift_increment  # Shift+Ctrl = 200px
            else:
                increment = self.shift_increment  # Shift = 20px

        # Calculate movement delta
        delta_x, delta_y = self._get_movement_delta(key, increment)

        if delta_x != 0 or delta_y != 0:
            self.arrow_moved.emit(arrow_id, delta_x, delta_y)
            return True

        return False

    def _get_movement_delta(self, key: Qt.Key, increment: int) -> tuple[int, int]:
        """Convert key to movement delta"""
        movement_map = {
            Qt.Key.Key_W: (0, -increment),  # Up
            Qt.Key.Key_A: (-increment, 0),  # Left
            Qt.Key.Key_S: (0, increment),   # Down
            Qt.Key.Key_D: (increment, 0),   # Right
        }
        return movement_map.get(key, (0, 0))
```

### 2.2 Connect Hotkey Service to Graph Editor

**File:** `src/desktop/modern/src/presentation/components/workbench/graph_editor/graph_editor.py`

**ADD** hotkey service integration to `__init__` (around line 45):

```python
def __init__(
    self,
    graph_service: IGraphEditorService,
    parent: Optional["SequenceWorkbench"] = None,
):
    # ... existing initialization ...

    # ADD: Hotkey service
    self._hotkey_service = GraphEditorHotkeyService(graph_service, self)
    self._connect_hotkey_signals()

def _connect_hotkey_signals(self):
    """Connect hotkey service signals"""
    self._hotkey_service.arrow_moved.connect(self._on_arrow_moved)
    self._hotkey_service.rotation_override_requested.connect(self._on_rotation_override)
    self._hotkey_service.special_placement_removal_requested.connect(self._on_special_placement_removal)
    self._hotkey_service.prop_placement_override_requested.connect(self._on_prop_placement_override)

def _on_arrow_moved(self, arrow_id: str, delta_x: int, delta_y: int):
    """Handle arrow movement from hotkeys"""
    print(f"🎯 Moving arrow {arrow_id} by ({delta_x}, {delta_y})")
    # TODO: Implement arrow position adjustment
    # This should update the arrow's position in the pictograph

def _on_rotation_override(self, arrow_id: str):
    """Handle rotation override (X key)"""
    print(f"🔄 Rotation override for arrow {arrow_id}")
    # TODO: Implement rotation override logic

def _on_special_placement_removal(self, arrow_id: str):
    """Handle special placement removal (Z key)"""
    print(f"❌ Removing special placement for arrow {arrow_id}")
    # TODO: Implement special placement removal

def _on_prop_placement_override(self, arrow_id: str):
    """Handle prop placement override (C key)"""
    print(f"🎭 Prop placement override for arrow {arrow_id}")
    # TODO: Implement prop placement override

# ENHANCE the keyPressEvent method (around line 300):
def keyPressEvent(self, event: QKeyEvent):
    """Handle key press events for hotkeys."""
    if not self._is_visible:
        super().keyPressEvent(event)
        return

    # Try hotkey service first
    if self._hotkey_service.handle_key_event(event):
        return  # Handled by hotkey service

    # Pass to parent if not handled
    super().keyPressEvent(event)
```

## Phase 3: Visual Feedback System (Week 3) - HIGH PRIORITY

### 3.1 Enhance Pictograph Container with Arrow Selection

**File:** `src/desktop/modern/src/presentation/components/workbench/graph_editor/pictograph_container.py`

**ADD** visual feedback methods (around line 100):

```python
class GraphEditorPictographContainer(QWidget):
    # ... existing code ...

    def __init__(self, parent):
        # ... existing initialization ...
        self._selected_arrow_items = {}  # Track selected arrow visual items
        self._selection_highlight_color = "#FFD700"  # Gold border color

    def set_selected_arrow(self, arrow_id: str):
        """Set selected arrow and update visual feedback"""
        # Clear previous selection
        self._clear_arrow_selection()

        # Set new selection
        self._selected_arrow_id = arrow_id
        self._apply_arrow_selection_visual(arrow_id)

        self.arrow_selected.emit(arrow_id)

    def _clear_arrow_selection(self):
        """Clear all arrow selection visual feedback"""
        if hasattr(self._pictograph_view, '_scene') and self._pictograph_view._scene:
            for item in self._pictograph_view._scene.items():
                if hasattr(item, 'setSelected'):
                    item.setSelected(False)
                if hasattr(item, 'clear_selection_highlight'):
                    item.clear_selection_highlight()

    def _apply_arrow_selection_visual(self, arrow_id: str):
        """Apply visual feedback for selected arrow"""
        if not hasattr(self._pictograph_view, '_scene') or not self._pictograph_view._scene:
            return

        for item in self._pictograph_view._scene.items():
            if hasattr(item, 'arrow_color') and item.arrow_color == arrow_id:
                # Add gold border highlighting
                if hasattr(item, 'add_selection_highlight'):
                    item.add_selection_highlight(self._selection_highlight_color)
                elif hasattr(item, 'setSelected'):
                    item.setSelected(True)
                break

    def refresh_display(self, beat_data: BeatData):
        """Refresh pictograph display with new beat data"""
        self.set_beat(beat_data)

        # Maintain selection if we had one
        if self._selected_arrow_id:
            self._apply_arrow_selection_visual(self._selected_arrow_id)
```

### 3.2 Add Arrow Highlighting to Pictograph Scene

**File:** Look for existing pictograph scene files and ADD selection highlighting capability:

```python
# This will likely need to be added to arrow rendering components
# The exact file depends on your pictograph scene architecture

class ArrowGraphicsItem(QGraphicsItem):  # Or whatever your arrow item class is
    def __init__(self, arrow_data, color):
        super().__init__()
        self.arrow_color = color
        self._selection_highlight = False
        self._highlight_color = "#FFD700"
        self._highlight_width = 3

    def add_selection_highlight(self, color: str = "#FFD700"):
        """Add selection highlighting to this arrow"""
        self._selection_highlight = True
        self._highlight_color = color
        self.update()  # Trigger repaint

    def clear_selection_highlight(self):
        """Clear selection highlighting"""
        self._selection_highlight = False
        self.update()  # Trigger repaint

    def paint(self, painter, option, widget):
        # ... existing arrow painting code ...

        # ADD: Draw selection highlight if selected
        if self._selection_highlight:
            pen = QPen(QColor(self._highlight_color))
            pen.setWidth(self._highlight_width)
            painter.setPen(pen)
            painter.drawRect(self.boundingRect().adjusted(-2, -2, 2, 2))
```

## Phase 4: Integration and Testing (Week 4) - MEDIUM PRIORITY

### 4.1 Create Integration Test Suite

**File:** `src/desktop/modern/tests/integration/test_graph_editor_data_flow.py` (NEW)

```python
import pytest
from unittest.mock import Mock, patch
from domain.models.core_models import BeatData, MotionData
from presentation.components.workbench.graph_editor.graph_editor import GraphEditor

class TestGraphEditorDataFlow:
    """Test the complete data flow from beat selection to UI updates"""

    def test_beat_selection_triggers_correct_panel(self, qtbot):
        """Test that selecting start position shows orientation, beats show turns"""
        # Setup
        graph_editor = self._create_graph_editor(qtbot)

        # Test start position
        start_beat = self._create_start_position_beat()
        graph_editor.set_selected_beat(start_beat, 0)

        # Verify orientation picker is shown
        assert graph_editor._left_adjustment_panel._stacked_widget.currentIndex() == 0
        assert graph_editor._right_adjustment_panel._stacked_widget.currentIndex() == 0

        # Test regular beat
        regular_beat = self._create_regular_beat()
        graph_editor.set_selected_beat(regular_beat, 1)

        # Verify turns controls are shown
        assert graph_editor._left_adjustment_panel._stacked_widget.currentIndex() == 1
        assert graph_editor._right_adjustment_panel._stacked_widget.currentIndex() == 1

    def test_turn_adjustment_propagates_to_beat_data(self, qtbot):
        """Test that turn changes update actual beat data"""
        # Setup
        graph_editor = self._create_graph_editor(qtbot)
        beat_data = self._create_regular_beat()
        graph_editor.set_selected_beat(beat_data, 1)

        # Apply turn change
        initial_turns = beat_data.blue_motion.turns
        graph_editor._right_adjustment_panel._adjust_turn(1.0)

        # Verify beat data was updated
        assert beat_data.blue_motion.turns == initial_turns + 1.0

    def test_hotkey_movement_works(self, qtbot):
        """Test that WASD hotkeys trigger arrow movement"""
        # Setup
        graph_editor = self._create_graph_editor(qtbot)
        graph_editor.set_selected_beat(self._create_regular_beat(), 1)

        # Simulate W key press
        key_event = self._create_key_event(Qt.Key.Key_W)

        with patch.object(graph_editor._hotkey_service, 'handle_key_event') as mock_handler:
            graph_editor.keyPressEvent(key_event)
            mock_handler.assert_called_once_with(key_event)

    def _create_graph_editor(self, qtbot):
        """Helper to create graph editor for testing"""
        # TODO: Implement based on your DI container setup
        pass

    def _create_start_position_beat(self) -> BeatData:
        """Helper to create start position beat data"""
        # TODO: Create with is_start_position = True
        pass

    def _create_regular_beat(self) -> BeatData:
        """Helper to create regular beat data"""
        # TODO: Create with blue_motion and red_motion
        pass
```

### 4.2 Add Performance Validation

**File:** `src/desktop/modern/tests/performance/test_graph_editor_performance.py` (NEW)

```python
import time
import pytest
from PyQt6.QtCore import Qt
from PyQt6.QtTest import QTest

class TestGraphEditorPerformance:
    """Validate performance requirements"""

    def test_beat_selection_response_time(self, qtbot):
        """Beat selection must respond < 100ms"""
        graph_editor = self._create_graph_editor(qtbot)
        beat_data = self._create_test_beat()

        start_time = time.time()
        graph_editor.set_selected_beat(beat_data, 1)
        QTest.qWait(10)  # Allow Qt event processing
        response_time = time.time() - start_time

        assert response_time < 0.1, f"Beat selection took {response_time:.3f}s, must be < 0.1s"

    def test_turn_adjustment_response_time(self, qtbot):
        """Turn adjustments must respond < 50ms"""
        graph_editor = self._create_graph_editor(qtbot)
        graph_editor.set_selected_beat(self._create_test_beat(), 1)

        adjustment_panel = graph_editor._right_adjustment_panel

        start_time = time.time()
        adjustment_panel._adjust_turn(0.5)
        response_time = time.time() - start_time

        assert response_time < 0.05, f"Turn adjustment took {response_time:.3f}s, must be < 0.05s"

    def test_hotkey_response_time(self, qtbot):
        """Hotkey processing must respond < 100ms"""
        graph_editor = self._create_graph_editor(qtbot)
        key_event = self._create_key_event(Qt.Key.Key_W)

        start_time = time.time()
        handled = graph_editor._hotkey_service.handle_key_event(key_event)
        response_time = time.time() - start_time

        assert response_time < 0.1, f"Hotkey processing took {response_time:.3f}s, must be < 0.1s"
        assert handled, "Hotkey should be handled"
```

## Key Integration Points Summary

### Files to Modify:

1. **`graph_editor_service.py`** - Fix data persistence
2. **`graph_editor.py`** - Add data flow service and hotkey integration
3. **`adjustment_panel.py`** - Enhance panel switching logic
4. **`pictograph_container.py`** - Add arrow selection visual feedback
5. **`workbench.py`** - Connect graph editor to beat frame updates

### New Files to Create:

1. **`graph_editor_data_flow_service.py`** - Central data flow coordination
2. **`test_graph_editor_data_flow.py`** - Integration tests
3. **`test_graph_editor_performance.py`** - Performance validation

### Critical Integration Patterns:

```python
# Beat Selection → Panel Switching
beat_data → determine_panel_mode() → show correct controls

# Data Changes → Propagation
user_input → update_beat_data() → persist_to_json() → notify_all_ui()

# Hotkey Input → Actions
key_press → hotkey_service → arrow_movement/commands → ui_updates

# Visual Feedback → Selection
arrow_click → set_selected_arrow() → apply_highlighting → update_cursor
```

This guide provides the exact code structure and integration points needed while leaving implementation details for the AI agent to fill in based on your existing codebase patterns.
