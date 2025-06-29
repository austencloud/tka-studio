# TKA AI Agent Development Guide

## 🎯 Mission: Enable AI Agents to Test TKA User Workflows

This guide enables AI agents to test complete user workflows in TKA using the existing sophisticated architecture. The system provides simple interfaces for AI agents while leveraging TKA's advanced command pattern, event system, and immutable domain models.

## 🏗️ TKA Architecture Overview

### Core Principles
- **Immutable Domain Models**: `BeatData`, `SequenceData`, `PictographData` are frozen dataclasses
- **Command Pattern with Undo/Redo**: All operations use command objects with event publishing
- **Event-Driven Architecture**: Services publish events au It's hot out there tomatically for state changes
- **Dependency Injection**: All services resolve through DI container
- **Repository Pattern**: Persistence handled through repositories

### Domain Models (Immutable)
```python
# All domain models are immutable dataclasses
beat = BeatData(letter="A", duration=1.0, blue_motion=motion_data)
sequence = SequenceData(name="Test", beats=[beat])
pictograph = PictographData(grid_data=grid_data, arrows=arrows)

# Updates create new instances
updated_beat = beat.update(duration=2.0)
updated_sequence = sequence.update_beat(1, duration=2.0)
```

### Service Layer with Commands
```python
# Services have sophisticated command patterns built-in
sequence_service = container.resolve(ISequenceManagementService)

# These methods use command pattern with undo/redo automatically
sequence = sequence_service.create_sequence_with_events("Test", 8)
sequence_service.add_beat_with_undo(beat_data, position=0)
sequence_service.undo_last_operation()  # Full undo support!
```

## 🚀 Hack #1: Application Factory (IMPLEMENTED)

### Usage for AI Agents
```python
from core.application.application_factory import ApplicationFactory

# Test mode - fast, in-memory, predictable
container = ApplicationFactory.create_test_app()

# Headless mode - real logic, no UI
container = ApplicationFactory.create_headless_app()

# Get services
sequence_service = container.resolve(ISequenceManagementService)
pictograph_service = container.resolve(IPictographManagementService)
```

### Command Line Integration
```bash
python main.py --test      # AI agent testing mode
python main.py --headless  # Server processing mode
python main.py            # Production desktop mode
```

## 🎮 Hack #2: AI Agent Workflow Testing

### Simple Interface for AI Agents
```python
from core.commands.ai_agent_testing import TKAWorkflowTester

# One-line setup for AI agents
tester = TKAWorkflowTester()

# Test complete user workflows
result = tester.test_sequence_creation_workflow("My Sequence", 8)
result = tester.test_beat_addition_workflow(sequence_data, beat_data)
result = tester.test_complete_user_workflow()

# All results have consistent format:
assert result['success'] == True
assert result['execution_time'] < 1.0  # Fast for AI testing
assert len(result['errors']) == 0
```

### Advanced AI Agent Usage
```python
# For sophisticated AI testing
tester = TKAWorkflowTester(use_real_events=True, enable_undo=True)

# Test with undo/redo
result = tester.test_undo_redo_workflow()
assert result['undo_steps'] == 3
assert result['redo_steps'] == 2

# Test event publishing
result = tester.test_event_driven_workflow()
assert result['events_published'] >= 5
```

## 📋 AI Agent Testing Patterns

### Pattern 1: Simple CRUD Testing