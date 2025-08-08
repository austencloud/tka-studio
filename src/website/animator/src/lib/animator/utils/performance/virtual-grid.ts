/**
 * Virtual grid manager for performance optimization during resize operations
 */

export interface VirtualGridItem {
	id: string;
	data: any;
	height?: number;
	isVisible?: boolean;
}

export interface VirtualGridState {
	items: VirtualGridItem[];
	visibleItems: VirtualGridItem[];
	startIndex: number;
	endIndex: number;
	totalHeight: number;
	containerHeight: number;
	scrollTop: number;
}

export interface VirtualGridOptions {
	itemHeight: number;
	overscan: number; // Number of items to render outside viewport
	columns: number;
	gap: number;
	padding: number;
}

/**
 * Virtual grid manager that can temporarily hide non-visible items during resize
 */
export class VirtualGridManager {
	private options: VirtualGridOptions;
	private state: VirtualGridState;
	private isResizing = false;
	private resizeMode: 'normal' | 'minimal' | 'hidden' = 'normal';
	private callbacks = new Set<() => void>();

	constructor(options: VirtualGridOptions) {
		this.options = options;
		this.state = {
			items: [],
			visibleItems: [],
			startIndex: 0,
			endIndex: 0,
			totalHeight: 0,
			containerHeight: 0,
			scrollTop: 0
		};
	}

	/**
	 * Set the items to be managed
	 */
	setItems(items: VirtualGridItem[]): void {
		this.state.items = items;
		this.updateVisibleItems();
		this.notifyCallbacks();
	}

	/**
	 * Update container dimensions and scroll position
	 */
	updateViewport(containerHeight: number, scrollTop: number): void {
		this.state.containerHeight = containerHeight;
		this.state.scrollTop = scrollTop;
		this.updateVisibleItems();
		this.notifyCallbacks();
	}

	/**
	 * Set resize mode to optimize performance
	 */
	setResizeMode(mode: 'normal' | 'minimal' | 'hidden'): void {
		this.resizeMode = mode;
		this.updateVisibleItems();
		this.notifyCallbacks();
	}

	/**
	 * Start resize operation - switch to performance mode
	 */
	startResize(): void {
		this.isResizing = true;
		this.setResizeMode('minimal'); // Show only visible items
	}

	/**
	 * End resize operation - restore full rendering
	 */
	endResize(): void {
		this.isResizing = false;
		// Use a small delay to let the resize settle before restoring all items
		setTimeout(() => {
			this.setResizeMode('normal');
		}, 50);
	}

	/**
	 * Calculate which items should be visible based on current mode
	 */
	private updateVisibleItems(): void {
		const { items, containerHeight, scrollTop } = this.state;
		const { itemHeight, overscan, columns, gap, padding } = this.options;

		if (items.length === 0) {
			this.state.visibleItems = [];
			this.state.startIndex = 0;
			this.state.endIndex = 0;
			this.state.totalHeight = 0;
			return;
		}

		// Calculate row height (item height + gap)
		const rowHeight = itemHeight + gap;
		const totalRows = Math.ceil(items.length / columns);
		this.state.totalHeight = totalRows * rowHeight + padding * 2;

		if (this.resizeMode === 'hidden') {
			// Hide all items during intense resize operations
			this.state.visibleItems = [];
			this.state.startIndex = 0;
			this.state.endIndex = 0;
			return;
		}

		// Calculate visible range
		const startRow = Math.floor((scrollTop - padding) / rowHeight);
		const endRow = Math.ceil((scrollTop + containerHeight - padding) / rowHeight);

		// Apply overscan based on resize mode
		const currentOverscan = this.resizeMode === 'minimal' ? 1 : overscan;
		const startRowWithOverscan = Math.max(0, startRow - currentOverscan);
		const endRowWithOverscan = Math.min(totalRows - 1, endRow + currentOverscan);

		// Convert rows to item indices
		this.state.startIndex = startRowWithOverscan * columns;
		this.state.endIndex = Math.min(items.length - 1, (endRowWithOverscan + 1) * columns - 1);

		// Extract visible items
		this.state.visibleItems = items.slice(this.state.startIndex, this.state.endIndex + 1);

		// Mark items as visible for external tracking
		items.forEach((item, index) => {
			item.isVisible = index >= this.state.startIndex && index <= this.state.endIndex;
		});
	}

	/**
	 * Get current state
	 */
	getState(): VirtualGridState {
		return { ...this.state };
	}

	/**
	 * Get spacer heights for virtual scrolling
	 */
	getSpacerHeights(): { top: number; bottom: number } {
		const { itemHeight, gap, columns, padding } = this.options;
		const rowHeight = itemHeight + gap;

		const topRows = Math.floor(this.state.startIndex / columns);
		const bottomRows = Math.ceil((this.state.items.length - this.state.endIndex - 1) / columns);

		return {
			top: topRows * rowHeight + padding,
			bottom: Math.max(0, bottomRows * rowHeight + padding)
		};
	}

	/**
	 * Subscribe to state changes
	 */
	subscribe(callback: () => void): () => void {
		this.callbacks.add(callback);
		return () => {
			this.callbacks.delete(callback);
		};
	}

	/**
	 * Notify all subscribers of state changes
	 */
	private notifyCallbacks(): void {
		this.callbacks.forEach((callback) => {
			try {
				callback();
			} catch (error) {
				console.warn('Error in virtual grid callback:', error);
			}
		});
	}

	/**
	 * Get performance stats
	 */
	getStats(): {
		totalItems: number;
		visibleItems: number;
		renderRatio: number;
		isResizing: boolean;
		resizeMode: string;
	} {
		const renderRatio =
			this.state.items.length > 0 ? this.state.visibleItems.length / this.state.items.length : 0;

		return {
			totalItems: this.state.items.length,
			visibleItems: this.state.visibleItems.length,
			renderRatio,
			isResizing: this.isResizing,
			resizeMode: this.resizeMode
		};
	}

	/**
	 * Force immediate update
	 */
	forceUpdate(): void {
		this.updateVisibleItems();
		this.notifyCallbacks();
	}

	/**
	 * Clean up resources
	 */
	destroy(): void {
		this.callbacks.clear();
	}
}
