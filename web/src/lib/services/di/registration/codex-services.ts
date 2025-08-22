/**
 * Codex Services Registration
 *
 * Registers all codex-related services with the DI container.
 */

import { LessonRepository } from "$lib/repositories/LessonRepository";
import { LetterMappingRepository } from "$lib/repositories/LetterMappingRepository";
import { CodexService } from "$lib/services/codex/CodexService";
import { PictographOperationsService } from "$lib/services/codex/PictographOperationsService";
import { CsvLoaderService } from "../../implementations/data/CsvLoaderService";
import { LetterQueryService } from "../../implementations/data/LetterQueryService";
import { MotionQueryService } from "../../implementations/data/MotionQueryService";
import {
  ICodexServiceInterface,
  ICsvLoaderServiceInterface,
  ILessonRepositoryInterface,
  ILetterMappingRepositoryInterface,
  ILetterQueryServiceInterface,
  IMotionQueryServiceInterface,
  IPictographOperationsServiceInterface,
} from "../interfaces/codex-interfaces";
import type { ServiceContainer } from "../ServiceContainer";
import {
  ICSVParserServiceInterface,
  IPictographTransformationServiceInterface,
} from "./shared-services";

/**
 * Register all codex services with their dependencies as singletons
 */
export async function registerCodexServices(
  container: ServiceContainer
): Promise<void> {
  // Register repositories and data services as singletons (no dependencies)
  container.registerSingleton(
    ILetterMappingRepositoryInterface,
    new LetterMappingRepository()
  );

  // 1. Register CsvLoaderService (no dependencies)
  container.registerSingleton(
    ICsvLoaderServiceInterface,
    new CsvLoaderService()
  );

  // 2. Register LetterQueryService with dependencies
  container.registerFactory(ILetterQueryServiceInterface, () => {
    const letterMappingRepo = container.resolve(
      ILetterMappingRepositoryInterface
    );
    const csvLoaderService = container.resolve(ICsvLoaderServiceInterface);
    const csvParserService = container.resolve(ICSVParserServiceInterface);
    const pictographTransformationService = container.resolve(
      IPictographTransformationServiceInterface
    );

    return new LetterQueryService(
      letterMappingRepo,
      csvLoaderService,
      csvParserService,
      pictographTransformationService
    );
  });

  // 3. Register MotionQueryService with dependencies
  container.registerFactory(IMotionQueryServiceInterface, () => {
    const csvLoaderService = container.resolve(ICsvLoaderServiceInterface);
    const csvParserService = container.resolve(ICSVParserServiceInterface);
    const pictographTransformationService = container.resolve(
      IPictographTransformationServiceInterface
    );

    return new MotionQueryService(
      csvLoaderService,
      csvParserService,
      pictographTransformationService
    );
  });

  // Register lesson repository as singleton (depends on letter mapping repository)
  const letterMappingRepo = container.resolve(
    ILetterMappingRepositoryInterface
  );
  container.registerSingleton(
    ILessonRepositoryInterface,
    new LessonRepository(letterMappingRepo)
  );

  // Register pictograph operations service as singleton (no dependencies)
  container.registerSingleton(
    IPictographOperationsServiceInterface,
    new PictographOperationsService()
  );

  // Register main codex service as singleton (depends on all the above)
  const lessonRepo = container.resolve(ILessonRepositoryInterface);

  const operationsService = container.resolve(
    IPictographOperationsServiceInterface
  );
  const letterQueryService = container.resolve(ILetterQueryServiceInterface);

  container.registerSingleton(
    ICodexServiceInterface,
    new CodexService(
      letterMappingRepo,
      lessonRepo,
      operationsService,
      letterQueryService
    )
  );

  console.log("✅ Codex services registered with DI container");
}
