// src/lib/components/SequenceWorkbench/BeatFrame/beatFrameHelpers.ts

export type LayoutDict = Record<string, [number, number]>;

export async function fetchDefaultLayouts(url: string): Promise<LayoutDict> {
	try {
		const resp = await fetch(url);
		if (!resp.ok) throw new Error(`Failed to fetch layouts from ${url}`);
		const data: LayoutDict = await resp.json();
		return data;
	} catch (err) {
		console.error('fetchDefaultLayouts error =>', err);
		// Return an empty dictionary so the caller can fallback
		return {};
	}
}

export function applyLayout(
	defaultLayouts: LayoutDict,
	beatCount: number,
	fallback: [number, number] = [4, 4]
): [number, number] {
	const key = String(beatCount);
	if (defaultLayouts[key]) {
		return defaultLayouts[key];
	}
	return fallback;
}

/**
 * Calculate the optimal cell size for the beat frame grid
 * @param beatCount Number of beats in the sequence
 * @param containerWidth Width of the container
 * @param containerHeight Height of the container
 * @param totalRows Number of rows in the grid
 * @param totalCols Number of columns in the grid
 * @param gap Gap between cells
 * @returns Optimal cell size in pixels
 */
export function calculateCellSize(
	beatCount: number,
	containerWidth: number,
	containerHeight: number,
	totalRows: number,
	totalCols: number,
	gap: number
): number {
	// Minimum cell size thresholds - pictographs won't shrink below these values
	// Instead, scrollbars will appear when content would need to be smaller
	const MIN_CELL_SIZE_FULLSCREEN = 100; // Minimum size in fullscreen mode
	const MIN_CELL_SIZE_NORMAL = 70; // Minimum size in normal mode

	// Ensure we have valid dimensions
	if (containerWidth <= 0 || containerHeight <= 0 || totalRows <= 0 || totalCols <= 0) {
		return 80; // Default fallback size - increased for better readability
	}

	// Detect if we're in fullscreen mode by checking container dimensions
	// Fullscreen containers are typically much larger
	const isLikelyFullscreen = containerWidth > 800 && containerHeight > 600;

	// Set the minimum cell size based on mode
	const minCellSize = isLikelyFullscreen ? MIN_CELL_SIZE_FULLSCREEN : MIN_CELL_SIZE_NORMAL;

	// Calculate total space needed for gaps
	const totalGapWidth = gap * (totalCols - 1);
	const totalGapHeight = gap * (totalRows - 1);

	// Calculate available space after accounting for gaps and padding
	// Reduce horizontal padding to use more space, keep vertical padding for safety
	const horizontalPadding = beatCount === 0 ? containerWidth * 0.05 : 10; // Reduced from 24 to 10px
	const verticalPadding = 24; // Keep vertical padding to prevent overflow
	const availableWidth = Math.max(0, containerWidth - totalGapWidth - horizontalPadding * 2);
	const availableHeight = Math.max(0, containerHeight - totalGapHeight - verticalPadding * 2);

	// Calculate cell size based on available space in both dimensions
	const cellWidthByContainer = Math.floor(availableWidth / totalCols);
	const cellHeightByContainer = Math.floor(availableHeight / totalRows);

	// Use the smaller dimension to maintain square cells and preserve aspect ratio
	const baseSize = Math.min(cellWidthByContainer, cellHeightByContainer);

	// Apply a scaling factor to ensure pictographs fit within cells
	// This scaling factor ensures pictographs are slightly smaller than their containers
	const scalingFactor = 0.92; // Reduce size by only 8% (was 15%)
	const scaledBaseSize = Math.floor(baseSize * scalingFactor);

	// For start position only, make it proportionally larger
	const cellSize = beatCount === 0 ? scaledBaseSize * 1.1 : scaledBaseSize;

	// Check if the calculated cell size is below the minimum threshold
	// If so, use the minimum size instead - this will cause overflow and enable scrollbars
	if (cellSize < minCellSize) {
		console.debug('Cell size below minimum threshold, using minimum size instead:', {
			calculatedSize: cellSize,
			minCellSize,
			totalRows,
			totalCols,
			containerWidth,
			containerHeight
		});

		// Apply different constraints based on mode
		if (isLikelyFullscreen) {
			return Math.min(Math.max(minCellSize, MIN_CELL_SIZE_FULLSCREEN), 200); // Min 100px, Max 200px for fullscreen
		} else {
			return Math.min(Math.max(minCellSize, MIN_CELL_SIZE_NORMAL), 160); // Min 80px, Max 160px for normal view
		}
	}

	// Apply different constraints based on mode
	if (isLikelyFullscreen) {
		// In fullscreen, allow larger cells but ensure they're not too large
		// This helps ensure pictographs are displayed side by side correctly
		return Math.min(Math.max(cellSize, MIN_CELL_SIZE_FULLSCREEN), 200); // Min 100px, Max 200px for fullscreen
	} else {
		// In normal mode, use more conservative constraints but allow larger cells
		return Math.min(Math.max(cellSize, MIN_CELL_SIZE_NORMAL), 160); // Min 80px, Max 160px for normal view
	}
}

const beatCountGridMap: Record<number, [number, number]> = {
	1: [1, 1], // One beat + start position
	2: [1, 2],
	3: [1, 3],
	4: [1, 4],
	5: [2, 4],
	6: [2, 4],
	7: [2, 4],
	8: [2, 4],
	9: [3, 4],
	10: [3, 4],
	11: [3, 4],
	12: [3, 4],
	13: [4, 4],
	14: [4, 4],
	15: [4, 4],
	16: [4, 4],
	17: [5, 4],
	18: [5, 4],
	19: [5, 4],
	20: [5, 4],
	21: [6, 4],
	22: [6, 4],
	23: [6, 4],
	24: [6, 4],
	25: [7, 4],
	26: [7, 4],
	27: [7, 4],
	28: [7, 4],
	29: [8, 4],
	30: [8, 4],
	31: [8, 4],
	32: [8, 4]
};

export function autoAdjustLayout(beatCount: number): [number, number] {
	// For empty sequence or only start position, use single column layout
	if (beatCount <= 0) return [1, 1];
	if (beatCount === 1) return [1, 1]; // Single beat + start position

	// Use predefined layouts for common beat counts
	if (beatCount <= 32 && beatCountGridMap[beatCount]) {
		return beatCountGridMap[beatCount];
	}

	// Default layout for larger sequences
	const cols = 4;
	const rows = Math.ceil(beatCount / cols);
	return [rows, cols];
}

/**
 * Verifies that BeatFrame elements are fully loaded and ready for rendering
 * @returns boolean indicating if BeatFrame elements are ready
 */
export function verifyBeatFrameElements(): boolean {
	const beatFrameElement = document.querySelector('.beat-frame-container');
	if (!beatFrameElement) {
		console.log('⚠️ BeatFrame element not found during verification');
		return false;
	}

	// Check for SVG elements
	const svgElements = beatFrameElement.querySelectorAll('svg');
	console.log(`🔍 BeatFrame verification: Found ${svgElements.length} SVG elements`);

	// Check for arrows and other critical elements
	const arrowElements = beatFrameElement.querySelectorAll('.arrow-path, .arrow-head');
	const propElements = beatFrameElement.querySelectorAll('.pictograph-prop');

	console.log(`🔍 BeatFrame verification details:`, {
		svgCount: svgElements.length,
		arrowCount: arrowElements.length,
		propCount: propElements.length
	});

	// Consider it valid if we have SVGs and either arrows or props
	return svgElements.length > 0 && (arrowElements.length > 0 || propElements.length > 0);
}

/**
 * Creates a temporary element for rendering the BeatFrame
 * @param width Width of the temporary element
 * @param height Height of the temporary element
 * @returns The created temporary element
 */
export function createTemporaryRenderElement(width: number, height: number): HTMLDivElement {
	const tempElement = document.createElement('div');
	tempElement.style.position = 'absolute';
	tempElement.style.left = '-9999px';
	tempElement.style.width = `${width}px`;
	tempElement.style.height = `${height}px`;
	tempElement.className = 'temp-beat-frame-clone';
	document.body.appendChild(tempElement);
	return tempElement;
}

/**
 * Clones the BeatFrame content into a temporary element for rendering
 * @param tempElement The temporary element to clone into
 * @returns boolean indicating success
 */
export function cloneBeatFrameContent(tempElement: HTMLDivElement): boolean {
	const beatFrameElement = document.querySelector('.beat-frame-container');
	if (!beatFrameElement) {
		console.error('Could not find BeatFrame element in the DOM');
		return false;
	}

	// Clone the BeatFrame content into our temporary element
	tempElement.innerHTML = beatFrameElement.innerHTML;

	// Force a layout calculation to ensure all elements are properly rendered
	tempElement.getBoundingClientRect();

	// Ensure SVG elements are properly cloned and visible
	const clonedSvgs = tempElement.querySelectorAll('svg');
	clonedSvgs.forEach((svg) => {
		// Ensure SVG has proper dimensions
		if (!svg.getAttribute('width') || svg.getAttribute('width') === '0') {
			svg.setAttribute('width', '100%');
		}
		if (!svg.getAttribute('height') || svg.getAttribute('height') === '0') {
			svg.setAttribute('height', '100%');
		}
		// Force visibility
		svg.style.visibility = 'visible';
		svg.style.display = 'block';
	});

	return clonedSvgs.length > 0;
}

/**
 * Logs detailed information about the BeatFrame element
 */
export function logBeatFrameDetails(): void {
	const beatFrameElement = document.querySelector('.beat-frame-container');
	if (!beatFrameElement) {
		console.error('Could not find BeatFrame element in the DOM');
		return;
	}

	// Verify BeatFrame has necessary elements
	const svgElements = beatFrameElement.querySelectorAll('svg');
	const arrowElements = beatFrameElement.querySelectorAll('.arrow-path, .arrow-head');
	const propElements = beatFrameElement.querySelectorAll('.pictograph-prop');

	// Log detailed information about what we found
	console.log('Found BeatFrame element with details:', {
		element: beatFrameElement,
		svgCount: svgElements.length,
		arrowCount: arrowElements.length,
		propCount: propElements.length,
		html: beatFrameElement.innerHTML.substring(0, 200) + '...' // Log a preview of the HTML
	});

	// Warn if we're missing expected elements
	if (svgElements.length === 0 || (arrowElements.length === 0 && propElements.length === 0)) {
		console.warn('⚠️ BeatFrame may be missing critical elements for rendering');
	}
}

/**
 * Removes a temporary element from the DOM
 * @param element The element to remove
 */
export function removeTemporaryElement(element: HTMLDivElement): void {
	if (element && element.parentNode) {
		document.body.removeChild(element);
	}
}

/**
 * Calculate a hash of the current settings and sequence state
 * @param settingsSnapshot The settings snapshot
 * @param sequenceSnapshot The sequence snapshot
 * @returns A string hash
 */
export function calculateSettingsHash(
	settingsSnapshot: Record<string, any>,
	sequenceSnapshot: Record<string, any>
): string {
	// Use our stable derived values to prevent unnecessary recalculations
	const hashInput = JSON.stringify({
		...settingsSnapshot,
		sequenceLength: sequenceSnapshot.beatsLength,
		sequenceTitle: sequenceSnapshot.title,
		difficultyLevel: sequenceSnapshot.difficulty,
		hasStartPosition: sequenceSnapshot.hasStartPosition
	});

	// Simple hash function
	let hash = 0;
	for (let i = 0; i < hashInput.length; i++) {
		const char = hashInput.charCodeAt(i);
		hash = (hash << 5) - hash + char;
		hash = hash & hash; // Convert to 32bit integer
	}
	return hash.toString();
}
