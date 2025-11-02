/**
 * Undo/Redo Service Interface
 *
 * Professional undo/redo management for Build tab operations.
 * Implements Command Pattern with action bundling for complex async operations.
 *
 * Based on industry best practices from modern web applications:
 * - Command Pattern for reversible operations
 * - Action bundling for handling concurrent async operations
 * - Memento Pattern for state snapshots
 * - Persistent history across sessions
 */

import type { ActiveBuildTab, SequenceData } from '$shared';

/**
 * Types of undoable operations in the Build tab
 */
export enum UndoOperationType {
  // Sequence construction operations
  SELECT_START_POSITION = 'SELECT_START_POSITION',
  ADD_BEAT = 'ADD_BEAT',
  REMOVE_BEATS = 'REMOVE_BEATS',
  CLEAR_SEQUENCE = 'CLEAR_SEQUENCE',

  // Beat modification operations Is it a bad idea to leave my King Song 18XL electric unicycle plugged in overnight I'm sorry I finished your thought
  UPDATE_BEAT = 'UPDATE_BEAT',
  INSERT_BEAT = 'INSERT_BEAT',

  // Transform operations
  MIRROR_SEQUENCE = 'MIRROR_SEQUENCE',
  ROTATE_SEQUENCE = 'ROTATE_SEQUENCE',
  SWAP_COLORS = 'SWAP_COLORS',

  // Edit operations
  MODIFY_BEAT_PROPERTIES = 'MODIFY_BEAT_PROPERTIES',

  // Generate operations
  GENERATE_SEQUENCE = 'GENERATE_SEQUENCE',
}

/**
 * Metadata for undo history entries
 */
export interface UndoMetadata {
  beatIndex?: number;
  beatsRemoved?: number;
  description?: string;
  [key: string]: unknown; // Allow additional metadata
}

/**
 * Snapshot of Build tab state at a specific point in time
 */
export interface BuildTabStateSnapshot {
  sequence: SequenceData | null;
  selectedBeatNumber: number | null;  // 0=start, 1=first beat, 2=second beat
  activeSection: ActiveBuildTab | null;
  shouldShowStartPositionPicker?: boolean;
  timestamp: number;
}

/**
 * A single undoable action in the history
 */
export interface UndoHistoryEntry {
  id: string; // Unique identifier for this action
  type: UndoOperationType;
  timestamp: number;
  beforeState: BuildTabStateSnapshot;
  afterState?: BuildTabStateSnapshot; // Optional: for redo optimization
  metadata?: UndoMetadata;
}

/**
 * Undo/Redo Service Interface
 */
export interface IUndoService {
  /**
   * Maximum number of undo entries to keep in history
   */
  readonly maxHistorySize: number;

  /**
   * Whether there are actions that can be undone
   */
  readonly canUndo: boolean;

  /**
   * Whether there are actions that can be redone
   */
  readonly canRedo: boolean;

  /**
   * Current undo history (for debugging/UI display)
   */
  readonly undoHistory: ReadonlyArray<UndoHistoryEntry>;

  /**
   * Current redo history (for debugging/UI display)
   */
  readonly redoHistory: ReadonlyArray<UndoHistoryEntry>;

  /**
   * Push a new action to the undo history
   * Clears redo history when a new action is performed
   *
   * @param type - Type of operation being performed
   * @param beforeState - State snapshot before the operation
   * @param metadata - Optional metadata about the operation
   * @returns The unique ID of the created history entry
   */
  pushUndo(
    type: UndoOperationType,
    beforeState: BuildTabStateSnapshot,
    metadata?: UndoMetadata
  ): string;

  /**
   * Undo the last operation
   * Moves the entry from undo history to redo history
   *
   * @returns The history entry that was undone, or null if nothing to undo
   */
  undo(): UndoHistoryEntry | null;

  /**
   * Redo the last undone operation
   * Moves the entry from redo history back to undo history
   *
   * @returns The history entry that was redone, or null if nothing to redo
   */
  redo(): UndoHistoryEntry | null;

  /**
   * Clear all undo and redo history
   */
  clearHistory(): void;

  /**
   * Clear only redo history (called when new action is performed)
   */
  clearRedoHistory(): void;

  /**
   * Get a human-readable description of the last undoable action
   *
   * @returns Description string or null if no undo available
   */
  getLastUndoDescription(): string | null;

  /**
   * Get a human-readable description of the last redoable action
   *
   * @returns Description string or null if no redo available
   */
  getLastRedoDescription(): string | null;

  /**
   * Load undo/redo history from persistent storage
   * Called during initialization
   */
  loadHistory(): Promise<void>;

  /**
   * Save undo/redo history to persistent storage
   * Called after each history modification
   */
  saveHistory(): Promise<void>;

  /**
   * Get the state snapshot that would be restored by undo
   * Useful for preview/debugging without actually undoing
   *
   * @returns The state snapshot or null if nothing to undo
   */
  peekUndoState(): BuildTabStateSnapshot | null;

  /**
   * Get the state snapshot that would be restored by redo
   * Useful for preview/debugging without actually redoing
   *
   * @returns The state snapshot or null if nothing to redo
   */
  peekRedoState(): BuildTabStateSnapshot | null;

  /**
   * Subscribe to changes in undo/redo state
   * Used by reactive wrappers to track state changes
   *
   * @param callback - Function to call when state changes
   * @returns Unsubscribe function
   */
  onChange(callback: () => void): () => void;
}
