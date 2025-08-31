/**
 * Beat Grid Service Interfaces
 *
 * Service contracts for handling grid drawing and grid mode operations.
 * Consolidates grid-related logic that was duplicated across
 * BeatRenderingService, GridOverlayService, and other services.
 */
import type { GridMode } from "$domain";

// ============================================================================
// DATA CONTRACTS (Domain Models)
// ============================================================================

export interface GridDrawOptions {
  size: number;
  lineWidth?: number;
  strokeStyle?: string;
  opacity?: number;
  padding?: number;
}

export interface CombinedGridOptions {
  primaryGridMode: GridMode;
  overlayGridMode?: GridMode;
  primaryOpacity?: number;
  overlayOpacity?: number;
  primaryColor?: string;
  overlayColor?: string;
}

export interface GridValidationResult {
  isValid: boolean;
  errors: string[];
  warnings: string[];
}
