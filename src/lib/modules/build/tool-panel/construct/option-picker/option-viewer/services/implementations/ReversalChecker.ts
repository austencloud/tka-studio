/**
 * Motion Analyzer Implementation
 *
 * Handles analysis of motion data for reversal counting based on rotation direction comparison.
 * Extracted from OptionPickerService for better separation of concerns.
 */

import type { PictographData } from "$shared";
import { injectable } from "inversify";
import type { IReversalChecker } from "../contracts/IReversalChecker";

@injectable()
export class ReversalChecker implements IReversalChecker {
  /**
   * Calculate the number of reversals found in a pictograph. We look at both the
   * intrinsic motion data (paths, motion types, turns) and, when available, the
   * surrounding sequence context to determine direction changes.
   */
  getReversalCount(option: PictographData, sequence: PictographData[] = []): number {
    if (!option?.motions) {
      return 0;
    }

    let maxReversals = 0;

    // Inspect each motion on the pictograph for intrinsic reversal cues
    Object.values(option.motions).forEach((motion) => {
      if (!motion) return;
      const reversals = this.analyzeMotionForReversals(motion);
      maxReversals = Math.max(maxReversals, reversals);
    });

    // Incorporate sequence-based comparison of rotationDirection metadata
    if (sequence.length > 0) {
      const sequenceReversals = this.analyzeSequenceContext(option, sequence);
      maxReversals = Math.max(maxReversals, sequenceReversals);
    }

    return Math.min(maxReversals, 2); // Keep within the available filter buckets
  }

  hasReversals(option: PictographData): boolean {
    return this.getReversalCount(option) > 0;
  }

  /**
   * Analyze a single motion for reversal patterns using the heuristics from the
   * previous monolithic service implementation.
   */
  private analyzeMotionForReversals(motion: any): number {
    let reversalCount = 0;

    if (motion?.motionType) {
      const motionTypeStr = motion.motionType.toString().toLowerCase();

      if (motionTypeStr.includes("pro") && motionTypeStr.includes("anti")) {
        reversalCount = Math.max(reversalCount, 1);
      } else if (motionTypeStr.includes("bi") || motionTypeStr.includes("switch")) {
        reversalCount = Math.max(reversalCount, 2);
      }
    }

    if (Array.isArray(motion?.path)) {
      reversalCount = Math.max(reversalCount, this.analyzePathForReversals(motion.path));
    }

    if (typeof motion?.turns === "number" && motion.turns > 1) {
      reversalCount = Math.max(reversalCount, Math.floor(motion.turns / 2));
    }

    return reversalCount;
  }

  /**
   * Inspects a motion path for direction changes using a simplified
   * clockwise/counter-clockwise heuristic.
   */
  private analyzePathForReversals(path: any[]): number {
    if (path.length < 3) return 0;

    let reversals = 0;
    let lastDirection: "cw" | "ccw" | null = null;

    for (let i = 0; i < path.length - 1; i++) {
      const current = path[i];
      const next = path[i + 1];
      const direction = this.determinePathDirection(current, next);

      if (lastDirection && direction && lastDirection !== direction) {
        reversals++;
      }

      if (direction) {
        lastDirection = direction;
      }
    }

    return reversals;
  }

  /**
   * Determine direction between two path points using a simple cross-product
   * style heuristic. Returns `cw`, `ccw`, or `null` if not enough movement.
   */
  private determinePathDirection(from: any, to: any): "cw" | "ccw" | null {
    if (!from || !to) return null;

    if (
      from.x !== undefined &&
      from.y !== undefined &&
      to.x !== undefined &&
      to.y !== undefined
    ) {
      const dx = to.x - from.x;
      const dy = to.y - from.y;
      const magnitude = Math.sqrt(dx * dx + dy * dy);

      if (magnitude < 0.01) {
        return null;
      }

      return dx > 0 ? "cw" : "ccw";
    }

    return null;
  }

  /**
   * Compare the current pictograph's rotation metadata against the prior
   * sequence to detect direction switches.
   */
  private analyzeSequenceContext(option: PictographData, sequence: PictographData[]): number {
    let reversalCount = 0;

    ["blue", "red"].forEach((color) => {
      const currentRotation = option.motions?.[color as "blue" | "red"]?.rotationDirection;

      if (!currentRotation || currentRotation === "noRotation") {
        return;
      }

      for (let i = sequence.length - 1; i >= 0; i--) {
        const previousRotation = sequence[i].motions?.[color as "blue" | "red"]?.rotationDirection;

        if (!previousRotation || previousRotation === "noRotation") {
          continue;
        }

        if (previousRotation !== currentRotation) {
          reversalCount++;
        }

        break;
      }
    });

    return reversalCount;
  }
}
