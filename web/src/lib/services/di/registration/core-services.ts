/**
 * Core Services Registration
 * Handles registration of core business logic and infrastructure services
 */

import type { ServiceContainer } from "../ServiceContainer";
import {
  IApplicationInitializationServiceInterface,
  IArrowRenderingServiceInterface,
  IConstructTabCoordinationServiceInterface,
  IDataTransformationServiceInterface,
  IDeviceDetectionServiceInterface,
  IExportServiceInterface,
  IGridRenderingServiceInterface,
  IMotionGenerationServiceInterface,
  IOptionDataServiceInterface,
  IOrientationCalculationServiceInterface,
  IOverlayRenderingServiceInterface,
  IPanelManagementServiceInterface,
  IPersistenceServiceInterface,
  IPictographRenderingServiceInterface,
  IPictographServiceInterface,
  IPropRenderingServiceInterface,
  ISequenceDomainServiceInterface,
  ISequenceGenerationServiceInterface,
  ISequenceServiceInterface,
  ISettingsServiceInterface,
  IStartPositionServiceInterface,
  ISvgConfigurationInterface,
  ISvgUtilityServiceInterface,
  IPrintablePageLayoutServiceInterface,
  IPageFactoryServiceInterface,
  IPageImageExportServiceInterface,
  ISequenceCardExportIntegrationServiceInterface,
} from "../interfaces/core-interfaces";

import { ApplicationInitializationService } from "../../implementations/ApplicationInitializationService";
import { ConstructTabCoordinationService } from "../../implementations/ConstructTabCoordinationService";
import { PictographRenderingService } from "../../implementations/PictographRenderingService";
import { SequenceService } from "../../implementations/SequenceService";
import { SequenceGenerationService } from "../../implementations/SequenceGenerationService";

import { IArrowPositioningOrchestratorInterface } from "../interfaces/positioning-interfaces";
import type { IArrowPositioningOrchestrator } from "../../positioning/core-services";

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

  // Register construct tab services
  container.registerSingletonClass(IStartPositionServiceInterface);
  container.registerSingletonClass(IOptionDataServiceInterface);

  // Register rendering microservices (in dependency order)
  container.registerSingletonClass(ISvgConfigurationInterface);
  container.registerSingletonClass(ISvgUtilityServiceInterface);
  container.registerSingletonClass(IDataTransformationServiceInterface);
  container.registerSingletonClass(IGridRenderingServiceInterface);
  container.registerSingletonClass(IArrowRenderingServiceInterface);
  container.registerSingletonClass(IOverlayRenderingServiceInterface);

  // Register main rendering services
  container.registerSingletonClass(IPropRenderingServiceInterface);

  // Register services with dependencies using factories
  container.registerFactory(ISequenceServiceInterface, () => {
    const sequenceDomainService = container.resolve(
      ISequenceDomainServiceInterface
    );
    const persistenceService = container.resolve(IPersistenceServiceInterface);
    return new SequenceService(sequenceDomainService, persistenceService);
  });

  container.registerFactory(IConstructTabCoordinationServiceInterface, () => {
    const sequenceService = container.resolve(ISequenceServiceInterface);
    const startPositionService = container.resolve(
      IStartPositionServiceInterface
    );
    return new ConstructTabCoordinationService(
      sequenceService,
      startPositionService
    );
  });

  // Register pictograph rendering service (depends on positioning and microservices)
  container.registerFactory(IPictographRenderingServiceInterface, () => {
    const arrowPositioning = container.resolve(
      IArrowPositioningOrchestratorInterface
    ) as IArrowPositioningOrchestrator;
    const propRendering = container.resolve(IPropRenderingServiceInterface);
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
      propRendering,
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
    const optionDataService = container.resolve(IOptionDataServiceInterface);
    const orientationCalculationService = container.resolve(
      IOrientationCalculationServiceInterface
    );
    return new SequenceGenerationService(
      optionDataService,
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
}
