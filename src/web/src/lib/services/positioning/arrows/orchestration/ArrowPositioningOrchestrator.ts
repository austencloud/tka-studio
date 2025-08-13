/**
 * Arrow Positioning Orchestrator
 *
 * Coordinates sophisticated microservices to provide complete arrow positioning.
 * Now uses all the comprehensive positioning services for functional parity.
 *
 * Direct TypeScript port with enhancements from the Python reference implementation.
 */

import type { ArrowData, MotionData, PictographData } from "$lib/domain";
import { Location, MotionType, RotationDirection } from "$lib/domain";
import type {
  IArrowAdjustmentCalculator,
  IArrowCoordinateSystemService,
  IArrowLocationCalculator,
  IArrowPositioningOrchestrator,
  IArrowRotationCalculator,
} from "../../core-services";
import type { Point } from "../../types";

export class ArrowPositioningOrchestrator
  implements IArrowPositioningOrchestrator
{
  /**
   * Orchestrator that coordinates all positioning microservices.
   *
   * Uses:
   * - ArrowLocationCalculator: Sophisticated location calculation with special cases
   * - ArrowRotationCalculator: Comprehensive rotation calculation with all motion types
   * - ArrowAdjustmentCalculator: Complex adjustment calculation with special/default placement
   * - ArrowCoordinateSystemService: Precise TKA coordinate system management
   */

  private locationCalculator: IArrowLocationCalculator;
  private rotationCalculator: IArrowRotationCalculator;
  private adjustmentCalculator: IArrowAdjustmentCalculator;
  private coordinateSystem: IArrowCoordinateSystemService;

  private mirrorConditions = {
    anti: { cw: true, ccw: false },
    other: { cw: false, ccw: true },
  };

  constructor(
    locationCalculator: IArrowLocationCalculator,
    rotationCalculator: IArrowRotationCalculator,
    adjustmentCalculator: IArrowAdjustmentCalculator,
    coordinateSystem: IArrowCoordinateSystemService,
  ) {
    this.locationCalculator = locationCalculator;
    this.rotationCalculator = rotationCalculator;
    this.adjustmentCalculator = adjustmentCalculator;
    this.coordinateSystem = coordinateSystem;
  }

  // Main async method for full positioning calculation
  async calculateArrowPositionAsync(
    arrowData: ArrowData,
    pictographData: PictographData,
    motionData?: MotionData,
  ): Promise<[number, number, number]> {
    /**
     * Calculate arrow position using sophisticated microservices pipeline.
     *
     * This method coordinates all positioning services to provide pixel-perfect
     * arrow positioning that matches the reference implementation.
     */
    try {
      // Extract motion data
      const motion =
        motionData || this.getMotionFromPictograph(arrowData, pictographData);

      if (!motion) {
        console.warn(
          `No motion data for ${arrowData.color}, returning center position`,
        );
        const center = this.coordinateSystem.getSceneCenter();
        return [center.x, center.y, 0.0];
      }

      const letter = pictographData.letter || "";

      // STEP 1: Calculate arrow location using sophisticated location calculator
      const location = this.locationCalculator.calculateLocation(
        motion,
        pictographData,
      );
      console.debug(
        `Calculated location: ${location} for ${arrowData.color} ${motion.motion_type}`,
      );

      // STEP 2: Get initial position from precise coordinate system
      let initialPosition = this.coordinateSystem.getInitialPosition(
        motion,
        location,
      );
      initialPosition = this.ensureValidPosition(initialPosition);
      console.debug(
        `Initial position: (${initialPosition.x}, ${initialPosition.y})`,
      );

      // STEP 3: Calculate rotation using comprehensive rotation calculator
      const rotation = this.rotationCalculator.calculateRotation(
        motion,
        location,
      );
      console.debug(
        `Calculated rotation: ${rotation}° for ${motion.motion_type} ${motion.prop_rot_dir}`,
      );

      // STEP 4: Calculate adjustment using sophisticated adjustment calculator
      const adjustment = await this.adjustmentCalculator.calculateAdjustment(
        pictographData,
        motion,
        letter,
        location,
        arrowData.color,
      );
      console.debug(
        `Calculated adjustment: (${adjustment.x}, ${adjustment.y})`,
      );

      const [adjustmentX, adjustmentY] =
        this.extractAdjustmentValues(adjustment);

      // STEP 5: Combine all positioning calculations
      const finalX = initialPosition.x + adjustmentX;
      const finalY = initialPosition.y + adjustmentY;

      return [finalX, finalY, rotation];
    } catch (error) {
      console.error("Arrow positioning failed:", error);
      // Fallback to center position
      const center = this.coordinateSystem.getSceneCenter();
      return [center.x, center.y, 0.0];
    }
  }

  // Synchronous version implementing IArrowPositioningOrchestrator interface
  calculateArrowPosition(
    arrowData: ArrowData,
    pictographData: PictographData,
    motionData?: MotionData,
  ): [number, number, number] {
    /**
     * Synchronous wrapper for calculateArrowPosition.
     * Note: This may not include full adjustment calculations due to async requirements.
     */
    try {
      const motion =
        motionData || this.getMotionFromPictograph(arrowData, pictographData);

      if (!motion) {
        console.warn(
          `No motion data for ${arrowData.color}, returning center position`,
        );
        const center = this.coordinateSystem.getSceneCenter();
        return [center.x, center.y, 0.0];
      }

      const letter = pictographData.letter || "";

      // Calculate location and rotation synchronously
      const location = this.locationCalculator.calculateLocation(
        motion,
        pictographData,
      );
      let initialPosition = this.coordinateSystem.getInitialPosition(
        motion,
        location,
      );
      initialPosition = this.ensureValidPosition(initialPosition);
      const rotation = this.rotationCalculator.calculateRotation(
        motion,
        location,
      );

      // Use proper adjustment calculator for synchronous operation
      const adjustment = this.adjustmentCalculator.calculateAdjustmentSync(
        pictographData,
        motion,
        letter,
        location,
        arrowData.color,
      );
      const [adjustmentX, adjustmentY] =
        this.extractAdjustmentValues(adjustment);

      const finalX = initialPosition.x + adjustmentX;
      const finalY = initialPosition.y + adjustmentY;

      return [finalX, finalY, rotation];
    } catch (error) {
      console.error("Synchronous arrow positioning failed:", error);
      const center = this.coordinateSystem.getSceneCenter();
      return [center.x, center.y, 0.0];
    }
  }

  calculateAllArrowPositions(pictographData: PictographData): PictographData {
    /**
     * Calculate positions and mirror states for all arrows in the pictograph.
     * Uses the sophisticated positioning pipeline for each arrow.
     */
    let updatedPictograph = pictographData;

    try {
      if (!pictographData.arrows) {
        return updatedPictograph;
      }

      // Process each arrow with the enhanced positioning pipeline
      for (const [color, arrowData] of Object.entries(pictographData.arrows)) {
        const motionData = pictographData.motions?.[color];

        if (arrowData.is_visible && motionData) {
          // Calculate position and rotation using synchronous services
          const [x, y, rotation] = this.calculateArrowPositionSync(
            arrowData,
            pictographData,
            motionData,
          );

          // Calculate mirror state
          const shouldMirror = this.shouldMirrorArrow(
            arrowData,
            pictographData,
          );

          // Update arrow with all calculated values
          updatedPictograph = this.updateArrowInPictograph(
            updatedPictograph,
            color,
            {
              position_x: x,
              position_y: y,
              rotation_angle: rotation,
              is_mirrored: shouldMirror,
            },
          );

          console.log(
            `Updated ${color} arrow: position=(${x}, ${y}), rotation=${rotation}°, mirrored=${shouldMirror}`,
          );
        }
      }
    } catch (error) {
      console.error("Failed to calculate all arrow positions:", error);
    }

    return updatedPictograph;
  }

  shouldMirrorArrow(
    arrowData: ArrowData,
    pictographData?: PictographData,
  ): boolean {
    /**
     * Determine if arrow should be mirrored using enhanced motion analysis.
     */
    try {
      let motion: MotionData | undefined;
      if (pictographData?.motions) {
        motion = pictographData.motions[arrowData.color];
      }

      if (!motion) {
        return false;
      }

      const motionType = (motion.motion_type || "").toLowerCase();
      const propRotDir = (motion.prop_rot_dir || "").toLowerCase();

      // Enhanced mirroring logic based on motion type and rotation direction
      if (motionType === "anti") {
        return this.mirrorConditions.anti[propRotDir as "cw" | "ccw"] || false;
      }
      return this.mirrorConditions.other[propRotDir as "cw" | "ccw"] || false;
    } catch (error) {
      console.warn("Mirror calculation failed, using default:", error);
      return false;
    }
  }

  applyMirrorTransform(
    arrowItem: HTMLElement | SVGElement,
    shouldMirror: boolean,
  ): void {
    /**
     * Apply mirror transformation with enhanced positioning awareness.
     */
    try {
      if (shouldMirror) {
        // Apply mirror transformation while preserving positioning
        const rect = arrowItem.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;

        const scaleX = -1; // Mirror horizontally
        const transform = `translate(${centerX}px, ${centerY}px) scale(${scaleX}, 1) translate(${-centerX}px, ${-centerY}px)`;

        arrowItem.style.transform = transform;
      } else {
        // Remove mirror transformation
        arrowItem.style.transform = "";
      }
    } catch (error) {
      console.warn("Failed to apply mirror transform:", error);
    }
  }

  // Private helper methods

  private calculateArrowPositionSync(
    _arrowData: ArrowData,
    _pictographData: PictographData,
    motionData: MotionData,
  ): [number, number, number] {
    /**
     * Internal synchronous method for full positioning calculation with adjustments.
     */
    const motion = motionData;
    const letter = _pictographData.letter || "";

    // STEP 1: Calculate arrow location
    const location = this.locationCalculator.calculateLocation(
      motion,
      _pictographData,
    );

    // STEP 2: Get initial position
    let initialPosition = this.coordinateSystem.getInitialPosition(
      motion,
      location,
    );
    initialPosition = this.ensureValidPosition(initialPosition);

    // STEP 3: Calculate rotation
    const rotation = this.rotationCalculator.calculateRotation(
      motion,
      location,
    );

    // STEP 4: Calculate adjustment using simplified method for sync operation
    const adjustment = this.getBasicAdjustment(motion, letter);

    const [adjustmentX, adjustmentY] = this.extractAdjustmentValues(adjustment);

    // STEP 5: Combine all positioning calculations
    const finalX = initialPosition.x + adjustmentX;
    const finalY = initialPosition.y + adjustmentY;

    return [finalX, finalY, rotation];
  }

  private getMotionFromPictograph(
    arrowData: ArrowData,
    pictographData: PictographData,
  ): MotionData | undefined {
    /**Extract motion data from pictograph data.*/
    if (!pictographData?.motions) {
      return undefined;
    }
    return pictographData.motions[arrowData.color];
  }

  private ensureValidPosition(initialPosition: Point): Point {
    /**Ensure position object has valid x and y attributes.*/
    if (
      initialPosition &&
      typeof initialPosition.x === "number" &&
      typeof initialPosition.y === "number"
    ) {
      return initialPosition;
    }

    console.warn("Invalid initial position, using scene center");
    return this.coordinateSystem.getSceneCenter();
  }

  private extractAdjustmentValues(
    adjustment: Point | number,
  ): [number, number] {
    /**Extract x and y values from adjustment object.*/
    if (typeof adjustment === "number") {
      return [adjustment, adjustment];
    }

    if (
      adjustment &&
      typeof adjustment.x === "number" &&
      typeof adjustment.y === "number"
    ) {
      return [adjustment.x, adjustment.y];
    }

    return [0.0, 0.0];
  }

  private getBasicAdjustment(motion: MotionData, _letter: string): Point {
    /**Get basic adjustment for synchronous operations with directional tuple processing.*/
    try {
      // Calculate the arrow location for directional processing
      const location = this.locationCalculator.calculateLocation(motion, {
        letter: _letter,
      } as any);

      // Get base adjustment values based on motion type and turns
      const baseAdjustment = this.getBaseAdjustmentValues(motion);

      // Apply directional tuple processing for location-specific adjustments
      const finalAdjustment = this.processDirectionalTuples(
        baseAdjustment,
        motion,
        location,
      );

      console.debug(
        `Basic adjustment for ${motion.motion_type} ${motion.turns} turns at ${location}: (${finalAdjustment.x}, ${finalAdjustment.y})`,
      );
      return finalAdjustment;
    } catch (error) {
      console.warn("Basic adjustment calculation failed:", error);
      return { x: 0, y: 0 };
    }
  }

  private getBaseAdjustmentValues(motion: MotionData): Point {
    /**Get base adjustment values before directional processing.*/
    const motionType = motion.motion_type;
    const turns = typeof motion.turns === "number" ? motion.turns : 0;
    const turnsStr =
      turns === Math.floor(turns) ? turns.toString() : turns.toString();

    // Base default adjustments (before directional rotation)
    const defaultAdjustments: Record<
      string,
      Record<string, [number, number]>
    > = {
      pro: {
        "0": [-10, -40],
        "0.5": [30, 105],
        "1": [30, 25],
        "1.5": [-35, 145],
        "2": [-10, -35],
        "2.5": [20, 100],
        "3": [30, 25],
      },
      anti: {
        "0": [0, -40],
        "0.5": [-15, 110],
        "1": [0, -40],
        "1.5": [20, 155],
        "2": [0, -40],
        "2.5": [0, 100],
        "3": [0, -50],
      },
      static: {
        "0": [0, 0],
      },
      dash: {
        "0": [0, 0],
      },
      float: {
        "0": [0, 0],
      },
    };

    const motionAdjustments = defaultAdjustments[motionType];
    if (motionAdjustments && motionAdjustments[turnsStr]) {
      const [x, y] = motionAdjustments[turnsStr];
      return { x, y };
    }

    return { x: 0, y: 0 };
  }

  private processDirectionalTuples(
    baseAdjustment: Point,
    motion: MotionData,
    location: Location,
  ): Point {
    /**Process directional tuples to get location-specific adjustments.*/
    try {
      // Generate directional tuples from base adjustment using rotation matrices
      const directionalTuples = this.generateDirectionalTuples(
        motion,
        baseAdjustment.x,
        baseAdjustment.y,
      );

      // Calculate quadrant index for tuple selection
      const quadrantIndex = this.calculateQuadrantIndex(location);

      // Select the appropriate tuple based on quadrant
      const selectedTuple = directionalTuples[quadrantIndex] || [0, 0];

      console.debug(
        `Directional tuples: ${JSON.stringify(directionalTuples)}, quadrant: ${quadrantIndex}, selected: [${selectedTuple[0]}, ${selectedTuple[1]}]`,
      );

      return { x: selectedTuple[0], y: selectedTuple[1] };
    } catch (error) {
      console.warn(
        "Directional tuple processing failed, using base adjustment:",
        error,
      );
      return baseAdjustment;
    }
  }

  private generateDirectionalTuples(
    motion: MotionData,
    baseX: number,
    baseY: number,
  ): Array<[number, number]> {
    /**Generate directional tuples using rotation matrices.*/
    const motionType = motion.motion_type;
    const rotationDir = motion.prop_rot_dir;

    // Convert rotation direction to string for mapping
    const rotationStr =
      rotationDir === RotationDirection.CLOCKWISE
        ? "clockwise"
        : rotationDir === RotationDirection.COUNTER_CLOCKWISE
          ? "counter_clockwise"
          : "clockwise"; // Default

    // Diamond grid mappings for PRO/ANTI motions (based on reference code)
    const shiftMappingDiamond = {
      [MotionType.PRO]: {
        clockwise: (x: number, y: number) => [
          [x, y], // NE (0)
          [-y, x], // SE (1)
          [-x, -y], // SW (2)
          [y, -x], // NW (3)
        ],
        counter_clockwise: (x: number, y: number) => [
          [-y, -x], // NE (0)
          [x, -y], // SE (1)
          [y, x], // SW (2)
          [-x, y], // NW (3)
        ],
      },
      [MotionType.ANTI]: {
        clockwise: (x: number, y: number) => [
          [-y, -x], // NE (0)
          [x, -y], // SE (1)
          [y, x], // SW (2)
          [-x, y], // NW (3)
        ],
        counter_clockwise: (x: number, y: number) => [
          [x, y], // NE (0)
          [-y, x], // SE (1)
          [-x, -y], // SW (2)
          [y, -x], // NW (3)
        ],
      },
    };

    // For static/dash/float, use simpler mappings
    if (
      motionType === MotionType.STATIC ||
      motionType === MotionType.DASH ||
      motionType === MotionType.FLOAT
    ) {
      return [
        [baseX, baseY],
        [-baseX, -baseY],
        [-baseY, baseX],
        [baseY, -baseX],
      ];
    }

    // Use shift mappings for pro/anti
    const mapping = shiftMappingDiamond[motionType];
    if (mapping && mapping[rotationStr as "clockwise" | "counter_clockwise"]) {
      const transformFunc =
        mapping[rotationStr as "clockwise" | "counter_clockwise"];
      return transformFunc(baseX, baseY) as Array<[number, number]>;
    }

    // Fallback: return same adjustment for all quadrants
    return [
      [baseX, baseY],
      [baseX, baseY],
      [baseX, baseY],
      [baseX, baseY],
    ];
  }

  private calculateQuadrantIndex(location: Location): number {
    /**Calculate quadrant index for the given location.*/
    const quadrantMap: Record<Location, number> = {
      [Location.NORTHEAST]: 0,
      [Location.SOUTHEAST]: 1,
      [Location.SOUTHWEST]: 2,
      [Location.NORTHWEST]: 3,
      // Cardinal directions map to nearest quadrant
      [Location.NORTH]: 0, // Maps to NE quadrant
      [Location.EAST]: 1, // Maps to SE quadrant
      [Location.SOUTH]: 2, // Maps to SW quadrant
      [Location.WEST]: 3, // Maps to NW quadrant
    };

    return quadrantMap[location] || 0;
  }

  private updateArrowInPictograph(
    pictographData: PictographData,
    color: string,
    updates: Partial<ArrowData>,
  ): PictographData {
    /**Update arrow properties in pictograph data.*/
    // Create a deep copy and update the specific arrow
    const updatedPictograph = { ...pictographData };

    if (updatedPictograph.arrows && updatedPictograph.arrows[color]) {
      updatedPictograph.arrows = {
        ...updatedPictograph.arrows,
        [color]: {
          ...updatedPictograph.arrows[color],
          ...updates,
        },
      };
    }

    return updatedPictograph;
  }
}
