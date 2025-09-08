/**
 * Option Picker Error Handler Implementation
 *
 * Professional error classification, recovery, and user guidance.
 */

import { injectable } from 'inversify';
import { OptionPickerErrors, type OptionPickerError, type OptionPickerErrorType } from '../../domain/errors/OptionPickerError';
import type { IOptionPickerErrorHandler } from '../contracts/IOptionPickerErrorHandler';

@injectable()
export class OptionPickerErrorHandler implements IOptionPickerErrorHandler {
  
  /**
   * Convert unknown errors into classified OptionPickerError types
   */
  handleError(error: unknown, context?: Record<string, unknown>): OptionPickerErrorType {
    // Handle already classified errors
    if (this.isOptionPickerError(error)) {
      return error;
    }

    // Network-related errors
    if (this.isNetworkError(error)) {
      return OptionPickerErrors.network(
        'NETWORK_ERROR',
        `Network request failed: ${error instanceof Error ? error.message : 'Unknown network error'}`,
        'Unable to load options. Please check your internet connection and try again.',
        error,
        context
      );
    }

    // Validation errors
    if (this.isValidationError(error)) {
      return OptionPickerErrors.validation(
        'VALIDATION_ERROR',
        `Validation failed: ${error instanceof Error ? error.message : 'Invalid input'}`,
        'The provided sequence data is invalid. Please check your sequence and try again.',
        error,
        context
      );
    }

    // Business rule violations
    if (this.isBusinessRuleError(error)) {
      return OptionPickerErrors.businessRule(
        'BUSINESS_RULE_ERROR',
        `Business rule violation: ${error instanceof Error ? error.message : 'Rule violation'}`,
        'This action violates business rules. Please review your sequence configuration.',
        error,
        context
      );
    }

    // Default to system error
    return OptionPickerErrors.system(
      'UNKNOWN_ERROR',
      `Unexpected error: ${error instanceof Error ? error.message : 'Unknown error'}`,
      'An unexpected error occurred. Please try again, and contact support if the problem persists.',
      error,
      context
    );
  }

  /**
   * Determine if an error can be retried
   */
  canRetry(error: OptionPickerError): boolean {
    return error.retryable;
  }

  /**
   * Determine if an error is recoverable without user intervention
   */
  isRecoverable(error: OptionPickerError): boolean {
    return error.recoverable;
  }

  /**
   * Get user-friendly error message
   */
  getUserMessage(error: OptionPickerError): string {
    return error.userMessage;
  }

  /**
   * Get recovery suggestions for the user
   */
  getRecoverySuggestions(error: OptionPickerError): string[] {
    switch (error.type) {
      case 'NETWORK':
        return [
          'Check your internet connection',
          'Try refreshing the page',
          'Wait a moment and try again'
        ];
      
      case 'VALIDATION':
        return [
          'Check your sequence data for errors',
          'Ensure all required fields are filled',
          'Contact support if the data appears correct'
        ];
      
      case 'BUSINESS_RULE':
        return [
          'Review your sequence configuration',
          'Check the sequence length and complexity',
          'Consult the documentation for valid sequences'
        ];
      
      case 'SYSTEM':
        return [
          'Try again in a few moments',
          'Refresh the page',
          'Contact support if the problem persists'
        ];
      
      default:
        return [
          'Try again',
          'Refresh the page',
          'Contact support if needed'
        ];
    }
  }

  /**
   * Log error for debugging and monitoring
   */
  logError(error: OptionPickerError): void {
    console.error(`[OptionPicker] ${error.type}:${error.code}`, {
      message: error.message,
      userMessage: error.userMessage,
      context: error.context,
      cause: error.cause,
      stack: error.stack
    });
  }

  // ============================================================================
  // PRIVATE HELPER METHODS
  // ============================================================================

  private isOptionPickerError(error: unknown): error is OptionPickerErrorType {
    return error instanceof Error && 
           error.name.startsWith('OptionPicker') &&
           'type' in error && 
           'code' in error;
  }

  private isNetworkError(error: unknown): boolean {
    if (!(error instanceof Error)) return false;
    
    const message = error.message.toLowerCase();
    return message.includes('network') ||
           message.includes('fetch') ||
           message.includes('connection') ||
           message.includes('timeout') ||
           error.name === 'NetworkError' ||
           error.name === 'TypeError' && message.includes('failed to fetch');
  }

  private isValidationError(error: unknown): boolean {
    if (!(error instanceof Error)) return false;
    
    const message = error.message.toLowerCase();
    return message.includes('validation') ||
           message.includes('invalid') ||
           message.includes('required') ||
           message.includes('schema') ||
           error.name === 'ValidationError';
  }

  private isBusinessRuleError(error: unknown): boolean {
    if (!(error instanceof Error)) return false;
    
    const message = error.message.toLowerCase();
    return message.includes('business') ||
           message.includes('rule') ||
           message.includes('constraint') ||
           message.includes('policy') ||
           error.name === 'BusinessRuleError';
  }
}
