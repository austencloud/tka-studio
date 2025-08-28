# TKA Interface Reorganization Plan

## 📊 **Current State Analysis**

### **What's Already Done:**
- ✅ `application/index.ts` - 417 lines (needs splitting)
- ✅ `infrastructure/device/index.ts` - device interfaces moved
- ✅ `domain/browse/index.ts` - browse interfaces moved  
- 📁 Empty prepared directories: `domain/export/`, `domain/pictograph/`, `domain/positioning/`, `domain/sequence/`, `shared/`

### **What Needs Organization:**
- 🗃️ **44 loose interface files** still in root interfaces directory
- 📏 **Large files requiring splits:**
  - `positioning-interfaces.ts` (532 lines)
  - `application-interfaces.ts` (417 lines) 
  - `sequence-card-export-interfaces.ts` (394 lines)
  - `generation-interfaces.ts` (306 lines)
  - `sequence-interfaces.ts` (304 lines)

---

## 🎯 **Target Structure**

```
src/lib/services/interfaces/
├── browse/                    # Business area: Sequence discovery
│   ├── browse-service.ts           # Core filtering/browsing (80 lines)
│   ├── thumbnail-service.ts        # Thumbnail management (40 lines) 
│   ├── search-service.ts           # Search functionality (50 lines)
│   ├── navigation-service.ts       # Navigation structure (60 lines)
│   └── favorites-service.ts        # User favorites (30 lines)
├── sequence/                  # Business area: Sequence management
│   ├── sequence-crud.ts            # CRUD operations (120 lines)
│   ├── sequence-validation.ts      # Validation logic (80 lines)
│   ├── sequence-animation.ts       # Animation interfaces (100 lines)
│   └── sequence-state.ts           # State management (109 lines)
├── export/                    # Business area: Export functionality  
│   ├── core/
│   │   ├── export-service.ts       # Main export logic (110 lines)
│   │   └── export-config.ts        # Configuration (86 lines)
│   ├── image/
│   │   ├── image-core.ts           # Core image export (188 lines)
│   │   ├── image-layout.ts         # Layout calculations (93 lines)
│   │   ├── image-rendering.ts      # Rendering engine (120 lines)
│   │   ├── image-utilities.ts      # Utility functions (184 lines)
│   │   ├── image-files.ts          # File operations (64 lines)
│   │   └── image-formats.ts        # Format definitions (67 lines)
│   ├── sequence-cards/
│   │   ├── card-interfaces.ts      # Basic card interfaces (169 lines)
│   │   ├── card-export-core.ts     # Core export logic (150 lines)
│   │   ├── card-export-layout.ts   # Layout export (120 lines)
│   │   └── card-export-rendering.ts # Rendering export (124 lines)
│   ├── documents/
│   │   ├── page-export.ts          # Page export (120 lines)
│   │   ├── pdf-export.ts           # PDF export (51 lines)
│   │   └── batch-export.ts         # Batch operations (56 lines)
│   └── rendering/
│       ├── svg-conversion.ts       # SVG operations (97 lines)
│       └── text-rendering.ts       # Text rendering (119 lines)
├── pictograph/                # Business area: Pictograph operations
│   └── pictograph-service.ts       # Pictograph interfaces (245 lines)
├── positioning/               # Business area: Mathematical positioning
│   ├── grid-positioning.ts         # Grid calculations (200 lines)
│   ├── pictograph-positioning.ts   # Pictograph placement (180 lines)
│   ├── mathematical-utils.ts       # Math utilities (100 lines)
│   └── positioning-types.ts        # Shared positioning types (52 lines)
├── workbench/                 # Business area: Workbench operations
│   └── workbench-service.ts        # Workbench interfaces (177 lines)
├── beat-frame/                # Business area: Beat frame system
│   ├── beat-frame-service.ts       # Frame management (134 lines)
│   ├── beat-grid-service.ts        # Grid operations (123 lines)
│   └── beat-fallback-service.ts    # Fallback handling (43 lines)
├── codex/                     # Business area: Codex/dictionary
│   └── codex-service.ts            # Codex interfaces (39 lines)
├── data/                      # Business area: Data management
│   └── data-service.ts             # Data interfaces (143 lines)
├── application/               # Cross-cutting: App-level services
│   ├── settings-service.ts         # Settings management (100 lines)
│   ├── startup-service.ts          # App initialization (80 lines)
│   ├── utility-services.ts         # CSV, enum mapping (120 lines)
│   ├── animation-orchestration.ts  # Animation coordination (80 lines)
│   └── option-services.ts          # Option/start position (37 lines)
├── infrastructure/            # Cross-cutting: Technical services
│   ├── device/
│   │   └── index.ts                # ✅ Already done
│   ├── responsive/
│   │   └── responsive-layout.ts    # Responsive utilities (98 lines)
│   ├── testing/
│   │   ├── metadata-testing.ts     # Testing interfaces (66 lines)
│   │   └── motion-testing.ts       # Motion testing (79 lines)
│   ├── background/
│   │   └── background-service.ts   # Background management (38 lines)
│   ├── build/
│   │   └── build-service.ts        # Build operations (45 lines)
│   ├── generation/
│   │   ├── generation-core.ts      # Core generation (150 lines)
│   │   └── generation-advanced.ts  # Advanced generation (156 lines)
│   ├── panels/
│   │   ├── panel-service.ts        # Panel management (77 lines)
│   │   └── option-picker.ts        # Option picker (142 lines)
│   └── services/
│       ├── start-position.ts       # Start position services (64 lines)
│       └── build-tab.ts            # Build tab service (45 lines)
├── shared/                    # Cross-cutting: Common types
│   ├── core-types.ts               # Core application types (121 lines)
│   ├── domain-types.ts             # Domain entity types (47 lines)
│   └── constants.ts                # Service constants (38 lines)
└── index.ts                   # Barrel export for all interfaces
```

---

## 📋 **Migration Plan**

### **Phase 1: Remove Confusing Structure**
1. **Delete empty `domain/` folder** - We decided this was redundant with `src/lib/domain/`
2. **Move existing consolidated content** from `domain/browse/` to `browse/`
3. **Keep `application/` and `infrastructure/`** - these are truly cross-cutting

### **Phase 2: Organize by Business Area**
1. **Create business area directories:**
   - `browse/` (sequence discovery)
   - `sequence/` (sequence management) 
   - `export/` (export functionality)
   - `pictograph/` (pictograph operations)
   - `positioning/` (mathematical positioning)
   - `workbench/` (workbench operations)
   - `beat-frame/` (beat frame system)
   - `codex/` (codex/dictionary)
   - `data/` (data management)

2. **Move single-file business areas:**
   - `pictograph-interfaces.ts` → `pictograph/pictograph-service.ts`
   - `workbench-interfaces.ts` → `workbench/workbench-service.ts`
   - `codex-interfaces.ts` → `codex/codex-service.ts`
   - `data-interfaces.ts` → `data/data-service.ts`

### **Phase 3: Split Large Files**

#### **Split `positioning-interfaces.ts` (532 lines):**
```
positioning/
├── grid-positioning.ts         # Grid calculation interfaces
├── pictograph-positioning.ts   # Pictograph placement interfaces  
├── mathematical-utils.ts       # Mathematical utility interfaces
└── positioning-types.ts        # Shared positioning types
```

#### **Split `application-interfaces.ts` (417 lines):**
```
application/
├── settings-service.ts         # Settings management interfaces
├── startup-service.ts          # App initialization interfaces
├── utility-services.ts         # CSV, enum mapping utilities
├── animation-orchestration.ts  # Animation coordination interfaces
└── option-services.ts          # Option/start position interfaces
```

#### **Split `sequence-card-export-interfaces.ts` (394 lines):**
```
export/sequence-cards/
├── card-interfaces.ts          # Basic card interface definitions
├── card-export-core.ts         # Core export logic
├── card-export-layout.ts       # Layout-specific export
└── card-export-rendering.ts    # Rendering-specific export
```

#### **Split `generation-interfaces.ts` (306 lines):**
```
infrastructure/generation/
├── generation-core.ts          # Core generation interfaces
└── generation-advanced.ts      # Advanced generation features
```

#### **Split `sequence-interfaces.ts` (304 lines):**
```
sequence/
├── sequence-crud.ts            # CRUD operation interfaces
├── sequence-validation.ts      # Validation interfaces
└── sequence-animation.ts       # Animation-related interfaces
```

### **Phase 4: Organize Export Domain**
**Export is the most complex - organize into logical sub-domains:**

1. **Core export functionality:**
   - `export-interfaces.ts` → `export/core/export-service.ts`
   - `export-config-interfaces.ts` → `export/core/export-config.ts`

2. **Image export (6 files):**
   - All `image-export-*.ts` files → `export/image/` directory

3. **Document export:**
   - `page-export-interfaces.ts` → `export/documents/page-export.ts`
   - `pdf-export-interfaces.ts` → `export/documents/pdf-export.ts`
   - `batch-export-interfaces.ts` → `export/documents/batch-export.ts`

4. **Rendering utilities:**
   - `svg-conversion-interfaces.ts` → `export/rendering/svg-conversion.ts`
   - `text-rendering-interfaces.ts` → `export/rendering/text-rendering.ts`

### **Phase 5: Infrastructure Organization**
**Organize remaining technical/infrastructure interfaces:**

1. **Testing interfaces:**
   - `metadata-testing-interfaces.ts` → `infrastructure/testing/metadata-testing.ts`
   - `motion-tester-interfaces.ts` → `infrastructure/testing/motion-testing.ts`

2. **Panel/UI interfaces:**
   - `panel-interfaces.ts` → `infrastructure/panels/panel-service.ts`
   - `option-picker-interfaces.ts` → `infrastructure/panels/option-picker.ts`

3. **Service interfaces:**
   - `IStartPositionService.ts` + `IStartPositionSelectionService.ts` → `infrastructure/services/start-position.ts`
   - `IBuildTabService.ts` → `infrastructure/services/build-tab.ts`

4. **Standalone services:**
   - `responsive-layout-interfaces.ts` → `infrastructure/responsive/responsive-layout.ts`
   - `background-interfaces.ts` → `infrastructure/background/background-service.ts`

### **Phase 6: Shared Types Organization**
**Move common types to shared directory:**

1. **Move core types:**
   - `core-types.ts` → `shared/core-types.ts`
   - `domain-types.ts` → `shared/domain-types.ts`
   - `service-constants.ts` → `shared/constants.ts`

2. **Delete utility files:**
   - `test-import.ts` (2 lines) - delete if not needed

### **Phase 7: Update Barrel Exports**
**Create comprehensive `index.ts` files:**

1. **Root barrel export** - Export all interfaces from organized structure
2. **Directory barrel exports** - Each directory gets its own `index.ts`
3. **Update existing imports** - Update any broken import paths

---

## 📏 **File Size Guidelines**

- ✅ **Target:** 50-150 lines per file
- ⚠️ **Acceptable:** 150-250 lines  
- 🚨 **Must Split:** 250+ lines

---

## 🎯 **Success Criteria**

1. **No file exceeds 250 lines**
2. **Clear business area organization**
3. **No naming conflicts with `src/lib/domain/`**
4. **Logical grouping of related interfaces**
5. **Easy navigation and discovery**
6. **All imports work correctly**
7. **TypeScript compilation succeeds**

---

## 🚨 **Risk Mitigation**

1. **Create git branch** before starting
2. **Migrate incrementally** (one business area at a time)
3. **Test TypeScript compilation** after each phase
4. **Update imports gradually** to avoid breaking changes
5. **Keep original files** until migration is complete and tested

---

## 📝 **Notes**

- **Remove `domain/` subfolder** - Redundant with `src/lib/domain/`
- **Keep `application/` and `infrastructure/`** - These are truly cross-cutting concerns
- **Export domain** is most complex and needs careful sub-organization
- **Large files must be split** - 532-line files are unmanageable
- **Business areas** should be self-contained with minimal cross-dependencies
