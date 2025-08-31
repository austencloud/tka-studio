/**
 * Animation Service Interfaces
 *
 * Consolidated export point for all animation-related service interfaces.
 */

// Animation Services
export * from "./IAnimationControlService";
export * from "./IAnimationStateService";
export * from "./IBeatCalculationService";
export * from "./IPropInterpolationService";
export * from "./ISequenceAnimationOrchestrator";

// Re-export animation domain types that are commonly used with animation services
export type {
  ISequenceAnimationEngine,
  PropStates,
  SequenceMetadata,
} from "$domain/data-interfaces/ISequenceAnimationEngine";
