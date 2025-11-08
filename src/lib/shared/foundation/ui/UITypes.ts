/**
 * Application UI Types
 *
 * Core UI state and navigation types for the application.
 * These represent domain concepts related to user interface navigation and theming.
 */

// Re-export ModuleId from navigation domain types (single source of truth)
export type { ModuleId } from "../../navigation/domain/types";

/**
 * Legacy tab IDs (for backwards compatibility during migration)
 * Maps old tab names to module concepts
 */
export type LegacyTabId =
  | "construct" // Legacy ID that maps to "build" module
  | "browse" // Legacy ID for browse/explore
  | "word-card" // Legacy hyphenated version
  | "about" // About page (not a proper module)
  | "animator"; // Animator feature

/**
 * All possible tab/module IDs (includes both new ModuleId and legacy IDs)
 * @deprecated Prefer using ModuleId for new code
 */
export type TabId =
  | import("../../navigation/domain/types").ModuleId
  | LegacyTabId;

/**
 * Available sections/tabs within the Create module
 * Note: Edit and Export are now slide-up panels, not tabs
 * Note: Animate is now a play button with inline animator
 * Note: Record and Share have been removed
 */
export type BuildModeId =
  | "guided"
  | "construct"
  | "one-handed"
  | "gestural"
  | "generate";

/**
 * Legacy type alias for backwards compatibility
 * @deprecated Use BuildModeId instead
 */
export type ActiveCreateModule = BuildModeId;

/**
 * UI theme options for foundation components
 */
export type UITheme = "light" | "dark";

/**
 * Performance metrics for UI state tracking
 * Note: Different from ApplicationPerformanceMetrics which track app-level metrics
 */
export interface UIPerformanceMetrics {
  initializationTime: number;
  lastRenderTime: number;
  memoryUsage: number;
}

/**
 * Snapshot of application performance and state for debugging
 */
export interface PerformanceSnapshot {
  timestamp: number;
  metrics: UIPerformanceMetrics;
  appState: object;
  memoryUsage: number;
}

/**
 * Generic export result interface
 * Base interface for all export operations across the application
 */
export interface ExportResult {
  success: boolean;
  canvas?: HTMLCanvasElement;
  blob?: Blob;
  data?: Blob;
  filename?: string;
  error?: string;
  warnings?: string[];
  metadata?: {
    format: string;
    size: number;
    dimensions: { width: number; height: number };
    beatCount: number;
    processingTime: number;
    successCount?: number;
    failureCount?: number;
    totalErrors?: number;
  };
}

// ============================================================================
// HTML2CANVAS INTEGRATION TYPES
// ============================================================================

/**
 * Html2Canvas function type for dynamic loading
 */
export interface Html2CanvasFunction {
  (
    element: HTMLElement,
    options?: Record<string, unknown>
  ): Promise<HTMLCanvasElement>;
}

/**
 * Window object extended with html2canvas
 */
export interface WindowWithHtml2Canvas extends Window {
  html2canvas: Html2CanvasFunction;
}
