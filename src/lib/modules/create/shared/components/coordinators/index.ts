/**
 * Coordinator Components Index
 *
 * Exports all coordinator components for CreateModule panel orchestration.
 */

export { default as EditCoordinator } from "./EditCoordinator.svelte";
export { default as AnimationCoordinator } from "./AnimationCoordinator.svelte";
export { default as ShareCoordinator } from "./ShareCoordinator.svelte";
export { default as SequenceActionsCoordinator } from "./SequenceActionsCoordinator.svelte";
export { default as CAPCoordinator } from "./CAPCoordinator.svelte";
// Temporarily removed due to circular dependency - imported directly in CreateModule
// export { default as ConfirmationDialogCoordinator } from './ConfirmationDialogCoordinator.svelte';
