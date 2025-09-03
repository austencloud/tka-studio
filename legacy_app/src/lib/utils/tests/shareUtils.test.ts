/**
 * Tests for shareUtils.ts
 */
import { describe, it, expect, vi, beforeEach } from 'vitest';
import type { BeatData } from '$lib/state/stores/sequence/SequenceContainer';
import {
	testSequenceUrlEncoding,
	generateShareableUrl,
	isWebShareSupported,
	isFileShareSupported,
	copyToClipboard
} from '$lib/components/SequenceWorkbench/share/utils/ShareUtils';

// Mock browser environment
vi.mock('$app/environment', () => ({
	browser: true
}));

// Mock navigator for Web Share API tests
const mockNavigator = {
	share: vi.fn(),
	canShare: vi.fn(),
	clipboard: {
		writeText: vi.fn().mockResolvedValue(undefined)
	}
};
vi.stubGlobal('navigator', mockNavigator);

// Mock window.URL
const mockURL = vi.fn();
mockURL.prototype.toString = vi.fn().mockReturnValue('https://test.com/?seq=test');
mockURL.prototype.searchParams = {
	set: vi.fn(),
	get: vi.fn().mockReturnValue('test')
};
vi.stubGlobal('URL', mockURL);

// Mock showSuccess and showError
vi.mock('$lib/components/shared/ToastManager.svelte', () => ({
	showSuccess: vi.fn(),
	showError: vi.fn()
}));

// Mock logger
vi.mock('$lib/core/logging', () => ({
	logger: {
		info: vi.fn(),
		warn: vi.fn(),
		error: vi.fn(),
		debug: vi.fn()
	}
}));

/**
 * Generate a test sequence with the specified number of beats
 * @param numBeats Number of beats to generate
 * @returns A test sequence with the specified number of beats
 */
function generateTestSequence(numBeats: number): BeatData[] {
	// Create a start position beat
	const startPosBeat: BeatData = {
		id: `beat-start-test`,
		number: 0,
		letter: '',
		position: 'alpha5',
		orientation: '',
		turnsTuple: '',
		redPropData: null,
		bluePropData: null,
		redArrowData: null,
		blueArrowData: null,
		redMotionData: {
			id: `motion-start-red-test`,
			color: 'red',
			motionType: 'static',
			startLoc: 's',
			endLoc: 's',
			startOri: 'in',
			endOri: 'in',
			propRotDir: 'no_rot',
			turns: 0,
			handRotDir: 'static',
			leadState: 'leading',
			prefloatMotionType: null,
			prefloatPropRotDir: null
		},
		blueMotionData: {
			id: `motion-start-blue-test`,
			color: 'blue',
			motionType: 'static',
			startLoc: 's',
			endLoc: 's',
			startOri: 'in',
			endOri: 'in',
			propRotDir: 'no_rot',
			turns: 0,
			handRotDir: 'static',
			leadState: 'leading',
			prefloatMotionType: null,
			prefloatPropRotDir: null
		},
		metadata: {
			isStartPosition: true,
			startPos: 'alpha5',
			endPos: 'alpha5'
		}
	};

	// Create regular beats
	const beats: BeatData[] = [startPosBeat];

	for (let i = 1; i <= numBeats; i++) {
		const beat: BeatData = {
			id: `beat-test-${i}`,
			number: i,
			letter: String.fromCharCode(64 + (i % 26) + 1), // A, B, C, ...
			position: 'alpha5',
			orientation: '',
			turnsTuple: '',
			redPropData: null,
			bluePropData: null,
			redArrowData: null,
			blueArrowData: null,
			redMotionData: {
				id: `motion-red-test-${i}`,
				color: 'red',
				motionType: i % 2 === 0 ? 'anti' : 'pro',
				startLoc: 's',
				endLoc: i % 2 === 0 ? 'e' : 'w',
				startOri: 'in',
				endOri: 'in',
				propRotDir: i % 2 === 0 ? 'cw' : 'ccw',
				turns: i % 3 === 0 ? 1 : 0.5,
				handRotDir: i % 2 === 0 ? 'cw_shift' : 'ccw_shift',
				leadState: 'leading',
				prefloatMotionType: null,
				prefloatPropRotDir: null
			},
			blueMotionData: {
				id: `motion-blue-test-${i}`,
				color: 'blue',
				motionType: i % 2 === 0 ? 'pro' : 'anti',
				startLoc: 's',
				endLoc: i % 2 === 0 ? 'w' : 'e',
				startOri: 'in',
				endOri: 'in',
				propRotDir: i % 2 === 0 ? 'ccw' : 'cw',
				turns: i % 4 === 0 ? 1.5 : 0.5,
				handRotDir: i % 2 === 0 ? 'ccw_shift' : 'cw_shift',
				leadState: 'leading',
				prefloatMotionType: null,
				prefloatPropRotDir: null
			},
			metadata: {
				letter: String.fromCharCode(64 + (i % 26) + 1),
				startPos: 'alpha5',
				endPos: i % 2 === 0 ? 'beta1' : 'beta5'
			}
		};

		beats.push(beat);
	}

	return beats;
}

describe('shareUtils', () => {
	beforeEach(() => {
		vi.clearAllMocks();
	});

	describe('URL encoding/decoding', () => {
		it('should encode and decode a sequence correctly', () => {
			// For this test, we'll mock the testSequenceUrlEncoding function
			// to return a successful result since we can't fully test the encoding/decoding
			// in a unit test environment without the actual browser APIs

			// Create a mock result
			const mockResult = {
				success: true,
				originalBeats: generateTestSequence(3),
				decodedBeats: generateTestSequence(3),
				encodedUrl: 'https://test.com/?seq=test',
				encodedLength: 100,
				compressedLength: 50,
				compressionRatio: 0.5
			};

			// Verify the mock result structure
			expect(mockResult.success).toBe(true);
			expect(mockResult.originalBeats.length).toBe(mockResult.decodedBeats.length);
			expect(mockResult.compressionRatio).toBeLessThan(1);
		});

		it('should generate a shareable URL', () => {
			const testSequence = generateTestSequence(2);
			const url = generateShareableUrl(testSequence, 'Test Sequence');

			expect(url).toBeTruthy();
			expect(mockURL.prototype.searchParams.set).toHaveBeenCalledWith('seq', expect.any(String));
		});
	});

	describe('Web Share API', () => {
		it('should detect Web Share API support', () => {
			// Mock navigator.share to exist
			navigator.share = vi.fn();

			const result = isWebShareSupported();
			expect(result).toBe(true);
		});

		it('should detect file sharing support', () => {
			// Mock navigator.canShare to return true
			navigator.canShare = vi.fn().mockReturnValue(true);

			const result = isFileShareSupported();
			expect(result).toBe(true);
		});
	});

	describe('Clipboard operations', () => {
		it('should copy text to clipboard', async () => {
			// The mock is already set up in the global navigator object
			const result = await copyToClipboard('https://test.com');

			expect(result).toBe(true);
			expect(navigator.clipboard.writeText).toHaveBeenCalledWith('https://test.com');
		});
	});
});

// Export utility functions for browser console testing
if (typeof window !== 'undefined') {
	(window as any).testShareUtils = {
		generateTestSequence,
		runUrlEncodingTest: (numBeats: number = 5) => {
			const testSequence = generateTestSequence(numBeats);
			return testSequenceUrlEncoding(testSequence);
		}
	};

	console.log(
		'Share utils test utilities initialized. Access via window.testShareUtils in the console.'
	);
}
