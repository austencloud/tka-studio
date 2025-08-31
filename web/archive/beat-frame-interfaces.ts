/**
 * Beat Frame Service Interfaces
 *
 * Pure TypeScript interfaces for beat frame layout and positioning services.
 * Extracted from BeatFrameService.svelte.ts to enable clean architecture.
 */
// ============================================================================
// CONFIGURATION TYPES
// ============================================================================
import type { BeatData } from "$lib/domain";
import type {
  BeatFrameConfig,
  ContainerDimensions,
  LayoutInfo,
  Position,
} from "$lib/domain/build/workbench/beat-frame";

// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

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

// ============================================================================
// RE-EXPORT DOMAIN TYPES
// ============================================================================
export type {
  BeatFrameConfig,
  ContainerDimensions,
  LayoutInfo,
  Position,
} from "$lib/domain/build/workbench/beat-frame";
