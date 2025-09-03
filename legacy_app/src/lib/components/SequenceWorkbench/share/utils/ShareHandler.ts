/**
 * Share Handler
 *
 * This module provides functionality for sharing sequences using the Web Share API.
 */

import { browser } from '$app/environment';
import { logger } from '$lib/core/logging';
import { showError, showSuccess } from '$lib/components/shared/ToastManager.svelte';
import type { SequenceRenderResult } from './ImageUtils';
import { dataURLtoBlob } from './ImageUtils';
import { isWebShareSupported, isFileShareSupported } from './WebShareApi';
import { generateShareableUrl } from './UrlUtils';

// Track the last time a share was attempted to prevent issues with multiple rapid calls
let lastShareApiCallTime = 0;
const MIN_SHARE_API_INTERVAL_MS = 1000; // Minimum 1 second between Web Share API calls

/**
 * Options for sharing a sequence
 */
export interface ShareOptions {
	sequenceBeats: any[]; // Use any[] to accommodate both Beat[] and BeatData[]
	sequenceName: string;
	imageResult?: SequenceRenderResult | null;
}

/**
 * Share a sequence with or without an image
 *
 * @param options Share options
 * @returns Promise resolving to true if sharing was successful
 */
export async function shareSequence(options: ShareOptions): Promise<boolean> {
	const { sequenceBeats, sequenceName, imageResult } = options;

	if (!browser) {
		console.log('ShareHandler: Not in browser environment, returning false');
		return false;
	}

	// Check if sequence is empty
	if (!sequenceBeats || sequenceBeats.length === 0) {
		showError('No sequence to share');
		return false;
	}

	// Check if Web Share API is supported
	if (!isWebShareSupported()) {
		showError("Your device doesn't support sharing");
		return false;
	}

	// Check if we've attempted to share too recently
	const now = Date.now();
	const timeSinceLastAttempt = now - lastShareApiCallTime;
	if (timeSinceLastAttempt < MIN_SHARE_API_INTERVAL_MS) {
		console.log(
			`ShareHandler: Share API called too soon (${timeSinceLastAttempt}ms since last attempt)`
		);
		showError('Please wait a moment before sharing again');
		return false;
	}

	// Update the last attempt time
	lastShareApiCallTime = now;

	try {
		// Generate shareable URL
		const shareUrl = generateShareableUrl(sequenceBeats, sequenceName);

		// Create share data
		const shareData: any = {
			title: 'Kinetic Constructor Sequence',
			text: `Check out this sequence: ${sequenceName}\n\nOpen this link to reconstruct: ${shareUrl}`,
			url: shareUrl
		};

		// Try to share with image if supported and image is available
		if (imageResult && imageResult.dataUrl && isFileShareSupported()) {
			try {
				// Convert data URL to blob
				const blob = dataURLtoBlob(imageResult.dataUrl);

				// Create file from blob
				const file = new File([blob], `${sequenceName}.png`, { type: 'image/png' });

				// Add file to share data
				shareData.files = [file];

				// Check if device can share with files
				if (navigator.canShare && navigator.canShare(shareData)) {
					// Use a small timeout to ensure the browser is ready
					await new Promise((resolve) => setTimeout(resolve, 100));

					await navigator.share(shareData);
					console.log('ShareHandler: Share with files completed successfully');
					showSuccess('Sequence shared successfully');
					return true;
				} else {
					console.log(
						'ShareHandler: Device cannot share with files, falling back to text+URL only'
					);
					// Fall through to text+URL sharing
				}
			} catch (fileError) {
				// If there's an error with file sharing, log it and fall back to text+URL sharing
				if (fileError instanceof Error && fileError.name === 'AbortError') {
					console.log('ShareHandler: User cancelled file sharing');
					return false;
				}

				console.warn(
					'ShareHandler: Error sharing with file, falling back to text+URL only:',
					fileError
				);
				// Fall through to text+URL sharing
			}
		}

		// Fall back to sharing just the text and URL
		console.log('ShareHandler: Attempting to share with text and URL only');
		const textOnlyShareData = {
			title: shareData.title,
			text: shareData.text,
			url: shareData.url
		};

		// Use a small timeout to ensure the browser is ready
		await new Promise((resolve) => setTimeout(resolve, 100));

		await navigator.share(textOnlyShareData);
		console.log('ShareHandler: Text+URL share completed successfully');
		showSuccess('Sequence shared successfully');
		return true;
	} catch (error) {
		// Don't show error for user cancellation
		if (error instanceof Error && error.name === 'AbortError') {
			console.log('ShareHandler: User cancelled sharing');
			return false;
		}

		console.error('ShareHandler: Error in shareSequence:', error);
		logger.error('Error sharing sequence', {
			error: error instanceof Error ? error : new Error(String(error))
		});

		// Only show error if it's not a user cancellation
		showError('Unable to share sequence. Please try again.');
		return false;
	} finally {
		// Ensure we update the last share time even if there was an error
		lastShareApiCallTime = Date.now();
	}
}
