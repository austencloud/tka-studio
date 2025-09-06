/**
 * Application UI Types
 *
 * Core UI state and navigation types for the application.
 * These represent domain concepts related to user interface navigation and theming.
 */

/**
 * Available application tabs
 */
export type TabId =
  | "construct"
  | "browse"
  | "sequence_card"
  | "word-card"
  | "write"
  | "learn"
  | "about"
  | "animator";

/**
 * Available build tab sub-sections
 */
export type ActiveBuildTab = "construct" | "generate" | "edit" | "export";

/**
 * Application theme options
 */
export type Theme = "light" | "dark";

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
  data?: Blob | string;
  filename?: string;
  error?: string;
  metadata?: Record<string, unknown>;
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
