/**
 * Container Validation Utilities
 * Validates that all registered services can be resolved correctly
 */

import {
  IApplicationInitializationServiceInterface,
  IDeviceDetectionServiceInterface,
  IPersistenceServiceInterface,
  ISequenceDomainServiceInterface,
  ISequenceServiceInterface,
  ISettingsServiceInterface,
} from "./interfaces/core-interfaces";
import type { ServiceContainer } from "./ServiceContainer";
import type { ServiceInterface } from "./types";

/**
 * Validate that all registered services can be resolved
 */
export async function validateContainerConfiguration(
  container: ServiceContainer,
): Promise<void> {
  const servicesToValidate = [
    // Core services needed by MainApplication
    IPersistenceServiceInterface,
    ISettingsServiceInterface,
    IDeviceDetectionServiceInterface,
    ISequenceDomainServiceInterface,
    ISequenceServiceInterface,
    IApplicationInitializationServiceInterface,
  ];

  for (const serviceInterface of servicesToValidate) {
    try {
      console.log(`🔍 Validating service: ${serviceInterface.token}`);
      const service = container.resolve(
        serviceInterface as ServiceInterface<unknown>,
      );
      if (!service) {
        throw new Error(
          `Service ${serviceInterface.token} resolved to null/undefined`,
        );
      }
      console.log(`✅ Service validated: ${serviceInterface.token}`);
    } catch (error) {
      console.error(
        `❌ Failed to validate service: ${serviceInterface.token}`,
        error,
      );
      throw new Error(
        `Failed to resolve ${serviceInterface.token}: ${error instanceof Error ? error.message : "Unknown error"}`,
      );
    }
  }
}
