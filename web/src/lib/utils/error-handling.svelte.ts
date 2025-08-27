/**
 * Standardized error handling utilities for TKA components
 * Provides consistent error boundaries and recovery strategies
 */

export interface ErrorState {
  hasError: boolean;
  errorMessage: string | null;
  errorCode?: string;
  retryCount: number;
}

export interface AsyncOperationState<T> {
  data: T | null;
  isLoading: boolean;
  error: ErrorState;
}

/**
 * Creates standardized error state management
 */
export function createErrorState() {
  let errorState = $state<ErrorState>({
    hasError: false,
    errorMessage: null,
    retryCount: 0,
  });

  function setError(error: unknown, code?: string) {
    const message = error instanceof Error ? error.message : String(error);
    errorState = {
      hasError: true,
      errorMessage: message,
      errorCode: code,
      retryCount: errorState.retryCount,
    };

    console.error(`TKA Error [${code || "UNKNOWN"}]:`, message, error);
  }

  function clearError() {
    errorState = {
      hasError: false,
      errorMessage: null,
      retryCount: errorState.retryCount,
    };
  }

  function incrementRetry() {
    errorState.retryCount += 1;
  }

  function resetRetries() {
    errorState.retryCount = 0;
  }

  return {
    get state() {
      return errorState;
    },
    setError,
    clearError,
    incrementRetry,
    resetRetries,
  };
}

/**
 * Creates async operation state with built-in error handling
 */
export function createAsyncState<T>() {
  let state = $state<AsyncOperationState<T>>({
    data: null,
    isLoading: false,
    error: {
      hasError: false,
      errorMessage: null,
      retryCount: 0,
    },
  });

  async function execute(
    operation: () => Promise<T>,
    options: { maxRetries?: number; retryDelay?: number } = {}
  ): Promise<T | null> {
    const { maxRetries = 3, retryDelay = 1000 } = options;

    state.isLoading = true;
    state.error.hasError = false;

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
      try {
        const result = await operation();
        state.data = result;
        state.isLoading = false;
        state.error.retryCount = 0;
        return result;
      } catch (error) {
        console.warn(`Attempt ${attempt + 1} failed:`, error);

        if (attempt === maxRetries) {
          const message =
            error instanceof Error ? error.message : String(error);
          state.error = {
            hasError: true,
            errorMessage: message,
            retryCount: attempt + 1,
          };
          state.isLoading = false;
          throw error;
        }

        if (retryDelay > 0) {
          await new Promise((resolve) => setTimeout(resolve, retryDelay));
        }
      }
    }

    return null;
  }

  function reset() {
    state = {
      data: null,
      isLoading: false,
      error: {
        hasError: false,
        errorMessage: null,
        retryCount: 0,
      },
    };
  }

  return {
    get state() {
      return state;
    },
    execute,
    reset,
  };
}

/**
 * Safe service resolution with error handling
 * FIXED: Now uses TYPES symbols instead of strings
 */
export async function safeResolve<T>(
  serviceType: symbol,
  fallback?: () => T
): Promise<T | null> {
  try {
    const { resolve } = await import("$lib/services/inversify/container");
    return resolve<T>(serviceType);
  } catch (error) {
    console.error(
      `Failed to resolve service ${serviceType.toString()}:`,
      error
    );
    return fallback ? fallback() : null;
  }
}

/**
 * Wraps component state with error boundary
 */
export function withErrorBoundary<T>(
  stateFactory: () => T,
  componentName: string
): T | null {
  try {
    return stateFactory();
  } catch (error) {
    console.error(`Error initializing ${componentName} state:`, error);
    return null;
  }
}
