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
import { registerSharedServices } from "./di/registration/shared-services";
import { registerBrowseServices } from "./di/registration/browse-services";
import { registerCoreServices } from "./di/registration/core-services";
import { registerPositioningServices } from "./di/registration/positioning-services";
import { registerMotionTesterServices } from "./di/registration/motion-tester-services";
import { registerAnimatorServices } from "./di/registration/animator-services";
import { registerCodexServices } from "./di/registration/codex-services";
import { registerMovementServices } from "./di/registration/movement-services";
// TODO: Uncomment when image export services are implemented
// import { registerImageExportServices } from "./di/registration/image-export-services";

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
    await registerBrowseServices(container);
    await registerMotionTesterServices(container);
    await registerMovementServices(container);
    // TODO: Uncomment when image export services are implemented
    // await registerImageExportServices(container);

    // Validate all registrations can be resolved
    await validateContainerConfiguration(container);

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
 * Helper function to resolve services from the global container
 */
export function resolve<T>(serviceInterface: ServiceInterface<T> | string): T {
  const container = getContainer();

  if (typeof serviceInterface === "string") {
    // Legacy string-based resolution for backward compatibility
    const mappedInterface = serviceInterfaceMap.get(serviceInterface);
    if (!mappedInterface) {
      console.error(
        `❌ Service interface not found for key: ${serviceInterface}`
      );
      console.error(
        `❌ Available service keys:`,
        Array.from(serviceInterfaceMap.keys())
      );
      throw new Error(
        `Service interface not found for key: ${serviceInterface}`
      );
    }
    return container.resolve(mappedInterface) as T;
  }

  return container.resolve(serviceInterface);
}
