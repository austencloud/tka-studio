/**
 * Workbench Service Interfaces
 *
 * Pure TypeScript interfaces for workbench coordination services.
 * Extracted from WorkbenchService.svelte.ts to enable clean architecture.
 */

import type { BeatData, SequenceData, PictographData } from "$lib/domain";
import { GridMode } from "$lib/domain";
import type { Letter } from "$lib/domain/Letter";

// ============================================================================
// WORKBENCH TYPES
// ============================================================================

export type WorkbenchMode = "view" | "edit" | "construct";

export interface WorkbenchConfig {
  mode: WorkbenchMode;
  isInitialized: boolean;
}

export interface BeatEditOperation {
  beatIndex: number;
  operation: "edit" | "clear" | "toggle";
  data?: Partial<BeatData>;
}

export interface BeatEditResult {
  success: boolean;
  updatedBeat?: BeatData;
  error?: string;
}

// ============================================================================
// SERVICE INTERFACES
// ============================================================================

/**
 * Pure business logic service for workbench coordination
 */
export interface IWorkbenchService {
  // Initialization
  initialize(): WorkbenchConfig;
  isInitialized(config: WorkbenchConfig): boolean;

  // Mode management
  setMode(config: WorkbenchConfig, mode: WorkbenchMode): WorkbenchConfig;
  canEditInMode(mode: WorkbenchMode): boolean;

  // Beat interaction logic
  shouldSelectBeatOnClick(mode: WorkbenchMode, beatIndex: number): boolean;
  shouldEditBeatOnDoubleClick(mode: WorkbenchMode, beatIndex: number): boolean;

  // Beat editing operations
  createEditBeatOperation(
    beatIndex: number,
    sequence: SequenceData | null
  ): BeatEditOperation | null;
  createClearBeatOperation(
    beatIndex: number,
    sequence: SequenceData | null
  ): BeatEditOperation | null;

  // Beat data creation
  createDefaultPictographData(letter?: Letter): PictographData;
  createEditedBeatData(
    originalBeat: BeatData,
    pictographData: PictographData
  ): BeatData;
  createClearedBeatData(originalBeat: BeatData): BeatData;

  // Sequence operations
  validateSequenceCreation(name: string, length: number): ValidationResult;
  createSequenceCreationParams(
    name?: string,
    length?: number
  ): SequenceCreationParams;

  // Configuration operations
  validateGridModeChange(currentMode: GridMode, newMode: GridMode): boolean;
  validateBeatSizeChange(currentSize: number, newSize: number): boolean;

  // Validation helpers
  isValidBeatIndex(sequence: SequenceData | null, beatIndex: number): boolean;
  canEditBeat(
    sequence: SequenceData | null,
    beatIndex: number,
    mode: WorkbenchMode
  ): boolean;
  canClearBeat(sequence: SequenceData | null, beatIndex: number): boolean;
}

/**
 * Workbench coordination service for managing service interactions
 */
export interface IWorkbenchCoordinationService {
  // Service coordination
  handleBeatClick(beatIndex: number, mode: WorkbenchMode): BeatClickResult;
  handleBeatDoubleClick(
    beatIndex: number,
    mode: WorkbenchMode,
    sequence: SequenceData | null
  ): BeatEditResult;
  handleBeatHover(beatIndex: number): void;
  handleBeatLeave(): void;

  // Beat operations coordination
  editBeat(
    beatIndex: number,
    sequence: SequenceData | null,
    mode: WorkbenchMode
  ): BeatEditResult;
  clearBeat(beatIndex: number, sequence: SequenceData | null): BeatEditResult;

  // Sequence operations coordination
  createNewSequence(name?: string, length?: number): SequenceCreationResult;

  // Configuration coordination
  setGridMode(mode: GridMode): ConfigurationResult;
  setBeatSize(size: number): ConfigurationResult;
}

// ============================================================================
// SUPPORTING TYPES
// ============================================================================

export interface ValidationResult {
  isValid: boolean;
  errors: string[];
  warnings: string[];
}

export interface SequenceCreationParams {
  name: string;
  length: number;
}

export interface SequenceCreationResult {
  success: boolean;
  sequence?: SequenceData;
  error?: string;
}

export interface BeatClickResult {
  shouldSelect: boolean;
  beatIndex: number;
}

export interface ConfigurationResult {
  success: boolean;
  error?: string;
}

export interface WorkbenchState {
  config: WorkbenchConfig;
  currentSequence: SequenceData | null;
  selectedBeatIndex: number;
  hoveredBeatIndex: number;
}

export interface WorkbenchActions {
  // Mode actions
  initialize(): void;
  setMode(mode: WorkbenchMode): void;

  // Beat interaction actions
  handleBeatClick(index: number): void;
  handleBeatDoubleClick(index: number): void;
  handleBeatHover(index: number): void;
  handleBeatLeave(): void;

  // Beat editing actions
  editBeat(index: number): void;
  clearBeat(index: number): void;

  // Sequence actions
  createNewSequence(name?: string, length?: number): void;

  // Configuration actions
  setGridMode(mode: GridMode): void;
  setBeatSize(size: number): void;
}
