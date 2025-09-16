/**
 * Reversal Detection Service Implementation
 *
 * Detects reversals between beats in sequences based on prop rotation direction changes.
 * Ported from desktop app's ReversalDetector logic.
 */

import type { BeatData, SequenceData } from "$shared";
import { MotionColor, RotationDirection } from "$shared";
import { injectable } from "inversify";
import { createBeatData } from "../../../shared/domain/factories/createBeatData";
import type { IReversalDetectionService } from "../contracts/image-export-rendering-interfaces";

@injectable()
export class ReversalDetectionService implements IReversalDetectionService {
  /**
   * Process reversals for an entire sequence
   */
  processReversals(sequence: SequenceData, beats: BeatData[]): BeatData[] {
    console.log("🔄 ReversalDetectionService: Processing reversals for sequence", sequence.name, "with", beats.length, "beats");
    const processedBeats: BeatData[] = [];

    for (let i = 0; i < beats.length; i++) {
      const currentBeat = beats[i];
      const previousBeats = beats.slice(0, i);

      console.log(`🔍 ReversalDetectionService: Processing beat ${i + 1}:`, {
        letter: currentBeat.pictographData?.letter,
        isBlank: currentBeat.isBlank,
        hasPictographData: !!currentBeat.pictographData,
        fullPictographData: currentBeat.pictographData
      });

      // Detect reversals for this beat
      const reversalInfo = this.detectReversal(previousBeats, currentBeat);

      console.log(`🎯 ReversalDetectionService: Beat ${i + 1} reversal info:`, reversalInfo);

      // Apply reversal symbols to the beat
      const processedBeat = this.applyReversalSymbols(currentBeat, reversalInfo);

      console.log(`📊 ReversalDetectionService: Final beat ${i + 1} data:`, {
        blueReversal: processedBeat.blueReversal,
        redReversal: processedBeat.redReversal,
        letter: processedBeat.pictographData?.letter
      });

      processedBeats.push(processedBeat);
    }

    console.log("✅ ReversalDetectionService: Completed processing", processedBeats.length, "beats");
    return processedBeats;
  }

  /**
   * Detect reversal for a single beat based on previous beats
   */
  detectReversal(
    previousBeats: BeatData[],
    currentBeat: BeatData
  ): { blueReversal: boolean; redReversal: boolean } {
    const reversalInfo = { blueReversal: false, redReversal: false };

    if (!currentBeat.pictographData || currentBeat.isBlank) {
      console.log("⚠️ ReversalDetectionService: Skipping beat - no pictograph data or is blank");
      return reversalInfo;
    }

    // Check blue motion reversal
    const lastBluePropRotDir = this._getLastValidPropRotDir(previousBeats, "blue");
    const currentBluePropRotDir = this._getPropRotDir(currentBeat, "blue");

    console.log("🔵 Blue prop rotation:", {
      last: lastBluePropRotDir,
      current: currentBluePropRotDir,
      isReversal: this._isReversal(lastBluePropRotDir, currentBluePropRotDir)
    });

    if (this._isReversal(lastBluePropRotDir, currentBluePropRotDir)) {
      reversalInfo.blueReversal = true;
    }

    // Check red motion reversal
    const lastRedPropRotDir = this._getLastValidPropRotDir(previousBeats, "red");
    const currentRedPropRotDir = this._getPropRotDir(currentBeat, "red");

    console.log("🔴 Red prop rotation:", {
      last: lastRedPropRotDir,
      current: currentRedPropRotDir,
      isReversal: this._isReversal(lastRedPropRotDir, currentRedPropRotDir)
    });

    if (this._isReversal(lastRedPropRotDir, currentRedPropRotDir)) {
      reversalInfo.redReversal = true;
    }

    return reversalInfo;
  }

  /**
   * Apply reversal symbols to a beat
   */
  applyReversalSymbols(
    beatData: BeatData,
    reversalInfo: { blueReversal: boolean; redReversal: boolean }
  ): BeatData {
    return createBeatData({
      ...beatData,
      blueReversal: reversalInfo.blueReversal,
      redReversal: reversalInfo.redReversal,
    });
  }

  /**
   * Get the last valid prop rotation direction for a color from previous beats
   */
  private _getLastValidPropRotDir(beats: BeatData[], color: "blue" | "red"): string | null {
    for (let i = beats.length - 1; i >= 0; i--) {
      const beat = beats[i];
      const propRotDir = this._getPropRotDir(beat, color);

      if (propRotDir && propRotDir !== "noRotation") {
        return propRotDir;
      }
    }
    return null;
  }

  /**
   * Get prop rotation direction for a specific color from a beat
   */
  private _getPropRotDir(beat: BeatData, color: "blue" | "red"): string | null {
    if (!beat.pictographData || beat.isBlank) {
      return null;
    }

    // Use current data structure: motions[MotionColor]
    const motionColor = color === "blue" ? MotionColor.BLUE : MotionColor.RED;
    const motionData = beat.pictographData.motions?.[motionColor];

    if (!motionData) {
      console.log(`⚠️ ReversalDetectionService: No motion data found for ${color} motion`);
      return null;
    }

    // Use rotationDirection property (current structure) instead of propRotDir (legacy)
    const rotationDirection = motionData.rotationDirection;

    console.log(`🔍 ReversalDetectionService: ${color} motion rotation direction:`, rotationDirection);

    return rotationDirection || null;
  }

  /**
   * Check if there's a reversal between two prop rotation directions
   */
  private _isReversal(lastPropRotDir: string | null, currentPropRotDir: string | null): boolean {
    // If either is null or noRotation, no reversal
    if (!lastPropRotDir || !currentPropRotDir ||
        lastPropRotDir === "noRotation" || currentPropRotDir === "noRotation") {
      return false;
    }

    // If directions are different, it's a reversal
    return lastPropRotDir !== currentPropRotDir;
  }
}
