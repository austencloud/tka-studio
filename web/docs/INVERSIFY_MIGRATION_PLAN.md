# TKA Web App - InversifyJS Migration Plan

## 🎯 **MIGRATION OVERVIEW**

**Goal**: Replace the current 2000+ line custom DI system with InversifyJS to achieve:

- 95% reduction in DI boilerplate code
- Enterprise-grade circular dependency resolution
- Type-safe dependency injection
- Industry-standard patterns
- Maintainable, scalable architecture

**Current State**: Custom DI system with 10 registration files, 13 interface files, and complex manual factory registrations
**Target State**: InversifyJS with decorators, automatic resolution, and minimal configuration

---

## 📋 **PHASE 1: SETUP & FOUNDATION**

### **1.1 Install Dependencies**

```bash
npm install inversify reflect-metadata
npm install --save-dev @types/node
```

### **1.2 Update TypeScript Configuration**

```json
// tsconfig.json
{
  "compilerOptions": {
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true,
    "types": ["reflect-metadata"]
  }
}
```

### **1.3 Create InversifyJS Configuration**

- [x] Create `src/lib/services/inversify/types.ts` - Service identifiers ✅
- [x] Create `src/lib/services/inversify/container.ts` - Container setup ✅
- [x] Create `src/lib/services/inversify/bootstrap.ts` - Application bootstrap ✅

### **1.4 Import reflect-metadata** ✅

- [x] Add `import "reflect-metadata";` to main entry points ✅
- [x] Create `src/hooks.client.ts` for client-side initialization ✅

---

## 📋 **PHASE 2: SERVICE CONVERSION**

### **2.1 Convert Service Interfaces (Priority: High)**

**Current Pattern:**

```typescript
export const ISequenceServiceInterface =
  createServiceInterface<ISequenceService>("ISequenceService", SequenceService);
```

**Target Pattern:**

```typescript
export const TYPES = {
  ISequenceService: Symbol.for("ISequenceService"),
  // ... other services
};
```

**Files to Convert:**

- [ ] `src/lib/services/di/interfaces/core-interfaces.ts`
- [ ] `src/lib/services/di/interfaces/movement-interfaces.ts`
- [ ] `src/lib/services/di/interfaces/positioning-interfaces.ts`
- [ ] `src/lib/services/di/interfaces/browse-interfaces.ts`
- [ ] `src/lib/services/di/interfaces/image-export-interfaces.ts`
- [ ] All other interface files (13 total)

### **2.2 Convert Service Implementations (Priority: High)**

**Current Pattern:**

```typescript
export class SequenceService implements ISequenceService {
  constructor(
    private sequenceDomainService: ISequenceDomainService,
    private persistenceService: IPersistenceService
  ) {}
}
```

**Target Pattern:**

```typescript
@injectable()
export class SequenceService implements ISequenceService {
  constructor(
    @inject(TYPES.ISequenceDomainService)
    private sequenceDomainService: ISequenceDomainService,
    @inject(TYPES.IPersistenceService)
    private persistenceService: IPersistenceService
  ) {}
}
```

**Critical Services to Convert First:**

- [ ] `SequenceService` - Core business logic
- [ ] `PictographRenderingService` - Complex 7-dependency service
- [ ] `SequenceStateService` - State management
- [ ] `PersistenceService` - Data layer
- [x] `SettingsService` - Configuration ✅ **COMPLETED**

---

## 📋 **PHASE 3: REGISTRATION ELIMINATION**

### **3.1 Replace Manual Factory Registrations**

**Current Nightmare (245 lines in core-services.ts):**

```typescript
container.registerFactory(IPictographRenderingServiceInterface, () => {
  const arrowPositioning = container.resolve(
    IArrowPositioningOrchestratorInterface
  );
  const svgUtility = container.resolve(ISvgUtilityServiceInterface);
  // ... 5 more manual resolutions
  return new PictographRenderingService(/* 7 parameters */);
});
```

**Target Simplicity:**

```typescript
container
  .bind<IPictographRenderingService>(TYPES.IPictographRenderingService)
  .to(PictographRenderingService)
  .inSingletonScope();
```

**Files to DELETE:**

- [ ] `src/lib/services/di/registration/core-services.ts` (245 lines)
- [ ] `src/lib/services/di/registration/movement-services.ts`
- [ ] `src/lib/services/di/registration/positioning-services.ts`
- [ ] `src/lib/services/di/registration/browse-services.ts`
- [ ] All 10 registration files

### **3.2 Replace Custom ServiceContainer**

- [ ] Delete `src/lib/services/di/ServiceContainer.ts` (140 lines)
- [ ] Delete `src/lib/services/di/types.ts`
- [ ] Delete `src/lib/services/di/validation.ts`
- [ ] Delete `src/lib/services/di/service-registry.ts`

---

## 📋 **PHASE 4: BOOTSTRAP REPLACEMENT**

### **4.1 Replace bootstrap.ts**

**Current Complex Bootstrap (100+ lines):**

```typescript
await registerSharedServices(container);
await registerCoreServices(container);
await registerCodexServices(container);
// ... 7 more registration calls with dependency ordering
```

**Target Simple Bootstrap:**

```typescript
const container = new Container();
container.load(coreModule, renderingModule, persistenceModule);
export { container };
```

### **4.2 Update Service Resolution**

**Current Pattern:**

```typescript
const sequenceService = resolve("ISequenceService");
```

**Target Pattern:**

```typescript
const sequenceService = container.get<ISequenceService>(TYPES.ISequenceService);
```

---

## 📋 **PHASE 5: COMPONENT INTEGRATION**

### **5.1 Update Svelte Components**

**Current Pattern:**

```svelte
<script lang="ts">
  import { resolve } from "$services/bootstrap";
  const sequenceService = resolve("ISequenceService");
</script>
```

**Target Pattern:**

```svelte
<script lang="ts">
  import { container } from "$services/inversify/container";
  import { TYPES } from "$services/inversify/types";
  const sequenceService = container.get<ISequenceService>(
    TYPES.ISequenceService
  );
</script>
```

### **5.2 Update State Factories**

- [ ] Update all `*-state-factory.svelte.ts` files
- [ ] Ensure proper service injection in state layer
- [ ] Maintain clean separation between services and reactive state

---

## 📋 **PHASE 6: TESTING & VALIDATION**

### **6.1 Update Tests**

- [ ] Update service mocking patterns
- [ ] Update dependency injection in tests
- [ ] Ensure all tests pass with new DI system

### **6.2 Validation Checklist**

- [ ] All services resolve correctly
- [ ] No circular dependency errors
- [ ] Application starts successfully
- [ ] All features work as expected
- [ ] Performance is maintained or improved

---

## 🚨 **CRITICAL SUCCESS FACTORS**

1. **Incremental Migration**: Convert services one module at a time
2. **Maintain Parallel Systems**: Keep old DI working until full migration
3. **Test Early & Often**: Validate each phase before proceeding
4. **Document Changes**: Update architecture docs as you go

---

## 📊 **EXPECTED OUTCOMES**

**Before Migration:**

- 2000+ lines of DI boilerplate
- 23+ files to maintain
- Manual dependency wiring
- Error-prone string tokens
- Complex ordering requirements

**After Migration:**

- ~100 lines of decorators and configuration
- 3-5 files to maintain
- Automatic dependency resolution
- Type-safe service identifiers
- Zero ordering requirements

**Estimated Time Savings**: 95% reduction in DI maintenance overhead

---

## ⏱️ **TIME ESTIMATES**

### **Realistic Timeline Breakdown**

| Phase       | Description              | Estimated Time | Complexity |
| ----------- | ------------------------ | -------------- | ---------- |
| **Phase 1** | Setup & Foundation       | **2-3 hours**  | Low        |
| **Phase 2** | Service Conversion       | **8-12 hours** | High       |
| **Phase 3** | Registration Elimination | **4-6 hours**  | Medium     |
| **Phase 4** | Bootstrap Replacement    | **2-3 hours**  | Low        |
| **Phase 5** | Component Integration    | **6-8 hours**  | Medium     |
| **Phase 6** | Testing & Validation     | **4-6 hours**  | Medium     |

### **Total Estimated Time: 26-38 hours**

### **Risk Factors That Could Add Time:**

- 🔄 **Circular dependency debugging**: +4-8 hours
- 🧪 **Complex service interdependencies**: +3-6 hours
- 📚 **InversifyJS learning curve**: +2-4 hours
- 🐛 **Unexpected integration issues**: +3-5 hours

### **Conservative Estimate: 35-50 hours**

### **Recommended Approach:**

- **Week 1**: Phase 1 + start Phase 2 (10-15 hours)
- **Week 2**: Complete Phase 2 + Phase 3 (15-20 hours)
- **Week 3**: Phases 4-6 + cleanup (10-15 hours)

---

## 📝 **NEXT STEPS**

1. **Start with Phase 1** - Set up InversifyJS foundation (2-3 hours)
2. **Convert one service module** - Prove the pattern works
3. **Gradually migrate** - One registration file at a time
4. **Delete old system** - Remove custom DI when migration complete

**Ready to begin Phase 1?**
