/**
 * Enhanced foldable device detection utility
 * Provides comprehensive detection for foldable devices with a focus on Samsung Z Fold series
 */

// --- Constants ---
// Enable debug logging via URL parameter (e.g., ?debug=foldable)
const DEBUG_MODE =
	typeof window !== 'undefined' && window.location.search.includes('debug=foldable');

// Device specification configuration
// NOTE: Keep these dimensions updated as new devices are released or tested
const FOLDABLE_DEVICE_SPECS = {
	zfold3: {
		models: ['SM-F926'],
		foldedDimensions: { width: { min: 350, max: 400 }, height: { min: 800, max: 900 } },
		unfoldedDimensions: { width: { min: 700, max: 800 }, height: { min: 800, max: 900 } }
	},
	zfold4: {
		models: ['SM-F936'],
		foldedDimensions: { width: { min: 350, max: 400 }, height: { min: 800, max: 900 } },
		unfoldedDimensions: { width: { min: 700, max: 800 }, height: { min: 800, max: 900 } }
	},
	zfold5: {
		models: ['SM-F946'],
		foldedDimensions: { width: { min: 350, max: 400 }, height: { min: 800, max: 900 } },
		unfoldedDimensions: { width: { min: 700, max: 820 }, height: { min: 800, max: 920 } }
	},
	zfold6: {
		models: ['SM-F956'], // Example model, update if needed
		foldedDimensions: { width: { min: 350, max: 410 }, height: { min: 800, max: 950 } }, // Estimated
		unfoldedDimensions: { width: { min: 800, max: 850 }, height: { min: 680, max: 750 } } // Based on previous user log
	}
	// Add other known foldable specs here (e.g., Pixel Fold)
};


// --- Interfaces ---
export interface FoldableDetectionResult {
	isFoldable: boolean;
	isUnfolded: boolean;
	foldableType: 'zfold' | 'other' | 'unknown';
	confidence: number; // Confidence score (0 to 1)
	detectionMethod?: string; // How the detection was made
}


// --- Main Detection Function ---
/**
 * Detects if the current device is likely foldable and its state.
 * Prioritizes manual overrides, then device spec matching, then APIs,
 * then User Agent checks, and finally a dimension heuristic as a fallback.
 * @returns {FoldableDetectionResult} Object containing detection results.
 */
export function detectFoldableDevice(): FoldableDetectionResult {
	// Check for manual override first (most reliable if set)
	const manualOverride = checkManualOverride();
	if (manualOverride) {
		if (DEBUG_MODE) console.log('Foldable Detect: Using Manual Override', manualOverride);
		return manualOverride;
	}

	// Default result (not foldable)
	let finalResult: FoldableDetectionResult = {
		isFoldable: false,
		isUnfolded: false,
		foldableType: 'unknown',
		confidence: 0,
		detectionMethod: 'none'
	};

	// Ensure code only runs in a browser environment
	if (typeof window === 'undefined' || typeof navigator === 'undefined') {
		console.warn('Foldable Detect: Cannot run outside browser environment.');
		return finalResult;
	}

	// --- Gather Environment Info ---
	const ua = navigator.userAgent;
	const windowW = window.innerWidth;
	const windowH = window.innerHeight;
	const pixelRatio = window.devicePixelRatio;
	const aspectRatio = windowW / windowH;

	if (DEBUG_MODE) {
		console.log('Foldable Detect: UA:', ua);
		console.log('Foldable Detect: Window WxH:', windowW, 'x', windowH);
		console.log('Foldable Detect: DPR:', pixelRatio);
		console.log('Foldable Detect: Aspect Ratio:', aspectRatio.toFixed(3));
	}

	// --- Detection Logic Pipeline ---

	// 1. Device Specification Matching (High Confidence)
	let specMatchFound = checkAgainstDeviceSpecs(ua, windowW, windowH, finalResult);
	if (specMatchFound) {
		if (DEBUG_MODE) console.log('Foldable Detect: Result from Spec Match', finalResult);
		saveDetectionResult(finalResult); // Save confident result
		return finalResult;
	}

	// 2. Screen Spanning / Window Segments APIs (High Confidence)
	const isScreenSpanning =
		window.matchMedia('(screen-spanning: single-fold-vertical)').matches ||
		window.matchMedia('(screen-spanning: single-fold-horizontal)').matches;
	let segmentCount = 0;
	try {
		// @ts-ignore - Experimental API
		if ('getWindowSegments' in navigator && typeof navigator.getWindowSegments === 'function') {
			// @ts-ignore
			segmentCount = navigator.getWindowSegments().length;
		}
	} catch (e) { if (DEBUG_MODE) console.warn("Error accessing getWindowSegments", e); }

	let viewportSegments: any[] | undefined;
	try {
		// @ts-ignore - Experimental API
		if (window.visualViewport && 'segments' in window.visualViewport) {
			// @ts-ignore
			viewportSegments = window.visualViewport.segments as any[] | undefined;
		}
	} catch (e) { if (DEBUG_MODE) console.warn("Error accessing visualViewport.segments", e); }

	const hasSegments = segmentCount > 1 || (viewportSegments && viewportSegments.length > 1);

	if (isScreenSpanning || hasSegments) {
		if (DEBUG_MODE) console.log('Foldable Detect: Detected via Spanning/Segments API');
		finalResult.isFoldable = true;
		finalResult.confidence = 0.8; // Fairly high confidence
		finalResult.detectionMethod = isScreenSpanning ? 'mediaQuery' : (segmentCount > 1 ? 'getWindowSegments' : 'visualViewport');
		// Heuristic for unfolded state when API detects foldability
		finalResult.isUnfolded = aspectRatio > 0.8 && aspectRatio < 1.3; // Assume nearly square is unfolded
		finalResult.foldableType = /galaxy z/i.test(ua) ? 'zfold' : 'other'; // UA hint for type

		if (DEBUG_MODE) console.log('Foldable Detect: Result from API Match', finalResult);
		saveDetectionResult(finalResult);
		return finalResult;
	}

	// 3. User Agent Platform Check (Exclude Desktops)
	const isLikelyDesktopUA = /Windows NT|Macintosh|Linux x86_64/i.test(ua) && !/Android|iPhone|iPad|iPod|Mobile/i.test(ua);
	if (isLikelyDesktopUA) {
		// If UA clearly indicates a standard desktop OS, it's not a foldable phone.
		if (DEBUG_MODE) console.log('Foldable Detect: Detected standard desktop platform via UA. Not foldable.');
		return finalResult; // Return default (isFoldable: false)
	}

	// 4. Generic Dimension + Pixel Ratio Heuristic (Lower Confidence Fallback)
	// Only attempt if not identified as desktop and APIs didn't confirm.
	if (DEBUG_MODE) console.log('Foldable Detect: No API/Desktop match, trying generic dimension heuristic...');
	// Check for somewhat square aspect ratio AND high pixel density
	if (windowW > 600 && aspectRatio > 0.8 && aspectRatio < 1.3 && pixelRatio > 1.5) {
		if (DEBUG_MODE) console.log('Foldable Detect: Generic dimension heuristic PASSED (with pixelRatio check).');
		finalResult.isFoldable = true;
		finalResult.isUnfolded = true; // Assume unfolded if dimensions match this heuristic
		finalResult.confidence = 0.5; // Lower confidence for heuristic
		finalResult.detectionMethod = 'GenericDimensionsPixelRatio';
		finalResult.foldableType = /galaxy z/i.test(ua) ? 'zfold' : 'other'; // Still check UA for type hint
	} else {
		if (DEBUG_MODE) console.log('Foldable Detect: Generic dimension heuristic FAILED.');
		// Keep default finalResult (isFoldable: false)
	}

	// --- Log Final Result and Return ---
	if (DEBUG_MODE && finalResult.isFoldable) {
		console.log('Foldable Detect: Result from Dimension Heuristic', finalResult);
	} else if (DEBUG_MODE && !finalResult.isFoldable) {
        console.log('Foldable Detect: Final Result - Not Foldable');
    }

	saveDetectionResult(finalResult); // Save if confidence is high enough
	return finalResult;
}


// --- Helper Functions ---

/**
 * Checks localStorage for a manual override setting.
 * @returns {FoldableDetectionResult | null} The override result or null if not found/invalid.
 */
function checkManualOverride(): FoldableDetectionResult | null {
	if (typeof window === 'undefined' || typeof localStorage === 'undefined') return null;
	try {
		const override = localStorage.getItem('foldableDeviceOverride');
		if (override) {
			const settings = JSON.parse(override);
			// Basic validation of stored settings
			if (typeof settings.isFoldable === 'boolean' && typeof settings.isUnfolded === 'boolean') {
				return {
					isFoldable: settings.isFoldable,
					foldableType: settings.foldableType || 'unknown',
					isUnfolded: settings.isUnfolded,
					confidence: 1.0, // Max confidence for manual override
					detectionMethod: 'ManualOverride'
				};
			}
		}
	} catch (e) {
		if (DEBUG_MODE) console.error('Error checking for manual override:', e);
	}
	return null;
}

/**
 * Saves confident detection results to localStorage (if foldable and confidence >= 0.6).
 * @param {FoldableDetectionResult} result - The detection result to potentially save.
 */
function saveDetectionResult(result: FoldableDetectionResult) {
	if (typeof window === 'undefined' || typeof localStorage === 'undefined') return;
	// Only save reasonably confident foldable detections
	if (!result.isFoldable || result.confidence < 0.6) return;

	try {
		const dataToSave = {
			...result,
			timestamp: Date.now(),
			width: window.innerWidth, // Save dimensions at time of detection
			height: window.innerHeight
		};
		localStorage.setItem('foldableDeviceState', JSON.stringify(dataToSave));
		if (DEBUG_MODE) console.log("Foldable Detect: Saved state to localStorage", dataToSave);
	} catch (e) {
		if (DEBUG_MODE) console.error('Error saving detection state:', e);
	}
}

/**
 * Checks the User Agent and current window dimensions against known foldable device specifications.
 * Modifies the passed 'result' object directly if a match is found.
 * @param {string} ua - The navigator.userAgent string.
 * @param {number} width - Current window innerWidth.
 * @param {number} height - Current window innerHeight.
 * @param {FoldableDetectionResult} result - The result object to modify.
 * @returns {boolean} True if a spec match was found, false otherwise.
 */
function checkAgainstDeviceSpecs(
	ua: string,
	width: number,
	height: number,
	result: FoldableDetectionResult
): boolean {
	for (const [deviceKey, specs] of Object.entries(FOLDABLE_DEVICE_SPECS)) {
		// Check if UA contains any of the known model strings for this device
		const isMatchingModel = specs.models.some((model) => ua.includes(model));

		if (isMatchingModel) {
			if (DEBUG_MODE) console.log(`Foldable Detect: Spec Match - Found model match for ${deviceKey}`);
			result.isFoldable = true;
			result.foldableType = deviceKey.startsWith('zfold') ? 'zfold' : 'other';
			result.confidence = 0.9; // High confidence for specific model match
			result.detectionMethod = 'DeviceSpecMatch';

			// Check current dimensions against UNFOLDED specs (allowing for orientation swap)
			const { min: minWUnfolded, max: maxWUnfolded } = specs.unfoldedDimensions.width;
			const { min: minHUnfolded, max: maxHUnfolded } = specs.unfoldedDimensions.height;

			const isUnfoldedMatch =
				(width >= minWUnfolded && width <= maxWUnfolded && height >= minHUnfolded && height <= maxHUnfolded) ||
				(height >= minWUnfolded && height <= maxWUnfolded && width >= minHUnfolded && width <= maxHUnfolded);

			result.isUnfolded = isUnfoldedMatch;
			if (DEBUG_MODE) console.log(`Foldable Detect: Spec Match - Unfolded state: ${result.isUnfolded}`);
			return true; // Stop checking once a model matches
		}
	}
	if (DEBUG_MODE) console.log('Foldable Detect: Spec Match - No matching model found.');
	return false; // No spec match found
}


// --- Utilities Export ---
/**
 * Provides methods for manually controlling or debugging foldable detection.
 */
export const FoldableDeviceUtils = {
	/**
	 * Sets a manual override in localStorage for testing purposes.
	 * Requires page reload to take effect.
	 */
	setManualOverride(settings: {
		isFoldable: boolean;
		foldableType: 'zfold' | 'other' | 'unknown';
		isUnfolded: boolean;
	}) {
		if (typeof localStorage !== 'undefined') {
			localStorage.setItem('foldableDeviceOverride', JSON.stringify(settings));
			if (DEBUG_MODE) console.log("Foldable Utils: Set Override", settings);
		} else {
			console.warn("Foldable Utils: Cannot set override, localStorage not available.");
		}
	},

	/**
	 * Clears any manual override from localStorage.
	 * Requires page reload to take effect.
	 */
	clearManualOverride() {
		if (typeof localStorage !== 'undefined') {
			localStorage.removeItem('foldableDeviceOverride');
			if (DEBUG_MODE) console.log("Foldable Utils: Cleared Override");
		} else {
			console.warn("Foldable Utils: Cannot clear override, localStorage not available.");
		}
	},

	/**
	 * Forces a re-run of the detection logic.
	 * @returns {FoldableDetectionResult} The latest detection result.
	 */
	refreshDetection() {
		if (DEBUG_MODE) console.log("Foldable Utils: Refreshing detection...");
		return detectFoldableDevice();
	},

	/**
	 * Gathers various pieces of information useful for debugging detection issues.
	 * @returns {object} An object containing debug information.
	 */
	getDebugInfo: (): object => {
		if (typeof window === 'undefined' || typeof navigator === 'undefined') {
			return { error: "Cannot get debug info outside browser environment." };
		}
		const currentDetection = detectFoldableDevice(); // Run detection to get current state
		const hasManualOverride = localStorage.getItem('foldableDeviceOverride') !== null;
		let apiChecks = {};
		try {
			apiChecks = {
				isScreenSpanning: window.matchMedia('(screen-spanning: single-fold-vertical)').matches || window.matchMedia('(screen-spanning: single-fold-horizontal)').matches,
				// @ts-ignore
				getWindowSegmentsLength: ('getWindowSegments' in navigator && typeof navigator.getWindowSegments === 'function') ? navigator.getWindowSegments().length : 'N/A',
				// @ts-ignore
				visualViewportSegmentsLength: (window.visualViewport && 'segments' in window.visualViewport) ? window.visualViewport.segments?.length : 'N/A',
			}
		} catch(e) {
			if(DEBUG_MODE) console.error("Error getting API check info:", e);
		}


		return {
			currentDetection,
			hasManualOverride,
			windowDimensions: {
				width: window.innerWidth,
				height: window.innerHeight,
				pixelRatio: window.devicePixelRatio,
                aspectRatio: (window.innerWidth / window.innerHeight).toFixed(3)
			},
			screenDimensions: {
				width: window.screen.width,
				height: window.screen.height,
				availWidth: window.screen.availWidth,
				availHeight: window.screen.availHeight
			},
			userAgent: navigator.userAgent,
			apiChecks
		};
	}
};

// Optional: Add listener for posture changes (highly experimental API)
// function registerPostureChangeListener() { ... }
// if (browser) { registerPostureChangeListener(); }

