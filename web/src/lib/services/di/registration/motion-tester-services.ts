/**
 * Motion Tester Services Registration
 *
 * Registers all services related to the motion tester functionality
 * following the TKA DI container pattern.
 */

import type { ServiceContainer } from "../ServiceContainer";
import {
  IAnimatedPictographDataServiceInterface,
  IMotionTesterCsvLookupServiceInterface,
} from "../interfaces/motion-tester-interfaces";
import { IOptionDataServiceInterface } from "../interfaces/core-interfaces";
import { CsvDataService } from "../../implementations/CsvDataService";

/**
 * Register all motion tester services
 */
export async function registerMotionTesterServices(
  container: ServiceContainer
): Promise<void> {
  // Register CSV Lookup Service with dependencies first
  container.registerFactory(IMotionTesterCsvLookupServiceInterface, () => {
    const csvDataService = new CsvDataService(); // Create instance directly
    const optionDataService = container.resolve(IOptionDataServiceInterface);
    return new IMotionTesterCsvLookupServiceInterface.implementation(
      csvDataService,
      optionDataService
    );
  });

  // Register AnimatedPictographDataService with CSV lookup dependency
  container.registerFactory(IAnimatedPictographDataServiceInterface, () => {
    const csvLookupService = container.resolve(
      IMotionTesterCsvLookupServiceInterface
    );
    return new IAnimatedPictographDataServiceInterface.implementation(
      csvLookupService
    );
  });

  console.log("✅ Motion tester services registered successfully");
}
