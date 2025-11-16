/**
 * Zod Schemas for TKA Domain Models
 *
 * Runtime validation schemas for critical data boundaries:
 * - LocalStorage persistence (prevents data corruption)
 * - PNG import validation (prevents malformed import crashes)
 * - External data validation (API safety)
 *
 * ⚠️  USAGE POLICY: Only use for data boundaries with external sources!
 *     Don't use for internal service constructors or component props.
 */

import { z } from "zod";
// Use barrel exports for consistency
import { GridMode, GridPositionGroup } from "../../pictograph/grid/domain";
import { PropType } from "../../pictograph/prop/domain";
import type { MotionDataSchema } from "../../pictograph/shared/domain/schemas";
import { PictographDataSchema } from "../../pictograph/shared/domain/schemas";

// ============================================================================
// COORDINATE AND PLACEMENT SCHEMAS
// ============================================================================

// Pictograph-specific schemas moved to pictograph/shared/domain/schemas/

// ============================================================================
// BEAT AND SEQUENCE SCHEMAS - The Main Targets
// ============================================================================

export const BeatDataSchema = PictographDataSchema.extend({
  // Beat context properties
  beatNumber: z
    .number()
    .int()
    .nonnegative("Beat number must be non-negative (0 or positive)"),
  duration: z.number().positive("Duration must be positive").default(1.0),
  blueReversal: z.boolean().default(false),
  redReversal: z.boolean().default(false),
  isBlank: z.boolean().default(false),
  isSelected: z.boolean().optional(),
});

export const SequenceDataSchema = z.object({
  id: z
    .string()
    .min(1, "Sequence ID cannot be empty")
    .refine((id) => {
      // Accept either UUID format or custom sequence ID format
      const uuidRegex =
        /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
      const customIdRegex = /^seq_\d+_[a-z0-9]+$/i; // seq_timestamp_randomstring
      const shortIdRegex = /^[a-zA-Zα-ωΑ-Ω-]+$/; // Short letter-based IDs like "bjea", "bσtw"

      return (
        uuidRegex.test(id) || customIdRegex.test(id) || shortIdRegex.test(id)
      );
    }, "Sequence ID must be a valid UUID, custom sequence ID (seq_*), or letter-based ID"),
  name: z
    .string()
    .min(1, "Sequence name cannot be empty")
    .max(100, "Sequence name too long"),
  word: z.string().default(""),
  beats: z.array(BeatDataSchema).default([]),

  // Optional positioning data
  startingPositionBeat: BeatDataSchema.optional(),
  startingPositionGroup: z.nativeEnum(GridPositionGroup).optional(),
  startPosition: BeatDataSchema.optional(),

  // Metadata and display
  thumbnails: z.array(z.string().url()).default([]),
  sequenceLength: z.number().int().positive().optional(),
  author: z.string().max(50).optional(),
  level: z.number().int().min(1).max(10).optional(),
  dateAdded: z.coerce.date().default(() => new Date()),
  gridMode: z.nativeEnum(GridMode).optional(),
  propType: z.nativeEnum(PropType).optional(),
  isFavorite: z.boolean().default(false),
  isCircular: z.boolean().default(false),
  difficultyLevel: z.string().max(20).optional(),
  tags: z.array(z.string().max(30)).max(10, "Too many tags").default([]),
  metadata: z.record(z.unknown()).default({}),
});

// ============================================================================
// PNG IMPORT SCHEMAS - Second Target
// ============================================================================

const PngMotionAttributesSchema = z.object({
  motion_type: z.string(), // PNG uses string values like "static", "pro", "anti"
  start_loc: z.string(), // PNG uses string values like "n", "s", "e", "w"
  end_loc: z.string(), // PNG uses string values like "n", "s", "e", "w"
  start_ori: z.string(), // PNG uses string values like "in", "out"
  end_ori: z.string(), // PNG uses string values like "in", "out"
  prop_rot_dir: z.string().optional(), // PNG uses "no_rot", "cw", "ccw"
  turns: z.union([z.number(), z.literal("fl")]).optional(),
});

export const PngStepSchema = z.object({
  beat: z
    .number()
    .int()
    .nonnegative("PNG beat number must be non-negative (0 or positive)"),
  letter: z.string().min(1, "PNG letter cannot be empty"),
  blue_attributes: PngMotionAttributesSchema.optional(), // snake_case to match PNG
  red_attributes: PngMotionAttributesSchema.optional(), // snake_case to match PNG
});

export const PngMetadataArraySchema = z.array(PngStepSchema);

// ============================================================================
// TYPE INFERENCE - Automatic TypeScript types from schemas
// ============================================================================

export type ValidatedSequenceData = z.infer<typeof SequenceDataSchema>;
export type ValidatedBeatData = z.infer<typeof BeatDataSchema>;
export type ValidatedPngStep = z.infer<typeof PngStepSchema>;
export type ValidatedMotionData = z.infer<typeof MotionDataSchema>;
export type ValidatedPictographData = z.infer<typeof PictographDataSchema>;

// ============================================================================
// VALIDATION UTILITIES
// ============================================================================

/**
 * Safe parsing that returns detailed error information
 */
export function safeParseWithContext<T>(
  schema: z.ZodSchema<T>,
  data: unknown,
  context: string = "data validation"
):
  | { success: true; data: T }
  | { success: false; error: string; details: z.ZodError } {
  const result = schema.safeParse(data);

  if (result.success) {
    return { success: true, data: result.data };
  } else {
    const firstError = result.error.errors[0];
    const path = firstError?.path.join(".") || "unknown";
    const message = `${context} failed: ${firstError?.message} at ${path}`;

    return {
      success: false,
      error: message,
      details: result.error,
    };
  }
}

/**
 * Throws with clear error messages - use for critical validation
 */
export function parseWithContext<T>(
  schema: z.ZodSchema<T>,
  data: unknown,
  context: string = "data validation"
): T {
  const result = safeParseWithContext(schema, data, context);
  if (result.success) {
    return result.data;
  } else {
    throw new Error(result.error);
  }
}
