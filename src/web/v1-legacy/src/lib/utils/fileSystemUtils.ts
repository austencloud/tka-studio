/**
 * File System Utilities
 *
 * This module provides utilities for working with the File System Access API
 * and handling file operations in a cross-platform way.
 */

import { browser } from '$app/environment';
import { logger } from '$lib/core/logging';

/**
 * Interface for directory handle metadata
 */
export interface DirectoryHandleMetadata {
	name: string;
	kind: string;
	path?: string;
	timestamp: number;
}

/**
 * Interface for file system permission descriptor
 */
export interface FileSystemPermissionDescriptor {
	mode?: 'read' | 'readwrite';
}

/**
 * Extended FileSystemDirectoryHandle with permission methods
 */
export interface FileSystemDirectoryHandleWithPermissions extends FileSystemDirectoryHandle {
	requestPermission(descriptor?: FileSystemPermissionDescriptor): Promise<PermissionState>;
}

/**
 * Extended Window with directory picker
 */
export interface WindowWithDirectoryPicker extends Window {
	showDirectoryPicker(options?: {
		id?: string;
		startIn?:
			| 'downloads'
			| 'desktop'
			| 'documents'
			| 'music'
			| 'pictures'
			| 'videos'
			| FileSystemHandle;
		mode?: 'read' | 'readwrite';
	}): Promise<FileSystemDirectoryHandle>;
}

/**
 * Get the default pictures directory path based on the operating system
 */
export function getDefaultPicturesPath(): string {
	if (!browser) return '';

	// Detect operating system
	const userAgent = navigator.userAgent.toLowerCase();

	if (userAgent.includes('win')) {
		return 'C:\\Users\\Public\\Pictures';
	} else if (userAgent.includes('mac')) {
		return '/Users/Shared/Pictures';
	} else if (userAgent.includes('linux')) {
		return '/home/Pictures';
	} else {
		return 'Pictures'; // Generic fallback
	}
}

/**
 * Save a directory handle to localStorage
 *
 * @param handle The directory handle to save
 * @param key The localStorage key to use
 */
export function saveDirHandleToLocalStorage(
	handle: FileSystemDirectoryHandle,
	key: string = 'exportDirectoryHandle'
): void {
	if (!browser) return;

	try {
		const metadata: DirectoryHandleMetadata = {
			name: handle.name,
			kind: handle.kind,
			timestamp: Date.now()
		};

		localStorage.setItem(key, JSON.stringify(metadata));
		logger.info(`Directory handle metadata saved to localStorage: ${handle.name}`);
	} catch (error) {
		logger.error(
			`Failed to save directory handle to localStorage: ${error instanceof Error ? error.message : String(error)}`
		);
	}
}

/**
 * Get a directory handle from localStorage
 *
 * @param key The localStorage key to use
 * @returns The directory handle metadata or null if not found
 */
export function getDirHandleFromLocalStorage(
	key: string = 'exportDirectoryHandle'
): DirectoryHandleMetadata | null {
	if (!browser) return null;

	try {
		const savedHandle = localStorage.getItem(key);
		if (!savedHandle) return null;

		const metadata = JSON.parse(savedHandle) as DirectoryHandleMetadata;
		return metadata;
	} catch (error) {
		logger.error(
			`Failed to get directory handle from localStorage: ${error instanceof Error ? error.message : String(error)}`
		);
		return null;
	}
}

/**
 * Check if the File System Access API is supported
 */
export function isFileSystemAccessSupported(): boolean {
	if (!browser) return false;
	return 'showDirectoryPicker' in window;
}

/**
 * Check if the device is mobile
 */
export function isMobileDevice(): boolean {
	if (!browser) return false;
	return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
}

/**
 * Get the platform type (desktop or mobile)
 */
export function getPlatformType(): 'desktop' | 'mobile' {
	return isMobileDevice() ? 'mobile' : 'desktop';
}

/**
 * Create a versioned file name for export
 *
 * @param sequenceName The name of the sequence
 * @param version The version number (default: 1)
 * @param extension The file extension (default: 'png')
 */
export function createVersionedFileName(
	sequenceName: string,
	version: number = 1,
	extension: string = 'png'
): string {
	// Clean the sequence name to be file-system friendly
	const cleanName = sequenceName.trim().replace(/[\\/:*?"<>|]/g, '_');

	// Use 'Untitled' if no name is provided
	const fileName = cleanName || 'Untitled';

	// Add version number
	return `${fileName}_v${version}.${extension}`;
}

/**
 * Create a file name for export based on sequence metadata
 * This is kept for backward compatibility
 *
 * @param sequenceName The name of the sequence
 * @param category The category of the sequence
 * @param extension The file extension (default: 'png')
 */
export function createExportFileName(
	sequenceName: string,
	category: string = '',
	extension: string = 'png'
): string {
	// Clean the sequence name to be file-system friendly
	const cleanName = sequenceName.trim().replace(/[\\/:*?"<>|]/g, '_');

	// Use 'Untitled' if no name is provided
	const fileName = cleanName || 'Untitled';

	// Add category prefix if provided
	const categoryPrefix = category ? `${createCategoryFolderName(category)}_` : '';

	// Add timestamp to ensure uniqueness
	const timestamp = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);

	return `${categoryPrefix}${fileName}_${timestamp}.${extension}`;
}

/**
 * Create a category folder name
 *
 * @param category The category name
 */
export function createCategoryFolderName(category: string): string {
	// Clean the category name to be file-system friendly
	const cleanCategory = category.trim().replace(/[\\/:*?"<>|]/g, '_');

	// Use 'Uncategorized' if no category is provided
	return cleanCategory || 'Uncategorized';
}

/**
 * Create a word-specific folder name
 *
 * This function preserves the original word format as much as possible
 * while ensuring it's file-system friendly.
 *
 * @param wordName The word name
 */
export function createWordFolderName(wordName: string): string {
	if (!wordName || wordName.trim() === '') {
		return 'Untitled';
	}

	// Preserve the original case and format
	let cleanWord = wordName.trim();

	// Replace invalid characters with underscores, but preserve letters, numbers, and basic punctuation
	cleanWord = cleanWord.replace(/[\\/:*?"<>|]/g, '_');

	// Ensure the name doesn't start or end with a period (Windows restriction)
	if (cleanWord.startsWith('.')) {
		cleanWord = '_' + cleanWord.substring(1);
	}

	if (cleanWord.endsWith('.')) {
		cleanWord = cleanWord.substring(0, cleanWord.length - 1) + '_';
	}

	// Ensure the name isn't a reserved Windows name
	const reservedNames = [
		'CON',
		'PRN',
		'AUX',
		'NUL',
		'COM1',
		'COM2',
		'COM3',
		'COM4',
		'COM5',
		'COM6',
		'COM7',
		'COM8',
		'COM9',
		'LPT1',
		'LPT2',
		'LPT3',
		'LPT4',
		'LPT5',
		'LPT6',
		'LPT7',
		'LPT8',
		'LPT9'
	];

	if (reservedNames.includes(cleanWord.toUpperCase())) {
		cleanWord = `_${cleanWord}_`;
	}

	return cleanWord || 'Untitled';
}

/**
 * Parse a version number from a filename
 *
 * @param filename The filename to parse
 * @param prefix The prefix to match (e.g., "AABB")
 * @returns The version number or 0 if not found
 */
export function parseVersionNumber(filename: string, prefix: string): number {
	if (!filename) return 0;

	// Create a regex pattern to match the prefix followed by _v and a number
	// This will match patterns like "AABB_v1.png", "AABB_v23.png", etc.
	const pattern = new RegExp(`^${prefix}_v(\\d+)\\.[a-zA-Z]+$`);
	const match = filename.match(pattern);

	if (match && match[1]) {
		const version = parseInt(match[1], 10);
		return isNaN(version) ? 0 : version;
	}

	return 0;
}

/**
 * Get the next version number for a file
 *
 * @param files Array of filenames
 * @param prefix The prefix to match (e.g., "AABB")
 * @returns The next version number (starting from 1)
 */
export function getNextVersionNumber(files: string[], prefix: string): number {
	if (!files || files.length === 0) return 1;

	// Parse version numbers from all matching files
	const versions = files
		.map((filename) => parseVersionNumber(filename, prefix))
		.filter((version) => version > 0);

	// If no valid versions found, start with 1
	if (versions.length === 0) return 1;

	// Find the highest version number and increment by 1
	return Math.max(...versions) + 1;
}
