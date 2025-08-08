/**
 * Prop Domain Model
 * 
 * Immutable data for a prop in a pictograph.
 * Based on modern desktop app's prop_data.py
 */

import { Orientation, PropType, RotationDirection } from './enums';

export interface PropData {
  readonly id: string;
  readonly prop_type: PropType;
  readonly color: string;
  readonly orientation: Orientation;
  readonly rotation_direction: RotationDirection;

  // Position data (calculated by positioning system)
  readonly location?: string | null;
  readonly position_x: number;
  readonly position_y: number;

  // State flags
  readonly is_visible: boolean;
  readonly is_selected: boolean;
}

export function createPropData(data: Partial<PropData> = {}): PropData {
  return {
    id: data.id ?? crypto.randomUUID(),
    prop_type: data.prop_type ?? PropType.STAFF,
    color: data.color ?? 'blue',
    orientation: data.orientation ?? Orientation.IN,
    rotation_direction: data.rotation_direction ?? RotationDirection.NO_ROTATION,
    location: data.location ?? null,
    position_x: data.position_x ?? 0.0,
    position_y: data.position_y ?? 0.0,
    is_visible: data.is_visible ?? true,
    is_selected: data.is_selected ?? false,
  };
}

export function updatePropData(prop: PropData, updates: Partial<PropData>): PropData {
  return {
    ...prop,
    ...updates,
  };
}

export function propDataToObject(prop: PropData): Record<string, any> {
  return {
    id: prop.id,
    prop_type: prop.prop_type,
    color: prop.color,
    orientation: prop.orientation,
    rotation_direction: prop.rotation_direction,
    location: prop.location,
    position_x: prop.position_x,
    position_y: prop.position_y,
    is_visible: prop.is_visible,
    is_selected: prop.is_selected,
  };
}

export function propDataFromObject(data: Record<string, any>): PropData {
  return createPropData({
    id: data.id,
    prop_type: data.prop_type,
    color: data.color,
    orientation: data.orientation,
    rotation_direction: data.rotation_direction,
    location: data.location,
    position_x: data.position_x,
    position_y: data.position_y,
    is_visible: data.is_visible,
    is_selected: data.is_selected,
  });
}
