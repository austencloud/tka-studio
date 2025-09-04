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
export * from "./models/application";
export * from "./models/csv-handling";
export * from "./models/device-recognition";
export * from "./models/pictograph";
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
// SCHEMAS (Validation schemas)
// ============================================================================
export * from "./schemas";
