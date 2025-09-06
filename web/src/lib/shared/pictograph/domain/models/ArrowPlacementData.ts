/**
 * Arrow Placement Domain Model
 *
 * Immutable placement data for an arrow in a pictograph.
 *
 */

export interface ArrowPlacementData {
  readonly positionX: number;
  readonly positionY: number;
  readonly rotationAngle: number;
  readonly coordinates: { x: number; y: number } | null;
  readonly svgCenter: { x: number; y: number } | null;
  readonly svgMirrored: boolean;
}

export function createArrowPlacementData(
  data: Partial<ArrowPlacementData> = {}
): ArrowPlacementData {
  return {
    positionX: data.positionX ?? 0.0,
    positionY: data.positionY ?? 0.0,
    rotationAngle: data.rotationAngle ?? 0.0,
    coordinates: data.coordinates ?? null,
    svgCenter: data.svgCenter ?? null,
    svgMirrored: data.svgMirrored ?? false,
  };
}
