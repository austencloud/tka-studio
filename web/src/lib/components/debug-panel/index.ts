/**
 * Debug Panel Components
 *
 * Refactored debug panel components for better maintainability and reusability.
 * This replaces the monolithic ArrowDebugInfoPanel.svelte.
 */

// Individual section components
export { default as DebugDataGrid } from "./DebugDataGrid.svelte";
export { default as DebugSection } from "./DebugSection.svelte";

// Utilities
export * from "./formatters";
export * from "./stepManager";

// Types
export interface DebugItem {
  label: string;
  value: string | number | boolean;
  type?: "text" | "number" | "boolean" | "angle" | "coordinate" | "percentage";
  className?: string;
}
