import { Container } from "inversify";

// Export TYPES immediately to avoid circular dependency
export { TYPES } from "./types";

// Create container
const container = new Container();

// Export container and resolve function immediately
export { container };
export const inversifyContainer = container;

// Track initialization state
let isInitialized = false;
let initializationPromise: Promise<void> | null = null;
let isHMRRecovering = false; // Track HMR recovery state

// Browser detection utility
const isBrowser = typeof window !== "undefined";

// Handle HMR (Hot Module Replacement) - improved resilience
if (import.meta.hot) {
  import.meta.hot.accept(() => {
    isHMRRecovering = true;
    // Don't reset initialization state - let existing container work
    // Auto-recover by re-initializing if needed
    if (!isInitialized) {
      initializeContainer()
        .then(() => {
          isHMRRecovering = false;
        })
        .catch((error) => {
          console.error("❌ HMR: Container recovery failed:", error);
          isHMRRecovering = false;
        });
    } else {
      isHMRRecovering = false;
    }
  });

  // Only reset if we absolutely have to
  import.meta.hot.dispose(() => {
    // Don't reset isInitialized - keep container working during HMR
    // Only clear the promise so it can re-initialize if needed
    initializationPromise = null;

    // Keep container bindings active during HMR to prevent resolution errors
  });
}

// DEPRECATED: Sync resolve function - use async resolve instead
export function resolveSync<T>(serviceType: symbol): T {
  // Don't resolve services during SSR
  if (!isBrowser) {
    throw new Error(
      `Cannot resolve service ${String(serviceType)} during server-side rendering. Use tryResolve() or ensure this code only runs in browser.`
    );
  }

  // If we're in HMR recovery mode, wait a bit for auto-recovery
  if (isHMRRecovering) {
    // Small delay to allow HMR recovery to complete
    setTimeout(() => {}, 10);
  }

  if (!isInitialized) {
    // During HMR, try to auto-recover by re-initializing silently
    if (import.meta.hot && !isHMRRecovering) {
      isHMRRecovering = true;
      // Start initialization in background but throw for now - next call should work
      initializeContainer()
        .then(() => {
          isHMRRecovering = false;
        })
        .catch((error) => {
          console.error("❌ HMR: Container recovery failed:", error);
          isHMRRecovering = false;
        });
    }

    throw new Error(
      `Container not initialized. Service ${String(serviceType)} cannot be resolved before container initialization completes.`
    );
  }

  try {
    return container.get<T>(serviceType);
  } catch (error) {
    // During HMR, container might have stale bindings
    if (import.meta.hot && !isHMRRecovering) {
      isHMRRecovering = true;
      initializeContainer()
        .then(() => {
          isHMRRecovering = false;
        })
        .catch((err) => {
          console.error("HMR re-initialization failed:", err);
          isHMRRecovering = false;
        });
    }
    throw error;
  }
}

// Safe resolve function that returns null if container is not ready
export function tryResolve<T>(serviceType: symbol): T | null {
  // Return null during SSR
  if (!isBrowser) {
    return null;
  }

  if (!isInitialized) {
    return null;
  }
  try {
    return container.get<T>(serviceType);
  } catch (error) {
    console.warn(`Failed to resolve ${String(serviceType)}:`, error);
    return null;
  }
}

// Async resolve function for use during initialization
export async function resolve<T>(serviceType: symbol): Promise<T> {
  await ensureContainerInitialized();
  return container.get<T>(serviceType);
}

// Check if container is initialized
export function isContainerInitialized(): boolean {
  return isInitialized;
}

// Get container status for debugging
export function getContainerStatus() {
  return {
    isInitialized,
    hasInitializationPromise: initializationPromise !== null,
    containerExists: container !== null,
  };
}

// Ensure container is initialized
export async function ensureContainerInitialized(): Promise<void> {
  if (isInitialized) return;
  if (initializationPromise) {
    await initializationPromise;
    return;
  }
  await initializeContainer();
}

// Load all modules synchronously for better HMR support
function initializeContainer() {
  // Don't initialize during SSR
  if (!isBrowser) {
    return Promise.resolve();
  }

  if (initializationPromise) {
    return initializationPromise;
  }

  initializationPromise = (async () => {
    try {
      // Try synchronous import first for better HMR support
      let modules;
      try {
        // Import synchronously if possible
        modules = await import("./modules");
      } catch (error) {
        console.warn(
          "Sync module import failed, falling back to async:",
          error
        );
        modules = await import("./modules");
      }

      const {
        coreModule,
        animatorModule,
        exploreModule,
        buildModule,
        navigationModule,
        pictographModule,
        renderModule,
        shareModule,
        learnModule,
        wordCardModule,
        writeModule,
        dataModule,
      } = modules;

      await container.load(
        coreModule,
        dataModule,
        pictographModule,
        animatorModule,
        exploreModule,
        buildModule,
        navigationModule,
        renderModule,
        shareModule,
        learnModule,
        wordCardModule,
        writeModule
      );
      isInitialized = true;
    } catch (error) {
      console.error("❌ TKA Container: Failed to load modules:", error);
      // Reset state so we can try again
      isInitialized = false;
      initializationPromise = null;
      throw error;
    }
  })();

  return initializationPromise;
}

// Initialize the container asynchronously without blocking exports (browser-only)
if (isBrowser) {
  initializeContainer();
}

// Export module initialization function for testing or manual control
export { initializeContainer };
