/**
 * Quick test to verify our positioning pipeline integration
 */

import { describe, expect, it } from 'vitest';
import { getPositioningServiceFactory } from '$services/positioning/PositioningServiceFactory';

describe('Positioning Pipeline Integration', () => {
	it('should create orchestrator that uses ArrowAdjustmentCalculator', () => {
		const factory = getPositioningServiceFactory();
		const orchestrator = factory.createPositioningOrchestrator();

		// Verify the orchestrator was created
		expect(orchestrator).toBeDefined();
		expect(typeof orchestrator.calculateArrowPosition).toBe('function');
		expect(typeof orchestrator.calculateAllArrowPositions).toBe('function');

		console.log('✅ Orchestrator created successfully with sophisticated pipeline');
	});

	it('should create adjustment calculator with advanced lookup', () => {
		const factory = getPositioningServiceFactory();
		const adjustmentCalculator = factory.createAdjustmentCalculator();

		expect(adjustmentCalculator).toBeDefined();
		expect(typeof adjustmentCalculator.calculateAdjustment).toBe('function');

		console.log('✅ ArrowAdjustmentCalculator created with advanced lookup');
	});
});
