import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { SpecialPlacementService } from './SpecialPlacementService';

// Minimal shapes for domain types used by the service
type MotionData = any;
type PictographData = any;

describe('SpecialPlacementService', () => {
	const originalFetch = global.fetch;

	beforeEach(() => {
		vi.useRealTimers();
	});

	afterEach(() => {
		vi.restoreAllMocks();
		global.fetch = originalFetch as typeof fetch;
	});

	it('returns special motion-type adjustment when present (diamond/from_layer2/C, (0,0) anti)', async () => {
		const svc = new SpecialPlacementService();

		// Mock fetch to return the real-ish JSON structure we expect
		const data = {
			'(0, 0)': {
				anti: [0, 40],
			},
			'(1.5, 1.5)': {
				anti: [-70, 125],
				pro: [-70, 120],
			},
		};

		global.fetch = vi.fn(async (url: any) => {
			const u = String(url);
			if (u.endsWith('/data/arrow_placement/diamond/special/from_layer2/C_placements.json')) {
				return new Response(JSON.stringify(data), { status: 200 });
			}
			return new Response('Not Found', { status: 404 });
		}) as unknown as typeof fetch;

		// force layer2 by using non in/out end orientations
		const pictograph: PictographData = {
			letter: 'C',
			grid_mode: 'diamond',
			motions: {
				blue: { end_ori: 'alpha', turns: 0 },
				red: { end_ori: 'alpha', turns: 0 },
			},
		};

		// motionData can be any; use anti so motion-type key is used
		const motion: MotionData = { motion_type: 'anti', turns: 0 };

		const point = await svc.getSpecialAdjustment(motion, pictograph);
		expect(point).not.toBeNull();
		expect(point).toEqual({ x: 0, y: 40 });
	});

	it('returns color-based adjustment when present (box/from_layer1/A, (0.5,0.5) blue)', async () => {
		const svc = new SpecialPlacementService();

		const data = {
			'(0.5, 0.5)': {
				blue: [-20, 35],
				red: [-15, 15],
			},
		};

		global.fetch = vi.fn(async (url: any) => {
			const u = String(url);
			if (u.endsWith('/data/arrow_placement/box/special/from_layer1/A_placements.json')) {
				return new Response(JSON.stringify(data), { status: 200 });
			}
			return new Response('Not Found', { status: 404 });
		}) as unknown as typeof fetch;

		const pictograph: PictographData = {
			letter: 'A',
			grid_mode: 'box',
			motions: {
				blue: { end_ori: 'in', turns: 0.5 },
				red: { end_ori: 'in', turns: 0.5 },
			},
		};

		const motion: MotionData = { motion_type: 'pro', turns: 0.5 };

		// Force color lookup by passing explicit arrowColor
		const point = await svc.getSpecialAdjustment(motion, pictograph, 'blue');
		expect(point).not.toBeNull();
		expect(point).toEqual({ x: -20, y: 35 });
	});
});
