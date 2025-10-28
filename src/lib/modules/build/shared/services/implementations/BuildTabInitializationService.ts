/**
 * Build Tab Initialization Service Implementation
 *
 * Manages complete initialization sequence for BuildTab's construction interface.
 * Resolves services, creates state, configures callbacks for sequence building workflow.
 *
 * Domain: Build Module - Sequence Construction Interface
 * Extracted from BuildTab.svelte onMount monolith.
 */

import { GridMode, TYPES, navigationState, resolve } from "$shared";
import { injectable } from "inversify";
import type { IStartPositionService } from "../../../construct/start-position-picker/services/contracts";
import { createBuildTabState, createConstructTabState } from "../../state";
import type { PanelCoordinationState } from "../../state/panel-coordination-state.svelte";
import type { 
  IBuildTabService, 
  ISequencePersistenceService, 
  ISequenceService,
  IBuildTabResponsiveLayoutService,
  INavigationSyncService,
  IBeatOperationsService
} from "../contracts";
import type { BuildTabInitializationResult, IBuildTabInitializationService } from "../contracts/IBuildTabInitializationService";
import { getBuildTabEventService } from "./BuildTabEventService";

@injectable()
export class BuildTabInitializationService implements IBuildTabInitializationService {
  private sequenceService: ISequenceService | null = null;
  private sequencePersistenceService: ISequencePersistenceService | null = null;
  private startPositionService: IStartPositionService | null = null;
  private buildTabService: IBuildTabService | null = null;
  private layoutService: IBuildTabResponsiveLayoutService | null = null;
  private navigationSyncService: INavigationSyncService | null = null;
  private beatOperationsService: IBeatOperationsService | null = null;

  async initialize(): Promise<BuildTabInitializationResult> {
    // Resolve all required services
    this.sequenceService = resolve(TYPES.ISequenceService) as ISequenceService;
    this.sequencePersistenceService = resolve(TYPES.ISequencePersistenceService) as ISequencePersistenceService;
    this.startPositionService = resolve(TYPES.IStartPositionService) as IStartPositionService;
    this.buildTabService = resolve(TYPES.IBuildTabService) as IBuildTabService;
    this.layoutService = resolve(TYPES.IBuildTabResponsiveLayoutService) as IBuildTabResponsiveLayoutService;
    this.navigationSyncService = resolve(TYPES.INavigationSyncService) as INavigationSyncService;
    this.beatOperationsService = resolve(TYPES.IBeatOperationsService) as IBeatOperationsService;

    // Wait a tick to ensure component context is fully established
    await new Promise(resolve => setTimeout(resolve, 0));

    // Create state objects
    const buildTabState = createBuildTabState(
      this.sequenceService,
      this.sequencePersistenceService
    );

    const constructTabState = createConstructTabState(
      this.buildTabService,
      buildTabState.sequenceState,
      this.sequencePersistenceService,
      buildTabState,
      navigationState
    );

    // Initialize services
    await this.buildTabService.initialize();

    // Initialize state with persistence
    await buildTabState.initializeWithPersistence();
    await constructTabState.initializeConstructTab();

    // Note: Event callbacks configured separately via configureEventCallbacks()
    // after component has created panelState

    // Load start positions
    await this.loadStartPositions(GridMode.DIAMOND);

    return {
      sequenceService: this.sequenceService,
      sequencePersistenceService: this.sequencePersistenceService,
      startPositionService: this.startPositionService,
      buildTabService: this.buildTabService,
      buildTabState,
      constructTabState,
      layoutService: this.layoutService,
      navigationSyncService: this.navigationSyncService,
      beatOperationsService: this.beatOperationsService,
    };
  }

  configureEventCallbacks(buildTabState: any, panelState: PanelCoordinationState): void {
    const buildTabEventService = getBuildTabEventService();

    // Set up sequence state callbacks for BuildTabEventService
    buildTabEventService.setSequenceStateCallbacks(
      () => buildTabState.sequenceState.getCurrentSequence(),
      (sequence) => buildTabState.sequenceState.setCurrentSequence(sequence)
    );

    // Set up option history callback
    buildTabEventService.setAddOptionToHistoryCallback(
      (beatIndex, beatData) => buildTabState.addOptionToHistory(beatIndex, beatData)
    );

    // Set up undo snapshot callback
    buildTabEventService.setPushUndoSnapshotCallback(
      (type, metadata) => buildTabState.pushUndoSnapshot(type, metadata)
    );

    // Configure panel state callbacks on sequenceState
    buildTabState.sequenceState.onEditPanelOpen = (beatIndex: number, beatData: any, beatsData: any[]) => {
      if (beatsData && beatsData.length > 0) {
        panelState.openBatchEditPanel(beatsData);
      } else {
        panelState.openEditPanel(beatIndex, beatData);
      }
    };

    buildTabState.sequenceState.onEditPanelClose = () => {
      panelState.closeEditPanel();
    };

    buildTabState.sequenceState.onAnimationStart = () => {
      panelState.setAnimating(true);
    };

    buildTabState.sequenceState.onAnimationEnd = () => {
      panelState.setAnimating(false);
    };
  }

  async loadStartPositions(gridMode: GridMode): Promise<void> {
    if (!this.startPositionService) {
      throw new Error("Start position service not initialized");
    }

    await this.startPositionService.getDefaultStartPositions(gridMode);
  }
}
