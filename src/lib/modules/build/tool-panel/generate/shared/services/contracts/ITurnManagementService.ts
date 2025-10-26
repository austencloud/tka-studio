import type { BeatData } from "$shared";

export interface ITurnManagementService {
  setTurns(beat: BeatData, turnBlue: number | "fl", turnRed: number | "fl"): void;
  updateDashStaticRotationDirections(
    beat: BeatData,
    propContinuity: string,
    blueRotationDirection: string,
    redRotationDirection: string
  ): void;
  getRandomRotationDirection(): string;
}

