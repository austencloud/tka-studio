import {
	CLOCKWISE,
	COUNTER_CLOCKWISE,
	NO_ROT,
	DIAMOND,
	BOX,
	PRO,
	ANTI,
	FLOAT,
	DASH,
	STATIC,
	NORTHEAST,
	SOUTHEAST,
	SOUTHWEST,
	NORTHWEST,
	WEST,
	SOUTH,
	EAST,
	NORTH
} from '$lib/types/Constants';
import type { DirectionTupleSet } from '../types';
import type { GridMode, PropRotDir, MotionType, ShiftHandRotDir } from '$lib/types/Types';

export function getDirectionTuples(
	x: number,
	y: number,
	motionType: MotionType,
	propRotDir: PropRotDir,
	gridMode: GridMode,
	options?: { startOri?: string; handRotDir?: ShiftHandRotDir }
): DirectionTupleSet {
	// No rotation special case
	if (propRotDir === NO_ROT && motionType !== STATIC) {
		return [
			[x, -y],
			[y, x],
			[-x, y],
			[-y, -x]
		];
	}

	switch (motionType) {
		case STATIC:
			return getStaticTuples(x, y, propRotDir, gridMode);
		case DASH:
			return getDashTuples(x, y, propRotDir, gridMode);
		case PRO:
			return getProTuples(x, y, propRotDir, gridMode);
		case ANTI:
			return getAntiTuples(x, y, propRotDir, gridMode);
		case FLOAT:
			return getFloatTuples(x, y, options?.handRotDir, gridMode);
		default:
			return [];
	}
}

function getDashTuples(
	x: number,
	y: number,
	propRotDir: PropRotDir,
	gridMode: GridMode
): DirectionTupleSet {
	if (gridMode === DIAMOND) {
		if (propRotDir === CLOCKWISE) {
			return [
				[x, -y],
				[y, x],
				[-x, y],
				[-y, -x]
			];
		} else if (propRotDir === COUNTER_CLOCKWISE) {
			return [
				[-x, -y],
				[y, -x],
				[x, y],
				[-y, x]
			];
		} else if (propRotDir === NO_ROT) {
			return [
				[x, y],
				[-y, -x],
				[x, -y],
				[y, x]
			];
		}
	} else if (gridMode === BOX) {
		if (propRotDir === CLOCKWISE) {
			return [
				[-y, x],
				[-x, -y],
				[y, -x],
				[x, y]
			];
		} else if (propRotDir === COUNTER_CLOCKWISE) {
			return [
				[-x, y],
				[-y, -x],
				[x, -y],
				[y, x]
			];
		} else if (propRotDir === NO_ROT) {
			return [
				[x, y],
				[-y, x],
				[-x, -y],
				[y, -x]
			];
		}
	}

	// Default fallback
	return [
		[x, y],
		[-x, -y],
		[-y, x],
		[y, -x]
	];
}

function getStaticTuples(
	x: number,
	y: number,
	propRotDir: PropRotDir,
	gridMode: GridMode
): DirectionTupleSet {
	if (gridMode === DIAMOND) {
		if (propRotDir === CLOCKWISE) {
			return [
				[x, -y],
				[y, x],
				[-x, y],
				[-y, -x]
			];
		} else if (propRotDir === COUNTER_CLOCKWISE) {
			return [
				[-x, -y],
				[y, -x],
				[x, y],
				[-y, x]
			];
		}
	} else if (gridMode === BOX) {
		if (propRotDir === CLOCKWISE) {
			return [
				[x, y],
				[-y, x],
				[-x, -y],
				[y, -x]
			];
		} else if (propRotDir === COUNTER_CLOCKWISE) {
			return [
				[-y, -x],
				[x, -y],
				[y, x],
				[-x, y]
			];
		}
	}

	// Default case when no valid match
	return [
		[x, y],
		[-x, -y],
		[-y, x],
		[y, -x]
	];
}

function getProTuples(
	x: number,
	y: number,
	propRotDir: PropRotDir,
	gridMode: GridMode
): DirectionTupleSet {
	if (gridMode === DIAMOND) {
		if (propRotDir === CLOCKWISE) {
			return [
				[x, y],
				[-y, x],
				[-x, -y],
				[y, -x]
			];
		} else if (propRotDir === COUNTER_CLOCKWISE) {
			return [
				[-y, -x],
				[x, -y],
				[y, x],
				[-x, y]
			];
		}
	} else if (gridMode === BOX) {
		if (propRotDir === CLOCKWISE) {
			return [
				[-x, y],
				[-y, -x],
				[x, -y],
				[y, x]
			];
		} else if (propRotDir === COUNTER_CLOCKWISE) {
			return [
				[x, y],
				[-y, x],
				[-x, -y],
				[y, -x]
			];
		}
	}

	// Default case
	return [];
}

function getAntiTuples(
	x: number,
	y: number,
	propRotDir: PropRotDir,
	gridMode: GridMode
): DirectionTupleSet {
	if (gridMode === DIAMOND) {
		if (propRotDir === CLOCKWISE) {
			return [
				[-y, -x],
				[x, -y],
				[y, x],
				[-x, y]
			];
		} else if (propRotDir === COUNTER_CLOCKWISE) {
			return [
				[x, y],
				[-y, x],
				[-x, -y],
				[y, -x]
			];
		}
	} else if (gridMode === BOX) {
		if (propRotDir === CLOCKWISE) {
			return [
				[-x, y],
				[-y, -x],
				[x, -y],
				[y, x]
			];
		} else if (propRotDir === COUNTER_CLOCKWISE) {
			return [
				[x, y],
				[-y, x],
				[-x, -y],
				[y, -x]
			];
		}
	}

	// Default case
	return [];
}

function getFloatTuples(
	x: number,
	y: number,
	handRotDir?: ShiftHandRotDir,
	gridMode?: GridMode
): DirectionTupleSet {
	// Based on the Python version, you'd implement float tuples with CW_HANDPATH and CCW_HANDPATH
	// This is a simplified implementation since the Python code references HandpathCalculator
	if (handRotDir === 'cw_shift') {
		return [
			[x, y],
			[-y, x],
			[-x, -y],
			[y, -x]
		];
	} else if (handRotDir === 'ccw_shift') {
		return [
			[-y, -x],
			[x, -y],
			[y, x],
			[-x, y]
		];
	}

	// Default when handRotDir is undefined
	return [
		[x, y],
		[x, y],
		[x, y],
		[x, y]
	];
}

export function getQuadrantIndex(
	arrow: { loc?: string; motionType: string },
	gridMode: GridMode
): number {
	const { loc = '', motionType } = arrow;

	if (gridMode === DIAMOND) {
		if ([STATIC, DASH].includes(motionType)) {
			switch (loc) {
				case 'n':
				case NORTH:
					return 0;
				case 'e':
				case EAST:
					return 1;
				case 's':
				case SOUTH:
					return 2;
				case 'w':
				case WEST:
					return 3;
				default:
					return 0;
			}
		}
	}

	// Existing logic for other cases remains the same
	if (gridMode === DIAMOND) {
		if ([PRO, ANTI, FLOAT].includes(motionType)) {
			switch (loc) {
				case 'ne':
				case NORTHEAST:
					return 0;
				case 'se':
				case SOUTHEAST:
					return 1;
				case 'sw':
				case SOUTHWEST:
					return 2;
				case 'nw':
				case NORTHWEST:
					return 3;
				default:
					return 0;
			}
		}
	} else if (gridMode === BOX) {
		if ([PRO, ANTI, FLOAT].includes(motionType)) {
			switch (loc) {
				case 'n':
				case NORTH:
					return 0;
				case 'e':
				case EAST:
					return 1;
				case 's':
				case SOUTH:
					return 2;
				case 'w':
				case WEST:
					return 3;
				default:
					return 0;
			}
		} else if ([STATIC, DASH].includes(motionType)) {
			switch (loc) {
				case 'ne':
				case NORTHEAST:
					return 0;
				case 'se':
				case SOUTHEAST:
					return 1;
				case 'sw':
				case SOUTHWEST:
					return 2;
				case 'nw':
				case NORTHWEST:
					return 3;
				default:
					return 0;
			}
		}
	}

	return 0;
}
