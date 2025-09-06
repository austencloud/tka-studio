// src/lib/components/PlacementManagers/ArrowPlacementManager/utils/positionCalculator.ts
import type { ArrowData } from '$lib/components/objects/Arrow/ArrowData';
import type { ArrowPlacementConfig, Coordinates } from '../types';
import { ANTI, DASH, FLOAT, PRO, STATIC } from '$lib/types/Constants';

/**
 * Gets the initial position for an arrow based on its type and location
 */
export function getInitialPosition(
  arrow: ArrowData,
  config: ArrowPlacementConfig
): Coordinates {
  const { motionType } = arrow;
  const { pictographData, gridData } = config;

  // Early return for invalid motion types
  if (!motionType) {
    return { x: 0, y: 0 };
  }

  // Determine position based on motion type
  switch (motionType) {
    case PRO:
    case ANTI:
    case FLOAT:
      return getShiftCoordinates(arrow, pictographData, gridData);
    case STATIC:
    case DASH:
      return getStaticDashCoordinates(arrow, pictographData, gridData);
    default:
      return { x: 0, y: 0 };
  }
}

/**
 * Gets coordinates for shift-type motions (Pro, Anti, Float)
 */
function getShiftCoordinates(
  arrow: ArrowData,
  pictographData: any,
  gridData: any
): Coordinates {
  const pointName = `${arrow.loc}_${pictographData.gridMode || 'diamond'}_layer2_point`;
  const point = gridData.allLayer2PointsNormal[pointName];

  if (!point?.coordinates) {
    console.warn(`Shift coordinate for '${pointName}' not found.`);
    return { x: 0, y: 0 };
  }

  return point.coordinates;
}

/**
 * Gets coordinates for static or dash motions
 */
function getStaticDashCoordinates(
  arrow: ArrowData,
  pictographData: any,
  gridData: any
): Coordinates {
  const pointName = `${arrow.loc}_${pictographData.gridMode || 'diamond'}_hand_point`;
  const point = gridData.allHandPointsNormal[pointName];

  if (!point?.coordinates) {
    console.warn(`Static coordinate for '${pointName}' not found.`);
    return { x: 0, y: 0 };
  }

  return point.coordinates;
}
