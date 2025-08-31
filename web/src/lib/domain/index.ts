/**
 * Domain Models Index
 *
 * Central export point for all domain models following modern desktop architecture.
 */

// Core Types and Models (includes UI backgrounds)
export * from "./core";

// Enums
export * from "./enums";

// Browse Models
export * from "./browse";

// Build Domain Types (explicit exports to avoid Position conflicts)
export * from "./build/generate";
export * from "./build/image-export";
export * from "./build/option-picker";
export type {
  BeatFrameConfig,
  Position as BeatFramePosition,
  ContainerDimensions,
  LayoutInfo,
} from "./build/workbench/beat-frame";
export * from "./build/workbench/BeatData";

// Layout Domain Types
export * from "./layout";

// Sequence Card Types
export * from "./sequence-card";

// Learn Domain Types
export * from "./learn";

// Schemas
export * from "./schemas";

// Note: data-interfaces not exported from main index to avoid conflicts
// Services should import data-interfaces directly when needed
