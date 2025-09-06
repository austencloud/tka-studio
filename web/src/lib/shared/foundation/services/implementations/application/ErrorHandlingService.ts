/**
 * Error Handling Service Implementation
 *
 * Provides centralized error handling and service resolution utilities.
 * Migrated from utils/error-handling.svelte.ts to proper service architecture.
 */

import { injectable } from "inversify";
import type { IErrorHandlingService } from "../../contracts/application/IErrorHandlingService";

@injectable()
export class ErrorHandlingService implements IErrorHandlingService {
  /**
   * Safe service resolution with error handling
   */
  async safeResolve<T>(
    serviceType: symbol,
    fallback?: () => T
  ): Promise<T | null> {
    try {
      // const { resolve } = await import("../../../inversify");
      const resolve = null; // Temporary fallback
      return (resolve as any)(serviceType);
    } catch (error) {
      console.error(
        `Failed to resolve service ${serviceType.toString()}:`,
        error
      );
      return fallback ? fallback() : null;
    }
  }

  /**
   * Handle and log errors consistently
   */
  handleError(error: unknown, context: string): void {
    const errorMessage = error instanceof Error ? error.message : String(error);
    const stack = error instanceof Error ? error.stack : undefined;

    console.error(`[${context}] Error:`, errorMessage);
    if (stack) {
      console.error(`[${context}] Stack:`, stack);
    }
  }

  /**
   * Create error with context information
   */
  createContextualError(
    message: string,
    context: string,
    originalError?: unknown
  ): Error {
    const contextualMessage = `[${context}] ${message}`;
    const error = new Error(contextualMessage);

    if (originalError instanceof Error) {
      error.cause = originalError;
      error.stack = originalError.stack;
    }

    return error;
  }

  logError(error: Error, context?: string): void {
    const contextStr = context ? `[${context}] ` : "";
    console.error(`${contextStr}Error:`, error.message);
    if (error.stack) {
      console.error("Stack:", error.stack);
    }
  }
}
