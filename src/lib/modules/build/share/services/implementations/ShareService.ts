/**
 * Share Service Implementation
 * 
 * Simple, focused service for sharing/downloading sequences.
 * Uses the render module for image generation.
 */

import { inject, injectable } from 'inversify';
import { TYPES } from '$shared/inversify/types';
import type { SequenceData } from '$shared';
import type { ISequenceRenderService } from '$render';
import type { ShareOptions } from '../../domain';
import type { IShareService } from '../contracts';

@injectable()
export class ShareService implements IShareService {
  constructor(
    @inject(TYPES.ISequenceRenderService) 
    private renderService: ISequenceRenderService
  ) {}

  async generatePreview(sequence: SequenceData, options: ShareOptions): Promise<string> {
    // Convert ShareOptions to SequenceExportOptions for render service
    // Use much smaller scale for thumbnail preview (faster loading)
    const renderOptions = this.convertToPreviewOptions(options);

    // Use render service to generate preview
    return await this.renderService.generatePreview(sequence, renderOptions);
  }

  async downloadImage(sequence: SequenceData, options: ShareOptions, filename?: string): Promise<void> {
    // Get image blob
    const blob = await this.getImageBlob(sequence, options);
    
    // Generate filename if not provided
    const finalFilename = filename || this.generateFilename(sequence, options);
    
    // Trigger download
    this.triggerDownload(blob, finalFilename);
  }

  async getImageBlob(sequence: SequenceData, options: ShareOptions): Promise<Blob> {
    // Convert ShareOptions to SequenceExportOptions for render service
    const renderOptions = this.convertToRenderOptions(options);
    
    // Use render service to generate blob
    return await this.renderService.renderSequenceToBlob(sequence, renderOptions);
  }

  generateFilename(sequence: SequenceData, options: ShareOptions): string {
    const sequenceName = sequence.word || sequence.name || 'sequence';
    const date = new Date().toISOString().split('T')[0]; // YYYY-MM-DD
    const extension = options.format.toLowerCase();
    
    // Clean filename
    const cleanName = sequenceName.replace(/[^a-zA-Z0-9-_]/g, '_');
    
    return `${cleanName}_${date}.${extension}`;
  }

  validateOptions(options: ShareOptions): { valid: boolean; errors: string[] } {
    const errors: string[] = [];

    // Validate format
    if (!['PNG', 'JPEG', 'WebP'].includes(options.format)) {
      errors.push(`Invalid format: ${options.format}`);
    }

    // Validate quality
    if (options.quality < 0 || options.quality > 1) {
      errors.push(`Quality must be between 0 and 1, got: ${options.quality}`);
    }

    // Validate beat size
    if (options.beatSize <= 0) {
      errors.push(`Beat size must be positive, got: ${options.beatSize}`);
    }

    // Validate margin
    if (options.margin < 0) {
      errors.push(`Margin must be non-negative, got: ${options.margin}`);
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  // Private helper methods

  private convertToRenderOptions(shareOptions: ShareOptions) {
    // Convert our simple ShareOptions to the render service's SequenceExportOptions
    return {
      // Core export settings
      includeStartPosition: shareOptions.includeStartPosition,
      addBeatNumbers: shareOptions.addBeatNumbers,
      addReversalSymbols: true, // Always include for completeness
      addUserInfo: shareOptions.addUserInfo,
      addWord: shareOptions.addWord,
      combinedGrids: false,
      addDifficultyLevel: shareOptions.addDifficultyLevel,

      // Scaling and sizing
      beatScale: 1.0,
      beatSize: shareOptions.beatSize,
      margin: shareOptions.margin,

      // Visibility settings
      redVisible: true,
      blueVisible: true,

      // User information
      userName: shareOptions.userName || 'TKA User',
      exportDate: new Date().toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
      }).replace(/\//g, '-'),
      notes: shareOptions.notes || 'Created with The Kinetic Alphabet',

      // Output format
      format: shareOptions.format,
      quality: shareOptions.quality,
      scale: 1.0,
      backgroundColor: shareOptions.backgroundColor,
    };
  }

  private convertToPreviewOptions(shareOptions: ShareOptions) {
    // Convert ShareOptions for thumbnail preview (MAXIMUM SPEED)
    return {
      // Core export settings - same as full export
      includeStartPosition: shareOptions.includeStartPosition,
      addBeatNumbers: shareOptions.addBeatNumbers,
      addReversalSymbols: true,
      addUserInfo: shareOptions.addUserInfo,
      addWord: shareOptions.addWord,
      combinedGrids: false,
      addDifficultyLevel: shareOptions.addDifficultyLevel,

      // Scaling and sizing - MINIMAL SIZE for instant generation
      beatScale: 0.15, // Tiny thumbnail (15% of full size) - lightning fast
      beatSize: shareOptions.beatSize,
      margin: shareOptions.margin,

      // Visibility settings
      redVisible: true,
      blueVisible: true,

      // User information
      userName: shareOptions.userName || 'TKA User',
      exportDate: new Date().toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'numeric',
        day: 'numeric',
      }).replace(/\//g, '-'),
      notes: shareOptions.notes || 'Created with The Kinetic Alphabet',

      // Output format - Maximum speed optimization
      format: 'JPEG' as const, // JPEG encodes much faster than PNG
      quality: 0.4, // Minimum acceptable quality for instant speed
      scale: 0.15, // Match beatScale for consistency
      backgroundColor: shareOptions.backgroundColor,
    };
  }

  private triggerDownload(blob: Blob, filename: string): void {
    // Create download link and trigger it
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  }
}
