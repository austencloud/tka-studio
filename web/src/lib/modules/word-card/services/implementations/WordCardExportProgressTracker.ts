/**
 * Word Card Export Progress Tracker
 *
 * Tracks progress for word card export operations.
 * Single responsibility: Progress tracking and event emission.
 */

import type { IWordCardExportProgressTracker } from "$services";
import type { BatchExportProgress } from "$wordcard/domain";

interface ProgressOperation {
  id: string;
  totalSteps: number;
  current: number;
  startTime: Date;
  errors: Error[];
  warnings: string[];
  callbacks: Set<(progress: BatchExportProgress) => void>;
  completed: boolean;
}

export class WordCardExportProgressTracker
  implements IWordCardExportProgressTracker
{
  private operations = new Map<string, ProgressOperation>();

  /**
   * Start tracking new operation
   */
  startOperation(operationId: string, totalSteps: number): void {
    const operation: ProgressOperation = {
      id: operationId,
      totalSteps,
      current: 0,
      startTime: new Date(),
      errors: [],
      warnings: [],
      callbacks: new Set(),
      completed: false,
    };

    this.operations.set(operationId, operation);
    console.log(
      `🎯 Started tracking operation: ${operationId} (${totalSteps} steps)`
    );
  }

  /**
   * Update progress for current operation
   */
  updateProgress(
    operationId: string,
    current: number,
    message: string,
    stage: BatchExportProgress["stage"]
  ): void {
    const operation = this.operations.get(operationId);
    if (!operation) {
      console.warn(`Operation ${operationId} not found`);
      return;
    }

    operation.current = current;

    const progress: BatchExportProgress = {
      current,
      total: operation.totalSteps,
      percentage: (current / operation.totalSteps) * 100,
      message,
      stage,
      errorCount: operation.errors.length,
      warningCount: operation.warnings.length,
      startTime: operation.startTime,
    };

    // Notify all callbacks
    operation.callbacks.forEach((callback) => {
      try {
        callback(progress);
      } catch (error) {
        console.error("Progress callback error:", error);
      }
    });

    console.log(
      `📊 Progress ${operationId}: ${current}/${operation.totalSteps} (${progress.percentage.toFixed(1)}%) - ${message}`
    );
  }

  /**
   * Add error to current operation
   */
  addError(operationId: string, error: Error): void {
    const operation = this.operations.get(operationId);
    if (!operation) {
      console.warn(`Operation ${operationId} not found`);
      return;
    }

    operation.errors.push(error);
    console.error(`❌ Error in operation ${operationId}:`, error.message);
  }

  /**
   * Add warning to current operation
   */
  addWarning(operationId: string, warning: string): void {
    const operation = this.operations.get(operationId);
    if (!operation) {
      console.warn(`Operation ${operationId} not found`);
      return;
    }

    operation.warnings.push(warning);
    console.warn(`⚠️ Warning in operation ${operationId}: ${warning}`);
  }

  /**
   * Complete operation
   */
  completeOperation(operationId: string): void {
    const operation = this.operations.get(operationId);
    if (!operation) {
      console.warn(`Operation ${operationId} not found`);
      return;
    }

    operation.completed = true;
    operation.current = operation.totalSteps;

    const finalProgress: BatchExportProgress = {
      current: operation.totalSteps,
      total: operation.totalSteps,
      percentage: 100,
      message: "Operation completed",
      stage: "finalizing",
      errorCount: operation.errors.length,
      warningCount: operation.warnings.length,
      startTime: operation.startTime,
    };

    // Final notification to all callbacks
    operation.callbacks.forEach((callback) => {
      try {
        callback(finalProgress);
      } catch (error) {
        console.error("Progress callback error:", error);
      }
    });

    const duration = Date.now() - operation.startTime.getTime();
    console.log(
      `✅ Completed operation ${operationId} in ${duration}ms. Errors: ${operation.errors.length}, Warnings: ${operation.warnings.length}`
    );

    // Clean up after a delay to allow final callbacks
    setTimeout(() => {
      this.operations.delete(operationId);
    }, 1000);
  }

  /**
   * Get current progress
   */
  getProgress(operationId: string): BatchExportProgress | null {
    const operation = this.operations.get(operationId);
    if (!operation) {
      return null;
    }

    return {
      current: operation.current,
      total: operation.totalSteps,
      percentage: (operation.current / operation.totalSteps) * 100,
      message: operation.completed ? "Completed" : "In progress",
      stage: operation.completed ? "finalizing" : "processing",
      errorCount: operation.errors.length,
      warningCount: operation.warnings.length,
      startTime: operation.startTime,
    };
  }

  /**
   * Subscribe to progress updates
   */
  onProgress(
    operationId: string,
    callback: (progress: BatchExportProgress) => void
  ): () => void {
    const operation = this.operations.get(operationId);
    if (!operation) {
      console.warn(
        `Operation ${operationId} not found for progress subscription`
      );
      return () => {}; // Return no-op unsubscribe function
    }

    operation.callbacks.add(callback);

    // Return unsubscribe function
    return () => {
      operation.callbacks.delete(callback);
    };
  }
}
