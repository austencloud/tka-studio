/**
 * Viewport and intersection utilities for performance optimization
 */

export interface ViewportObserverOptions {
	root?: Element | null;
	rootMargin?: string;
	threshold?: number | number[];
}

export interface ViewportEntry {
	element: Element;
	isIntersecting: boolean;
	intersectionRatio: number;
	boundingClientRect: DOMRectReadOnly;
}

export type ViewportCallback = (_entries: ViewportEntry[]) => void;

/**
 * Enhanced intersection observer wrapper with better performance characteristics
 */
export class ViewportObserver {
	private observer: IntersectionObserver;
	private callbacks = new Map<Element, ViewportCallback>();

	constructor(options: ViewportObserverOptions = {}) {
		const defaultOptions: ViewportObserverOptions = {
			root: null,
			rootMargin: '50px', // Start loading slightly before entering viewport
			threshold: [0, 0.1, 0.5, 1.0] // Multiple thresholds for granular control
		};

		const finalOptions = { ...defaultOptions, ...options };

		// Check if we're in a browser environment
		if (typeof window !== 'undefined' && 'IntersectionObserver' in window) {
			this.observer = new IntersectionObserver((entries) => {
				const processedEntries: ViewportEntry[] = entries.map((entry) => ({
					element: entry.target,
					isIntersecting: entry.isIntersecting,
					intersectionRatio: entry.intersectionRatio,
					boundingClientRect: entry.boundingClientRect
				}));

				// Group entries by element and call respective callbacks
				const elementGroups = new Map<Element, ViewportEntry[]>();

				for (const entry of processedEntries) {
					if (!elementGroups.has(entry.element)) {
						elementGroups.set(entry.element, []);
					}
					elementGroups.get(entry.element)!.push(entry);
				}

				// Call callbacks for each element
				for (const [element, elementEntries] of elementGroups) {
					const callback = this.callbacks.get(element);
					if (callback) {
						callback(elementEntries);
					}
				}
			}, finalOptions);
		} else {
			// Create a mock observer for SSR environments
			this.observer = {
				observe: () => {},
				unobserve: () => {},
				disconnect: () => {},
				root: null,
				rootMargin: '',
				thresholds: [],
				takeRecords: () => []
			} as unknown as IntersectionObserver;
		}
	}

	/**
	 * Start observing an element with a specific callback
	 */
	observe(element: Element, callback: ViewportCallback): void {
		this.callbacks.set(element, callback);
		this.observer.observe(element);
	}

	/**
	 * Stop observing an element
	 */
	unobserve(element: Element): void {
		this.callbacks.delete(element);
		this.observer.unobserve(element);
	}

	/**
	 * Disconnect the observer and clean up all callbacks
	 */
	disconnect(): void {
		this.callbacks.clear();
		this.observer.disconnect();
	}
}

/**
 * Singleton viewport observer for thumbnail visibility tracking
 */
class ThumbnailViewportManager {
	private static instance: ThumbnailViewportManager;
	private observer: ViewportObserver;
	private visibleElements = new Set<Element>();

	private constructor() {
		// Only create observer in browser environment
		if (typeof window !== 'undefined') {
			this.observer = new ViewportObserver({
				rootMargin: '100px', // Larger margin for thumbnails
				threshold: [0, 0.1] // Just need to know if it's visible or not
			});
		} else {
			// Create a minimal mock for SSR
			this.observer = {
				observe: () => () => {},
				unobserve: () => {},
				disconnect: () => {}
			} as any;
		}
	}

	static getInstance(): ThumbnailViewportManager {
		if (!ThumbnailViewportManager.instance) {
			ThumbnailViewportManager.instance = new ThumbnailViewportManager();
		}
		return ThumbnailViewportManager.instance;
	}

	/**
	 * Register a thumbnail element for viewport tracking
	 */
	registerThumbnail(element: Element, onVisible: () => void, onHidden: () => void): () => void {
		this.observer.observe(element, (entries) => {
			for (const entry of entries) {
				if (entry.isIntersecting && entry.intersectionRatio > 0) {
					if (!this.visibleElements.has(element)) {
						this.visibleElements.add(element);
						onVisible();
					}
				} else {
					if (this.visibleElements.has(element)) {
						this.visibleElements.delete(element);
						onHidden();
					}
				}
			}
		});

		// Return cleanup function
		return () => {
			this.observer.unobserve(element);
			this.visibleElements.delete(element);
		};
	}

	/**
	 * Check if an element is currently visible
	 */
	isVisible(element: Element): boolean {
		return this.visibleElements.has(element);
	}

	/**
	 * Get all currently visible elements
	 */
	getVisibleElements(): Set<Element> {
		return new Set(this.visibleElements);
	}

	/**
	 * Get count of visible elements
	 */
	getVisibleCount(): number {
		return this.visibleElements.size;
	}
}

export const thumbnailViewportManager = ThumbnailViewportManager.getInstance();

/**
 * Simple utility to check if an element is in viewport without observer
 */
export function isElementInViewport(element: Element, margin = 0): boolean {
	const rect = element.getBoundingClientRect();
	const windowHeight = window.innerHeight || document.documentElement.clientHeight;
	const windowWidth = window.innerWidth || document.documentElement.clientWidth;

	return (
		rect.top >= -margin &&
		rect.left >= -margin &&
		rect.bottom <= windowHeight + margin &&
		rect.right <= windowWidth + margin
	);
}

/**
 * Get the percentage of an element that is visible in the viewport
 */
export function getElementVisibilityRatio(element: Element): number {
	const rect = element.getBoundingClientRect();
	const windowHeight = window.innerHeight || document.documentElement.clientHeight;
	const windowWidth = window.innerWidth || document.documentElement.clientWidth;

	// Calculate visible area
	const visibleTop = Math.max(0, rect.top);
	const visibleLeft = Math.max(0, rect.left);
	const visibleBottom = Math.min(windowHeight, rect.bottom);
	const visibleRight = Math.min(windowWidth, rect.right);

	if (visibleTop >= visibleBottom || visibleLeft >= visibleRight) {
		return 0; // Not visible
	}

	const visibleArea = (visibleBottom - visibleTop) * (visibleRight - visibleLeft);
	const totalArea = rect.height * rect.width;

	return totalArea > 0 ? visibleArea / totalArea : 0;
}
