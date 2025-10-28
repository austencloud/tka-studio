/**
 * Build Tab Initialization Service Contract
 *
 * Handles all initialization logic for BuildTab including:
 * - Service resolution
 * - State object creation
 * - Persistence initialization
 * - Start position loading
 * - Event service configuration
 *
 * Extracted from BuildTab.svelte onMount monolith.
 */

import type { GridMode } from "$shared";
import type { PanelCoordinationState } from "../../state/panel-coordination-state.svelte";
import type { IBeatOperationsService } from "./IBeatOperationsService";
import type { IBuildTabResponsiveLayoutService } from "./IBuildTabResponsiveLayoutService";
import type { INavigationSyncService } from "./INavigationSyncService";

export interface BuildTabInitializationResult {
  sequenceService: any;
  sequencePersistenceService: any;
  startPositionService: any;
  buildTabService: any;
  buildTabState: any;
  constructTabState: any;
  layoutService: IBuildTabResponsiveLayoutService;
  navigationSyncService: INavigationSyncService;
  beatOperationsService: IBeatOperationsService;
}

export interface IBuildTabInitializationService {
  /**
   * Initialize all services and state for BuildTab
   * @returns Initialized services and state objects
   * @throws Error if initialization fails
   */
  initialize(): Promise<BuildTabInitializationResult>;

  /**
   * Configure event service callbacks for sequence operations
   * @param buildTabState Build tab state object
   * @param panelState Panel coordination state for callback handlers
   */
  configureEventCallbacks(buildTabState: any, panelState: PanelCoordinationState): void;

  /**
   * Load default start positions for a grid mode
   * @param gridMode Grid mode to load start positions for
   */
  loadStartPositions(gridMode: GridMode): Promise<void>;
}
