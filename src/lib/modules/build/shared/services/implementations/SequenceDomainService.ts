/**
 * Sequence Domain Service - REAL Business Logic from Desktop
 *
 * Ported from desktop.modern.application.services.sequence.beat_sequence_service
 * and desktop.modern.domain.models for actual validation and business rules.
 */

import type { BeatData, SequenceData, ValidationErrorInfo, ValidationResult } from "$shared";
import { GridMode } from "$shared";
// Domain types
// import type { SequenceCreateRequest } from "$shared";

// Behavioral contracts
import { injectable } from "inversify";
// import type { ISequenceDomainService } from "../contracts";

@injectable()
export class SequenceDomainService {

  validateSequence(sequence: any): boolean {
    // TODO: Implement sequence validation
    return true;
  }

  transformSequence(sequence: any): any {
    // TODO: Implement sequence transformation
    return sequence;
  }

  // Duplicate methods removed - using the detailed implementations below

  /**
   * Validate sequence creation request - REAL validation from desktop
   */
  validateCreateRequest(request: any): ValidationResult {
    const errors: ValidationErrorInfo[] = [];

    // Validation from desktop SequenceData.__post_init__
    if (!request.name || request.name.trim().length === 0) {
      errors.push({
        code: "MISSING_NAME",
        message: "Sequence name is required",
        field: "name",
        severity: "error",
      });
    }

    if (request.name && request.name.length > 100) {
      errors.push({
        code: "NAME_TOO_LONG",
        message: "Sequence name must be less than 100 characters",
        field: "name",
        severity: "error",
      });
    }

    // Length validation from desktop domain models
    // Allow 0 length for progressive creation (start position only)
    if (
      request.length !== undefined &&
      (request.length < 0 || request.length > 64)
    ) {
      errors.push({
        code: "INVALID_LENGTH",
        message: "Sequence length must be between 0 and 64",
        field: "length",
        severity: "error",
      });
    }

    // Grid mode validation from desktop enums
    if (
      request.gridMode &&
      ![GridMode.DIAMOND, GridMode.BOX].includes(request.gridMode)
    ) {
      errors.push({
        code: "INVALID_GRID_MODE",
        message: "Grid mode must be either GridMode.DIAMOND or GridMode.BOX",
        field: "gridMode",
        severity: "error",
      });
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings: [],
    };
  }

  /**
   * Create sequence with proper beat numbering - from desktop SequenceData
   */
  createSequence(request: any): SequenceData {
    const validation = this.validateCreateRequest(request);
    if (!validation.isValid) {
      throw new Error(
        `Invalid sequence request: ${validation.errors.join(", ")}`
      );
    }

    // Create beats with proper numbering (desktop logic)
    const beats: BeatData[] = [];
    const length = request.length || 0;
    for (let i = 1; i <= length; i++) {
      beats.push(this.createEmptyBeat(i));
    }

    // Create sequence following desktop SequenceData structure
    const sequence: SequenceData = {
      id: this.generateId(),
      name: request.name.trim(),
      word: "",
      beats,
      thumbnails: [],
      isFavorite: false,
      isCircular: false,
      tags: [],
      metadata: { length: request.length },
    };

    return sequence;
  }

  /**
   * Update beat with proper validation - from desktop BeatSequenceService
   */
  updateBeat(
    sequence: SequenceData,
    beatIndex: number,
    beatData: BeatData
  ): SequenceData {
    // Validation from desktop BeatSequenceService
    if (beatIndex < 0 || beatIndex >= sequence.beats.length) {
      throw new Error(`Invalid beat index: ${beatIndex}`);
    }

    // Validate beat data
    if (beatData.duration && beatData.duration < 0) {
      throw new Error("Beat duration must be positive");
    }

    // Legacy field guard (beatNumber) for migrated data
    if (
      typeof (beatData as unknown as { beatNumber?: number }).beatNumber ===
      "number"
    ) {
      if ((beatData as unknown as { beatNumber: number }).beatNumber < 0) {
        throw new Error("Beat number must be non-negative");
      }
    }

    // Create new beats array with updated beat
    const newBeats = [...sequence.beats];
    newBeats[beatIndex] = { ...beatData };

    return { ...sequence, beats: newBeats } as SequenceData;
  }

  /**
   * Calculate sequence word - from desktop SequenceWordCalculator
   */
  calculateSequenceWord(sequence: SequenceData): string {
    if (!sequence.beats || sequence.beats.length === 0) {
      return "";
    }

    // Extract letters from beats (desktop logic)
    const word = sequence.beats
      .map((beat: any) => beat?.letter)
      .join("");

    // Apply word simplification for circular sequences (desktop logic)
    return this.simplifyRepeatedWord(word);
  }

  /**
   * Simplify repeated patterns - from desktop WordSimplifier
   */
  private simplifyRepeatedWord(word: string): string {
    if (!word) return word;

    const canFormByRepeating = (s: string, pattern: string): boolean => {
      const patternLen = pattern.length;
      for (let i = 0; i < s.length; i += patternLen) {
        if (s.slice(i, i + patternLen) !== pattern) {
          return false;
        }
      }
      return true;
    };

    const n = word.length;

    // Try each possible pattern length from smallest to largest
    for (let i = 1; i <= Math.floor(n / 2); i++) {
      const pattern = word.slice(0, i);
      if (n % i === 0 && canFormByRepeating(word, pattern)) {
        return pattern;
      }
    }

    return word;
  }

  /**
   * Create empty beat - from desktop BeatData structure
   */
  private createEmptyBeat(beatNumber: number): BeatData {
    return {
      id: crypto.randomUUID(),
      beatNumber: beatNumber,
      duration: 1.0,
      blueReversal: false,
      redReversal: false,
      isBlank: true,
      // PictographData properties (since BeatData extends PictographData)
      letter: null,
      startPosition: null,
      endPosition: null,
      motions: {},
    };
  }

  /**
   * Generate unique ID - following desktop pattern
   */
  private generateId(): string {
    return `seq_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }
}
