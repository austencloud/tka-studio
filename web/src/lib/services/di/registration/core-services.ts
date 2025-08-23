/**
 * Core Services Registration
 * Handles registration of core business logic and infrastructure services
 */

import type { ServiceContainer } from "../ServiceContainer";
import { IBeatFrameServiceInterface } from "../interfaces/beat-frame-interfaces";
import { ILetterQueryServiceInterface } from "../interfaces/codex-interfaces";
import {
  IApplicationInitializationServiceInterface,
  IArrowRenderingServiceInterface,
  IBeatFallbackRenderingServiceInterface,
  IBeatGridServiceInterface,
  IConstructTabCoordinationServiceInterface,
  IDataTransformationServiceInterface,
  IDeviceDetectionServiceInterface,
  IExportServiceInterface,
  IGridRenderingServiceInterface,
  IImageFormatConverterServiceInterface,
  IMotionGenerationServiceInterface,
  IOrientationCalculationServiceInterface,
  IOverlayRenderingServiceInterface,
  IPageFactoryServiceInterface,
  IPageImageExportServiceInterface,
  IPanelManagementServiceInterface,
  IPersistenceServiceInterface,
  IPictographRenderingServiceInterface,
  IPictographServiceInterface,
  IPrintablePageLayoutServiceInterface,
  // ✅ REMOVED: PropRenderingService is deprecated
  IPropCoordinatorServiceInterface,
  ISequenceCardExportIntegrationServiceInterface,
  ISequenceDeletionServiceInterface,
  ISequenceDomainServiceInterface,
  ISequenceGenerationServiceInterface,
  ISequenceImportServiceInterface,
  ISequenceServiceInterface,
  ISettingsServiceInterface,
  IStartPositionSelectionServiceInterface,
  IStartPositionServiceInterface,
  ISvgConfigurationInterface,
  // New conversion and rendering microservices
  ISVGToCanvasConverterServiceInterface,
  ISvgUtilityServiceInterface,
  IWorkbenchBeatOperationsServiceInterface,
} from "../interfaces/core-interfaces";
import { ISequenceStateServiceInterface } from "../interfaces/sequence-state-interfaces";
import {
  IWorkbenchCoordinationServiceInterface,
  IWorkbenchServiceInterface,
} from "../interfaces/workbench-interfaces";

import { ApplicationInitializationService } from "../../implementations/application/ApplicationInitializationService";
import { ConstructTabCoordinationService } from "../../implementations/construct/ConstructTabCoordinationService";
import { SequenceGenerationService } from "../../implementations/generation/SequenceGenerationService";
import { PictographRenderingService } from "../../implementations/rendering/PictographRenderingService";
import { SequenceDeletionService } from "../../implementations/sequence/SequenceDeletionService";
import { SequenceImportService } from "../../implementations/sequence/SequenceImportService";
import { SequenceService } from "../../implementations/sequence/SequenceService";
import { WorkbenchBeatOperationsService } from "../../implementations/sequence/WorkbenchBeatOperationsService";

import type { IArrowPositioningOrchestrator } from "../../positioning/core-services";
import { IArrowPositioningOrchestratorInterface } from "../interfaces/positioning-interfaces";

/**
 * Register all core services with their dependencies
 */
export async function registerCoreServices(
  container: ServiceContainer
): Promise<void> {
  // Register domain services (no dependencies)
  container.registerSingletonClass(ISequenceDomainServiceInterface);

  // Register infrastructure services
  container.registerSingletonClass(IPersistenceServiceInterface);
  container.registerSingletonClass(ISettingsServiceInterface);
  container.registerSingletonClass(IDeviceDetectionServiceInterface);
  container.registerSingletonClass(IPanelManagementServiceInterface);

  // Register layout services
  container.registerSingletonClass(IBeatFrameServiceInterface);

  // Register sequence state services
  container.registerSingletonClass(ISequenceStateServiceInterface);

  // Register workbench services
  container.registerSingletonClass(IWorkbenchServiceInterface);
  container.registerSingletonClass(IWorkbenchCoordinationServiceInterface);

  // Register construct tab services
  container.registerSingletonClass(IStartPositionServiceInterface);
  container.registerSingletonClass(IStartPositionSelectionServiceInterface);

  // Register rendering microservices (in dependency order)
  container.registerSingletonClass(ISvgConfigurationInterface);
  container.registerSingletonClass(ISvgUtilityServiceInterface);
  container.registerSingletonClass(IDataTransformationServiceInterface);
  container.registerSingletonClass(IGridRenderingServiceInterface);
  container.registerSingletonClass(IArrowRenderingServiceInterface);
  container.registerSingletonClass(IOverlayRenderingServiceInterface);

  // Register main rendering services
  // ✅ REMOVED: PropRenderingService is deprecated
  container.registerSingletonClass(IPropCoordinatorServiceInterface);

  // Register sequence services
  container.registerFactory(ISequenceImportServiceInterface, () => {
    return new SequenceImportService();
  });

  container.registerFactory(ISequenceDeletionServiceInterface, () => {
    const sequenceService = container.resolve(ISequenceServiceInterface);
    const persistenceService = container.resolve(IPersistenceServiceInterface);
    return new SequenceDeletionService(sequenceService, persistenceService);
  });

  container.registerFactory(IWorkbenchBeatOperationsServiceInterface, () => {
    const sequenceService = container.resolve(ISequenceServiceInterface);
    const persistenceService = container.resolve(IPersistenceServiceInterface);
    return new WorkbenchBeatOperationsService(
      sequenceService,
      persistenceService
    );
  });

  container.registerFactory(ISequenceServiceInterface, () => {
    const sequenceDomainService = container.resolve(
      ISequenceDomainServiceInterface
    );
    const persistenceService = container.resolve(IPersistenceServiceInterface);
    const sequenceImportService = container.resolve(
      ISequenceImportServiceInterface
    );
    return new SequenceService(
      sequenceDomainService,
      persistenceService,
      sequenceImportService
    );
  });

  container.registerFactory(IConstructTabCoordinationServiceInterface, () => {
    const sequenceService = container.resolve(ISequenceServiceInterface);
    const startPositionService = container.resolve(
      IStartPositionServiceInterface
    );
    const workbenchBeatOperations = container.resolve(
      IWorkbenchBeatOperationsServiceInterface
    );
    return new ConstructTabCoordinationService(
      sequenceService,
      startPositionService,
      workbenchBeatOperations
    );
  });

  // Register pictograph rendering service (depends on positioning and microservices)
  container.registerFactory(IPictographRenderingServiceInterface, () => {
    const arrowPositioning = container.resolve(
      IArrowPositioningOrchestratorInterface
    ) as IArrowPositioningOrchestrator;
    // ✅ REMOVED: PropRenderingService is deprecated
    const svgUtility = container.resolve(ISvgUtilityServiceInterface);
    const gridRendering = container.resolve(IGridRenderingServiceInterface);
    const arrowRendering = container.resolve(IArrowRenderingServiceInterface);
    const overlayRendering = container.resolve(
      IOverlayRenderingServiceInterface
    );
    const dataTransformation = container.resolve(
      IDataTransformationServiceInterface
    );
    return new PictographRenderingService(
      arrowPositioning,
      null, // ✅ FIXED: PropRenderingService is deprecated, pass null
      svgUtility,
      gridRendering,
      arrowRendering,
      overlayRendering,
      dataTransformation
    );
  });

  // Register pictograph service (no dependencies after rendering is registered)
  container.registerSingletonClass(IPictographServiceInterface);

  // Register export service
  container.registerSingletonClass(IExportServiceInterface);

  // Register generation services
  container.registerSingletonClass(IMotionGenerationServiceInterface);
  container.registerSingletonClass(IOrientationCalculationServiceInterface);

  // Register sequence generation service with dependencies
  container.registerFactory(ISequenceGenerationServiceInterface, () => {
    const letterQueryService = container.resolve(ILetterQueryServiceInterface);
    const orientationCalculationService = container.resolve(
      IOrientationCalculationServiceInterface
    );
    return new SequenceGenerationService(
      letterQueryService,
      orientationCalculationService
    );
  });

  // Register page layout and export services
  container.registerSingletonClass(IPrintablePageLayoutServiceInterface);
  container.registerSingletonClass(IPageImageExportServiceInterface);

  // Register page factory service with dependency
  container.registerFactory(IPageFactoryServiceInterface, () => {
    const layoutService = container.resolve(
      IPrintablePageLayoutServiceInterface
    );
    return new IPageFactoryServiceInterface.implementation(layoutService);
  });

  // Register export integration service with dependency
  container.registerFactory(
    ISequenceCardExportIntegrationServiceInterface,
    () => {
      const pageImageExportService = container.resolve(
        IPageImageExportServiceInterface
      );
      return new ISequenceCardExportIntegrationServiceInterface.implementation(
        pageImageExportService
      );
    }
  );

  // Register application initialization service with factory
  container.registerFactory(IApplicationInitializationServiceInterface, () => {
    const settingsService = container.resolve(ISettingsServiceInterface);
    const persistenceService = container.resolve(IPersistenceServiceInterface);
    return new ApplicationInitializationService(
      settingsService,
      persistenceService
    );
  });

  // Register new conversion and rendering microservices
  container.registerSingletonClass(ISVGToCanvasConverterServiceInterface);
  container.registerSingletonClass(IImageFormatConverterServiceInterface);
  container.registerSingletonClass(IBeatGridServiceInterface);

  // Register beat fallback service (no dependencies needed)
  container.registerSingletonClass(IBeatFallbackRenderingServiceInterface);
}
