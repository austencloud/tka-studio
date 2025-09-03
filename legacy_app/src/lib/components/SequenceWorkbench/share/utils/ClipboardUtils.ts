/**
 * Utilities for clipboard operations
 */
import { browser } from '$app/environment';
import { logger } from '$lib/core/logging';
import { showError, showSuccess } from '$lib/components/shared/ToastManager.svelte';

/**
 * Copy a URL to the clipboard
 * @param {string} url - The URL to copy
 * @returns {Promise<boolean>} True if copying was successful
 */
export async function copyToClipboard(url: string): Promise<boolean> {
    if (!browser) return false;

    try {
        await navigator.clipboard.writeText(url);
        showSuccess('Link copied to clipboard');
        return true;
    } catch (error) {
        logger.error('Failed to copy to clipboard', {
            error: error instanceof Error ? error : new Error(String(error))
        });
        showError('Failed to copy link to clipboard');
        return false;
    }
}

/**
 * Copy an image to the clipboard (if supported)
 * @param {Blob} blob - The image blob to copy
 * @returns {Promise<boolean>} True if copying was successful
 */
export async function copyImageToClipboard(blob: Blob): Promise<boolean> {
    if (!browser) return false;

    try {
        // Check if the clipboard API supports writing images
        if (!navigator.clipboard || !navigator.clipboard.write) {
            showError('Your browser does not support copying images to clipboard');
            return false;
        }

        // Create a ClipboardItem with the image
        const item = new ClipboardItem({
            [blob.type]: blob
        });

        // Write to clipboard
        await navigator.clipboard.write([item]);
        showSuccess('Image copied to clipboard');
        return true;
    } catch (error) {
        logger.error('Failed to copy image to clipboard', {
            error: error instanceof Error ? error : new Error(String(error))
        });
        showError('Failed to copy image to clipboard');
        return false;
    }
}
