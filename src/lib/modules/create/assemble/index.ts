/**
 * Guided Builder (Guided Construct) - Barrel Export
 *
 * Exports all components, services, and state for Guided Construct mode
 */

// Components
export { default as AssemblerOrchestrator } from "./components/AssemblerOrchestrator.svelte";
export { default as GuidedConstructTab } from "./components/AssemblerTab.svelte";
export { default as SinglePropStartPositionPicker } from "./components/SinglePropStartPositionPicker.svelte";
export { default as GuidedOptionViewer } from "./components/AssemblyOptionPicker.svelte";

// Handpath Builder Module
export * from "./handpath-builder";

// Services
export { GuidedOptionGenerator } from "./services/GuidedOptionGenerator";
export type { IGuidedOptionGenerator } from "./services/GuidedOptionGenerator";

// State
export { createGuidedConstructState } from "./state/guided-construct-state.svelte";
export type {
  GuidedConstructState,
  GuidedConstructConfig,
} from "./state/guided-construct-state.svelte";
