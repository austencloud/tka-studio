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

