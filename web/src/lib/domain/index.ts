// Core models - direct exports
export * from "./enums/Letter";
export * from "./models/build/workbench/BeatData";
export * from "./models/core/application/ApplicationTypes";
export * from "./models/core/device-recognition/DeviceTypes";
export * from "./models/core/pictograph/GridData";
export * from "./models/core/pictograph/MotionData";
export * from "./models/core/pictograph/PictographData";
export * from "./models/core/sequence/SequenceData";
export type {
  ExportResult,
  ValidationError,
  ValidationResult,
} from "./models/sequence-card/SequenceCard";

// Export factory functions (non-conflicting)
export { createBeatData } from "./models/build/workbench/BeatData";

// Core domain exports (specific to avoid conflicts)
export * from "./core/AppSettings";
export * from "./core/ui";
export * from "./enums/Letter";
export * from "./models/core/application/ApplicationTypes";
export * from "./models/core/csv-handling/CsvModels";
export * from "./models/core/device-recognition/DeviceTypes";

// Pictograph exports (specific to avoid conflicts)
export * from "./core/pictograph/ArrowPlacementData";
export * from "./core/pictograph/gridCoordinates";
export * from "./core/pictograph/LetterBorderUtils";
export * from "./core/pictograph/PropPlacementData";
export * from "./core/pictograph/SvgTypes";
export * from "./models/core/pictograph/GridData";
export * from "./models/core/pictograph/MotionData";
export * from "./models/core/pictograph/PictographData";
export * from "./models/core/pictograph/PositioningModels";

// Enum exports (specific to avoid conflicts)
export * from "./enums/enums";

// Export build types from new locations
export type {
  GenerationOptions,
  LetterDerivationResult,
} from "./models/build/generate/GenerateModels";

export type {
  LayoutCalculationParams,
  LayoutCalculationResult,
  OptionPickerLayoutCalculationResult,
  ResponsiveLayoutConfig,
} from "./models/build/construct/OptionPicker";

export type {
  BeatClickResult,
  BeatEditOperation,
  BeatEditResult,
  SequenceCreationParams,
  SequenceCreationResult,
  WorkbenchActions,
  WorkbenchConfig,
  WorkbenchState,
} from "./models/build/workbench/WorkbenchModels";

export type { WorkbenchMode } from "./types/build/WorkbenchTypes";

// Export beat frame types
export * from "./models/build/workbench/BeatFrame";

// Export sequence operations types
export * from "./models/build/workbench/SequenceOperations";

// Export workbench types
export * from "./types/build/WorkbenchTypes";

// Export image export types
export type {
  BeatRenderOptions,
  CompositionOptions,
  ExportError,
  ExportProgress,
  LayoutData,
  TextRenderOptions,
  TKAImageExportOptions,
  UserInfo,
} from "./models/build/export/ImageExport";

// Export image format types
export type {
  ImageFormatOptions,
  OptimizationSettings,
} from "./models/build/export/ImageFormat";

// Export panel management types (browse-specific)
export type {
  PanelConfiguration,
  PanelState,
  ResizeOperation,
  SplitterConfig,
} from "./models/browse/PanelManagement";

// Export option picker layout types (build/construct-specific)
export type {
  OptionPickerGridConfiguration,
  OptionPickerLayoutCalculationParams,
  OptionPickerLayoutDimensions,
} from "./models/build/construct/OptionPickerLayout";

// Export page layout types (sequence-card-specific)
export type {
  DPIConfiguration,
  GridCalculationOptions,
  GridConfig,
  LayoutCalculationRequest,
  LayoutValidationResult,
  Margins,
  Page,
  PageCreationOptions,
  PageDimensions,
  PageLayoutConfig,
  Rectangle,
} from "./models/sequence-card/PageLayout";

// Export sequence-card types except conflicting ones
// Export sequence card types directly (no intermediate exports)
export type {
  CacheConfig,
  CacheEntry,
  DeviceCapabilities,
  ExportOptions,
  ProgressInfo,
  ProgressStage,
  ResponsiveSettings,
  SequenceCardExportSettings,
} from "./models/sequence-card/SequenceCard";

export type {
  OptimizationGoal,
  PageOrientation,
  SequenceCardLayoutMode,
} from "./types/PageLayoutTypes";

export * from "./models/sequence-card/PageLayoutConstants";
export * from "./models/sequence-card/sequence-card-models";
export * from "./models/sequence-card/SequenceCardExport";

// Export sequence card export types
export type {
  BatchExportOptions,
  BatchExportResult,
  ImageExportOptions,
  PDFExportOptions,
} from "./models/sequence-card/export-config";

// Export browse types directly (no intermediate exports)
export {
  createFilterConfig,
  formatFilterDisplayName,
  isMultiValueFilter,
  isRangeFilter,
} from "./models/browse/BrowseFilters";

export {
  createCustomSortConfig,
  getAvailableSortConfigs,
  getAvailableSortMethods,
  getSortConfig,
  getSortDisplayName,
  SORT_CONFIGS,
} from "./models/browse/BrowseSorting";

export {
  createDefaultBrowseState,
  createDefaultDisplayState,
  createDefaultLoadingState,
  NavigationMode,
  updateBrowseState,
} from "./models/browse/BrowseState";

export * from "./models/browse/Metadata";

export type { FilterConfig } from "./models/browse/FilterModels";
export type { SortConfig } from "./models/browse/SortModels";
export type { FilterValue, SortDirection } from "./types/browse/BrowseTypes";

export type {
  BrowseDisplayState,
  BrowseLoadingState,
  BrowseState,
  SequenceFilterResult,
} from "./models/browse/BrowseState";

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
} from "./models/browse/BrowseModels";

export type {
  FavoriteItem,
  FavoritesCollection,
} from "./models/browse/FavoritesModels";

export type {
  AnimationConfig,
  AnimationState,
} from "./models/browse/AnimationModels";

export type {
  BeatOperationResult,
  SequenceStatistics,
  SequenceTransformOptions,
} from "./models/browse/SequenceState";

// Background types will be added when the actual files are found

// Export pictograph types (only what actually exists)
// PictographData and createPictographData are already exported above

// Export positioning types (what actually exists)
export type {
  Point,
  Position,
} from "./models/core/pictograph/PositioningModels";

// AppSettings doesn't exist yet

// Schema types don't exist in domain yet

// Export learn/codex domain types
export type {
  LetterCategory,
  PictographTransformOperation,
} from "./types/CodexTypes";

export type {
  CodexConfiguration,
  CodexLetter,
  LessonConfiguration,
  LetterMapping,
  LetterRow,
} from "./models/learn/CodexModels";

// Export factory functions
export {
  createCodexLetter,
  createLetterMapping,
  createLetterRow,
} from "./models/learn/CodexModels";

// Export workbench types
export type { ConfigurationResult } from "./models/build/workbench/WorkbenchModels";

// Export option picker utility functions
export {
  getContainerAspect,
  getDeviceConfig,
  getDeviceType,
} from "./models/build/construct/OptionPickerUtils";

// ResizeDirection is already exported from enums above

// Export additional option picker layout types
export type { DeviceConfig } from "./models/build/construct/OptionPickerLayoutModels";

// Export service interfaces (needed by some files)
export type { ILessonRepository } from "../services/contracts/learn/ILessonRepository";
export type { ILetterMappingRepository } from "../services/contracts/learn/ILetterMappingRepository";

// Export SVG conversion types
export type {
  RenderQualitySettings,
  SVGConversionOptions,
} from "./models/core/rendering/SvgConversion";

// Export grid types (including beat grid types)
export type {
  CombinedGridOptions,
  GridDrawOptions,
  GridValidationResult,
} from "./models/core/pictograph/GridData";

// Export schema types
export { PngMetadataArraySchema, SequenceDataSchema } from "./schemas";

// Export memory estimation types
export interface MemoryEstimate {
  estimatedMB: number;
  safe: boolean;
}

// Export sequence card types
export type { SequenceCardPaperSize } from "./types/PageLayoutTypes";

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
