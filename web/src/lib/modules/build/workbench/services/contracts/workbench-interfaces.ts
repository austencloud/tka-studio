/**
 * Workbench Service Interfaces
 *
 * Pure TypeScript interfaces for workbench coordination services.
 * Extracted from WorkbenchService.svelte.ts to enable clean architecture.
 */
// ============================================================================
// WORKBENCH TYPES
// ============================================================================
import type {
  BeatClickResult,
  BeatData,
  BeatEditOperation,
  BeatEditResult,
  ConfigurationResult,
  Letter,
  PictographData,
  SequenceCreationParams,
  SequenceCreationResult,
  SequenceData,
  ValidationResult,
  WorkbenchConfig,
  WorkbenchMode,
} from "$domain";
import { GridMode } from "$domain";

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

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

export interface IWorkbenchCoordinationService {
  // Service coordination
  handleBeatClick(beatIndex: number, mode: WorkbenchMode): BeatClickResult;
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
