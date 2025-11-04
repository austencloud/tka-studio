// Foundation UI Components
// Reusable UI building blocks that are used across multiple modules

export { default as Drawer } from "./Drawer.svelte";
export { default as SheetDragHandle } from "./SheetDragHandle.svelte";
export { default as ConfirmDialog } from "./ConfirmDialog.svelte";
export { default as ErrorScreen } from "./ErrorScreen.svelte";
export { default as FontAwesomeIcon } from "./FontAwesomeIcon.svelte";
export { default as HorizontalSwipeContainer } from "./HorizontalSwipeContainer.svelte";
export { default as SkeletonLoader } from "./SkeletonLoader.svelte";
export { default as SimpleGlassScroll } from "./SimpleGlassScroll.svelte";
// Export types
export type { ScrollbarVariant, UISize, UIVariant } from "./types";

// Export UI types that are missing from shared exports
export type {
  ActiveCreateModule,
  BuildModeId,
  ExportResult,
  Html2CanvasFunction,
  PerformanceSnapshot,
  TabId,
  UIPerformanceMetrics,
  UITheme,
  WindowWithHtml2Canvas,
} from "./UITypes";
