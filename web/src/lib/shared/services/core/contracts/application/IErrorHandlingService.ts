/**
 * Error Handling Service Interface
 *
 * Provides centralized error handling and service resolution utilities.
 */

export interface IErrorHandlingService {
  /**
   * Safe service resolution with error handling
   */
  safeResolve<T>(serviceType: symbol, fallback?: () => T): Promise<T | null>;

  /**
   * Handle and log errors consistently
   */
  handleError(error: unknown, context: string): void;

  /**
   * Create error with context information
   */
  createContextualError(
    message: string,
    context: string,
    originalError?: unknown
  ): Error;
}
