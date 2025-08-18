/**
 * Arrow Position Calculator
 *
 * Handles the main arrow positioning calculation logic.
 * Coordinates with other services to compute final arrow positions.
 */

import type { ArrowData, MotionData, PictographData } from "$lib/domain";
import type {
  IArrowAdjustmentCalculator,
  IArrowCoordinateSystemService,
  IArrowLocationCalculator,
  IArrowPositioningOrchestrator,
  IArrowRotationCalculator,
} from "../../core-services";
import { ArrowAdjustmentProcessor } from "./ArrowAdjustmentProcessor";
import { ArrowCoordinateTransformer } from "./ArrowCoordinateTransformer";
import { ArrowDataProcessor } from "./ArrowDataProcessor";

export class ArrowPositionCalculator implements IArrowPositioningOrchestrator {
  private locationCalculator: IArrowLocationCalculator;
  private rotationCalculator: IArrowRotationCalculator;
  private adjustmentCalculator: IArrowAdjustmentCalculator;
  private coordinateSystem: IArrowCoordinateSystemService;

  private adjustmentProcessor: ArrowAdjustmentProcessor;
  private coordinateTransformer: ArrowCoordinateTransformer;
  private dataProcessor: ArrowDataProcessor;

  constructor(
    locationCalculator: IArrowLocationCalculator,
    rotationCalculator: IArrowRotationCalculator,
    adjustmentCalculator: IArrowAdjustmentCalculator,
    coordinateSystem: IArrowCoordinateSystemService
  ) {
    this.locationCalculator = locationCalculator;
    this.rotationCalculator = rotationCalculator;
    this.adjustmentCalculator = adjustmentCalculator;
    this.coordinateSystem = coordinateSystem;

    this.adjustmentProcessor = new ArrowAdjustmentProcessor();
    this.coordinateTransformer = new ArrowCoordinateTransformer();
    this.dataProcessor = new ArrowDataProcessor(coordinateSystem);
  }

  async calculateArrowPosition(
    arrowData: ArrowData,
    pictographData: PictographData,
    motionData?: MotionData
  ): Promise<[number, number, number]> {
    /**
     * Calculate arrow position asynchronously with full service coordination.
     */
    try {
      // STEP 1: Extract or use provided motion data
      const motion =
        motionData ||
        this.dataProcessor.getMotionFromPictograph(arrowData, pictographData);
      if (!motion) {
        console.warn("No motion data available for arrow positioning");
        const center = this.coordinateSystem.getSceneCenter();
        return [center.x, center.y, 0];
      }

      // STEP 2: Calculate location and initial position
      const location = this.locationCalculator.calculateLocation(motion);
      const initialPosition = this.coordinateSystem.getInitialPosition(
        motion,
        location
      );
      const validPosition =
        this.dataProcessor.ensureValidPosition(initialPosition);

      // STEP 3: Calculate rotation
      const rotation = this.rotationCalculator.calculateRotation(
        motion,
        location
      );

      // STEP 4: Calculate adjustment using sophisticated service
      const adjustment = await this.adjustmentCalculator.calculateAdjustment(
        pictographData,
        motion,
        arrowData.color,
        location
      );
      const [adjustmentX, adjustmentY] =
        this.dataProcessor.extractAdjustmentValues(adjustment);

      // STEP 5: Apply rotation transformation to adjustment coordinates
      const [transformedAdjustmentX, transformedAdjustmentY] =
        this.coordinateTransformer.transformAdjustmentByRotation(
          adjustmentX,
          adjustmentY,
          rotation
        );

      // STEP 6: Combine all positioning calculations
      const finalX = validPosition.x + transformedAdjustmentX;
      const finalY = validPosition.y + transformedAdjustmentY;

      return [finalX, finalY, rotation];
    } catch (error) {
      console.error("Arrow positioning calculation failed:", error);
      const center = this.coordinateSystem.getSceneCenter();
      return [center.x, center.y, 0];
    }
  }

  async updateArrowPosition(
    pictographData: PictographData,
    color: string,
    motionData?: MotionData
  ): Promise<PictographData> {
    /**
     * Update arrow position in pictograph data.
     */
    try {
      const arrowData = pictographData.arrows?.[color];
      if (!arrowData) {
        console.warn(`No arrow data found for color: ${color}`);
        return pictographData;
      }

      const [x, y, rotation] = await this.calculateArrowPosition(
        arrowData,
        pictographData,
        motionData
      );

      // CRITICAL: Also calculate mirroring for this arrow
      const shouldMirror = this.shouldMirrorArrow(arrowData, pictographData);

      const updates: Partial<ArrowData> = {
        position_x: x,
        position_y: y,
        rotation_angle: rotation,
        is_mirrored: shouldMirror,
      };
      return this.dataProcessor.updateArrowInPictograph(
        pictographData,
        color,
        updates
      );
    } catch (error) {
      console.error("Arrow position update failed:", error);
      return pictographData;
    }
  }

  async calculateAllArrowPositions(
    pictographData: PictographData
  ): Promise<PictographData> {
    /**
     * Calculate positions for all arrows in the pictograph.
     */
    try {
      if (!pictographData.arrows) {
        return pictographData;
      }

      let updatedPictograph = { ...pictographData };

      for (const color of Object.keys(pictographData.arrows)) {
        const arrowData = pictographData.arrows[color];
        if (arrowData) {
          const [x, y, rotation] = await this.calculateArrowPosition(
            arrowData,
            updatedPictograph
          );

          // CRITICAL: Also calculate mirroring for this arrow
          const shouldMirror = this.shouldMirrorArrow(
            arrowData,
            updatedPictograph
          );

          const updates: Partial<ArrowData> = {
            position_x: x,
            position_y: y,
            rotation_angle: rotation,
            is_mirrored: shouldMirror,
          };

          updatedPictograph = this.dataProcessor.updateArrowInPictograph(
            updatedPictograph,
            color,
            updates
          );
        }
      }

      return updatedPictograph;
    } catch (error) {
      console.error("Failed to calculate all arrow positions:", error);
      return pictographData;
    }
  }

  shouldMirrorArrow(
    arrowData: ArrowData,
    pictographData?: PictographData
  ): boolean {
    /**
     * Determine if arrow should be mirrored based on motion type and prop rotation direction.
     *
     * Mirror conditions (matching desktop logic):
     * - Anti motion + clockwise → Mirror = True
     * - Anti motion + counterclockwise → Mirror = False
     * - Pro motion + clockwise → Mirror = False
     * - Pro motion + counterclockwise → Mirror = True
     * - Other motions follow "pro" rules
     */

    // Get motion data for this arrow's color
    if (!pictographData?.motions) {
      console.warn(
        "🚫 shouldMirrorArrow: No motion data available, defaulting to no mirror"
      );
      return false;
    }

    const motion = pictographData.motions[arrowData.color];
    if (!motion) {
      console.warn(
        `🚫 shouldMirrorArrow: No motion found for color ${arrowData.color}, defaulting to no mirror`
      );
      return false;
    }

    const motionType = motion.motion_type?.toLowerCase();
    const propRotDir = motion.prop_rot_dir?.toLowerCase();

    if (!motionType || !propRotDir) {
      console.warn(
        `🚫 shouldMirrorArrow: Missing motion_type (${motionType}) or prop_rot_dir (${propRotDir}), defaulting to no mirror`
      );
      return false;
    }

    // Mirror conditions matching desktop implementation
    const mirrorConditions = {
      anti: { cw: true, ccw: false },
      other: { cw: false, ccw: true },
    };

    // Use "anti" conditions for anti motion, "other" for everything else (pro, static, dash, float)
    const conditionKey = motionType === "anti" ? "anti" : "other";
    const shouldMirror = mirrorConditions[conditionKey][propRotDir] ?? false;

    console.log(
      `🪞 shouldMirrorArrow: ${arrowData.color} arrow - motion: ${motionType}, prop_rot_dir: ${propRotDir} → mirror: ${shouldMirror}`
    );

    return shouldMirror;
  }

  applyMirrorTransform(
    arrowItem: HTMLElement | SVGElement,
    shouldMirror: boolean
  ): void {
    /**
     * Apply mirror transformation to arrow graphics item.
     */
    if (shouldMirror) {
      arrowItem.style.transform = `${arrowItem.style.transform || ""} scaleX(-1)`;
    } else {
      // Remove mirror transformation
      const transform = arrowItem.style.transform || "";
      arrowItem.style.transform = transform
        .replace(/scaleX\(-1\)\s*/g, "")
        .trim();
    }
  }
}
