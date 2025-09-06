/**
 * Shared Domain - Main Export Point
 *
 * Central barrel export for all shared domain models, types, and enums.
 * These are cross-cutting concerns used across multiple modules.
 */

// ============================================================================
// ENUMS (Core enums used throughout the application)
// ============================================================================
export * from "./enums";

// ============================================================================
// MODELS (Shared data models)
// ============================================================================
export * from "../pictograph/domain/models";
export * from "./models/application";
export * from "./models/csv-handling";
export * from "./models/device-recognition";
export * from "./models/rendering";
export * from "./models/sequence";
export * from "./models/validation";

// ============================================================================
// TYPES (Shared type definitions)
// ============================================================================
// export * from "./types"; // Empty directory - no types yet

// ============================================================================
// UI TYPES (Shared UI-related types)
// ============================================================================
export * from "./ui";

// ============================================================================
// WORD CARD TYPES (Re-exported for convenience)
// ============================================================================
export type {
  DPIConfig,
  DPIConfiguration,
  GridCalculationOptions,
  LayoutCalculationRequest,
  LayoutCalculationResult,
  LayoutValidationError,
  LayoutValidationResult,
  LayoutValidationWarning,
  MeasurementUnit,
  PageCreationOptions,
  PageDimensions,
  PageLayoutConfig,
  PageMargins,
  PageOrientation,
  PaperSpecification,
  PrintConfig,
  Rectangle,
  WordCardGridConfig,
  WordCardPaperSize,
} from "../../modules/word-card/domain";

// ============================================================================
// WORKBENCH TYPES (Re-exported for convenience)
// ============================================================================
export type {
  BeatClickResult,
  BeatEditOperation,
  BeatEditResult,
  ConfigurationResult,
  SequenceCreateRequest,
  SequenceCreationParams,
  SequenceCreationResult,
  WorkbenchConfig,
  WorkbenchMode,
} from "../../modules/build/workbench/domain";

// ============================================================================
// SCHEMAS (Validation schemas)
// ============================================================================
export * from "./schemas";
