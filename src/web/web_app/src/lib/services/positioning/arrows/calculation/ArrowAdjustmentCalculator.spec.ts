import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { ArrowAdjustmentCalculator } from './ArrowAdjustmentCalculator';

describe('ArrowAdjustmentCalculator (end-to-end positioning)', () => {
	const originalFetch = global.fetch;

	beforeEach(() => {
		vi.useRealTimers();
	});

	afterEach(() => {
		vi.restoreAllMocks();
		global.fetch = originalFetch as typeof fetch;
	});

	it('calculates full arrow adjustment (base + directional) for diamond grid', async () => {
		// Mock special placement data
		global.fetch = vi.fn(async (url: any) => {
			const u = String(url);
			if (u.includes('arrow_placement')) {
				const data = u.includes('special') ? {} : { pro: { '0': [50, 25] } };
				return new Response(JSON.stringify(data), { status: 200 });
			}
			return new Response('Not Found', { status: 404 });
		}) as unknown as typeof fetch;

		const calc = new ArrowAdjustmentCalculator();

		const motion = {
			motion_type: 'pro',
			start_location: 'NE',
			end_location: 'SW',
			prop_rot_dir: 'cw',
			turns: 0,
		} as any;

		const pictograph = {
			letter: 'A',
			grid_mode: 'diamond',
			motions: { blue: motion, red: motion },
		} as any;

		const result = await calc.calculateAdjustment(pictograph, motion, 'A', 'NE' as any, 'blue');

		// Should return some adjustment (base + directional tuple)
		expect(result).toBeDefined();
		expect(typeof result.x).toBe('number');
		expect(typeof result.y).toBe('number');
	});
});
