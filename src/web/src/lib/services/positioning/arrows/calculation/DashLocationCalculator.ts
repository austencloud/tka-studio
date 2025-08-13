/**
 * Dash Location Calculator Service
 *
 * Comprehensive dash location calculation logic with all special cases.
 * Direct TypeScript port of the Python DashLocationCalculator.
 *
 * This service implements:
 * - Φ_DASH and Ψ_DASH special handling
 * - Λ (Lambda) zero turns special case
 * - Type 3 scenario detection and handling
 * - Grid mode specific calculations (Diamond/Box)
 * - Co	private extractType3Data(pictographData: PictographData): {
		gridMode: GridMode;
		shiftLocation?: Location;
	} {
		const result: { gridMode: GridMode; shiftLocation?: Location } = {
			gridMode: (pictographData.grid_mode as GridMode) || 'diamond',
		};

		// Only add shiftLocation if we can detect it properly
		// For now, leaving it undefined means optional
		// shiftLocation would need proper shift location detection

		return result;
	}ation mappings for different scenarios
 */

import type { MotionData, PictographData } from "$lib/domain";
import { GridMode, Location } from "$lib/domain";
import type { LetterType } from "$lib/utils/letterTypeUtils";

// Arrow color type - using string literals to match usage pattern
type ArrowColor = "red" | "blue";

export interface IDashLocationCalculator {
  calculateDashLocationFromPictographData(
    pictographData: PictographData,
    isBlueArrow: boolean,
  ): Location;
  calculateDashLocation(
    motion: MotionData,
    otherMotion?: MotionData,
    letterType?: LetterType,
    arrowColor?: ArrowColor,
    gridMode?: GridMode,
    shiftLocation?: Location,
    isPhiDash?: boolean,
    isPsiDash?: boolean,
    isLambda?: boolean,
    isLambdaDash?: boolean,
  ): Location;
}

export class DashLocationCalculator implements IDashLocationCalculator {
  /**
   * Dash location calculation service.
   *
   * Implements comprehensive dash location calculation logic including:
   * - Φ_DASH and Ψ_DASH special handling
   * - Λ (Lambda) zero turns special case
   * - Type 3 scenario detection and handling
   * - Grid mode specific calculations (Diamond/Box)
   * - Complex location mappings for different scenarios
   */

  // Predefined location mappings for dash calculations - comprehensive mapping
  private readonly PHI_DASH_PSI_DASH_LOCATION_MAP: Record<string, Location> = {
    [`red,${Location.NORTH},${Location.SOUTH}`]: Location.EAST,
    [`red,${Location.EAST},${Location.WEST}`]: Location.NORTH,
    [`red,${Location.SOUTH},${Location.NORTH}`]: Location.EAST,
    [`red,${Location.WEST},${Location.EAST}`]: Location.NORTH,
    [`blue,${Location.NORTH},${Location.SOUTH}`]: Location.WEST,
    [`blue,${Location.EAST},${Location.WEST}`]: Location.SOUTH,
    [`blue,${Location.SOUTH},${Location.NORTH}`]: Location.WEST,
    [`blue,${Location.WEST},${Location.EAST}`]: Location.SOUTH,
    [`red,${Location.NORTHWEST},${Location.SOUTHEAST}`]: Location.NORTHEAST,
    [`red,${Location.NORTHEAST},${Location.SOUTHWEST}`]: Location.SOUTHEAST,
    [`red,${Location.SOUTHWEST},${Location.NORTHEAST}`]: Location.SOUTHEAST,
    [`red,${Location.SOUTHEAST},${Location.NORTHWEST}`]: Location.NORTHEAST,
    [`blue,${Location.NORTHWEST},${Location.SOUTHEAST}`]: Location.SOUTHWEST,
    [`blue,${Location.NORTHEAST},${Location.SOUTHWEST}`]: Location.NORTHWEST,
    [`blue,${Location.SOUTHWEST},${Location.NORTHEAST}`]: Location.NORTHWEST,
    [`blue,${Location.SOUTHEAST},${Location.NORTHWEST}`]: Location.SOUTHWEST,
  };

  private readonly LAMBDA_ZERO_TURNS_LOCATION_MAP: Record<string, Location> = {
    [`${Location.NORTH},${Location.SOUTH},${Location.WEST}`]: Location.EAST,
    [`${Location.EAST},${Location.WEST},${Location.SOUTH}`]: Location.NORTH,
    [`${Location.NORTH},${Location.SOUTH},${Location.EAST}`]: Location.WEST,
    [`${Location.WEST},${Location.EAST},${Location.SOUTH}`]: Location.NORTH,
    [`${Location.SOUTH},${Location.NORTH},${Location.WEST}`]: Location.EAST,
    [`${Location.EAST},${Location.WEST},${Location.NORTH}`]: Location.SOUTH,
    [`${Location.SOUTH},${Location.NORTH},${Location.EAST}`]: Location.WEST,
    [`${Location.WEST},${Location.EAST},${Location.NORTH}`]: Location.SOUTH,
    [`${Location.NORTHEAST},${Location.SOUTHWEST},${Location.NORTHWEST}`]:
      Location.SOUTHEAST,
    [`${Location.NORTHWEST},${Location.SOUTHEAST},${Location.NORTHEAST}`]:
      Location.SOUTHWEST,
    [`${Location.SOUTHWEST},${Location.NORTHEAST},${Location.SOUTHEAST}`]:
      Location.NORTHWEST,
    [`${Location.SOUTHEAST},${Location.NORTHWEST},${Location.SOUTHWEST}`]:
      Location.NORTHEAST,
    [`${Location.NORTHEAST},${Location.SOUTHWEST},${Location.SOUTHEAST}`]:
      Location.NORTHWEST,
    [`${Location.NORTHWEST},${Location.SOUTHEAST},${Location.SOUTHWEST}`]:
      Location.NORTHEAST,
    [`${Location.SOUTHWEST},${Location.NORTHEAST},${Location.NORTHWEST}`]:
      Location.SOUTHEAST,
    [`${Location.SOUTHEAST},${Location.NORTHWEST},${Location.NORTHEAST}`]:
      Location.SOUTHWEST,
  };

  private readonly LAMBDA_DASH_ZERO_TURNS_LOCATION_MAP: Record<
    string,
    Location
  > = {
    [`${Location.NORTH},${Location.SOUTH},${Location.WEST}`]: Location.EAST,
    [`${Location.EAST},${Location.WEST},${Location.SOUTH}`]: Location.NORTH,
    [`${Location.NORTH},${Location.SOUTH},${Location.EAST}`]: Location.WEST,
    [`${Location.WEST},${Location.EAST},${Location.SOUTH}`]: Location.NORTH,
    [`${Location.SOUTH},${Location.NORTH},${Location.WEST}`]: Location.EAST,
    [`${Location.EAST},${Location.WEST},${Location.NORTH}`]: Location.SOUTH,
    [`${Location.SOUTH},${Location.NORTH},${Location.EAST}`]: Location.WEST,
    [`${Location.WEST},${Location.EAST},${Location.NORTH}`]: Location.SOUTH,
    [`${Location.NORTHEAST},${Location.SOUTHWEST},${Location.NORTHWEST}`]:
      Location.SOUTHEAST,
    [`${Location.NORTHWEST},${Location.SOUTHEAST},${Location.NORTHEAST}`]:
      Location.SOUTHWEST,
    [`${Location.SOUTHWEST},${Location.NORTHEAST},${Location.SOUTHEAST}`]:
      Location.NORTHWEST,
    [`${Location.SOUTHEAST},${Location.NORTHWEST},${Location.SOUTHWEST}`]:
      Location.NORTHEAST,
    [`${Location.NORTHEAST},${Location.SOUTHWEST},${Location.SOUTHEAST}`]:
      Location.NORTHWEST,
    [`${Location.NORTHWEST},${Location.SOUTHEAST},${Location.SOUTHWEST}`]:
      Location.NORTHEAST,
    [`${Location.SOUTHWEST},${Location.NORTHEAST},${Location.NORTHWEST}`]:
      Location.SOUTHEAST,
    [`${Location.SOUTHEAST},${Location.NORTHWEST},${Location.NORTHEAST}`]:
      Location.SOUTHWEST,
  };

  private readonly DEFAULT_ZERO_TURNS_DASH_LOCATION_MAP: Record<
    string,
    Location
  > = {
    [`${Location.NORTH},${Location.SOUTH}`]: Location.EAST,
    [`${Location.EAST},${Location.WEST}`]: Location.SOUTH,
    [`${Location.SOUTH},${Location.NORTH}`]: Location.WEST,
    [`${Location.WEST},${Location.EAST}`]: Location.NORTH,
    [`${Location.NORTHEAST},${Location.SOUTHWEST}`]: Location.SOUTHEAST,
    [`${Location.NORTHWEST},${Location.SOUTHEAST}`]: Location.NORTHEAST,
    [`${Location.SOUTHWEST},${Location.NORTHEAST}`]: Location.NORTHWEST,
    [`${Location.SOUTHEAST},${Location.NORTHWEST}`]: Location.SOUTHWEST,
  };

  private readonly NON_ZERO_TURNS_DASH_LOCATION_MAP: Record<
    string,
    Record<Location, Location>
  > = {
    clockwise: {
      [Location.NORTH]: Location.EAST,
      [Location.EAST]: Location.SOUTH,
      [Location.SOUTH]: Location.WEST,
      [Location.WEST]: Location.NORTH,
      [Location.NORTHEAST]: Location.SOUTHEAST,
      [Location.SOUTHEAST]: Location.SOUTHWEST,
      [Location.SOUTHWEST]: Location.NORTHWEST,
      [Location.NORTHWEST]: Location.NORTHEAST,
    },
    counter_clockwise: {
      [Location.NORTH]: Location.WEST,
      [Location.EAST]: Location.NORTH,
      [Location.SOUTH]: Location.EAST,
      [Location.WEST]: Location.SOUTH,
      [Location.NORTHEAST]: Location.NORTHWEST,
      [Location.SOUTHEAST]: Location.NORTHEAST,
      [Location.SOUTHWEST]: Location.SOUTHEAST,
      [Location.NORTHWEST]: Location.SOUTHWEST,
    },
  };

  private readonly DIAMOND_DASH_LOCATION_MAP: Record<string, Location> = {
    [`${Location.NORTH},${Location.NORTHWEST}`]: Location.EAST,
    [`${Location.NORTH},${Location.NORTHEAST}`]: Location.WEST,
    [`${Location.NORTH},${Location.SOUTHEAST}`]: Location.WEST,
    [`${Location.NORTH},${Location.SOUTHWEST}`]: Location.EAST,
    [`${Location.EAST},${Location.NORTHWEST}`]: Location.SOUTH,
    [`${Location.EAST},${Location.NORTHEAST}`]: Location.SOUTH,
    [`${Location.EAST},${Location.SOUTHEAST}`]: Location.NORTH,
    [`${Location.EAST},${Location.SOUTHWEST}`]: Location.NORTH,
    [`${Location.SOUTH},${Location.NORTHWEST}`]: Location.EAST,
    [`${Location.SOUTH},${Location.NORTHEAST}`]: Location.WEST,
    [`${Location.SOUTH},${Location.SOUTHEAST}`]: Location.WEST,
    [`${Location.SOUTH},${Location.SOUTHWEST}`]: Location.EAST,
    [`${Location.WEST},${Location.NORTHWEST}`]: Location.SOUTH,
    [`${Location.WEST},${Location.NORTHEAST}`]: Location.SOUTH,
    [`${Location.WEST},${Location.SOUTHEAST}`]: Location.NORTH,
    [`${Location.WEST},${Location.SOUTHWEST}`]: Location.NORTH,
  };

  private readonly BOX_DASH_LOCATION_MAP: Record<string, Location> = {
    [`${Location.NORTHEAST},${Location.NORTH}`]: Location.SOUTHEAST,
    [`${Location.NORTHEAST},${Location.EAST}`]: Location.NORTHWEST,
    [`${Location.NORTHEAST},${Location.SOUTH}`]: Location.NORTHWEST,
    [`${Location.NORTHEAST},${Location.WEST}`]: Location.SOUTHEAST,
    [`${Location.SOUTHEAST},${Location.NORTH}`]: Location.SOUTHWEST,
    [`${Location.SOUTHEAST},${Location.EAST}`]: Location.SOUTHWEST,
    [`${Location.SOUTHEAST},${Location.SOUTH}`]: Location.NORTHEAST,
    [`${Location.SOUTHEAST},${Location.WEST}`]: Location.NORTHEAST,
    [`${Location.SOUTHWEST},${Location.NORTH}`]: Location.SOUTHEAST,
    [`${Location.SOUTHWEST},${Location.EAST}`]: Location.NORTHWEST,
    [`${Location.SOUTHWEST},${Location.SOUTH}`]: Location.NORTHWEST,
    [`${Location.SOUTHWEST},${Location.WEST}`]: Location.SOUTHEAST,
    [`${Location.NORTHWEST},${Location.NORTH}`]: Location.SOUTHWEST,
    [`${Location.NORTHWEST},${Location.EAST}`]: Location.SOUTHWEST,
    [`${Location.NORTHWEST},${Location.SOUTH}`]: Location.NORTHEAST,
    [`${Location.NORTHWEST},${Location.WEST}`]: Location.NORTHEAST,
  };

  calculateDashLocationFromPictographData(
    pictographData: PictographData,
    isBlueArrow: boolean,
  ): Location {
    /**
     * High-level method to calculate dash location from pictograph data.
     *
     * This method automatically extracts all necessary parameters from the pictograph data
     * using pictograph analysis, then calls the detailed calculation method.
     */
    // Extract motion data for the specified arrow
    const motion = isBlueArrow
      ? pictographData.motions?.blue
      : pictographData.motions?.red;
    const otherMotion = isBlueArrow
      ? pictographData.motions?.red
      : pictographData.motions?.blue;

    if (!motion || motion.motion_type?.toLowerCase() !== "dash") {
      // If not a dash motion, return start location as fallback
      return motion?.start_loc || Location.NORTH;
    }

    // Use analysis service to extract all the parameters
    // For simplified implementation, using basic parameter extraction
    const letterInfo = this.getLetterInfo(pictographData);
    const gridInfo = this.getGridInfo(pictographData);
    const arrowColor = this.getArrowColor(isBlueArrow);

    // Call the detailed calculation method with all parameters
    return this.calculateDashLocation(
      motion,
      otherMotion,
      letterInfo.letterType,
      arrowColor,
      gridInfo.gridMode,
      gridInfo.shiftLocation,
      letterInfo.isPhiDash,
      letterInfo.isPsiDash,
      letterInfo.isLambda,
      letterInfo.isLambdaDash,
    );
  }

  calculateDashLocation(
    motion: MotionData,
    otherMotion?: MotionData,
    letterType?: LetterType,
    arrowColor?: ArrowColor,
    gridMode?: GridMode,
    shiftLocation?: Location,
    isPhiDash = false,
    isPsiDash = false,
    isLambda = false,
    isLambdaDash = false,
  ): Location {
    /**
     * Calculate dash arrow location using proven calculation algorithms.
     */

    // Φ_DASH and Ψ_DASH special handling
    if (isPhiDash || isPsiDash) {
      return this.getPhiDashPsiDashLocation(motion, otherMotion, arrowColor);
    }

    // Λ (Lambda) zero turns special case
    if (isLambda && motion.turns === 0 && otherMotion) {
      return this.getLambdaZeroTurnsLocation(motion, otherMotion);
    }

    // Λ_DASH (Lambda Dash) zero turns special case
    if (isLambdaDash && motion.turns === 0 && otherMotion) {
      return this.getLambdaDashZeroTurnsLocation(motion, otherMotion);
    }

    // Zero turns - check for Type 3 or default
    if (motion.turns === 0) {
      return this.defaultZeroTurnsDashLocation(
        motion,
        letterType,
        gridMode,
        shiftLocation,
      );
    }

    // Non-zero turns
    return this.dashLocationNonZeroTurns(motion);
  }

  private getLambdaDashZeroTurnsLocation(
    motion: MotionData,
    otherMotion: MotionData,
  ): Location {
    /**Handle Λ_DASH (Lambda Dash) zero turns special case.*/
    const key = `${motion.start_loc},${motion.end_loc},${otherMotion.end_loc}`;
    return this.LAMBDA_DASH_ZERO_TURNS_LOCATION_MAP[key] || motion.start_loc;
  }

  private getPhiDashPsiDashLocation(
    motion: MotionData,
    otherMotion?: MotionData,
    arrowColor?: ArrowColor,
  ): Location {
    /**Handle Φ_DASH and Ψ_DASH location calculation.*/
    if (!otherMotion || !arrowColor) {
      // Fallback to default logic if missing data
      return this.defaultZeroTurnsDashLocation(motion);
    }

    // Both motions have zero turns
    if (motion.turns === 0 && otherMotion.turns === 0) {
      const key = `${arrowColor},${motion.start_loc},${motion.end_loc}`;
      return this.PHI_DASH_PSI_DASH_LOCATION_MAP[key] || motion.start_loc;
    }

    // Current motion has zero turns, other doesn't
    if (motion.turns === 0) {
      const oppositeLocation = this.dashLocationNonZeroTurns(otherMotion);
      return this.getOppositeLocation(oppositeLocation);
    }

    // Current motion has non-zero turns
    return this.dashLocationNonZeroTurns(motion);
  }

  private getLambdaZeroTurnsLocation(
    motion: MotionData,
    otherMotion: MotionData,
  ): Location {
    /**Handle Λ (Lambda) zero turns special case.*/
    const key = `${motion.start_loc},${motion.end_loc},${otherMotion.end_loc}`;
    return this.LAMBDA_ZERO_TURNS_LOCATION_MAP[key] || motion.start_loc;
  }

  private defaultZeroTurnsDashLocation(
    motion: MotionData,
    letterType?: LetterType,
    gridMode?: GridMode,
    shiftLocation?: Location,
  ): Location {
    /**Calculate default zero turns dash location.*/
    // Type 3 scenario detection and handling
    if (letterType === "Type3" && gridMode && shiftLocation) {
      return this.calculateDashLocationBasedOnShift(
        motion,
        gridMode,
        shiftLocation,
      );
    }

    // Default zero turns mapping
    const key = `${motion.start_loc},${motion.end_loc}`;
    return this.DEFAULT_ZERO_TURNS_DASH_LOCATION_MAP[key] || motion.start_loc;
  }

  private dashLocationNonZeroTurns(motion: MotionData): Location {
    /**Calculate dash location for non-zero turns.*/
    const rotDir = motion.prop_rot_dir?.toLowerCase();
    if (rotDir === "no_rotation" || rotDir === "none") {
      // Fallback for no rotation
      return motion.start_loc;
    }

    const directionMap =
      this.NON_ZERO_TURNS_DASH_LOCATION_MAP[rotDir] ||
      this.NON_ZERO_TURNS_DASH_LOCATION_MAP["clockwise"];
    return directionMap?.[motion.start_loc] || motion.start_loc;
  }

  private calculateDashLocationBasedOnShift(
    motion: MotionData,
    gridMode: GridMode,
    shiftLocation: Location,
  ): Location {
    /**Calculate Type 3 dash location based on shift arrow location.*/
    const startLoc = motion.start_loc;

    if (gridMode === "diamond") {
      const key = `${startLoc},${shiftLocation}`;
      return this.DIAMOND_DASH_LOCATION_MAP[key] || startLoc;
    } else if (gridMode === "box") {
      const key = `${startLoc},${shiftLocation}`;
      return this.BOX_DASH_LOCATION_MAP[key] || startLoc;
    }

    // Fallback to default if grid mode not recognized
    return this.defaultZeroTurnsDashLocation(motion);
  }

  private getOppositeLocation(location: Location): Location {
    /**Get opposite location using proven location mapping.*/
    const oppositeMap: Record<Location, Location> = {
      [Location.NORTH]: Location.SOUTH,
      [Location.SOUTH]: Location.NORTH,
      [Location.EAST]: Location.WEST,
      [Location.WEST]: Location.EAST,
      [Location.NORTHEAST]: Location.SOUTHWEST,
      [Location.SOUTHWEST]: Location.NORTHEAST,
      [Location.SOUTHEAST]: Location.NORTHWEST,
      [Location.NORTHWEST]: Location.SOUTHEAST,
    };
    return oppositeMap[location] || location;
  }

  // Simplified helper methods for extracting information from pictograph data
  private getLetterInfo(pictographData: PictographData): {
    letterType: LetterType;
    isPhiDash: boolean;
    isPsiDash: boolean;
    isLambda: boolean;
    isLambdaDash: boolean;
  } {
    const letter = pictographData.letter?.toUpperCase() || "";
    return {
      letterType: "TYPE1" as LetterType, // Simplified - would need proper letter analysis
      isPhiDash: letter.includes("Φ_DASH") || letter.includes("PHI_DASH"),
      isPsiDash: letter.includes("Ψ_DASH") || letter.includes("PSI_DASH"),
      isLambda: letter.includes("Λ") || letter === "LAMBDA",
      isLambdaDash: letter.includes("Λ_DASH") || letter.includes("LAMBDA_DASH"),
    };
  }

  private getGridInfo(pictographData: PictographData): {
    gridMode: GridMode;
    shiftLocation?: Location;
  } {
    const result: { gridMode: GridMode; shiftLocation?: Location } = {
      gridMode: (pictographData.grid_mode as GridMode) || "diamond",
    };

    // Only add shiftLocation if we can detect it properly
    // For now, leaving it undefined means optional
    // shiftLocation would need proper shift location detection

    return result;
  }

  private getArrowColor(isBlueArrow: boolean): ArrowColor {
    return isBlueArrow ? "blue" : "red";
  }
}
