import { describe, it, expect } from 'vitest';
import {
    calculateWorkbenchIsPortrait,
    calculateButtonSizeFactor,
    calculateBeatFrameShouldScroll,
    calculateCombinedUnitHeight,
    calculateAvailableHeightForBeatFrame
} from '../SequenceLayoutCalculator';

describe('SequenceLayoutCalculator', () => {
    describe('calculateWorkbenchIsPortrait', () => {
        it('should return true for portrait orientation with narrow width', () => {
            expect(calculateWorkbenchIsPortrait(400, 800)).toBe(true);
        });

        it('should return false for landscape orientation', () => {
            expect(calculateWorkbenchIsPortrait(1000, 600)).toBe(false);
        });

        it('should return false for portrait orientation with wide width', () => {
            expect(calculateWorkbenchIsPortrait(800, 1000)).toBe(false);
        });
    });

    describe('calculateButtonSizeFactor', () => {
        it('should return 0.7 for small screens', () => {
            expect(calculateButtonSizeFactor(300, 500)).toBe(0.7);
        });

        it('should return 0.8 for medium screens', () => {
            expect(calculateButtonSizeFactor(500, 800)).toBe(0.8);
        });

        it('should return 1.0 for large screens', () => {
            expect(calculateButtonSizeFactor(800, 1000)).toBe(1.0);
        });
    });

    describe('calculateBeatFrameShouldScroll', () => {
        it('should return false when natural height is 0', () => {
            expect(calculateBeatFrameShouldScroll(0, 500, 50)).toBe(false);
        });

        it('should return false when natural height fits within available space', () => {
            // Container height: 500, label height: 50, vertical padding: 20, beat frame wrapper padding: 10
            // Available height: 500 - 20 - 50 - 10 = 420
            // Natural height: 400
            expect(calculateBeatFrameShouldScroll(400, 500, 50)).toBe(false);
        });

        it('should return true when natural height exceeds available space', () => {
            // Container height: 500, label height: 50, vertical padding: 20, beat frame wrapper padding: 10
            // Available height: 500 - 20 - 50 - 10 = 420
            // Natural height: 450
            expect(calculateBeatFrameShouldScroll(450, 500, 50)).toBe(true);
        });
    });

    describe('calculateCombinedUnitHeight', () => {
        it('should return the sum of label height and beat frame height', () => {
            expect(calculateCombinedUnitHeight(50, 300)).toBe(350);
        });

        it('should handle zero values', () => {
            expect(calculateCombinedUnitHeight(0, 300)).toBe(300);
            expect(calculateCombinedUnitHeight(50, 0)).toBe(50);
            expect(calculateCombinedUnitHeight(0, 0)).toBe(0);
        });
    });

    describe('calculateAvailableHeightForBeatFrame', () => {
        it('should calculate available height correctly with default padding', () => {
            // Container height: 500, label height: 50, vertical padding: 20, beat frame wrapper padding: 10
            // Available height: 500 - 20 - 50 - 10 = 420
            expect(calculateAvailableHeightForBeatFrame(500, 50)).toBe(420);
        });

        it('should calculate available height correctly with custom padding', () => {
            // Container height: 500, label height: 50, vertical padding: 30, beat frame wrapper padding: 10
            // Available height: 500 - 30 - 50 - 10 = 410
            expect(calculateAvailableHeightForBeatFrame(500, 50, 30)).toBe(410);
        });
    });
});
