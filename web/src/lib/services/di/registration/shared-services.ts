/**
 * Shared Services Registration
 * Handles registration of shared utility services used across multiple domains
 */

import type { ServiceContainer } from "../ServiceContainer";
import type {
  IEnumMappingService,
  ICSVParserService,
  ICSVLoaderService,
} from "../../interfaces/application-interfaces";

import { EnumMappingService } from "../../implementations/shared/EnumMappingService";
import { CSVParserService } from "../../implementations/shared/CSVParserService";
import { CSVLoaderService } from "../../implementations/shared/CSVLoaderService";
import { PictographTransformationService } from "../../implementations/shared/PictographTransformationService";
import { OptionFilteringService } from "../../implementations/shared/OptionFilteringService";

// Define service interface symbols for shared services
export const IEnumMappingServiceInterface = Symbol("IEnumMappingService");
export const ICSVParserServiceInterface = Symbol("ICSVParserService");
export const ICSVLoaderServiceInterface = Symbol("ICSVLoaderService");
export const IPictographTransformationServiceInterface = Symbol("IPictographTransformationService");
export const IOptionFilteringServiceInterface = Symbol("IOptionFilteringService");

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

  container.registerFactory(ICSVLoaderServiceInterface, () => {
    return new CSVLoaderService();
  });

  // Register transformation services (depend on enum mapping)
  container.registerFactory(IPictographTransformationServiceInterface, () => {
    const enumMappingService = container.resolve(IEnumMappingServiceInterface) as IEnumMappingService;
    return new PictographTransformationService(enumMappingService);
  });

  // Register filtering services (depend on enum mapping)
  container.registerFactory(IOptionFilteringServiceInterface, () => {
    const enumMappingService = container.resolve(IEnumMappingServiceInterface) as IEnumMappingService;
    return new OptionFilteringService(enumMappingService);
  });
}

/**
 * Helper function to resolve shared services with proper typing
 */
export function resolveSharedServices(container: ServiceContainer) {
  return {
    enumMappingService: container.resolve(IEnumMappingServiceInterface) as IEnumMappingService,
    csvParserService: container.resolve(ICSVParserServiceInterface) as ICSVParserService,
    csvLoaderService: container.resolve(ICSVLoaderServiceInterface) as ICSVLoaderService,
    pictographTransformationService: container.resolve(IPictographTransformationServiceInterface),
    optionFilteringService: container.resolve(IOptionFilteringServiceInterface),
  };
}
