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
  | "word_card"
  | "word-card"
  | "write"
  | "learn"
  | "about"
  | "animator";

/**
 * Available build tab sub-sections
 * Note: Edit functionality is now handled via a slide-out panel, not a tab
 */
export type ActiveBuildTab =
  | "construct"
  | "generate"
  | "animate"
  | "share"
  | "record";

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
