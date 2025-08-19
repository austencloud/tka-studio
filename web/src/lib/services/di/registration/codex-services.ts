/**
 * Codex Services Registration
 *
 * Registers all codex-related services with the DI container.
 */

import type { ServiceContainer } from "../ServiceContainer";
import { LetterMappingRepository } from "$lib/repositories/LetterMappingRepository";
import { LessonRepository } from "$lib/repositories/LessonRepository";
import { PictographQueryService } from "$lib/services/codex/PictographQueryService";
import { PictographOperationsService } from "$lib/services/codex/PictographOperationsService";
import { CodexService } from "$lib/services/codex/CodexService";
import {
  ICodexServiceInterface,
  ILetterMappingRepositoryInterface,
  ILessonRepositoryInterface,
  IPictographQueryServiceInterface,
  IPictographOperationsServiceInterface,
  ICsvDataServiceInterface,
} from "../interfaces/codex-interfaces";
import { CsvDataService } from "../../implementations/CsvDataService";
import { IOptionDataServiceInterface } from "../interfaces/core-interfaces";
import { OptionDataService } from "../../implementations/OptionDataService";

/**
 * Register all codex services with their dependencies
 */
export async function registerCodexServices(
  container: ServiceContainer
): Promise<void> {
  // Register repositories and data services (no dependencies)
  container.registerFactory(ILetterMappingRepositoryInterface, () => {
    return new LetterMappingRepository();
  });

  container.registerFactory(ICsvDataServiceInterface, () => {
    return new CsvDataService();
  });

  // Register lesson repository (depends on letter mapping repository)
  container.registerFactory(ILessonRepositoryInterface, () => {
    const letterMappingRepo = container.resolve(
      ILetterMappingRepositoryInterface
    );
    return new LessonRepository(letterMappingRepo);
  });

  // Register pictograph query service (depends on letter mapping repository, csv data service, and option data service)
  container.registerFactory(IPictographQueryServiceInterface, () => {
    const letterMappingRepo = container.resolve(
      ILetterMappingRepositoryInterface
    );
    const csvDataService = container.resolve(ICsvDataServiceInterface);
    const optionDataService = container.resolve(IOptionDataServiceInterface);
    return new PictographQueryService(
      letterMappingRepo,
      csvDataService,
      optionDataService as OptionDataService // Type assertion to handle interface/implementation mismatch
    );
  });

  // Register pictograph operations service (no dependencies)
  container.registerFactory(IPictographOperationsServiceInterface, () => {
    return new PictographOperationsService();
  });

  // Register main codex service (depends on all the above)
  container.registerFactory(ICodexServiceInterface, () => {
    const letterMappingRepo = container.resolve(
      ILetterMappingRepositoryInterface
    );
    const lessonRepo = container.resolve(ILessonRepositoryInterface);
    const pictographQueryService = container.resolve(
      IPictographQueryServiceInterface
    );
    const operationsService = container.resolve(
      IPictographOperationsServiceInterface
    );

    return new CodexService(
      letterMappingRepo,
      lessonRepo,
      pictographQueryService,
      operationsService
    );
  });

  console.log("✅ Codex services registered with DI container");
}
