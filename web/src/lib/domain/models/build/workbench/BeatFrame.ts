/**
 * Beat Frame Service Interfaces
 *
 * Pure TypeScript interfaces for beat frame layout and positioning services.
 * Extracted from BeatFrameService.svelte.ts to enable clean architecture.
 */
// ============================================================================
// CONFIGURATION TYPES
// ============================================================================
import { GridMode } from "$domain";

// ============================================================================
// DATA CONTRACTS (Domain Models)
// ============================================================================

export interface BeatFrameConfig {
  /** Number of columns allocated for BEATS (excludes the Start tile column) */
  columns: number;
  beatSize: number;
  gap: number;
  gridMode: GridMode;
  cellSize: number;
  showBeatNumbers: boolean;
  /** Whether to reserve the first column for the Start Position tile */
  hasStartTile: boolean;
  enableHover: boolean;
  enableDrag: boolean;
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

