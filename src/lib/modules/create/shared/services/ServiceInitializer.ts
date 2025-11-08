/**
 * Service Initializer
 *
 * Centralized service resolution and initialization for CreateModule.
 * Extracts service management logic from CreateModule.svelte to improve testability
 * and follow Single Responsibility Principle.
 *
 * Domain: Create module - Service Management
 */

import { resolve, TYPES } from "$shared";
import type { IStartPositionService } from "../../construct/start-position-picker/services/contracts";
import type { IShareService } from "../../share/services/contracts";
import type {
  IBeatOperationsService,
  ICreateModuleService,
  INavigationSyncService,
  IResponsiveLayoutService,
  ISequencePersistenceService,
  ISequenceService,
} from "./contracts";

/**
 * Container for all CreateModule services
 */
export interface CreateModuleServices {
  sequenceService: ISequenceService;
  sequencePersistenceService: ISequencePersistenceService;
  startPositionService: IStartPositionService;
  CreateModuleService: ICreateModuleService;
  layoutService: IResponsiveLayoutService;
  navigationSyncService: INavigationSyncService;
  beatOperationsService: IBeatOperationsService;
  shareService: IShareService;
}

/**
 * Service Initializer
 * Resolves all services from DI container and handles initialization
 */
export class ServiceInitializer {
  /**
   * Resolve all required services from DI container
   * @throws Error if any service cannot be resolved
   */
  static resolveServices(): CreateModuleServices {
    try {
      return {
        sequenceService: resolve<ISequenceService>(TYPES.ISequenceService),
        sequencePersistenceService: resolve<ISequencePersistenceService>(
          TYPES.ISequencePersistenceService
        ),
        startPositionService: resolve<IStartPositionService>(
          TYPES.IStartPositionService
        ),
        CreateModuleService: resolve<ICreateModuleService>(
          TYPES.ICreateModuleService
        ),
        layoutService: resolve<IResponsiveLayoutService>(
          TYPES.IResponsiveLayoutService
        ),
        navigationSyncService: resolve<INavigationSyncService>(
          TYPES.INavigationSyncService
        ),
        beatOperationsService: resolve<IBeatOperationsService>(
          TYPES.IBeatOperationsService
        ),
        shareService: resolve<IShareService>(TYPES.IShareService),
      };
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : "Unknown error resolving services";
      throw new Error(`Failed to resolve CreateModule services: ${message}`);
    }
  }

  /**
   * Initialize services that require async setup
   */
  static async initializeServices(
    services: CreateModuleServices
  ): Promise<void> {
    await services.CreateModuleService.initialize();
  }
}
