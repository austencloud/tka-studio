/**
 * SVG to Image conversion utility
 * Converts SVG strings to HTMLImageElement for canvas rendering
 */

/**
 * Convert SVG string to HTMLImageElement
 */
export function svgStringToImage(
  svgString: string,
  width: number,
  height: number,
): Promise<HTMLImageElement> {
  return new Promise((resolve, reject) => {
    const img = new Image();

    img.onload = () => {
      resolve(img);
    };

    img.onerror = (error) => {
      reject(new Error(`Failed to load SVG image: ${error}`));
    };

    // Create blob URL from SVG string
    const blob = new Blob([svgString], { type: "image/svg+xml" });
    const url = URL.createObjectURL(blob);

    // Set image source
    img.src = url;

    // Clean up blob URL after image loads
    img.onload = () => {
      URL.revokeObjectURL(url);
      resolve(img);
    };
  });
}
