import {
  createGridPointData,
  GridMode,
  Location,
  type GridPointData,
} from "$domain";

/**
 * DefaultPropPositioner - Calculates default prop positions using grid coordinates
 * Ported from legacy web app to ensure positioning parity
 */
export class DefaultPropPositioner {
  private fallbackCoordinates: Record<string, { x: number; y: number }> = {
    // Default positions if grid points aren't found - matching legacy fallbacks
    n: { x: 475, y: 330 },
    e: { x: 620, y: 475 },
    s: { x: 475, y: 620 },
    w: { x: 330, y: 475 },
    ne: { x: 620, y: 330 },
    se: { x: 620, y: 620 },
    sw: { x: 330, y: 620 },
    nw: { x: 330, y: 330 },
  };

  constructor(
    private gridData: GridPointData,
    private gridMode: GridMode
  ) {
    // Validate grid data on initialization
    if (!gridData || !gridData.allHandPointsNormal) {
      throw new Error("Invalid grid data provided to DefaultPropPositioner");
    }
  }

  /**
   * Calculate coordinates for a prop based on its location
   */
  public calculateCoordinates(location: Location | string): {
    x: number;
    y: number;
  } {
    // Normalize location to lowercase to match grid coordinate keys
    const normalizedLocation = (
      typeof location === "string" ? location : location
    ).toLowerCase();
    const pointName = `${normalizedLocation}_${this.gridMode.valueOf()}_hand_point`;
    const gridPoint = this.getGridPoint(pointName);

    if (gridPoint && gridPoint.coordinates) {
      return gridPoint.coordinates;
    } else {
      const fallback = this.getFallbackCoordinates(normalizedLocation);
      return fallback;
    }
  }

  /**
   * Get grid point by name from grid data
   */
  private getGridPoint(
    pointName: string
  ): { coordinates: { x: number; y: number } } | null {
    // Try to find the point in allHandPointsNormal
    if (
      this.gridData.allHandPointsNormal &&
      this.gridData.allHandPointsNormal[pointName]
    ) {
      const point = this.gridData.allHandPointsNormal[pointName];
      if (point.coordinates) {
        return { coordinates: point.coordinates };
      }
    }

    // Try alternative naming patterns
    const alternativeNames = [
      pointName,
      pointName.replace("_hand_point", ""),
      `${pointName}_normal`,
      `hand_${pointName}`,
    ];

    for (const altName of alternativeNames) {
      if (
        this.gridData.allHandPointsNormal &&
        this.gridData.allHandPointsNormal[altName]
      ) {
        const point = this.gridData.allHandPointsNormal[altName];
        if (point.coordinates) {
          return { coordinates: point.coordinates };
        }
      }
    }

    return null;
  }

  /**
   * Get fallback coordinates for a location
   */
  private getFallbackCoordinates(location: string): { x: number; y: number } {
    return this.fallbackCoordinates[location] || { x: 475, y: 475 }; // Center fallback
  }

  /**
   * Static helper method for quick coordinate calculation
   */
  static calculatePosition(
    location: Location,
    gridMode: GridMode
  ): { x: number; y: number } {
    try {
      const gridPointData = createGridPointData(gridMode);
      const positioner = new DefaultPropPositioner(gridPointData, gridMode);
      const result = positioner.calculateCoordinates(location);
      return result;
    } catch (error) {
      console.error("Error calculating position:", error);
      // Return center as ultimate fallback
      return { x: 475, y: 475 };
    }
  }
}

export default DefaultPropPositioner;
