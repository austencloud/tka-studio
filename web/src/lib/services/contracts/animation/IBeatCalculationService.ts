/**
 * Beat Calculation Service Interface
 *
 * Interface for beat calculation and timing services.
 * Handles beat state calculations and validation.
 */

import type { BeatData } from "$domain";

export interface IBeatCalculationService {
  calculateBeatState(
    currentBeat: number,
    beats: readonly BeatData[],
    totalBeats: number
  ): BeatCalculationResult;
  validateBeats(beats: readonly BeatData[]): boolean;
  getBeatSafely(beats: readonly BeatData[], index: number): BeatData | null;
  calculateTotalDuration(beats: readonly BeatData[]): number;
  findBeatByNumber(
    beats: readonly BeatData[],
    beatNumber: number
  ): BeatData | null;
}

export interface BeatCalculationResult {
  currentBeatIndex: number;
  beatProgress: number;
  currentBeatData: BeatData;
  isValid: boolean;
}
