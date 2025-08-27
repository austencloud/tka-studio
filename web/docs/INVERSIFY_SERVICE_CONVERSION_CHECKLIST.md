# InversifyJS Service Conversion Checklist

## 🎯 **CONVERSION STRATEGY**

**Priority Order:**

1. **Zero Dependencies** - Services with no dependencies (easiest)
2. **Minimal Dependencies** - Services with 1-2 simple dependencies
3. **Medium Dependencies** - Services with 3-5 dependencies
4. **Complex Dependencies** - Services with 6+ dependencies or circular refs

---

## ✅ **PHASE 1: ZERO DEPENDENCIES (Start Here)**

### **Application Services**

- [x] **SettingsService** ✅ **COMPLETED** - Zero dependencies, perfect first conversion
- [x] **DeviceDetectionService** ✅ **COMPLETED** - Zero dependencies, browser detection
- [x] **ApplicationInitializationService** ✅ **COMPLETED** - Minimal dependencies (ISettingsService, IPersistenceService)

### **Data Services**

- [x] **EnumMappingService** ✅ **COMPLETED** - Zero dependencies, enum utilities
- [x] **CSVParserService** ✅ **COMPLETED** - Zero dependencies, CSV parsing
- [x] **DataTransformationService** ✅ **COMPLETED** - Zero dependencies, data transformation
- [x] **CsvLoaderService** ✅ **COMPLETED** - Zero dependencies, CSV loading
- [ ] **LetterQueryService** - ❌ **HAS DEPENDENCIES** - letter lookup (needs ILetterMappingRepository, ICsvLoaderService, etc.)
- [ ] **MotionQueryService** - ❌ **HAS DEPENDENCIES** - motion lookup (needs dependencies)

### **Domain Services**

- [x] **GridModeDeriver** ✅ **COMPLETED** - Zero dependencies, grid mode logic
- [x] **LetterDeriver** ✅ **COMPLETED** - Zero dependencies, letter derivation
- [x] **PictographValidatorService** ✅ **COMPLETED** - Zero dependencies, validation logic
- [x] **PositionPatternService** ✅ **COMPLETED** - Zero dependencies, position patterns

### **Utility Services**

- [x] **SvgConfiguration** ✅ **COMPLETED** - Zero dependencies, SVG config
- [x] **FilenameGeneratorService** ✅ **COMPLETED** - Zero dependencies, filename generation
- [ ] **ExportOptionsValidator** - ❌ **HAS DEPENDENCIES** - validation (needs IExportMemoryCalculator)

---

## 🟡 **PHASE 2: MINIMAL DEPENDENCIES (1-2 deps)**

### **Persistence Services**

- [x] **LocalStoragePersistenceService** ✅ **COMPLETED** - Implements IPersistenceService
- [x] **FilterPersistenceService** ✅ **COMPLETED** - Zero dependencies, filter state persistence

### **Domain Services**

- [x] **SequenceDomainService** ✅ **COMPLETED** - Zero dependencies (business logic)
- [x] **StartPositionService** ✅ **COMPLETED** - Zero dependencies (position management)

### **Rendering Utilities**

- [x] **SvgUtilityService** ✅ **COMPLETED** - Depends on SvgConfiguration (with @inject decorator)
- [x] **GridRenderingService** ✅ **COMPLETED** - Depends on SvgConfiguration (with @inject decorator)
- [x] **ArrowRenderingService** ✅ **COMPLETED** - Depends on SvgConfiguration (with @inject decorator)
- [x] **OverlayRenderingService** ✅ **COMPLETED** - Depends on SvgConfiguration (with @inject decorator)

### **Export Services**

- [x] **ExportConfigurationManager** ✅ **COMPLETED** - Minimal dependencies
- [x] **ExportMemoryCalculator** ✅ **COMPLETED** - Minimal dependencies
- [x] **DimensionCalculationService** ✅ **COMPLETED** - Zero dependencies, SSR issues resolved!
- [x] **LayoutCalculationService** ✅ **COMPLETED** - Minimal dependencies
- [x] **ExportOptionsValidator** ✅ **COMPLETED** - Depends on IExportMemoryCalculator

### **Positioning Services**

- [x] **ArrowAdjustmentCalculator** ✅ **COMPLETED** - Depends on GridModeDeriver (with dynamic value)
- [x] **ArrowPositioningService** ✅ **COMPLETED** - Minimal dependencies

### **Layout Services**

- [x] **BeatGridService** ✅ **COMPLETED** - Minimal dependencies

---

## 🟠 **PHASE 3: MEDIUM DEPENDENCIES (3-5 deps)**

### **Core Business Logic**

- [ ] **SequenceService** - Depends on domain + persistence services
- [ ] **SequenceStateService** - Depends on sequence + persistence services
- [ ] **SequenceImportService** - Depends on sequence + validation services
- [ ] **SequenceDeletionService** - Depends on sequence + persistence services

### **Browse Services**

- [x] **BrowseService** ✅ **COMPLETED** - Zero dependencies, pure business logic service
- [x] **ThumbnailService** ✅ **COMPLETED** - Zero dependencies, thumbnail loading and caching
- [ ] **SequenceIndexService** - ❌ **FILE NOT FOUND** - sequence indexing
- [x] **FavoritesService** ✅ **COMPLETED** - Zero dependencies, favorites management
- [x] **NavigationService** ✅ **COMPLETED** - Zero dependencies, navigation state
- [ ] **SectionService** - ❌ **FILE NOT FOUND** - section management
- [ ] **DeleteService** - ❌ **FILE NOT FOUND** - deletion operations

### **Positioning Services (REMAINING)**

- [ ] **ArrowLocationService** - Depends on positioning utilities
- [ ] **ArrowPlacementKeyService** - Depends on positioning services
- [ ] **BetaOffsetCalculator** - Depends on positioning services
- [ ] **BetaPropDirectionCalculator** - Depends on positioning services
- [ ] **PropPlacementService** - Depends on positioning services
- [x] **PositionMapper** ✅ **COMPLETED** - Zero dependencies, pure position mapping logic

### **Generation Services**

- [ ] **PictographGenerator** - Depends on domain + positioning services
- [ ] **SequenceGenerationService** - Depends on generation + domain services
- [ ] **OrientationCalculationService** - Depends on positioning services
- [ ] **PageFactoryService** - Depends on rendering services

### **Layout Services**

- [x] **BeatFrameService** ✅ **COMPLETED** - Zero dependencies, pure business logic service
- [ ] **SimpleBeatGridService** - ❌ **STILL IN CUSTOM DI** - Depends on rendering services
- [x] **BeatFallbackRenderingService** ✅ **COMPLETED** - Zero dependencies, pure fallback rendering

---

## 🔴 **PHASE 4: COMPLEX DEPENDENCIES (6+ deps or circular)**

### **Main Orchestrators**

- [ ] **PictographRenderingService** - **7 dependencies** (most complex!)
  - ArrowPositioningOrchestrator
  - SvgUtilityService
  - GridRenderingService
  - ArrowRenderingService
  - OverlayRenderingService
  - DataTransformationService
  - PropRenderingService (nullable)

- [ ] **ArrowPositioningOrchestrator** - Complex positioning logic
- [ ] **PropCoordinatorService** - Complex prop coordination

### **Workbench Services**

- [ ] **WorkbenchService** - Complex workbench orchestration
- [ ] **WorkbenchCoordinationService** - Complex coordination logic
- [ ] **WorkbenchBeatOperationsService** - Complex beat operations

### **Image Export Services**

- [ ] **TKAImageExportService** - Complex export orchestration
- [ ] **TKAImageExportOrchestrator** - Main export orchestrator
- [ ] **ImageCompositionService** - Complex image composition
- [ ] **BeatRenderingService** - Complex beat rendering
- [ ] **CanvasManagementService** - Complex canvas management
- [ ] **ImagePreviewGenerator** - Complex preview generation
- [ ] **GridOverlayService** - Complex grid overlay
- [ ] **TextRenderingService** - Complex text rendering
- [ ] **FileExportService** - Complex file export

### **Advanced Services**

- [ ] **ConstructTabCoordinationService** - Complex tab coordination
- [ ] **PanelManagementService** - Complex panel management

---

Alexa Music All right here's Spotify Why are you so loud Alexa lower the volume Alexa lower the volume ## 📊 **CONVERSION STATISTICS**

- **Total Services**: ~90 services
- **Zero Dependencies**: ~15 services (17%)
- **Minimal Dependencies**: ~25 services (28%)
- **Medium Dependencies**: ~35 services (39%)
- **Complex Dependencies**: ~15 services (17%)

**✅ COMPLETED**: 53/90 (58.9%)
**🔄 REMAINING**: 37/90 (41.1%)

### **✅ SUCCESSFULLY MIGRATED TO INVERSIFYJS (53 services)**

1. SettingsService
2. EnumMappingService
3. CSVParserService
4. DataTransformationService
5. GridModeDeriver
6. LetterDeriver
7. PictographValidatorService
8. PositionPatternService
9. SvgConfiguration
10. FilenameGeneratorService
11. SvgUtilityService
12. GridRenderingService
13. ArrowRenderingService
14. OverlayRenderingService
15. LocalStoragePersistenceService
16. SequenceDomainService
17. StartPositionService
18. ArrowAdjustmentCalculator
19. FilterPersistenceService
20. DeviceDetectionService
21. ExportMemoryCalculator
22. CsvLoaderService
23. BeatGridService
24. ExportConfigurationManager
25. LayoutCalculationService
26. ArrowPositioningService
27. DimensionCalculationService
28. ApplicationInitializationService
29. ExportOptionsValidator
30. BeatFrameService
31. BeatFallbackRenderingService
32. PositionMapper
33. SequenceImportService
34. ThumbnailService
35. NavigationService
36. BrowseService
37. FavoritesService
38. PanelManagementService
39. SectionService
40. SequenceIndexService
41. DeleteService
42. SequenceStateService
43. WorkbenchService
44. WorkbenchCoordinationService
45. StartPositionSelectionService
46. GridRenderingService
47. ArrowRenderingService
48. OverlayRenderingService
49. PropCoordinatorService
50. ExportService
51. FilterPersistenceService
52. PictographRenderingService

---

## 🎯 **NEXT RECOMMENDED CONVERSIONS**

**Priority: Focus on remaining zero-dependency services first**

1. **ApplicationInitializationService** - Zero dependencies, application startup
2. **ExportOptionsValidator** - Check dependencies first
3. **DimensionCalculationService** - Fix SSR issues, then convert
4. **LetterQueryService** - Has dependencies, convert after dependencies ready
5. **MotionQueryService** - Has dependencies, convert after dependencies ready

**Next Phase: Services still in Custom DI that could be converted**

- **BeatFrameService** - Check current dependencies
- **SimpleBeatGridService** - Check current dependencies
- **BeatFallbackRenderingService** - Check current dependencies
- **PositionMapper** - Currently in custom DI, needs dependency analysis

---

## 📝 **CONVERSION NOTES**

- **Start with zero dependencies** to build confidence
- **Work bottom-up** - convert dependencies before dependents
- **Test each conversion** before moving to the next
- **Update this checklist** as services are completed
- **Watch for circular dependencies** in complex services

**Current Focus: Complete remaining zero-dependency services, then tackle services with resolved dependencies**

## 🔄 **MIGRATION STATUS SUMMARY**

**✅ MAJOR PROGRESS**: 37/90 services (41.1%) successfully migrated to InversifyJS
**🎯 CURRENT PHASE**: Converting remaining zero-dependency services and tackling services with resolved dependencies
**⚠️ BLOCKERS**:

- Some services still registered in both systems during transition
- Circular dependencies in positioning services need careful handling

**🚀 NEXT STEPS**:

1. ✅ **COMPLETED**: Fix DimensionCalculationService SSR issues
2. ✅ **COMPLETED**: Convert ApplicationInitializationService with dependencies
3. Convert remaining services (ExportOptionsValidator, services still in custom DI)
4. Remove dual registrations once migration is complete
