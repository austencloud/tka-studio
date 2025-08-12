/**
 * Converts an SVG string to an HTMLImageElement with comprehensive sanitization.
 *
 * @param svg - SVG markup as string
 * @param width - Optional width for the image
 * @param height - Optional height for the image
 * @param timeout - Optional timeout in ms (defaults to 5000ms)
 * @returns Promise<HTMLImageElement>
 */
export function svgStringToImage(
	svg: string,
	width?: number,
	height?: number,
	timeout = 5000
): Promise<HTMLImageElement> {
	return new Promise((resolve, reject) => {
		// Input validation
		if (typeof svg !== 'string' || !svg.trim().startsWith('<svg')) {
			reject(new Error('Invalid SVG string.'));
			return;
		}

		try {
			// Comprehensive SVG sanitization
			// Remove high-risk elements and attributes
			const safeSvg = svg
				// Remove script tags
				.replace(/<script[\s\S]*?>[\s\S]*?<\/script>/gi, '')
				// Remove event handlers (on*)
				.replace(/\son\w+\s*=\s*(['"]).*?\1/gi, '')
				// Remove javascript: URLs
				.replace(/(?:href|xlink:href|src)=(['"])javascript:.*?\1/gi, '')
				// Remove data: URLs (commonly used in XSS)
				.replace(/(?:href|xlink:href|src)=(['"])data:(?!image\/svg\+xml).*?\1/gi, '')
				// Remove use of external entities
				.replace(/<!ENTITY\s+\w+\s+(?:PUBLIC|SYSTEM).*?>/gi, '')
				// Remove inline event handlers from animations
				.replace(/<(?:set|animate)(?:\s+[^>]*?)(?:\s+begin\s*=\s*['"].+?['"])/gi, (match) =>
					match.replace(/begin\s*=\s*(['"])(?:.*?click.*?|.*?mouseover.*?)\1/gi, '')
				);

			// Create a data URL using modern encoding methods
			const encoded =
				'data:image/svg+xml;base64,' +
				btoa(
					encodeURIComponent(safeSvg).replace(/%([0-9A-F]{2})/g, (_match, p1) =>
						String.fromCharCode(parseInt(p1, 16))
					)
				);

			// Create the image
			// Check if window is defined (browser environment)
			if (typeof window === 'undefined') {
				throw new Error('This function requires a browser environment with a window object');
			}

			const img = new window.Image(width, height);

			// Set up timeout to prevent hanging
			const timeoutId = setTimeout(() => {
				img.onload = null;
				img.onerror = null;
				reject(new Error('SVG loading timed out after ' + timeout + 'ms.'));
			}, timeout);

			// Handle successful load
			img.onload = () => {
				clearTimeout(timeoutId);
				resolve(img);
			};

			// Handle error with detail
			img.onerror = (err) => {
				clearTimeout(timeoutId);
				reject(
					new Error(
						'Failed to load SVG as image: ' + (err instanceof Error ? err.message : 'Unknown error')
					)
				);
			};

			// Set source to trigger loading
			img.src = encoded;
		} catch (err) {
			reject(
				new Error('SVG processing error: ' + (err instanceof Error ? err.message : String(err)))
			);
		}
	});
}
