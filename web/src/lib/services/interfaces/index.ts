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
  Coordinates,
  GridPoint,
  GridData,
  ArrowPosition,
  LegacyArrowData,
  ArrowPlacementConfig,
  PropData,
  PropPosition,
  HandRotDir,
  GridMode,
  DifficultyLevel,
  OptionFilters,
  ServiceInterface,
} from "./core-types";

export { defineService } from "./core-types";

// Domain types
export type {
  ArrowData,
  BeatData,
  MotionData,
  PictographData,
  SequenceData,
  BrowseDisplayState,
  BrowseLoadingState,
  BrowseSequenceMetadata,
  FilterType,
  FilterValue,
  SortMethod,
  LayoutConfig,
  ExportOptions,
  SequenceCardExportSettings,
  DeviceCapabilities,
  PrintLayoutOptions,
  CacheEntry,
  CacheConfig,
  ProgressInfo,
  ValidationResult,
  MotionType,
  Location,
  Orientation,
  RotationDirection,
} from "./domain-types";

// ============================================================================
// APPLICATION INTERFACES
// ============================================================================

export type {
  AppSettings,
  IApplicationInitializationService,
  ISettingsService,
  IConstructTabCoordinationService,
  IOptionDataService,
  IStartPositionService,
} from "./application-interfaces";

// ============================================================================
// SEQUENCE INTERFACES
// ============================================================================

export type {
  ISequenceService,
  ISequenceDomainService,
  IPersistenceService,
  SequenceCreateRequest,
} from "./sequence-interfaces";

// ============================================================================
// PICTOGRAPH INTERFACES
// ============================================================================

export type {
  ISvgConfiguration,
  IPictographService,
  IPictographRenderingService,
  ISvgUtilityService,
  IGridRenderingService,
  IArrowRenderingService,
  IOverlayRenderingService,
  IDataTransformationService,
} from "./pictograph-interfaces";

// ============================================================================
// POSITIONING INTERFACES
// ============================================================================

export type {
  IArrowPlacementDataService,
  IArrowPlacementKeyService,
  IPropRenderingService,
} from "./positioning-interfaces";

// Export orchestrator from positioning services
export type { IArrowPositioningOrchestrator } from "../positioning/core-services";

// ============================================================================
// GENERATION INTERFACES
// ============================================================================

export type {
  GenerationOptions,
  ISequenceGenerationService,
  IMotionGenerationService,
} from "./generation-interfaces";

// ============================================================================
// BROWSE INTERFACES
// ============================================================================

export type {
  IDeleteService,
  IFavoritesService,
  IFilterPersistenceService,
  INavigationService,
  ISectionService,
  IBrowseService,
  ISequenceIndexService,
  IThumbnailService,
  DeleteConfirmationData,
  DeleteResult,
  FilterState,
  BrowseState,
  NavigationItem,
  NavigationSection,
  SectionConfiguration,
  SequenceSection,
} from "./browse-interfaces";

// ============================================================================
// DEVICE INTERFACES
// ============================================================================

export type {
  ResponsiveSettings,
  IDeviceDetectionService,
} from "./device-interfaces";

// ============================================================================
// EXPORT INTERFACES
// ============================================================================

export type {
  IExportService,
  ISequenceCardImageService,
  ISequenceCardLayoutService,
  ISequenceCardPageService,
  ISequenceCardBatchService,
  ISequenceCardCacheService,
  IEnhancedExportService,
} from "./export-interfaces";

// ============================================================================
// TKA IMAGE EXPORT INTERFACES
// ============================================================================

export type {
  TKAImageExportOptions,
  BeatRenderOptions,
  TextRenderOptions,
  CompositionOptions,
  UserInfo,
  LayoutData,
  ITKAImageExportService,
  ILayoutCalculationService,
  IBeatRenderingService,
  ITextRenderingService,
  IImageCompositionService,
  IFileExportService,
  IDimensionCalculationService,
  IGridOverlayService,
  IReversalDetectionService,
  IFontManagementService,
  ICanvasManagementService,
  IExportSettingsService,
  ExportProgress,
  ExportError,
  ExportResult,
  RenderQualitySettings,
  LayoutConstraints,
} from "./image-export-interfaces";

export {
  ITKAImageExportServiceInterface,
  ILayoutCalculationServiceInterface,
  IBeatRenderingServiceInterface,
  ITextRenderingServiceInterface,
  IImageCompositionServiceInterface,
  IFileExportServiceInterface,
  IDimensionCalculationServiceInterface,
  IGridOverlayServiceInterface,
  IReversalDetectionServiceInterface,
  IFontManagementServiceInterface,
  ICanvasManagementServiceInterface,
  IExportSettingsServiceInterface,
} from "./image-export-interfaces";

// ============================================================================
// PANEL INTERFACES
// ============================================================================

export type {
  IPanelManagementService,
  PanelState,
  PanelConfiguration,
  ResizeOperation,
  ResizeDirection,
} from "./panel-interfaces";
