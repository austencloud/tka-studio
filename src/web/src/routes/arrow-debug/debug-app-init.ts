/**
 * Arrow Debug App Initialization
 *
 * Ensures the DI container is properly initialized before the debug components load.
 */

import { createWebApplication } from "$lib/services/bootstrap";

// Global flag to track initialization
let isInitialized = false;
let initializationPromise: Promise<void> | null = null;

/**
 * Initialize the application DI container if not already done
 */
export async function initializeDebugApp(): Promise<void> {
  if (isInitialized) {
    return;
  }

  if (initializationPromise) {
    return initializationPromise;
  }

  initializationPromise = (async () => {
    try {
      console.log("🔧 Initializing Arrow Debug application...");
      await createWebApplication();
      isInitialized = true;
      console.log("✅ Arrow Debug application initialized successfully");
    } catch (error) {
      console.error("❌ Failed to initialize Arrow Debug application:", error);
      throw error;
    }
  })();

  return initializationPromise;
}

/**
 * Check if the application is initialized
 */
export function isDebugAppInitialized(): boolean {
  return isInitialized;
}
