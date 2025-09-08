/**

 *
 * Extracted business logic from WorkbenchService.svelte.ts
 * Contains only pure functions with no reactive state.
 */

import type {
  PictographData,
  SequenceData,
  ValidationResult,
} from "$shared";
import {
  createPictographData,
  GridMode,
  Letter,
} from "$shared";
import { injectable } from "inversify";
import type { IWorkbenchService } from "../contracts";
import { type BeatData, type WorkbenchConfig, type WorkbenchMode, type BeatEditOperation, createBeatData, type SequenceCreationParams } from "../../domain";
@injectable()
export class WorkbenchService implements IWorkbenchService {
  private currentBeat: BeatData | null = null;
  private config: WorkbenchConfig = {
    mode: "edit",
    isInitialized: false
  };

  // ============================================================================
  // REQUIRED INTERFACE METHODS
  // ============================================================================

  getConfig(): WorkbenchConfig {
    return this.config;
  }

  async initializeWorkbench(): Promise<void> {
    console.log("✅ WorkbenchService: Workbench initialized");
  }

  getCurrentBeat(): BeatData | null {
    return this.currentBeat;
  }

  async updateBeat(beat: BeatData): Promise<void> {
    this.currentBeat = beat;
    console.log("✅ WorkbenchService: Beat updated", beat);
  }

  clearWorkbench(): void {
    this.currentBeat = null;
    console.log("✅ WorkbenchService: Workbench cleared");
  }

  // ============================================================================
  // INITIALIZATION
  // ============================================================================

  initialize(): WorkbenchConfig {
    return {
      mode: "construct",
      isInitialized: true,
    };
  }

  isInitialized(config: WorkbenchConfig): boolean {
    return config.isInitialized;
  }

  // ============================================================================
  // MODE MANAGEMENT
  // ============================================================================

  setMode(config: WorkbenchConfig, mode: WorkbenchMode): WorkbenchConfig {
    return {
      ...config,
      mode,
    };
  }

  canEditInMode(mode: WorkbenchMode): boolean {
    return mode === "construct" || mode === "edit";
  }

  // ============================================================================
  // BEAT INTERACTION LOGIC
  // ============================================================================

  shouldSelectBeatOnClick(_mode: WorkbenchMode, beatIndex: number): boolean {
    return beatIndex >= 0; // Always select valid beats
  }

  shouldEditBeatOnDoubleClick(mode: WorkbenchMode, beatIndex: number): boolean {
    return this.canEditInMode(mode) && beatIndex >= 0;
  }

  // ============================================================================
  // BEAT EDITING OPERATIONS
  // ============================================================================

  createEditBeatOperation(
    beatIndex: number,
    sequence: SequenceData | null
  ): BeatEditOperation | null {
    if (!this.isValidBeatIndex(sequence, beatIndex)) {
      return null;
    }

    return {
      beatIndex,
      operation: "edit",
    };
  }

  createClearBeatOperation(
    beatIndex: number,
    sequence: SequenceData | null
  ): BeatEditOperation | null {
    if (!this.isValidBeatIndex(sequence, beatIndex)) {
      return null;
    }

    return {
      beatIndex,
      operation: "clear",
    };
  }

  // ============================================================================
  // BEAT DATA CREATION
  // ============================================================================

  createDefaultPictographData(letter: Letter = Letter.A): PictographData {
    return createPictographData({
      letter,
    });
  }

  createEditedBeatData(
    originalBeat: BeatData,
    pictographData: PictographData
  ): BeatData {
    return createBeatData({
      ...originalBeat,
      isBlank: false,
      pictographData,
    });
  }

  createClearedBeatData(originalBeat: BeatData): BeatData {
    return createBeatData({
      ...originalBeat,
      isBlank: true,
      pictographData: null,
    });
  }

  // ============================================================================
  // SEQUENCE OPERATIONS
  // ============================================================================

  validateSequenceCreation(name: string, length: number): ValidationResult {
    const errors: string[] = [];
    const warnings: string[] = [];

    if (!name.trim()) {
      errors.push("Sequence name is required");
    }

    if (length < 1) {
      errors.push("Sequence length must be at least 1");
    }

    if (length > 64) {
      errors.push("Sequence length cannot exceed 64 beats");
    }

    if (length > 32) {
      warnings.push("Large sequences may impact performance");
    }

    return {
      isValid: errors.length === 0,
      errors: errors.map((err) => ({
        message: err,
        code: "VALIDATION_ERROR",
        severity: "error" as const,
      })),
      warnings: warnings.map((warn) => ({
        message: warn,
        code: "VALIDATION_WARNING",
        severity: "warning" as const,
      })),
    };
  }

  createSequenceCreationParams(
    name: string = "New Sequence",
    length: number = 16
  ): SequenceCreationParams {
    return {
      name: name.trim() || "New Sequence",
      length: Math.max(1, Math.min(64, length)),
    };
  }

  // ============================================================================
  // CONFIGURATION OPERATIONS
  // ============================================================================

  validateGridModeChange(_currentMode: GridMode, newMode: GridMode): boolean {
    // All grid mode changes are valid
    return Object.values(GridMode).includes(newMode);
  }

  validateBeatSizeChange(_currentSize: number, newSize: number): boolean {
    return newSize >= 50 && newSize <= 300;
  }

  // ============================================================================
  // VALIDATION HELPERS
  // ============================================================================

  isValidBeatIndex(sequence: SequenceData | null, beatIndex: number): boolean {
    if (!sequence) return false;
    return beatIndex >= 0 && beatIndex < sequence.beats.length;
  }

  canEditBeat(
    sequence: SequenceData | null,
    beatIndex: number
  ): boolean {
    return (
      this.canEditInMode(this.config.mode) && this.isValidBeatIndex(sequence, beatIndex)
    );
  }

  canClearBeat(sequence: SequenceData | null, beatIndex: number): boolean {
    if (!this.isValidBeatIndex(sequence, beatIndex)) {
      return false;
    }

    if (!sequence) {
      return false;
    }

    const beat = sequence.beats[beatIndex];
    return !beat.isBlank; // Can only clear non-blank beats
  }

  // ============================================================================
  // BEAT OPERATION HELPERS
  // ============================================================================

  /**
   * Determines if a beat should be edited or toggled based on its current state
   */
  getBeatEditAction(beat: BeatData): "edit" | "clear" {
    return beat.isBlank ? "edit" : "clear";
  }

  /**
   * Creates appropriate beat data based on the edit action
   */
  applyBeatEditAction(beat: BeatData, action: "edit" | "clear"): BeatData {
    if (action === "edit") {
      const pictographData = this.createDefaultPictographData();
      return this.createEditedBeatData(beat, pictographData);
    } else {
      return this.createClearedBeatData(beat);
    }
  }

  /**
   * Validates that a beat edit operation can be performed
   */
  validateBeatEditOperation(
    operation: BeatEditOperation,
    sequence: SequenceData | null,
    mode: WorkbenchMode
  ): ValidationResult {
    const errors: string[] = [];

    if (!this.isValidBeatIndex(sequence, operation.beatIndex)) {
      errors.push(`Invalid beat index: ${operation.beatIndex}`);
    }

    if (!this.canEditInMode(mode)) {
      errors.push(`Cannot edit beats in ${mode} mode`);
    }

    if (operation.operation === "clear" && sequence) {
      const beat = sequence.beats[operation.beatIndex];
      if (beat?.isBlank) {
        errors.push("Cannot clear an already blank beat");
      }
    }

    return {
      isValid: errors.length === 0,
      errors: errors.map((err) => ({
        message: err,
        code: "VALIDATION_ERROR",
        severity: "error" as const,
      })),
      warnings: [],
    };
  }


}
