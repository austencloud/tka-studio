/**
 * Pure Utilities Index
 *
 * ONLY exports pure utility functions that don't require dependency injection.
 * All functions that need services have been moved to services/implementations.
 */

// Animation utilities
export {
  getAnimationSettings,
  shouldAnimate,
  shouldAnimate as shouldAnimateGlobal,
} from "./animation-control";
export * from "./fold-transition";
export {
  conditionalFade,
  fade,
  fadeIn,
  fadeOut,
  shouldAnimate as shouldAnimateLocal,
} from "./simple-fade";

// Background utilities
export * from "./background-preloader";
export * from "./background/backgroundUtils";

// Storage utilities
export * from "./dev-storage-cleanup";
export * from "./safe-storage";
export * from "./session-storage-cleanup";

// File utilities
export * from "./file-download";
export * from "./png-metadata-extractor";
export * from "./png-parser";

// Image utilities (pure functions)
export * from "./letter-image-getter";

// UI utilities
export * from "./seo-utils";

// Performance utilities
export * from "./memoizationUtils";

// Pure validation utilities (if any remain pure)
export * from "./validation";

// Math utilities (pure functions from animator services)
export {
  calculateCoordinatesFromAngle,
  calculateMotionEndpoints,
  lerpAngle,
  type MotionEndpoints,
} from "$implementations";

// Motion utilities (pure functions)
export * from "../services/contracts/animator/motion-helpers";

// NOTE: The following have been moved to services:
// - betaDetection -> BetaDetectionService
// - error-handling -> ErrorHandlingService
// - motion-helpers -> MotionHelperService
// - pictograph-rendering-utils -> Already in services
// - letterMigration -> Will be migrated to service
// - simpleMigration -> Will be migrated to service
// - letter-image-getter -> Will be migrated to service
// - Math utilities -> Keep separate in animator/utils/math
