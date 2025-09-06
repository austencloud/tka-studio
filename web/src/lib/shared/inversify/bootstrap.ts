/**
 * InversifyJS Application Bootstrap
 *
 * This file handles the initialization of the InversifyJS container
 * and replaces the complex bootstrap.ts from the old DI system.
 */

import "reflect-metadata";

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
  } catch (error) {
    console.error("❌ Failed to initialize InversifyJS container:", error);
    throw error;
  }
}

// Export container and types for convenience
export { container, resolve, TYPES } from "./container";
