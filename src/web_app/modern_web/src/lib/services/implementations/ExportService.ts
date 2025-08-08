/**
 * Export Service - Sequence export functionality
 * 
 * Handles exporting sequences to various formats (images, JSON, etc.)
 */

import type { SequenceData } from '@tka/schemas';
import type { 
	IExportService, 
	ExportOptions,
	IPictographService 
} from '../interfaces';

export class ExportService implements IExportService {
	constructor(
		private pictographService: IPictographService
	) {}

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
			const cols = Math.ceil(Math.sqrt(sequence.beats.length));
			const rows = Math.ceil(sequence.beats.length / cols);

			canvas.width = cols * beatSize + (cols - 1) * spacing;
			canvas.height = rows * beatSize + (rows - 1) * spacing;

			// Set background
			ctx.fillStyle = '#ffffff';
			ctx.fillRect(0, 0, canvas.width, canvas.height);

			// Render each beat (placeholder implementation)
			for (let i = 0; i < sequence.beats.length; i++) {
				const beat = sequence.beats[i];
				const col = i % cols;
				const row = Math.floor(i / cols);
				const x = col * (beatSize + spacing);
				const y = row * (beatSize + spacing);

				await this.renderBeatPlaceholder(ctx, beat, x, y, beatSize);
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
			throw new Error(`Export failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
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
				version: '2.0.0'
			};

			return JSON.stringify(exportData, null, 2);
		} catch (error) {
			console.error('Failed to export sequence as JSON:', error);
			throw new Error(`JSON export failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
		}
	}

	/**
	 * Render beat placeholder on canvas
	 */
	private async renderBeatPlaceholder(
		ctx: CanvasRenderingContext2D,
		beat: any,
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
		ctx.fillText(
			beat.beatNumber.toString(),
			x + size / 2,
			y + size / 2 + 6
		);

		// Draw motion indicators
		if (beat.blueMotion) {
			ctx.fillStyle = '#3b82f6';
			ctx.fillRect(x + 5, y + 5, 10, 10);
		}

		if (beat.redMotion) {
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
			includeMetadata: false
		};
	}
}
