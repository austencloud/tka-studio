/**
 * Export Types
 *
 * This module provides shared types and interfaces for the enhanced image export functionality.
 */

import type { Beat } from '$lib/types/Beat';

/**
 * Options for enhanced image export
 */
export interface EnhancedExportOptions {
  // Content options
  beats: Beat[];
  startPosition?: Beat | null;

  // Layout options
  columns?: number;
  spacing?: number;
  includeStartPosition?: boolean;

  // Visual options
  backgroundColor?: string;
  scale?: number;
  quality?: number;
  format?: 'png' | 'jpeg';

  // Content flags
  addWord?: boolean;
  addUserInfo?: boolean;
  addDifficultyLevel?: boolean;
  addBeatNumbers?: boolean;
  addReversalSymbols?: boolean;

  // Content values
  title?: string;
  userName?: string;
  notes?: string;
  exportDate?: string;
  difficultyLevel?: number;
}

/**
 * Result of exporting an image
 */
export interface EnhancedExportResult {
  dataUrl: string;
  width: number;
  height: number;
  format: string;
}

/**
 * Canvas dimensions information
 */
export interface CanvasDimensions {
  width: number;
  height: number;
  topMargin: number;
  bottomMargin: number;
  beatSize: number;
  rows: number;
  columns: number; // Total columns including start position column if present
  columnsForBeats: number; // Columns available for regular beats
}

/**
 * Required options with defaults applied
 */
export type RequiredExportOptions = Required<Omit<EnhancedExportOptions, 'beats' | 'startPosition'>> & {
  beats: Beat[];
  startPosition: Beat | null;
};
