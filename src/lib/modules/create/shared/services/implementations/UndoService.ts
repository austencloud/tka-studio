/**
 * Undo/Redo Service Implementation
 *
 * Professional undo/redo management using Command Pattern with persistent storage.
 * Handles complex async operations and provides a clean API for Create module operations.
 *
 * Uses Svelte 5 runes for reactive state management.
 */

import { injectable } from "inversify";
import type {
  CreateModuleStateSnapshot,
  IUndoService,
  UndoHistoryEntry,
  UndoMetadata,
  UndoOperationType,
} from "../contracts/IUndoService";

/**
 * Default maximum number of undo entries to keep
 */
const DEFAULT_MAX_HISTORY_SIZE = 50;

/**
 * LocalStorage key for persisting undo history
 */
const UNDO_HISTORY_STORAGE_KEY = "tka_build_undo_history";

/**
 * LocalStorage key for persisting redo history
 */
const REDO_HISTORY_STORAGE_KEY = "tka_build_redo_history";

/**
 * Human-readable descriptions for operation types
 */
const OPERATION_DESCRIPTIONS: Record<UndoOperationType, string> = {
  SELECT_START_POSITION: "Select Start Position",
  ADD_BEAT: "Add Beat",
  REMOVE_BEATS: "Remove Beats",
  CLEAR_SEQUENCE: "Clear Sequence",
  UPDATE_BEAT: "Update Beat",
  INSERT_BEAT: "Insert Beat",
  MIRROR_SEQUENCE: "Mirror Sequence",
  ROTATE_SEQUENCE: "Rotate Sequence",
  SWAP_COLORS: "Swap Colors",
  MODIFY_BEAT_PROPERTIES: "Modify Beat Properties",
  GENERATE_SEQUENCE: "Generate Sequence",
};

@injectable()
export class UndoService implements IUndoService {
  // Pure TypeScript arrays - reactivity handled by wrapper
  private _undoHistory: UndoHistoryEntry[] = [];
  private _redoHistory: UndoHistoryEntry[] = [];
  private _maxHistorySize: number = DEFAULT_MAX_HISTORY_SIZE;
  private _changeCallbacks: Set<() => void> = new Set();

  constructor() {
    // Load persisted history
    this.loadHistory();
  }

  // ============================================================================
  // EVENT SYSTEM FOR REACTIVITY
  // ============================================================================

  /**
   * Subscribe to changes in undo/redo state
   */
  onChange(callback: () => void): () => void {
    this._changeCallbacks.add(callback);
    // Return unsubscribe function
    return () => this._changeCallbacks.delete(callback);
  }

  /**
   * Notify all subscribers of state change
   */
  private notifyChange(): void {
    this._changeCallbacks.forEach((callback) => callback());
  }

  // ============================================================================
  // PUBLIC GETTERS
  // ============================================================================

  get maxHistorySize(): number {
    return this._maxHistorySize;
  }

  get canUndo(): boolean {
    return this._undoHistory.length > 0;
  }

  get canRedo(): boolean {
    return this._redoHistory.length > 0;
  }

  get undoHistory(): ReadonlyArray<UndoHistoryEntry> {
    return this._undoHistory;
  }

  get redoHistory(): ReadonlyArray<UndoHistoryEntry> {
    return this._redoHistory;
  }

  // ============================================================================
  // PUBLIC METHODS
  // ============================================================================

  /**
   * Push a new action to the undo history
   */
  pushUndo(
    type: UndoOperationType,
    beforeState: CreateModuleStateSnapshot,
    metadata?: UndoMetadata
  ): string {
    // Generate unique ID for this action
    const id = this.generateActionId();

    // Create history entry
    const entry: UndoHistoryEntry = {
      id,
      type,
      timestamp: Date.now(),
      beforeState,
      metadata: metadata ?? { description: "" },
    };

    // Add to undo history
    this._undoHistory.push(entry);

    // Trim history if it exceeds max size
    if (this._undoHistory.length > this._maxHistorySize) {
      this._undoHistory.shift();
    }

    // Clear redo history when new action is performed
    this._redoHistory = [];

    // Persist to storage
    this.saveHistory().catch((error) => {
      console.error(
        "❌ UndoService: Failed to save history after push:",
        error
      );
    });

    // Notify subscribers of change
    this.notifyChange();

    return id;
  }

  /**
   * Undo the last operation
   */
  undo(): UndoHistoryEntry | null {
    if (!this.canUndo) {
      return null;
    }

    // Pop from undo history
    const entry = this._undoHistory.pop()!;

    // Move to redo history
    this._redoHistory.push(entry);

    // Persist to storage
    this.saveHistory().catch((error) => {
      console.error(
        "❌ UndoService: Failed to save history after undo:",
        error
      );
    });

    // Notify subscribers of change
    this.notifyChange();

    return entry;
  }

  /**
   * Redo the last undone operation
   */
  redo(): UndoHistoryEntry | null {
    if (!this.canRedo) {
      return null;
    }

    // Pop from redo history
    const entry = this._redoHistory.pop()!;

    // Move back to undo history
    this._undoHistory.push(entry);

    // Persist to storage
    this.saveHistory().catch((error) => {
      console.error(
        "❌ UndoService: Failed to save history after redo:",
        error
      );
    });

    // Notify subscribers of change
    this.notifyChange();

    return entry;
  }

  /**
   * Clear all undo and redo history
   */
  clearHistory(): void {
    this._undoHistory = [];
    this._redoHistory = [];

    // Persist to storage
    this.saveHistory().catch((error) => {
      console.error(
        "❌ UndoService: Failed to save history after clear:",
        error
      );
    });

    // Notify subscribers of change
    this.notifyChange();
  }

  /**
   * Clear only redo history
   */
  clearRedoHistory(): void {
    this._redoHistory = [];

    // Persist to storage
    this.saveHistory().catch((error) => {
      console.error(
        "❌ UndoService: Failed to save history after clearing redo:",
        error
      );
    });

    // Notify subscribers of change
    this.notifyChange();
  }

  /**
   * Get description of last undoable action
   */
  getLastUndoDescription(): string | null {
    if (!this.canUndo) {
      return null;
    }

    const lastEntry = this._undoHistory[this._undoHistory.length - 1];
    if (!lastEntry) {
      return null;
    }

    // Use custom description if provided
    if (lastEntry && lastEntry.metadata?.description) {
      return lastEntry.metadata.description;
    }

    // Fall back to operation type description
    return OPERATION_DESCRIPTIONS[lastEntry!.type] || "Last Action";
  }

  /**
   * Get description of last redoable action
   */
  getLastRedoDescription(): string | null {
    if (!this.canRedo) {
      return null;
    }

    const lastEntry = this._redoHistory[this._redoHistory.length - 1];
    if (!lastEntry) {
      return null;
    }

    // Use custom description if provided
    if (lastEntry && lastEntry.metadata?.description) {
      return lastEntry.metadata.description;
    }

    // Fall back to operation type description
    return OPERATION_DESCRIPTIONS[lastEntry!.type] || "Last Action";
  }

  /**
   * Load history from persistent storage
   */
  async loadHistory(): Promise<void> {
    try {
      // Load undo history
      const undoData = localStorage.getItem(UNDO_HISTORY_STORAGE_KEY);
      if (undoData) {
        this._undoHistory = JSON.parse(undoData);
      }

      // Load redo history
      const redoData = localStorage.getItem(REDO_HISTORY_STORAGE_KEY);
      if (redoData) {
        this._redoHistory = JSON.parse(redoData);
      }

      // Notify subscribers after loading
      this.notifyChange();
    } catch (error) {
      console.error(
        "❌ UndoService: Failed to load history from storage:",
        error
      );
      // Reset to empty on error
      this._undoHistory = [];
      this._redoHistory = [];
      this.notifyChange();
    }
  }

  /**
   * Save history to persistent storage
   */
  async saveHistory(): Promise<void> {
    try {
      localStorage.setItem(
        UNDO_HISTORY_STORAGE_KEY,
        JSON.stringify(this._undoHistory)
      );
      localStorage.setItem(
        REDO_HISTORY_STORAGE_KEY,
        JSON.stringify(this._redoHistory)
      );
    } catch (error) {
      console.error(
        "❌ UndoService: Failed to save history to storage:",
        error
      );
      throw error;
    }
  }

  /**
   * Peek at the state that would be restored by undo
   */
  peekUndoState(): CreateModuleStateSnapshot | null {
    if (!this.canUndo) {
      return null;
    }

    const lastEntry = this._undoHistory[this._undoHistory.length - 1];
    return lastEntry ? lastEntry!.beforeState : null;
  }

  /**
   * Peek at the state that would be restored by redo
   */
  peekRedoState(): CreateModuleStateSnapshot | null {
    if (!this.canRedo) {
      return null;
    }

    // For redo, we want the "after" state, which is the current state when the action was performed
    const entry = this._redoHistory[this._redoHistory.length - 1];
    return entry ? entry!.afterState || null : null;
  }

  // ============================================================================
  // PRIVATE METHODS
  // ============================================================================

  /**
   * Generate a unique action ID
   */
  private generateActionId(): string {
    return `${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
  }
}
