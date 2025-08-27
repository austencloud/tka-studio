/**
 * InversifyJS Application Bootstrap
 *
 * This file handles the initialization of the InversifyJS container
 * and replaces the complex bootstrap.ts from the old DI system.
 */

import "reflect-metadata";
import { container } from "./container";
import { runServiceResolutionTests } from "./test-service-resolution";

/**
 * Initialize the InversifyJS container and all services
 * This replaces the createWebApplication() function from the old bootstrap
 */
export async function initializeInversifyContainer(): Promise<void> {
  console.log("🚀 Initializing InversifyJS container...");

  try {
    // TODO: Load service modules here as they are converted
    // Example:
    // await loadCoreServices();
    // await loadRenderingServices();
    // await loadPositioningServices();

    console.log("✅ InversifyJS container initialized");

    // Run service resolution tests
    runServiceResolutionTests();
  } catch (error) {
    console.error("❌ Failed to initialize InversifyJS container:", error);
    throw error;
  }
}

/**
 * Get the initialized container
 * This provides backward compatibility with the old bootstrap pattern
 */
export function getContainer() {
  return container;
}

/**
 * Legacy resolve function for backward compatibility
 * This allows existing code to work during the migration
 */
export function resolve<T>(serviceType: symbol): T {
  return container.get<T>(serviceType);
}

// Export container and types for convenience
export { container } from "./container";
export { TYPES } from "./types";
