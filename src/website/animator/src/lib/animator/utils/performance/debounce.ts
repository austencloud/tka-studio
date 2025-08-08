/**
 * Performance utilities for debouncing and throttling operations
 */

export type DebounceFunction<T extends (..._args: any[]) => any> = (
	..._args: Parameters<T>
) => void;

/**
 * Creates a debounced version of a function that delays execution until after
 * the specified delay has passed since the last time it was invoked.
 */
export function debounce<T extends (..._args: any[]) => any>(
	func: T,
	delay: number
): DebounceFunction<T> {
	let timeoutId: ReturnType<typeof setTimeout> | null = null;

	return (...args: Parameters<T>) => {
		if (timeoutId !== null) {
			clearTimeout(timeoutId);
		}

		timeoutId = setTimeout(() => {
			func(...args);
			timeoutId = null;
		}, delay);
	};
}

/**
 * Creates a throttled version of a function that only executes at most once
 * per specified interval.
 */
export function throttle<T extends (..._args: any[]) => any>(
	func: T,
	interval: number
): DebounceFunction<T> {
	let lastExecution = 0;
	let timeoutId: ReturnType<typeof setTimeout> | null = null;

	return (...args: Parameters<T>) => {
		const now = Date.now();
		const timeSinceLastExecution = now - lastExecution;

		if (timeSinceLastExecution >= interval) {
			func(...args);
			lastExecution = now;
		} else {
			if (timeoutId !== null) {
				clearTimeout(timeoutId);
			}

			timeoutId = setTimeout(() => {
				func(...args);
				lastExecution = Date.now();
				timeoutId = null;
			}, interval - timeSinceLastExecution);
		}
	};
}

/**
 * Creates a function that executes immediately on first call, then debounces subsequent calls
 */
export function immediateDebounce<T extends (..._args: any[]) => any>(
	func: T,
	delay: number
): DebounceFunction<T> {
	let timeoutId: ReturnType<typeof setTimeout> | null = null;
	let hasExecuted = false;

	return (...args: Parameters<T>) => {
		if (!hasExecuted) {
			func(...args);
			hasExecuted = true;
			return;
		}

		if (timeoutId !== null) {
			clearTimeout(timeoutId);
		}

		timeoutId = setTimeout(() => {
			func(...args);
			timeoutId = null;
		}, delay);
	};
}

/**
 * Request animation frame based throttling for smooth animations
 */
export function rafThrottle<T extends (..._args: any[]) => any>(func: T): DebounceFunction<T> {
	let rafId: number | null = null;

	return (...args: Parameters<T>) => {
		if (rafId !== null) {
			cancelAnimationFrame(rafId);
		}

		rafId = requestAnimationFrame(() => {
			func(...args);
			rafId = null;
		});
	};
}
