/**
 * Create Module Initialization Service Contract
 *
 * Handles all initialization logic for CreateModule including:
 * - Service resolution
 * - State object creation
 * - Persistence initialization
 * - Start position loading
 * - Event service configuration
 *
 * Extracted from CreateModule.svelte onMount monolith.
 */

import type { GridMode } from "$shared";
import type { PanelCoordinationState } from "../../state/panel-coordination-state.svelte";
import type { IBeatOperationsService } from "./IBeatOperationsService";
import type { INavigationSyncService } from "./INavigationSyncService";
import type { IResponsiveLayoutService } from "./IResponsiveLayoutService";

export interface CreateModuleInitializationResult {
  sequenceService: any;
  sequencePersistenceService: any;
  startPositionService: any;
  CreateModuleService: any;
  CreateModuleState: any;
  constructTabState: any;
  layoutService: IResponsiveLayoutService;
  navigationSyncService: INavigationSyncService;
  beatOperationsService: IBeatOperationsService;
}

export interface ICreateModuleInitializationService {
  /**
   * Initialize all services and state for CreateModule
   * @returns Initialized services and state objects
   * @throws Error if initialization fails
   */
  initialize(): Promise<CreateModuleInitializationResult>;

  /**
   * Configure event service callbacks for sequence operations
   * @param CreateModuleState Create Module State object
   * @param panelState Panel coordination state for callback handlers
   */
  configureEventCallbacks(
    CreateModuleState: any,
    panelState: PanelCoordinationState
  ): void;

  /**
   * Configure clear sequence callback
   * @param CreateModuleState Create Module State object
   * @param constructTabState Construct tab state for clearing
   */
  configureClearSequenceCallback(
    CreateModuleState: any,
    constructTabState: any
  ): void;

  /**
   * Load default start positions for a grid mode
   * @param gridMode Grid mode to load start positions for
   */
  loadStartPositions(gridMode: GridMode): Promise<void>;
}
