/**
 * Optimized resize management for thumbnail performance
 */

import { debounce } from './debounce.js';
import { thumbnailViewportManager } from './viewport.js';

export interface ResizeTarget {
	element: Element;
	callback: () => void;
	priority: 'high' | 'normal' | 'low';
}

export interface ResizeManagerOptions {
	debounceDelay?: number;
	enableViewportOptimization?: boolean;
	batchSize?: number;
}

/**
 * Centralized resize manager that optimizes resize operations
 * for better performance with many elements
 */
export class ResizeManager {
	private static instance: ResizeManager;
	private targets = new Map<Element, ResizeTarget>();
	private isResizing = false;
	private resizeObserver: ResizeObserver;
	private debouncedProcess: () => void;
	private throttledProcess: () => void;
	private options: Required<ResizeManagerOptions>;

	private constructor(options: ResizeManagerOptions = {}) {
		this.options = {
			debounceDelay: 16, // One frame at 60fps for immediate feel
			enableViewportOptimization: true,
			batchSize: 20, // Larger batches for better performance
			...options
		};

		// Create debounced processor for non-resizing scenarios
		this.debouncedProcess = debounce(() => this.processResizes(), this.options.debounceDelay);
		// Use immediate processing during resizing for responsive feel
		this.throttledProcess = () => this.processVisibleResizes();

		// Create resize observer (only in browser environment)
		if (typeof window !== 'undefined' && 'ResizeObserver' in window) {
			this.resizeObserver = new ResizeObserver(() => {
				if (this.isResizing) {
					// During active resizing, only process visible elements with throttling
					this.throttledProcess();
				} else {
					// When not actively resizing, use debounced processing for all elements
					this.debouncedProcess();
				}
			});
		} else {
			// Create a mock observer for SSR environments
			this.resizeObserver = {
				observe: () => {},
				unobserve: () => {},
				disconnect: () => {}
			} as unknown as ResizeObserver;
		}
	}

	static getInstance(options?: ResizeManagerOptions): ResizeManager {
		if (!ResizeManager.instance) {
			ResizeManager.instance = new ResizeManager(options);
		}
		return ResizeManager.instance;
	}

	/**
	 * Register an element for optimized resize handling
	 */
	register(
		element: Element,
		callback: () => void,
		priority: 'high' | 'normal' | 'low' = 'normal'
	): () => void {
		const target: ResizeTarget = { element, callback, priority };
		this.targets.set(element, target);
		this.resizeObserver.observe(element);

		// Return cleanup function
		return () => {
			this.unregister(element);
		};
	}

	/**
	 * Unregister an element from resize handling
	 */
	unregister(element: Element): void {
		this.targets.delete(element);
		this.resizeObserver.unobserve(element);
	}

	/**
	 * Set the resizing state (called by sidebar manager)
	 */
	setResizing(isResizing: boolean): void {
		this.isResizing = isResizing;

		if (!isResizing) {
			// When resizing ends, process all elements immediately for responsive feel
			this.processAllResizes();
		}
	}

	/**
	 * Process only visible elements during active resizing
	 */
	private processVisibleResizes(): void {
		if (!this.options.enableViewportOptimization) {
			this.processAllResizes();
			return;
		}

		const visibleElements = thumbnailViewportManager.getVisibleElements();
		const visibleTargets: ResizeTarget[] = [];

		// Collect visible targets
		for (const element of visibleElements) {
			const target = this.targets.get(element);
			if (target) {
				visibleTargets.push(target);
			}
		}

		// Sort by priority
		visibleTargets.sort((a, b) => {
			const priorityOrder = { high: 0, normal: 1, low: 2 };
			return priorityOrder[a.priority] - priorityOrder[b.priority];
		});

		// Process in batches to avoid blocking
		this.processBatched(visibleTargets);
	}

	/**
	 * Process all registered elements (used when not actively resizing)
	 */
	private processResizes(): void {
		this.processAllResizes();
	}

	/**
	 * Process all targets
	 */
	private processAllResizes(): void {
		const allTargets = Array.from(this.targets.values());

		// Sort by priority
		allTargets.sort((a, b) => {
			const priorityOrder = { high: 0, normal: 1, low: 2 };
			return priorityOrder[a.priority] - priorityOrder[b.priority];
		});

		this.processBatched(allTargets);
	}

	/**
	 * Process targets in batches to avoid blocking the main thread
	 */
	private processBatched(targets: ResizeTarget[]): void {
		if (targets.length === 0) {
			return;
		}

		if (this.isResizing) {
			// During resizing, process all visible elements immediately for responsive feel
			for (const target of targets) {
				try {
					target.callback();
				} catch {
					// Error in resize callback
				}
			}
		} else {
			// When not resizing, use batching to avoid blocking
			const batchSize = this.options.batchSize;
			let currentIndex = 0;

			const processBatch = () => {
				const endIndex = Math.min(currentIndex + batchSize, targets.length);

				for (let i = currentIndex; i < endIndex; i++) {
					try {
						targets[i].callback();
					} catch {
						// Error in resize callback
					}
				}

				currentIndex = endIndex;

				if (currentIndex < targets.length) {
					// Schedule next batch
					requestAnimationFrame(processBatch);
				}
			};

			processBatch();
		}
	}

	/**
	 * Force immediate processing of all elements
	 */
	forceProcess(): void {
		this.processAllResizes();
	}

	/**
	 * Get statistics about registered elements
	 */
	getStats(): {
		totalRegistered: number;
		visibleCount: number;
		isResizing: boolean;
	} {
		return {
			totalRegistered: this.targets.size,
			visibleCount: this.options.enableViewportOptimization
				? thumbnailViewportManager.getVisibleCount()
				: this.targets.size,
			isResizing: this.isResizing
		};
	}

	/**
	 * Clean up all resources
	 */
	destroy(): void {
		this.targets.clear();
		this.resizeObserver.disconnect();
		ResizeManager.instance = null as any;
	}
}

// Export singleton instance
export const resizeManager = ResizeManager.getInstance();
