/**
 * Filename Generator Service
 *
 * Handles filename generation for TKA image exports.
 * Extracted from the monolithic TKAImageExportService to focus solely on filename concerns.
 */

import type { SequenceData } from "$shared/domain";
import { injectable } from "inversify";
import type { SequenceExportOptions } from "../../domain/models";
import type { IFilenameGeneratorService } from "../contracts";

@injectable()
export class FilenameGeneratorService implements IFilenameGeneratorService {
  /**
   * Generate default filename for export
   */
  generateDefaultFilename(
    sequence: SequenceData,
    options: Partial<SequenceExportOptions>
  ): string {
    const word = sequence.word || "sequence";
    const format = options.format || "PNG";

    return this.generateVersionedFilename(word, format);
  }

  /**
   * Generate versioned filename to avoid conflicts
   */
  generateVersionedFilename(word: string, format: string): string {
    const sanitizedWord = this.sanitizeFilename(word);
    const timestamp = new Date()
      .toISOString()
      .slice(0, 19)
      .replace(/[:T]/g, "-");
    const extension = format.toLowerCase();

    return `${sanitizedWord}-${timestamp}.${extension}`;
  }

  /**
   * Sanitize filename to be filesystem safe
   */
  sanitizeFilename(filename: string): string {
    return filename
      .replace(/[^a-zA-Z0-9\-_\s]/g, "") // Remove invalid characters
      .replace(/\s+/g, "-") // Replace spaces with hyphens
      .replace(/-+/g, "-") // Replace multiple hyphens with single
      .replace(/^-|-$/g, "") // Remove leading/trailing hyphens
      .substring(0, 50) // Limit length
      .toLowerCase();
  }
}
