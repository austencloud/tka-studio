/**
 * Sequence Renderer
 *
 * This module provides functionality for rendering sequences to images.
 */

import { browser } from '$app/environment';
import { logger } from '$lib/core/logging';
import { exportSequenceImage } from '$lib/components/Pictograph/export/SequenceImageExporter';

import type { SequenceRenderResult } from './ImageUtils';
import { findBeatFrameElement } from './ElementFinder';
import { getImageExportSettings } from '$lib/state/image-export-settings.svelte';

/**
 * Options for rendering a sequence
 */
export interface SequenceRenderOptions {
	sequenceName: string;
	sequenceBeats: any[]; // Use any[] to accommodate both Beat[] and BeatData[]
	difficultyLevel?: number;
	beatFrameElement?: HTMLElement | null;
}

/**
 * Render a sequence to an image
 *
 * @param options Render options
 * @returns Promise resolving to the render result or null if rendering failed
 */
export async function renderSequence(
	options: SequenceRenderOptions
): Promise<SequenceRenderResult | null> {
	const { sequenceName, sequenceBeats, difficultyLevel = 1, beatFrameElement = null } = options;

	// Try to find the beat frame element if not provided
	let element = beatFrameElement;
	if (!element) {
		element = findBeatFrameElement();
	}

	if (!browser || !element) {
		console.error('Cannot render: not in browser environment or no beat frame element');

		// Try to find the element one more time using more aggressive selectors
		const alternativeElement =
			document.querySelector('.sequence-widget') ||
			document.querySelector('.sequence-container') ||
			document.querySelector('.sequence');

		if (alternativeElement instanceof HTMLElement) {
			console.log('SequenceRenderer: Found alternative element for rendering:', alternativeElement);
			element = alternativeElement;
		} else {
			return null;
		}
	}

	try {
		console.log('SequenceRenderer: Starting sequence rendering');
		console.log('SequenceRenderer: Beat frame element:', element);

		// Get export settings using new function
		let settings = getImageExportSettings();
		console.log('SequenceRenderer: Export settings:', settings);

		// Find the start position beat
		let startPosition = null;
		for (const beat of sequenceBeats) {
			if (beat.metadata?.isStartPosition) {
				startPosition = beat;
				break;
			}
		}

		console.log('SequenceRenderer: Start position found:', !!startPosition);
		console.log('SequenceRenderer: Sequence beats count:', sequenceBeats.length);

		// Ensure the beat frame element is fully rendered
		// Add a small delay to ensure all SVGs are fully rendered
		await new Promise((resolve) => setTimeout(resolve, 250));

		// Export the sequence using the same settings as the image export tab
		const result = await exportSequenceImage(element, {
			beats: sequenceBeats as any,
			startPosition: startPosition as any,
			backgroundColor: '#FFFFFF', // Always use white for better contrast
			scale: 2, // Higher scale for better quality
			quality: 1.0, // Always use maximum quality
			format: 'png', // PNG format for lossless quality
			// Use the same column calculation as the preview to ensure consistency
			// This ensures the downloaded image matches what the user sees in the preview
			columns: sequenceBeats.length <= 4 ? sequenceBeats.length : 4,
			spacing: 0,
			// Always include start position
			includeStartPosition: true, // Force to true regardless of settings
			addWord: settings.addWord === undefined ? true : !!settings.addWord,
			addUserInfo: settings.addUserInfo === undefined ? true : !!settings.addUserInfo,
			addDifficultyLevel:
				settings.addDifficultyLevel === undefined ? true : !!settings.addDifficultyLevel,
			addBeatNumbers: settings.addBeatNumbers === undefined ? true : !!settings.addBeatNumbers,
			addReversalSymbols:
				settings.addReversalSymbols === undefined ? true : !!settings.addReversalSymbols,
			title: sequenceName,
			userName: settings.userName || 'User',
			notes: settings.customNote || 'Created using The Kinetic Constructor',
			difficultyLevel: difficultyLevel
		});

		console.log('SequenceRenderer: Rendering completed successfully', {
			dataUrlLength: result?.dataUrl?.length || 0,
			width: result?.width || 0,
			height: result?.height || 0
		});

		// Validate the result
		if (!result || !result.dataUrl || result.dataUrl.length < 1000) {
			console.error('SequenceRenderer: Invalid rendering result', result);
			throw new Error('Failed to generate a valid image');
		}

		return result;
	} catch (error) {
		console.error('Error rendering sequence:', error);
		logger.error('Error rendering sequence', {
			error: error instanceof Error ? error : new Error(String(error))
		});
		return null;
	}
}
