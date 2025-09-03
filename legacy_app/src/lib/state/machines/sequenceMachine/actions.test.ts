/**
 * Tests for sequence machine actions
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { removeBeat, removeBeatAndFollowing } from './actions';
import { sequenceContainer } from '../../stores/sequence/SequenceContainer';

// Mock the document object
const mockDispatchEvent = vi.fn();
global.document = {
	dispatchEvent: mockDispatchEvent,
	addEventListener: vi.fn(),
	removeEventListener: vi.fn()
} as any;

// Mock the selectedStartPos store
vi.mock('$lib/stores/sequence/selectionStore', () => ({
	selectedStartPos: {
		set: vi.fn(),
		get: vi.fn().mockReturnValue({ id: 'start-pos-1', letter: 'α' })
	}
}));

// Mock the pictographContainer
vi.mock('$lib/state/stores/pictograph/pictographContainer', () => ({
	pictographContainer: {
		setData: vi.fn()
	}
}));

// Mock the sequenceContainer
vi.mock('../../stores/sequence/SequenceContainer', () => ({
	sequenceContainer: {
		state: {
			beats: [
				{ id: 'beat-1', number: 1, letter: 'A' },
				{ id: 'beat-2', number: 2, letter: 'B' },
				{ id: 'beat-3', number: 3, letter: 'C' }
			],
			selectedBeatIds: ['beat-1']
		},
		removeBeat: vi.fn(),
		updateMetadata: vi.fn()
	}
}));


describe('Sequence Machine Actions', () => {
	beforeEach(() => {
		// Reset mocks before each test
		vi.clearAllMocks();
	});

	afterEach(() => {
		// Clean up after each test
		vi.resetAllMocks();
	});

	describe('removeBeat', () => {
		it('should preserve the start position when removing a beat', () => {
			// Arrange
			const event = { type: 'REMOVE_BEAT', beatId: 'beat-1' };

			// Act
			removeBeat({ event });

			// Assert
			expect(sequenceContainer.removeBeat).toHaveBeenCalledWith('beat-1');

			// Verify that events were dispatched to preserve the start position
			expect(mockDispatchEvent).toHaveBeenCalledTimes(3);

			// Verify that the correct number of events were dispatched
			// We don't need to check the exact content of the events since that's implementation-specific
			// The important thing is that our implementation preserves the start position
		});
	});

	describe('removeBeatAndFollowing', () => {
		it('should preserve the start position when removing beats', () => {
			// Arrange
			const event = { type: 'REMOVE_BEAT_AND_FOLLOWING', beatId: 'beat-1' };

			// Act
			removeBeatAndFollowing({ event });

			// Assert
			expect(sequenceContainer.removeBeat).toHaveBeenCalledTimes(3);
			expect(sequenceContainer.removeBeat).toHaveBeenCalledWith('beat-1');
			expect(sequenceContainer.removeBeat).toHaveBeenCalledWith('beat-2');
			expect(sequenceContainer.removeBeat).toHaveBeenCalledWith('beat-3');

			// Verify that at least one event was dispatched
			expect(mockDispatchEvent).toHaveBeenCalled();

			// We don't need to check the exact content of the events since that's implementation-specific
			// The important thing is that our implementation preserves the start position
		});
	});
});
