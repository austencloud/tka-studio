import {
	NORTH,
	EAST,
	SOUTH,
	WEST,
	NORTHEAST,
	SOUTHEAST,
	SOUTHWEST,
	NORTHWEST,
	CLOCKWISE,
	COUNTER_CLOCKWISE,
	DASH,
	STATIC,
	CW_SHIFT,
	CCW_SHIFT
} from '$lib/types/Constants';

export type Location =
	| typeof NORTH
	| typeof EAST
	| typeof SOUTH
	| typeof WEST
	| typeof NORTHEAST
	| typeof SOUTHEAST
	| typeof SOUTHWEST
	| typeof NORTHWEST;

export type HandpathDirection = typeof CW_SHIFT | typeof CCW_SHIFT | typeof DASH | typeof STATIC;

export class HandpathCalculator {
	private readonly loc_map_cw: Record<Location, Location> = {
		[SOUTH]: WEST,
		[WEST]: NORTH,
		[NORTH]: EAST,
		[EAST]: SOUTH,
		[NORTHEAST]: SOUTHEAST,
		[SOUTHEAST]: SOUTHWEST,
		[SOUTHWEST]: NORTHWEST,
		[NORTHWEST]: NORTHEAST
	};

	private readonly loc_map_ccw: Record<Location, Location> = {
		[SOUTH]: EAST,
		[EAST]: NORTH,
		[NORTH]: WEST,
		[WEST]: SOUTH,
		[NORTHEAST]: NORTHWEST,
		[NORTHWEST]: SOUTHWEST,
		[SOUTHWEST]: SOUTHEAST,
		[SOUTHEAST]: NORTHEAST
	};

	private readonly loc_map_dash: Record<Location, Location> = {
		[SOUTH]: NORTH,
		[NORTH]: SOUTH,
		[WEST]: EAST,
		[EAST]: WEST,
		[NORTHEAST]: SOUTHWEST,
		[SOUTHEAST]: NORTHWEST,
		[SOUTHWEST]: NORTHEAST,
		[NORTHWEST]: SOUTHEAST
	};

	private readonly loc_map_static: Record<Location, Location> = {
		[SOUTH]: SOUTH,
		[NORTH]: NORTH,
		[WEST]: WEST,
		[EAST]: EAST,
		[NORTHEAST]: NORTHEAST,
		[SOUTHEAST]: SOUTHEAST,
		[SOUTHWEST]: SOUTHWEST,
		[NORTHWEST]: NORTHWEST
	};

	private readonly hand_rot_dir_map: Record<string, HandpathDirection> = {
		[`${SOUTH},${WEST}`]: CW_SHIFT,
		[`${WEST},${NORTH}`]: CW_SHIFT,
		[`${NORTH},${EAST}`]: CW_SHIFT,
		[`${EAST},${SOUTH}`]: CW_SHIFT,
		[`${WEST},${SOUTH}`]: CCW_SHIFT,
		[`${NORTH},${WEST}`]: CCW_SHIFT,
		[`${EAST},${NORTH}`]: CCW_SHIFT,
		[`${SOUTH},${EAST}`]: CCW_SHIFT,
		[`${SOUTH},${NORTH}`]: DASH,
		[`${WEST},${EAST}`]: DASH,
		[`${NORTH},${SOUTH}`]: DASH,
		[`${EAST},${WEST}`]: DASH,
		[`${NORTH},${NORTH}`]: STATIC,
		[`${EAST},${EAST}`]: STATIC,
		[`${SOUTH},${SOUTH}`]: STATIC,
		[`${WEST},${WEST}`]: STATIC,
		[`${NORTHEAST},${SOUTHEAST}`]: CW_SHIFT,
		[`${SOUTHEAST},${SOUTHWEST}`]: CW_SHIFT,
		[`${SOUTHWEST},${NORTHWEST}`]: CW_SHIFT,
		[`${NORTHWEST},${NORTHEAST}`]: CW_SHIFT,
		[`${NORTHEAST},${NORTHWEST}`]: CCW_SHIFT,
		[`${NORTHWEST},${SOUTHWEST}`]: CCW_SHIFT,
		[`${SOUTHWEST},${SOUTHEAST}`]: CCW_SHIFT,
		[`${SOUTHEAST},${NORTHEAST}`]: CCW_SHIFT,
		[`${NORTHEAST},${SOUTHWEST}`]: DASH,
		[`${SOUTHEAST},${NORTHWEST}`]: DASH,
		[`${SOUTHWEST},${NORTHEAST}`]: DASH,
		[`${NORTHWEST},${SOUTHEAST}`]: DASH,
		[`${NORTHEAST},${NORTHEAST}`]: STATIC,
		[`${SOUTHEAST},${SOUTHEAST}`]: STATIC,
		[`${SOUTHWEST},${SOUTHWEST}`]: STATIC,
		[`${NORTHWEST},${NORTHWEST}`]: STATIC
	};

	getHandRotDirection(startLoc: Location, endLoc: Location): HandpathDirection {
		const key = `${startLoc},${endLoc}`;
		return this.hand_rot_dir_map[key] || STATIC;
	}

	calculateRotatedLocation(startLoc: Location, rotationDirection: HandpathDirection): Location {
		switch (rotationDirection) {
			case CW_SHIFT:
				return this.loc_map_cw[startLoc] || startLoc;
			case CCW_SHIFT:
				return this.loc_map_ccw[startLoc] || startLoc;
			case DASH:
				return this.loc_map_dash[startLoc] || startLoc;
			case STATIC:
			default:
				return this.loc_map_static[startLoc] || startLoc;
		}
	}
}

export const handpathUtils = new HandpathCalculator();
