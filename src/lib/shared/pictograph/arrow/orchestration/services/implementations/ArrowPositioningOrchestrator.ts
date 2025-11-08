/**
 * Arrow Positioning Orchestrator
 *
 * Main implementation of the arrow positioning pipeline.
 * Coordinates with other services to compute final arrow positions.
 */

import type {
  ArrowPlacementData,
  IArrowAdjustmentCalculator,
  IArrowLocationCalculator,
  IArrowPositioningOrchestrator,
  MotionData,
  PictographData,
} from "$shared";
import { TYPES } from "$shared/inversify/types";
import { inject, injectable } from "inversify";
import type { IArrowRotationCalculator } from "../../../positioning/calculation/services/contracts";
import type {
  IArrowCoordinateTransformer,
  IArrowDataProcessor,
  IArrowGridCoordinateService,
} from "../contracts";

@injectable()
export class ArrowPositioningOrchestrator
  implements IArrowPositioningOrchestrator
{
  private locationCalculator: IArrowLocationCalculator;
  private rotationCalculator: IArrowRotationCalculator;
  private adjustmentCalculator: IArrowAdjustmentCalculator;
  private coordinateSystem: IArrowGridCoordinateService;

  private coordinateTransformer: IArrowCoordinateTransformer;
  private dataProcessor: IArrowDataProcessor;

  constructor(
    @inject(TYPES.IArrowLocationCalculator)
    locationCalculator: IArrowLocationCalculator,
    @inject(TYPES.IArrowRotationCalculator)
    rotationCalculator: IArrowRotationCalculator,
    @inject(TYPES.IArrowAdjustmentCalculator)
    adjustmentCalculator: IArrowAdjustmentCalculator,
    @inject(TYPES.IArrowGridCoordinateService)
    coordinateSystem: IArrowGridCoordinateService,
    @inject(TYPES.IArrowCoordinateTransformer)
    coordinateTransformer: IArrowCoordinateTransformer,
    @inject(TYPES.IArrowDataProcessor)
    dataProcessor: IArrowDataProcessor
  ) {
    this.locationCalculator = locationCalculator;
    this.rotationCalculator = rotationCalculator;
    this.adjustmentCalculator = adjustmentCalculator;
    this.coordinateSystem = coordinateSystem;
    this.coordinateTransformer = coordinateTransformer;
    this.dataProcessor = dataProcessor;
  }

  async calculateArrowPoint(
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
          "🚫 ArrowPositioningOrchestrator: No motion data provided, using scene center"
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
      const rotation = await this.rotationCalculator.calculateRotation(
        motion,
        location,
        pictographData
      );

      // STEP 4: Calculate adjustment using sophisticated service
      const adjustment = await this.adjustmentCalculator.calculateAdjustment(
        pictographData,
        motion,
        pictographData.letter || "A", // ✅ FIXED: Pass letter as 3rd parameter
        location, // ✅ FIXED: Pass location as 4th parameter
        motion.color // ✅ FIXED: Pass color as 5th parameter
      );

      const [adjustmentX, adjustmentY] =
        this.dataProcessor.extractAdjustmentValues(adjustment);

      // STEP 5: Calculate final position (no rotation transformation needed)
      // The adjustment values are already calculated correctly for the final position
      const finalX = validPosition.x + adjustmentX;
      const finalY = validPosition.y + adjustmentY;

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

      const [x, y, rotation] = await this.calculateArrowPoint(
        pictographData,
        motionData
      );

      console.log(`[ArrowPos] ${color} arrow calculated:`, { x, y, rotation });

      // CRITICAL: Also calculate mirroring for this arrow
      const shouldMirror = this.shouldMirrorArrow(arrowData, pictographData);

      // Apply manual adjustments from keyboard controls (WASD)
      const manualAdjustX = arrowData.manualAdjustmentX || 0;
      const manualAdjustY = arrowData.manualAdjustmentY || 0;

      console.log(`[ArrowPos] ${color} manual adjustments from arrowData:`, {
        manualAdjustX,
        manualAdjustY,
      });
      console.log(`[ArrowPos] ${color} arrowData:`, arrowData);

      const updates: Partial<ArrowPlacementData> = {
        positionX: x + manualAdjustX, // Add manual adjustment to calculated position
        positionY: y + manualAdjustY, // Add manual adjustment to calculated position
        rotationAngle: rotation,
        svgMirrored: shouldMirror, // ✅ FIXED: Use correct property name
        manualAdjustmentX: manualAdjustX, // Preserve manual adjustments
        manualAdjustmentY: manualAdjustY, // Preserve manual adjustments
      };

      console.log(`[ArrowPos] ${color} final position:`, {
        x: x + manualAdjustX,
        y: y + manualAdjustY,
      });

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

  async calculateAllArrowPoints(
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

          const [x, y, rotation] = await this.calculateArrowPoint(
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

          // Apply manual adjustments from keyboard controls (WASD)
          const manualAdjustX = arrowData.manualAdjustmentX || 0;
          const manualAdjustY = arrowData.manualAdjustmentY || 0;

          console.log(`[ArrowPos ALL] ${color} manual adjustments:`, {
            manualAdjustX,
            manualAdjustY,
          });
          console.log(`[ArrowPos ALL] ${color} calculated pos:`, {
            x,
            y,
            rotation,
          });

          const updates: Partial<ArrowPlacementData> = {
            positionX: x + manualAdjustX, // Add manual adjustment to calculated position
            positionY: y + manualAdjustY, // Add manual adjustment to calculated position
            rotationAngle: rotation,
            svgMirrored: shouldMirror, // ✅ FIXED: Use correct property name
            manualAdjustmentX: manualAdjustX, // Preserve manual adjustments
            manualAdjustmentY: manualAdjustY, // Preserve manual adjustments
          };

          console.log(`[ArrowPos ALL] ${color} final updates:`, updates);

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
