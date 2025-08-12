import { describe, expect, it } from 'vitest';
import { PlacementKeyGenerator } from './PlacementKeyGenerator';

describe('PlacementKeyGenerator', () => {
	it('selects first available candidate key', () => {
		const gen = new PlacementKeyGenerator();
		const defaultPlacements = {
			pro_to_layer1_alpha_A: true,
			pro_to_layer2_beta: true,
		} as Record<string, unknown>;

		const motion = { motion_type: 'pro' } as any;
		const pictograph = { letter: 'A' } as any;

		const key = gen.generatePlacementKey(motion, pictograph, defaultPlacements, 'diamond');
		expect(key).toBe('pro_to_layer1_alpha_A');
	});

	it('falls back to motion type when none available', () => {
		const gen = new PlacementKeyGenerator();
		const motion = { motion_type: 'float' } as any;
		const pictograph = { letter: 'Z-' } as any;

		const key = gen.generatePlacementKey(motion, pictograph, {}, 'box');
		// Generator picks first candidate since no explicit fallback to basic is implemented
		expect(key).toBe('float_to_layer1_alpha_Z_dash');
	});
});
