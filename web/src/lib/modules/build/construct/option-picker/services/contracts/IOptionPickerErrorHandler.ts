/**
 * Option Picker Error Handler Interface
 *
 * Professional error handling and recovery strategies.
 */

import type { OptionPickerError, OptionPickerErrorType } from '../../domain/errors/OptionPickerError';

export interface IOptionPickerErrorHandler {
  /**
   * Convert unknown errors into classified OptionPickerError types
   */
  handleError(error: unknown, context?: Record<string, unknown>): OptionPickerErrorType;

  /**
   * Determine if an error can be retried
   */
  canRetry(error: OptionPickerError): boolean;

  /**
   * Determine if an error is recoverable without user intervention
   */
  isRecoverable(error: OptionPickerError): boolean;

  /**
   * Get user-friendly error message
   */
  getUserMessage(error: OptionPickerError): string;

  /**
   * Get recovery suggestions for the user
   */
  getRecoverySuggestions(error: OptionPickerError): string[];

  /**
   * Log error for debugging and monitoring
   */
  logError(error: OptionPickerError): void;
}
