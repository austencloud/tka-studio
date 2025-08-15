# TKA Architecture Guide: Clean Svelte 5 + Microservices

This guide documents the **correct architectural patterns** for TKA and provides **migration paths** from problematic code.

## 🏗️ **Architecture Overview**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   COMPONENTS    │    │   STATE LAYER   │    │  SERVICE LAYER  │
│   (UI Logic)    │◄──►│ (Reactive State)│◄──►│ (Business Logic)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
    Svelte 5 Runes         Runes Factories         Pure TypeScript
    Component State        Component-Scoped           DI Container
    User Interactions      Service Wrappers          Domain Logic
```

## ✅ **CORRECT PATTERNS**

### **1. Component Layer**

```svelte
<!-- ✅ GOOD: Component with proper DI usage -->
<script lang="ts">
  import { resolve } from "$services/bootstrap";
  import { createSequenceState } from "$state/sequence-state-factory.svelte";

  // Get services from DI container
  const sequenceService = resolve("ISequenceService");

  // Create component-scoped reactive state
  const state = createSequenceState(sequenceService);

  // Component-local state
  let selectedIndex = $state(0);

  // Reactive computations
  let isValid = $derived(state.currentSequence && !state.hasError);
</script>
```

### **2. State Layer (Reactive Wrappers)**

```typescript
// ✅ GOOD: State factory pattern
export function createSequenceState(service: ISequenceService) {
  let sequences = $state<SequenceData[]>([]);
  let loading = $state(false);

  return {
    get sequences() {
      return sequences;
    },
    get loading() {
      return loading;
    },

    async loadSequences() {
      loading = true;
      sequences = await service.getAllSequences(); // Pure service call
      loading = false;
    },
  };
}
```

### **3. Service Layer (Pure Business Logic)**

```typescript
// ✅ GOOD: Pure TypeScript service
export class SequenceService implements ISequenceService {
  constructor(
    private domainService: ISequenceDomainService,
    private persistence: IPersistenceService
  ) {}

  async createSequence(request: SequenceCreateRequest): Promise<SequenceData> {
    // Pure business logic - no runes, no Svelte
    const sequence = this.domainService.createSequence(request);
    await this.persistence.saveSequence(sequence);
    return sequence;
  }
}
```

## ❌ **ANTI-PATTERNS TO AVOID**

### **1. Services with Runes**

```typescript
// ❌ BAD: Service using reactive state
class BadSequenceService {
  #currentSequence = $state<SequenceData | null>(null); // NO!

  // Business logic mixed with reactive state
}
```

### **2. Global Singleton State**

```typescript
// ❌ BAD: Global state
const state = $state({ sequences: [] });
export { state }; // Exported globally - bad!
```

### **3. Business Logic in State**

```typescript
// ❌ BAD: Complex business logic in state layer
export function updateCurrentBeat(beatIndex: number, beatData: BeatData) {
  // Complex validation and calculation logic here - belongs in service!
}
```

## 🔄 **MIGRATION STRATEGY**

### **Phase 1: Service Layer Clean-up**

#### **Files to Migrate**:

- `src/lib/services/SequenceStateService.svelte.ts` → Pure service
- `src/lib/services/BeatFrameService.svelte.ts` → Pure service
- `src/lib/services/PictographService.svelte.ts` → Pure service
- `src/lib/services/WorkbenchService.svelte.ts` → Pure service

#### **Migration Steps**:

1. **Extract business logic** to pure TypeScript service
2. **Remove runes** from service implementations
3. **Register in DI container**
4. **Create state factory** to wrap service with runes
5. **Update components** to use factory pattern

### **Phase 2: State Layer Restructuring**

#### **Files to Migrate**:

- `src/lib/state/sequenceState.svelte.ts` → State factory
- `src/lib/stores/constructTabState.svelte.ts` → State factory
- `src/lib/stores/simpleAppState.svelte.ts` → State factory

#### **Migration Steps**:

1. **Convert global state** to factory functions
2. **Extract business logic** to services
3. **Create component-scoped** reactive wrappers
4. **Update all imports** to use factories

### **Phase 3: Directory Cleanup**

#### **Actions**:

1. **Remove `stores/` directory** after migration
2. **Consolidate state factories** in `state/` directory
3. **Ensure all services** are in `services/implementations/`
4. **Update import paths** throughout codebase

## 📋 **MIGRATION CHECKLIST**

### **Service Migration Checklist**

- [ ] Remove all `$state`, `$derived`, `$effect` from service
- [ ] Ensure service has no Svelte imports
- [ ] Register service in DI container
- [ ] Create corresponding interface
- [ ] Add unit tests for business logic
- [ ] Create state factory wrapper

### **State Migration Checklist**

- [ ] Convert global state to factory function
- [ ] Move business logic to services
- [ ] Ensure state is component-scoped
- [ ] Update all consuming components
- [ ] Remove old state files after migration
- [ ] Update import statements

### **Component Migration Checklist**

- [ ] Use `resolve()` to get services from DI
- [ ] Create state using factory pattern
- [ ] Remove direct service instantiation
- [ ] Ensure reactive state is component-scoped
- [ ] Test component in isolation

## 🧪 **TESTING STRATEGY**

### **Service Testing**

```typescript
// Services are pure TypeScript - easy to test
describe("SequenceService", () => {
  let service: SequenceService;
  let mockPersistence: MockPersistenceService;

  beforeEach(() => {
    mockPersistence = new MockPersistenceService();
    service = new SequenceService(mockDomainService, mockPersistence);
  });

  it("should create sequence", async () => {
    const result = await service.createSequence({ name: "Test", length: 8 });
    expect(result.name).toBe("Test");
  });
});
```

### **State Testing**

```typescript
// State factories are testable with mock services
describe("createSequenceState", () => {
  it("should load sequences", async () => {
    const mockService = { getAllSequences: () => Promise.resolve([]) };
    const state = createSequenceState(mockService);

    await state.loadSequences();
    expect(state.sequences).toEqual([]);
  });
});
```

## 📚 **EXAMPLES**

See the `src/lib/examples/` directory for complete working examples:

- `examples/state/sequence-state-factory.svelte.ts` - Proper state factory
- `examples/services/example-sequence-service.ts` - Pure service implementation
- `examples/components/` - Component usage patterns (coming soon)

## 🚨 **VALIDATION**

### **Architecture Validation Questions**

1. Can business logic be tested without UI? (**Should be YES**)
2. Is component state purely reactive? (**Should be YES**)
3. Are services pure TypeScript? (**Should be YES**)
4. Does DI container resolve cleanly? (**Should be YES**)
5. Is state component-scoped? (**Should be YES**)

### **File Extension Rules**

- **Services**: `.ts` (pure TypeScript)
- **State**: `.svelte.ts` (uses runes)
- **Components**: `.svelte` (Svelte components)
- **Domain**: `.ts` (pure TypeScript)

### **Import Rules**

- **Services**: No Svelte imports allowed
- **State**: Can import from Svelte
- **Components**: Can import anything
- **Domain**: No framework imports

## 🛠️ **TOOLS**

Create linting rules to enforce architecture:

```json
// .eslintrc.json additions
{
  "rules": {
    "no-restricted-imports": [
      "error",
      {
        "patterns": [
          {
            "group": ["**/services/**/*.ts"],
            "message": "Services cannot import Svelte - use pure TypeScript"
          }
        ]
      }
    ]
  }
}
```

This guide ensures your TKA codebase follows clean architecture principles with proper separation of concerns.
