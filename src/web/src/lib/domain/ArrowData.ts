/**
 * Arrow Domain Model
 *
 * Immutable data for an arrow in a pictograph.
 * Based on modern desktop app's arrow_data.py
 */

import { ArrowType } from "./enums";

export interface ArrowData {
  readonly id: string;
  readonly arrow_type: ArrowType;
  readonly color: string;
  readonly turns: number;
  readonly is_mirrored: boolean;

  // Motion properties
  readonly motion_type: string;
  readonly start_orientation: string;
  readonly end_orientation: string;
  readonly rotation_direction: string;

  // Position data (calculated by positioning system)
  readonly location?: string | null;
  readonly position_x: number;
  readonly position_y: number;
  readonly rotation_angle: number;
  readonly coordinates?: { x: number; y: number } | null;
  readonly svg_center?: { x: number; y: number } | null;
  readonly svg_mirrored?: boolean;

  // State flags
  readonly is_visible: boolean;
  readonly is_selected: boolean;
}

export function createArrowData(data: Partial<ArrowData> = {}): ArrowData {
  return {
    id: data.id ?? crypto.randomUUID(),
    arrow_type: data.arrow_type ?? ArrowType.BLUE,
    color: data.color ?? "blue",
    turns: data.turns ?? 0.0,
    is_mirrored: data.is_mirrored ?? false,
    motion_type: data.motion_type ?? "static",
    start_orientation: data.start_orientation ?? "in",
    end_orientation: data.end_orientation ?? "in",
    rotation_direction: data.rotation_direction ?? "clockwise",
    location: data.location ?? null,
    position_x: data.position_x ?? 0.0,
    position_y: data.position_y ?? 0.0,
    rotation_angle: data.rotation_angle ?? 0.0,
    coordinates: data.coordinates ?? null,
    svg_center: data.svg_center ?? null,
    svg_mirrored: data.svg_mirrored ?? false,
    is_visible: data.is_visible ?? true,
    is_selected: data.is_selected ?? false,
  };
}

export function updateArrowData(
  arrow: ArrowData,
  updates: Partial<ArrowData>,
): ArrowData {
  return {
    ...arrow,
    ...updates,
  };
}

export function arrowDataToObject(arrow: ArrowData): Record<string, unknown> {
  return {
    id: arrow.id,
    arrow_type: arrow.arrow_type,
    color: arrow.color,
    turns: arrow.turns,
    is_mirrored: arrow.is_mirrored,
    location: arrow.location,
    position_x: arrow.position_x,
    position_y: arrow.position_y,
    rotation_angle: arrow.rotation_angle,
    is_visible: arrow.is_visible,
    is_selected: arrow.is_selected,
  };
}

export function arrowDataFromObject(data: Record<string, unknown>): ArrowData {
  const partialData: Record<string, unknown> = {};

  if (typeof data.id === "string") partialData.id = data.id;
  if (data.arrow_type) partialData.arrow_type = data.arrow_type as ArrowType;
  if (typeof data.color === "string") partialData.color = data.color;
  if (typeof data.turns === "number") partialData.turns = data.turns;
  if (typeof data.is_mirrored === "boolean")
    partialData.is_mirrored = data.is_mirrored;
  if (typeof data.location === "string") partialData.location = data.location;
  if (typeof data.position_x === "number")
    partialData.position_x = data.position_x;
  if (typeof data.position_y === "number")
    partialData.position_y = data.position_y;
  if (typeof data.rotation_angle === "number")
    partialData.rotation_angle = data.rotation_angle;
  if (typeof data.is_visible === "boolean")
    partialData.is_visible = data.is_visible;
  if (typeof data.is_selected === "boolean")
    partialData.is_selected = data.is_selected;

  return createArrowData(partialData as Partial<ArrowData>);
}
