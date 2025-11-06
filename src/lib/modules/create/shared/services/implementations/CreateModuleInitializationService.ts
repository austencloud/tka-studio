/**
 * Create Module Initialization Service Implementation
 *
 * Manages complete initialization sequence for CreateModule's construction interface.
 * Resolves services, creates state, configures callbacks for sequence building workflow.
 *
 * Domain: Create module - Sequence Construction Interface
 * Extracted from CreateModule.svelte onMount monolith.
 */

import { GridMode, TYPES, navigationState, resolve } from "$shared";
import { injectable } from "inversify";
import type { IStartPositionService } from "../../../construct/start-position-picker/services/contracts";
import { createCreateModuleState, createConstructTabState } from "../../state";
import type { PanelCoordinationState } from "../../state/panel-coordination-state.svelte";
import type {
  IBeatOperationsService,
  ICreateModuleService,
  INavigationSyncService,
  IResponsiveLayoutService,
  ISequencePersistenceService,
  ISequenceService
} from "../contracts";
import type { CreateModuleInitializationResult, ICreateModuleInitializationService } from "../contracts/ICreateModuleInitializationService";
import { getCreateModuleEventService } from "./CreateModuleEventService";

@injectable()
export class CreateModuleInitializationService implements ICreateModuleInitializationService {
  private sequenceService: ISequenceService | null = null;
  private sequencePersistenceService: ISequencePersistenceService | null = null;
  private startPositionService: IStartPositionService | null = null;
  private CreateModuleService: ICreateModuleService | null = null;
  private layoutService: IResponsiveLayoutService | null = null;
  private navigationSyncService: INavigationSyncService | null = null;
  private beatOperationsService: IBeatOperationsService | null = null;

  async initialize(): Promise<CreateModuleInitializationResult> {
    // Resolve all required services
    this.sequenceService = resolve(TYPES.ISequenceService) as ISequenceService;
    this.sequencePersistenceService = resolve(TYPES.ISequencePersistenceService) as ISequencePersistenceService;
    this.startPositionService = resolve(TYPES.IStartPositionService) as IStartPositionService;
    this.CreateModuleService = resolve(TYPES.ICreateModuleService) as ICreateModuleService;
    this.layoutService = resolve(TYPES.IResponsiveLayoutService) as IResponsiveLayoutService;
    this.navigationSyncService = resolve(TYPES.INavigationSyncService) as INavigationSyncService;
    this.beatOperationsService = resolve(TYPES.IBeatOperationsService) as IBeatOperationsService;

    // Wait a tick to ensure component context is fully established
    await new Promise(resolve => setTimeout(resolve, 0));

    // Create state objects
    const CreateModuleState = createCreateModuleState(
      this.sequenceService,
      this.sequencePersistenceService
    );

    const constructTabState = createConstructTabState(
      this.CreateModuleService,
      CreateModuleState.sequenceState,
      this.sequencePersistenceService,
      CreateModuleState,
      navigationState
    );

    // Initialize services
    await this.CreateModuleService.initialize();

    // Initialize state with persistence
    await CreateModuleState.initializeWithPersistence();
    await constructTabState.initializeConstructTab();

    // Note: Event callbacks configured separately via configureEventCallbacks()
    // after component has created panelState

    // Load start positions
    await this.loadStartPositions(GridMode.DIAMOND);

    return {
      sequenceService: this.sequenceService,
      sequencePersistenceService: this.sequencePersistenceService,
      startPositionService: this.startPositionService,
      CreateModuleService: this.CreateModuleService,
      CreateModuleState,
      constructTabState,
      layoutService: this.layoutService,
      navigationSyncService: this.navigationSyncService,
      beatOperationsService: this.beatOperationsService,
    };
  }

  configureEventCallbacks(CreateModuleState: any, panelState: PanelCoordinationState): void {
    const CreateModuleEventService = getCreateModuleEventService();

    // Set up sequence state callbacks for CreateModuleEventService
    CreateModuleEventService.setSequenceStateCallbacks(
      () => CreateModuleState.sequenceState.getCurrentSequence(),
      (sequence) => CreateModuleState.sequenceState.setCurrentSequence(sequence)
    );

    // Set up option history callback
    CreateModuleEventService.setAddOptionToHistoryCallback(
      (beatIndex, beatData) => CreateModuleState.addOptionToHistory(beatIndex, beatData)
    );

    // Set up undo snapshot callback
    CreateModuleEventService.setPushUndoSnapshotCallback(
      (type, metadata) => CreateModuleState.pushUndoSnapshot(type, metadata)
    );

    // Configure panel state callbacks on sequenceState
    CreateModuleState.sequenceState.onEditPanelOpen = (beatIndex: number, beatData: any, beatsData: any[]) => {
      if (beatsData && beatsData.length > 0) {
        panelState.openBatchEditPanel(beatsData);
      } else {
        panelState.openEditPanel(beatIndex, beatData);
      }
    };

    CreateModuleState.sequenceState.onEditPanelClose = () => {
      panelState.closeEditPanel();
    };

    CreateModuleState.sequenceState.onAnimationStart = () => {
      panelState.setAnimating(true);
    };

    CreateModuleState.sequenceState.onAnimationEnd = () => {
      panelState.setAnimating(false);
    };
  }

  configureClearSequenceCallback(CreateModuleState: any, constructTabState: any): void {
    // Set up clear sequence callback (to ensure UI state is properly updated)
    CreateModuleState.setClearSequenceCompletelyCallback(async () => {
      if (constructTabState?.clearSequenceCompletely) {
        await constructTabState.clearSequenceCompletely();
      }
    });
  }

  async loadStartPositions(gridMode: GridMode): Promise<void> {
    if (!this.startPositionService) {
      throw new Error("Start position service not initialized");
    }

    await this.startPositionService.getDefaultStartPositions(gridMode);
  }
}
