# TKA-Specific Enterprise Interface Organization Plan

## Current State Analysis

### 🔍 **Your Actual Interface Chaos (Confirmed)**

**Current Structure Issues:**

- **28 interface files** in `/src/lib/services/interfaces/`
- **258-line mega barrel export** in `index.ts`
- **183 DI tokens** scattered in `types.ts`
- **Mixed concerns everywhere**: types, interfaces, constants, and test files
- **Inconsistent naming**: `-interfaces.ts` vs `core-types.ts` vs `domain-types.ts`

**Specific Problems Found:**

- `sequence-interfaces.ts` includes page layout services (business + technical mixed)
- `image-export-interfaces.ts` has 8 different export service categories crammed together
- `service-constants.ts` uses different patterns than `types.ts` for DI tokens
- Related services split across files (positioning has subdirectories)

---

## TKA-Optimized Domain Structure

### 🏗️ **Phase 1: Domain-Driven Organization (Based on Your Actual Services)**

```
src/lib/contracts/
├── domain/                          # Business Domain Contracts
│   ├── sequence/                    # From your implementations/sequence/
│   │   ├── core/
│   │   │   ├── ISequenceService.ts              # CRUD operations
│   │   │   ├── ISequenceDomainService.ts        # Business logic
│   │   │   ├── ISequenceStateService.ts         # State management
│   │   │   └── SequenceTypes.ts                 # Core sequence data
│   │   ├── operations/
│   │   │   ├── ISequenceImportService.ts        # External data import
│   │   │   ├── IDeleteService.ts                # Deletion operations
│   │   │   └── OperationTypes.ts                # Operation-specific types
│   │   ├── tokens/
│   │   │   └── SequenceTokens.ts                # All sequence DI tokens
│   │   └── index.ts                             # Domain barrel export
│   │
│   ├── pictograph/                  # From your pictograph-interfaces.ts
│   │   ├── rendering/
│   │   │   ├── IGridRenderingService.ts         # Grid visualization
│   │   │   ├── IArrowRenderingService.ts        # Arrow visualization
│   │   │   ├── IOverlayRenderingService.ts      # Overlay rendering
│   │   │   └── RenderingTypes.ts                # Rendering configs
│   │   ├── svg/
│   │   │   ├── ISvgUtilityService.ts            # SVG manipulation
│   │   │   ├── ISvgConfiguration.ts             # SVG config
│   │   │   └── SvgTypes.ts                      # SVG-specific types
│   │   ├── tokens/
│   │   │   └── PictographTokens.ts              # All pictograph DI tokens
│   │   └── index.ts
│   │
│   ├── export/                      # From your implementations/export/
│   │   ├── core/
│   │   │   ├── IExportService.ts                # Main export orchestrator
│   │   │   └── ExportCoreTypes.ts               # Core export types
│   │   ├── image/
│   │   │   ├── ITKAImageExportService.ts        # TKA-specific exports
│   │   │   ├── ICanvasManagementService.ts      # Canvas operations
│   │   │   ├── IImageCompositionService.ts      # Image composition
│   │   │   ├── IFileExportService.ts            # File operations
│   │   │   └── ImageExportTypes.ts              # Image export configs
│   │   ├── layout/
│   │   │   ├── ILayoutCalculationService.ts     # Page layout
│   │   │   ├── IDimensionCalculationService.ts  # Dimensions
│   │   │   ├── IExportConfigurationManager.ts   # Layout config
│   │   │   └── LayoutTypes.ts                   # Layout calculations
│   │   ├── sequence-cards/
│   │   │   ├── ISequenceCardImageService.ts     # Card image generation
│   │   │   ├── ISequenceCardLayoutService.ts    # Card layout
│   │   │   ├── ISequenceCardPageService.ts      # Card pagination
│   │   │   └── SequenceCardTypes.ts             # Card-specific types
│   │   ├── validation/
│   │   │   ├── IExportOptionsValidator.ts       # Export validation
│   │   │   ├── IExportMemoryCalculator.ts       # Memory estimation
│   │   │   └── ValidationTypes.ts               # Validation configs
│   │   ├── tokens/
│   │   │   └── ExportTokens.ts                  # All export DI tokens
│   │   └── index.ts
│   │
│   ├── browse/                      # From your implementations/browse/
│   │   ├── core/
│   │   │   ├── IBrowseService.ts                # Main browse orchestrator
│   │   │   ├── ISectionService.ts               # Section management
│   │   │   ├── ISequenceIndexService.ts         # Search indexing
│   │   │   └── BrowseTypes.ts                   # Browse data structures
│   │   ├── management/
│   │   │   ├── IThumbnailService.ts             # Thumbnail generation
│   │   │   ├── IFavoritesService.ts             # User favorites
│   │   │   ├── IFilterPersistenceService.ts     # Filter state
│   │   │   └── ManagementTypes.ts               # Management configs
│   │   ├── tokens/
│   │   │   └── BrowseTokens.ts                  # All browse DI tokens
│   │   └── index.ts
│   │
│   ├── workbench/                   # From your implementations/workbench/
│   │   ├── core/
│   │   │   ├── IWorkbenchService.ts             # Main workbench
│   │   │   ├── IWorkbenchCoordinationService.ts # Coordination
│   │   │   └── WorkbenchTypes.ts                # Workbench state
│   │   ├── operations/
│   │   │   ├── IWorkbenchBeatOperationsService.ts # Beat manipulation
│   │   │   ├── IConstructTabCoordinationService.ts # Tab coordination
│   │   │   └── OperationTypes.ts                # Operation configs
│   │   ├── tokens/
│   │   │   └── WorkbenchTokens.ts               # All workbench DI tokens
│   │   └── index.ts
│   │
│   ├── positioning/                 # From your implementations/positioning/
│   │   ├── arrows/
│   │   │   ├── IArrowPositioningService.ts      # Arrow positioning
│   │   │   ├── IArrowPlacementService.ts        # Arrow placement
│   │   │   ├── IArrowAdjustmentCalculator.ts    # Arrow adjustments
│   │   │   └── ArrowTypes.ts                    # Arrow positioning types
│   │   ├── props/
│   │   │   ├── IPropPlacementService.ts         # Prop positioning
│   │   │   ├── IPropCoordinatorService.ts       # Prop coordination
│   │   │   └── PropTypes.ts                     # Prop positioning types
│   │   ├── calculations/
│   │   │   ├── IOrientationCalculationService.ts # Orientation math
│   │   │   ├── IBetaOffsetCalculator.ts         # Beta calculations
│   │   │   └── CalculationTypes.ts              # Math types
│   │   ├── tokens/
│   │   │   └── PositioningTokens.ts             # All positioning DI tokens
│   │   └── index.ts
│   │
│   ├── animation/                   # NEW: For your animation services
│   │   ├── core/
│   │   │   ├── IAnimationStateService.ts        # Animation state
│   │   │   ├── ISequenceAnimationOrchestrator.ts # Animation orchestration
│   │   │   └── AnimationTypes.ts                # Animation data
│   │   ├── control/
│   │   │   ├── IAnimationControlService.ts      # Animation controls
│   │   │   ├── IPropInterpolationService.ts     # Prop animation
│   │   │   └── ControlTypes.ts                  # Control configs
│   │   ├── tokens/
│   │   │   └── AnimationTokens.ts               # All animation DI tokens
│   │   └── index.ts
│   │
│   ├── motion/                      # NEW: For your motion analysis
│   │   ├── analysis/
│   │   │   ├── IMotionQueryService.ts           # Motion querying
│   │   │   ├── IMotionParameterService.ts       # Motion parameters
│   │   │   ├── IMotionLetterIdentificationService.ts # Letter ID
│   │   │   └── AnalysisTypes.ts                 # Motion analysis types
│   │   ├── generation/
│   │   │   ├── ISequenceGenerationService.ts    # Motion generation
│   │   │   ├── IPictographValidatorService.ts   # Motion validation
│   │   │   └── GenerationTypes.ts               # Generation configs
│   │   ├── tokens/
│   │   │   └── MotionTokens.ts                  # All motion DI tokens
│   │   └── index.ts
│   │
│   ├── beat-frame/                  # NEW: For your beat services
│   │   ├── core/
│   │   │   ├── IBeatFrameService.ts             # Beat frame management
│   │   │   ├── IBeatGridService.ts              # Beat grid rendering
│   │   │   └── BeatTypes.ts                     # Beat data structures
│   │   ├── rendering/
│   │   │   ├── IBeatRenderingService.ts         # Beat visualization
│   │   │   ├── IBeatFallbackRenderingService.ts # Fallback rendering
│   │   │   └── RenderingTypes.ts                # Beat rendering configs
│   │   ├── tokens/
│   │   │   └── BeatTokens.ts                    # All beat DI tokens
│   │   └── index.ts
│   │
│   └── codex/                       # NEW: For your letter/codex services
│       ├── core/
│       │   ├── ICodexService.ts                 # Main codex service
│       │   ├── ILetterQueryService.ts           # Letter querying
│       │   └── CodexTypes.ts                    # Codex data structures
│       ├── mapping/
│       │   ├── ILetterMappingRepository.ts      # Letter mappings
│       │   ├── IOptionFilteringService.ts       # Option filtering
│       │   └── MappingTypes.ts                  # Mapping configurations
│       ├── tokens/
│       │   └── CodexTokens.ts                   # All codex DI tokens
│       └── index.ts
│
├── infrastructure/                  # Technical Infrastructure
│   ├── persistence/
│   │   ├── IPersistenceService.ts               # Data storage abstraction
│   │   ├── ILocalStoragePersistenceService.ts   # Local storage impl
│   │   ├── PersistenceTypes.ts                  # Storage types
│   │   ├── PersistenceTokens.ts                 # Storage DI tokens
│   │   └── index.ts
│   ├── device/
│   │   ├── IDeviceDetectionService.ts           # Device capabilities
│   │   ├── DeviceTypes.ts                       # Device data structures
│   │   ├── DeviceTokens.ts                      # Device DI tokens
│   │   └── index.ts
│   ├── data/
│   │   ├── ICSVParserService.ts                 # CSV parsing
│   │   ├── ICsvLoaderService.ts                 # CSV loading
│   │   ├── IDataTransformationService.ts        # Data transformation
│   │   ├── DataTypes.ts                         # Data processing types
│   │   ├── DataTokens.ts                        # Data DI tokens
│   │   └── index.ts
│   └── rendering/
│       ├── ICanvasService.ts                    # Canvas manipulation
│       ├── IDomManipulationService.ts           # DOM operations
│       ├── RenderingTypes.ts                    # Technical rendering types
│       ├── RenderingTokens.ts                   # Rendering DI tokens
│       └── index.ts
│
├── application/                     # Application-Level Services
│   ├── initialization/
│   │   ├── IApplicationInitializationService.ts # App startup
│   │   ├── InitializationTypes.ts               # Startup configs
│   │   └── index.ts
│   ├── settings/
│   │   ├── ISettingsService.ts                  # User preferences
│   │   ├── SettingsTypes.ts                     # Settings data
│   │   └── index.ts
│   ├── navigation/
│   │   ├── INavigationService.ts                # App navigation
│   │   ├── IPanelManagementService.ts           # Panel management
│   │   ├── NavigationTypes.ts                   # Navigation state
│   │   └── index.ts
│   ├── tokens/
│   │   └── ApplicationTokens.ts                 # All app DI tokens
│   └── index.ts
│
├── shared/                          # Cross-Cutting Contracts
│   ├── CoreTypes.ts                             # From your core-types.ts
│   ├── DomainTypes.ts                           # From your domain-types.ts
│   ├── ValidationTypes.ts                       # Validation contracts
│   ├── SharedTokens.ts                          # Common DI tokens
│   └── index.ts
│
└── index.ts                                     # Root barrel (domain exports only)
```

---

## TKA-Specific Migration Strategy

### 🔄 **Phase-by-Phase Implementation**

**Phase 1: Foundation (Week 1)**

1. Create new `/contracts` directory structure
2. Move `core-types.ts` → `shared/CoreTypes.ts`
3. Move `domain-types.ts` → `shared/DomainTypes.ts`
4. Create domain token files from your 183-line `types.ts`

**Phase 2: Simple Domains First (Week 2)** 5. **Device domain**: Move `IDeviceDetectionService` (simplest - only 1 service) 6. **Application domain**: Move `IApplicationInitializationService`, `ISettingsService` 7. **Infrastructure/persistence**: Move `IPersistenceService`, `IFilterPersistenceService`

**Phase 3: Core Business Domains (Week 3-4)** 8. **Browse domain**: Move all browse interfaces (clean separation) 9. **Sequence domain**: Move sequence interfaces (split page layout to export) 10. **Navigation domain**: Move `INavigationService`, `IPanelManagementService`

**Phase 4: Complex Domains (Week 5-6)** 11. **Positioning domain**: Move positioning interfaces (handle subdirectories) 12. **Pictograph domain**: Move pictograph interfaces (large file) 13. **Animation domain**: Create new domain for animation services 14. **Motion domain**: Create new domain for motion services

**Phase 5: Most Complex Domain (Week 7-8)** 15. **Export domain**: Break apart mega `image-export-interfaces.ts` 16. **Beat-frame domain**: Create new domain for beat services 17. **Codex domain**: Create new domain for codex services

**Phase 6: Integration & Cleanup (Week 9)** 18. Update all imports throughout codebase 19. Update InversifyJS container registration to use new tokens 20. Remove old `/interfaces` folder 21. Update build configuration and path mappings

---

## Key Benefits for TKA

### ✅ **Immediate Improvements**

**Developer Experience**:

- **Find interfaces by business domain**: "I need sequence services" → `contracts/domain/sequence/`
- **Smaller, focused files**: No more 258-line barrel exports
- **Clear service ownership**: Each domain team owns their contracts

**Maintainability**:

- **Easier InversifyJS updates**: Domain-specific token files
- **Better testing**: Mock domain services independently
- **Cleaner dependencies**: Separation of business vs infrastructure

**Svelte Integration**:

- **Cleaner component imports**: `import type { ISequenceService } from '@contracts/sequence'`
- **Better intellisense**: Domain-grouped types
- **Reduced bundle size**: Import only needed contracts

### 🛠️ **Technical Implementation Notes**

**InversifyJS Container Updates**:

```typescript
// New container.ts structure
import { SEQUENCE_TOKENS } from "@contracts/domain/sequence";
import { EXPORT_TOKENS } from "@contracts/domain/export";
import { BROWSE_TOKENS } from "@contracts/domain/browse";

// Instead of your current 183-line TYPES object
container.bind(SEQUENCE_TOKENS.ISequenceService).to(SequenceService);
container.bind(EXPORT_TOKENS.ITKAImageExportService).to(TKAImageExportService);
```

**Path Mapping Updates** (tsconfig.json):

```json
{
  "compilerOptions": {
    "paths": {
      "@contracts/*": ["src/lib/contracts/*"],
      "@contracts/sequence": ["src/lib/contracts/domain/sequence"],
      "@contracts/export": ["src/lib/contracts/domain/export"]
    }
  }
}
```

This organization transforms your interface chaos into a clean, domain-driven contract system that scales with your TKA application complexity.
