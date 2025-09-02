/**
 * Workbench Models
 *
 * Interface definitions for workbench data structures.
 * Contains only data models, not service contracts.
 */

import type { BeatData, SequenceData, WorkbenchMode } from "$domain";
import { GridMode } from "$domain";

// ============================================================================
// DOMAIN DATA MODELS
// ============================================================================

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

// ============================================================================
// BEAT FRAME MODELS
// ============================================================================

export interface ContainerDimensions {
  width: number;
  height: number;
  isFullscreen: boolean;
}

export interface BeatFrameConfig {
  cellSize: number;
  beatSize: number; // Alias for cellSize for backward compatibility
  gap: number;
  columns: number;
  hasStartTile: boolean;
  showBeatNumbers: boolean;
  enableHover: boolean;
  enableDrag: boolean;
  gridMode?: GridMode;
}

export interface LayoutInfo {
  rows: number;
  columns: number;
  cellSize: number;
  totalWidth: number;
  totalHeight: number;
  shouldScroll: boolean;
}
