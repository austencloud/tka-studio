import type { IDeviceDetector, IViewportService } from "$shared";
import { ensureContainerInitialized, GridMode, resolve } from "$shared";
import { TYPES } from "$shared/inversify/types";
import type { IStartPositionService } from "../../construct/start-position-picker/services/contracts";
import type {
  CreateModuleServices,
  CreateModuleStates,
  InitializationResult,
  InitializationStatus,
} from "../orchestration/types";
import type {
  ICreateModuleService,
  ISequencePersistenceService,
  ISequenceService,
} from "../services/contracts";
import { getCreateModuleEventService } from "../services/implementations/CreateModuleEventService";
import { createCreateModuleState, createConstructTabState } from "../state";

/**
 * Handles all CreateModule initialization logic in one place
 * Extracted from CreateModule.svelte onMount to improve testability
 */
export class CreateModuleInitializer {
  /**
   * Resolve all required services from DI container
   */
  async resolveServices(): Promise<CreateModuleServices> {
    await ensureContainerInitialized();

    const services: CreateModuleServices = {
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
      deviceDetector: resolve<IDeviceDetector>(TYPES.IDeviceDetector),
      viewportService: resolve<IViewportService>(TYPES.IViewportService),
    };

    // Validate all services resolved successfully
    const missingServices = Object.entries(services)
      .filter(([_, service]) => !service)
      .map(([key]) => key);

    if (missingServices.length > 0) {
      throw new Error(
        `Failed to resolve services: ${missingServices.join(", ")}`
      );
    }

    return services;
  }

  /**
   * Create state factories from resolved services
   */
  async createStates(
    services: CreateModuleServices
  ): Promise<CreateModuleStates> {
    const { sequenceService, sequencePersistenceService, CreateModuleService } =
      services;

    // Wait a tick to ensure component context is fully established
    await new Promise((resolve) => setTimeout(resolve, 0));

    const CreateModuleState = createCreateModuleState(
      sequenceService,
      sequencePersistenceService
    );

    const constructTabState = createConstructTabState(
      CreateModuleService,
      CreateModuleState.sequenceState,
      sequencePersistenceService
    );

    return { CreateModuleState, constructTabState };
  }

  /**
   * Initialize services and wire up callbacks
   */
  async initializeServices(
    services: CreateModuleServices,
    states: CreateModuleStates
  ): Promise<void> {
    const { CreateModuleService, startPositionService } = services;
    const { CreateModuleState } = states;

    // Initialize Create Module Service
    await CreateModuleService.initialize();

    // Set up sequence state callbacks for CreateModuleEventService
    const CreateModuleEventService = getCreateModuleEventService();
    CreateModuleEventService.setSequenceStateCallbacks(
      () => CreateModuleState.sequenceState.getCurrentSequence(),
      (sequence) => CreateModuleState.sequenceState.setCurrentSequence(sequence)
    );

    // Set up option history callback
    CreateModuleEventService.setAddOptionToHistoryCallback(
      (beatIndex, beatData) =>
        CreateModuleState.addOptionToHistory(beatIndex, beatData)
    );

    // Load start positions
    await startPositionService.getDefaultStartPositions(GridMode.DIAMOND);
  }

  /**
   * Initialize states with persisted data
   */
  async initializeStates(states: CreateModuleStates): Promise<void> {
    const { CreateModuleState, constructTabState } = states;

    await CreateModuleState.initializeWithPersistence();
    await constructTabState.initializeConstructTab();
  }

  /**
   * Main initialization - orchestrates all setup steps with error handling and performance tracking
   */
  async initialize(): Promise<InitializationResult> {
    const startTime = performance.now();

    try {
      // Step 1: Resolve services
      const services = await this.resolveServices();

      // Step 2: Create state factories
      const states = await this.createStates(services);

      // Step 3: Initialize services and wire up callbacks
      await this.initializeServices(services, states);

      // Step 4: Load persisted data
      await this.initializeStates(states);

      const initTime = performance.now() - startTime;
      console.log(`✅ CreateModule initialized in ${initTime.toFixed(2)}ms`);

      // Success status
      const status: InitializationStatus = {
        servicesResolved: true,
        statesInitialized: true,
        persistenceLoaded: true,
        ready: true,
      };

      return {
        services,
        states,
        status,
      };
    } catch (error) {
      const initTime = performance.now() - startTime;
      console.error(
        `❌ CreateModule initialization failed after ${initTime.toFixed(2)}ms:`,
        error
      );

      // Error status
      const status: InitializationStatus = {
        servicesResolved: false,
        statesInitialized: false,
        persistenceLoaded: false,
        ready: false,
        error: error instanceof Error ? error.message : String(error),
      };

      throw new Error(`CreateModule initialization failed: ${status.error}`);
    }
  }
}
