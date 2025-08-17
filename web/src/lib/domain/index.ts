/**
 * Domain Models Index
 *
 * Central export point for all domain models following modern desktop architecture.
 */

// Enums
export * from "./enums";

// Core Models
export * from "./MotionData";
export * from "./GridData";
export * from "./ArrowData";
export * from "./PropData";
export * from "./PictographData";
export * from "./BeatData";
export * from "./SequenceData";

// Page Layout - explicitly re-export to resolve Orientation ambiguity
export type {
  PageDimensions,
  Margins,
  Rectangle,
  PrintConfiguration,
  PaperSize,
  GridCalculationOptions,
  PageLayoutConfig,
  Orientation as PageOrientation, // Rename to avoid conflict with enum Orientation
} from "./pageLayout";

// Browse Models
export * from "./browse";
