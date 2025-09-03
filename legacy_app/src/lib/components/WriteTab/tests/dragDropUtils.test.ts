import { describe, it, expect, vi, beforeEach } from 'vitest';
import { setupDraggable, setupDropTarget } from '../utils/dragDropUtils';

// Create a proper mock for DragEvent
class MockDragEvent extends Event {
	dataTransfer: {
		setData: ReturnType<typeof vi.fn>;
		getData: ReturnType<typeof vi.fn>;
		setDragImage: ReturnType<typeof vi.fn>;
		effectAllowed: string;
		dropEffect: string;
		types: string[];
	};
	preventDefault: ReturnType<typeof vi.fn>;
	stopPropagation: ReturnType<typeof vi.fn>;

	constructor(type: string) {
		super(type, { bubbles: true });
		this.preventDefault = vi.fn();
		this.stopPropagation = vi.fn();
		this.dataTransfer = {
			setData: vi.fn(),
			getData: vi.fn(),
			setDragImage: vi.fn(),
			effectAllowed: '',
			dropEffect: '',
			types: ['application/sequence-data']
		};
	}
}

// Helper function to create drag events
const createDragEvent = (type: string): MockDragEvent => {
	return new MockDragEvent(type) as unknown as MockDragEvent;
};

describe('dragDropUtils', () => {
	let element: HTMLElement;

	beforeEach(() => {
		// Create a fresh element for each test
		element = document.createElement('div');
		vi.clearAllMocks();
	});

	describe('setupDraggable', () => {
		it('should set the element as draggable', () => {
			setupDraggable(element, { test: 'data' });
			expect(element.getAttribute('draggable')).toBe('true');
		});

		it('should handle dragstart event', () => {
			const onDragStart = vi.fn();
			const data = { test: 'data' };

			setupDraggable(element, data, { onDragStart });

			const event = createDragEvent('dragstart');
			element.dispatchEvent(event);

			expect(event.dataTransfer?.setData).toHaveBeenCalledWith(
				'application/sequence-data',
				JSON.stringify(data)
			);
			expect(onDragStart).toHaveBeenCalled();
		});

		it('should set drag image if provided', () => {
			const dragImage = document.createElement('img');
			const data = { test: 'data' };

			setupDraggable(element, data, { dragImage });

			const event = createDragEvent('dragstart');
			element.dispatchEvent(event);

			expect(event.dataTransfer?.setDragImage).toHaveBeenCalledWith(dragImage, 0, 0);
		});

		it('should set effectAllowed if provided', () => {
			const data = { test: 'data' };

			setupDraggable(element, data, { effectAllowed: 'move' });

			const event = createDragEvent('dragstart');
			element.dispatchEvent(event);

			expect(event.dataTransfer?.effectAllowed).toBe('move');
		});
	});

	describe('setupDropTarget', () => {
		it('should handle dragover event', () => {
			const onDragOver = vi.fn();

			setupDropTarget(element, { onDragOver });

			const event = createDragEvent('dragover');
			element.dispatchEvent(event);

			expect(event.preventDefault).toHaveBeenCalled();
			expect(onDragOver).toHaveBeenCalled();
		});

		it('should set dropEffect if data type is accepted', () => {
			setupDropTarget(element, {
				acceptedTypes: ['application/sequence-data'],
				dropEffect: 'move'
			});

			const event = createDragEvent('dragover');
			element.dispatchEvent(event);

			expect(event.dataTransfer?.dropEffect).toBe('move');
		});

		it('should set dropEffect to none if data type is not accepted', () => {
			setupDropTarget(element, {
				acceptedTypes: ['application/other-type'],
				dropEffect: 'move'
			});

			const event = createDragEvent('dragover');
			element.dispatchEvent(event);

			expect(event.dataTransfer?.dropEffect).toBe('none');
		});

		it('should handle drop event and parse data', () => {
			const onDrop = vi.fn();
			const data = { test: 'data' };

			setupDropTarget(element, { onDrop });

			const event = createDragEvent('drop');
			event.dataTransfer!.getData = vi.fn().mockReturnValue(JSON.stringify(data));

			element.dispatchEvent(event);

			expect(event.preventDefault).toHaveBeenCalled();
			expect(event.dataTransfer?.getData).toHaveBeenCalled();
			expect(onDrop).toHaveBeenCalledWith(event, data);
		});
	});
});
