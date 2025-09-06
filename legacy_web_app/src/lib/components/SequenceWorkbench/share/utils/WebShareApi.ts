/**
 * Utilities for working with the Web Share API
 */
import { browser } from '$app/environment';
import { logger } from '$lib/core/logging';
import { showError, showSuccess } from '$lib/components/shared/ToastManager.svelte';
import type { ShareData } from './types';

// Track the last time a share was attempted to prevent issues with multiple rapid calls
let lastShareApiCallTime = 0;
const MIN_SHARE_API_INTERVAL_MS = 1000; // Minimum 1 second between Web Share API calls

/**
 * Check if Web Share API is supported
 * @returns {boolean} True if Web Share API is supported
 */
export function isWebShareSupported(): boolean {
    if (!browser) {
        return false;
    }

    try {
        // Basic check for Web Share API support
        const hasShareAPI = 'share' in navigator && typeof navigator.share === 'function';
        return hasShareAPI;
    } catch (error) {
        console.warn('shareUtils: Error checking Web Share API support:', error);
        return false;
    }
}

/**
 * Check if file sharing is supported via Web Share API
 * @returns {boolean} True if file sharing is supported
 */
export function isFileShareSupported(): boolean {
    if (!browser) {
        return false;
    }

    try {
        // First check if basic Web Share API is supported
        if (!isWebShareSupported()) {
            return false;
        }

        // Then check if canShare method exists
        if (!('canShare' in navigator && typeof navigator.canShare === 'function')) {
            return false;
        }

        // Create a dummy file for testing
        const dummyFile = new File(['test'], 'test.png', { type: 'image/png' });

        // Check if the browser can share files
        const canShareFiles = navigator.canShare({ files: [dummyFile] });

        return canShareFiles;
    } catch (error) {
        // If any error occurs, assume file sharing is not supported
        console.warn('shareUtils: File sharing check failed:', error);
        return false;
    }
}

/**
 * Check if the device is mobile
 * @returns {boolean} True if the device is mobile
 */
export function isMobileDevice(): boolean {
    if (!browser) return false;
    return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

/**
 * Share a sequence using the Web Share API
 * @param {ShareData} shareData - The data to share
 * @returns {Promise<boolean>} True if sharing was successful
 */
export async function shareSequence(shareData: ShareData): Promise<boolean> {
    if (!browser) {
        console.log('shareUtils: Not in browser environment, returning false');
        return false;
    }

    if (!isWebShareSupported()) {
        console.log('shareUtils: Web Share API not supported, returning false');
        showError("Your device doesn't support sharing");
        return false;
    }

    // Check if we've attempted to share too recently
    const now = Date.now();
    const timeSinceLastAttempt = now - lastShareApiCallTime;
    if (timeSinceLastAttempt < MIN_SHARE_API_INTERVAL_MS) {
        console.log(
            `shareUtils: Share API called too soon (${timeSinceLastAttempt}ms since last attempt)`
        );
        showError('Please wait a moment before sharing again');
        return false;
    }

    // Update the last attempt time
    lastShareApiCallTime = now;

    try {
        // Use a small timeout to ensure the browser is ready
        await new Promise((resolve) => setTimeout(resolve, 100));

        await navigator.share(shareData);
        console.log('shareUtils: Share completed successfully');
        logger.info('Sequence shared successfully');
        showSuccess('Sequence shared successfully');
        return true;
    } catch (error) {
        // Don't show error for user cancellation
        if (error instanceof Error && error.name === 'AbortError') {
            console.log('shareUtils: User cancelled sharing');
            logger.info('User cancelled sharing');
            return false;
        }

        console.error('shareUtils: Error in shareSequence:', error);
        logger.error('Error sharing sequence', {
            error: error instanceof Error ? error : new Error(String(error))
        });
        showError('Failed to share sequence');
        return false;
    } finally {
        // Ensure we update the last share time even if there was an error
        lastShareApiCallTime = Date.now();
    }
}

/**
 * Share a sequence image with a reconstruction URL
 * This is the primary sharing function that handles both image and URL sharing
 * @param {any} imageResult - The rendered image result
 * @param {string} sequenceName - The name of the sequence
 * @param {string} shareUrl - The shareable URL
 * @returns {Promise<boolean>} True if sharing was successful
 */
export async function shareSequenceWithImage(
    imageResult: any,
    sequenceName: string,
    shareUrl: string
): Promise<boolean> {
    console.log('shareSequenceWithImage called with:', { sequenceName, shareUrl });

    if (!browser) {
        console.log('shareUtils: Not in browser environment, returning false');
        return false;
    }

    // First check if Web Share API is supported at all
    if (!isWebShareSupported()) {
        console.log('shareUtils: Web Share API not supported, returning false');
        showError("Your device doesn't support sharing");
        return false;
    }

    // Check if we've attempted to share too recently
    const now = Date.now();
    const timeSinceLastAttempt = now - lastShareApiCallTime;
    if (timeSinceLastAttempt < MIN_SHARE_API_INTERVAL_MS) {
        console.log(
            `shareUtils: Share API called too soon (${timeSinceLastAttempt}ms since last attempt)`
        );
        showError('Please wait a moment before sharing again');
        return false;
    }

    // Update the last attempt time
    lastShareApiCallTime = now;

    try {
        // Prepare the share text
        const shareTitle = 'Kinetic Constructor Sequence';
        const shareText = `Check out this sequence${sequenceName ? ': ' + sequenceName : ''}\n\nOpen this link to reconstruct: ${shareUrl}`;

        // First try to share with image if file sharing is supported
        const fileShareSupported = isFileShareSupported();
        console.log('shareUtils: File sharing supported:', fileShareSupported);

        if (fileShareSupported && imageResult && imageResult.dataUrl) {
            try {
                // Convert the data URL to a Blob
                console.log('shareUtils: Converting data URL to Blob');
                const blob = dataURLtoBlob(imageResult.dataUrl);

                // Create a File from the Blob
                console.log('shareUtils: Creating File from Blob');
                const fileName = `${sequenceName || 'kinetic-sequence'}.png`;
                const file = new File([blob], fileName, { type: 'image/png' });

                // Create share data with the image file
                const shareData: ShareData = {
                    title: shareTitle,
                    text: shareText,
                    url: shareUrl,
                    files: [file]
                };

                // Check if the device can share this content with files
                if (navigator.canShare && navigator.canShare(shareData)) {
                    console.log('shareUtils: Device can share with files, calling navigator.share');

                    // Use a small timeout to ensure the browser is ready
                    await new Promise((resolve) => setTimeout(resolve, 100));

                    await navigator.share(shareData);
                    console.log('shareUtils: Share with files completed successfully');
                    showSuccess('Sequence shared successfully');
                    return true;
                } else {
                    console.log('shareUtils: Device cannot share with files, falling back to text+URL only');
                    // Fall through to text+URL sharing
                }
            } catch (fileError) {
                // If there's an error with file sharing, log it and fall back to text+URL sharing
                if (fileError instanceof Error && fileError.name === 'AbortError') {
                    console.log('shareUtils: User cancelled file sharing');
                    return false;
                }

                console.warn(
                    'shareUtils: Error sharing with file, falling back to text+URL only:',
                    fileError
                );
                // Fall through to text+URL sharing
            }
        }

        // Fallback to sharing just the text and URL
        console.log('shareUtils: Attempting to share with text and URL only');
        const textOnlyShareData: ShareData = {
            title: shareTitle,
            text: shareText,
            url: shareUrl
        };

        // Use a small timeout to ensure the browser is ready
        await new Promise((resolve) => setTimeout(resolve, 100));

        await navigator.share(textOnlyShareData);
        console.log('shareUtils: Text+URL share completed successfully');
        showSuccess('Sequence shared successfully');
        return true;
    } catch (error) {
        // Don't show error for user cancellation
        if (error instanceof Error && error.name === 'AbortError') {
            console.log('shareUtils: User cancelled sharing');
            return false;
        }

        console.error('shareUtils: Error in shareSequenceWithImage:', error);
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

/**
 * Convert a data URL to a Blob
 * @param {string} dataUrl - The data URL to convert
 * @returns {Blob} The converted Blob
 */
function dataURLtoBlob(dataUrl: string): Blob {
    const arr = dataUrl.split(',');
    const mime = arr[0].match(/:(.*?);/)?.[1] || 'image/png';
    const bstr = atob(arr[1]);
    let n = bstr.length;
    const u8arr = new Uint8Array(n);

    while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
    }

    return new Blob([u8arr], { type: mime });
}
