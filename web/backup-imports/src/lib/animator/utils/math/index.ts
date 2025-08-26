/**
 * Math Services Index
 *
 * Centralized exports for all math-related services.
 * This replaces the monolithic standalone-math.ts file.
 */

// Constants
export * from "./MathConstants.js";

// Angle calculations
export * from "./AngleCalculationService.js";

// Motion calculations
export * from "./MotionCalculationService.js";

// Endpoint calculations
export * from "./EndpointCalculationService.js";

// Coordinate updates
export * from "./CoordinateUpdateService.js";

// ✅ ELIMINATED: PropAttributes - using native MotionData instead!
// Re-export types for backward compatibility
export type { PropState } from "../../../components/animator/types/PropState.js";
