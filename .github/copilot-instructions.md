# TKA Web App - AI Coding Agent Instructions

## Project Context & Vision

**TKA (The Kinetic Alphabet)** is the **modern web incarnation** of a flow arts choreography system with multiple iterations:

- **Desktop App** (`../desktop/`) - Complete feature set, legacy Qt/Python application
- **Legacy Web App** (`legacy_web/`) - Previous web implementation with reference algorithms
- **Modern Web App** (`web/` - this project) - **Final form** using cutting-edge web technologies

This modern web app leverages lessons learned from previous versions while rebuilding with **Svelte 5**, **TypeScript**, and **modern browser APIs** for the ultimate user experience.

## Domain Knowledge - TKA Choreography Concepts

### Core Flow Arts Domain

TKA is a **systematic notation system for flow arts** (staff, hoop, clubc, etc.) that breaks down complex movements into discrete, analyzable components:

- **Pictographs** - Visual representations of movement poses/positions
- **Sequences** - Ordered collections of pictographs forming complete movements
- **Beats** - Individual time units within sequences (extends pictograph with timing)
- **Motions** - Direction and type of movement between positions

### Key Domain Models

- **`PictographData`** - Core movement data with grid positions, arrows, orientations
- **`BeatData`** - Pictograph + timing information + beat metadata
- **`SequenceData`** - Complete movement sequences with multiple beats
- **`MotionData`** - Movement types (static, pro, anti, float, dash)
- **`ArrowPlacementData`** - Precise arrow positioning and calculations

### Grid System & Positioning

- **Grid Locations** - Named positions (Top, Bottom, Center, etc.)
- **Grid Modes** - Diamond vs Box grid layouts
- **Arrow Calculations** - Complex positioning algorithms for visual representation
- **Motion Types** - Different movement patterns with specific rules

### Technical Terminology

- **Props** - Physical objects being manipulated (staff, triad, etc.)
- **Orientations** - Directional states and rotations
- **CAP (Continuous Assembly Patterns)** - Advanced movement constraint system
- **VTG (Vulcan Tech Gospel)** - Specific poi technique methodology

**CRITICAL**: Understanding these domain concepts is essential for working on any TKA feature. The codebase contains complex algorithms for position calculations, arrow placements, and movement validations.

## Architecture Overview

This is a sophisticated Svelte 5 web application for creating and manipulating movement-based pictographs. The codebase follows a **modular architecture** with **dependency injection** and specific **HMR (Hot Module Replacement)** patterns.

## Legacy Reference Points

### Desktop App (`../desktop/`)

- **Complete implementation** of all TKA algorithms and features
- **Source of truth** for business logic, algorithms, and UI patterns
- **Qt/Python architecture** with fully functional sequence generation, editing, and export

### Legacy Web App (`legacy_web/`)

- **Algorithmic references** for complex calculations (positioning, generation, props)
- **Proven patterns** for sequence manipulation and data structures
- **Migration targets** - algorithms ported to modern TypeScript implementation

### Key Migration Patterns

```typescript
// Example: Legacy algorithm port
// From: legacy_web/BetaPropDirectionCalculator.ts
// To: src/lib/shared/pictograph/prop/services/implementations/BetaPropDirectionCalculator.ts

// Maintains exact logic while adapting to modern DI and TypeScript patterns
```

### Cross-App File Access

```typescript
// vite.config.ts enables access to sibling directories
server: {
  fs: {
    allow: [".", "../animator", "../desktop"],
  },
}
```

## Core Technologies

- **Svelte 5** with **runes** (`$state`, `$derived`, `$props`, `$effect`)
- **SvelteKit** for routing and SSR
- **InversifyJS** for dependency injection
- **Dexie.js** for persistent data storage (IndexedDB)
- **Fabric.js** for canvas operations
- **TypeScript** with strict configuration

## Key Architectural Patterns

### 1. Module-First Architecture

The app is organized into domain modules under `src/lib/modules/`:

- `build/` - Sequence construction and editing
- `Explore/` - Sequence browsing and display
- `learn/` - Educational content (PDFs, codex, quizzes)
- `write/` - Act creation and music integration
- `animator/` - Sequence animation
- `word-card/` - Printable sequence cards

### 2. Dependency Injection with InversifyJS

**CRITICAL**: All services use dependency injection. Never instantiate services directly.

```typescript
// ✅ CORRECT - Use container resolution
import { resolve, TYPES } from "$shared";
const service = resolve<IServiceInterface>(TYPES.IServiceInterface);

// ❌ WRONG - Never instantiate directly
const service = new ServiceImplementation();
```

Service types are defined in `src/lib/shared/inversify/types.ts` and modules are loaded in `src/lib/shared/inversify/modules/`.

### 3. Svelte 5 Runes State Management

All reactive state uses Svelte 5 runes pattern with factory functions:

```typescript
// State factory pattern
export function createComponentState() {
  let data = $state<DataType>([]);
  let isLoading = $state(false);
  const derived = $derived(data.length > 0);

  return {
    get data() {
      return data;
    },
    get isLoading() {
      return isLoading;
    },
    get derived() {
      return derived;
    },
    updateData: (newData: DataType[]) => {
      data = newData;
    },
  };
}
```

**State Management Patterns**:

- **Factory Functions**: All state managed through factory functions returning getters/setters
- **Reactive Chains**: Use `$derived` for computed values, `$effect` for side effects
- **State Isolation**: Each component/module manages its own state, avoiding global state pollution
- **HMR Persistence**: State factories designed to survive hot reloads

### 4. HMR-Safe Container Management

The dependency injection container is HMR-safe with global state persistence:

```typescript
// HMR preserves container across reloads
if (import.meta.hot) {
  import.meta.hot.accept(() => {
    // Container restored from global state
  });
}
```

## Import Patterns & Circular Dependency Prevention

### Critical Import Rules

1. **Within modules**: Use relative imports, NEVER barrel exports (`$shared`)
2. **Cross-module**: Use module aliases (`$build`, `$Explore`, etc.)
3. **Services**: Always use DI container resolution
4. **Types only**: Use `import type` for type-only imports

```typescript
// ✅ CORRECT patterns
import { ComponentA } from "./components/ComponentA.svelte"; // Same module
import { ServiceB } from "$build/services"; // Cross-module
import type { DataType } from "$shared"; // Types only
import { resolve, TYPES } from "$shared"; // DI only

// ❌ WRONG - Causes circular dependencies
import { BackgroundSystem } from "$shared"; // From within shared module
```

### Module Aliases (svelte.config.js)

- `$shared` - Shared utilities, services, components
- `$build`, `$Explore`, `$learn`, `$write`, `$animator`, `$wordcard` - Module aliases
- Use these for cross-module imports only

## Development Workflows

### Starting Development

```bash
npm run dev  # Starts Vite dev server with HMR
```

### Running Tests

```bash
npm run test              # All Vitest tests (unit + integration + debug)
npm run test:unit         # Unit tests only
npm run test:integration  # Integration tests only
npm run test:e2e          # Playwright E2E tests
npm run check             # TypeScript checking
```

### Build Process

```bash
npm run build    # SvelteKit build for production
npm run preview  # Preview production build
```

## Debugging & Error Handling

### Comprehensive Debug System

The app includes sophisticated debugging tools for development:

#### HMR Debug Utilities (`src/lib/shared/utils/hmr-debug.ts`)

```typescript
// Available in browser console during development
window.__TKA_HMR_DEBUG__.report(); // Get HMR state report
window.__TKA_HMR_DEBUG__.clear(); // Clear debug logs
window.__TKA_HMR_DEBUG__.debug("Custom message");
```

#### Error Handling Service

```typescript
const errorService = resolve<IErrorHandlingService>(
  TYPES.IErrorHandlingService
);
errorService.handleError(error, "Component context");
errorService.reportCriticalError(error, "Critical system failure");
```

#### PictographDataDebugger

Specialized debugging for pictograph data flow:

```typescript
import { pictographDataDebugger } from "$build/services";
pictographDataDebugger.setDebugEnabled(true);
pictographDataDebugger.debugPictograph(pictographData);
```

#### Performance Tracking

```typescript
const tracker = PerformanceTracker.getInstance();
tracker.update(); // Call in animation loops
console.log("FPS:", tracker.getFPS());
```

### Console Forwarding

Development mode automatically forwards browser console logs to server terminal for easier debugging.

## Testing Patterns

### Test Structure

```
tests/
├── unit/           # Fast, isolated unit tests
├── integration/    # Service integration tests
├── debug/         # Debug and development tests
├── e2e/           # End-to-end Playwright tests
└── setup/         # Test configuration
```

### Test Configuration

- **Vitest**: Unit and integration tests with jsdom environment
- **Playwright**: E2E tests across Chrome, Firefox, Safari
- **Mock Setup**: Comprehensive mocking for browser APIs and services

### Writing Tests

```typescript
// Use configured aliases
import { MyService } from "$lib/services/MyService";
import { resolve, TYPES } from "$shared";

// Services resolved via test containers
const service = resolve<IMyService>(TYPES.IMyService);
```

## Component Patterns

### 1. Props with Runes

```typescript
const {
  sequence,
  isFavorite = false,
  onAction = () => {},
} = $props<{
  sequence: SequenceData;
  isFavorite?: boolean;
  onAction?: (action: string, sequence: SequenceData) => void;
}>();
```

### 2. Service Resolution in Components

```typescript
let service: IServiceInterface | null = $state(null);

onMount(async () => {
  try {
    service = resolve<IServiceInterface>(TYPES.IServiceInterface);
  } catch (error) {
    console.error("Failed to resolve service:", error);
  }
});
```

### 3. Event Handling with HMR-Safe Patterns

Components should handle service resolution failures gracefully during HMR.

### 4. Svelte 5 Snippets for Organization

Modern components use snippets for better code organization:

```typescript
// In component script
const renderEmpty = () => `<div>No data available</div>`;
const renderLoading = () => `<div>Loading...</div>`;
```

### 5. Effect Usage Patterns

```typescript
// Watch for changes and perform side effects
$effect(() => {
  console.log("Data changed:", data);
  // Cleanup automatically handled by Svelte 5
});

// Effect with cleanup
$effect(() => {
  const interval = setInterval(() => {
    // Some periodic task
  }, 1000);

  return () => clearInterval(interval);
});
```

## Data Persistence

### Dexie.js with Persistence Service

All data operations go through `IPersistenceService`:

```typescript
const persistenceService = resolve<IPersistenceService>(
  TYPES.IPersistenceService
);

// CRUD operations
await persistenceService.saveSequence(sequenceData);
const sequences = await persistenceService.getSequences();
```

Database schema includes:

- `sequences` - User-created sequence data
- `pictographs` - Pictograph library
- `userWork` - Tab states and work-in-progress

## Canvas and Rendering

### Fabric.js Integration

Canvas operations use Fabric.js through dedicated services:

- Grid rendering via `IGridRenderingService`
- Arrow positioning via `IArrowPositioningOrchestrator`
- SVG manipulation via `ISvgUtilityService`

### Performance Considerations

- Use `PerformanceTracker.getInstance()` for monitoring FPS in animations
- Complex pictograph rendering is cached and optimized
- Arrow positioning calculations are computationally expensive - cache results

## Advanced Debugging Techniques

### Domain-Specific Debugging

```typescript
// For pictograph data flow issues
import { pictographDataDebugger } from "$build/services";
pictographDataDebugger.setDebugEnabled(true);
pictographDataDebugger.startTrace("my-debug-session");
pictographDataDebugger.debugPictograph(pictographData);

// For arrow placement issues
const arrowService = resolve<IArrowPlacementService>(
  TYPES.IArrowPlacementService
);
await arrowService.debugAvailableKeys(MotionType.STATIC, GridMode.DIAMOND);
```

### Error Boundary Patterns

```typescript
// Centralized error handling
const errorService = resolve<IErrorHandlingService>(
  TYPES.IErrorHandlingService
);

try {
  // Risky operation
} catch (error) {
  errorService.handleError(error, "Component operation context");
  // Graceful fallback
}
```

### State Debugging

```typescript
// Track state changes in development
$effect(() => {
  if (import.meta.env.DEV) {
    console.log("State changed:", { data, isLoading, error });
  }
});
```

## Common Gotchas & Critical Patterns

### Development Gotchas

1. **Service Resolution**: Always check if services resolved successfully before use
2. **HMR**: State factories should be HMR-resilient - avoid side effects during initialization
3. **Circular Dependencies**: Never import from `$shared` within shared modules themselves
4. **Async DI**: Use `resolve()` not `resolveSync()` - container is async-initialized
5. **Component State**: Use factory functions, not class-based state management
6. **Derived Functions**: Call derived functions with `()` - `filteredData()` not `filteredData`
7. **Effect Cleanup**: Always return cleanup functions from `$effect` for intervals/subscriptions
8. **State Mutation**: Don't mutate state directly - use reassignment or update functions

### Critical Performance Patterns

- **Arrow Positioning**: Extremely expensive - cache placement data aggressively
- **Pictograph Rendering**: Use SVG caching for complex renders
- **State Derivations**: Keep derived calculations simple to avoid infinite loops
- **Effect Dependencies**: Be explicit about what triggers effects to prevent cascades

### Domain-Specific Gotchas

- **Grid Modes**: Diamond vs Box modes have different positioning algorithms
- **Motion Types**: Static, Pro, Anti, Float, Dash each have specific validation rules
- **Sequence Validation**: Beats must be sequential and consistent with sequence metadata
- **Arrow Calculations**: Placement keys are specific to motion type and grid mode combinations

## File Structure Conventions

- `*.svelte.ts` - Svelte 5 runes state files
- `*Service.ts` - Service implementations (DI-managed)
- `I*Service.ts` - Service interfaces/contracts
- `*-models.ts` - Domain models and types
- `*-state.svelte.ts` - State management files using runes
- `index.ts` - Barrel exports for modules (but avoid within same module)

## Testing Patterns

### Testing Best Practices

- **Unit tests**: Test individual components/services in isolation
- **Integration tests**: Test service interactions and data flow
- **Debug tests**: Development debugging scenarios and edge cases
- **E2E tests**: Full user workflows across browsers
- **Services**: Always resolve via test containers, never instantiate directly
- **Mocking**: Use vitest setup for browser API mocks
- **Async Testing**: Proper async/await patterns for service resolution

### Common Test Patterns

```typescript
// Service testing
const service = resolve<IMyService>(TYPES.IMyService);
expect(service).toBeDefined();

// Component testing with service mocking
const mockService = vi.fn();
container.bind(TYPES.IMyService).toConstantValue(mockService);

// State testing
const state = createMyState();
expect(state.data).toEqual([]);
```

## Configuration & Build

### Key Configuration Files

- `vite.config.ts` - Vite build configuration with aliases and plugins
- `svelte.config.js` - Svelte 5 with HMR enabled and module aliases
- `tsconfig.json` - TypeScript with strict mode and modern features
- `vitest.config.ts` - Test configuration with jsdom and aliases
- `playwright.config.ts` - E2E test configuration across browsers

### Development vs Production

- **Source Maps**: Enabled in development, configurable for production
- **Console Forwarding**: Development only - browser logs sent to server terminal
- **HMR Debug**: Development only - extensive debugging utilities available
- **Error Handling**: More verbose in development, sanitized in production

This architecture emphasizes **separation of concerns**, **dependency injection**, **HMR resilience**, and **domain-driven design** - follow these patterns consistently for maintainable, performant code.
