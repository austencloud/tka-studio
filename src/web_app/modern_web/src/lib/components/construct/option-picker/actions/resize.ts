/**
 * Resize Action using Svelte 5 - No stores, pure functional approach
 *
 * A Svelte action that detects element resizing and calls the callback
 * with the new width and height. Includes debounced fallback for window resize.
 */

import type { Action } from 'svelte/action';

/**
 * Debounce utility function - pure functional approach
 */
function debounce<T extends (...args: unknown[]) => unknown>(
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
			timeoutId = null;
		}, delay);
	};

	debounced.cancel = () => {
		if (timeoutId !== null) {
			clearTimeout(timeoutId);
			timeoutId = null;
		}
	};

	return debounced as T & { cancel: () => void };
}

/**
 * Resize action for Svelte 5 - detects element resizing
 */
export const resize: Action<HTMLElement, (width: number, height: number) => void> = (
	node,
	callback
) => {
	// Ensure callback is a function
	if (typeof callback !== 'function') {
		console.warn('Resize action requires a callback function.');
		return {
			destroy() {},
			update() {},
		};
	}

	// Initial measurement with proper timing
	if (node) {
		requestAnimationFrame(() => {
			if (node) {
				const { width, height } = node.getBoundingClientRect();
				callback(width, height);
			}
		});
	}

	// Set up ResizeObserver if available (modern approach)
	let resizeObserver: ResizeObserver | undefined;
	let debouncedHandleResize: (() => void) & { cancel: () => void };

	if (typeof ResizeObserver !== 'undefined') {
		resizeObserver = new ResizeObserver((entries) => {
			if (!entries.length) return;

			const entry = entries[0];
			if (entry?.contentRect) {
				const { width, height } = entry.contentRect;
				// Call the current callback (supports dynamic updates)
				if (typeof callback === 'function') {
					callback(width, height);
				}
			}
		});

		resizeObserver.observe(node);

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
			},
		};
	} else {
		// Fallback for older browsers without ResizeObserver
		console.warn('ResizeObserver not supported. Using debounced window resize fallback.');

		const handleResize = () => {
			if (node) {
				const { width, height } = node.getBoundingClientRect();
				if (typeof callback === 'function') {
					callback(width, height);
				}
			}
		};

		// Create debounced resize handler
		debouncedHandleResize = debounce(handleResize, 200);
		window.addEventListener('resize', debouncedHandleResize);

		return {
			update(newCallback: (width: number, height: number) => void) {
				if (typeof newCallback === 'function') {
					callback = newCallback;
				} else {
					console.warn('Resize action update requires a function.');
				}
			},
			destroy() {
				if (debouncedHandleResize) {
					debouncedHandleResize.cancel();
					window.removeEventListener('resize', debouncedHandleResize);
				}
			},
		};
	}
};

/**
 * Create a resize observer using runes for manual control
 */
export function createResizeObserver() {
	let width = $state(0);
	let height = $state(0);
	let isObserving = $state(false);
	let observer: ResizeObserver | null = null;

	function observe(element: HTMLElement) {
		if (!element) return;

		// Clean up existing observer
		if (observer) {
			observer.disconnect();
		}

		// Initial measurement
		const rect = element.getBoundingClientRect();
		width = rect.width;
		height = rect.height;

		// Set up new observer
		if (typeof ResizeObserver !== 'undefined') {
			observer = new ResizeObserver((entries) => {
				if (!entries.length) return;

				const entry = entries[0];
				if (entry?.contentRect) {
					width = entry.contentRect.width;
					height = entry.contentRect.height;
				}
			});

			observer.observe(element);
			isObserving = true;
		} else {
			console.warn('ResizeObserver not supported');
			isObserving = false;
		}
	}

	function disconnect() {
		if (observer) {
			observer.disconnect();
			observer = null;
		}
		isObserving = false;
	}

	return {
		// Reactive state
		get width() {
			return width;
		},
		get height() {
			return height;
		},
		get isObserving() {
			return isObserving;
		},

		// Actions
		observe,
		disconnect,
	};
}

/**
 * Create a window resize listener using runes
 */
export function createWindowResizeObserver() {
	let windowWidth = $state(typeof window !== 'undefined' ? window.innerWidth : 0);
	let windowHeight = $state(typeof window !== 'undefined' ? window.innerHeight : 0);
	let isListening = $state(false);

	const debouncedResize = debounce(() => {
		if (typeof window !== 'undefined') {
			windowWidth = window.innerWidth;
			windowHeight = window.innerHeight;
		}
	}, 100);

	function startListening() {
		if (typeof window === 'undefined') return;

		// Initial values
		windowWidth = window.innerWidth;
		windowHeight = window.innerHeight;

		// Add listener
		window.addEventListener('resize', debouncedResize);
		isListening = true;
	}

	function stopListening() {
		if (typeof window === 'undefined') return;

		window.removeEventListener('resize', debouncedResize);
		debouncedResize.cancel();
		isListening = false;
	}

	// Auto-cleanup effect
	$effect(() => {
		return () => {
			if (isListening) {
				stopListening();
			}
		};
	});

	return {
		// Reactive state
		get windowWidth() {
			return windowWidth;
		},
		get windowHeight() {
			return windowHeight;
		},
		get isListening() {
			return isListening;
		},

		// Actions
		startListening,
		stopListening,
	};
}
