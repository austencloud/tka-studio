/**
 * CreateModule Orchestration Types
 *
 * Central type definitions for the CreateModule orchestration architecture.
 * These types define the contracts between different layers of the system.
 */

import type { IDeviceDetector, IViewportService } from "$shared";
import type { IStartPositionService } from "../../construct/start-position-picker/services/contracts";
import type {
  ICreateModuleService,
  ISequencePersistenceService,
  ISequenceService,
} from "../services/contracts";
import type { createCreateModuleState } from "../state/create-module-state.svelte";
import type { createConstructTabState } from "../state/construct-tab-state.svelte";

/**
 * Collection of all services required by CreateModule
 */
export interface CreateModuleServices {
  sequenceService: ISequenceService;
  sequencePersistenceService: ISequencePersistenceService;
  startPositionService: IStartPositionService;
  CreateModuleService: ICreateModuleService;
  deviceDetector: IDeviceDetector;
  viewportService: IViewportService;
}

/**
 * Collection of all state objects used by CreateModule
 */
export interface CreateModuleStates {
  CreateModuleState: ReturnType<typeof createCreateModuleState>;
  constructTabState: ReturnType<typeof createConstructTabState>;
}

/**
 * Layout configuration for responsive layout management
 */
export interface LayoutConfiguration {
  /** Navigation layout position: top for desktop/tablet, left for landscape mobile, bottom for portrait mobile */
  navigationLayout: "top" | "left" | "bottom";

  /** Whether panels should be side-by-side (true) or stacked (false) */
  shouldUseSideBySideLayout: boolean;

  /** Current viewport width in pixels */
  viewportWidth: number;

  /** Current viewport height in pixels */
  viewportHeight: number;

  /** Whether device is detected as desktop */
  isDesktop: boolean;

  /** Whether device is in landscape mobile mode */
  isLandscapeMobile: boolean;

  /** Aspect ratio (width / height) */
  aspectRatio: number;

  /** Whether device is likely Z Fold unfolded */
  isLikelyZFoldUnfolded: boolean;
}

/**
 * Initialization status tracking
 */
export interface InitializationStatus {
  /** Whether all services have been resolved */
  servicesResolved: boolean;

  /** Whether state factories have been initialized */
  statesInitialized: boolean;

  /** Whether persistence has been loaded */
  persistenceLoaded: boolean;

  /** Whether initialization is complete and system is ready */
  ready: boolean;

  /** Any error that occurred during initialization */
  error?: string;
}

/**
 * Result of initialization process
 */
export interface InitializationResult {
  services: CreateModuleServices;
  states: CreateModuleStates;
  status: InitializationStatus;
}
