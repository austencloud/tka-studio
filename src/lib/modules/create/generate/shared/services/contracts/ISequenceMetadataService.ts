import type { BeatData } from "$shared";
import type { GenerationOptions } from "../../domain/models/generate-models";

export interface ISequenceMetadataService {
  generateSequenceName(options: GenerationOptions): string;
  calculateWordFromBeats(beats: BeatData[]): string;
  mapDifficultyToLevel(difficulty: any): number;
  createGenerationMetadata(options: {
    beatsGenerated: number;
    propContinuity: string;
    blueRotationDirection: string;
    redRotationDirection: string;
    turnIntensity: number;
    level: number;
  }): Record<string, any>;
}
