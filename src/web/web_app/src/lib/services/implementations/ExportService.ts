/**
 * Export Service - Sequence export functionality
 *
 * Handles exporting sequences to various formats (images, JSON, etc.)
 */

import type { BeatData, SequenceData } from '$lib/domain';
import type { ExportOptions, IExportService, IPictographService } from '../interfaces';

export class ExportService implements IExportService {
	// pictographService reserved for future richer rendering; omitted to reduce lint noise
	constructor(_pictographService: IPictographService) {}

	/**
	 * Export sequence as PNG image
	 */
	async exportSequenceAsImage(sequence: SequenceData, options: ExportOptions): Promise<Blob> {
		try {
			console.log(`Exporting sequence "${sequence.name}" as image`);

			// Create canvas for rendering
			const canvas = document.createElement('canvas');
			const ctx = canvas.getContext('2d');

			if (!ctx) {
				throw new Error('Canvas 2D context not available');
			}

			// Calculate dimensions
			const beatSize = options.beatSize;
			const spacing = options.spacing;
			const totalBeats = sequence.beats.length;
			const cols = Math.ceil(Math.sqrt(totalBeats));
			const rows = Math.ceil(totalBeats / cols);

			canvas.width = cols * beatSize + (cols - 1) * spacing;
			canvas.height = rows * beatSize + (rows - 1) * spacing;

			// Set background
			ctx.fillStyle = '#ffffff';
			ctx.fillRect(0, 0, canvas.width, canvas.height);

			// Render each beat (placeholder implementation)
			for (let i = 0; i < totalBeats; i++) {
				const beat = sequence.beats[i];
				const col = i % cols;
				const row = Math.floor(i / cols);
				const x = col * (beatSize + spacing);
				const y = row * (beatSize + spacing);

				await this.renderBeatPlaceholder(ctx, beat as BeatData, x, y, beatSize);
			}

			// Add title if requested
			if (options.includeTitle) {
				this.renderTitle(ctx, sequence.name, canvas.width);
			}

			// Convert to blob
			return new Promise<Blob>((resolve, reject) => {
				canvas.toBlob((blob) => {
					if (blob) {
						resolve(blob);
					} else {
						reject(new Error('Failed to create image blob'));
					}
				}, 'image/png');
			});
		} catch (error) {
			console.error('Failed to export sequence as image:', error);
			throw new Error(
				`Export failed: ${error instanceof Error ? error.message : 'Unknown error'}`
			);
		}
	}

	/**
	 * Export sequence as JSON
	 */
	async exportSequenceAsJson(sequence: SequenceData): Promise<string> {
		try {
			console.log(`Exporting sequence "${sequence.name}" as JSON`);

			// Add export metadata
			const exportData = {
				...sequence,
				exportedAt: new Date().toISOString(),
				exportedBy: 'TKA V2 Modern',
				version: '2.0.0',
			};

			return JSON.stringify(exportData, null, 2);
		} catch (error) {
			console.error('Failed to export sequence as JSON:', error);
			throw new Error(
				`JSON export failed: ${error instanceof Error ? error.message : 'Unknown error'}`
			);
		}
	}

	/**
	 * Render beat placeholder on canvas
	 */
	private async renderBeatPlaceholder(
		ctx: CanvasRenderingContext2D,
		beat: BeatData,
		x: number,
		y: number,
		size: number
	): Promise<void> {
		// Draw beat frame
		ctx.strokeStyle = '#e5e7eb';
		ctx.lineWidth = 2;
		ctx.strokeRect(x, y, size, size);

		// Draw beat number
		ctx.fillStyle = '#374151';
		ctx.font = '16px monospace';
		ctx.textAlign = 'center';
		ctx.fillText(String(beat.beat_number), x + size / 2, y + size / 2 + 6);

		// Draw motion indicators
		const blueMotion = beat.pictograph_data?.motions?.blue;
		if (blueMotion) {
			ctx.fillStyle = '#3b82f6';
			ctx.fillRect(x + 5, y + 5, 10, 10);
		}

		const redMotion = beat.pictograph_data?.motions?.red;
		if (redMotion) {
			ctx.fillStyle = '#ef4444';
			ctx.fillRect(x + size - 15, y + 5, 10, 10);
		}
	}

	/**
	 * Render title on canvas
	 */
	private renderTitle(ctx: CanvasRenderingContext2D, title: string, canvasWidth: number): void {
		ctx.fillStyle = '#111827';
		ctx.font = 'bold 24px system-ui';
		ctx.textAlign = 'center';
		ctx.fillText(title, canvasWidth / 2, 30);
	}

	/**
	 * Get default export options
	 */
	getDefaultExportOptions(): ExportOptions {
		return {
			beatSize: 150,
			spacing: 10,
			includeTitle: true,
			includeMetadata: false,
		};
	}
}
