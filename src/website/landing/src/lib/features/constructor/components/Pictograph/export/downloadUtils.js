/**
 * Download utilities for TKA Constructor
 * Provides functionality for downloading images and files
 */

/**
 * @typedef {Object} DownloadResult
 * @property {boolean} success - Whether the download was successful
 * @property {string} [message] - Success or error message
 * @property {string} [filename] - The filename that was downloaded
 * @property {Error} [error] - Error object if download failed
 */

/**
 * Download an image from a data URL or blob
 * @param {string|Blob} imageData - Image data URL or blob
 * @param {string} filename - Filename for the download
 * @param {Object} [options] - Download options
 * @returns {Promise<DownloadResult>} Download result
 */
export async function downloadImage(imageData, filename, options = {}) {
  try {
    let blob;

    // Convert data URL to blob if needed
    if (typeof imageData === 'string') {
      if (imageData.startsWith('data:')) {
        blob = dataURLToBlob(imageData);
      } else {
        throw new Error('Invalid image data format');
      }
    } else if (imageData instanceof Blob) {
      blob = imageData;
    } else {
      throw new Error('Image data must be a data URL string or Blob');
    }

    // Create download link
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;

    // Trigger download
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // Clean up
    URL.revokeObjectURL(url);

    return {
      success: true,
      message: 'Image downloaded successfully',
      filename: filename
    };

  } catch (error) {
    console.error('Download failed:', error);
    return {
      success: false,
      message: `Download failed: ${error.message}`,
      error: error
    };
  }
}

/**
 * Convert data URL to Blob
 * @param {string} dataURL - Data URL string
 * @returns {Blob} Blob object
 */
function dataURLToBlob(dataURL) {
  const parts = dataURL.split(',');
  const header = parts[0];
  const data = parts[1];

  const mimeMatch = header.match(/data:([^;]+)/);
  const mime = mimeMatch ? mimeMatch[1] : 'application/octet-stream';

  const isBase64 = header.includes('base64');
  let bytes;

  if (isBase64) {
    bytes = atob(data);
  } else {
    bytes = decodeURIComponent(data);
  }

  const uint8Array = new Uint8Array(bytes.length);
  for (let i = 0; i < bytes.length; i++) {
    uint8Array[i] = bytes.charCodeAt(i);
  }

  return new Blob([uint8Array], { type: mime });
}

/**
 * Download text content as a file
 * @param {string} content - Text content to download
 * @param {string} filename - Filename for the download
 * @param {string} [mimeType] - MIME type for the file
 * @returns {Promise<DownloadResult>} Download result
 */
export async function downloadText(content, filename, mimeType = 'text/plain') {
  try {
    const blob = new Blob([content], { type: mimeType });
    return await downloadImage(blob, filename);
  } catch (error) {
    console.error('Text download failed:', error);
    return {
      success: false,
      message: `Text download failed: ${error.message}`,
      error: error
    };
  }
}

/**
 * Download JSON data as a file
 * @param {Object} data - Data to download as JSON
 * @param {string} filename - Filename for the download
 * @returns {Promise<DownloadResult>} Download result
 */
export async function downloadJSON(data, filename) {
  try {
    const jsonString = JSON.stringify(data, null, 2);
    return await downloadText(jsonString, filename, 'application/json');
  } catch (error) {
    console.error('JSON download failed:', error);
    return {
      success: false,
      message: `JSON download failed: ${error.message}`,
      error: error
    };
  }
}

/**
 * Check if downloads are supported in the current browser
 * @returns {boolean} True if downloads are supported
 */
export function isDownloadSupported() {
  return typeof document !== 'undefined' &&
         'createElement' in document &&
         'createObjectURL' in URL;
}
