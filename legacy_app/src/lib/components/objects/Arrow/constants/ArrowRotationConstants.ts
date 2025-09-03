// src/lib/components/objects/Arrow/constants/ArrowRotationConstants.ts
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
	NO_ROT,
	IN,
	OUT,
	CLOCK,
	COUNTER,
	CW_SHIFT,
	CCW_SHIFT,
	RED,
	BLUE
} from '$lib/types/Constants';
import type { Loc, PropRotDir, Orientation } from '$lib/types/Types';

// Type definitions for rotation maps
export type RotationDirectionMap = {
	[key in Loc]?: number;
};

export type PropRotDirMap = {
	[key in PropRotDir]?: RotationDirectionMap;
};

export type OrientationMap = {
	[key in Orientation]?: PropRotDirMap;
};

export type LocationOverrideMap = {
	[key in Loc]?: number | { [key in PropRotDir]?: number };
};

// Pro motion rotation angles
export const PRO_ROTATION_MAP: PropRotDirMap = {
	[CLOCKWISE]: {
		[NORTH]: 315,
		[EAST]: 45,
		[SOUTH]: 135,
		[WEST]: 225,
		[NORTHEAST]: 0,
		[SOUTHEAST]: 90,
		[SOUTHWEST]: 180,
		[NORTHWEST]: 270
	},
	[COUNTER_CLOCKWISE]: {
		[NORTH]: 45,
		[EAST]: 135,
		[SOUTH]: 225,
		[WEST]: 315,
		[NORTHEAST]: 90,
		[SOUTHEAST]: 180,
		[SOUTHWEST]: 270,
		[NORTHWEST]: 0
	},
	[NO_ROT]: {}
};

// Anti motion rotation angles - regular pattern
export const ANTI_REGULAR_MAP: PropRotDirMap = {
	[CLOCKWISE]: {
		[NORTH]: 45,
		[EAST]: 135,
		[SOUTH]: 225,
		[WEST]: 315,
		[NORTHEAST]: 90,
		[SOUTHEAST]: 180,
		[SOUTHWEST]: 270,
		[NORTHWEST]: 0
	},
	[COUNTER_CLOCKWISE]: {
		[NORTH]: 315,
		[EAST]: 45,
		[SOUTH]: 135,
		[WEST]: 225,
		[NORTHEAST]: 0,
		[SOUTHEAST]: 90,
		[SOUTHWEST]: 180,
		[NORTHWEST]: 270
	},
	[NO_ROT]: {}
};

// Anti motion rotation angles - alternate pattern
export const ANTI_ALT_MAP: PropRotDirMap = {
	[CLOCKWISE]: {
		[NORTH]: 315,
		[EAST]: 225,
		[SOUTH]: 135,
		[WEST]: 45,
		[NORTHEAST]: 270,
		[SOUTHEAST]: 180,
		[SOUTHWEST]: 90,
		[NORTHWEST]: 360
	},
	[COUNTER_CLOCKWISE]: {
		[NORTH]: 315,
		[EAST]: 45,
		[SOUTH]: 135,
		[WEST]: 225,
		[NORTHEAST]: 360,
		[SOUTHEAST]: 90,
		[SOUTHWEST]: 180,
		[NORTHWEST]: 270
	},
	[NO_ROT]: {}
};

// Float motion rotation angles
export const FLOAT_DIRECTION_MAP: { [key: string]: RotationDirectionMap } = {
	[CW_SHIFT]: {
		[NORTH]: 315,
		[EAST]: 45,
		[SOUTH]: 135,
		[WEST]: 225,
		[NORTHEAST]: 0,
		[SOUTHEAST]: 90,
		[SOUTHWEST]: 180,
		[NORTHWEST]: 270
	},
	[CCW_SHIFT]: {
		[NORTH]: 135,
		[EAST]: 225,
		[SOUTH]: 315,
		[WEST]: 45,
		[NORTHEAST]: 180,
		[SOUTHEAST]: 270,
		[SOUTHWEST]: 0,
		[NORTHWEST]: 90
	}
};

// Dash motion with no rotation
export const DASH_NO_ROTATION_MAP: { [key: string]: number } = {
	[`${NORTH}-${SOUTH}`]: 90,
	[`${EAST}-${WEST}`]: 180,
	[`${SOUTH}-${NORTH}`]: 270,
	[`${WEST}-${EAST}`]: 0,
	[`${SOUTHEAST}-${NORTHWEST}`]: 225,
	[`${SOUTHWEST}-${NORTHEAST}`]: 315,
	[`${NORTHWEST}-${SOUTHEAST}`]: 45,
	[`${NORTHEAST}-${SOUTHWEST}`]: 135
};

// Dash motion based on orientation
export const DASH_ORIENTATION_MAP: OrientationMap = {
	[IN]: {
		[CLOCKWISE]: {
			[NORTH]: 0,
			[EAST]: 90,
			[SOUTH]: 180,
			[WEST]: 270,
			[NORTHEAST]: 45,
			[SOUTHEAST]: 135,
			[SOUTHWEST]: 225,
			[NORTHWEST]: 315
		},
		[COUNTER_CLOCKWISE]: {
			[NORTH]: 0,
			[EAST]: 270,
			[SOUTH]: 180,
			[WEST]: 90,
			[NORTHEAST]: 315,
			[SOUTHEAST]: 225,
			[SOUTHWEST]: 135,
			[NORTHWEST]: 45
		},
		[NO_ROT]: {}
	},
	[OUT]: {
		[CLOCKWISE]: {
			[NORTH]: 0,
			[EAST]: 90,
			[SOUTH]: 180,
			[WEST]: 270,
			[NORTHEAST]: 45,
			[SOUTHEAST]: 135,
			[SOUTHWEST]: 225,
			[NORTHWEST]: 315
		},
		[COUNTER_CLOCKWISE]: {
			[NORTH]: 0,
			[EAST]: 270,
			[SOUTH]: 180,
			[WEST]: 90,
			[NORTHEAST]: 315,
			[SOUTHEAST]: 225,
			[SOUTHWEST]: 135,
			[NORTHWEST]: 45
		},
		[NO_ROT]: {}
	},
	[CLOCK]: {
		[CLOCKWISE]: {
			[NORTH]: 0,
			[EAST]: 90,
			[SOUTH]: 180,
			[WEST]: 270,
			[NORTHEAST]: 45,
			[SOUTHEAST]: 135,
			[SOUTHWEST]: 225,
			[NORTHWEST]: 315
		},
		[COUNTER_CLOCKWISE]: {
			[NORTH]: 0,
			[EAST]: 270,
			[SOUTH]: 180,
			[WEST]: 90,
			[NORTHEAST]: 315,
			[SOUTHEAST]: 225,
			[SOUTHWEST]: 135,
			[NORTHWEST]: 45
		},
		[NO_ROT]: {}
	},
	[COUNTER]: {
		[CLOCKWISE]: {
			[NORTH]: 0,
			[EAST]: 90,
			[SOUTH]: 180,
			[WEST]: 270,
			[NORTHEAST]: 45,
			[SOUTHEAST]: 135,
			[SOUTHWEST]: 225,
			[NORTHWEST]: 315
		},
		[COUNTER_CLOCKWISE]: {
			[NORTH]: 0,
			[EAST]: 270,
			[SOUTH]: 180,
			[WEST]: 90,
			[NORTHEAST]: 315,
			[SOUTHEAST]: 225,
			[SOUTHWEST]: 135,
			[NORTHWEST]: 45
		},
		[NO_ROT]: {}
	}
};

// Clockwise dash angle overrides
export const CW_DASH_ANGLE_OVERRIDE_MAP: RotationDirectionMap = {
	[NORTH]: 270,
	[EAST]: 0,
	[SOUTH]: 90,
	[WEST]: 180,
	[NORTHEAST]: 315,
	[SOUTHEAST]: 45,
	[SOUTHWEST]: 135,
	[NORTHWEST]: 225
};

// Counter-clockwise dash angle overrides
export const CCW_DASH_ANGLE_OVERRIDE_MAP: RotationDirectionMap = {
	[NORTH]: 270,
	[EAST]: 180,
	[SOUTH]: 90,
	[WEST]: 0,
	[NORTHEAST]: 225,
	[SOUTHEAST]: 135,
	[SOUTHWEST]: 45,
	[NORTHWEST]: 315
};

// Radial static direction map
export const RADIAL_STATIC_DIRECTION_MAP: PropRotDirMap = {
	[CLOCKWISE]: {
		[NORTH]: 0,
		[EAST]: 90,
		[SOUTH]: 180,
		[WEST]: 270,
		[NORTHEAST]: 45,
		[SOUTHEAST]: 135,
		[SOUTHWEST]: 225,
		[NORTHWEST]: 315
	},
	[COUNTER_CLOCKWISE]: {
		[NORTH]: 0,
		[EAST]: 270,
		[SOUTH]: 180,
		[WEST]: 90,
		[NORTHEAST]: 315,
		[SOUTHEAST]: 225,
		[SOUTHWEST]: 135,
		[NORTHWEST]: 45
	},
	[NO_ROT]: {}
};

// Non-radial static direction map
export const NONRADIAL_STATIC_DIRECTION_MAP: PropRotDirMap = {
	[CLOCKWISE]: {
		[NORTH]: 180,
		[EAST]: 270,
		[SOUTH]: 0,
		[WEST]: 90,
		[NORTHEAST]: 225,
		[SOUTHEAST]: 315,
		[SOUTHWEST]: 45,
		[NORTHWEST]: 135
	},
	[COUNTER_CLOCKWISE]: {
		[NORTH]: 180,
		[EAST]: 90,
		[SOUTH]: 0,
		[WEST]: 270,
		[NORTHEAST]: 135,
		[SOUTHEAST]: 45,
		[SOUTHWEST]: 315,
		[NORTHWEST]: 225
	},
	[NO_ROT]: {}
};

// Static from radial angle override map
export const STATIC_FROM_RADIAL_ANGLE_OVERRIDE_MAP: LocationOverrideMap = {
	[NORTH]: 180,
	[EAST]: { [CLOCKWISE]: 270, [COUNTER_CLOCKWISE]: 90, [NO_ROT]: 0 },
	[SOUTH]: 0,
	[WEST]: { [CLOCKWISE]: 90, [COUNTER_CLOCKWISE]: 270, [NO_ROT]: 0 },
	[NORTHEAST]: { [CLOCKWISE]: 225, [COUNTER_CLOCKWISE]: 135, [NO_ROT]: 0 },
	[SOUTHEAST]: { [CLOCKWISE]: 315, [COUNTER_CLOCKWISE]: 45, [NO_ROT]: 0 },
	[SOUTHWEST]: { [CLOCKWISE]: 45, [COUNTER_CLOCKWISE]: 315, [NO_ROT]: 0 },
	[NORTHWEST]: { [CLOCKWISE]: 135, [COUNTER_CLOCKWISE]: 225, [NO_ROT]: 0 }
};

// Static from non-radial angle override map
export const STATIC_FROM_NONRADIAL_ANGLE_OVERRIDE_MAP: LocationOverrideMap = {
	[NORTH]: 0,
	[EAST]: { [CLOCKWISE]: 90, [COUNTER_CLOCKWISE]: 270, [NO_ROT]: 0 },
	[SOUTH]: 180,
	[WEST]: { [CLOCKWISE]: 270, [COUNTER_CLOCKWISE]: 90, [NO_ROT]: 0 },
	[NORTHEAST]: { [CLOCKWISE]: 45, [COUNTER_CLOCKWISE]: 315, [NO_ROT]: 0 },
	[SOUTHEAST]: { [CLOCKWISE]: 135, [COUNTER_CLOCKWISE]: 225, [NO_ROT]: 0 },
	[SOUTHWEST]: { [CLOCKWISE]: 225, [COUNTER_CLOCKWISE]: 135, [NO_ROT]: 0 },
	[NORTHWEST]: { [CLOCKWISE]: 315, [COUNTER_CLOCKWISE]: 45, [NO_ROT]: 0 }
};

// Phi Dash and Psi Dash angle map
// These are derived from the Python PHI_DASH_PSI_DASH_LOCATION_MAP with corresponding rotation angles
export const PHI_DASH_PSI_DASH_ANGLE_MAP: { [key: string]: number } = {
	[`${RED}_${NORTH}_${SOUTH}`]: 90,
	[`${RED}_${EAST}_${WEST}`]: 0,
	[`${RED}_${SOUTH}_${NORTH}`]: 90,
	[`${RED}_${WEST}_${EAST}`]: 0,
	[`${BLUE}_${NORTH}_${SOUTH}`]: 270,
	[`${BLUE}_${EAST}_${WEST}`]: 180,
	[`${BLUE}_${SOUTH}_${NORTH}`]: 270,
	[`${BLUE}_${WEST}_${EAST}`]: 180,
	[`${RED}_${NORTHWEST}_${SOUTHEAST}`]: 45,
	[`${RED}_${NORTHEAST}_${SOUTHWEST}`]: 135,
	[`${RED}_${SOUTHWEST}_${NORTHEAST}`]: 135,
	[`${RED}_${SOUTHEAST}_${NORTHWEST}`]: 45,
	[`${BLUE}_${NORTHWEST}_${SOUTHEAST}`]: 225,
	[`${BLUE}_${NORTHEAST}_${SOUTHWEST}`]: 315,
	[`${BLUE}_${SOUTHWEST}_${NORTHEAST}`]: 315,
	[`${BLUE}_${SOUTHEAST}_${NORTHWEST}`]: 225
};

// Lambda Zero Turns angle map
// Based on Python's LAMBDA_ZERO_TURNS_LOCATION_MAP with rotation angles
export const LAMBDA_ZERO_TURNS_ANGLE_MAP: { [key: string]: number } = {
	[`${NORTH}_${SOUTH}_${WEST}`]: 90,
	[`${EAST}_${WEST}_${SOUTH}`]: 0,
	[`${NORTH}_${SOUTH}_${EAST}`]: 270,
	[`${WEST}_${EAST}_${SOUTH}`]: 0,
	[`${SOUTH}_${NORTH}_${WEST}`]: 90,
	[`${EAST}_${WEST}_${NORTH}`]: 180,
	[`${SOUTH}_${NORTH}_${EAST}`]: 270,
	[`${WEST}_${EAST}_${NORTH}`]: 180,
	[`${NORTHEAST}_${SOUTHWEST}_${NORTHWEST}`]: 135,
	[`${NORTHWEST}_${SOUTHEAST}_${NORTHEAST}`]: 225,
	[`${SOUTHWEST}_${NORTHEAST}_${SOUTHEAST}`]: 315,
	[`${SOUTHEAST}_${NORTHWEST}_${SOUTHWEST}`]: 45,
	[`${NORTHEAST}_${SOUTHWEST}_${SOUTHEAST}`]: 315,
	[`${NORTHWEST}_${SOUTHEAST}_${SOUTHWEST}`]: 45,
	[`${SOUTHWEST}_${NORTHEAST}_${NORTHWEST}`]: 135,
	[`${SOUTHEAST}_${NORTHWEST}_${NORTHEAST}`]: 225
};

// Diamond Dash angle map
// Translated from Python's DIAMOND_DASH_LOCATION_MAP
export const DIAMOND_DASH_ANGLE_MAP: { [key: string]: number } = {
	[`${NORTH}_${NORTHWEST}`]: 90,
	[`${NORTH}_${NORTHEAST}`]: 270,
	[`${NORTH}_${SOUTHEAST}`]: 270,
	[`${NORTH}_${SOUTHWEST}`]: 90,
	[`${EAST}_${NORTHWEST}`]: 180,
	[`${EAST}_${NORTHEAST}`]: 180,
	[`${EAST}_${SOUTHEAST}`]: 0,
	[`${EAST}_${SOUTHWEST}`]: 0,
	[`${SOUTH}_${NORTHWEST}`]: 90,
	[`${SOUTH}_${NORTHEAST}`]: 270,
	[`${SOUTH}_${SOUTHEAST}`]: 270,
	[`${SOUTH}_${SOUTHWEST}`]: 270,
	[`${WEST}_${NORTHWEST}`]: 180,
	[`${WEST}_${NORTHEAST}`]: 180,
	[`${WEST}_${SOUTHEAST}`]: 0,
	[`${WEST}_${SOUTHWEST}`]: 0
};

// Box Dash angle map
// Translated from Python's BOX_DASH_LOCATION_MAP
export const BOX_DASH_ANGLE_MAP: { [key: string]: number } = {
	[`${NORTHEAST}_${NORTH}`]: 135,
	[`${NORTHEAST}_${EAST}`]: 315,
	[`${NORTHEAST}_${SOUTH}`]: 315,
	[`${NORTHEAST}_${WEST}`]: 135,
	[`${SOUTHEAST}_${NORTH}`]: 225,
	[`${SOUTHEAST}_${EAST}`]: 225,
	[`${SOUTHEAST}_${SOUTH}`]: 45,
	[`${SOUTHEAST}_${WEST}`]: 45,
	[`${SOUTHWEST}_${NORTH}`]: 135,
	[`${SOUTHWEST}_${EAST}`]: 315,
	[`${SOUTHWEST}_${SOUTH}`]: 315,
	[`${SOUTHWEST}_${WEST}`]: 135,
	[`${NORTHWEST}_${NORTH}`]: 225,
	[`${NORTHWEST}_${EAST}`]: 225,
	[`${NORTHWEST}_${SOUTH}`]: 45,
	[`${NORTHWEST}_${WEST}`]: 45
};

// Opposite location map for retrieving opposite directions
export const OPPOSITE_LOCATION_MAP: { [key: string]: Loc } = {
	[NORTH]: SOUTH,
	[SOUTH]: NORTH,
	[EAST]: WEST,
	[WEST]: EAST,
	[NORTHEAST]: SOUTHWEST,
	[SOUTHWEST]: NORTHEAST,
	[SOUTHEAST]: NORTHWEST,
	[NORTHWEST]: SOUTHEAST
};
