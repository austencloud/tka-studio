/**
 * Pictograph Domain Model
 *
 * Immutable data for a complete pictograph.
 * Based on modern desktop app's pictograph_data.py
 */

import type { ArrowData } from './ArrowData';
import { createArrowData } from './ArrowData';
import type { GridData } from './GridData';
import { createGridData } from './GridData';
import type { MotionData } from './MotionData';
import type { PropData } from './PropData';
import { createPropData } from './PropData';
import { ArrowType, Direction, GridPosition, LetterType, Timing } from './enums';

export interface PictographData {
	// Core identity
	readonly id: string;

	// Grid configuration
	readonly grid_data: GridData;

	// Arrows, props, and motions (consistent dictionary approach)
	readonly arrows: Record<string, ArrowData>; // "blue", "red"
	readonly props: Record<string, PropData>; // "blue", "red"
	readonly motions: Record<string, MotionData>; // "blue", "red"

	// Letter and position data
	readonly letter?: string | null;
	readonly start_position?: GridPosition | null;
	readonly end_position?: GridPosition | null;

	// Legacy compatibility properties
	readonly start_pos?: string | null;
	readonly end_pos?: string | null;
	readonly grid_mode?: string | null;

	// Letter determination fields
	readonly beat: number;
	readonly timing?: Timing | null;
	readonly direction?: Direction | null;
	readonly duration?: number | null;
	readonly letter_type?: LetterType | null;

	// Visual state
	readonly is_blank: boolean;
	readonly is_mirrored: boolean;

	// Metadata
	readonly metadata: Record<string, unknown>;
}

export function createPictographData(data: Partial<PictographData> = {}): PictographData {
	// Ensure we have blue and red arrows
	const arrows = {
		blue: createArrowData({ arrow_type: ArrowType.BLUE, color: 'blue' }),
		red: createArrowData({ arrow_type: ArrowType.RED, color: 'red' }),
		...data.arrows,
	};

	// Ensure we have blue and red props
	const props = {
		blue: createPropData({ color: 'blue' }),
		red: createPropData({ color: 'red' }),
		...data.props,
	};

	return {
		id: data.id ?? crypto.randomUUID(),
		grid_data: data.grid_data ?? createGridData(),
		arrows,
		props,
		motions: data.motions ?? {},
		letter: data.letter ?? null,
		start_position: data.start_position ?? null,
		end_position: data.end_position ?? null,
		beat: data.beat ?? 0,
		timing: data.timing ?? null,
		direction: data.direction ?? null,
		duration: data.duration ?? null,
		letter_type: data.letter_type ?? null,
		is_blank: data.is_blank ?? false,
		is_mirrored: data.is_mirrored ?? false,
		metadata: data.metadata ?? {},
	};
}

export function updatePictographData(
	pictograph: PictographData,
	updates: Partial<PictographData>
): PictographData {
	return {
		...pictograph,
		...updates,
	};
}

export function updateArrow(
	pictograph: PictographData,
	color: string,
	updates: Partial<ArrowData>
): PictographData {
	if (!(color in pictograph.arrows)) {
		throw new Error(`Arrow color '${color}' not found`);
	}

	const currentArrow = pictograph.arrows[color];
	const updatedArrow = { ...currentArrow, ...updates };
	const newArrows = { ...pictograph.arrows, [color]: updatedArrow } as Record<string, ArrowData>;
	return { ...pictograph, arrows: newArrows };
}

export function updateProp(
	pictograph: PictographData,
	color: string,
	updates: Partial<PropData>
): PictographData {
	if (!(color in pictograph.props)) {
		throw new Error(`Prop color '${color}' not found`);
	}

	const currentProp = pictograph.props[color];
	const updatedProp = { ...currentProp, ...updates };
	const newProps = { ...pictograph.props, [color]: updatedProp } as Record<string, PropData>;
	return { ...pictograph, props: newProps };
}

// Convenience getters
export function getBlueArrow(pictograph: PictographData): ArrowData {
	return pictograph.arrows.blue ?? createArrowData({ arrow_type: ArrowType.BLUE, color: 'blue' });
}

export function getRedArrow(pictograph: PictographData): ArrowData {
	return pictograph.arrows.red ?? createArrowData({ arrow_type: ArrowType.RED, color: 'red' });
}

export function getBlueProp(pictograph: PictographData): PropData {
	return pictograph.props.blue ?? createPropData({ color: 'blue' });
}

export function getRedProp(pictograph: PictographData): PropData {
	return pictograph.props.red ?? createPropData({ color: 'red' });
}

export function pictographDataToObject(pictograph: PictographData): Record<string, unknown> {
	return {
		id: pictograph.id,
		grid_data: pictograph.grid_data,
		arrows: pictograph.arrows,
		props: pictograph.props,
		motions: pictograph.motions,
		letter: pictograph.letter,
		start_position: pictograph.start_position,
		end_position: pictograph.end_position,
		beat: pictograph.beat,
		timing: pictograph.timing,
		direction: pictograph.direction,
		duration: pictograph.duration,
		letter_type: pictograph.letter_type,
		is_blank: pictograph.is_blank,
		is_mirrored: pictograph.is_mirrored,
		metadata: pictograph.metadata,
	};
}

export function pictographDataFromObject(data: Record<string, unknown>): PictographData {
	// eslint-disable-next-line @typescript-eslint/no-explicit-any
	const partialData: any = {};

	if (data.id !== undefined) {
		partialData.id = data.id;
	}
	if (data.grid_data !== undefined) {
		partialData.grid_data = data.grid_data;
	}
	if (data.arrows !== undefined) {
		partialData.arrows = data.arrows;
	}
	if (data.props !== undefined) {
		partialData.props = data.props;
	}
	if (data.motions !== undefined) {
		partialData.motions = data.motions;
	}
	if (data.letter !== undefined) {
		partialData.letter = data.letter;
	}
	if (data.start_position !== undefined) {
		partialData.start_position = data.start_position;
	}
	if (data.end_position !== undefined) {
		partialData.end_position = data.end_position;
	}
	if (data.beat !== undefined) {
		partialData.beat = data.beat;
	}
	if (data.timing !== undefined) {
		partialData.timing = data.timing;
	}
	if (data.direction !== undefined) {
		partialData.direction = data.direction;
	}
	if (data.duration !== undefined) {
		partialData.duration = data.duration;
	}
	if (data.letter_type !== undefined) {
		partialData.letter_type = data.letter_type;
	}
	if (data.is_blank !== undefined) {
		partialData.is_blank = data.is_blank;
	}
	if (data.is_mirrored !== undefined) {
		partialData.is_mirrored = data.is_mirrored;
	}
	if (data.metadata !== undefined) {
		partialData.metadata = data.metadata;
	}

	return createPictographData(partialData);
}
