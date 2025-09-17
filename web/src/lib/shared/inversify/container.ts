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

// Handle HMR (Hot Module Replacement) - reset state if needed
if (import.meta.hot) {
  import.meta.hot.accept(() => {
    console.log("🔄 HMR: Container module reloaded");
  });

  // Reset initialization state on HMR to allow re-initialization
  import.meta.hot.dispose(() => {
    console.log("🔄 HMR: Disposing container state");
    isInitialized = false;
    initializationPromise = null;
  });
}

// Export resolve function
export function resolve<T>(serviceType: symbol): T {
  if (!isInitialized) {
    throw new Error(
      `Container not initialized. Service ${String(serviceType)} cannot be resolved before container initialization completes.`
    );
  }
  return container.get<T>(serviceType);
}

// Async resolve function for use during initialization
export async function resolveAsync<T>(serviceType: symbol): Promise<T> {
  await ensureContainerInitialized();
  return container.get<T>(serviceType);
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

// Load all modules asynchronously
async function initializeContainer() {
  if (initializationPromise) {
    return initializationPromise;
  }

  initializationPromise = (async () => {
    try {
      // Import modules dynamically to avoid circular dependencies
      const {
        coreModule,
        animatorModule,
        galleryModule,
        buildModule,
        exportModule,
        pictographModule,
        learnModule,
        wordCardModule,
        writeModule,
        dataModule,
      } = await import("./modules");

      await container.load(
        coreModule,
        dataModule,
        pictographModule,
        animatorModule,
        galleryModule,
        buildModule,
        exportModule,
        learnModule,
        wordCardModule,
        writeModule
      );
      isInitialized = true;
      console.log("✅ TKA Container: All modules loaded successfully");
    } catch (error) {
      console.error("❌ TKA Container: Failed to load modules:", error);
      throw error;
    }
  })();

  return initializationPromise;
}

// Initialize the container asynchronously without blocking exports
initializeContainer();

// Export module initialization function for testing or manual control
export { initializeContainer };

