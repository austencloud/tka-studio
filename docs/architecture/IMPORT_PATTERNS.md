# TKA Modern Desktop Import Patterns

## Overview

This document defines the **canonical import patterns** for the TKA Modern Desktop application. These patterns ensure consistency, maintainability, and proper architecture layer separation.

## Core Principle: Relative Imports

The TKA Modern Desktop application uses **relative imports** throughout the codebase to maintain a self-contained structure and support the established clean architecture.

## Correct Import Patterns

### Domain Layer
```python
# ✅ CORRECT - Relative imports within modern directory
from domain.models.core_models import BeatData, SequenceData, MotionData
from domain.models.pictograph_models import PictographData, ArrowData
from domain.models.positioning_models import ArrowPositionResult
from domain.models.settings_models import SettingsData
```

### Application Layer
```python
# ✅ CORRECT - Relative imports within modern directory
from application.services.core.sequence_management_service import SequenceManagementService
from application.services.positioning.arrow_positioning_service import ArrowPositioningService
from application.services.data.pictograph_data_service import PictographDataService
```

### Presentation Layer
```python
# ✅ CORRECT - Relative imports within modern directory
from presentation.components.workbench.workbench import ModernSequenceWorkbench
from presentation.components.option_picker.option_picker import OptionPicker
from presentation.components.pictograph.pictograph_scene import PictographScene
```

### Core Layer
```python
# ✅ CORRECT - Relative imports within modern directory
from core.dependency_injection.di_container import DIContainer
from core.interfaces.core_services import ISequenceManagementService
from core.events.event_bus import EventBus
```

### Infrastructure Layer
```python
# ✅ CORRECT - Relative imports within modern directory
from infrastructure.api.main import app
from infrastructure.repositories.sequence_repository import SequenceRepository
```

## ANTI-PATTERNS - DO NOT USE

### ❌ Absolute Imports with Full Paths
```python
# ❌ WRONG - These patterns violate TKA's relative import convention
from desktop.modern.src.domain.models.core_models import BeatData
from src.desktop.modern.src.domain.models.core_models import BeatData
from desktop.modern.src.application.services.core.sequence_management_service import SequenceManagementService
```

### ❌ Mixed Import Patterns
```python
# ❌ WRONG - Inconsistent import patterns cause enum object identity issues
from domain.models.core_models import MotionType  # Relative
from desktop.modern.src.domain.models.core_models import MotionType  # Absolute
```

## Architecture Layer Rules

### 1. Domain Layer (Pure Business Logic)
- **Imports**: Only other domain models and Python standard library
- **No Dependencies**: Cannot import from application, presentation, core, or infrastructure layers
- **Pattern**: `from domain.models.{module} import {Class}`

### 2. Application Layer (Business Services)
- **Imports**: Domain models, core interfaces, other application services
- **Pattern**: `from application.services.{category}.{service} import {Class}`
- **Dependencies**: `from domain.models.{module}`, `from core.interfaces.{interface}`

### 3. Presentation Layer (UI Components)
- **Imports**: Application services, domain models (read-only), core interfaces
- **Pattern**: `from presentation.components.{category}.{component} import {Class}`
- **Dependencies**: `from application.services.{service}`, `from domain.models.{module}`

### 4. Core Layer (Cross-cutting Concerns)
- **Imports**: Domain models for interface definitions, Python standard library
- **Pattern**: `from core.{category}.{module} import {Class}`
- **Dependencies**: Minimal - primarily domain models for type hints

### 5. Infrastructure Layer (External Concerns)
- **Imports**: Domain models, application services, core interfaces
- **Pattern**: `from infrastructure.{category}.{module} import {Class}`
- **Dependencies**: All layers as needed for external integration

## Testing Import Patterns

### Test Files
```python
# ✅ CORRECT - Tests use same relative import patterns
from domain.models.core_models import BeatData, SequenceData
from application.services.core.sequence_management_service import SequenceManagementService
from fixtures.domain_fixtures import create_test_sequence
```

## Path Setup for Tests

Tests require the `src` directory to be added to the Python path:

```python
# In test files or test runners
import sys
from pathlib import Path

# Add src directory to path for relative imports
modern_src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(modern_src_path))
```

## Validation

To verify import patterns are correct, run:

```bash
# From src/desktop/modern directory
python -c "import sys; sys.path.insert(0, 'src'); from domain.models.core_models import BeatData; print('✅ Imports work correctly')"
```

## Benefits of This Pattern

1. **Self-Contained**: Modern directory is completely self-contained
2. **Clean Architecture**: Clear layer boundaries and dependencies
3. **IDE Support**: Better autocomplete and navigation
4. **Consistency**: Single import pattern throughout codebase
5. **Maintainability**: Easy to refactor and reorganize
6. **Testing**: Simplified test setup and execution

## Enforcement

- Use the `scripts/fix_relative_imports.py` script to fix any absolute import patterns
- The `import_analysis_service.py` can detect and report import pattern violations
- All new code must follow these patterns from the start

---

**Remember**: Consistency is key. Always use relative imports within the modern directory to maintain TKA's clean architecture principles.
