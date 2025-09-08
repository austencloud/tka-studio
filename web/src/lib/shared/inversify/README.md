# Modular Inversify Container Architecture

## Overview

This document describes the new modular architecture for the TKA Inversify container, replacing the massive single-file container with a maintainable, domain-driven module system.

## Architecture Pattern

We follow the **Container Module Pattern** recommended by the Inversify team, which provides:

- **Domain separation**: Each module handles bindings for a specific domain
- **Maintainability**: Smaller, focused files that are easier to understand and modify
- **Testability**: Each module can be tested in isolation
- **Lazy loading**: Modules can be loaded conditionally if needed
- **Error isolation**: Issues in one module don't affect others

## Module Structure

```
src/lib/shared/inversify/
├── container.ts              # Main container that loads all modules
├── types.ts                  # Centralized service type definitions
├── modules/
│   ├── index.ts             # Module exports
│   ├── core.module.ts       # Application core services
│   ├── data.module.ts       # Data processing services
│   ├── pictograph.module.ts # Pictograph rendering services
│   ├── animator.module.ts   # Animation services
│   ├── browse.module.ts     # Browse gallery services
│   ├── build.module.ts      # Build workbench services
│   ├── export.module.ts     # Export services
│   ├── learn.module.ts      # Learning/codex services
│   ├── word-card.module.ts  # Word card services
│   └── write.module.ts      # Write tab services
```

## Module Responsibilities

### Core Module (`core.module.ts`)
- Application initialization services
- Device detection
- Foundation services (file download, storage, SEO)
- Settings management
- Resource tracking

### Data Module (`data.module.ts`)
- CSV loading and parsing
- Data transformation
- Enum mapping
- Background services

### Pictograph Module (`pictograph.module.ts`)
- Arrow positioning and rendering
- Grid services
- Prop coordination
- Query handlers
- Key generators and processors

### Animator Module (`animator.module.ts`)
- Animation control and state
- Motion parameter services
- Sequence animation orchestration
- SVG rendering utilities

### Browse Module (`browse.module.ts`)
- Gallery services
- Navigation and favorites
- State persistence
- Thumbnail management

### Build Module (`build.module.ts`)
- Option picker services
- Start position management
- Generation services
- Workbench coordination
- Sequence operations

### Export Module (`export.module.ts`)
- Image export services
- Canvas management
- Text rendering
- File format conversion
- Layout calculation

### Learn Module (`learn.module.ts`)
- Codex services
- Quiz management
- Letter mapping

### Word Card Module (`word-card.module.ts`)
- Word card generation
- Batch processing
- Image conversion
- Metadata overlay

### Write Module (`write.module.ts`)
- Act services
- Music player

## Best Practices Implemented

### 1. **Async Module Loading**
All modules use async loading pattern to support future enhancements like lazy loading or conditional module loading.

### 2. **Proper TypeScript Imports**
Using type-only imports where appropriate to comply with `verbatimModuleSyntax`.

### 3. **Centralized Type Definitions**
All service types remain in the central `types.ts` file for consistency.

### 4. **Error Handling**
The main container includes comprehensive error handling during module loading.

### 5. **Scope Management**
Singleton scopes are properly maintained (e.g., `StartPositionService`).

## Usage

### Basic Usage
```typescript
import { container, resolve, TYPES } from "@/lib/shared/inversify/container";

// Get a service
const sequenceService = resolve<ISequenceService>(TYPES.ISequenceService);

// Or use container directly
const galleryService = container.get<IGalleryService>(TYPES.IGalleryService);
```

### Testing Individual Modules
```typescript
import { Container } from "inversify";
import { coreModule } from "@/lib/shared/inversify/modules/core.module";

describe("Core Module", () => {
  let testContainer: Container;

  beforeEach(async () => {
    testContainer = new Container();
    await testContainer.load(coreModule);
  });

  it("should provide settings service", () => {
    const settingsService = testContainer.get(TYPES.ISettingsService);
    expect(settingsService).toBeDefined();
  });
});
```

### Conditional Module Loading
```typescript
// Load only specific modules for testing or specific environments
const container = new Container();
await container.load(coreModule, dataModule);
```

## Migration Benefits

### Before (443-line monolithic container)
- ❌ Single massive file hard to navigate
- ❌ All services loaded together
- ❌ Difficult to test individual domains
- ❌ High coupling between unrelated services
- ❌ Merge conflicts when multiple developers work on DI

### After (modular architecture)
- ✅ Small, focused modules (10-50 lines each)
- ✅ Clear domain separation
- ✅ Independent testing possible
- ✅ Reduced coupling
- ✅ Fewer merge conflicts
- ✅ Better code organization
- ✅ Future-ready for lazy loading

## Future Enhancements

### Lazy Loading
```typescript
// Future: Load modules only when needed
const loadBrowseModule = async () => {
  if (!container.isBound(TYPES.IGalleryService)) {
    const { browseModule } = await import("./modules/browse.module");
    await container.load(browseModule);
  }
};
```

### Environment-Specific Modules
```typescript
// Load different modules for different environments
if (process.env.NODE_ENV === 'development') {
  await container.load(debugModule);
}
```

### Feature Flags
```typescript
// Conditional loading based on feature flags
if (featureFlags.enableWordCards) {
  await container.load(wordCardModule);
}
```

## Maintenance Guidelines

1. **Keep modules focused**: Each module should handle one domain
2. **Avoid cross-module dependencies**: Services should not directly depend on services from other modules
3. **Use interfaces**: Always bind to interfaces, not concrete classes
4. **Document module purpose**: Each module should have a clear comment explaining its scope
5. **Test modules independently**: Write tests for each module in isolation
6. **Review module size**: If a module gets too large (>100 lines), consider splitting it

## Backup

The original container is backed up as `container.backup.ts` and can be restored if needed.
