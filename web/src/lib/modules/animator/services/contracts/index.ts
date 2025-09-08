/**
 * Animation Service Interfaces
 *
 * Consolidated export point for all animation-related service interfaces.
 */

// Animation Services
export * from "./IAnimationControlService";
export * from "./IAnimationStateService";
export * from "./IBeatCalculationService";
export * from "./IMotionParameterService";
export * from "./IPropInterpolationService";
export * from "./ISequenceAnimationEngine";
export * from "./ISequenceAnimationOrchestrator";

// Rendering interfaces
export * from "./IPictographRenderingService";

// Legacy interfaces (to be refactored) - commented out to avoid duplicate exports
// export * from "./animator-interfaces";
