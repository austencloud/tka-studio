/**
 * Download Handler
 *
 * This module provides functionality for downloading sequence images.
 */

import { browser } from '$app/environment';
import { logger } from '$lib/core/logging';
import { showError, showSuccess, showInfo } from '$lib/components/shared/ToastManager.svelte';
import {
	downloadImage,
	type DownloadResult
} from '$lib/components/Pictograph/export/downloadUtils';
import { getImageExportSettings } from '$lib/state/image-export-settings.svelte';
import { isMobileDevice } from '$lib/utils/fileSystemUtils';
import type { SequenceRenderResult } from './ImageUtils';

/**
 * Options for downloading a sequence image
 */
export interface DownloadOptions {
	sequenceName: string;
	imageResult: SequenceRenderResult;
}

/**
 * Download a sequence image
 *
 * @param options Download options
 * @returns Promise resolving to true if download was successful
 */
export async function downloadSequenceImage(options: DownloadOptions): Promise<boolean> {
	const { sequenceName, imageResult } = options;

	if (!browser) {
		console.log('DownloadHandler: Not in browser environment, returning false');
		return false;
	}

	try {
		console.log('DownloadHandler: Starting download process');

		// Get export settings
		let settings: any = {};
		try {
			// Get settings directly using new function
			settings = getImageExportSettings();
			console.log('DownloadHandler: Using settings from getImageExportSettings()', {
				...settings
			});
		} catch (error) {
			console.error('DownloadHandler: Error getting export settings from function', error);

			// Fall back to localStorage if function fails
			try {
				// Get settings from localStorage as fallback
				const savedSettings = localStorage.getItem('image-export-settings');
				if (savedSettings) {
					try {
						const parsed = JSON.parse(savedSettings);
						if (parsed && typeof parsed === 'object') {
							settings = parsed;
							console.log('DownloadHandler: Using settings from localStorage', settings);
						}
					} catch (parseError) {
						console.error(
							'DownloadHandler: Failed to parse settings from localStorage',
							parseError
						);
					}
				}
			} catch (localStorageError) {
				console.error(
					'DownloadHandler: Error getting export settings from localStorage',
					localStorageError
				);
				// Use empty object, which will fall back to defaults
				settings = {};
			}
		}

		// Get the exact sequence word from the UI
		const exactWordName = sequenceName || 'Sequence';

		// Log the exact word being used
		console.log('DownloadHandler: Using exact sequence word:', exactWordName);

		// Use the exact word for the filename (preserving case and format)
		// This makes it more recognizable to users
		const filename = `${exactWordName}.png`;

		console.log('DownloadHandler: Downloading sequence:', {
			wordName: exactWordName,
			dataUrlLength: imageResult.dataUrl.length,
			filename
		});

		// Use the direct download approach with the standard file save dialog
		try {
			console.log('DownloadHandler: Starting download with downloadImage function');

			// Download the image with improved error handling
			const result = await downloadImage({
				dataUrl: imageResult.dataUrl,
				filename
			});

			// Log the result for debugging
			console.log('DownloadHandler: downloadImage returned:', result);

			if (result.success) {
				// Determine if we're on a mobile device
				const isMobile = isMobileDevice();

				// Show appropriate success message based on platform
				if (isMobile) {
					// For mobile, show a simpler message
					showSuccess("Image saved to your device's Downloads folder", { duration: 5000 });
				} else if (result.folderPath !== 'Browser Tab' && result.fileName) {
					// For desktop with known path, create a descriptive message
					const folderToShow = result.folderPath || 'Downloads';
					let message = `Image saved as "${result.fileName}"`;
					message += ` to ${folderToShow}`;

					// Show a detailed message with the file location
					showInfo(message, {
						duration: 7000 // Longer duration so user has time to read
					});
				} else if (result.folderPath === 'Browser Tab') {
					// For browser tab exports
					showSuccess('Image opened in a new browser tab', { duration: 5000 });
				} else {
					// Generic success message as fallback
					showSuccess('Image saved successfully to Downloads folder', { duration: 5000 });
				}

				console.log('DownloadHandler: Download completed successfully');
				return true;
			} else {
				console.warn('DownloadHandler: Download function returned false without throwing an error');
				throw new Error('Download function returned false');
			}
		} catch (downloadError) {
			// Log the full error for debugging
			console.error(
				'DownloadHandler: Download error:',
				downloadError instanceof Error
					? {
							name: downloadError.name,
							message: downloadError.message,
							stack: downloadError.stack
						}
					: downloadError
			);

			// Check for user cancellation with standardized error message
			if (
				downloadError instanceof Error &&
				(downloadError.message === 'USER_CANCELLED_OPERATION' ||
					downloadError.message.includes('cancelled') ||
					downloadError.message.includes('canceled') ||
					downloadError.message.includes('aborted') ||
					downloadError.name === 'AbortError')
			) {
				console.log('DownloadHandler: User cancelled save operation');
				// Return false but don't show an error message for user cancellations
				return false;
			}

			// Show error for actual errors (not cancellations)
			showError('Failed to download sequence. Please try again.');
			return false;
		}
	} catch (error) {
		showError('Failed to download sequence');
		console.error('DownloadHandler: Download error:', error);
		logger.error('Error downloading sequence', {
			error: error instanceof Error ? error : new Error(String(error))
		});
		return false;
	}
}
