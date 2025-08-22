/**
 * Domain Types Re-exports
 *
 * Clean re-export of domain models for service interfaces.
 * This centralizes domain type imports to avoid repetition across interface files.
 */

// Re-export core domain models
export type {
  ArrowPlacementData,
  PropPlacementData,
  BeatData,
  SequenceData,
  MotionData,
  PictographData,
} from "../../domain";

// Re-export browse domain types
export type {
  BrowseDisplayState,
  BrowseLoadingState,
  FilterType,
  FilterValue,
  SortMethod,
} from "../../domain/browse";

// Re-export sequence card domain types
export type {
  LayoutConfig,
  ExportOptions,
  SequenceCardExportSettings,
  DeviceCapabilities,
  PrintLayoutOptions,
  CacheEntry,
  CacheConfig,
  ProgressInfo,
  ValidationResult,
  ExportResult,
} from "../../domain/sequenceCard";

// Re-export enums for convenience
export type {
  MotionType,
  Location,
  Orientation,
  RotationDirection,
} from "../../domain/enums";
