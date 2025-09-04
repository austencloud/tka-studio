/**
 * Browse Components - Browse tab and related components
 */

// Main browse tab component
export { default as BrowseTab } from "./BrowseTab.svelte";

// Layout components
export { default as BrowseLayout } from "./BrowseLayout.svelte";
export { default as NavigationSidebar } from "./NavigationSidebar.svelte";
export { default as PanelContainer } from "./PanelContainer.svelte";

// Content components
export { default as AnimationPanel } from "../../animator/components/AnimationPanel.svelte";
export { default as AccordionSection } from "./AccordionSection.svelte";
export { default as CategoryButton } from "./CategoryButton.svelte";
export { default as FilterSelectionPanel } from "./FilterSelectionPanel.svelte";
export { default as QuickAccessSection } from "./QuickAccessSection.svelte";

// Viewer components
export { default as FullscreenSequenceViewer } from "./FullscreenSequenceViewer.svelte";

// UI components
export { default as BrowseLoadingOverlay } from "./BrowseLoadingOverlay.svelte";
export { default as DeleteConfirmationDialog } from "./DeleteConfirmationDialog.svelte";
export { default as BrowseErrorBanner } from "./ErrorBanner.svelte";
export { default as LoadingSpinner } from "./LoadingSpinner.svelte";

// Sub-module exports
export * from "./gallery";
export * from "./fullscreen";
export * from "./thumbnail";
export * from "./viewer";

// Event handlers
export * from "../services/implementations/browse-event-handlers";
export * from "../services/implementations/navigation-event-handlers";
