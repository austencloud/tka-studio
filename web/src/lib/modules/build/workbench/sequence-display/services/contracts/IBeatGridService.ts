/**
 * Beat Grid Service Contracts
 * 
 * Defines interfaces for beat grid layout and interaction services.
 */

import type {
  BeatData,
  BeatGridConfig,
  ContainerDimensions,
  LayoutInfo,
} from "$shared";
import type { ImageCanvasCoordinate } from "../../domain";

export interface IBeatGridService {
  // Configuration methods
  getDefaultConfig(): BeatGridConfig;
  validateConfig(config: Partial<BeatGridConfig>): BeatGridConfig;

  // Layout calculation methods
  calculateBeatPosition(
    index: number,
    beatCount?: number,
    config?: BeatGridConfig
  ): ImageCanvasCoordinate;

  calculateStartPosition(
    beatCount: number,
    config?: BeatGridConfig,
    containerDimensions?: ContainerDimensions
  ): ImageCanvasCoordinate;

  calculateFrameDimensions(
    beatCount: number,
    config?: BeatGridConfig,
    containerDimensions?: ContainerDimensions
  ): { width: number; height: number };

  calculateLayoutInfo(
    beatCount: number,
    config?: BeatGridConfig,
    containerDimensions?: ContainerDimensions
  ): LayoutInfo;

  // Layout optimization methods
  autoAdjustLayout(beatCount: number): [number, number];

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
    config?: BeatGridConfig
  ): number;

  isBeatVisible(beat: BeatData): boolean;
  getBeatDisplayText(beat: BeatData): string;
}
