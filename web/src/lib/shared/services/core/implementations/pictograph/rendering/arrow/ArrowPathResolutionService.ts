/**
 * Arrow Path Resolution Service
 *
 * Responsible for determining the correct SVG file path based on motion data.
 * Extracted from ArrowRenderer to improve modularity and reusability.
 */

import type { ArrowPlacementData, MotionData } from "$domain";
import type { IArrowPathResolutionService } from "$services";
import { injectable } from "inversify";

@injectable()
export class ArrowPathResolutionService implements IArrowPathResolutionService {
  /**
   * Get arrow SVG path based on motion type and properties (extracted from Arrow.svelte)
   */
  getArrowPath(
    arrowData: ArrowPlacementData,
    motionData: MotionData
  ): string | null {
    if (!arrowData || !motionData) {
      console.warn(
        "🚫 ArrowPathResolutionService: Missing arrowData or motionData, cannot determine arrow path"
      );
      return null;
    }

    const { motionType, turns } = motionData;
    const baseDir = `/images/arrows/${motionType}`;

    // For motion types that have turn-based subdirectories (pro, anti, static)
    if (["pro", "anti", "static"].includes(motionType)) {
      // Determine if we should use radial vs non-radial arrows
      // Use non-radial only for clock/counter orientations, radial for everything else
      // ✅ FIXED: Orientation data comes from MotionData only
      const startOrientation = motionData.startOrientation || "in";
      const endOrientation = motionData.endOrientation || "in";

      const isNonRadial =
        startOrientation === "clock" ||
        startOrientation === "counter" ||
        endOrientation === "clock" ||
        endOrientation === "counter";

      const subDir = isNonRadial ? "from_nonradial" : "from_radial";
      const turnValue = typeof turns === "number" ? turns.toFixed(1) : "0.0";
      const path = `${baseDir}/${subDir}/${motionType}_${turnValue}.svg`;

      return path;
    }

    // For simple motion types (dash, float) - use base directory
    const path = `${baseDir}.svg`;
    return path;
  }

  /**
   * Get the correct arrow SVG path based on motion data (optimized version)
   */
  getArrowSvgPath(motionData: MotionData | undefined): string {
    if (!motionData) {
      return "/images/arrows/static/from_radial/static_0.svg";
    }

    const motionType = motionData.motionType;
    const turnsVal = motionData.turns;
    const startOrientation = motionData.startOrientation;

    if (motionType === "float") {
      return "/images/arrows/float.svg";
    }

    const radialPath =
      startOrientation === "in" ? "from_radial" : "from_nonradial";

    let turnsStr: string;
    if (turnsVal === "fl") {
      turnsStr = "fl";
    } else if (typeof turnsVal === "number") {
      turnsStr = turnsVal % 1 === 0 ? `${turnsVal}.0` : turnsVal.toString();
    } else {
      turnsStr = "0.0";
    }

    return `/images/arrows/${motionType}/${radialPath}/${motionType}_${turnsStr}.svg`;
  }
}
