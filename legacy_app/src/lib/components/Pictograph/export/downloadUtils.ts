/**
 * Download Utilities
 *
 * This module provides utilities for downloading images.
 */

import { browser } from '$app/environment';
import { logger } from '$lib/core/logging';

/**
 * Options for downloading an image
 */
export interface DownloadOptions {
	dataUrl: string;
	filename: string;
	mimeType?: string;
}

/**
 * Result of downloading an image
 */
export interface DownloadResult {
	success: boolean;
	filePath?: string;
	fileName?: string;
	folderPath?: string;
}

/**
 * Downloads an image from a data URL
 *
 * @param options Download options
 * @returns Promise resolving to a DownloadResult object
 */
export async function downloadImage(options: DownloadOptions): Promise<DownloadResult> {
	// Validate environment
	if (!browser) {
		return Promise.reject(new Error('Cannot download: not in browser environment'));
	}

	try {
		console.log(`DownloadUtils: Downloading image as "${options.filename}"`);
		console.log(`DownloadUtils: Data URL length: ${options.dataUrl.length}`);

		// Validate the data URL format
		if (!options.dataUrl || !options.dataUrl.startsWith('data:')) {
			throw new Error('Invalid data URL format');
		}

		// Extract MIME type from data URL if not provided
		const mimeType =
			options.mimeType || options.dataUrl.split(',')[0].match(/:(.*?);/)?.[1] || 'image/png';

		console.log(`DownloadUtils: Using MIME type: ${mimeType}`);

		// Try to use the File System Access API for a better download experience
		if (window.showSaveFilePicker) {
			try {
				// Convert data URL to Blob
				const blob = dataURLtoBlob(options.dataUrl);
				console.log(`DownloadUtils: Created blob of size: ${blob.size} bytes`);

				// Set up options for the save dialog - removed 'mode' property which was causing issues
				const opts = {
					suggestedName: options.filename,
					types: [
						{
							description: 'Image Files',
							accept: {
								'image/png': ['.png'],
								'image/jpeg': ['.jpg', '.jpeg']
							}
						}
					],
					// Try to default to Downloads folder
					startIn: 'downloads' as
						| 'desktop'
						| 'documents'
						| 'downloads'
						| 'music'
						| 'pictures'
						| 'videos'
				};

				console.log(`DownloadUtils: Opening save dialog with options:`, opts);

				try {
					// Show the save file picker
					const fileHandle = await window.showSaveFilePicker(opts);
					console.log(`DownloadUtils: User selected file:`, fileHandle);

					try {
						// Create a writable stream
						const writable = await fileHandle.createWritable();

						try {
							// Write the blob to the file
							await writable.write(blob);

							// Close the file
							await writable.close();

							// Get the folder path from the file handle
							let folderPath = 'Downloads'; // Default to Downloads folder
							let fileName = options.filename;

							try {
								// Try to get the file path if available
								// @ts-ignore - This is a non-standard property that might be available in some browsers
								if (fileHandle.name) {
									fileName = fileHandle.name;
								}

								// Try to get the folder path using multiple approaches

								// Approach 1: Try to get the directory handle name
								// @ts-ignore - This is a non-standard property that might be available in some browsers
								if (fileHandle.directoryHandle && fileHandle.directoryHandle.name) {
									// @ts-ignore
									folderPath = fileHandle.directoryHandle.name;
									console.log(
										'DownloadUtils: Got folder path from directoryHandle.name:',
										folderPath
									);
								}

								// Approach 2: Try to get the parent directory from the file path
								// @ts-ignore - This is a non-standard property that might be available in some browsers
								else if (fileHandle.path) {
									// @ts-ignore
									const path = fileHandle.path;
									const lastSlashIndex = path.lastIndexOf('/');
									if (lastSlashIndex > 0) {
										folderPath = path.substring(0, lastSlashIndex);
										console.log('DownloadUtils: Got folder path from fileHandle.path:', folderPath);
									}
								}

								// Approach 3: Try to use the File System API to get the parent directory
								// @ts-ignore - This is a non-standard property that might be available in some browsers
								else if (fileHandle.getParentDirectory) {
									try {
										// @ts-ignore
										const parentDir = await fileHandle.getParentDirectory();
										if (parentDir && parentDir.name) {
											folderPath = parentDir.name;
											console.log(
												'DownloadUtils: Got folder path from getParentDirectory():',
												folderPath
											);
										}
									} catch (parentDirError) {
										console.warn('DownloadUtils: Error getting parent directory:', parentDirError);
									}
								}

								// If we still don't have a folder path, use a default
								if (!folderPath) {
									folderPath = 'Downloads'; // Default to Downloads folder
									console.log('DownloadUtils: Using default Downloads folder path');
								}
							} catch (pathError) {
								console.warn('DownloadUtils: Could not get file path details:', pathError);
								// Ensure we have a default folder path
								folderPath = 'Downloads';
							}

							console.log(`DownloadUtils: File saved successfully to ${folderPath}/${fileName}`);
							return {
								success: true,
								fileName,
								folderPath,
								filePath: folderPath ? `${folderPath}/${fileName}` : undefined
							};
						} catch (writeError) {
							console.error('DownloadUtils: Error writing to file:', writeError);
							throw writeError;
						}
					} catch (writableError) {
						console.error('DownloadUtils: Error creating writable stream:', writableError);
						throw writableError;
					}
				} catch (pickerError) {
					// Check if this is a user cancellation
					if (
						pickerError instanceof Error &&
						(pickerError.name === 'AbortError' ||
							pickerError.message.includes('user aborted') ||
							pickerError.message.includes('cancelled') ||
							pickerError.message.includes('canceled'))
					) {
						console.log('DownloadUtils: User cancelled the save dialog');
						throw new Error('USER_CANCELLED_OPERATION');
					}

					console.error('DownloadUtils: Error with save file picker:', pickerError);
					throw pickerError;
				}
			} catch (fsaError) {
				// Check if this is a user cancellation (AbortError)
				if (
					fsaError instanceof Error &&
					(fsaError.name === 'AbortError' ||
						fsaError.message.includes('user aborted') ||
						fsaError.message.includes('cancelled') ||
						fsaError.message.includes('canceled'))
				) {
					console.log('DownloadUtils: User cancelled the save dialog');
					// Throw a standardized cancellation error that can be caught by the caller
					throw new Error('USER_CANCELLED_OPERATION');
				}

				// Log the specific error for debugging
				console.warn(
					'DownloadUtils: File System Access API failed:',
					fsaError instanceof Error ? fsaError.message : String(fsaError),
					fsaError
				);

				// Add more detailed logging to help diagnose the issue
				if (fsaError instanceof Error) {
					console.warn('Error name:', fsaError.name);
					console.warn('Error message:', fsaError.message);
					console.warn('Error stack:', fsaError.stack);
				}

				// Fall through to traditional approach for other errors
			}
		} else {
			console.log(
				`DownloadUtils: File System Access API not supported, using traditional approach`
			);
		}

		// Traditional download approach using a link element
		try {
			// Convert data URL to Blob using the dataURLtoBlob function
			const blob = dataURLtoBlob(options.dataUrl);
			console.log(`DownloadUtils: Created blob of size: ${blob.size} bytes`);

			// Create object URL from blob
			const url = URL.createObjectURL(blob);
			console.log(`DownloadUtils: Created object URL: ${url}`);

			// Create download link
			const link = document.createElement('a');
			link.href = url;
			link.download = options.filename;
			link.style.display = 'none';

			// Add to DOM
			document.body.appendChild(link);

			// Force a layout calculation to ensure the link is in the DOM
			link.getBoundingClientRect();

			// Longer delay to ensure the browser is ready
			await new Promise((resolve) => setTimeout(resolve, 100));

			// Trigger click with a try/catch to handle any browser restrictions
			try {
				console.log(`DownloadUtils: Clicking download link`);
				link.click();
				console.log(`DownloadUtils: Download link clicked`);
			} catch (clickError) {
				console.error(`DownloadUtils: Error clicking link:`, clickError);
				throw clickError;
			}

			// Clean up with a longer timeout
			setTimeout(() => {
				if (document.body.contains(link)) {
					document.body.removeChild(link);
				}
				URL.revokeObjectURL(url);
				console.log(`DownloadUtils: Cleaned up resources`);
			}, 500);

			// For traditional download, we can't get the exact path
			// But we can provide the filename
			return {
				success: true,
				fileName: options.filename,
				// For browser downloads, typically goes to Downloads folder
				folderPath: 'Downloads'
			};
		} catch (linkError) {
			console.warn(
				'DownloadUtils: Traditional approach failed, trying alternative method',
				linkError
			);

			// Try an alternative approach using window.open
			try {
				// Create a new window/tab with the image
				const newWindow = window.open();
				if (!newWindow) {
					throw new Error('Failed to open new window. Popup might be blocked.');
				}

				// Add null check before accessing properties on newWindow
				if (newWindow.document) {
					// Create HTML content for the new window
					const htmlContent = `
						<html>
							<head>
								<title>${options.filename}</title>
								<style>
									body { margin: 0; display: flex; justify-content: center; align-items: center; height: 100vh; background: #f0f0f0; }
									img { max-width: 100%; max-height: 100%; }
									.download-instructions { position: fixed; top: 10px; left: 0; right: 0; text-align: center; background: rgba(0,0,0,0.7); color: white; padding: 10px; }
								</style>
							</head>
							<body>
								<div class="download-instructions">Right-click on the image and select "Save Image As..." to download</div>
								<img src="${options.dataUrl}" alt="${options.filename}">
							</body>
						</html>
					`;

					// Use a modern approach to avoid the deprecated document.write
					try {
						// Open a new document and set its content type
						newWindow.document.open('text/html', 'replace');

						// Insert the HTML content
						// @ts-ignore - TypeScript doesn't like this but it's the recommended way
						newWindow.document.documentElement.innerHTML = htmlContent.trim();

						// Close the document to finish loading
						newWindow.document.close();
					} catch (docError) {
						// Fallback to the old method if the modern approach fails
						console.warn('DownloadUtils: Modern document writing failed, using fallback', docError);
						newWindow.document.open();
						// @ts-ignore - Suppress the deprecation warning
						newWindow.document.write(htmlContent);
						newWindow.document.close();
					}
				}

				return {
					success: true,
					fileName: options.filename,
					folderPath: 'Browser Tab' // This is opened in a new tab
				};
			} catch (windowError) {
				console.error('DownloadUtils: Alternative approach failed', windowError);

				// Last resort: direct data URL approach
				const link = document.createElement('a');
				link.href = options.dataUrl;
				link.download = options.filename;
				link.target = '_blank';
				link.style.display = 'none';

				document.body.appendChild(link);
				await new Promise((resolve) => setTimeout(resolve, 100));
				link.click();

				setTimeout(() => {
					if (document.body.contains(link)) {
						document.body.removeChild(link);
					}
				}, 500);

				return {
					success: true,
					fileName: options.filename,
					folderPath: 'Downloads' // Last resort method typically saves to Downloads
				};
			}
		}
	} catch (error) {
		// Log detailed error information
		logger.error('Error downloading image', {
			error: error instanceof Error ? error : new Error(String(error))
		});

		// Re-throw the error
		throw new Error(
			`Failed to download image: ${error instanceof Error ? error.message : String(error)}`
		);
	}
}

/**
 * Converts a data URL to a Blob
 *
 * @param dataUrl The data URL to convert
 * @returns The resulting Blob
 */
export function dataURLtoBlob(dataUrl: string): Blob {
	// Split the data URL into the data and MIME type
	const arr = dataUrl.split(',');
	const mimeMatch = arr[0].match(/:(.*?);/);
	if (!mimeMatch || !mimeMatch[1]) {
		throw new Error('Invalid data URL format');
	}
	const mime = mimeMatch[1];
	const bstr = atob(arr[1]);
	let n = bstr.length;
	const u8arr = new Uint8Array(n);

	// Convert to Uint8Array
	while (n--) {
		u8arr[n] = bstr.charCodeAt(n);
	}

	// Create and return Blob
	return new Blob([u8arr], { type: mime });
}
