/**
 * Beat Frame Service Interfaces
 *
 * Pure TypeScript interfaces for beat frame layout and positioning services.
 * Extracted from BeatFrameService.svelte.ts to enable clean architecture.
 */

import type { BeatData } from "$lib/domain";
import { GridMode } from "$lib/domain";

// ============================================================================
// CONFIGURATION TYPES
// ============================================================================

export interface BeatFrameConfig {
  /** Number of columns allocated for BEATS (excludes the Start tile column) */
  columns: number;
  beatSize: number;
  gap: number;
  gridMode: GridMode;
  /** Whether to reserve the first column for the Start Position tile */
  hasStartTile: boolean;
}

export interface ContainerDimensions {
  width: number;
  height: number;
  isFullscreen: boolean;
}

export interface LayoutInfo {
  rows: number;
  columns: number;
  cellSize: number;
  totalWidth: number;
  totalHeight: number;
  shouldScroll: boolean;
}

export interface Position {
  x: number;
  y: number;
}

// ============================================================================
// SERVICE INTERFACES
// ============================================================================

/**
 * Pure business logic service for beat frame layout calculations
 */
export interface IBeatFrameService {
  // Layout calculation methods (pure functions)
  calculateBeatPosition(
    index: number,
    beatCount?: number,
    config?: BeatFrameConfig
  ): Position;
  calculateStartPosition(beatCount: number, config?: BeatFrameConfig): Position;
  calculateFrameDimensions(
    beatCount: number,
    config?: BeatFrameConfig
  ): { width: number; height: number };
  calculateLayoutInfo(
    beatCount: number,
    config?: BeatFrameConfig,
    containerDimensions?: ContainerDimensions
  ): LayoutInfo;

  // Layout optimization methods
  autoAdjustLayout(beatCount: number): [number, number]; // [rows, columns]
  calculateCellSize(
    beatCount: number,
    containerWidth: number,
    containerHeight: number,
    rows: number,
    totalCols: number,
    gap: number
  ): number;
  calculateOptimalCellSize(
    beatCount: number,
    rows: number,
    totalCols: number,
    containerDimensions?: ContainerDimensions
  ): number;

  // Beat interaction helpers
  getBeatAtPosition(
    x: number,
    y: number,
    beatCount: number,
    config?: BeatFrameConfig
  ): number;
  isBeatVisible(beat: BeatData): boolean;
  getBeatDisplayText(beat: BeatData): string;

  // Configuration helpers
  getDefaultConfig(): BeatFrameConfig;
  validateConfig(config: Partial<BeatFrameConfig>): BeatFrameConfig;
}

/**
 * Configuration service for beat frame settings
 */
export interface IBeatFrameConfigService {
  getConfig(): BeatFrameConfig;
  updateConfig(updates: Partial<BeatFrameConfig>): BeatFrameConfig;
  resetToDefaults(): BeatFrameConfig;

  // Container dimension management
  getContainerDimensions(): ContainerDimensions;
  updateContainerDimensions(
    dimensions: Partial<ContainerDimensions>
  ): ContainerDimensions;
}

/**
 * State management service for beat frame interactions
 */
export interface IBeatFrameStateService {
  // Hover state
  getHoveredBeatIndex(): number;
  setHoveredBeatIndex(index: number): void;
  clearHover(): void;

  // Drag state
  getDraggedBeatIndex(): number;
  setDraggedBeatIndex(index: number): void;
  clearDrag(): void;

  // Selection helpers
  isHovered(index: number): boolean;
  isDragged(index: number): boolean;
}
