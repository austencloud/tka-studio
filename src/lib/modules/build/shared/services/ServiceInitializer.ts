/**
 * Service Initializer
 *
 * Centralized service resolution and initialization for BuildTab.
 * Extracts service management logic from BuildTab.svelte to improve testability
 * and follow Single Responsibility Principle.
 *
 * Domain: Build Module - Service Management
 */

import { resolve, TYPES } from "$shared";
import type { IStartPositionService } from "../../construct/start-position-picker/services/contracts";
import type { IShareService } from "../../share/services/contracts";
import type {
  IBeatOperationsService,
  IBuildTabService,
  INavigationSyncService,
  IResponsiveLayoutService,
  ISequencePersistenceService,
  ISequenceService
} from "./contracts";

/**
 * Container for all BuildTab services
 */
export interface BuildTabServices {
  sequenceService: ISequenceService;
  sequencePersistenceService: ISequencePersistenceService;
  startPositionService: IStartPositionService;
  buildTabService: IBuildTabService;
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
  static resolveServices(): BuildTabServices {
    try {
      return {
        sequenceService: resolve<ISequenceService>(TYPES.ISequenceService),
        sequencePersistenceService: resolve<ISequencePersistenceService>(TYPES.ISequencePersistenceService),
        startPositionService: resolve<IStartPositionService>(TYPES.IStartPositionService),
        buildTabService: resolve<IBuildTabService>(TYPES.IBuildTabService),
        layoutService: resolve<IResponsiveLayoutService>(TYPES.IResponsiveLayoutService),
        navigationSyncService: resolve<INavigationSyncService>(TYPES.INavigationSyncService),
        beatOperationsService: resolve<IBeatOperationsService>(TYPES.IBeatOperationsService),
        shareService: resolve<IShareService>(TYPES.IShareService)
      };
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unknown error resolving services";
      throw new Error(`Failed to resolve BuildTab services: ${message}`);
    }
  }

  /**
   * Initialize services that require async setup
   */
  static async initializeServices(services: BuildTabServices): Promise<void> {
    await services.buildTabService.initialize();
  }
}
