/**
 * Application Bootstrap - TKA V2 Modern
 *
 * This module creates and configures the application's dependency injection container,
 * registering all services and their dependencies following the clean architecture
 * pattern established in the desktop application.
 */

import { ServiceContainer } from "./di/ServiceContainer";
import type { ServiceInterface } from "./di/types";

// Import registration functions
import { registerBrowseServices } from "./di/registration/browse-services";
import { registerCoreServices } from "./di/registration/core-services";
import { registerPositioningServices } from "./di/registration/positioning-services";
import { registerSharedServices } from "./di/registration/shared-services";

import { registerAnimatorServices } from "./di/registration/animator-services";
import { registerBackgroundServices } from "./di/registration/background-services";
import { registerCodexServices } from "./di/registration/codex-services";
import { registerGenerationServices } from "./di/registration/generation-services";

import { registerSequenceCardExportServices } from "./di/registration/sequence-card-export-services";

/**
 * Create and configure the web application DI container
 */
export async function createWebApplication(): Promise<ServiceContainer> {
  const container = new ServiceContainer("tka-web-v2");

  try {
    // Register services in the correct dependency order
    // Shared services must be registered first as they have no dependencies
    await registerSharedServices(container);
    await registerCoreServices(container);
    await registerCodexServices(container);
    await registerPositioningServices(container);
    await registerAnimatorServices(container);
    await registerBackgroundServices(container);
    await registerBrowseServices(container);

    await registerGenerationServices(container);
    // ⚠️ TEMPORARILY DISABLED: Image export services still use old DI system
    // await registerImageExportServices(container);
    await registerSequenceCardExportServices(container);

    // Temporarily disable validation to fix infinite loop
    // await validateContainerConfiguration(container);

    // Set as global container so resolve() function works
    setGlobalContainer(container);

    return container;
  } catch (error) {
    console.error("❌ Failed to initialize application container:", error);
    throw new Error(
      `Application initialization failed: ${error instanceof Error ? error.message : "Unknown error"}`
    );
  }
}

/**
 * Global container instance for use throughout the application
 */
let globalContainer: ServiceContainer | null = null;

/**
 * Get the global container instance
 */
export function getContainer(): ServiceContainer {
  if (!globalContainer) {
    throw new Error(
      "Application container not initialized. Call createWebApplication() first."
    );
  }
  return globalContainer;
}

/**
 * Set the global container instance (used by bootstrap)
 */
export function setGlobalContainer(container: ServiceContainer | null): void {
  globalContainer = container;
}

/**
 * DISABLED: Legacy DI system - use InversifyJS instead
 */
export function legacyResolve<T>(
  serviceInterface: ServiceInterface<T> | string
): T {
  throw new Error(
    `🚨 LEGACY DI SYSTEM DISABLED! Service "${serviceInterface}" must use InversifyJS container instead. ` +
      `Import { resolve, TYPES } from "$lib/services/inversify/container" and use resolve(TYPES.ServiceName)`
  );
}
