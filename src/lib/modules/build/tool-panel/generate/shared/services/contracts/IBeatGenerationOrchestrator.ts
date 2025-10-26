/**
 * Beat Generation Orchestrator Interface
 *
 * Orchestrates the generation of multiple beats for a sequence.
 */
import type { BeatData, GridMode } from "$shared";
import { PropContinuity } from "../../domain/models/generate-models";
import type { TurnAllocation } from "./ITurnAllocator";

export interface BeatGenerationOptions {
  level: number;
  turnAllocation: TurnAllocation;
  propContinuity: PropContinuity;
  blueRotationDirection: string;
  redRotationDirection: string;
  letterTypes: string[];
  gridMode: GridMode;
}

export interface IBeatGenerationOrchestrator {
  /**
   * Generate multiple beats for a sequence
   * @param sequence - Current sequence (start position + any existing beats)
   * @param count - Number of beats to generate
   * @param options - Generation options
   * @returns Promise resolving to array of generated beats
   */
  generateBeats(
    sequence: BeatData[],
    count: number,
    options: BeatGenerationOptions
  ): Promise<BeatData[]>;

  /**
   * Generate a single next beat
   * @param sequence - Current sequence
   * @param options - Generation options
   * @param turnBlue - Blue turn value for this beat
   * @param turnRed - Red turn value for this beat
   * @returns Promise resolving to the next beat
   */
  generateNextBeat(
    sequence: BeatData[],
    options: BeatGenerationOptions,
    turnBlue: number | "fl",
    turnRed: number | "fl"
  ): Promise<BeatData>;
}
