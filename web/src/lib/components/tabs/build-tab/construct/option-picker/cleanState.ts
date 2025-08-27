/**
 * Clean State Management Modules
 *
 * Re-exports for the refactored, modular state management system
 */

// Main orchestrator (use this in most cases)
export {
  createSectionState,
  type SectionState,
} from "$lib/state/construct/option-picker/index.svelte";

// Individual state modules (for advanced use cases)
export {
  createDeviceState,
  type DeviceState,
} from "$lib/state/construct/option-picker/deviceState.svelte";
export {
  createContainerState,
  type ContainerState,
} from "$lib/state/construct/option-picker/containerState.svelte";
export {
  createLayoutState,
  type LayoutState,
} from "$lib/state/construct/option-picker/layoutState.svelte";
export {
  createUIState,
  type UIState,
} from "$lib/state/construct/option-picker/uiState.svelte";
