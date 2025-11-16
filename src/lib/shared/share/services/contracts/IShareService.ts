/**
 * Share Service Contract
 *
 * Simple, focused interface for sharing/downloading sequences.
 * Replaces the over-engineered export module.
 */

import type { SequenceData } from "$shared";
import type { ShareOptions } from "../../domain";

export interface IShareService {
  /**
   * Generate a preview image for the share interface
   * Returns data URL for immediate display
   */
  generatePreview(
    sequence: SequenceData,
    options: ShareOptions
  ): Promise<string>;

  /**
   * Download sequence as image file
   * Simple download functionality - the core feature users need
   */
  downloadImage(
    sequence: SequenceData,
    options: ShareOptions,
    filename?: string
  ): Promise<void>;

  /**
   * Get image as blob for future sharing features
   * Prepares for social media integration
   */
  getImageBlob(sequence: SequenceData, options: ShareOptions): Promise<Blob>;

  /**
   * Generate appropriate filename for the sequence
   */
  generateFilename(sequence: SequenceData, options: ShareOptions): string;

  /**
   * Validate share options
   */
  validateOptions(options: ShareOptions): { valid: boolean; errors: string[] };

  /**
   * Share sequence via device's native share functionality
   * Handles Web Share API with file sharing and fallbacks
   */
  shareViaDevice(sequence: SequenceData, options: ShareOptions): Promise<void>;
}
