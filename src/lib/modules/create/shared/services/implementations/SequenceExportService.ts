import { injectable } from "inversify";
import type {
  ISequenceExportService,
  CondensedSequenceData,
  CondensedStartPosition,
  CondensedBeatData,
  CondensedMotionData,
  CondensedStartMotion,
} from "../contracts/ISequenceExportService";

/**
 * Service for exporting sequence data in various formats
 * Pure business logic - no Svelte dependencies
 */
@injectable()
export class SequenceExportService implements ISequenceExportService {
  /**
   * Create a condensed, human-readable version of sequence data
   * Removes: IDs, placement data, metadata, redundant fields
   * Keeps: Essential motion data for reconstruction
   */
  createCondensedSequence(sequenceData: any): CondensedSequenceData {
    const condensed: CondensedSequenceData = {
      word: sequenceData.word,
      beats: [],
    };

    // Include start position FIRST if it exists
    if (sequenceData.startingPositionBeat || sequenceData.startPosition) {
      const startPos =
        sequenceData.startingPositionBeat || sequenceData.startPosition;
      condensed.startPosition = this.extractStartPosition(startPos);
    }

    // Process each beat AFTER start position
    if (sequenceData.beats && Array.isArray(sequenceData.beats)) {
      condensed.beats = sequenceData.beats.map((beat: any) =>
        this.extractBeatData(beat)
      );
    }

    return condensed;
  }

  /**
   * Extract condensed start position data
   */
  private extractStartPosition(startPos: any): CondensedStartPosition {
    return {
      letter: startPos.letter,
      gridPosition: startPos.gridPosition,
      motions: {
        blue: this.extractStartMotion(startPos.motions?.blue),
        red: this.extractStartMotion(startPos.motions?.red),
      },
    };
  }

  /**
   * Extract condensed start motion data (location and orientation only)
   */
  private extractStartMotion(motion: any): CondensedStartMotion {
    return {
      startLocation: motion?.startLocation,
      startOrientation: motion?.startOrientation,
    };
  }

  /**
   * Extract condensed beat data
   */
  private extractBeatData(beat: any): CondensedBeatData {
    return {
      letter: beat.letter,
      beatNumber: beat.beatNumber,
      gridPosition: beat.gridPosition,
      duration: beat.duration,
      blueReversal: beat.blueReversal,
      redReversal: beat.redReversal,
      motions: {
        blue: this.extractMotionData(beat.motions?.blue),
        red: this.extractMotionData(beat.motions?.red),
      },
    };
  }

  /**
   * Extract condensed motion data (essential fields only)
   */
  private extractMotionData(motion: any): CondensedMotionData {
    return {
      motionType: motion?.motionType,
      rotationDirection: motion?.rotationDirection,
      startLocation: motion?.startLocation,
      endLocation: motion?.endLocation,
      turns: motion?.turns,
      startOrientation: motion?.startOrientation,
      endOrientation: motion?.endOrientation,
    };
  }
}
