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
