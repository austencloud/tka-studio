/**
 * Validation Utilities for TKA
 *
 * Provides standardized validation error handling and safe parsing utilities.
 * Used by services that need to validate external data (LocalStorage, PNG imports, etc.)
 */

import { z } from "zod";

export class ValidationError extends Error {
  constructor(
    message: string,
    public readonly zodError?: z.ZodError,
    public readonly context?: string
  ) {
    super(message);
    this.name = "ValidationError";
  }
}

/**
 * Creates a user-friendly validation error from a Zod error
 */
export function createValidationError(
  error: z.ZodError,
  context: string = "data validation"
): ValidationError {
  const firstError = error.errors[0];
  const path = firstError?.path.join(".") || "unknown field";
  const message = `${context} failed: ${firstError?.message} at ${path}`;

  return new ValidationError(message, error, context);
}

/**
 * Safe parsing with better error messages - returns result object
 */
export function safeParse<T>(
  schema: z.ZodSchema<T>,
  data: unknown,
  context?: string
): { success: true; data: T } | { success: false; error: ValidationError } {
  const result = schema.safeParse(data);

  if (result.success) {
    return { success: true, data: result.data };
  } else {
    return {
      success: false,
      error: createValidationError(result.error, context),
    };
  }
}

/**
 * Safe parsing that returns null on failure - useful for optional validation
 */
export function safeParseOrNull<T>(
  schema: z.ZodSchema<T>,
  data: unknown,
  context?: string
): T | null {
  const result = safeParse(schema, data, context);
  if (result.success) {
    return result.data;
  } else {
    console.warn(`Validation failed (${context}):`, result.error.message);
    return null;
  }
}

/**
 * Strict parsing that throws on failure - use for critical validations
 */
export function parseStrict<T>(
  schema: z.ZodSchema<T>,
  data: unknown,
  context?: string
): T {
  const result = safeParse(schema, data, context);
  if (result.success) {
    return result.data;
  } else {
    throw result.error;
  }
}

/**
 * Validation with fallback value - useful for graceful degradation
 */
export function parseWithFallback<T>(
  schema: z.ZodSchema<T>,
  data: unknown,
  fallback: T,
  context?: string
): T {
  const result = safeParseOrNull(schema, data, context);
  return result ?? fallback;
}

/**
 * Array validation that filters out invalid items instead of failing entirely
 */
export function parseArrayWithFilter<T>(
  itemSchema: z.ZodSchema<T>,
  data: unknown[],
  context?: string
): T[] {
  if (!Array.isArray(data)) {
    console.warn(`Expected array for ${context}, got ${typeof data}`);
    return [];
  }

  const validItems: T[] = [];
  let invalidCount = 0;

  for (let i = 0; i < data.length; i++) {
    const result = safeParse(itemSchema, data[i], `${context}[${i}]`);
    if (result.success) {
      validItems.push(result.data);
    } else {
      invalidCount++;
      console.warn(
        `Skipping invalid item in ${context}[${i}]:`,
        result.error.message
      );
    }
  }

  if (invalidCount > 0) {
    console.info(
      `Filtered out ${invalidCount} invalid items from ${context} (kept ${validItems.length})`
    );
  }

  return validItems;
}
