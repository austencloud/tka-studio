// Foundation UI Components
// Reusable UI building blocks that are used across multiple modules

export { default as ErrorScreen } from "./ErrorScreen.svelte";
export { default as IOSToggle } from "./IOSToggle.svelte";
export { default as LoadingScreen } from "./LoadingScreen.svelte";
export { default as SimpleGlassScroll } from "./SimpleGlassScroll.svelte";
export { default as Splitter } from "./Splitter.svelte";

// Re-export types for convenience
// export type { ScrollbarVariant } from "./SimpleGlassScroll.svelte";

// Temporary type definition
export type ScrollbarVariant = "default" | "minimal" | "thick";
