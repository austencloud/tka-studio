/**
 * Error classes for the state registry
 */

// Base error class for persistence operations
export class PersistenceError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'PersistenceError';
  }
}

// Error for corrupted data
export class DataCorruptionError extends PersistenceError {
  constructor(id: string, originalError?: Error) {
    super(`Corrupted data detected for ${id}${originalError ? `: ${originalError.message}` : ''}`);
    this.name = 'DataCorruptionError';
  }
}

// Error for storage operations
export class StorageError extends PersistenceError {
  constructor(operation: string, originalError?: Error) {
    super(
      `Storage operation failed during ${operation}${
        originalError ? `: ${originalError.message}` : ''
      }`
    );
    this.name = 'StorageError';
  }
}
