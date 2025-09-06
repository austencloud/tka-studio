/**
 * Utilities for URL handling and sequence URL generation
 */
import type { BeatData } from '$lib/state/stores/sequence/SequenceContainer';
import { browser } from '$app/environment';
import { logger } from '$lib/core/logging';
import { showSuccess } from '$lib/components/shared/ToastManager.svelte';
import { encodeSequenceCompact } from './SequenceEncoder';
import { decodeSequenceCompact } from './SequenceDecoder';
import { compressString, decompressString } from '$lib/utils/lzstring';

/**
 * Generate a compact shareable URL for a sequence
 * @param {BeatData[]} beats - The sequence beats
 * @param {string} _sequenceName - The name of the sequence (unused, kept for API compatibility)
 * @returns {Promise<string>} The shareable URL
 */
export async function generateShareableUrl(
	beats: BeatData[],
	_sequenceName: string
): Promise<string> {
	if (!browser) return '';

	try {
		// Generate compact format
		const compact = encodeSequenceCompact(beats);

		// Compress the string using our centralized utility
		const encoded = await compressString(compact);

		// Create URL with data
		const url = new URL(window.location.href);
		url.searchParams.set('seq', encoded);

		return url.toString();
	} catch (error) {
		logger.error('Failed to generate shareable URL', {
			error: error instanceof Error ? error : new Error(String(error))
		});
		return window.location.href;
	}
}

/**
 * Check for a sequence in the URL and load it if found
 * @param {any} sequenceContainer - The sequence container to load the sequence into
 * @returns {Promise<boolean>} True if a sequence was found and loaded
 */
export async function checkForSequenceInUrl(sequenceContainer: any): Promise<boolean> {
	if (!browser) return false;

	try {
		// Get the URL parameters
		const url = new URL(window.location.href);
		const seqParam = url.searchParams.get('seq');

		// If no sequence parameter, return false
		if (!seqParam) {
			return false;
		}

		// Try to decompress the sequence parameter
		const decompressedParam = await decompressString(seqParam);

		// Try to decode the sequence
		const reconstructedBeats = await decodeSequenceCompact(decompressedParam);

		// If no beats were reconstructed, return false
		if (!reconstructedBeats || reconstructedBeats.length === 0) {
			return false;
		}

		// Load the sequence into the app
		sequenceContainer.setSequence(reconstructedBeats);

		// Show success message
		const moveCount = reconstructedBeats.length - 1; // Subtract start position
		showSuccess(`Loaded sequence with ${moveCount} move${moveCount !== 1 ? 's' : ''}`);

		// Remove the parameter from URL (optional)
		const url2 = new URL(window.location.href);
		url2.searchParams.delete('seq');
		window.history.replaceState({}, '', url2);

		return true;
	} catch (error) {
		const errorMsg = error instanceof Error ? error.message : String(error);
		logger.error(`Failed to reconstruct sequence from URL: ${errorMsg}`);
		return false;
	}
}
