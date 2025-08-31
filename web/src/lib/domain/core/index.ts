/**
 * Core Domain Types
 *
 * Export point for core domain types and fundamental data structures.
 */

export * from "./ApplicationTypes";
export * from "./AppSettings";
export * from "./Letter";
export * from "./pictograph";
export * from "./SequenceData";
export * from "./types";
export * from "./ui";

// Note: Types from other domain areas are exported directly from domain/index.ts
// to avoid duplicate exports. Import them directly from their source modules.
