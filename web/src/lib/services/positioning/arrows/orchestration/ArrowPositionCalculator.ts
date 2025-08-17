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

  async calculateArrowPositionAsync(
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

  calculateArrowPosition(
    arrowData: ArrowData,
    pictographData: PictographData,
    motionData?: MotionData
  ): [number, number, number] {
    /**
     * Calculate arrow position synchronously with basic adjustment processing.
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

      // STEP 2: Calculate location and initial position synchronously
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

      // STEP 4: Get basic adjustment with directional processing
      const adjustment = this.adjustmentProcessor.getBasicAdjustment(
        motion,
        arrowData.color,
        this.locationCalculator
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

      // STEP 6: Combine positioning calculations
      const finalX = validPosition.x + transformedAdjustmentX;
      const finalY = validPosition.y + transformedAdjustmentY;

      return [finalX, finalY, rotation];
    } catch (error) {
      console.error("Synchronous arrow positioning failed:", error);
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

      const [x, y, rotation] = await this.calculateArrowPositionAsync(
        arrowData,
        pictographData,
        motionData
      );

      const updates: Partial<ArrowData> = {
        position_x: x,
        position_y: y,
        rotation_angle: rotation,
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

  calculateAllArrowPositions(pictographData: PictographData): PictographData {
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
          const [x, y, rotation] = this.calculateArrowPosition(
            arrowData,
            updatedPictograph
          );

          const updates: Partial<ArrowData> = {
            position_x: x,
            position_y: y,
            rotation_angle: rotation,
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
     * Determine if arrow should be mirrored based on motion type.
     */
    // For now, use the is_mirrored property from arrow data
    // This can be enhanced with more sophisticated logic later
    return arrowData.is_mirrored;
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
