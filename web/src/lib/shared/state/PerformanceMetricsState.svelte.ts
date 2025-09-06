/**
 * Performance Metrics Service
 *
 * Tracks application performance metrics.
 * Clean separation of performance tracking from other concerns.
 */

import type { UIPerformanceMetrics } from "../domain";
import type { IPerformanceMetricsState } from "./app-state-interfaces";

export class PerformanceMetricsState implements IPerformanceMetricsState {
  // Performance metrics state
  #performanceMetrics = $state<UIPerformanceMetrics>({
    initializationTime: 0,
    lastRenderTime: 0,
    memoryUsage: 0,
  });

  // ============================================================================
  // GETTERS
  // ============================================================================

  get performanceMetrics() {
    return this.#performanceMetrics;
  }

  // ============================================================================
  // ACTIONS
  // ============================================================================

  updateInitializationTime(time: number): void {
    this.#performanceMetrics.initializationTime = time;
  }

  updateLastRenderTime(time: number): void {
    this.#performanceMetrics.lastRenderTime = time;
  }

  updateMemoryUsage(): void {
    if (typeof performance !== "undefined" && "memory" in performance) {
      const memory = (performance as { memory: { usedJSHeapSize: number } })
        .memory;
      this.#performanceMetrics.memoryUsage = Math.round(
        memory.usedJSHeapSize / 1048576
      );
    }
  }

  resetMetrics(): void {
    this.#performanceMetrics.initializationTime = 0;
    this.#performanceMetrics.lastRenderTime = 0;
    this.#performanceMetrics.memoryUsage = 0;
  }
}

// Export the class for DI container binding
// Singleton instance will be managed by the DI container
