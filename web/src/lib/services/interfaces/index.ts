/**
 * Interfaces Barrel Export
 *
 * Central export point for all service interfaces.
 * This provides a clean API for importing service interfaces throughout the application.
 */

// ============================================================================
// CORE TYPES AND DOMAIN MODELS
// ============================================================================

// Core types
export type {
  ArrowPlacementConfig,
  Coordinates,
  DifficultyLevel,
  GridData,
  GridMode,
  GridPoint,
  HandRotDir,
  LegacyArrowData,
  OptionFilters,
  PropPlacementData,
  PropPosition,
  ServiceInterface,
} from "./core-types";

// ArrowPosition is now exported from positioning/types.ts
export type { ArrowPosition } from "../positioning/types";

export { defineService } from "./core-types";

// Domain types
export type {
  ArrowPlacementData,
  BeatData,
  BrowseDisplayState,
  BrowseLoadingState,
  CacheConfig,
  CacheEntry,
  DeviceCapabilities,
  ExportOptions,
  ExportResult,
  FilterType,
  FilterValue,
  LayoutConfig,
  Location,
  MotionData,
  MotionType,
  Orientation,
  PictographData,
  PrintLayoutOptions,
  ProgressInfo,
  RotationDirection,
  SequenceCardExportSettings,
  SequenceData,
  SortMethod,
  ValidationResult,
} from "./domain-types";

// ============================================================================
// APPLICATION INTERFACES
// ============================================================================

export type {
  AppSettings,
  IConstructTabCoordinationService,
  IOptionDataService,
  ISettingsService,
  IStartPositionService,
} from "./application-interfaces";
export type { IApplicationInitializationService } from "./application/IApplicationInitializationService";

// ============================================================================
// SEQUENCE INTERFACES
// ============================================================================

export type {
  IPersistenceService,
  ISequenceDomainService,
  ISequenceService,
  SequenceCreateRequest,
} from "./sequence-interfaces";

// ============================================================================
// PICTOGRAPH INTERFACES
// ============================================================================

export type {
  ArrowSvgData,
  IArrowPathResolutionService,
  IArrowPositioningService,
  IArrowRenderingService,
  IDataTransformationService,
  IFallbackArrowService,
  IGridRenderingService,
  IOverlayRenderingService,
  ISvgColorTransformationService,
  ISvgConfiguration,
  ISvgLoadingService,
  ISvgParsingService,
  ISvgUtilityService,
  SVGDimensions,
} from "./pictograph-interfaces";

// ============================================================================
// POSITIONING INTERFACES
// ============================================================================

export type {
  IArrowAdjustmentCalculator,
  IArrowAdjustmentLookup,
  IArrowCoordinateSystemService,
  IArrowLocationCalculator,
  IArrowPlacementKeyService,
  IArrowPlacementService,
  IArrowPositioningOrchestrator,
  IArrowRotationCalculator,
  IAttributeKeyGenerator,
  IBetaOffsetCalculator,
  IDashLocationCalculator,
  IDefaultPlacementService,
  IDefaultPlacementServiceJson,
  IDirectionalTupleCalculator,
  IDirectionalTupleProcessor,
  IGridModeDeriver,
  IPlacementKeyGenerator,
  IPositionMapper,
  IPropRenderingService,
  IQuadrantIndexCalculator,
  ISpecialPlacementOriKeyGenerator,
  ISpecialPlacementService,
  ITurnsTupleKeyGenerator,
  Point,
  Position,
} from "./positioning-interfaces";

// Note: IArrowPositioningOrchestrator is now exported with other positioning interfaces below

// ============================================================================
// GENERATION INTERFACES
// ============================================================================

export type {
  GenerationOptions,
  IMotionGenerationService,
  ISequenceGenerationService,
} from "./generation-interfaces";

// ============================================================================
// BROWSE INTERFACES
// ============================================================================

export type {
  BrowseState,
  DeleteConfirmationData,
  DeleteResult,
  FilterState,
  IBrowseService,
  IDeleteService,
  IFavoritesService,
  IFilterPersistenceService,
  INavigationService,
  ISectionService,
  ISequenceIndexService,
  IThumbnailService,
  NavigationItem,
  NavigationSection,
  SectionConfiguration,
  SequenceSection,
} from "./browse-interfaces";

// ============================================================================
// DEVICE INTERFACES
// ============================================================================

export type {
  IDeviceDetectionService,
  ResponsiveSettings,
} from "./application/IDeviceDetectionService";

// ============================================================================
// EXPORT INTERFACES
// ============================================================================

export type {
  IEnhancedExportService,
  IExportService,
  ISequenceCardBatchService,
  ISequenceCardCacheService,
  ISequenceCardImageService,
  ISequenceCardLayoutService,
  ISequenceCardPageService,
} from "./export-interfaces";

// ============================================================================
// TKA IMAGE EXPORT INTERFACES
// ============================================================================

export type {
  BeatRenderOptions,
  CompositionOptions,
  ExportError,
  ExportProgress,
  ExportValidationResult,
  IBeatRenderingService,
  ICanvasManagementService,
  IDimensionCalculationService,
  IExportConfigurationManager,
  IExportMemoryCalculator,
  IExportOptionsValidator,
  IExportSettingsService,
  IFileExportService,
  IFilenameGeneratorService,
  IFontManagementService,
  IGridOverlayService,
  IImageCompositionService,
  IImagePreviewGenerator,
  ILayoutCalculationService,
  IReversalDetectionService,
  ITKAImageExportService,
  ITextRenderingService,
  LayoutConstraints,
  LayoutData,
  MemoryEstimate,
  RenderQualitySettings,
  TKAImageExportOptions,
  TextRenderOptions,
  UserInfo,
} from "./image-export-interfaces";

// Text rendering component interfaces
export type {
  IDifficultyBadgeRenderer,
  ITextRenderingUtils,
  IUserInfoRenderer,
  IWordTextRenderer,
} from "./text-rendering-interfaces";

export {
  IBeatRenderingServiceInterface,
  ICanvasManagementServiceInterface,
  IDimensionCalculationServiceInterface,
  IExportConfigurationManagerInterface,
  IExportMemoryCalculatorInterface,
  IExportOptionsValidatorInterface,
  IExportSettingsServiceInterface,
  IFileExportServiceInterface,
  IFilenameGeneratorServiceInterface,
  IFontManagementServiceInterface,
  IGridOverlayServiceInterface,
  IImageCompositionServiceInterface,
  IImagePreviewGeneratorInterface,
  ILayoutCalculationServiceInterface,
  IReversalDetectionServiceInterface,
  ITKAImageExportServiceInterface,
  ITextRenderingServiceInterface,
} from "./image-export-interfaces";

// Text rendering component DI interfaces
export {
  IDifficultyBadgeRendererInterface,
  ITextRenderingUtilsInterface,
  IUserInfoRendererInterface,
  IWordTextRendererInterface,
} from "./image-export-interfaces";

// ============================================================================
// PANEL INTERFACES
// ============================================================================

export type {
  IPanelManagementService,
  PanelConfiguration,
  PanelState,
  ResizeDirection,
  ResizeOperation,
} from "./panel-interfaces";

// ============================================================================
// METADATA TESTING INTERFACES
// ============================================================================

export type {
  IBatchAnalysisService,
  IMetadataAnalysisService,
  IMetadataExtractionService,
  ISequenceDiscoveryService,
} from "./metadata-testing-interfaces";

// ============================================================================
// OPTION PICKER INTERFACES
// ============================================================================

export type {
  IOptionPickerDataService,
  IOptionPickerLayoutService,
  OptionPickerGridConfiguration,
  OptionPickerLayoutCalculationParams,
  OptionPickerLayoutCalculationResult,
  OptionPickerLayoutDimensions,
} from "./option-picker-interfaces";
