// src/lib/utils/appInitializer.ts
import { sequenceContainer } from '$lib/state/stores/sequence/SequenceContainer';
import { checkForSequenceInUrl } from '$lib/components/SequenceWorkbench/share/utils/ShareUtils';
import { logger } from '$lib/core/logging';

/**
 * Initialize the application, reporting progress via callback for XState
 * @param progressCallback Callback function provided by the XState actor for progress updates
 */
export async function initializeApplication(
	progressCallback?: (progress: number, message: string) => void
): Promise<boolean> {
	const reportProgress = (progress: number, message: string) => {
		progressCallback?.(progress, message);
	};

	reportProgress(0, 'Starting initialization...');

	try {
		const isBrowser = typeof window !== 'undefined';
		let preloadingPromise: Promise<any> = Promise.resolve();

		// Phase 1: SVG Preloading (Browser only)
		if (isBrowser) {
			reportProgress(10, 'Preloading SVG resources...');
			const { initSvgPreloading } = await import('./SvgPreloader');
			preloadingPromise = initSvgPreloading();
		} else {
			reportProgress(10, 'Server-side rendering (skipping SVG preload)...');
		}

		// Phase 2: Check for sequence in URL (Browser only)
		if (isBrowser) {
			reportProgress(30, 'Checking for shared sequence...');
			const foundSequenceInUrl = checkForSequenceInUrl(sequenceContainer);

			// If we didn't find a sequence in URL, load from localStorage
			if (!foundSequenceInUrl) {
				reportProgress(40, 'Loading saved sequence...');
				sequenceContainer.loadFromLocalStorage();
			}
		}

		// Phase 3: Wait for SVG Preloading (Browser only)
		const preloadProgress = 70;
		if (isBrowser) {
			reportProgress(preloadProgress, 'Finalizing resource loading...');
			await preloadingPromise;
		} else {
			reportProgress(preloadProgress, 'Skipping SVG finalize...');
		}

		// Phase 4: Final Preparations
		reportProgress(90, 'Preparing user interface...');
		if (isBrowser) {
			await new Promise((resolve) => setTimeout(resolve, 100));
		}

		// Phase 5: Complete
		reportProgress(100, 'Ready!');
		return true;
	} catch (error) {
		console.error('Initialization failed:', error);
		throw error;
	}
}
