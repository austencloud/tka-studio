// Core models - direct exports from new locations
export * from "./build/models/workbench/BeatData";
export * from "./core/enums/Letter";
export * from "./core/models/application/ApplicationTypes";
export * from "./core/models/device-recognition/DeviceTypes";
export * from "./core/models/pictograph/GridData";
export * from "./core/models/pictograph/MotionData";
export * from "./core/models/pictograph/PictographData";
export * from "./core/models/sequence/SequenceData";
export type {
  ExportResult,
  ValidationError,
  ValidationResult,
} from "./word-cards/models/WordCard";

// Export factory functions (non-conflicting)
export { createBeatData } from "./build/models/workbench/BeatData";

// Core domain exports (specific to avoid conflicts)
export * from "./core/AppSettings";
export * from "./core/enums/Letter";
export * from "./core/ui";
// export * from "./core/models/application/ApplicationTypes"; // Already exported via core/index.ts
export * from "./core/models/csv-handling/CsvModels";
export * from "./core/models/device-recognition/DeviceTypes";

// Pictograph exports (specific to avoid conflicts)
export * from "./core/models/pictograph/ArrowPlacementData";
export * from "./core/models/pictograph/gridCoordinates";
export * from "./core/models/pictograph/GridData";
export * from "./core/models/pictograph/LetterBorderUtils";
export * from "./core/models/pictograph/MotionData";
export * from "./core/models/pictograph/PictographData";
export * from "./core/models/pictograph/PositioningModels";
export * from "./core/models/pictograph/PropPlacementData";
export * from "./core/models/pictograph/SvgTypes";

// Enum exports (specific to avoid conflicts)
export * from "./core/enums/enums";

// Export build types from new locations
export type {
  GenerationOptions,
  LetterDerivationResult,
} from "./build/models/generate/GenerateModels";

export type {
  LayoutCalculationParams,
  OptionPickerLayoutCalculationResult,
  ResponsiveLayoutConfig,
} from "./build/models/construct/OptionPicker";

// Note: LayoutCalculationResult now exported from word-card-models (the correct version)

export type {
  BeatClickResult,
  BeatEditOperation,
  BeatEditResult,
  SequenceCreationParams,
  SequenceCreationResult,
  WorkbenchActions,
  WorkbenchConfig,
  WorkbenchState,
} from "./build/models/workbench/WorkbenchModels";

export type { WorkbenchMode } from "./build/types/WorkbenchTypes";

// Export beat frame types
export * from "./build/models/workbench/BeatFrame";

// Export sequence operations types
export * from "./build/models/workbench/SequenceOperations";

// Export workbench types
export * from "./build/types/WorkbenchTypes";

// Export image export types
export type {
  BeatRenderOptions,
  CompositionOptions,
  ExportError,
  ExportProgress,
  SequenceExportOptions as ImageExportOptions,
  LayoutData,
  TextRenderOptions,
  UserInfo,
} from "./build/models/export/SequenceExportOptions";

// Export image format types
export type {
  ImageFormatOptions,
  OptimizationSettings,
} from "./build/models/export/ImageFormat";

// Export panel management types (browse-specific)
export type {
  BrowsePanelConfig as BrowsePanelConfig,
  BrowsePanelState as BrowsePanelState,
  ResizeOperation,
  SplitterConfig,
} from "./browse/models/PanelManagement";

// Export option picker layout types (build/construct-specific)
export type {
  OptionPickerGridConfiguration,
  OptionPickerLayoutCalculationParams,
  OptionPickerLayoutDimensions,
} from "./build/models/construct/OptionPickerLayout";

// Export page layout types (word-card-specific)
export type {
  DPIConfiguration,
  GridConfig,
  LayoutValidationResult,
  Margins,
  PageDimensions,
  LayoutCalculationResult as PageLayoutCalculationResult,
  Rectangle,
} from "./word-cards/models/PageLayout";

// Export the correct GridCalculationOptions and related types from sequence-card-models
export type {
  GridCalculationOptions,
  LayoutCalculationRequest,
  LayoutCalculationResult,
  Page,
  PageCreationOptions,
  PageLayoutConfig,
  SequenceCardGridConfig,
} from "./word-cards/models/word-card-models";

// Export word-card types except conflicting ones
// Export word card types directly (no intermediate exports)
export type {
  CacheConfig,
  CacheEntry,
  DeviceCapabilities,
  ExportOptions,
  ProgressInfo,
  ProgressStage,
  ResponsiveSettings,
  SequenceCardExportSettings,
} from "./word-cards/models/WordCard";

export type {
  OptimizationGoal,
  PageOrientation,
  SequenceCardLayoutMode,
} from "./word-cards/types/PageLayoutTypes";

export * from "./word-cards/models/PageLayoutConstants";
export * from "./word-cards/models/word-card-models";
export * from "./word-cards/models/WordCardExport";

// Export additional word-card types
export type {
  GridLayout,
  LayoutRecommendation,
} from "./word-cards/models/word-card-models";

// Export word card export types
export type {
  BatchExportOptions,
  BatchExportResult,
  // ImageExportOptions, // Already exported above as TKAImageExportOptions alias
  PDFExportOptions,
} from "./word-cards/models/export-config";

// Export browse types directly (no intermediate exports)
export {
  createFilterConfig,
  formatFilterDisplayName,
  isMultiValueFilter,
  isRangeFilter,
} from "./browse/models/BrowseFilters";

export {
  createCustomSortConfig,
  getAvailableSortConfigs,
  getAvailableSortMethods,
  getSortConfig,
  getSortDisplayName,
  SORT_CONFIGS,
} from "./browse/models/BrowseSorting";

export {
  createDefaultBrowseState,
  createDefaultDisplayState,
  createDefaultLoadingState,
  NavigationMode,
  updateBrowseState,
} from "./browse/models/BrowseState";

export * from "./browse/models/Metadata";

export type { FilterConfig } from "./browse/models/FilterModels";
export type { SortConfig } from "./browse/models/SortModels";
export type { FilterValue, SortDirection } from "./browse/types/BrowseTypes";

export type {
  BrowseDisplayState,
  BrowseLoadingState,
  BrowseState,
  SequenceFilterResult,
} from "./browse/models/BrowseState";

export type {
  BrowseConfig,
  BrowseDeleteConfirmationData,
  BrowseDeleteResult,
  BrowseResult,
  FilterOption,
  FilterState,
  NavigationItem,
  NavigationSection,
  SearchCriteria,
  SectionConfiguration,
  SequenceSection,
  SortOption,
} from "./browse/models/BrowseModels";

export type {
  FavoriteItem,
  FavoritesCollection,
} from "./browse/models/FavoritesModels";

export type {
  AnimationConfig,
  AnimationState,
} from "./animator/models/AnimationModels";

export type { PropState } from "./animator/types/PropState";

export type {
  BeatOperationResult,
  SequenceStatistics,
  SequenceTransformOptions,
} from "./browse/models/SequenceState";

// Background types will be added when the actual files are found

// Export pictograph types (only what actually exists)
// PictographData and createPictographData are already exported above

// Export positioning types (what actually exists)
export type { Point } from "./core/models/pictograph/PositioningModels";

// AppSettings doesn't exist yet

// Schema types don't exist in domain yet

// Export learn/codex domain types
export type {
  LetterCategory,
  PictographTransformOperation,
} from "./learn/types/CodexTypes";

export type {
  CodexConfiguration,
  CodexLetter,
  LessonConfiguration,
  LetterMapping,
  LetterRow,
} from "./learn/models/CodexModels";

// Export learn types and enums
export * from "./learn/types/learn";

// Export factory functions
export {
  createCodexLetter,
  createLetterMapping,
  createLetterRow,
} from "./learn/models/CodexModels";

// Export workbench types
export type { ConfigurationResult } from "./build/models/workbench/WorkbenchModels";

// Export option picker utility functions
export {
  getContainerAspect,
  getDeviceConfig,
  getDeviceType,
} from "./build/models/construct/OptionPickerUtils";

// ResizeDirection is already exported from enums above

// Export additional option picker layout types
export type { DeviceConfig } from "./build/models/construct/OptionPickerLayoutModels";

// Export service interfaces (needed by some files)
export type { ILessonRepository } from "../services/contracts/learn/ILessonRepository";
export type { ILetterMappingRepository } from "../services/contracts/learn/ILetterMappingRepository";

// Export SVG conversion types
export type {
  RenderQualitySettings,
  SVGConversionOptions,
} from "./core/models/rendering/SvgConversion";

// Export grid types (including beat grid types)
export type {
  CombinedGridOptions,
  GridDrawOptions,
  GridValidationResult,
} from "./core/models/pictograph/GridData";

// Export schema types
export { PngMetadataArraySchema, SequenceDataSchema } from "./schemas";

// Export memory estimation types
export interface MemoryEstimate {
  estimatedMB: number;
  safe: boolean;
}

// Export word card types
export type { SequenceCardPaperSize } from "./word-cards/types/PageLayoutTypes";

// Export word-cards/write types (excluding SequenceData to avoid conflict)
export {
  createDefaultMusicPlayerState,
  createEmptyAct,
  formatTime,
  generateActThumbnail,
  generateSequenceThumbnail,
} from "./word-cards/types/write";
export type {
  ActData,
  ActThumbnailInfo,
  MusicPlayerState,
} from "./word-cards/types/write";

// Export HTML2Canvas types
export interface Html2CanvasFunction {
  (
    element: HTMLElement,
    options?: Record<string, unknown>
  ): Promise<HTMLCanvasElement>;
}

export interface WindowWithHtml2Canvas extends Window {
  html2canvas: Html2CanvasFunction;
}
