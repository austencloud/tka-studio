/**
 * Option Picker Error Types
 *
 * Professional error classification and recovery strategies
 * for the option picker component.
 */

export interface OptionPickerError {
  type: 'NETWORK' | 'VALIDATION' | 'BUSINESS_RULE' | 'SYSTEM' | 'USER_INPUT';
  code: string;
  message: string;
  userMessage: string;
  recoverable: boolean;
  retryable: boolean;
  cause?: unknown;
  context?: Record<string, unknown>;
  stack?: string;
}

export class OptionPickerNetworkError extends Error implements OptionPickerError {
  readonly type = 'NETWORK' as const;
  readonly recoverable = true;
  readonly retryable = true;

  constructor(
    public readonly code: string,
    public readonly message: string,
    public readonly userMessage: string,
    public readonly cause?: unknown,
    public readonly context?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'OptionPickerNetworkError';
  }
}

export class OptionPickerValidationError extends Error implements OptionPickerError {
  readonly type = 'VALIDATION' as const;
  readonly recoverable = false;
  readonly retryable = false;

  constructor(
    public readonly code: string,
    public readonly message: string,
    public readonly userMessage: string,
    public readonly cause?: unknown,
    public readonly context?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'OptionPickerValidationError';
  }
}

export class OptionPickerBusinessRuleError extends Error implements OptionPickerError {
  readonly type = 'BUSINESS_RULE' as const;
  readonly recoverable = false;
  readonly retryable = false;

  constructor(
    public readonly code: string,
    public readonly message: string,
    public readonly userMessage: string,
    public readonly cause?: unknown,
    public readonly context?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'OptionPickerBusinessRuleError';
  }
}

export class OptionPickerSystemError extends Error implements OptionPickerError {
  readonly type = 'SYSTEM' as const;
  readonly recoverable = true;
  readonly retryable = true;

  constructor(
    public readonly code: string,
    public readonly message: string,
    public readonly userMessage: string,
    public readonly cause?: unknown,
    public readonly context?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'OptionPickerSystemError';
  }
}

export type OptionPickerErrorType = 
  | OptionPickerNetworkError 
  | OptionPickerValidationError 
  | OptionPickerBusinessRuleError 
  | OptionPickerSystemError;

// Error factory functions
export const OptionPickerErrors = {
  network: (code: string, message: string, userMessage: string, cause?: unknown, context?: Record<string, unknown>) =>
    new OptionPickerNetworkError(code, message, userMessage, cause, context),

  validation: (code: string, message: string, userMessage: string, cause?: unknown, context?: Record<string, unknown>) =>
    new OptionPickerValidationError(code, message, userMessage, cause, context),

  businessRule: (code: string, message: string, userMessage: string, cause?: unknown, context?: Record<string, unknown>) =>
    new OptionPickerBusinessRuleError(code, message, userMessage, cause, context),

  system: (code: string, message: string, userMessage: string, cause?: unknown, context?: Record<string, unknown>) =>
    new OptionPickerSystemError(code, message, userMessage, cause, context),
};
