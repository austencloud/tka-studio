/**
 * Sequence State Orchestrator
 *
 * Composes all sub-states and operations into a unified sequence state:
 * - Core state (sequences, loading, errors)
 * - Selection state (beat selection, start position)
 * - Arrow state (arrow positioning)
 * - Animation state (removal animations)
 * - Persistence coordination
 * - Beat operations
 * - Transform operations
 * - Service integration
 *
 * RESPONSIBILITY: Composition and delegation, minimal business logic
 *
 * REPLACES: The 890-line god object sequence-state.svelte.ts
 */

import type {
    ActiveBuildTab,
    ArrowPosition,
    BeatData,
    PictographData,
    SequenceData,
    ValidationResult,
} from "$shared";
import { GridMode } from "$shared";
import type {
    ISequencePersistenceService,
    ISequenceService,
} from "../services/contracts";
import type { ISequenceStatisticsService } from "../services/contracts/ISequenceStatisticsService";
import type { ISequenceTransformationService } from "../services/contracts/ISequenceTransformationService";
import type { ISequenceValidationService } from "../services/contracts/ISequenceValidationService";
import { createSequenceAnimationState } from "./animation/SequenceAnimationState.svelte";
import { createSequenceArrowState } from "./arrow/SequenceArrowState.svelte";
import { createSequenceCoreState } from "./core/SequenceCoreState.svelte";
import { createSequenceBeatOperations } from "./operations/SequenceBeatOperations";
import { createSequenceTransformOperations } from "./operations/SequenceTransformOperations";
import { createSequencePersistenceCoordinator } from "./persistence/SequencePersistenceCoordinator.svelte";
import { createSequenceSelectionState } from "./selection/SequenceSelectionState.svelte";

/**
 * Clean service configuration - no more type gymnastics!
 */
export interface SequenceStateServices {
  sequenceService?: ISequenceService;
  sequencePersistenceService?: ISequencePersistenceService;
  sequenceStatisticsService?: ISequenceStatisticsService;
  sequenceTransformationService?: ISequenceTransformationService;
  sequenceValidationService?: ISequenceValidationService;
}

export function createSequenceState(services: SequenceStateServices) {
  const {
    sequenceService,
    sequencePersistenceService,
    sequenceStatisticsService,
    sequenceTransformationService,
    sequenceValidationService
  } = services;

  // Create sub-states
  const coreState = createSequenceCoreState();
  const selectionState = createSequenceSelectionState();
  const arrowState = createSequenceArrowState();
  const animationState = createSequenceAnimationState();

  // Create persistence coordinator
  const persistenceCoordinator = createSequencePersistenceCoordinator(
    sequencePersistenceService ?? null,
    undefined // Reversal detection service removed
  );

  // 🚀 PERFORMANCE: Debounced auto-save to prevent excessive persistence operations
  let saveTimeout: ReturnType<typeof setTimeout> | null = null;
  const SAVE_DEBOUNCE_MS = 500; // Wait 500ms after last change before saving

  // Create operation facades
  const beatOperations = createSequenceBeatOperations({
    coreState,
    selectionState,
    animationState,
    onSave: saveSequenceDataOnly,
  });

  const transformOperations = createSequenceTransformOperations({
    coreState,
    selectionState,
    sequenceStatisticsService: sequenceStatisticsService ?? null,
    sequenceTransformationService: sequenceTransformationService ?? null,
    sequenceValidationService: sequenceValidationService ?? null,
  });

  // ============================================================================
  // PERSISTENCE INTEGRATION
  // ============================================================================

  async function initializeWithPersistence(): Promise<void> {
    const savedState = await persistenceCoordinator.initialize();

    if (savedState) {
      coreState.setCurrentSequence(savedState.currentSequence);
      selectionState.setStartPosition(savedState.selectedStartPosition);
    }
  }

  async function saveCurrentState(activeBuildSection: ActiveBuildTab): Promise<void> {
    await persistenceCoordinator.saveState({
      currentSequence: coreState.currentSequence,
      selectedStartPosition: selectionState.selectedStartPosition,
      hasStartPosition: selectionState.hasStartPosition,
      activeBuildSection,
    });
  }

  async function saveSequenceDataOnly(): Promise<void> {
    await persistenceCoordinator.saveSequenceOnly(
      coreState.currentSequence,
      selectionState.selectedStartPosition,
      selectionState.hasStartPosition
    );
  }

  // ============================================================================
  // SEQUENCE SERVICE INTEGRATION
  // ============================================================================

  async function loadSequences(): Promise<void> {
    if (!sequenceService) return;

    coreState.setLoading(true);
    coreState.clearError();

    try {
      const sequences = await sequenceService.getAllSequences();
      coreState.setSequences(sequences);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Unknown error loading sequences";
      coreState.setError(errorMessage);
      console.error("Failed to load sequences:", error);
    } finally {
      coreState.setLoading(false);
    }
  }

  async function createSequence(request: {
    name: string;
    length: number;
  }): Promise<SequenceData | null> {
    if (!sequenceService) return null;

    coreState.setLoading(true);
    coreState.clearError();

    try {
      const sequence = await sequenceService.createSequence({
        ...request,
        word: request.name,
      });

      coreState.addSequence(sequence);
      coreState.setCurrentSequence(sequence);
      return sequence;
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Unknown error creating sequence";
      coreState.setError(errorMessage);
      console.error("Failed to create sequence:", error);
      return null;
    } finally {
      coreState.setLoading(false);
    }
  }

  async function updateSequenceBeats(
    sequenceId: string,
    beatIndex: number,
    beatData: BeatData
  ): Promise<void> {
    if (!sequenceService) return;

    try {
      await sequenceService.updateBeat(sequenceId, beatIndex, beatData);
      // Update local state
      if (coreState.currentSequence && beatIndex >= 0 && beatIndex < coreState.currentSequence.beats.length) {
        const newBeats = [...coreState.currentSequence.beats];
        newBeats[beatIndex] = beatData;
        coreState.setCurrentSequence({
          ...coreState.currentSequence,
          beats: newBeats,
        });
      }
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Unknown error updating beat";
      coreState.setError(errorMessage);
      console.error("Failed to update beat:", error);
    }
  }

  // ============================================================================
  // ENHANCED SEQUENCE OPERATIONS
  // ============================================================================

  function setCurrentSequence(sequence: SequenceData | null): void {
    coreState.setCurrentSequence(sequence);
    selectionState.clearSelection();

    // Update start position from sequence
    if (sequence && sequence.startingPositionBeat) {
      selectionState.setStartPosition(sequence.startingPositionBeat);
      console.log("⏪ SequenceState: Updated hasStartPosition to true (from sequence)");
    } else {
      selectionState.setStartPosition(null);
    }

    // 🚀 PERFORMANCE: Debounced auto-save to prevent blocking on every beat addition
    if (saveTimeout) {
      clearTimeout(saveTimeout);
    }
    saveTimeout = setTimeout(() => {
      saveSequenceDataOnly().catch((error) => {
        console.error("Failed to auto-save sequence state:", error);
      });
    }, SAVE_DEBOUNCE_MS);
  }

  function setSelectedStartPosition(startPosition: PictographData | null): void {
    selectionState.setStartPosition(startPosition);

    // 🚀 PERFORMANCE: Debounced auto-save
    if (saveTimeout) {
      clearTimeout(saveTimeout);
    }
    saveTimeout = setTimeout(() => {
      saveSequenceDataOnly().catch((error) => {
        console.error("Failed to auto-save start position state:", error);
      });
    }, SAVE_DEBOUNCE_MS);
  }

  async function clearSequenceCompletely(): Promise<void> {
    try {
      console.log("🎬 Starting clear sequence fade-out");
      animationState.startClearing();

      await new Promise((resolve) => setTimeout(resolve, 300));

      coreState.setCurrentSequence(null);
      selectionState.reset();
      coreState.clearError();

      await persistenceCoordinator.clearState();

      animationState.endClearing();
      console.log("✅ SequenceState: Sequence cleared completely");
    } catch (error) {
      console.error("❌ SequenceState: Failed to clear sequence:", error);
      coreState.setError(error instanceof Error ? error.message : "Failed to clear sequence");
      animationState.endClearing();
    }
  }

  function getCurrentSequenceData(): BeatData[] {
    const sequence = coreState.currentSequence;
    if (sequence) {
      const beats = sequence.beats || [];
      const startPosition = sequence.startingPositionBeat || sequence.startPosition;

      if (beats.length > 0) {
        return beats.map((beat: BeatData) => beat).filter(Boolean);
      } else if (startPosition && !startPosition.isBlank) {
        return [startPosition];
      }
    }

    // FIXED: Don't return selectedStartPosition here!
    // The selectedStartPosition is tracked separately in construct-tab-state.
    // Returning it here causes the option picker to think there's a sequence when there isn't.
    // This was causing the "no options available" bug.
    return [];
  }

  function getSelectedBeatData(): BeatData | null {
    // If start position is selected, return it as BeatData
    if (
      selectionState.isStartPositionSelected &&
      selectionState.selectedStartPosition
    ) {
      return {
        ...selectionState.selectedStartPosition,
        beatNumber: 0,
        duration: 1000,
        blueReversal: false,
        redReversal: false,
        isBlank: false,
      };
    }

    // Otherwise return selected beat
    if (selectionState.selectedBeatIndex === null || !coreState.currentSequence) {
      return null;
    }

    return (
      coreState.currentSequence.beats[selectionState.selectedBeatIndex] ?? null
    );
  }

  function selectBeat(beatNumber: number | null): void {
    if (beatNumber === null) {
      selectionState.clearSelection();
      return;
    }

    // Validate beatNumber is within valid range
    // beatNumber 0 = start position (always valid if we have a start position)
    // beatNumber 1 to N = beats in the sequence
    const currentSequence = coreState.currentSequence;

    if (beatNumber === 0) {
      // Start position - always allow selection
      selectionState.selectBeat(beatNumber);
    } else if (currentSequence && beatNumber >= 1 && beatNumber <= currentSequence.beats.length) {
      // Regular beat - validate it exists
      selectionState.selectBeat(beatNumber);
    } else {
      selectionState.clearSelection();
    }
  }

  function resetSequenceState(): void {
    coreState.reset();
    selectionState.reset();
    arrowState.reset();
    animationState.reset();
  }

  // ============================================================================
  // PUBLIC API - Unified interface matching original
  // ============================================================================

  return {
    // State getters - delegate to sub-states
    get currentSequence() {
      return coreState.currentSequence;
    },
    get sequences() {
      return coreState.sequences;
    },
    get isLoading() {
      return coreState.isLoading;
    },
    get error() {
      return coreState.error;
    },
    get selectedBeatIndex() {
      return selectionState.selectedBeatIndex;
    },
    get selectedBeatNumber() {
      return selectionState.selectedBeatNumber;
    },
    get selectedSequenceId() {
      return coreState.selectedSequenceId;
    },
    get showBeatNumbers() {
      return true;
    },
    get gridMode() {
      return coreState.gridMode;
    },
    get arrowPositions() {
      return arrowState.arrowPositions;
    },
    get arrowPositioningInProgress() {
      return arrowState.arrowPositioningInProgress;
    },
    get arrowPositioningError() {
      return arrowState.arrowPositioningError;
    },
    get selectedStartPosition() {
      return selectionState.selectedStartPosition;
    },
    get hasStartPosition() {
      return selectionState.hasStartPosition;
    },
    get isInitialized() {
      return persistenceCoordinator.isInitialized;
    },
    get selectedBeatData() {
      return getSelectedBeatData();
    },

    // Computed getters
    getCurrentSequence: () => coreState.currentSequence,
    getCurrentSequenceData,
    getSequences: () => coreState.sequences,
    getIsLoading: () => coreState.isLoading,
    getError: () => coreState.error,
    getSelectedBeatIndex: () => selectionState.selectedBeatIndex,
    getSelectedBeatNumber: () => selectionState.selectedBeatNumber,
    getSelectedSequenceId: () => coreState.selectedSequenceId,
    getRemovingBeatIndex: () => animationState.removingBeatIndex,
    getRemovingBeatIndices: () => animationState.removingBeatIndices,
    getIsClearing: () => animationState.isClearing,
    getShowBeatNumbers: () => true,
    getGridMode: () => coreState.gridMode,
    getArrowPositions: () => arrowState.arrowPositions,
    getArrowPositioningInProgress: () => arrowState.arrowPositioningInProgress,
    getArrowPositioningError: () => arrowState.arrowPositioningError,
    getCurrentBeats: () => (coreState.currentSequence ? [...coreState.currentSequence.beats] : []),
    getSelectedBeatData,
    getSelectedBeat: () => beatOperations.getBeat(selectionState.selectedBeatIndex ?? 0),
    getHasCurrentSequence: () => coreState.hasSequence,
    getSequenceCount: () => coreState.sequenceCount,
    getHasUnsavedChanges: () => coreState.currentSequence !== null && coreState.sequences.length > 0,
    getHasArrowPositions: () => arrowState.hasArrowPositions,
    getArrowPositioningComplete: () => arrowState.arrowPositioningComplete,
    hasSequence: () => coreState.hasSequence,
    beatCount: () => beatOperations.getBeatCount(),
    sequenceStatistics: () => transformOperations.getSequenceStatistics(),
    sequenceWord: () => transformOperations.generateSequenceWord(),
    sequenceDuration: () => transformOperations.calculateSequenceDuration(),

    // Core actions
    setCurrentSequence,
    addSequence: (sequence: SequenceData) => {
      coreState.addSequence(sequence);
      setCurrentSequence(sequence);
    },
    updateSequence: (sequence: SequenceData) => coreState.updateSequence(sequence),
    removeSequence: (sequenceId: string) => coreState.removeSequence(sequenceId),
    setSequences: (sequences: SequenceData[]) => coreState.setSequences(sequences),
    setLoading: (loading: boolean) => coreState.setLoading(loading),
    setError: (error: string | null) => coreState.setError(error),
    clearError: () => coreState.clearError(),
    updateCurrentBeat: (beatIndex: number, beatData: BeatData) => {
      if (coreState.currentSequence && beatIndex >= 0 && beatIndex < coreState.currentSequence.beats.length) {
        const newBeats = [...coreState.currentSequence.beats];
        newBeats[beatIndex] = beatData;
        coreState.setCurrentSequence({ ...coreState.currentSequence, beats: newBeats });
      }
    },

    // Selection actions
    selectBeat,
    clearSelection: () => selectionState.clearSelection(),
    selectStartPositionForEditing: () => selectionState.selectStartPosition(),
    isBeatSelected: (beatNumber: number) => selectionState.isBeatSelected(beatNumber),
    setSelectedStartPosition,

    // Grid mode
    setGridMode: (mode: GridMode) => coreState.setGridMode(mode),
    setShowBeatNumbers: (_show: boolean) => {}, // No-op, always shown

    // Arrow state
    setArrowPositions: (positions: Map<string, ArrowPosition>) => arrowState.setArrowPositions(positions),
    setArrowPositioningInProgress: (inProgress: boolean) => arrowState.setPositioningInProgress(inProgress),
    setArrowPositioningError: (error: string | null) => arrowState.setPositioningError(error),
    getArrowPosition: (color: string) => arrowState.getArrowPosition(color),
    clearArrowPositions: () => arrowState.clearArrowPositions(),

    // Animation state - expose for undo operations
    animationState,

    // Reset
    resetSequenceState,

    // Beat operations - delegate to facade
    addBeat: (beatData?: Partial<BeatData>) => beatOperations.addBeat(beatData),
    removeBeat: (beatIndex: number) => beatOperations.removeBeat(beatIndex),
    removeBeatWithAnimation: (beatIndex: number, onComplete?: () => void) =>
      beatOperations.removeBeatWithAnimation(beatIndex, onComplete),
    removeBeatAndSubsequent: (beatIndex: number) => beatOperations.removeBeatAndSubsequent(beatIndex),
    removeBeatAndSubsequentWithAnimation: (beatIndex: number, onComplete?: () => void) =>
      beatOperations.removeBeatAndSubsequentWithAnimation(beatIndex, onComplete),
    updateBeat: (beatIndex: number, beatData: Partial<BeatData>) =>
      beatOperations.updateBeat(beatIndex, beatData),
    insertBeat: (beatIndex: number, beatData?: Partial<BeatData>) =>
      beatOperations.insertBeat(beatIndex, beatData),
    clearSequence: () => beatOperations.clearSequence(),
    clearSequenceCompletely,
    getBeat: (index: number) => beatOperations.getBeat(index),
    hasContent: () => beatOperations.hasContent(),

    // Transform operations - delegate to facade
    setStartPosition: (startPosition: BeatData) => transformOperations.setStartPosition(startPosition),
    mirrorSequence: () => transformOperations.mirrorSequence(),
    swapColors: () => transformOperations.swapColors(),
    rotateSequence: (direction: "clockwise" | "counterclockwise") =>
      transformOperations.rotateSequence(direction),
    duplicateSequence: (newName?: string) => transformOperations.duplicateSequence(newName),
    validateCurrentSequence: (): ValidationResult | null => transformOperations.validateSequence(),

    // Persistence
    initializeWithPersistence,
    saveCurrentState,
    saveSequenceDataOnly,
    clearPersistedState: () => persistenceCoordinator.clearState(),

    // Service integration
    loadSequences,
    createSequence,
    updateSequenceBeats,

    // Multi-select operations
    get selectedBeatNumbers() {
      return selectionState.selectedBeatNumbers;
    },
    get isMultiSelectMode() {
      return selectionState.isMultiSelectMode;
    },
    get selectionCount() {
      return selectionState.selectionCount;
    },
    enterMultiSelectMode: (beatNumber: number) => selectionState.enterMultiSelectMode(beatNumber),
    exitMultiSelectMode: () => selectionState.exitMultiSelectMode(),
    toggleBeatInMultiSelect: (beatNumber: number) => selectionState.toggleBeatInMultiSelect(beatNumber),
  };
}

export type SequenceState = ReturnType<typeof createSequenceState>;
