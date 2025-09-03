/**
 * Utility functions for HTML5 drag and drop operations
 */
import { browser } from '$app/environment';
import hapticFeedbackService from '$lib/services/HapticFeedbackService';

/**
 * Sets up a draggable element with the provided data
 *
 * @param element The HTML element to make draggable
 * @param data The data to attach to the drag operation
 * @param options Additional options for the drag operation
 */
export function setupDraggable(
	element: HTMLElement,
	data: any,
	options: {
		dragImage?: HTMLElement;
		effectAllowed?:
			| 'copy'
			| 'move'
			| 'link'
			| 'copyMove'
			| 'copyLink'
			| 'linkMove'
			| 'all'
			| 'none';
		onDragStart?: (event: DragEvent) => void;
		onDragEnd?: (event: DragEvent) => void;
	} = {}
) {
	// Set the element as draggable
	element.setAttribute('draggable', 'true');

	// Handle drag start
	element.addEventListener('dragstart', (event: DragEvent) => {
		if (!event.dataTransfer) return;

		// Set the drag effect
		event.dataTransfer.effectAllowed = options.effectAllowed || 'copy';

		// Set the drag image if provided
		if (options.dragImage) {
			event.dataTransfer.setDragImage(options.dragImage, 0, 0);
		}

		// Set the data
		const jsonData = JSON.stringify(data);
		event.dataTransfer.setData('application/sequence-data', jsonData);
		event.dataTransfer.setData('text/plain', jsonData);

		// Provide haptic feedback when starting to drag
		if (browser) {
			hapticFeedbackService.trigger('selection');
		}

		// Call the onDragStart callback if provided
		if (options.onDragStart) {
			options.onDragStart(event);
		}
	});

	// Handle drag end
	element.addEventListener('dragend', (event: DragEvent) => {
		if (options.onDragEnd) {
			options.onDragEnd(event);
		}
	});
}

/**
 * Sets up a drop target element
 *
 * @param element The HTML element to make a drop target
 * @param options Options for the drop target
 */
export function setupDropTarget(
	element: HTMLElement,
	options: {
		acceptedTypes?: string[];
		dropEffect?: 'copy' | 'move' | 'link' | 'none';
		onDragEnter?: (event: DragEvent) => void;
		onDragOver?: (event: DragEvent) => void;
		onDragLeave?: (event: DragEvent) => void;
		onDrop?: (event: DragEvent, data: any) => void;
	} = {}
) {
	const acceptedTypes = options.acceptedTypes || ['application/sequence-data'];
	const dropEffect = options.dropEffect || 'copy';

	// Handle drag enter
	element.addEventListener('dragenter', (event: DragEvent) => {
		event.preventDefault();

		if (options.onDragEnter) {
			options.onDragEnter(event);
		}
	});

	// Handle drag over
	element.addEventListener('dragover', (event: DragEvent) => {
		event.preventDefault();

		if (!event.dataTransfer) return;

		// Check if the data type is accepted
		const isAccepted = acceptedTypes.some((type) => event.dataTransfer?.types.includes(type));

		if (isAccepted) {
			event.dataTransfer.dropEffect = dropEffect;
		} else {
			event.dataTransfer.dropEffect = 'none';
		}

		if (options.onDragOver) {
			options.onDragOver(event);
		}
	});

	// Handle drag leave
	element.addEventListener('dragleave', (event: DragEvent) => {
		if (options.onDragLeave) {
			options.onDragLeave(event);
		}
	});

	// Handle drop
	element.addEventListener('drop', (event: DragEvent) => {
		event.preventDefault();

		if (!event.dataTransfer) return;

		// Get the data
		let data: any = null;

		for (const type of acceptedTypes) {
			const dataString = event.dataTransfer.getData(type);

			if (dataString) {
				try {
					data = JSON.parse(dataString);
					break;
				} catch (error) {
					console.error(`Failed to parse drop data for type ${type}:`, error);
				}
			}
		}

		if (data && options.onDrop) {
			// Provide haptic feedback for successful drop
			if (browser) {
				hapticFeedbackService.trigger('success');
			}

			options.onDrop(event, data);
		}
	});
}

/**
 * Creates a Svelte action for making an element draggable
 *
 * @param node The HTML element to make draggable
 * @param params The parameters for the draggable action
 */
export function draggable(
	node: HTMLElement,
	params: {
		data: any;
		dragImage?: HTMLElement;
		effectAllowed?:
			| 'copy'
			| 'move'
			| 'link'
			| 'copyMove'
			| 'copyLink'
			| 'linkMove'
			| 'all'
			| 'none';
		onDragStart?: (event: DragEvent) => void;
		onDragEnd?: (event: DragEvent) => void;
	}
) {
	setupDraggable(node, params.data, {
		dragImage: params.dragImage,
		effectAllowed: params.effectAllowed,
		onDragStart: params.onDragStart,
		onDragEnd: params.onDragEnd
	});

	return {
		update(newParams: typeof params) {
			// Update the data
			params = newParams;
		},
		destroy() {
			// Clean up event listeners if needed
			node.removeAttribute('draggable');
		}
	};
}

/**
 * Creates a Svelte action for making an element a drop target
 *
 * @param node The HTML element to make a drop target
 * @param params The parameters for the drop target action
 */
export function dropTarget(
	node: HTMLElement,
	params: {
		acceptedTypes?: string[];
		dropEffect?: 'copy' | 'move' | 'link' | 'none';
		onDragEnter?: (event: DragEvent) => void;
		onDragOver?: (event: DragEvent) => void;
		onDragLeave?: (event: DragEvent) => void;
		onDrop?: (event: DragEvent, data: any) => void;
	} = {}
) {
	setupDropTarget(node, params);

	return {
		update(newParams: typeof params) {
			// Update the parameters
			params = newParams;
		},
		destroy() {
			// Clean up event listeners if needed
		}
	};
}
