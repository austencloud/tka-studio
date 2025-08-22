/**
 * Shared Services Registration
 * Handles registration of shared utility services used across multiple domains
 */

import type { IEnumMappingService } from "../../interfaces/application-interfaces";
import type { ServiceContainer } from "../ServiceContainer";

import {
  CSVParserService,
  type ICSVParserService,
} from "../../implementations/data/CSVParserService";
import { EnumMappingService } from "../../implementations/data/EnumMappingService";

import type { IOptionFilteringService } from "../../implementations/data/OptionFilteringService";
import { OptionFilteringService } from "../../implementations/data/OptionFilteringService";
import type { IPictographTransformationService } from "../../implementations/data/PictographTransformationService";
import { PictographTransformationService } from "../../implementations/data/PictographTransformationService";

// Import ServiceInterface type
import type { ServiceInterface } from "../types";

// Define service interface objects for shared services
export const IEnumMappingServiceInterface: ServiceInterface<IEnumMappingService> =
  {
    token: "IEnumMappingService",
    implementation: null as unknown as new (
      ...args: unknown[]
    ) => IEnumMappingService,
  };

export const ICSVParserServiceInterface: ServiceInterface<ICSVParserService> = {
  token: "ICSVParserService",
  implementation: null as unknown as new (
    ...args: unknown[]
  ) => ICSVParserService,
};

export const IPictographTransformationServiceInterface: ServiceInterface<IPictographTransformationService> =
  {
    token: "IPictographTransformationService",
    implementation: null as unknown as new (
      ...args: unknown[]
    ) => IPictographTransformationService,
  };

export const IOptionFilteringServiceInterface: ServiceInterface<IOptionFilteringService> =
  {
    token: "IOptionFilteringService",
    implementation: null as unknown as new (
      ...args: unknown[]
    ) => IOptionFilteringService,
  };

/**
 * Register all shared utility services
 * These services are used across multiple domains and should be registered first
 */
export async function registerSharedServices(
  container: ServiceContainer
): Promise<void> {
  // Register core utility services (no dependencies)
  container.registerFactory(IEnumMappingServiceInterface, () => {
    return new EnumMappingService();
  });

  container.registerFactory(ICSVParserServiceInterface, () => {
    return new CSVParserService();
  });

  // Register transformation services (depend on enum mapping)
  container.registerFactory(IPictographTransformationServiceInterface, () => {
    const enumMappingService = container.resolve(
      IEnumMappingServiceInterface
    ) as IEnumMappingService;
    return new PictographTransformationService(enumMappingService);
  });

  // Register filtering services (depend on enum mapping)
  container.registerFactory(IOptionFilteringServiceInterface, () => {
    const enumMappingService = container.resolve(
      IEnumMappingServiceInterface
    ) as IEnumMappingService;
    return new OptionFilteringService(enumMappingService);
  });

  console.log("✅ Shared services registered successfully");
}

/**
 * Helper function to resolve shared services with proper typing
 */
export function resolveSharedServices(container: ServiceContainer) {
  return {
    enumMappingService: container.resolve(
      IEnumMappingServiceInterface
    ) as IEnumMappingService,
    csvParserService: container.resolve(
      ICSVParserServiceInterface
    ) as ICSVParserService,

    pictographTransformationService: container.resolve(
      IPictographTransformationServiceInterface
    ),
    optionFilteringService: container.resolve(IOptionFilteringServiceInterface),
  };
}
