// Foundation UI Components
// Reusable UI building blocks that are used across multiple modules

export { default as BottomSheet } from "./BottomSheet.svelte";
export { default as SheetDragHandle } from "./SheetDragHandle.svelte";
export { default as ConfirmDialog } from "./ConfirmDialog.svelte";
export { default as ErrorBanner } from "./ErrorBanner.svelte";
export { default as ErrorScreen } from "./ErrorScreen.svelte";
export { default as FloatingFullscreenButton } from "./FloatingFullscreenButton.svelte";
export { default as FontAwesomeIcon } from "./FontAwesomeIcon.svelte";
export { default as HorizontalSwipeContainer } from "./HorizontalSwipeContainer.svelte";
export { default as IOSToggle } from "./IOSToggle.svelte";
export { default as LoadingScreen } from "./LoadingScreen.svelte";
export { default as LoadingSpinner } from "./LoadingSpinner.svelte";
export { default as SimpleGlassScroll } from "./SimpleGlassScroll.svelte";
export { default as Splitter } from "./Splitter.svelte";
// Export types
export type { ScrollbarVariant, UISize, UIVariant } from "./types";

// Export UI types that are missing from shared exports
export type {
  ActiveBuildTab,
  ExportResult,
  Html2CanvasFunction,
  PerformanceSnapshot,
  TabId,
  UIPerformanceMetrics,
  UITheme,
  WindowWithHtml2Canvas,
} from "./UITypes";
