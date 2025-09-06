/**
 * Tests for the sequence store adapter
 */
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { sequenceContainer } from './SequenceContainer';
import {
	sequenceStore,
	selectedBeatsStore,
	currentBeatStore,
	beatCountStore
} from './sequenceAdapter';
import type { BeatData } from './SequenceContainer';
import { get } from 'svelte/store';

// Mock localStorage
const localStorageMock = (() => {
	let store: Record<string, string> = {};
	return {
		getItem: vi.fn((key: string) => store[key] || null),
		setItem: vi.fn((key: string, value: string) => {
			store[key] = value.toString();
		}),
		clear: vi.fn(() => {
			store = {};
		})
	};
})();

// Mock browser environment
vi.stubGlobal('localStorage', localStorageMock);
vi.stubGlobal('browser', true);

describe('Sequence Store Adapter', () => {
	// Reset the container before each test
	beforeEach(() => {
		sequenceContainer.reset();
		localStorageMock.clear();
	});

	it('should reflect the container state', () => {
		const storeState = get(sequenceStore);
		expect(storeState.beats).toEqual([]);
		expect(storeState.selectedBeatIds).toEqual([]);
		expect(storeState.currentBeatIndex).toBe(0);
		expect(storeState.isModified).toBe(false);
	});

	it('should update when the container changes', async () => {
		// Add a beat to the container
		sequenceContainer.addBeat({ id: '1', number: 1, letter: 'A' });

		// Wait for the store to update
		await new Promise((resolve) => setTimeout(resolve, 100));

		// Check that the store reflects the container state
		const storeState = get(sequenceStore);
		expect(storeState.beats).toHaveLength(1);
		expect(storeState.beats[0].id).toBe('1');
		expect(storeState.isModified).toBe(true);
	});

	it('should update the container when the store is set', () => {
		// Set the store state
		sequenceStore.set({
			beats: [{ id: '1', number: 1, letter: 'A' }],
			selectedBeatIds: ['1'],
			currentBeatIndex: 0,
			isModified: true,
			metadata: {
				name: 'Test Sequence',
				difficulty: 2,
				tags: ['test'],
				createdAt: new Date(),
				lastModified: new Date()
			}
		});

		// Check that the container reflects the store state
		expect(sequenceContainer.state.beats).toHaveLength(1);
		expect(sequenceContainer.state.beats[0].id).toBe('1');
		expect(sequenceContainer.state.selectedBeatIds).toEqual(['1']);
		expect(sequenceContainer.state.metadata.name).toBe('Test Sequence');
	});

	it('should update the container when the store is updated', () => {
		// Update the store state
		sequenceStore.update((state) => ({
			...state,
			beats: [{ id: '1', number: 1, letter: 'A' }],
			metadata: {
				...state.metadata,
				name: 'Updated Sequence'
			}
		}));

		// Check that the container reflects the updated store state
		expect(sequenceContainer.state.beats).toHaveLength(1);
		expect(sequenceContainer.state.beats[0].id).toBe('1');
		expect(sequenceContainer.state.metadata.name).toBe('Updated Sequence');
	});

	it('should forward action methods to the container', () => {
		// Use the store's action methods
		sequenceStore.addBeat({ id: '1', number: 1, letter: 'A' });
		sequenceStore.selectBeat('1');
		sequenceStore.updateMetadata({ name: 'Action Test' });

		// Check that the container state was updated
		expect(sequenceContainer.state.beats).toHaveLength(1);
		expect(sequenceContainer.state.beats[0].id).toBe('1');
		expect(sequenceContainer.state.selectedBeatIds).toEqual(['1']);
		expect(sequenceContainer.state.metadata.name).toBe('Action Test');
	});

	it('should provide derived stores', async () => {
		// Set up some test data
		const beats: BeatData[] = [
			{ id: '1', number: 1, letter: 'A' },
			{ id: '2', number: 2, letter: 'B' }
		];

		sequenceStore.setSequence(beats);
		sequenceStore.selectBeat('1');
		sequenceStore.setCurrentBeatIndex(0);

		// Wait for the derived stores to update
		await new Promise((resolve) => setTimeout(resolve, 100));

		// Check the derived stores
		expect(get(selectedBeatsStore)).toHaveLength(1);
		expect(get(selectedBeatsStore)[0].id).toBe('1');

		expect(get(currentBeatStore)?.id).toBe('1');

		expect(get(beatCountStore)).toBe(2);
	});

	it('should handle complex operations correctly', async () => {
		// Add some beats
		sequenceStore.addBeats([
			{ id: '1', number: 1, letter: 'A' },
			{ id: '2', number: 2, letter: 'B' },
			{ id: '3', number: 3, letter: 'C' }
		]);

		// Select multiple beats
		sequenceStore.selectBeat('1');
		sequenceStore.selectBeat('2', true);

		// Update a beat
		sequenceStore.updateBeat('1', { letter: 'X' });

		// Remove a beat
		sequenceStore.removeBeat('3');

		// Wait for the store to update
		await new Promise((resolve) => setTimeout(resolve, 100));

		// Check the final state
		const storeState = get(sequenceStore);
		expect(storeState.beats).toHaveLength(2);
		expect(storeState.beats[0].letter).toBe('X');
		expect(storeState.selectedBeatIds).toEqual(['1', '2']);
		expect(storeState.isModified).toBe(true);

		// Check that the container state matches
		expect(sequenceContainer.state.beats).toHaveLength(2);
		expect(sequenceContainer.state.beats[0].letter).toBe('X');
		expect(sequenceContainer.state.selectedBeatIds).toEqual(['1', '2']);
	});
});
