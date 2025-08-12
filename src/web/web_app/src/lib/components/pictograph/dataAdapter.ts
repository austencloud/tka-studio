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
	MotionData,
} from '$lib/domain';
import { createMotionData } from '$lib/domain';
import {
	ArrowType,
	Direction,
	GridMode,
	GridPosition,
	LetterType,
	Orientation,
	PropType,
	RotationDirection,
	Timing,
} from '$lib/domain/enums';
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
			blue:
				(legacy as { motions?: { blue?: MotionData } }).motions?.blue || createMotionData(),
			red: (legacy as { motions?: { red?: MotionData } }).motions?.red || createMotionData(),
		},
		letter: legacy.letter !== undefined ? legacy.letter : null,
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
		letter: modern.letter || null,
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
export function legacyToModernArrowData(
	legacy: Record<string, unknown>,
	color: 'blue' | 'red'
): ModernArrowData {
	// Calculate the correct arrow location based on start/end positions
	const calculatedLocation = calculateArrowLocation({
		start_loc: (legacy.startLoc as string) || (legacy.start_loc as string) || '',
		end_loc: (legacy.endLoc as string) || (legacy.end_loc as string) || '',
		motion_type: (legacy.motionType as string) || (legacy.motion_type as string) || 'static',
	});

	return {
		id: (legacy.id as string) || crypto.randomUUID(),
		arrow_type: color === 'blue' ? ArrowType.BLUE : ArrowType.RED,
		color,
		motion_type: (legacy.motionType as string) || (legacy.motion_type as string) || 'static',
		location:
			calculatedLocation || (legacy.loc as string) || (legacy.location as string) || 'center',
		start_orientation:
			(legacy.startOri as string) || (legacy.start_orientation as string) || 'in',
		end_orientation: (legacy.endOri as string) || (legacy.end_orientation as string) || 'in',
		rotation_direction:
			(legacy.propRotDir as string) || (legacy.rotation_direction as string) || 'clockwise',
		turns: (legacy.turns as number) || 0,
		is_mirrored: (legacy.svgMirrored as boolean) || (legacy.is_mirrored as boolean) || false,
		position_x:
			(legacy.coords as { x?: number })?.x || (legacy.coordinates as { x?: number })?.x || 0,
		position_y:
			(legacy.coords as { y?: number })?.y || (legacy.coordinates as { y?: number })?.y || 0,
		rotation_angle: (legacy.rotAngle as number) || (legacy.rotation_angle as number) || 0,
		coordinates:
			(legacy.coords as { x: number; y: number }) ||
			(legacy.coordinates as { x: number; y: number }) ||
			null,
		svg_center:
			(legacy.svgCenter as { x: number; y: number }) ||
			(legacy.svg_center as { x: number; y: number }) ||
			null,
		svg_mirrored: (legacy.svgMirrored as boolean) || (legacy.svg_mirrored as boolean) || false,
		is_visible: legacy.is_visible !== undefined ? (legacy.is_visible as boolean) : true,
		is_selected: (legacy.is_selected as boolean) || false,
	};
}

/**
 * Convert legacy prop data to modern structure
 */
export function legacyToModernPropData(
	legacy: Record<string, unknown>,
	color: 'blue' | 'red'
): ModernPropData {
	return {
		id: (legacy.id as string) || crypto.randomUUID(),
		prop_type:
			(legacy.propType as PropType) || (legacy.prop_type as PropType) || PropType.STAFF,
		color,
		orientation:
			(legacy.ori as Orientation) || (legacy.orientation as Orientation) || Orientation.IN,
		rotation_direction:
			(legacy.rotDir as RotationDirection) ||
			(legacy.rotation_direction as RotationDirection) ||
			RotationDirection.NO_ROTATION,
		location: (legacy.loc as string) || (legacy.location as string) || 'center',
		position_x:
			(legacy.coords as { x?: number })?.x || (legacy.coordinates as { x?: number })?.x || 0,
		position_y:
			(legacy.coords as { y?: number })?.y || (legacy.coordinates as { y?: number })?.y || 0,
		rotation_angle: (legacy.rotAngle as number) || (legacy.rotation_angle as number) || 0,
		coordinates:
			(legacy.coords as { x: number; y: number }) ||
			(legacy.coordinates as { x: number; y: number }) ||
			null,
		svg_center:
			(legacy.svgCenter as { x: number; y: number }) ||
			(legacy.svg_center as { x: number; y: number }) ||
			null,
		is_visible: legacy.is_visible !== undefined ? (legacy.is_visible as boolean) : true,
		is_selected: (legacy.is_selected as boolean) || false,
	};
}

/**
 * Extract arrow data from legacy pictograph structure (direct properties)
 */
export function extractLegacyArrowData(legacy: Record<string, unknown>): {
	blue: ModernArrowData | null;
	red: ModernArrowData | null;
} {
	const blue =
		(legacy.blueArrowData as Record<string, unknown>) ||
		(legacy.blue_arrow_data as Record<string, unknown>) ||
		null;
	const red =
		(legacy.redArrowData as Record<string, unknown>) ||
		(legacy.red_arrow_data as Record<string, unknown>) ||
		null;

	return {
		blue: blue ? legacyToModernArrowData(blue, 'blue') : null,
		red: red ? legacyToModernArrowData(red, 'red') : null,
	};
}

/**
 * Extract prop data from legacy pictograph structure (direct properties)
 */
export function extractLegacyPropData(legacy: Record<string, unknown>): {
	blue: ModernPropData | null;
	red: ModernPropData | null;
} {
	const blue =
		(legacy.bluePropData as Record<string, unknown>) ||
		(legacy.blue_prop_data as Record<string, unknown>) ||
		null;
	const red =
		(legacy.redPropData as Record<string, unknown>) ||
		(legacy.red_prop_data as Record<string, unknown>) ||
		null;

	return {
		blue: blue ? legacyToModernPropData(blue, 'blue') : null,
		red: red ? legacyToModernPropData(red, 'red') : null,
	};
}

/**
 * Convert any pictograph data (legacy or modern) to modern structure
 */
export function ensureModernPictographData(
	data: Record<string, unknown>
): ModernPictographData | null {
	if (!data) return null;

	// If it already looks like modern data (has grid_data property)
	if (data.grid_data && data.arrows && data.props && typeof data.id === 'string') {
		return data as unknown as ModernPictographData;
	}

	// If it looks like legacy data with direct properties
	if (data.redArrowData || data.blueArrowData || data.redPropData || data.bluePropData) {
		const arrows = extractLegacyArrowData(data);
		const props = extractLegacyPropData(data);

		return {
			id: typeof data.id === 'string' ? data.id : crypto.randomUUID(),
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
					(data.blueMotionData as MotionData) ||
					(data.blue_motion_data as MotionData) ||
					createMotionData(),
				red:
					(data.redMotionData as MotionData) ||
					(data.red_motion_data as MotionData) ||
					createMotionData(),
			},
			letter: typeof data.letter === 'string' ? data.letter : null,
			start_position:
				typeof data.startPos === 'string'
					? (data.startPos as GridPosition)
					: typeof data.start_position === 'string'
						? (data.start_position as GridPosition)
						: null,
			end_position:
				typeof data.endPos === 'string'
					? (data.endPos as GridPosition)
					: typeof data.end_position === 'string'
						? (data.end_position as GridPosition)
						: null,
			beat: typeof data.beat === 'number' ? data.beat : 0,
			timing: typeof data.timing === 'string' ? (data.timing as Timing) : null,
			direction: typeof data.direction === 'string' ? (data.direction as Direction) : null,
			duration: typeof data.duration === 'number' ? data.duration : null,
			letter_type:
				typeof data.letter_type === 'string' ? (data.letter_type as LetterType) : null,
			is_blank: typeof data.is_blank === 'boolean' ? data.is_blank : false,
			is_mirrored: typeof data.is_mirrored === 'boolean' ? data.is_mirrored : false,
			metadata:
				typeof data.metadata === 'object' && data.metadata !== null
					? (data.metadata as Record<string, unknown>)
					: {},
		};
	}

	// If it's from the service interfaces
	if (data.arrows || data.props) {
		return legacyToModernPictographData(data as unknown as LegacyPictographData);
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
