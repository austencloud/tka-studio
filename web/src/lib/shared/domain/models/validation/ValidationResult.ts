/**
 * Standard validation result interface used across the application
 */

export interface ValidationResult {
  isValid: boolean;
  errors: ValidationError[];
  warnings?: ValidationWarning[];
}

export interface ValidationError {
  code: string;
  message: string;
  field?: string;
  value?: unknown;
  severity: "error" | "warning" | "info";
}

export interface ValidationWarning {
  code: string;
  message: string;
  field?: string;
  value?: unknown;
}
