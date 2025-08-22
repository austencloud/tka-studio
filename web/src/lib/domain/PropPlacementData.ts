/**
 * Prop Placement Data Model
 *
 * Immutable data for prop positioning and placement calculations.
 */

export interface PropPlacementData {
  readonly positionX: number;
  readonly positionY: number;
  readonly rotationAngle: number;
  readonly coordinates?: { x: number; y: number } | null;
  readonly svgCenter?: { x: number; y: number } | null;
}

/**
 * Create PropPlacementData with default values
 */
export function createPropPlacementData(
  data: Partial<PropPlacementData> = {}
): PropPlacementData {
  return {
    positionX: data.positionX ?? 0.0,
    positionY: data.positionY ?? 0.0,
    rotationAngle: data.rotationAngle ?? 0.0,
    coordinates: data.coordinates ?? null,
    svgCenter: data.svgCenter ?? null,
  };
}

/**
 * Create PropPlacementData from position and rotation
 */
export function createPropPlacementFromPosition(
  x: number,
  y: number,
  rotation: number = 0
): PropPlacementData {
  return createPropPlacementData({
    positionX: x,
    positionY: y,
    rotationAngle: rotation,
    coordinates: { x, y },
  });
}
