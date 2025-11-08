export * from "./create-module-state.svelte";
export * from "./construct-tab-state.svelte";

/**
 * Sequence State - Clean Refactored Version
 *
 * This module replaces the 890-line god object with a composable architecture:
 *
 * - SequenceCoreState: Core sequence data (123 lines)
 * - SequenceSelectionState: Selection tracking (114 lines)
 * - SequenceArrowState: Arrow positioning (77 lines)
 * - SequenceAnimationState: Animation state (97 lines)
 * - SequencePersistenceCoordinator: Persistence (119 lines)
 * - SequenceBeatOperations: Beat operations (235 lines)
 * - SequenceTransformOperations: Transform operations (142 lines)
 * - SequenceStateOrchestrator: Composition layer (456 lines)
 *
 * TOTAL: ~1363 lines across 8 focused files vs 890 lines in 1 file
 *
 * WHY MORE LINES?
 * - Explicit interfaces and proper typing
 * - Clear separation of concerns
 * - Better documentation
 * - Individual testability
 * - Removed hidden coupling
 * - Eliminated type gymnastics
 *
 * BENEFITS:
 * - Each module has single responsibility
 * - Easy to test in isolation
 * - Clear dependencies
 * - No god object anti-pattern
 * - Type-safe throughout
 * - HMR-friendly
 */

// Main exports
export { createSequenceState } from "./SequenceStateOrchestrator.svelte";
export type {
  SequenceState,
  SequenceStateServices,
} from "./SequenceStateOrchestrator.svelte";

// Export sub-states for advanced usage
export { createSequenceCoreState } from "./core/SequenceCoreState.svelte";
export type { SequenceCoreState } from "./core/SequenceCoreState.svelte";

export { createSequenceSelectionState } from "./selection/SequenceSelectionState.svelte";
export type { SequenceSelectionState } from "./selection/SequenceSelectionState.svelte";

export { createSequenceArrowState } from "./arrow/SequenceArrowState.svelte";
export type { SequenceArrowState } from "./arrow/SequenceArrowState.svelte";

export { createSequenceAnimationState } from "./animation/SequenceAnimationState.svelte";
export type { SequenceAnimationState } from "./animation/SequenceAnimationState.svelte";

export { createSequencePersistenceCoordinator } from "./persistence/SequencePersistenceCoordinator.svelte";
export type { SequencePersistenceCoordinator } from "./persistence/SequencePersistenceCoordinator.svelte";

export { createSequenceBeatOperations } from "./operations/SequenceBeatOperations";
export type { SequenceBeatOperations } from "./operations/SequenceBeatOperations";

export { createSequenceTransformOperations } from "./operations/SequenceTransformOperations";
export type { SequenceTransformOperations } from "./operations/SequenceTransformOperations";
