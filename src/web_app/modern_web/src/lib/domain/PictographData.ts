/**
 * Pictograph Domain Model
 * 
 * Immutable data for a complete pictograph.
 * Based on modern desktop app's pictograph_data.py
 */

import type { ArrowData } from './ArrowData';
import type { PropData } from './PropData';
import type { MotionData } from './MotionData';
import type { GridData } from './GridData';
import { ArrowType, Direction, GridPosition, LetterType, PropType, Timing } from './enums';
import { createArrowData } from './ArrowData';
import { createPropData } from './PropData';
import { createGridData } from './GridData';

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
  readonly metadata: Record<string, any>;
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
  const newArrows = { ...pictograph.arrows, [color]: updatedArrow };

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
  const newProps = { ...pictograph.props, [color]: updatedProp };

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

export function pictographDataToObject(pictograph: PictographData): Record<string, any> {
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

export function pictographDataFromObject(data: Record<string, any>): PictographData {
  return createPictographData({
    id: data.id,
    grid_data: data.grid_data,
    arrows: data.arrows,
    props: data.props,
    motions: data.motions,
    letter: data.letter,
    start_position: data.start_position,
    end_position: data.end_position,
    beat: data.beat,
    timing: data.timing,
    direction: data.direction,
    duration: data.duration,
    letter_type: data.letter_type,
    is_blank: data.is_blank,
    is_mirrored: data.is_mirrored,
    metadata: data.metadata,
  });
}
