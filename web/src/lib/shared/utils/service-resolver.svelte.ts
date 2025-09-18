/**
 * HMR-Safe Service Resolution Utility
 * 
 * This utility provides a robust way to resolve services from the DI container
 * that gracefully handles Hot Module Replacement (HMR) scenarios where the
 * container might not be fully initialized when components are reloaded.
 * 
 * Features:
 * - Lazy service resolution (only when actually needed)
 * - Automatic retry logic for container initialization
 * - HMR-safe with proper error handling
 * - Reactive service references using Svelte 5 runes
 * - Clean API that maintains simple component code
 */

import { browser } from "$app/environment";
import { resolve, TYPES } from "$shared/inversify";

/**
 * Service resolver state for a specific service type
 */
interface ServiceResolver<T> {
  /** The resolved service instance (null if not yet resolved) */
  readonly value: T | null;
  /** Whether the service is currently being resolved */
  readonly isResolving: boolean;
  /** Last error encountered during resolution */
  readonly error: Error | null;
  /** Manually trigger service resolution */
  resolve(): void;
}

/**
 * Creates a reactive service resolver that handles HMR gracefully
 * 
 * @param serviceSymbol - The service symbol to resolve
 * @param options - Configuration options
 * @returns Reactive service resolver
 * 
 * @example
 * ```typescript
 * const shareService = createServiceResolver<IShareService>(TYPES.IShareService);
 * 
 * // Use in component:
 * $effect(() => {
 *   if (shareService.value) {
 *     // Service is available, safe to use
 *     shareService.value.doSomething();
 *   }
 * });
 * ```
 */
export function createServiceResolver<T>(
  serviceSymbol: symbol,
  options: {
    /** Maximum number of retry attempts */
    maxRetries?: number;
    /** Delay between retry attempts (ms) */
    retryDelay?: number;
    /** Whether to auto-resolve on creation */
    autoResolve?: boolean;
  } = {}
): ServiceResolver<T> {
  const {
    maxRetries = 5,
    retryDelay = 100,
    autoResolve = true
  } = options;

  let service = $state<T | null>(null);
  let isResolving = $state(false);
  let error = $state<Error | null>(null);
  let retryCount = 0;
  let retryTimeout: number | null = null;

  /**
   * Attempts to resolve the service from the container
   */
  async function attemptResolve(): Promise<void> {
    if (!browser || isResolving) return;

    isResolving = true;
    error = null;

    try {
      // Clear any pending retry
      if (retryTimeout) {
        clearTimeout(retryTimeout);
        retryTimeout = null;
      }

      // Attempt to resolve the service
      const resolvedService = resolve<T>(serviceSymbol);
      
      // Success!
      service = resolvedService;
      retryCount = 0;
      isResolving = false;
      
      console.log(`✅ ServiceResolver: Successfully resolved service ${serviceSymbol.toString()}`);
      
    } catch (err) {
      const resolveError = err instanceof Error ? err : new Error(String(err));
      
      // Check if this is a container initialization error
      const isContainerError = resolveError.message.includes('Container not initialized') ||
                              resolveError.message.includes('No bindings found');
      
      if (isContainerError && retryCount < maxRetries) {
        // Schedule retry for container initialization errors
        retryCount++;
        console.warn(`⚠️ ServiceResolver: Container not ready for ${serviceSymbol.toString()}, retrying (${retryCount}/${maxRetries})...`);
        
        retryTimeout = window.setTimeout(() => {
          attemptResolve();
        }, retryDelay * retryCount); // Exponential backoff
        
      } else {
        // Max retries reached or non-container error
        error = resolveError;
        isResolving = false;
        
        if (retryCount >= maxRetries) {
          console.error(`❌ ServiceResolver: Failed to resolve ${serviceSymbol.toString()} after ${maxRetries} retries:`, resolveError);
        } else {
          console.error(`❌ ServiceResolver: Failed to resolve ${serviceSymbol.toString()}:`, resolveError);
        }
      }
    }
  }

  /**
   * Manual resolve trigger
   */
  function manualResolve(): void {
    retryCount = 0; // Reset retry count for manual attempts
    attemptResolve();
  }

  // Auto-resolve on creation if enabled
  if (autoResolve) {
    attemptResolve();
  }

  // Cleanup on destroy
  $effect(() => {
    return () => {
      if (retryTimeout) {
        clearTimeout(retryTimeout);
      }
    };
  });

  return {
    get value() { return service; },
    get isResolving() { return isResolving; },
    get error() { return error; },
    resolve: manualResolve
  };
}

/**
 * Creates multiple service resolvers at once
 * 
 * @param serviceMap - Map of service names to symbols
 * @returns Map of service names to resolvers
 * 
 * @example
 * ```typescript
 * const services = createServiceResolvers({
 *   share: TYPES.IShareService,
 *   sequence: TYPES.ISequenceService
 * });
 * 
 * // Use: services.share.value, services.sequence.value
 * ```
 */
export function createServiceResolvers<T extends Record<string, symbol>>(
  serviceMap: T,
  options?: Parameters<typeof createServiceResolver>[1]
): { [K in keyof T]: ServiceResolver<any> } {
  const resolvers = {} as { [K in keyof T]: ServiceResolver<any> };
  
  for (const [name, symbol] of Object.entries(serviceMap)) {
    resolvers[name as keyof T] = createServiceResolver(symbol, options);
  }
  
  return resolvers;
}

/**
 * Utility to check if all services in a resolver map are ready
 */
export function allServicesReady(resolvers: Record<string, ServiceResolver<any>>): boolean {
  return Object.values(resolvers).every(resolver => resolver.value !== null);
}

/**
 * Utility to get all errors from a resolver map
 */
export function getServiceErrors(resolvers: Record<string, ServiceResolver<any>>): Error[] {
  return Object.values(resolvers)
    .map(resolver => resolver.error)
    .filter((error): error is Error => error !== null);
}
