/**
 * Utilities for image handling and processing
 */
import { browser } from '$app/environment';

/**
 * Convert a data URL to a Blob
 * @param {string} dataUrl - The data URL to convert
 * @returns {Blob} The converted Blob
 */
export function dataURLtoBlob(dataUrl: string): Blob {
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

/**
 * Create a File object from a data URL
 * @param {string} dataUrl - The data URL to convert
 * @param {string} fileName - The name for the file
 * @returns {File} The created File object
 */
export function createFileFromDataURL(dataUrl: string, fileName: string): File {
    const blob = dataURLtoBlob(dataUrl);
    return new File([blob], fileName, { type: blob.type });
}

/**
 * Define a simple interface for sequence render results
 */
export interface SequenceRenderResult {
    dataUrl: string;
    width: number;
    height: number;
}
