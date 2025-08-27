# TKA InversifyJS Migration Guide

## 🎯 **Mission Statement**

We are migrating TKA's custom dependency injection system to **InversifyJS** - a mature, industry-standard IoC container. This migration will improve maintainability, reduce complexity, and provide better tooling support while preserving all existing business logic.

## 🚫 **CRITICAL RULE: NO FALLBACKS OR SIMPLIFICATIONS**

**We do NOT create simplified versions, fallbacks, or placeholder implementations.** All existing business logic has been carefully crafted and must be preserved exactly. The migration focuses on **changing the DI container, not the business logic**.

## 📊 **Current Progress Status**

### ✅ **Successfully Migrated (1/27+ services)**

- **ArrowAdjustmentCalculator** - First successful migration, fully functional in InversifyJS

### 🔄 **In Progress**

- **Arrow Positioning Services** - Complex circular dependencies being resolved

### ⏳ **Pending Migration**

- **25+ remaining services** - Awaiting systematic migration

## 🏗️ **Architecture Overview**

### **Current State: Dual DI Systems**

```
┌─────────────────────┐    ┌─────────────────────┐
│   Custom DI System  │    │    InversifyJS      │
│   (Legacy)          │    │    (Target)         │
├─────────────────────┤    ├─────────────────────┤
│ • 25+ services      │ -> │ • 1 service (so far)│
│ • Complex circular  │    │ • Clean resolution  │
│ • Manual management │    │ • Auto lifecycle    │
│ • Hard to debug     │    │ • Rich tooling      │
└─────────────────────┘    └─────────────────────┘
```

### **Target State: Pure InversifyJS**

```
┌─────────────────────────────────────┐
│            InversifyJS              │
│         (All Services)              │
├─────────────────────────────────────┤
│ • All 27+ services migrated         │
│ • Circular dependencies resolved    │
│ • Consistent service lifecycle      │
│ • Better debugging & testing        │
│ • Industry-standard patterns        │
└─────────────────────────────────────┘
```

## 🔍 **Why InversifyJS?**

### **Problems with Custom DI System**

1. **Circular Dependencies** - Complex, hard-to-debug circular references
2. **Manual Lifecycle Management** - Error-prone service instantiation
3. **Limited Tooling** - No IDE support, debugging tools, or ecosystem
4. **Maintenance Burden** - Custom code requires ongoing maintenance
5. **Knowledge Barrier** - Team members need to learn custom patterns

### **Benefits of InversifyJS**

1. **Mature Ecosystem** - Battle-tested, widely adopted IoC container
2. **Automatic Lifecycle** - Handles singleton, transient, and scoped lifecycles
3. **Circular Dependency Resolution** - Built-in support for complex dependency graphs
4. **Rich Tooling** - IDE support, debugging tools, and extensive documentation
5. **TypeScript Native** - First-class TypeScript support with decorators
6. **Industry Standard** - Well-known patterns that new team members understand

## 📁 **Key Files & Progress Tracking**

### **InversifyJS Configuration**

- `web/src/lib/services/inversify/container.ts` - Main container configuration
- `web/src/lib/services/inversify/types.ts` - Service type definitions
- `web/src/lib/services/bootstrap.ts` - Bootstrap and initialization

### **Migration Progress Tracking**

- `web/src/lib/services/inversify/container.ts` - See service bindings (currently 26 services)
- `web/src/lib/services/di/` - Custom DI system (legacy, being phased out)
- `web/src/lib/services/implementations/` - Service implementations (shared by both systems)

### **Positioning Services (Current Focus)**

- `web/src/lib/services/positioning/` - Arrow positioning business logic
- `web/src/lib/services/di/interfaces/positioning-interfaces.ts` - Custom DI interfaces
- `web/src/lib/services/di/registration/positioning-services.ts` - Custom DI registration

## 🔧 **Migration Strategy**

### **Phase 1: Foundation (✅ Complete)**

- Set up InversifyJS container
- Migrate core services (settings, device detection, etc.)
- Establish migration patterns

### **Phase 2: Positioning Services (🔄 Current)**

- Resolve circular dependencies in arrow positioning
- Migrate positioning calculation services
- Maintain exact business logic behavior

### **Phase 3: Remaining Services (⏳ Pending)**

- Migrate data services (CSV, query, etc.)
- Migrate UI services (export, generation, etc.)
- Complete custom DI system removal

## 🚨 **Current Challenge: Arrow Positioning Circular Dependencies**

### **The Problem**

The arrow positioning services have complex circular dependencies:

```
ArrowPositioningService -> ArrowPositionCalculator -> ArrowAdjustmentCalculator
                      \                            /
                       -> ArrowLocationCalculator -
```

### **The Solution Approach**

1. **Identify Dependency Graph** - Map all circular references
2. **Use InversifyJS Features** - Leverage lazy injection and factory patterns
3. **Preserve Business Logic** - Keep all calculation logic exactly the same
4. **Test Thoroughly** - Ensure positioning behavior is identical

### **Current Status**

- **ArrowAdjustmentCalculator** ✅ - Successfully migrated and working
- **ArrowPositioningService** ❌ - Blocked by circular dependencies
- **Supporting Services** ⏳ - Waiting for dependency resolution

## 📋 **Migration Checklist Template**

For each service migration:

### **Pre-Migration**

- [ ] Identify all dependencies
- [ ] Check for circular references
- [ ] Document current behavior
- [ ] Create comprehensive tests

### **Migration**

- [ ] Add service to InversifyJS types
- [ ] Create container binding
- [ ] Handle dependency injection
- [ ] Resolve circular dependencies (if any)

### **Post-Migration**

- [ ] Verify identical behavior
- [ ] Update all consumers
- [ ] Remove from custom DI system
- [ ] Update documentation

## 🎯 **Success Metrics**

### **Technical Metrics**

- **Service Count**: 1/27+ services migrated to InversifyJS
- **Test Coverage**: All migrated services maintain 100% test compatibility
- **Performance**: No degradation in service resolution speed
- **Memory**: No increase in memory usage

### **Quality Metrics**

- **Zero Regressions**: All existing functionality preserved
- **Clean Architecture**: Proper separation of concerns maintained
- **Type Safety**: Full TypeScript support throughout

## 🔄 **Next Immediate Steps**

1. **Resolve ArrowPositioningService Circular Dependencies**
   - Use InversifyJS lazy injection patterns
   - Implement factory pattern for complex dependencies
   - Test positioning calculations thoroughly

2. **Complete Positioning Service Migration**
   - Migrate ArrowLocationCalculator
   - Migrate ArrowRotationCalculator
   - Migrate ArrowCoordinateSystemService

3. **Systematic Service Migration**
   - Continue with data services
   - Move to UI services
   - Complete custom DI removal

## 📚 **Resources & References**

### **InversifyJS Documentation**

- [Official Documentation](https://inversify.io/)
- [Circular Dependencies Guide](https://github.com/inversify/InversifyJS/blob/master/wiki/circular_dependencies.md)
- [TypeScript Integration](https://github.com/inversify/InversifyJS/blob/master/wiki/basic_js_example.md)

### **TKA Codebase Context**

- **Architecture**: Clean Architecture with Domain-Driven Design
- **Business Logic**: Arrow positioning, pictograph generation, sequence management
- **UI Framework**: Svelte 5 with runes-based reactivity
- **Type System**: Full TypeScript with strict mode

## 🔍 **Detailed Service Inventory**

### **Successfully Migrated to InversifyJS (26 services)**

1. **ISequenceDomainService** - Sequence business logic
2. **IPersistenceService** - Data persistence
3. **ISettingsService** - Application settings
4. **IDeviceDetectionService** - Device capability detection
5. **IEnumMappingService** - Enum value mapping
6. **ICSVParserService** - CSV data parsing
7. **IDataTransformationService** - Data transformation utilities
8. **IGridModeDeriver** - Grid mode calculation
9. **ILetterDeriver** - Letter classification
10. **IPictographValidatorService** - Pictograph validation
11. **IPositionPatternService** - Position pattern analysis
12. **ISvgConfiguration** - SVG configuration
13. **IFilenameGeneratorService** - File naming utilities
14. **IArrowAdjustmentCalculator** - Arrow position adjustments ✨ **Latest Migration**
15. **IArrowPathResolutionService** - Arrow path resolution
16. **IArrowCoordinateSystemService** - Coordinate system management
17. **ISvgLoadingService** - SVG content loading
18. **IPropCoordinatorService** - Prop coordination
19. **IBetaOffsetCalculator** - Beta position offsets
20. **IOrientationCalculationService** - Orientation calculations
21. **IPositionMapper** - Position mapping
22. **IPositionCalculatorService** - Position calculations
23. **ILetterMappingRepository** - Letter mapping data
24. **ILetterQueryService** - Letter query operations
25. **ICsvLoaderService** - CSV file loading
26. **IPictographDataDebugger** - Debug utilities

### **Remaining in Custom DI System**

- **IArrowPositioningService** - Main positioning orchestrator (blocked by circular deps)
- **IArrowLocationCalculator** - Location calculations
- **IArrowRotationCalculator** - Rotation calculations
- **IDashLocationCalculator** - Dash movement calculations
- **IDirectionalTupleProcessor** - Directional data processing
- **IArrowLocationService** - Location service wrapper
- **IArrowPlacementKeyService** - Placement key generation
- **IArrowPlacementService** - Placement coordination

## 🔧 **Technical Implementation Notes**

### **Successful Migration Pattern (ArrowAdjustmentCalculator)**

```typescript
// 1. Add to InversifyJS types
IArrowAdjustmentCalculator: Symbol.for("IArrowAdjustmentCalculator");

// 2. Create container binding with dependency resolution
container
  .bind<IArrowAdjustmentCalculator>(TYPES.IArrowAdjustmentCalculator)
  .toDynamicValue(() => {
    const gridModeService = container.get<IGridModeDeriver>(
      TYPES.IGridModeDeriver
    );
    return new ArrowAdjustmentCalculator(gridModeService);
  });

// 3. Update consumers to use InversifyJS
const adjustmentCalculator = container.get<IArrowAdjustmentCalculator>(
  TYPES.IArrowAdjustmentCalculator
);
```

### **Circular Dependency Challenge**

The positioning services form a complex dependency graph that requires careful resolution using InversifyJS patterns like:

- **Lazy Injection**: `@lazyInject()` decorator
- **Factory Pattern**: Dynamic service creation
- **Interface Segregation**: Breaking large interfaces into smaller ones

---

**Last Updated**: 2025-08-25  
**Migration Status**: Phase 2 - Positioning Services  
**Next Milestone**: Complete arrow positioning service migration  
**Application Status**: ✅ Fully functional with 26 InversifyJS services
