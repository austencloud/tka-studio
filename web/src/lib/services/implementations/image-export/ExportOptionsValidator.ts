/**
 * Export Options Validator
 *
 * Handles validation of export options and sequence data for TKA image exports.
 * Extracted from the monolithic TKAImageExportService to focus solely on validation concerns.
 */

import type { SequenceData } from "$domain";
import { inject, injectable } from "inversify";
import type {
  ExportValidationResult,
  IExportMemoryCalculator,
  IExportOptionsValidator,
  TKAImageExportOptions,
} from "../../contracts/image-export-interfaces";
import { TYPES } from "../../inversify/types";

@injectable()
export class ExportOptionsValidator implements IExportOptionsValidator {
  constructor(
    @inject(TYPES.IExportMemoryCalculator)
    private memoryCalculator: IExportMemoryCalculator
  ) {}

  /**
   * Validate export parameters
   */
  validateExport(
    sequence: SequenceData,
    options: TKAImageExportOptions
  ): ExportValidationResult {
    const errors: string[] = [];

    // Validate sequence
    const sequenceValidation = this.validateSequence(sequence);
    errors.push(...sequenceValidation.errors);

    // Validate options
    const optionsValidation = this.validateOptions(options);
    errors.push(...optionsValidation.errors);

    // Memory estimation validation
    if (sequenceValidation.valid && optionsValidation.valid) {
      if (!this.memoryCalculator.isWithinMemoryLimits(sequence, options)) {
        const memoryEstimate = this.memoryCalculator.estimateMemoryUsage(
          sequence,
          options
        );
        errors.push(
          `Image would require ${Math.round(memoryEstimate.estimatedMB)}MB memory (limit: 200MB)`
        );
      }
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  /**
   * Validate just the options (without sequence)
   */
  validateOptions(options: TKAImageExportOptions): ExportValidationResult {
    const errors: string[] = [];

    // Validate beat scale
    if (options.beatScale <= 0 || options.beatScale > 5) {
      errors.push("Beat scale must be between 0.1 and 5.0");
    }

    // Validate beat size
    if (options.beatSize < 50 || options.beatSize > 500) {
      errors.push("Beat size must be between 50 and 500 pixels");
    }

    // Validate margin
    if (options.margin < 0 || options.margin > 200) {
      errors.push("Margin must be between 0 and 200 pixels");
    }

    // Validate quality for JPEG
    if (options.format === "JPEG") {
      if (options.quality < 0.1 || options.quality > 1.0) {
        errors.push("JPEG quality must be between 0.1 and 1.0");
      }
    }

    // Validate format
    if (!["PNG", "JPEG"].includes(options.format)) {
      errors.push("Format must be PNG or JPEG");
    }

    // Validate user info
    if (options.addUserInfo) {
      if (!options.userName || options.userName.trim().length === 0) {
        errors.push("User name is required when adding user info");
      }
      if (options.userName && options.userName.length > 50) {
        errors.push("User name must be 50 characters or less");
      }
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  /**
   * Validate just the sequence data
   */
  validateSequence(sequence: SequenceData): ExportValidationResult {
    const errors: string[] = [];

    if (!sequence) {
      errors.push("Sequence data is required");
      return { valid: false, errors };
    }

    if (!sequence.beats) {
      errors.push("Sequence must have beats array");
    } else if (sequence.beats.length === 0) {
      errors.push("Sequence must have at least one beat");
    } else if (sequence.beats.length > 100) {
      errors.push("Sequence cannot have more than 100 beats");
    }

    if (!sequence.word || sequence.word.trim().length === 0) {
      errors.push("Sequence must have a word");
    }

    if (sequence.word && sequence.word.length > 20) {
      errors.push("Sequence word must be 20 characters or less");
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }
}
