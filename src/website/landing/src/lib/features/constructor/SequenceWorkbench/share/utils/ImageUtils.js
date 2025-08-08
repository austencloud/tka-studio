// Image utility functions
export function dataURLtoBlob(dataURL) {
  const arr = dataURL.split(",");
  const mime = arr[0].match(/:(.*?);/)[1];
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);
  while (n--) {
    u8arr[n] = bstr.charCodeAt(n);
  }
  return new Blob([u8arr], { type: mime });
}

export function blobToDataURL(blob) {
  return new Promise((resolve) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.readAsDataURL(blob);
  });
}

export function resizeImage(dataURL, maxWidth = 800, maxHeight = 600) {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");

      // Calculate new dimensions
      let { width, height } = img;
      if (width > maxWidth) {
        height = (height * maxWidth) / width;
        width = maxWidth;
      }
      if (height > maxHeight) {
        width = (width * maxHeight) / height;
        height = maxHeight;
      }

      canvas.width = width;
      canvas.height = height;
      ctx.drawImage(img, 0, 0, width, height);
      resolve(canvas.toDataURL("image/png"));
    };
    img.src = dataURL;
  });
}

/**
 * Create a File object from a data URL
 * @param {string} dataURL - The data URL to convert
 * @param {string} filename - The filename for the file
 * @param {string} mimeType - Optional MIME type (will be extracted from data URL if not provided)
 * @returns {File} File object
 */
export function createFileFromDataURL(dataURL, filename, mimeType = null) {
  // Extract MIME type from data URL if not provided
  if (!mimeType) {
    const match = dataURL.match(/data:([^;]+)/);
    mimeType = match ? match[1] : "application/octet-stream";
  }

  // Convert data URL to blob first
  const blob = dataURLtoBlob(dataURL);

  // Create File object from blob
  return new File([blob], filename, { type: mimeType });
}

/**
 * Create a File object from a blob
 * @param {Blob} blob - The blob to convert
 * @param {string} filename - The filename for the file
 * @param {string} mimeType - Optional MIME type (will use blob type if not provided)
 * @returns {File} File object
 */
export function createFileFromBlob(blob, filename, mimeType = null) {
  return new File([blob], filename, { type: mimeType || blob.type });
}

/**
 * Get image dimensions from data URL
 * @param {string} dataURL - The data URL to analyze
 * @returns {Promise<{width: number, height: number}>} Image dimensions
 */
export function getImageDimensions(dataURL) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => {
      resolve({ width: img.width, height: img.height });
    };
    img.onerror = () => {
      reject(new Error("Failed to load image"));
    };
    img.src = dataURL;
  });
}

/**
 * Convert image to different format
 * @param {string} dataURL - Source image data URL
 * @param {string} format - Target format ('image/png', 'image/jpeg', 'image/webp')
 * @param {number} quality - Quality for lossy formats (0-1)
 * @returns {Promise<string>} Converted image data URL
 */
export function convertImageFormat(
  dataURL,
  format = "image/png",
  quality = 0.9
) {
  return new Promise((resolve) => {
    const img = new Image();
    img.onload = () => {
      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");

      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);

      resolve(canvas.toDataURL(format, quality));
    };
    img.src = dataURL;
  });
}
