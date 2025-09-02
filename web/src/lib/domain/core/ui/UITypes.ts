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
  | "write"
  | "learn"
  | "about"
  | "motion-tester";

/**
 * Available build tab sub-sections
 */
export type ActiveBuildSubTab = "construct" | "generate" | "edit" | "export";

/**
 * Application theme options
 */
export type Theme = "light" | "dark";

/**
 * Performance metrics for application state tracking
 * Note: Different from background PerformanceMetrics which track fps/rendering
 */
export interface ApplicationPerformanceMetrics {
  initializationTime: number;
  lastRenderTime: number;
  memoryUsage: number;
}
