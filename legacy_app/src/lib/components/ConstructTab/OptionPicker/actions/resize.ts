import type { Action } from 'svelte/action';

/**
 * Debounce utility function.
 * Creates a debounced function that delays invoking the input function until
 * after 'delay' milliseconds have elapsed since the last time the debounced
 * function was invoked.
 *
 * @param func The function to debounce.
 * @param delay The number of milliseconds to delay.
 * @returns A debounced function with a `cancel` method.
 */
function debounce<T extends (...args: any[]) => any>(
	func: T,
	delay: number
): T & { cancel: () => void } {
	let timeoutId: ReturnType<typeof setTimeout> | null = null;

	const debounced = (...args: Parameters<T>) => {
		if (timeoutId !== null) {
			clearTimeout(timeoutId);
		}
		timeoutId = setTimeout(() => {
			func(...args);
			timeoutId = null; // Clear timeoutId after execution
		}, delay);
	};

	// Method to cancel any pending timeout
	debounced.cancel = () => {
		if (timeoutId !== null) {
			clearTimeout(timeoutId);
			timeoutId = null;
		}
	};

	return debounced as T & { cancel: () => void }; // Cast needed as TS doesn't infer the added method well
}

/**
 * A Svelte action that detects element resizing and calls the callback
 * with the new width and height. Includes debounced fallback for window resize.
 */
export const resize: Action<HTMLElement, (width: number, height: number) => void> = (
	node,
	callback
) => {
	// Ensure callback is a function
	if (typeof callback !== 'function') {
		console.warn('Resize action requires a callback function.');
		// Optionally return an empty action object if no callback
		return {
			destroy() {},
			update() {}
		};
	}

	// Initial measurement
	if (node) {
		// Use requestAnimationFrame to ensure layout is stable after initial render
		requestAnimationFrame(() => {
			if (node) {
				// Re-check node existence inside rAF
				const { width, height } = node.getBoundingClientRect();
				callback(width, height);
			}
		});
	}

	// Set up ResizeObserver if available
	let resizeObserver: ResizeObserver | undefined;
	let debouncedHandleResize: (() => void) & { cancel: () => void }; // Store debounced function reference for cleanup

	if (typeof ResizeObserver !== 'undefined') {
		resizeObserver = new ResizeObserver((entries) => {
			// ResizeObserver entries are inherently debounced/throttled by the browser
			if (!entries.length) return;

			const entry = entries[0];
			// Ensure contentRect is available (robustness)
			if (entry.contentRect) {
				const { width, height } = entry.contentRect;
				// Call the latest callback
				if (typeof callback === 'function') {
					callback(width, height);
				}
			}
		});

		resizeObserver.observe(node);

		// Return object for ResizeObserver path
		return {
			update(newCallback: (width: number, height: number) => void) {
				if (typeof newCallback === 'function') {
					callback = newCallback;
				} else {
					console.warn('Resize action update requires a function.');
				}
			},
			destroy() {
				if (resizeObserver) {
					resizeObserver.disconnect();
				}
			}
		};
	} else {
		// Fallback for browsers without ResizeObserver (using debounced window resize)
		console.warn('ResizeObserver not supported. Falling back to debounced window resize listener.');

		const handleResize = () => {
			if (node) {
				// Check node existence inside handler
				const { width, height } = node.getBoundingClientRect();
				// Call the latest callback
				if (typeof callback === 'function') {
					callback(width, height);
				}
			}
		};

		// Create the debounced version of handleResize
		// Using a delay of 200ms as a starting point
		debouncedHandleResize = debounce(handleResize, 200);

		window.addEventListener('resize', debouncedHandleResize);

		// Return object for fallback path
		return {
			update(newCallback: (width: number, height: number) => void) {
				if (typeof newCallback === 'function') {
					callback = newCallback;
				} else {
					console.warn('Resize action update requires a function.');
				}
			},
			destroy() {
				// Cancel any pending debounced call before removing listener
				if (debouncedHandleResize) {
					debouncedHandleResize.cancel();
					window.removeEventListener('resize', debouncedHandleResize);
				}
			}
		};
	}
};
