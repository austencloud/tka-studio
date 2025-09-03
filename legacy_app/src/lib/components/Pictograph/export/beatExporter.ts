/**
 * Beat Exporter
 *
 * This module provides functionality to export a single beat as an image.
 * It uses a direct SVG approach for more reliable rendering.
 */

import { browser } from '$app/environment';
import { logger } from '$lib/core/logging';
import type { PictographData } from '$lib/types/PictographData';
import { renderSvgToImage } from './svgRenderer';
import { downloadImage } from './downloadUtils';

/**
 * Options for exporting a beat as an image
 */
export interface BeatExportOptions {
	// Content options
	pictographData: PictographData;
	beatNumber?: number;
	isStartPosition?: boolean;

	// Visual options
	backgroundColor?: string;
	scale?: number;
	quality?: number;
	format?: 'png' | 'jpeg';

	// Dimensions
	width?: number;
	height?: number;
}

/**
 * Result of exporting a beat as an image
 */
export interface BeatExportResult {
	dataUrl: string;
	width: number;
	height: number;
	format: string;
}

/**
 * Exports a single beat as an image
 *
 * @param svgElement The SVG element to export
 * @param options Export options
 * @returns Promise resolving to the export result
 */
export async function exportBeatAsImage(
	svgElement: SVGElement,
	options: BeatExportOptions
): Promise<BeatExportResult> {
	// Validate environment
	if (!browser) {
		return Promise.reject(new Error('Cannot export: not in browser environment'));
	}

	// Validate element
	if (!svgElement) {
		return Promise.reject(new Error('Cannot export: no SVG element provided'));
	}

	try {
		console.log('BeatExporter: Starting export process');

		// Default options
		const defaultOptions: Required<BeatExportOptions> = {
			pictographData: options.pictographData,
			backgroundColor: '#FFFFFF',
			scale: 2,
			quality: 0.92,
			format: 'png',
			width: 950,
			height: 950,
			beatNumber: options.beatNumber || 0,
			isStartPosition: options.isStartPosition || false
		};

		// Merge options
		const mergedOptions: Required<BeatExportOptions> = { ...defaultOptions, ...options };

		// Render the SVG to an image
		const result = await renderSvgToImage({
			element: svgElement,
			backgroundColor: mergedOptions.backgroundColor,
			scale: mergedOptions.scale,
			quality: mergedOptions.quality,
			format: mergedOptions.format,
			width: mergedOptions.width,
			height: mergedOptions.height
		});

		console.log('BeatExporter: Export completed successfully', {
			width: result.width,
			height: result.height,
			dataUrlLength: result.dataUrl.length
		});

		// Return the result
		return {
			dataUrl: result.dataUrl,
			width: result.width,
			height: result.height,
			format: result.format
		};
	} catch (error) {
		// Log detailed error information
		logger.error('Error exporting beat image', {
			error: error instanceof Error ? error : new Error(String(error))
		});

		// Re-throw the error
		throw new Error(
			`Failed to export beat image: ${error instanceof Error ? error.message : String(error)}`
		);
	}
}

/**
 * Downloads a beat image
 *
 * @param result The beat export result
 * @param filename The filename to use for the download
 * @returns Promise resolving to true if successful
 */
export async function downloadBeatImage(
	result: BeatExportResult,
	filename: string = `pictograph-${Date.now()}.png`
): Promise<boolean> {
	return downloadImage({
		dataUrl: result.dataUrl,
		filename: filename.endsWith(`.${result.format}`) ? filename : `${filename}.${result.format}`
	});
}
