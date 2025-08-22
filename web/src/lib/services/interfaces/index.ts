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
  IApplicationInitializationService,
  IConstructTabCoordinationService,
  IOptionDataService,
  ISettingsService,
  IStartPositionService,
} from "./application-interfaces";

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
  IPictographRenderingService,
  IPictographService,
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
  IArrowPlacementKeyService,
  IArrowPlacementService,
  IPropRenderingService,
} from "./positioning-interfaces";

// Export orchestrator from positioning services
export type { IArrowPositioningOrchestrator } from "../positioning/core-services";

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
} from "./device-interfaces";

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
  IBeatRenderingService,
  ICanvasManagementService,
  IDimensionCalculationService,
  IExportSettingsService,
  IFileExportService,
  IFontManagementService,
  IGridOverlayService,
  IImageCompositionService,
  ILayoutCalculationService,
  IReversalDetectionService,
  ITextRenderingService,
  ITKAImageExportService,
  LayoutConstraints,
  LayoutData,
  RenderQualitySettings,
  TextRenderOptions,
  TKAImageExportOptions,
  UserInfo,
} from "./image-export-interfaces";

export {
  IBeatRenderingServiceInterface,
  ICanvasManagementServiceInterface,
  IDimensionCalculationServiceInterface,
  IExportSettingsServiceInterface,
  IFileExportServiceInterface,
  IFontManagementServiceInterface,
  IGridOverlayServiceInterface,
  IImageCompositionServiceInterface,
  ILayoutCalculationServiceInterface,
  IReversalDetectionServiceInterface,
  ITextRenderingServiceInterface,
  ITKAImageExportServiceInterface,
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
