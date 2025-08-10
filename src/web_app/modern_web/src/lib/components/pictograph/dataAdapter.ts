/**
 * Data Structure Bridge - Legacy to Modern Adapter
 *
 * This module provides functions to convert between legacy pictograph data
 * structures (used by services) and modern domain structures (used by components).
 */

import type {
	ArrowData as ModernArrowData,
	BeatData as ModernBeatData,
	PictographData as ModernPictographData,
	PropData as ModernPropData,
} from '$lib/domain';
import { createMotionData } from '$lib/domain';
import { ArrowType, GridMode, Orientation, PropType, RotationDirection } from '$lib/domain/enums';
import type { PictographData as LegacyPictographData } from '$lib/services/interfaces';
import { calculateArrowLocation } from './utils/arrowLocationCalculator';

/**
 * Convert legacy pictograph data to modern domain structure
 */
export function legacyToModernPictographData(legacy: LegacyPictographData): ModernPictographData {
	return {
		id: legacy.id,
		grid_data: {
			grid_mode: GridMode.DIAMOND, // Default, could be extracted from legacy if available
			center_x: 0,
			center_y: 0,
			radius: 100,
			grid_points: {},
		},
		arrows: {
			blue: legacy.arrows?.blue || createEmptyModernArrowData('blue'),
			red: legacy.arrows?.red || createEmptyModernArrowData('red'),
		},
		props: {
			blue: legacy.props?.blue || createEmptyModernPropData('blue'),
			red: legacy.props?.red || createEmptyModernPropData('red'),
		},
		motions: {
			blue: (legacy as any).motions?.blue || createMotionData(),
			red: (legacy as any).motions?.red || createMotionData(),
		},
		letter: legacy.letter ?? null,
		start_position: null, // Map if available in legacy
		end_position: null, // Map if available in legacy
		beat: 0, // Map if available in legacy
		timing: null, // Map if available in legacy
		direction: null, // Map if available in legacy
		duration: null, // Map if available in legacy
		letter_type: null, // Map if available in legacy
		is_blank: false, // Map if available in legacy
		is_mirrored: false, // Map if available in legacy
		metadata: {},
	};
}

/**
 * Convert modern pictograph data to legacy structure (for service compatibility)
 */
export function modernToLegacyPictographData(modern: ModernPictographData): LegacyPictographData {
	return {
		id: modern.id,
		grid_data: modern.grid_data,
		arrows: modern.arrows,
		props: modern.props,
		motions: modern.motions,
		letter: modern.letter,
		beat: modern.beat,
		is_blank: modern.is_blank,
		is_mirrored: modern.is_mirrored,
		metadata: modern.metadata,
	};
}

/**
 * Convert beat data to pictograph data for rendering
 */
export function beatDataToPictographData(beat: ModernBeatData): ModernPictographData | null {
	if (!beat.pictograph_data) {
		return null;
	}

	return beat.pictograph_data;
}

/**
 * Create empty arrow data with proper defaults
 */
function createEmptyModernArrowData(color: 'blue' | 'red'): ModernArrowData {
	return {
		id: crypto.randomUUID(),
		arrow_type: color === 'blue' ? ArrowType.BLUE : ArrowType.RED,
		color,
		motion_type: 'static',
		location: 'center',
		start_orientation: 'in',
		end_orientation: 'in',
		rotation_direction: 'clockwise',
		turns: 0,
		is_mirrored: false,
		position_x: 0,
		position_y: 0,
		rotation_angle: 0,
		coordinates: null,
		svg_center: null,
		svg_mirrored: false,
		is_visible: true,
		is_selected: false,
	};
}

/**
 * Create empty prop data with proper defaults
 */
function createEmptyModernPropData(color: 'blue' | 'red'): ModernPropData {
	return {
		id: crypto.randomUUID(),
		prop_type: PropType.STAFF,
		color,
		orientation: Orientation.IN,
		rotation_direction: RotationDirection.NO_ROTATION,
		location: 'center',
		position_x: 0,
		position_y: 0,
		rotation_angle: 0,
		coordinates: null,
		svg_center: null,
		is_visible: true,
		is_selected: false,
	};
}

/**
 * Convert legacy arrow data to modern structure with calculated location
 */
export function legacyToModernArrowData(legacy: any, color: 'blue' | 'red'): ModernArrowData {
	// Calculate the correct arrow location based on start/end positions
	const calculatedLocation = calculateArrowLocation({
		start_loc: legacy.startLoc || legacy.start_loc || '',
		end_loc: legacy.endLoc || legacy.end_loc || '',
		motion_type: legacy.motionType || legacy.motion_type || 'static',
	});

	return {
		id: legacy.id || crypto.randomUUID(),
		arrow_type: color === 'blue' ? ArrowType.BLUE : ArrowType.RED,
		color,
		motion_type: legacy.motionType || legacy.motion_type || 'static',
		location: calculatedLocation || legacy.loc || legacy.location || 'center',
		start_orientation: legacy.startOri || legacy.start_orientation || 'in',
		end_orientation: legacy.endOri || legacy.end_orientation || 'in',
		rotation_direction: legacy.propRotDir || legacy.rotation_direction || 'clockwise',
		turns: legacy.turns || 0,
		is_mirrored: legacy.svgMirrored || legacy.is_mirrored || false,
		position_x: legacy.coords?.x || legacy.coordinates?.x || 0,
		position_y: legacy.coords?.y || legacy.coordinates?.y || 0,
		rotation_angle: legacy.rotAngle || legacy.rotation_angle || 0,
		coordinates: legacy.coords || legacy.coordinates || null,
		svg_center: legacy.svgCenter || legacy.svg_center || null,
		svg_mirrored: legacy.svgMirrored || legacy.svg_mirrored || false,
		is_visible: legacy.is_visible !== undefined ? legacy.is_visible : true,
		is_selected: legacy.is_selected || false,
	};
}

/**
 * Convert legacy prop data to modern structure
 */
export function legacyToModernPropData(legacy: any, color: 'blue' | 'red'): ModernPropData {
	return {
		id: legacy.id || crypto.randomUUID(),
		prop_type: legacy.propType || legacy.prop_type || PropType.STAFF,
		color,
		orientation: legacy.ori || legacy.orientation || Orientation.IN,
		rotation_direction:
			legacy.rotDir || legacy.rotation_direction || RotationDirection.NO_ROTATION,
		location: legacy.loc || legacy.location || 'center',
		position_x: legacy.coords?.x || legacy.coordinates?.x || 0,
		position_y: legacy.coords?.y || legacy.coordinates?.y || 0,
		rotation_angle: legacy.rotAngle || legacy.rotation_angle || 0,
		coordinates: legacy.coords || legacy.coordinates || null,
		svg_center: legacy.svgCenter || legacy.svg_center || null,
		is_visible: legacy.is_visible !== undefined ? legacy.is_visible : true,
		is_selected: legacy.is_selected || false,
	};
}

/**
 * Extract arrow data from legacy pictograph structure (direct properties)
 */
export function extractLegacyArrowData(legacy: any): {
	blue: ModernArrowData | null;
	red: ModernArrowData | null;
} {
	const blue = legacy.blueArrowData || legacy.blue_arrow_data || null;
	const red = legacy.redArrowData || legacy.red_arrow_data || null;

	return {
		blue: blue ? legacyToModernArrowData(blue, 'blue') : null,
		red: red ? legacyToModernArrowData(red, 'red') : null,
	};
}

/**
 * Extract prop data from legacy pictograph structure (direct properties)
 */
export function extractLegacyPropData(legacy: any): {
	blue: ModernPropData | null;
	red: ModernPropData | null;
} {
	const blue = legacy.bluePropData || legacy.blue_prop_data || null;
	const red = legacy.redPropData || legacy.red_prop_data || null;

	return {
		blue: blue ? legacyToModernPropData(blue, 'blue') : null,
		red: red ? legacyToModernPropData(red, 'red') : null,
	};
}

/**
 * Convert any pictograph data (legacy or modern) to modern structure
 */
export function ensureModernPictographData(data: any): ModernPictographData | null {
	if (!data) return null;

	// If it already looks like modern data (has grid_data property)
	if (data.grid_data && data.arrows && data.props) {
		return data as ModernPictographData;
	}

	// If it looks like legacy data with direct properties
	if (data.redArrowData || data.blueArrowData || data.redPropData || data.bluePropData) {
		const arrows = extractLegacyArrowData(data);
		const props = extractLegacyPropData(data);

		return {
			id: data.id || crypto.randomUUID(),
			grid_data: {
				grid_mode: (data.gridMode || data.grid_mode || GridMode.DIAMOND) as GridMode,
				center_x: 0,
				center_y: 0,
				radius: 100,
				grid_points: {},
			},
			arrows: {
				blue: arrows.blue || createEmptyModernArrowData('blue'),
				red: arrows.red || createEmptyModernArrowData('red'),
			},
			props: {
				blue: props.blue || createEmptyModernPropData('blue'),
				red: props.red || createEmptyModernPropData('red'),
			},
			motions: {
				blue:
					data.blueMotionData ||
					data.blue_motion_data ||
					data.motions?.blue ||
					createMotionData(),
				red:
					data.redMotionData ||
					data.red_motion_data ||
					data.motions?.red ||
					createMotionData(),
			},
			letter: data.letter,
			start_position: data.startPos || data.start_position || null,
			end_position: data.endPos || data.end_position || null,
			beat: data.beat || 0,
			timing: data.timing || null,
			direction: data.direction || null,
			duration: data.duration || null,
			letter_type: data.letter_type || null,
			is_blank: data.is_blank || false,
			is_mirrored: data.is_mirrored || false,
			metadata: data.metadata || {},
		};
	}

	// If it's from the service interfaces
	if (data.arrows || data.props) {
		return legacyToModernPictographData(data);
	}

	return null;
}

/**
 * Debug helper to log data structure differences
 */
export function debugDataStructure(data: unknown, label: string = 'Data'): void {
	// Runtime type inspection only (debug utility)
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	const d = data as any;
	console.group(`🔍 ${label} Structure Analysis`);
	console.log('Raw data:', d);
	console.log('Has grid_data (modern):', !!d?.grid_data);
	console.log('Has gridMode (legacy):', !!d?.gridMode);
	console.log('Has arrows dict (modern):', !!d?.arrows);
	console.log('Has redArrowData (legacy):', !!d?.redArrowData);
	console.log('Has props dict (modern):', !!d?.props);
	console.log('Has redPropData (legacy):', !!d?.redPropData);

	const modern = ensureModernPictographData(d);
	console.log('Converted to modern:', modern);
	console.groupEnd();
}
