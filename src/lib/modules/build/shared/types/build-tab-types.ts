/**
 * Build Tab Type Definitions
 *
 * Centralized type definitions for BuildTab components and state.
 * Extracted from inline types in ToolPanel.svelte for better maintainability.
 */

import type { ActiveBuildTab, BeatData, PictographData } from "$shared";
import type { SimplifiedStartPositionState } from "../../construct/start-position-picker/state/start-position-state.svelte";
import type { UndoHistoryEntry, UndoMetadata } from "../services/contracts/IUndoService";
import type { SequenceState } from "../state/SequenceStateOrchestrator.svelte";

/**
 * Build Tab State Interface
 *
 * Master tab state shared across all sub-tabs (Construct, Generate, Edit, Export).
 */
export interface IBuildTabState {
  // Loading and error state
  readonly isLoading: boolean;
  readonly error: string | null;
  readonly isTransitioning: boolean;
  readonly hasError: boolean;

  // Sequence state
  readonly hasSequence: boolean;
  readonly sequenceState: SequenceState;

  // Navigation state
  readonly activeSection: ActiveBuildTab | null;
  readonly canGoBack: boolean;
  readonly isNavigatingBack: boolean;

  // History tracking
  readonly hasOptionHistory: boolean;
  readonly canUndo: boolean;

  // Persistence state
  readonly isPersistenceInitialized: boolean;
  readonly isSectionLoading: boolean;

  // Tab accessibility
  readonly canAccessEditTab: boolean;
  readonly canAccessExportTab: boolean;

  // State mutations
  setLoading: (loading: boolean) => void;
  setTransitioning: (transitioning: boolean) => void;
  setError: (errorMessage: string | null) => void;
  clearError: () => void;
  setactiveToolPanel: (panel: ActiveBuildTab) => void;
  goBack: () => void;

  // Option history management
  addOptionToHistory: (beatIndex: number, beatData: BeatData) => void;
  popLastOptionFromHistory: () => { beatIndex: number; beatData: BeatData; timestamp: number } | null;
  clearOptionHistory: () => void;

  // Undo history management
  readonly undoHistory: ReadonlyArray<UndoHistoryEntry>;
  pushUndoSnapshot: (
    type: 'REMOVE_BEATS' | 'CLEAR_SEQUENCE' | 'ADD_BEAT' | 'SELECT_START_POSITION',
    metadata?: UndoMetadata
  ) => void;
  undo: () => boolean;
  clearUndoHistory: () => void;
  setShowStartPositionPickerCallback: (callback: () => void) => void;
  setOnUndoingOptionCallback: (callback: (isUndoing: boolean) => void) => void;

  // Persistence
  initializeWithPersistence: () => Promise<void>;
  saveCurrentState: () => Promise<void>;
}

/**
 * Construct Tab State Interface
 *
 * State specific to the Construct sub-tab functionality.
 */
export interface IConstructTabState {
  // Loading and error state
  readonly isLoading: boolean;
  readonly error: string | null;
  readonly isTransitioning: boolean;
  readonly hasError: boolean;

  // Picker state
  readonly canSelectOptions: boolean;
  readonly showStartPositionPicker: boolean | null;
  readonly shouldShowStartPositionPicker: () => boolean | null;
  readonly isPickerStateLoading: boolean;

  // Initialization state
  readonly isInitialized: boolean;

  // Selection state
  readonly selectedStartPosition: PictographData | null;

  // Filter state
  readonly isContinuousOnly: boolean;

  // Services
  readonly startPositionStateService: SimplifiedStartPositionState;

  // State mutations
  setLoading: (loading: boolean) => void;
  setTransitioning: (transitioning: boolean) => void;
  setError: (errorMessage: string | null) => void;
  clearError: () => void;
  setShowStartPositionPicker: (show: boolean) => void;
  setSelectedStartPosition: (position: PictographData | null) => void;
  setContinuousOnly: (continuous: boolean) => void;
  clearSequenceCompletely: () => Promise<void>;
  restorePickerStateAfterUndo: () => void;
  syncPickerStateWithSequence: () => void;

  // Event handlers
  handleStartPositionSelected: (pictographData: PictographData | null, source?: "user" | "sync") => void;

  // Initialization
  initializeConstructTab: () => Promise<void>;
}

/**
 * Animation Panel State Interface
 *
 * State for animation panel collapse/expand and visibility.
 */
export interface IAnimationPanelState {
  readonly isAnimationVisible: boolean;
  readonly isAnimationCollapsed: boolean;
  toggleAnimationCollapse: () => void;
  setAnimationVisible: (visible: boolean) => void;
}

/**
 * Animation State Reference Interface
 *
 * Shared reference between AnimationPanel and AnimateControls.
 */
export interface IAnimationStateRef {
  isPlaying: boolean;
  currentBeat: number;
  totalBeats: number;
  speed: number;
  shouldLoop: boolean;
  play: () => void;
  stop: () => void;
  jumpToBeat: (beat: number) => void;
  setSpeed: (speed: number) => void;
  setShouldLoop: (loop: boolean) => void;
  nextBeat: () => void;
  previousBeat: () => void;
}

/**
 * Tool Panel Props Interface
 *
 * Props passed to ToolPanel component from parent BuildTab.
 */
export interface IToolPanelProps {
  buildTabState: IBuildTabState;
  constructTabState: IConstructTabState;
  onOptionSelected: (option: PictographData) => Promise<void>;
  onPracticeBeatIndexChange?: (index: number | null) => void;
  isSideBySideLayout?: () => boolean;
  activeTab?: ActiveBuildTab | null;
  onTabChange?: (tab: ActiveBuildTab) => void;
  onOpenFilters?: () => void;
  onCloseFilters?: () => void;
  isFilterPanelOpen?: boolean;
}

/**
 * Tool Panel Methods Interface
 *
 * Public methods exposed by ToolPanel component via ref binding.
 */
export interface IToolPanelMethods {
  getAnimationStateRef: () => IAnimationStateRef;
}

/**
 * Batch Edit Changes Interface
 *
 * Partial beat data changes that can be applied to multiple beats at once.
 */
export type BatchEditChanges = Partial<BeatData>;
