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
import { registerMotionTesterServices } from "./di/registration/motion-tester-services";
import { registerAnimatorServices } from "./di/registration/animator-services";
// TODO: Uncomment when image export services are implemented
// import { registerImageExportServices } from "./di/registration/image-export-services";

/**
 * Create and configure the web application DI container
 */
export async function createWebApplication(): Promise<ServiceContainer> {
  const container = new ServiceContainer("tka-web-v2");

  try {
    // Register services in the correct dependency order
    await registerCoreServices(container);
    await registerPositioningServices(container);
    await registerAnimatorServices(container);
    await registerBrowseServices(container);
    await registerMotionTesterServices(container);
    // TODO: Uncomment when image export services are implemented
    // await registerImageExportServices(container);

    // Validate all registrations can be resolved
    await validateContainerConfiguration(container);

    // Set as global container so resolve() function works
    setGlobalContainer(container);
    console.log("🌍 Global container set successfully");

    console.log(
      "✅ TKA V2 Modern application container initialized successfully"
    );
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
  console.log(
    `🌍 getContainer called, globalContainer exists:`,
    globalContainer !== null
  );
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
  console.log(`🌐 Bootstrap resolve called with:`, serviceInterface);
  const container = getContainer();

  if (typeof serviceInterface === "string") {
    console.log(`🔑 String-based resolution for: ${serviceInterface}`);
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
    console.log(`✅ Found mapped interface for: ${serviceInterface}`);
    return container.resolve(mappedInterface) as T;
  }

  console.log(`🔧 Direct interface resolution for: ${serviceInterface.token}`);
  return container.resolve(serviceInterface);
}
