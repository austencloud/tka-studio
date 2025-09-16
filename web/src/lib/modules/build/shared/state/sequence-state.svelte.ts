// Unified file moved from src/lib/state/sequence-state.svelte.ts
// See that file history for rationale.

import type {
    ActiveBuildTab,
    ArrowPosition,
    BeatData,
    PictographData,
    SequenceData,
    ValidationResult
} from "$shared";
import { GridMode } from "$shared";
import type { ISequencePersistenceService, ISequenceStateService } from "../services/contracts";
import type {
    ISequenceService,
} from "../services/contracts/sequence-contracts";

export function createSequenceState(
  services:
    | {
        sequenceService?: ISequenceService;
        sequenceStateService?: ISequenceStateService;
        sequencePersistenceService?: ISequencePersistenceService;
      }
    | ISequenceService
    | ISequenceStateService
) {
  // Back-compat: allow passing a single service instance or an options object
  let sequenceService: ISequenceService | undefined;
  let sequenceStateService: ISequenceStateService | undefined;
  let sequencePersistenceService: ISequencePersistenceService | undefined;
  const isObject = (x: unknown): x is Record<string, unknown> =>
    !!x && typeof x === "object";
  const isSequenceService = (x: unknown): x is ISequenceService =>
    isObject(x) && "getAllSequences" in x && "updateBeat" in x;
  const isSequenceStateService = (x: unknown): x is ISequenceStateService =>
    isObject(x) && "addBeat" in x && "removeBeat" in x;

  if (isObject(services) && ("sequenceService" in services || "sequenceStateService" in services || "sequencePersistenceService" in services)) {
    sequenceService = (services as { sequenceService?: ISequenceService }).sequenceService;
    sequenceStateService = (services as { sequenceStateService?: ISequenceStateService }).sequenceStateService;
    sequencePersistenceService = (services as { sequencePersistenceService?: ISequencePersistenceService }).sequencePersistenceService;
  } else if (isSequenceService(services)) {
    sequenceService = services;
  } else if (isSequenceStateService(services)) {
    sequenceStateService = services;
  }

  const state = $state({
    currentSequence: null as SequenceData | null,
    sequences: [] as SequenceData[],
    isLoading: false,
    error: null as string | null,
    selectedBeatIndex: null as number | null,
    selectedSequenceId: null as string | null,
    showBeatNumbers: true,
    gridMode: GridMode.DIAMOND as GridMode,
    arrowPositions: new Map<string, ArrowPosition>(),
    arrowPositioningInProgress: false,
    arrowPositioningError: null as string | null,
    // Persistence state
    selectedStartPosition: null as PictographData | null,
    hasStartPosition: false,
    isInitialized: false,
  });

  function getSequences() {
    return state.sequences;
  }
  function getIsLoading() {
    return state.isLoading;
  }
  function getError() {
    return state.error;
  }
  function getSelectedBeatIndex() {
    return state.selectedBeatIndex;
  }
  function getSelectedSequenceId() {
    return state.selectedSequenceId;
  }
  function getShowBeatNumbers() {
    return state.showBeatNumbers;
  }
  function getGridMode() {
    return state.gridMode;
  }
  function getArrowPositions() {
    return state.arrowPositions;
  }
  function getArrowPositioningInProgress() {
    return state.arrowPositioningInProgress;
  }
  function getArrowPositioningError() {
    return state.arrowPositioningError;
  }

  function getCurrentBeats(): BeatData[] {
    return state.currentSequence ? [...state.currentSequence.beats] : [];
  }
  function getSelectedBeatData(): BeatData | null {
    if (state.selectedBeatIndex === null || !state.currentSequence) {
      return null;
    }
    return state.currentSequence.beats[state.selectedBeatIndex] ?? null;
  }

  // ============================================================================
  // PERSISTENCE FUNCTIONS
  // ============================================================================

  async function initializeWithPersistence(): Promise<void> {
    if (!sequencePersistenceService || state.isInitialized) return;

    try {
      await sequencePersistenceService.initialize();
      const savedState = await sequencePersistenceService.loadCurrentState();

      if (savedState) {
        // Apply reversal detection to loaded sequence if it exists
        let currentSequence = savedState.currentSequence;
        if (currentSequence && sequenceStateService) {
          console.log("🔄 SequenceState: Applying reversal detection to loaded sequence");
          currentSequence = sequenceStateService.applyReversalDetection(currentSequence);
        }

        state.currentSequence = currentSequence;
        state.selectedStartPosition = savedState.selectedStartPosition;
        state.hasStartPosition = savedState.hasStartPosition;

        if (currentSequence) {
          state.selectedSequenceId = currentSequence.id;
        }
      }

      state.isInitialized = true;
      console.log("✅ SequenceState: Initialized with persistence");
    } catch (error) {
      console.error("❌ SequenceState: Failed to initialize with persistence:", error);
      state.isInitialized = true; // Continue without persistence
    }
  }

  async function saveCurrentState(activeBuildSubTab: ActiveBuildTab): Promise<void> {
    if (!sequencePersistenceService) return;

    try {
      await sequencePersistenceService.saveCurrentState({
        currentSequence: state.currentSequence,
        selectedStartPosition: state.selectedStartPosition,
        hasStartPosition: state.hasStartPosition,
        activeBuildSubTab,
      });
    } catch (error) {
      console.error("❌ SequenceState: Failed to save current state:", error);
    }
  }

  async function saveSequenceDataOnly(): Promise<void> {
    if (!sequencePersistenceService) return;

    try {
      // Load current state to preserve the active tab
      const currentState = await sequencePersistenceService.loadCurrentState();
      const preservedTab = currentState?.activeBuildSubTab || "construct";

      await sequencePersistenceService.saveCurrentState({
        currentSequence: state.currentSequence,
        selectedStartPosition: state.selectedStartPosition,
        hasStartPosition: state.hasStartPosition,
        activeBuildSubTab: preservedTab,
      });
    } catch (error) {
      console.error("❌ SequenceState: Failed to save sequence data:", error);
    }
  }

  async function clearPersistedState(): Promise<void> {
    if (!sequencePersistenceService) return;

    try {
      await sequencePersistenceService.clearCurrentState();
      console.log("✅ SequenceState: Cleared persisted state");
    } catch (error) {
      console.error("❌ SequenceState: Failed to clear persisted state:", error);
    }
  }

  function setCurrentSequence(sequence: SequenceData | null): void {
    state.currentSequence = sequence;
    state.selectedSequenceId = sequence?.id ?? null;
    state.selectedBeatIndex = null;

    // Auto-save state when sequence changes
    saveSequenceDataOnly().catch(error => {
      console.error("Failed to auto-save sequence state:", error);
    });
  }

  function setSelectedStartPosition(startPosition: PictographData | null): void {
    state.selectedStartPosition = startPosition;
    state.hasStartPosition = startPosition !== null;

    // Auto-save state when start position changes
    saveSequenceDataOnly().catch(error => {
      console.error("Failed to auto-save start position state:", error);
    });
  }
  function addSequence(sequence: SequenceData): void {
    state.sequences.push(sequence);
    setCurrentSequence(sequence);
  }
  function updateSequence(updatedSequence: SequenceData): void {
    const index = state.sequences.findIndex((s) => s.id === updatedSequence.id);
    if (index >= 0) state.sequences[index] = updatedSequence;
    if (state.currentSequence?.id === updatedSequence.id) {
      state.currentSequence = updatedSequence;
    }
  }
  function removeSequence(sequenceId: string): void {
    state.sequences = state.sequences.filter((s) => s.id !== sequenceId);
    if (state.currentSequence?.id === sequenceId) setCurrentSequence(null);
  }
  function setSequences(newSequences: SequenceData[]): void {
    state.sequences = newSequences;
  }
  function setLoading(loading: boolean): void {
    state.isLoading = loading;
  }
  function setError(error: string | null): void {
    state.error = error;
  }
  function clearError(): void {
    state.error = null;
  }
  function updateCurrentBeat(beatIndex: number, beatData: BeatData): void {
    if (
      state.currentSequence &&
      beatIndex >= 0 &&
      beatIndex < state.currentSequence.beats.length
    ) {
      const newBeats = [...state.currentSequence.beats];
      newBeats[beatIndex] = beatData;
      state.currentSequence = {
        ...state.currentSequence,
        beats: newBeats,
      } as SequenceData;
    }
  }
  function setGridMode(mode: GridMode): void {
    state.gridMode = mode;
  }
  function setShowBeatNumbers(show: boolean): void {
    state.showBeatNumbers = show;
  }
  function setArrowPositions(positions: Map<string, ArrowPosition>): void {
    state.arrowPositions = positions;
  }
  function setArrowPositioningInProgress(inProgress: boolean): void {
    state.arrowPositioningInProgress = inProgress;
  }
  function setArrowPositioningError(error: string | null): void {
    state.arrowPositioningError = error;
  }
  function getArrowPosition(color: string): ArrowPosition | null {
    return state.arrowPositions.get(color) || null;
  }
  function clearArrowPositions(): void {
    state.arrowPositions.clear();
  }
  function resetSequenceState(): void {
    state.currentSequence = null;
    state.sequences = [];
    state.isLoading = false;
    state.error = null;
    state.selectedBeatIndex = null;
    state.selectedSequenceId = null;
    state.gridMode = GridMode.DIAMOND;
    state.arrowPositions.clear();
    state.arrowPositioningInProgress = false;
    state.arrowPositioningError = null;
  }

  async function loadSequences(): Promise<void> {
    setLoading(true);
    setError(null);
    try {
      if (!sequenceService) return;
      const sequences = await sequenceService.getAllSequences();
      setSequences(sequences);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Unknown error loading sequences";
      setError(errorMessage);
      console.error("Failed to load sequences:", error);
    } finally {
      setLoading(false);
    }
  }

  async function createSequence(request: { name: string; length: number }): Promise<SequenceData | null> {
    setLoading(true);
    setError(null);
    try {
      if (!sequenceService) {
        return null;
      }

      const sequence = await sequenceService.createSequence({
        ...request,
        word: request.name // Use name as word if not provided
      });

      addSequence(sequence);
      return sequence;
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Unknown error creating sequence";
      setError(errorMessage);
      console.error("Failed to create sequence:", error);
      return null;
    } finally {
      setLoading(false);
    }
  }

  async function updateSequenceBeats(
    sequenceId: string,
    beatIndex: number,
    beatData: BeatData
  ): Promise<void> {
    try {
      if (!sequenceService) return;
      await sequenceService.updateBeat(sequenceId, beatIndex, beatData);
      updateCurrentBeat(beatIndex, beatData);
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : "Unknown error updating beat";
      setError(errorMessage);
      console.error("Failed to update beat:", error);
    }
  }

  function getSelectedBeat(): BeatData | null {
    if (state.selectedBeatIndex === null || !state.currentSequence) return null;
    if (sequenceStateService) {
      return sequenceStateService.getSelectedBeat(
        state.currentSequence,
        state.selectedBeatIndex
      );
    }
    return (state.currentSequence.beats[state.selectedBeatIndex] ?? null) as BeatData | null;
  }
  function hasCurrentSequence(): boolean {
    return state.currentSequence !== null;
  }
  function getBeatCount(): number {
    return state.currentSequence?.beats.length ?? 0;
  }
  function getSequenceStatistics() {
    if (!state.currentSequence || !sequenceStateService) return null;
    return sequenceStateService.getSequenceStatistics(state.currentSequence);
  }
  function getSequenceWord(): string {
    if (!state.currentSequence || !sequenceStateService) return "";
    return sequenceStateService.generateSequenceWord(state.currentSequence);
  }
  function getSequenceDuration(): number {
    if (!state.currentSequence || !sequenceStateService) return 0;
    return sequenceStateService.calculateSequenceDuration(state.currentSequence);
  }
  function getSequenceCount(): number {
    return state.sequences.length;
  }
  function getHasUnsavedChanges(): boolean {
    // Track changes by comparing current sequence with a saved snapshot
    // For now, we'll consider any loaded sequence as potentially having changes
    // TODO: Implement proper change tracking with sequence snapshots
    return state.currentSequence !== null && state.sequences.length > 0;
  }
  function getHasArrowPositions(): boolean {
    return state.arrowPositions.size > 0;
  }
  function getArrowPositioningComplete(): boolean {
    return !state.arrowPositioningInProgress && state.arrowPositions.size > 0;
  }
  function selectBeat(index: number | null): void {
    if (index === null) {
      state.selectedBeatIndex = null;
      return;
    }
    if (!sequenceStateService) {
      state.selectedBeatIndex = index;
      return;
    }
    if (sequenceStateService.isValidBeatIndex(state.currentSequence, index)) {
      state.selectedBeatIndex = index;
    } else {
      state.selectedBeatIndex = null;
    }
  }
  function clearSelection(): void {
    state.selectedBeatIndex = null;
  }
  function addBeat(beatData?: Partial<BeatData>): void {
    if (!state.currentSequence || !sequenceStateService) return;
    try {
      state.currentSequence = sequenceStateService.addBeat(state.currentSequence, beatData);
      state.error = null;
    } catch (err) {
      state.error = err instanceof Error ? err.message : "Failed to add beat";
    }
  }
  function removeBeat(beatIndex: number): void {
    if (!state.currentSequence || !sequenceStateService) return;
    try {
      state.currentSequence = sequenceStateService.removeBeat(state.currentSequence, beatIndex);
      if (state.selectedBeatIndex === beatIndex) {
        state.selectedBeatIndex = null;
      } else if (state.selectedBeatIndex !== null && state.selectedBeatIndex > beatIndex) {
        state.selectedBeatIndex = state.selectedBeatIndex - 1;
      }
      state.error = null;
    } catch (err) {
      state.error = err instanceof Error ? err.message : "Failed to remove beat";
    }
  }
  function updateBeat(beatIndex: number, beatData: Partial<BeatData>): void {
    if (!state.currentSequence || !sequenceStateService) return;
    try {
      const completeBeatData = beatData ? { ...beatData } : { id: '', beatNumber: beatIndex + 1, isBlank: true, duration: 1 };
      state.currentSequence = sequenceStateService.updateBeat(
        state.currentSequence,
        beatIndex,
        completeBeatData as BeatData
      );
      state.error = null;
    } catch (err) {
      state.error = err instanceof Error ? err.message : "Failed to update beat";
    }
  }
  function insertBeat(beatIndex: number, beatData?: Partial<BeatData>): void {
    if (!state.currentSequence || !sequenceStateService) return;
    try {
      const completeBeatData = beatData || { id: '', beatNumber: beatIndex + 1, isBlank: true, duration: 1 };
      state.currentSequence = sequenceStateService.insertBeat(
        state.currentSequence,
        beatIndex,
        completeBeatData as BeatData
      );
      if (state.selectedBeatIndex !== null && state.selectedBeatIndex >= beatIndex) {
        state.selectedBeatIndex = state.selectedBeatIndex + 1;
      }
      state.error = null;
    } catch (err) {
      state.error = err instanceof Error ? err.message : "Failed to insert beat";
    }
  }
  function clearSequenceBeats(): void {
    if (!state.currentSequence || !sequenceStateService) return;
    try {
      state.currentSequence = sequenceStateService.clearSequence(state.currentSequence);
      state.selectedBeatIndex = null;
      state.error = null;
    } catch (err) {
      state.error = err instanceof Error ? err.message : "Failed to clear sequence";
    }
  }

  async function clearSequence(): Promise<void> {
    try {
      // Clear the sequence state
      state.currentSequence = null;
      state.selectedSequenceId = null;
      state.selectedBeatIndex = null;
      state.selectedStartPosition = null;
      state.hasStartPosition = false;
      state.error = null;

      // Clear persisted state
      await clearPersistedState();

      console.log("✅ SequenceState: Sequence cleared completely");
    } catch (error) {
      console.error("❌ SequenceState: Failed to clear sequence:", error);
      state.error = error instanceof Error ? error.message : "Failed to clear sequence";
    }
  }
  function duplicateSequence(newName?: string): SequenceData | null {
    if (!state.currentSequence || !sequenceStateService) return null;
    try {
      const duplicated = sequenceStateService.duplicateSequence(state.currentSequence, newName);
      state.error = null;
      return duplicated;
    } catch (err) {
      state.error = err instanceof Error ? err.message : "Failed to duplicate sequence";
      return null;
    }
  }
  function setStartPosition(startPosition: BeatData): void {
    if (!state.currentSequence || !sequenceStateService) {
      return;
    }
    
    try {
      state.currentSequence = sequenceStateService.setStartPosition(
        state.currentSequence,
        startPosition
      );
      state.error = null;
    } catch (err) {
      console.error("Error in setStartPosition:", err);
      state.error = err instanceof Error ? err.message : "Failed to set start position";
    }
  }
  function mirrorSequence(): void {
    if (!state.currentSequence || !sequenceStateService) return;
    try {
      state.currentSequence = sequenceStateService.mirrorSequence(state.currentSequence);
      state.error = null;
    } catch (err) {
      state.error = err instanceof Error ? err.message : "Failed to mirror sequence";
    }
  }
  function swapColors(): void {
    if (!state.currentSequence || !sequenceStateService) return;
    try {
      state.currentSequence = sequenceStateService.swapColors(state.currentSequence);
      state.error = null;
    } catch (err) {
      state.error = err instanceof Error ? err.message : "Failed to swap colors";
    }
  }
  function rotateSequence(direction: "clockwise" | "counterclockwise"): void {
    if (!state.currentSequence || !sequenceStateService) return;
    try {
      const rotationAmount = direction === "clockwise" ? 1 : -1;
      state.currentSequence = sequenceStateService.rotateSequence(
        state.currentSequence,
        rotationAmount
      );
      state.error = null;
    } catch (err) {
      state.error = err instanceof Error ? err.message : "Failed to rotate sequence";
    }
  }
  function validateCurrentSequence(): ValidationResult | null {
    if (!state.currentSequence || !sequenceStateService) return null;
    return sequenceStateService.validateSequence(state.currentSequence);
  }
  function isBeatSelected(index: number): boolean {
    return state.selectedBeatIndex === index;
  }
  function getBeat(index: number): BeatData | null {
    if (sequenceStateService)
      return sequenceStateService.getSelectedBeat(state.currentSequence, index);
    if (!state.currentSequence) return null;
    return state.currentSequence.beats[index] ?? null;
  }
  function hasContent(): boolean {
    return state.currentSequence?.beats.some((b) => !b.isBlank) ?? false;
  }

  return {
    get currentSequence() {
      return state.currentSequence;
    },
    get sequences() {
      return state.sequences;
    },
    get isLoading() {
      return state.isLoading;
    },
    get error() {
      return state.error;
    },
    get selectedBeatIndex() {
      return state.selectedBeatIndex;
    },
    get selectedSequenceId() {
      return state.selectedSequenceId;
    },
    get showBeatNumbers() {
      return state.showBeatNumbers;
    },
    get gridMode() {
      return state.gridMode;
    },
    get arrowPositions() {
      return state.arrowPositions;
    },
    get arrowPositioningInProgress() {
      return state.arrowPositioningInProgress;
    },
    get arrowPositioningError() {
      return state.arrowPositioningError;
    },
    get selectedStartPosition() {
      return state.selectedStartPosition;
    },
    get hasStartPosition() {
      return state.hasStartPosition;
    },
    get isInitialized() {
      return state.isInitialized;
    },

    // Getters
    getCurrentSequence: () => state.currentSequence,

    // CONSOLIDATION: Single source of truth for current sequence data as PictographData array
    getCurrentSequenceData: () => {
      const sequence = state.currentSequence;
      if (sequence) {
        const beats = sequence.beats || [];

        // Check for start position if there are no beats yet
        const startPosition = sequence.startingPositionBeat || sequence.startPosition;

        let result: any[] = [];

        // If we have beats, use them
        if (beats.length > 0) {
          result = beats.map((beat: any) => beat.pictographData).filter(Boolean);
          return result;
        }
        // If no beats but we have a start position in the sequence, include it
        else if (startPosition?.pictographData) {
          result = [startPosition.pictographData];
          return result;
        }

        // Fall through to check selectedStartPosition below
      }

      // If no sequence but we have a selected start position (e.g., from persistence), use it
      if (state.selectedStartPosition) {
        return [state.selectedStartPosition];
      }

      return [];
    },
    getSequences,
    getIsLoading,
    getError,
    getSelectedBeatIndex,
    getSelectedSequenceId,
    getShowBeatNumbers,
    getGridMode,
    getArrowPositions,
    getArrowPositioningInProgress,
    getArrowPositioningError,

    // Computed getters
    getCurrentBeats,
    getSelectedBeatData,
    getSelectedBeat: getSelectedBeat,
    getHasCurrentSequence: hasCurrentSequence,
    getSequenceCount,
    getHasUnsavedChanges,
    getHasArrowPositions,
    getArrowPositioningComplete,
    hasSequence: hasCurrentSequence,
    beatCount: getBeatCount,
    sequenceStatistics: getSequenceStatistics,
    sequenceWord: getSequenceWord,
    sequenceDuration: getSequenceDuration,

    // Actions
    setCurrentSequence,
    addSequence,
    updateSequence,
    removeSequence,
    setSequences,
    setLoading,
    setError,
    clearError,
    updateCurrentBeat,
    selectBeat,
    setGridMode,
    setShowBeatNumbers,
    setArrowPositions,
    setArrowPositioningInProgress,
    setArrowPositioningError,
    getArrowPosition,
    clearArrowPositions,
    resetSequenceState,
    clearSelection,
    addBeat,
    removeBeat,
    updateBeat,
    insertBeat,
    clearSequence: clearSequenceBeats,
    clearSequenceCompletely: clearSequence,
    duplicateSequence,
    setStartPosition,
    setSelectedStartPosition,
    mirrorSequence,
    swapColors,
    rotateSequence,
    validateCurrentSequence,
    isBeatSelected,
    getBeat,
    hasContent,

    // Persistence functions
    initializeWithPersistence,
    saveCurrentState,
    saveSequenceDataOnly,
    clearPersistedState,

    // Service integration
    loadSequences,
    createSequence,
    updateSequenceBeats,
  };
}

export type SequenceState = ReturnType<typeof createSequenceState>;
