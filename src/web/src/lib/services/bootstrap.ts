/**
 * Application Bootstrap - TKA V2 Modern
 *
 * This module creates and configures the application's dependency injection container,
 * registering all services and their dependencies following the clean architecture
 * pattern established in the desktop application.
 */

import { serviceInterfaceMap } from "./di/service-registry";
import { ServiceContainer } from "./di/ServiceContainer";
import type { ServiceInterface } from "./di/types";
import { validateContainerConfiguration } from "./di/validation";

// Import registration functions
import { registerBrowseServices } from "./di/registration/browse-services";
import { registerCoreServices } from "./di/registration/core-services";
import { registerPositioningServices } from "./di/registration/positioning-services";

/**
 * Create and configure the web application DI container
 */
export async function createWebApplication(): Promise<ServiceContainer> {
  const container = new ServiceContainer("tka-web-v2");

  try {
    // Register services in the correct dependency order
    await registerCoreServices(container);
    await registerPositioningServices(container);
    await registerBrowseServices(container);

    // Validate all registrations can be resolved
    await validateContainerConfiguration(container);

    // Set as global container so resolve() function works
    setGlobalContainer(container);

    console.log(
      "✅ TKA V2 Modern application container initialized successfully",
    );
    return container;
  } catch (error) {
    console.error("❌ Failed to initialize application container:", error);
    throw new Error(
      `Application initialization failed: ${error instanceof Error ? error.message : "Unknown error"}`,
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
      "Application container not initialized. Call createWebApplication() first.",
    );
  }
  return globalContainer;
}

/**
 * Set the global container instance (used by bootstrap)
 */
export function setGlobalContainer(container: ServiceContainer): void {
  globalContainer = container;
}

/**
 * Helper function to resolve services from the global container
 */
export function resolve<T>(serviceInterface: ServiceInterface<T> | string): T {
  const container = getContainer();

  if (typeof serviceInterface === "string") {
    // Legacy string-based resolution for backward compatibility
    const mappedInterface = serviceInterfaceMap.get(serviceInterface);
    if (!mappedInterface) {
      throw new Error(
        `Service interface not found for key: ${serviceInterface}`,
      );
    }
    return container.resolve(mappedInterface) as T;
  }

  return container.resolve(serviceInterface);
}
