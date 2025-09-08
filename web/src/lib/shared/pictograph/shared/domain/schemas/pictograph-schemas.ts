/**
 * Pictograph Zod Schemas
 *
 * Runtime validation schemas for pictograph-specific data boundaries:
 * - Motion data validation
 * - Pictograph data validation
 * - Arrow and prop placement validation
 *
 * ⚠️  USAGE POLICY: Only use for data boundaries with external sources!
 *     Don't use for internal service constructors or component props.
 */

import { z } from "zod";
// Import enums directly from their sources to avoid circular dependencies
import { Letter } from "../../../../foundation/domain/models/Letter";
import { GridLocation, GridPosition } from "../../../grid/domain/enums/grid-enums";
import { PropType } from "../../../prop/domain/enums/prop-enums";
import { MotionColor, MotionType, Orientation, RotationDirection } from "../enums/pictograph-enums";

// ============================================================================
// COORDINATE AND PLACEMENT SCHEMAS
// ============================================================================

const CoordinateSchema = z
  .object({
    x: z.number(),
    y: z.number(),
  })
  .nullable();

const ArrowPlacementDataSchema = z.object({
  positionX: z.number().default(0.0),
  positionY: z.number().default(0.0),
  rotationAngle: z.number().default(0.0),
  coordinates: CoordinateSchema.default(null),
  svgCenter: CoordinateSchema.default(null),
  svgMirrored: z.boolean().default(false),
});

const PropPlacementDataSchema = z.object({
  positionX: z.number().default(0.0),
  positionY: z.number().default(0.0),
  rotationAngle: z.number().default(0.0),
  coordinates: CoordinateSchema.default(null),
  svgCenter: CoordinateSchema.default(null),
});

// ============================================================================
// MOTION AND PICTOGRAPH SCHEMAS
// ============================================================================

const MotionDataSchema = z.object({
  motionType: z.nativeEnum(MotionType).default(MotionType.STATIC),
  rotationDirection: z
    .nativeEnum(RotationDirection)
    .default(RotationDirection.NO_ROTATION),
  startLocation: z.nativeEnum(GridLocation).default(GridLocation.NORTH),
  endLocation: z.nativeEnum(GridLocation).default(GridLocation.NORTH),
  turns: z.union([z.number(), z.literal("fl")]).default(0.0),
  startOrientation: z.nativeEnum(Orientation).default(Orientation.IN),
  endOrientation: z.nativeEnum(Orientation).default(Orientation.IN),
  isVisible: z.boolean().default(true),
  propType: z.nativeEnum(PropType).default(PropType.STAFF),
  arrowLocation: z.nativeEnum(GridLocation).default(GridLocation.NORTH),
  color: z.nativeEnum(MotionColor).default(MotionColor.BLUE),
  arrowPlacementData: ArrowPlacementDataSchema.default({}),
  propPlacementData: PropPlacementDataSchema.default({}),
  prefloatMotionType: z.nativeEnum(MotionType).nullable().default(null),
  prefloatRotationDirection: z
    .nativeEnum(RotationDirection)
    .nullable()
    .default(null),
});

const PictographDataSchema = z.object({
  id: z
    .string()
    .min(1)
    .default(() => crypto.randomUUID()),
  letter: z.nativeEnum(Letter).nullable().default(null),
  startPosition: z.nativeEnum(GridPosition).nullable().default(null),
  endPosition: z.nativeEnum(GridPosition).nullable().default(null),
  motions: z.record(z.nativeEnum(MotionColor), MotionDataSchema).default({}),
});

// ============================================================================
// EXPORTS
// ============================================================================

export {
  ArrowPlacementDataSchema,
  CoordinateSchema,
  MotionDataSchema,
  PictographDataSchema,
  PropPlacementDataSchema
};

