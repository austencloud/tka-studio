// src/lib/components/objects/Arrow/ArrowPlacementManager/utils/adjustmentCalculator.ts
import type { ArrowData } from '$lib/components/objects/Arrow/ArrowData';
import type { ArrowPlacementConfig, Coordinates } from '../types';
import type { Motion } from '$lib/components/objects/Motion/Motion';
import { getDefaultAdjustment } from './defaultPlacementUtils';
import { getDirectionTuples, getQuadrantIndex } from './directionUtils';
import { getSpecialAdjustment } from './specialPlacementUtils';
import type { ShiftHandRotDir } from '$lib/types/Types';

/**
 * Calculates position adjustments for an arrow based on its properties
 * and the pictograph configuration.
 * This function precisely matches the Python ArrowAdjustmentCalculator's behavior.
 */
export function calculateAdjustment(arrow: ArrowData, config: ArrowPlacementConfig): Coordinates {
  const { pictographData } = config;

  // No adjustments needed if no letter is set (matches Python's check)
  if (!pictographData.letter) {
    return { x: 0, y: 0 };
  }

  // 1. Try to get special adjustment first (matches Python's flow)
  const specialAdjustment = getSpecialAdjustment(arrow, config);

  // 2. Get base adjustment values - either from special placement or default
  let x: number, y: number;
  if (specialAdjustment) {
    [x, y] = specialAdjustment;

  } else {
    // Fall back to default adjustment (matches Python behavior)
    [x, y] = getDefaultAdjustment(arrow, config);
  }

  // 3. Get the motion object (matches Python behavior)
  const motion = getMotionForArrow(arrow, pictographData);
  if (!motion) {
    return { x, y }; // Return base adjustment if no motion found
  }

  // 4. Generate directional tuples (matches Python's DirectionalTupleGenerator)
  const directionalAdjustments = getDirectionTuples(
    x,
    y,
    motion.motionType,
    motion.propRotDir,
    motion.gridMode || 'diamond',
    {
      startOri: motion.startOri,
      handRotDir:
        (motion.handRotDirCalculator?.getHandRotDir(
          motion.startLoc,
          motion.endLoc
        ) as ShiftHandRotDir) || undefined
    }
  );

  if (!directionalAdjustments || directionalAdjustments.length === 0) {
    return { x, y }; // Return base adjustment if no directional adjustments
  }

  // 5. Get the quadrant index (matches Python's QuadrantIndexHandler)
  const quadrantIndex = getQuadrantIndex(arrow, pictographData.gridMode || 'diamond');

  if (quadrantIndex < 0 || quadrantIndex >= directionalAdjustments.length) {
    return { x: 0, y: 0 }; // Return zero adjustment for invalid indices
  }

  // 6. Apply the selected adjustment (matches Python's _get_final_adjustment)
  const [adjX, adjY] = directionalAdjustments[quadrantIndex];



  // Return the final adjustment - EXACTLY like Python does
  return { x: adjX, y: adjY };
}

/**
 * Gets the motion object for an arrow based on its color.
 * Matches Python's behavior.
 */
function getMotionForArrow(arrow: ArrowData, pictographData: any): Motion | null {
  if (arrow.color === 'red' && pictographData.redMotion) {
    return pictographData.redMotion;
  } else if (arrow.color === 'blue' && pictographData.blueMotion) {
    return pictographData.blueMotion;
  }
  return null;
}
