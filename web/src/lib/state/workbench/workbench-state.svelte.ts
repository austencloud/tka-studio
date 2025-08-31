/**
 * Workbench State Factory
 *
 * Reactive state wrapper around the pure WorkbenchService and coordination services.
 * Follows the established TKA state factory pattern.
 */

import { GridMode } from "$domain";
import type {
  IWorkbenchCoordinationService,
  IWorkbenchService,
  WorkbenchConfig,
  WorkbenchMode,
} from "$lib/services/contracts/workbench-interfaces";

/**
 * Creates component-scoped workbench state
 *
 * @param workbenchService - Injected via DI container
 * @param coordinationService - Injected via DI container
 * @param sequenceState - Sequence state from parent component
 * @param beatFrameState - Beat frame state from parent component
 * @returns Reactive state object with getters and actions
 */
export function createWorkbenchState(
  workbenchService: IWorkbenchService,
  coordinationService: IWorkbenchCoordinationService,
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  sequenceState: any, // Will be properly typed when sequence state is available
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  beatFrameState: any // Will be properly typed when beat frame state is available
) {
  // ============================================================================
  // REACTIVE STATE (Component-scoped)
  // ============================================================================

  let config = $state<WorkbenchConfig>({
    mode: "construct",
    isInitialized: false,
  });

  let error = $state<string | null>(null);
  let isLoading = $state<boolean>(false);

  // ============================================================================
  // DERIVED STATE (Reactive computations)
  // ============================================================================

  const isInitialized = $derived(() => workbenchService.isInitialized(config));
  const mode = $derived(() => config.mode);
  const canEdit = $derived(() => workbenchService.canEditInMode(config.mode));

  // Delegate to other state objects
  const currentSequence = $derived(
    () => sequenceState?.currentSequence ?? null
  );
  const selectedBeatIndex = $derived(
    () => sequenceState?.selectedBeatIndex ?? -1
  );
  const hoveredBeatIndex = $derived(
    () => beatFrameState?.hoveredBeatIndex ?? -1
  );

  // ============================================================================
  // GETTERS (Reactive access to state)
  // ============================================================================

  return {
    // Core state getters
    get config() {
      return config;
    },

    get error() {
      return error;
    },

    get isLoading() {
      return isLoading;
    },

    // Derived state getters
    get isInitialized() {
      return isInitialized;
    },

    get mode() {
      return mode;
    },

    get canEdit() {
      return canEdit;
    },

    get currentSequence() {
      return currentSequence;
    },

    get selectedBeatIndex() {
      return selectedBeatIndex;
    },

    get hoveredBeatIndex() {
      return hoveredBeatIndex;
    },

    // ============================================================================
    // ACTIONS (State mutations and service calls)
    // ============================================================================

    // Initialization actions
    initialize() {
      try {
        config = workbenchService.initialize();
        error = null;
      } catch (err) {
        error =
          err instanceof Error ? err.message : "Failed to initialize workbench";
      }
    },

    // Mode management actions
    setMode(newMode: WorkbenchMode) {
      try {
        config = workbenchService.setMode(config, newMode);
        error = null;
      } catch (err) {
        error = err instanceof Error ? err.message : "Failed to set mode";
      }
    },

    // Beat interaction actions
    handleBeatClick(index: number) {
      try {
        const result = coordinationService.handleBeatClick(index, config.mode);

        if (result.shouldSelect && sequenceState) {
          sequenceState.selectBeat(index);
        }

        error = null;
      } catch (err) {
        error =
          err instanceof Error ? err.message : "Failed to handle beat click";
      }
    },

    handleBeatHover(index: number) {
      try {
        coordinationService.handleBeatHover(index);

        // Delegate to beat frame state
        if (beatFrameState) {
          beatFrameState.setHoveredBeatIndex(index);
        }

        error = null;
      } catch (err) {
        error =
          err instanceof Error ? err.message : "Failed to handle beat hover";
      }
    },

    handleBeatLeave() {
      try {
        coordinationService.handleBeatLeave();

        // Delegate to beat frame state
        if (beatFrameState) {
          beatFrameState.clearHover();
        }

        error = null;
      } catch (err) {
        error =
          err instanceof Error ? err.message : "Failed to handle beat leave";
      }
    },

    // Beat editing actions
    editBeat(index: number) {
      try {
        const result = coordinationService.editBeat(
          index,
          currentSequence(),
          config.mode
        );

        if (result.success && result.updatedBeat && sequenceState) {
          sequenceState.updateBeat(index, result.updatedBeat);
        } else if (!result.success) {
          error = result.error || "Failed to edit beat";
        }
      } catch (err) {
        error = err instanceof Error ? err.message : "Failed to edit beat";
      }
    },

    clearBeat(index: number) {
      try {
        const result = coordinationService.clearBeat(index, currentSequence());

        if (result.success && result.updatedBeat && sequenceState) {
          sequenceState.updateBeat(index, result.updatedBeat);
        } else if (!result.success) {
          error = result.error || "Failed to clear beat";
        }
      } catch (err) {
        error = err instanceof Error ? err.message : "Failed to clear beat";
      }
    },

    // Sequence actions
    createNewSequence(name?: string, length?: number) {
      try {
        isLoading = true;
        const result = coordinationService.createNewSequence(name, length);

        if (result.success && sequenceState) {
          // Delegate to sequence state service
          sequenceState.createNewSequence(name || "New Sequence", length || 16);
        } else if (!result.success) {
          error = result.error || "Failed to create sequence";
        }
      } catch (err) {
        error =
          err instanceof Error ? err.message : "Failed to create sequence";
      } finally {
        isLoading = false;
      }
    },

    // Configuration actions
    setGridMode(gridMode: GridMode) {
      try {
        const result = coordinationService.setGridMode(gridMode);

        if (result.success && beatFrameState) {
          // Delegate to beat frame state
          beatFrameState.setConfig({ gridMode });
        } else if (!result.success) {
          error = result.error || "Failed to set grid mode";
        }
      } catch (err) {
        error = err instanceof Error ? err.message : "Failed to set grid mode";
      }
    },

    setBeatSize(size: number) {
      try {
        const result = coordinationService.setBeatSize(size);

        if (result.success && beatFrameState) {
          // Delegate to beat frame state
          beatFrameState.setConfig({ beatSize: size });
        } else if (!result.success) {
          error = result.error || "Failed to set beat size";
        }
      } catch (err) {
        error = err instanceof Error ? err.message : "Failed to set beat size";
      }
    },

    // ============================================================================
    // CONVENIENCE METHODS
    // ============================================================================

    // Check if beat can be edited
    canEditBeat(index: number): boolean {
      return workbenchService.canEditBeat(
        currentSequence(),
        index,
        config.mode
      );
    },

    // Check if beat can be cleared
    canClearBeat(index: number): boolean {
      return workbenchService.canClearBeat(currentSequence(), index);
    },

    // Get current workbench status
    getStatus(): string {
      if (!isInitialized) return "Not initialized";
      if (isLoading) return "Loading...";
      if (error) return `Error: ${error}`;
      return `Ready (${config.mode} mode)`;
    },
  };
}

/**
 * Type definition for the workbench state
 */
export type WorkbenchState = ReturnType<typeof createWorkbenchState>;
