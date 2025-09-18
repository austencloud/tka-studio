/**
 * Reversal Detection Service Implementation
 *
 * Detects reversals between beats in sequences based on prop rotation direction changes.
 * Ported from desktop app's ReversalDetector logic.
 */

import type { BeatData, SequenceData } from "$shared";
import { MotionColor } from "$shared";
import { injectable } from "inversify";
import { createBeatData } from "../../domain/factories/createBeatData";
import type { IReversalDetectionService } from "../contracts/IReversalDetectionService";

@injectable()
export class ReversalDetectionService implements IReversalDetectionService {
  /**
   * Process reversals for an entire sequence
   */
  processReversals(sequence: SequenceData): SequenceData {
    console.log("🔄 ReversalDetectionService: Processing reversals for sequence", sequence.name, "with", sequence.beats.length, "beats");
    const processedBeats: BeatData[] = [];

    for (let i = 0; i < sequence.beats.length; i++) {
      const currentBeat = sequence.beats[i];
      const previousBeats = sequence.beats.slice(0, i);



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
    
    return {
      ...sequence,
      beats: processedBeats
    };
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
   * Detect reversal for an option preview based on current sequence
   * This is used to show reversal indicators on options before they're selected
   */
  detectReversalForOption(
    currentSequence: BeatData[],
    optionPictographData: PictographData
  ): { blueReversal: boolean; redReversal: boolean } {
    const reversalInfo = { blueReversal: false, redReversal: false };

    if (!optionPictographData || !optionPictographData.motions) {
      return reversalInfo;
    }

    // If sequence is empty, no reversals possible
    if (currentSequence.length === 0) {
      return reversalInfo;
    }

    // Get the last valid prop rotation directions from the current sequence
    const lastBluePropRotDir = this._getLastValidPropRotDirFromSequence(currentSequence, "blue");
    const lastRedPropRotDir = this._getLastValidPropRotDirFromSequence(currentSequence, "red");

    // Get the prop rotation directions from the option's motion data
    const optionBluePropRotDir = this._getPropRotDirFromPictographData(optionPictographData, "blue");
    const optionRedPropRotDir = this._getPropRotDirFromPictographData(optionPictographData, "red");

    // Check for reversals
    if (this._isReversal(lastBluePropRotDir, optionBluePropRotDir)) {
      reversalInfo.blueReversal = true;
    }

    if (this._isReversal(lastRedPropRotDir, optionRedPropRotDir)) {
      reversalInfo.redReversal = true;
    }

    return reversalInfo;
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

  /**
   * Get the last valid prop rotation direction from a sequence of beats
   */
  private _getLastValidPropRotDirFromSequence(beats: BeatData[], color: "blue" | "red"): string | null {
    // Iterate backwards through the beats to find the last valid rotation direction
    for (let i = beats.length - 1; i >= 0; i--) {
      const beat = beats[i];
      if (beat.pictographData && !beat.isBlank) {
        const propRotDir = this._getPropRotDir(beat, color);
        if (propRotDir && propRotDir !== "noRotation") {
          return propRotDir;
        }
      }
    }
    return null;
  }

  /**
   * Get prop rotation direction from PictographData (for option previews)
   */
  private _getPropRotDirFromPictographData(pictographData: PictographData, color: "blue" | "red"): string | null {
    const motionData = pictographData.motions?.[color];
    if (!motionData) {
      return null;
    }

    // Use rotationDirection property from the motion data
    const rotationDirection = motionData.rotationDirection;
    return rotationDirection || null;
  }
}
