/**
 * Animation Service Interfaces
 *
 * Consolidated export point for all animation-related service interfaces.
 */

// Core Animation Services
export * from "./IAnimationLoopService";
export * from "./IAnimationPlaybackController";
export * from "./IAnimationStateManager";

// Animator service interfaces
export * from "./IBeatCalculator";
export * from "./IPropInterpolator";
export * from "./ISequenceAnimationOrchestrator";

// Calculation & Utility Services
export * from "./IAngleCalculator";
export * from "./ICoordinateUpdater";
export * from "./IEndpointCalculator";
export * from "./IMotionCalculator";

// Rendering Services
export * from "./ICanvasRenderer";
export * from "./ISVGGenerator";
export * from "./IGifExportService";
export * from "./IGifExportOrchestrator";

// ============================================================================
// ARCHIVED CONTRACTS (moved to archive/animator-unused-services/)
// ============================================================================
// export * from "./IAnimationController";
// export * from "./IMotionParameterManager";
// export * from "./IOverlayRenderer";
// export * from "./IPictographRenderer"; // Unused - no implementation exists
