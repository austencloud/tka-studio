/**
 * Tests for the container.ts module
 */

import { describe, test, expect } from 'vitest';
import { createContainer } from './container';

// Test the safeClone function indirectly through the container
describe('State Container', () => {
	// Test basic functionality
	test('should create a container with initial state', () => {
		const container = createContainer({ count: 0 }, (_state, update) => ({
			increment: () => {
				update((s) => {
					s.count += 1;
				});
			}
		}));

		expect(container.state.count).toBe(0);
		container.increment();
		expect(container.state.count).toBe(1);
	});

	// Test handling of non-serializable objects
	test('should handle non-serializable objects', () => {
		// Create an object with a circular reference
		const circularObj: any = { name: 'circular' };
		circularObj.self = circularObj;

		// Create an object with a DOM node
		const domObj = {
			name: 'dom',
			element: typeof document !== 'undefined' ? document.createElement('div') : null
		};

		// Create an object with a function
		const funcObj = {
			name: 'function',
			callback: () => console.log('hello')
		};

		// Create a container with these objects
		const container = createContainer(
			{
				circular: circularObj,
				dom: domObj,
				func: funcObj,
				normal: { a: 1, b: 2 }
			},
			(_state, update) => ({
				updateNormal: () => {
					update((s) => {
						s.normal.a = 3;
					});
				}
			})
		);

		// The container should be created successfully
		expect(container).toBeDefined();

		// We should be able to access the normal properties
		expect(container.state.normal.a).toBe(1);

		// We should be able to update the state
		container.updateNormal();
		expect(container.state.normal.a).toBe(3);

		// The circular reference should be handled (either as null or as a new object)
		expect(container.state.circular).toBeDefined();

		// The DOM node should be replaced with null
		if (container.state.dom.element !== null) {
			expect(container.state.dom.element).toBeNull();
		}

		// The function should be replaced with a function or null
		expect(
			typeof container.state.func.callback === 'function' || container.state.func.callback === null
		).toBeTruthy();
	});

	// Test reset functionality
	test('should reset state to initial values', () => {
		const container = createContainer({ count: 0, name: 'test' }, (_state, update) => ({
			increment: () => {
				update((s) => {
					s.count += 1;
				});
			},
			setName: (name: string) => {
				update((s) => {
					s.name = name;
				});
			}
		}));

		// Modify state
		container.increment();
		container.setName('modified');

		expect(container.state.count).toBe(1);
		expect(container.state.name).toBe('modified');

		// Reset state
		container.reset();

		// State should be back to initial values
		expect(container.state.count).toBe(0);
		expect(container.state.name).toBe('test');
	});
});
