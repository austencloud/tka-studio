/**
 * Shared types for the share utilities
 */

/**
 * Interface for share data
 */
export interface ShareData {
    title: string;
    text: string;
    url: string;
    files?: File[]; // Support for image files in share data
}
