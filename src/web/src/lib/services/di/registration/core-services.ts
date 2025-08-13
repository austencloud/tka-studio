/**
 * Core Services Registration
 * Handles registration of core business logic and infrastructure services
 */

import type { ServiceContainer } from "../ServiceContainer";
import {
  IApplicationInitializationServiceInterface,
  IConstructTabCoordinationServiceInterface,
  IDeviceDetectionServiceInterface,
  IExportServiceInterface,
  IMotionGenerationServiceInterface,
  IOptionDataServiceInterface,
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
} from "../interfaces/core-interfaces";

import { ApplicationInitializationService } from "../../implementations/ApplicationInitializationService";
import { ConstructTabCoordinationService } from "../../implementations/ConstructTabCoordinationService";
import { PictographRenderingService } from "../../implementations/PictographRenderingService";
import { SequenceService } from "../../implementations/SequenceService";

import { IArrowPositioningServiceInterface } from "../interfaces/positioning-interfaces";

/**
 * Register all core services with their dependencies
 */
export async function registerCoreServices(
  container: ServiceContainer,
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

  // Register rendering services
  container.registerSingletonClass(IPropRenderingServiceInterface);

  // Register services with dependencies using factories
  container.registerFactory(ISequenceServiceInterface, () => {
    const sequenceDomainService = container.resolve(
      ISequenceDomainServiceInterface,
    );
    const persistenceService = container.resolve(IPersistenceServiceInterface);
    return new SequenceService(sequenceDomainService, persistenceService);
  });

  container.registerFactory(IConstructTabCoordinationServiceInterface, () => {
    const sequenceService = container.resolve(ISequenceServiceInterface);
    const startPositionService = container.resolve(
      IStartPositionServiceInterface,
    );
    return new ConstructTabCoordinationService(
      sequenceService,
      startPositionService,
    );
  });

  // Register pictograph rendering service (depends on positioning services)
  container.registerFactory(IPictographRenderingServiceInterface, () => {
    const arrowPositioning = container.resolve(
      IArrowPositioningServiceInterface,
    );
    const propRendering = container.resolve(IPropRenderingServiceInterface);
    return new PictographRenderingService(arrowPositioning, propRendering);
  });

  // Register pictograph service (no dependencies after rendering is registered)
  container.registerSingletonClass(IPictographServiceInterface);

  // Register export service
  container.registerSingletonClass(IExportServiceInterface);

  // Register generation services
  container.registerSingletonClass(IMotionGenerationServiceInterface);
  container.registerSingletonClass(ISequenceGenerationServiceInterface);

  // Register application initialization service with factory
  container.registerFactory(IApplicationInitializationServiceInterface, () => {
    const settingsService = container.resolve(ISettingsServiceInterface);
    const persistenceService = container.resolve(IPersistenceServiceInterface);
    return new ApplicationInitializationService(
      settingsService,
      persistenceService,
    );
  });
}
