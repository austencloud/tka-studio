/**
 * Browse Module
 *
 * Complete browse module with all components, domain models, services, and state
 * for sequence browsing functionality.
 */

// Re-export everything from all layers
// Note: components directory doesn't exist yet
// export * from "./components";
// Export domain types selectively to avoid conflicts
export type {
  CompleteFilterState,
  FilterHistoryEntry,
  GalleryFilterConfiguration,
} from "./gallery/domain";
export * from "./gallery/domain/enums";
export * from "./gallery/domain/models";
// export * from "./services"; // No services directory

// Export state selectively to avoid conflicts
export * from "./gallery/state/gallery-panel-state.svelte";
export * from "./gallery/state/gallery-state-factory.svelte";
// Export GalleryFilterState class from state (not the interface from domain)
export { GalleryFilterState as GalleryFilterStateService } from "./gallery/state/GalleryFilterState.svelte";
export * from "./gallery/state/GallerySearchState.svelte";
export * from "./gallery/state/GalleryState.svelte";
export type { BrowseState } from "./shared/state/browse-state-models";
export * from "./shared/state/BrowseDisplayState.svelte";
export * from "./shared/state/BrowseNavigationState.svelte";
export * from "./shared/state/BrowseSelectionState.svelte";
