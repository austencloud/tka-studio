# Event Bus Removal Plan

## 🎯 **Objective**

Remove the event bus system entirely and ensure Qt signal coordinators handle all inter-component communication.

## 📋 **Phase 1: Remove Event Bus Core Files**

### Files to Delete:

- `src/desktop/modern/core/events/event_bus.py`
- `src/desktop/modern/core/events/domain_events.py`
- `src/desktop/modern/core/events/__init__.py`
- `src/desktop/modern/core/events/` (entire directory)

### Test Files to Delete:

- `src/desktop/modern/tests/specification/core/test_event_bus.py`
- `src/desktop/modern/tests/specification/core/test_event_bus_contracts.py`
- `tests/test_event_bus_core.py`
- `tests/test_performance.py` (event bus sections)

## 📋 **Phase 2: Remove Event Bus Registration**

### Service Registration Files to Update:

- `src/shared/application/services/core/registrars/event_system_registrar.py` (DELETE)
- `src/desktop/modern/core/service_locator.py` (remove event bus code)
- Service registration managers (remove event bus registration)

## 📋 **Phase 3: Update Services Using Event Bus**

### Replace Event Bus with Qt Signals:

1. **UIStateManager** (`src/shared/application/services/ui/ui_state_manager.py`)
   - Remove `get_event_bus()` import
   - Remove `self._event_bus = get_event_bus()`
   - Replace `self._event_bus.publish(event)` with Qt signals

2. **Component Visibility Manager**
   - Replace event publishing with signals

3. **Start Position Picker**
   - Replace event publishing with signals

4. **Other Services**
   - Update all services that import/use event bus

## 📋 **Phase 4: Clean Up Imports**

### Remove Event Bus Imports:

- Remove `from desktop.modern.core.events import ...`
- Remove `EVENT_BUS_AVAILABLE` flags
- Remove conditional event bus code

## 📋 **Phase 5: Extend Qt Signal Coordinators**

### Enhance Existing Coordinators:

- Add signals for UI state changes
- Add signals for component visibility
- Add signals for start position selection
- Ensure all event bus use cases are covered

## ✅ **Success Criteria**

- [ ] No event bus imports anywhere
- [ ] All services use Qt signals only
- [ ] Application runs without errors
- [ ] All functionality preserved
- [ ] Cleaner, simpler architecture
