// src/lib/utils/memoizationUtils.ts


/**
 * Creates a memoized function with a limited cache size (LRU)
 * @param fn The function to memoize
 * @param maxSize Maximum cache size before evicting older entries
 * @param keyFn Optional function to generate a custom cache key
 * @returns Memoized function with the same signature as the original
 */
export function memoizeLRU<T extends (...args: any[]) => any>(
	fn: T,
	maxSize: number = 100,
	keyFn?: (...args: Parameters<T>) => string
): T {
	const cache = new Map<string, ReturnType<T>>();
	const keyOrder: string[] = []; // Track key access order for LRU

	const memoized = (...args: Parameters<T>): ReturnType<T> => {
		const key = keyFn ? keyFn(...args) : JSON.stringify(args);

		// Check if result is already in cache
		if (cache.has(key)) {
			// Move this key to the end (most recently used)
			const keyIndex = keyOrder.indexOf(key);
			if (keyIndex > -1) {
				keyOrder.splice(keyIndex, 1);
			}
			keyOrder.push(key);

			return cache.get(key) as ReturnType<T>;
		}

		// Ensure cache doesn't exceed max size
		if (cache.size >= maxSize && keyOrder.length > 0) {
			// Remove least recently used item
			const oldestKey = keyOrder.shift();
			if (oldestKey) cache.delete(oldestKey);
		}

		// Calculate result and store in cache
		const result = fn(...args);
		cache.set(key, result);
		keyOrder.push(key);

		return result;
	};

	// Add a method to clear the cache if needed
	(memoized as any).clearCache = () => {
		cache.clear();
		keyOrder.length = 0;
	};

	return memoized as T;
}
