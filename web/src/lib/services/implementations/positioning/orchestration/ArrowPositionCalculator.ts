/**
 * Arrow Position Calculator
 *
 * Handles the main arrow positioning calculation logic.
 * Coordinates with other services to compute final arrow positions.
 */

import type { ArrowPlacementData, MotionData, PictographData } from "$domain";
import type {
  IArrowAdjustmentCalculator,
  IArrowCoordinateSystemService,
  IArrowLocationCalculator,
  IArrowPositioningOrchestrator,
  IArrowRotationCalculator,
} from "$lib/services/contracts/positioning-interfaces";
import { inject, injectable } from "inversify";
import { TYPES } from "../../../inversify/types";
import { ArrowAdjustmentProcessor } from "./ArrowAdjustmentProcessor";
import { ArrowCoordinateTransformer } from "./ArrowCoordinateTransformer";
import { ArrowDataProcessor } from "./ArrowDataProcessor";

@injectable()
export class ArrowPositionCalculator implements IArrowPositioningOrchestrator {
  private locationCalculator: IArrowLocationCalculator;
  private rotationCalculator: IArrowRotationCalculator;
  private adjustmentCalculator: IArrowAdjustmentCalculator;
  private coordinateSystem: IArrowCoordinateSystemService;

  private adjustmentProcessor: ArrowAdjustmentProcessor;
  private coordinateTransformer: ArrowCoordinateTransformer;
  private dataProcessor: ArrowDataProcessor;

  constructor(
    @inject(TYPES.IArrowLocationCalculator)
    locationCalculator: IArrowLocationCalculator,
    @inject(TYPES.IArrowRotationCalculator)
    rotationCalculator: IArrowRotationCalculator,
    @inject(TYPES.IArrowAdjustmentCalculator)
    adjustmentCalculator: IArrowAdjustmentCalculator,
    @inject(TYPES.IArrowCoordinateSystemService)
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
    pictographData: PictographData,
    motionData: MotionData
  ): Promise<[number, number, number]> {
    /**
     * Calculate arrow position asynchronously with full service coordination.
     */
    try {
      // STEP 1: Extract or use provided motion data
      // ✅ FIXED: Pass color directly since ArrowPlacementData no longer has color
      const motion = motionData;
      if (!motion) {
        console.warn(
          "🚫 ArrowPositionCalculator: No motion data provided, using scene center"
        );
        const center = this.coordinateSystem.getSceneCenter();
        return [center.x, center.y, 0];
      }

      // STEP 2: Calculate location and initial position
      const location = this.locationCalculator.calculateLocation(
        motion,
        pictographData
      );

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
        location,
        motion.color // ✅ FIXED: Use color from MotionData as optional parameter
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
    _motionData?: MotionData
  ): Promise<PictographData> {
    /**
     * Update arrow position in pictograph data.
     */
    try {
      const motionData =
        pictographData.motions?.[color as keyof typeof pictographData.motions];
      const arrowData = motionData?.arrowPlacementData;
      if (!arrowData) {
        console.warn(`No arrow data found for color: ${color}`);
        return pictographData;
      }

      const [x, y, rotation] = await this.calculateArrowPosition(
        pictographData,
        motionData
      );

      // CRITICAL: Also calculate mirroring for this arrow
      const shouldMirror = this.shouldMirrorArrow(arrowData, pictographData);

      const updates: Partial<ArrowPlacementData> = {
        positionX: x,
        positionY: y,
        rotationAngle: rotation,
        svgMirrored: shouldMirror, // ✅ FIXED: Use correct property name
      };

      // 🚨 CRITICAL FIX: Pass the calculated arrow location to persist in pictograph data
      const motionUpdates = {
        arrowLocation: location, // Use the calculated location from above
      } as unknown as Partial<MotionData>;

      return this.dataProcessor.updateArrowInPictograph(
        pictographData,
        color,
        updates,
        motionUpdates
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
      if (!pictographData.motions) {
        return pictographData;
      }

      let updatedPictograph = { ...pictographData };

      for (const color of Object.keys(pictographData.motions)) {
        const motionData =
          pictographData.motions[color as keyof typeof pictographData.motions];
        const arrowData = motionData?.arrowPlacementData;
        if (arrowData && motionData) {
          // Calculate location first to store it properly
          const calculatedLocation = this.locationCalculator.calculateLocation(
            motionData,
            updatedPictograph
          );

          const [x, y, rotation] = await this.calculateArrowPosition(
            updatedPictograph,
            motionData
          );

          // CRITICAL: Also calculate mirroring for this arrow
          const currentMotionData =
            updatedPictograph.motions?.[
              color as keyof typeof updatedPictograph.motions
            ];
          const shouldMirror = this.shouldMirrorArrow(
            arrowData,
            updatedPictograph,
            currentMotionData
          );

          const updates: Partial<ArrowPlacementData> = {
            positionX: x,
            positionY: y,
            rotationAngle: rotation,
            svgMirrored: shouldMirror, // ✅ FIXED: Use correct property name
          };

          // 🚨 CRITICAL FIX: Pass the calculated arrow location to persist in pictograph data
          const motionUpdates = {
            arrowLocation: calculatedLocation, // Use the calculated location from above
          } as unknown as Partial<MotionData>;

          updatedPictograph = this.dataProcessor.updateArrowInPictograph(
            updatedPictograph,
            color,
            updates,
            motionUpdates
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
    _arrowData: ArrowPlacementData,
    pictographData?: PictographData,
    motionData?: MotionData
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
    if (!pictographData?.motions || !motionData) {
      return false;
    }

    const motionType = motionData.motionType?.toLowerCase();
    const propRotDir = motionData.rotationDirection?.toLowerCase();

    if (!motionType || !propRotDir) {
      return false;
    }

    // Mirror conditions matching desktop implementation
    const mirrorConditions = {
      anti: { cw: true, ccw: false },
      other: { cw: false, ccw: true },
    };

    // Use "anti" conditions for anti motion, "other" for everything else (pro, static, dash, float)
    const conditionKey = motionType === "anti" ? "anti" : "other";
    const shouldMirror =
      mirrorConditions[conditionKey][
        propRotDir as keyof typeof mirrorConditions.anti
      ] ?? false;

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
