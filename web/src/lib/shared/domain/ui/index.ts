/**
 * Core UI Domain Types
 *
 * Cross-cutting UI concerns that span multiple business domains.
 * Following enterprise architecture patterns for presentation layer organization.
 */

// Background systems
export * from "./backgrounds";

// Core UI types
export * from "./UITypes";

// Background types (re-export for convenience)
export type {
  AccessibilitySettings,
  BackgroundSystem,
  Dimensions,
  QualityLevel,
  ShootingStar,
  ShootingStarState,
  Star,
} from "./backgrounds/BackgroundTypes";

export { BackgroundType } from "./backgrounds/BackgroundTypes";
