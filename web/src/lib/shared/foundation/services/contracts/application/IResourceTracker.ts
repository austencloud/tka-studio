/**
 * Resource Tracker Service Contract
 * 
 * Manages lifecycle of browser resources (DOM elements, WebGL contexts, workers, etc.)
 * to prevent memory leaks and ensure proper cleanup.
 * 
 * Follows the established dependency injection architecture pattern.
 */

export interface IResourceTracker {
  /**
   * Track a resource for automatic cleanup
   * @param resource - The resource to track (DOM element, WebGL context, worker, etc.)
   */
  trackResource(resource: unknown): void;

  /**
   * Stop tracking a resource (useful when manually disposing)
   * @param resource - The resource to untrack
   */
  untrackResource(resource: unknown): void;

  /**
   * Dispose all tracked resources and clear the tracker
   * Called during cleanup to prevent memory leaks
   */
  disposeAll(): void;

  /**
   * Get count of currently tracked resources (for debugging)
   */
  getTrackedCount(): number;

  /**
   * Check if the tracker is active
   */
  isActive(): boolean;

  /**
   * Deactivate the tracker (prevents new resources from being tracked)
   */
  deactivate(): void;
}
