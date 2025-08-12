import { describe, expect, it } from 'vitest';
import { SpecialPlacementOriKeyGenerator } from './SpecialPlacementOriKeyGenerator';

describe('SpecialPlacementOriKeyGenerator', () => {
	it('returns from_layer1 for in/out orientations', () => {
		const gen = new SpecialPlacementOriKeyGenerator();
		const pictograph = {
			motions: {
				blue: { end_ori: 'in' },
				red: { end_ori: 'out' },
			},
		} as any;

		const key = gen.generateOrientationKey({} as any, pictograph);
		expect(key).toBe('from_layer1');
	});

	it('returns from_layer3_blue1_red2 for mixed orientations', () => {
		const gen = new SpecialPlacementOriKeyGenerator();
		const pictograph = {
			motions: {
				blue: { end_ori: 'in' },
				red: { end_ori: 'alpha' },
			},
		} as any;

		const key = gen.generateOrientationKey({} as any, pictograph);
		expect(key).toBe('from_layer3_blue1_red2');
	});

	it('returns from_layer2 for alpha/beta orientations', () => {
		const gen = new SpecialPlacementOriKeyGenerator();
		const pictograph = {
			motions: {
				blue: { end_ori: 'alpha' },
				red: { end_ori: 'beta' },
			},
		} as any;

		const key = gen.generateOrientationKey({} as any, pictograph);
		expect(key).toBe('from_layer2');
	});
});
