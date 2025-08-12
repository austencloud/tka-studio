import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { ArrowAdjustmentLookup } from './ArrowAdjustmentLookup';

// Mock services: simulate the special/default services and key generators
const createMockServices = () => {
	const mockSpecial = {
		getSpecialAdjustment: vi.fn(),
	};

	const mockDefault = {
		getAvailablePlacementKeys: vi.fn().mockResolvedValue(['pro']),
		getDefaultAdjustment: vi.fn().mockResolvedValue({ x: 100, y: 50 }),
	};

	const mockOriKeyGen = {
		generateOrientationKey: vi.fn().mockReturnValue('from_layer1'),
	};

	const mockPlacementKeyGen = {
		generatePlacementKey: vi.fn().mockReturnValue('pro'),
	};

	const mockTurnsGen = {
		generateTurnsTuple: vi.fn().mockReturnValue([0, 0]),
	};

	const mockAttrGen = {
		getKeyFromArrow: vi.fn().mockReturnValue('basic'),
	};

	return {
		mockSpecial,
		mockDefault,
		mockOriKeyGen,
		mockPlacementKeyGen,
		mockTurnsGen,
		mockAttrGen,
	};
};

describe('ArrowAdjustmentLookup (advanced orchestration)', () => {
	beforeEach(() => {
		vi.useRealTimers();
	});

	afterEach(() => {
		vi.restoreAllMocks();
	});

	it('returns special adjustment when available', async () => {
		const mocks = createMockServices();
		mocks.mockSpecial.getSpecialAdjustment.mockResolvedValue({ x: 20, y: -30 });

		const lookup = new ArrowAdjustmentLookup(
			mocks.mockSpecial as any,
			mocks.mockDefault as any,
			mocks.mockOriKeyGen as any,
			mocks.mockPlacementKeyGen as any,
			mocks.mockTurnsGen as any,
			mocks.mockAttrGen as any
		);

		const pictograph = { letter: 'C', grid_mode: 'diamond' } as any;
		const motion = { motion_type: 'anti', turns: 0 } as any;

		const result = await lookup.getBaseAdjustment(pictograph, motion, 'C');
		expect(result).toEqual({ x: 20, y: -30 });
		expect(mocks.mockSpecial.getSpecialAdjustment).toHaveBeenCalledWith(
			motion,
			pictograph,
			undefined
		);
	});

	it('falls back to default when special not available', async () => {
		const mocks = createMockServices();
		mocks.mockSpecial.getSpecialAdjustment.mockResolvedValue(null);

		const lookup = new ArrowAdjustmentLookup(
			mocks.mockSpecial as any,
			mocks.mockDefault as any,
			mocks.mockOriKeyGen as any,
			mocks.mockPlacementKeyGen as any,
			mocks.mockTurnsGen as any,
			mocks.mockAttrGen as any
		);

		const pictograph = { letter: 'A', grid_mode: 'diamond' } as any;
		const motion = { motion_type: 'pro', turns: 0 } as any;

		const result = await lookup.getBaseAdjustment(pictograph, motion, 'A');
		expect(result).toEqual({ x: 100, y: 50 });
		expect(mocks.mockDefault.getDefaultAdjustment).toHaveBeenCalledWith(
			'pro',
			0,
			'pro',
			'diamond'
		);
	});

	it('generates lookup keys from key services', async () => {
		const mocks = createMockServices();
		mocks.mockSpecial.getSpecialAdjustment.mockResolvedValue({ x: 5, y: 10 });

		const lookup = new ArrowAdjustmentLookup(
			mocks.mockSpecial as any,
			mocks.mockDefault as any,
			mocks.mockOriKeyGen as any,
			mocks.mockPlacementKeyGen as any,
			mocks.mockTurnsGen as any,
			mocks.mockAttrGen as any
		);

		const pictograph = { motions: { blue: {}, red: {} } } as any;
		const motion = { motion_type: 'float' } as any;

		await lookup.getBaseAdjustment(pictograph, motion, 'T');

		expect(mocks.mockOriKeyGen.generateOrientationKey).toHaveBeenCalledWith(motion, pictograph);
		expect(mocks.mockTurnsGen.generateTurnsTuple).toHaveBeenCalledWith(pictograph);
		expect(mocks.mockAttrGen.getKeyFromArrow).toHaveBeenCalled();
	});
});
