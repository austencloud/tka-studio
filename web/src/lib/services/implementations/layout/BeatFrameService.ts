/**
 * Pure Beat Frame Service Implementation
 *
 * Extracted business logic from BeatFrameService.svelte.ts
 * Contains only pure functions with no reactive state.
 */

import type { BeatData } from "$domain";
import { GridMode } from "$domain";
import type {
  BeatFrameConfig,
  ContainerDimensions,
  LayoutInfo,
  Position,
} from "$domain/build/workbench/beat-frame";
import type { IBeatFrameService } from "$lib/services/contracts/beat-frame-interfaces";
import { injectable } from "inversify";

@injectable()
export class BeatFrameService implements IBeatFrameService {
  // ============================================================================
  // CONFIGURATION METHODS
  // ============================================================================

  getDefaultConfig(): BeatFrameConfig {
    return {
      columns: 4,
      beatSize: 160,
      gap: 0,
      gridMode: GridMode.DIAMOND,
      hasStartTile: true,
    };
  }

  validateConfig(config: Partial<BeatFrameConfig>): BeatFrameConfig {
    const defaults = this.getDefaultConfig();
    return {
      columns: Math.max(1, config.columns ?? defaults.columns),
      beatSize: Math.max(50, config.beatSize ?? defaults.beatSize),
      gap: Math.max(0, config.gap ?? defaults.gap),
      gridMode: config.gridMode ?? defaults.gridMode,
      hasStartTile: config.hasStartTile ?? defaults.hasStartTile,
    };
  }

  // ============================================================================
  // LAYOUT CALCULATION METHODS
  // ============================================================================

  calculateBeatPosition(
    index: number,
    beatCount?: number,
    config?: BeatFrameConfig
  ): Position {
    const effectiveConfig = config ?? this.getDefaultConfig();

    // Use the optimal layout for this beat count
    const [, cols] = this.autoAdjustLayout(beatCount ?? index + 1);
    const columnsForBeats = Math.max(1, cols);
    const row = Math.floor(index / columnsForBeats);
    const col =
      (index % columnsForBeats) + (effectiveConfig.hasStartTile ? 1 : 0);

    const step = effectiveConfig.beatSize + effectiveConfig.gap;
    return { x: col * step, y: row * step };
  }

  calculateStartPosition(
    beatCount: number,
    config?: BeatFrameConfig
  ): Position {
    const effectiveConfig = config ?? this.getDefaultConfig();

    if (!effectiveConfig.hasStartTile) {
      return { x: 0, y: 0 };
    }

    // Start position is always at [0,0] when enabled
    return { x: 0, y: 0 };
  }

  calculateFrameDimensions(
    beatCount: number,
    config?: BeatFrameConfig
  ): { width: number; height: number } {
    const effectiveConfig = config ?? this.getDefaultConfig();
    const step = effectiveConfig.beatSize + effectiveConfig.gap;

    // If no beats, size to just the Start tile (desktop shows START only)
    if (beatCount <= 0) {
      const width = effectiveConfig.hasStartTile ? effectiveConfig.beatSize : 0;
      const height = effectiveConfig.beatSize;
      return { width, height };
    }

    const [rows, cols] = this.autoAdjustLayout(beatCount);
    const totalCols = cols + (effectiveConfig.hasStartTile ? 1 : 0);

    return {
      width: totalCols * step - effectiveConfig.gap,
      height: rows * step - effectiveConfig.gap,
    };
  }

  calculateLayoutInfo(
    beatCount: number,
    config?: BeatFrameConfig,
    containerDimensions?: ContainerDimensions
  ): LayoutInfo {
    const effectiveConfig = config ?? this.getDefaultConfig();
    const effectiveContainer = containerDimensions ?? {
      width: 0,
      height: 0,
      isFullscreen: false,
    };

    // Get optimal layout without mutating state
    const [rows, cols] = this.autoAdjustLayout(beatCount);
    const totalCols = cols + (effectiveConfig.hasStartTile ? 1 : 0);

    // Calculate optimal cell size without mutating state
    const optimalCellSize = this.calculateOptimalCellSize(
      beatCount,
      rows,
      totalCols,
      effectiveContainer
    );

    const step = optimalCellSize + effectiveConfig.gap;
    const totalWidth = totalCols * step - effectiveConfig.gap;
    const totalHeight = rows * step - effectiveConfig.gap;

    // Check if content would overflow container
    const containerWidth = effectiveContainer.width;
    const containerHeight = effectiveContainer.height;

    const shouldScroll =
      (containerWidth > 0 && totalWidth > containerWidth) ||
      (containerHeight > 0 && totalHeight > containerHeight) ||
      optimalCellSize <= (effectiveContainer.isFullscreen ? 140 : 120) * 1.1;

    return {
      rows,
      columns: cols,
      cellSize: optimalCellSize,
      totalWidth,
      totalHeight,
      shouldScroll,
    };
  }

  // ============================================================================
  // LAYOUT OPTIMIZATION METHODS
  // ============================================================================

  autoAdjustLayout(beatCount: number): [number, number] {
    if (beatCount <= 0) return [1, 1];
    if (beatCount <= 4) return [1, beatCount];
    if (beatCount <= 8) return [2, 4];
    if (beatCount <= 12) return [3, 4];
    if (beatCount <= 16) return [4, 4];
    if (beatCount <= 20) return [4, 5];
    if (beatCount <= 24) return [4, 6];
    if (beatCount <= 28) return [4, 7];
    if (beatCount <= 32) return [4, 8];

    // For larger sequences, use dynamic calculation
    const cols = Math.ceil(Math.sqrt(beatCount));
    const rows = Math.ceil(beatCount / cols);
    return [rows, cols];
  }

  calculateCellSize(
    beatCount: number,
    containerWidth: number,
    containerHeight: number,
    rows: number,
    totalCols: number,
    gap: number
  ): number {
    if (containerWidth <= 0 || containerHeight <= 0) {
      return 160; // Default fallback
    }

    // Calculate maximum cell size that fits in container
    const maxCellWidth = (containerWidth - gap * (totalCols - 1)) / totalCols;
    const maxCellHeight = (containerHeight - gap * (rows - 1)) / rows;
    const maxCellSize = Math.min(maxCellWidth, maxCellHeight);

    // Apply minimum size constraints
    const minSize = 50;
    const maxSize = 300;

    return Math.max(minSize, Math.min(maxSize, Math.floor(maxCellSize)));
  }

  calculateOptimalCellSize(
    beatCount: number,
    rows: number,
    totalCols: number,
    containerDimensions?: ContainerDimensions
  ): number {
    const effectiveContainer = containerDimensions ?? {
      width: 0,
      height: 0,
      isFullscreen: false,
    };

    if (effectiveContainer.width <= 0 || effectiveContainer.height <= 0) {
      return 160; // Default fallback
    }

    return this.calculateCellSize(
      beatCount,
      effectiveContainer.width,
      effectiveContainer.height,
      rows,
      totalCols,
      0 // gap is handled in the config
    );
  }

  // ============================================================================
  // BEAT INTERACTION HELPERS
  // ============================================================================

  getBeatAtPosition(
    x: number,
    y: number,
    beatCount: number,
    config?: BeatFrameConfig
  ): number {
    const effectiveConfig = config ?? this.getDefaultConfig();
    const step = effectiveConfig.beatSize + effectiveConfig.gap;
    const colRaw = Math.floor(x / step);
    const row = Math.floor(y / step);

    // Ignore clicks on the Start tile column
    const startOffset = effectiveConfig.hasStartTile ? 1 : 0;
    if (colRaw < startOffset) return -1;

    const col = colRaw - startOffset;
    const index = row * Math.max(1, effectiveConfig.columns) + col;
    return index >= 0 && index < beatCount ? index : -1;
  }

  isBeatVisible(beat: BeatData): boolean {
    return !beat.isBlank || beat.pictographData != null;
  }

  getBeatDisplayText(beat: BeatData): string {
    if (beat.isBlank && !beat.pictographData) {
      // fallback: show beat number if available on metadata or domain type
      return beat.beatNumber.toString();
    }
    return beat.pictographData?.letter?.toString() || "";
  }
}
