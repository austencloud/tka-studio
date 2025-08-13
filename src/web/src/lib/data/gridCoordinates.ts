/**
 * Grid coordinate data for pictograph rendering
 * This data defines the precise positioning points for arrows and props
 * in both diamond and box grid modes.
 *
 * Coordinates are in the 950x950 scene coordinate system with center at (475, 475)
 */

export interface GridCoordinateData {
  hand_points: {
    normal: Record<string, string>;
    strict: Record<string, string>;
  };
  layer2_points: {
    normal: Record<string, string>;
    strict: Record<string, string>;
  };
  outer_points: Record<string, string>;
  center_point: string;
}

export const gridCoordinates: Record<"diamond" | "box", GridCoordinateData> = {
  diamond: {
    hand_points: {
      normal: {
        n_diamond_hand_point: "(475.0, 331.9)",
        e_diamond_hand_point: "(618.1, 475.0)",
        s_diamond_hand_point: "(475.0, 618.1)",
        w_diamond_hand_point: "(331.9, 475.0)",
      },
      strict: {
        n_diamond_hand_point_strict: "(475.0, 325.0)",
        e_diamond_hand_point_strict: "(625.0, 475.0)",
        s_diamond_hand_point_strict: "(475.0, 625.0)",
        w_diamond_hand_point_strict: "(325.0, 475.0)",
      },
    },
    layer2_points: {
      normal: {
        ne_diamond_layer2_point: "(618.1, 331.9)",
        se_diamond_layer2_point: "(618.1, 618.1)",
        sw_diamond_layer2_point: "(331.9, 618.1)",
        nw_diamond_layer2_point: "(331.9, 331.9)",
      },
      strict: {
        ne_diamond_layer2_point_strict: "(625.0, 325.0)",
        se_diamond_layer2_point_strict: "(625.0, 625.0)",
        sw_diamond_layer2_point_strict: "(325.0, 625.0)",
        nw_diamond_layer2_point_strict: "(325.0, 325.0)",
      },
    },
    outer_points: {
      n_diamond_outer_point: "(475, 175)",
      e_diamond_outer_point: "(775, 475)",
      s_diamond_outer_point: "(475, 775)",
      w_diamond_outer_point: "(175, 475)",
    },
    center_point: "(475.0, 475.0)",
  },
  box: {
    hand_points: {
      normal: {
        ne_box_hand_point: "(576.2, 373.8)",
        se_box_hand_point: "(576.2, 576.2)",
        sw_box_hand_point: "(373.8, 576.2)",
        nw_box_hand_point: "(373.8, 373.8)",
      },
      strict: {
        ne_box_hand_point_strict: "(581.1, 368.9)",
        se_box_hand_point_strict: "(581.1, 581.1)",
        sw_box_hand_point_strict: "(368.9, 581.1)",
        nw_box_hand_point_strict: "(368.9, 368.9)",
      },
    },
    layer2_points: {
      normal: {
        n_box_layer2_point: "(475, 272.6)",
        e_box_layer2_point: "(677.4, 475)",
        s_box_layer2_point: "(475, 677.4)",
        w_box_layer2_point: "(272.6, 475)",
      },
      strict: {
        n_box_layer2_point_strict: "(475, 262.9)",
        e_box_layer2_point_strict: "(687.1, 475)",
        s_box_layer2_point_strict: "(475, 687.1)",
        w_box_layer2_point_strict: "(262.9, 475)",
      },
    },
    outer_points: {
      ne_box_outer_point: "(262.9, 247.9)",
      se_box_outer_point: "(687.1, 247.9)",
      sw_box_outer_point: "(687.1, 672.1)",
      nw_box_outer_point: "(262.9, 672.1)",
    },
    center_point: "(475.0, 475.0)",
  },
};

/**
 * Parse coordinate string "(x, y)" into {x, y} object
 */
export function parseCoordinates(
  coordString: string,
): { x: number; y: number } | null {
  if (!coordString || coordString === "None") return null;

  try {
    const parts = coordString.replace(/[()]/g, "").split(", ").map(parseFloat);
    if (parts.length !== 2) {
      console.error(`Invalid coordinate format: "${coordString}"`);
      return null;
    }
    const [x, y] = parts;
    if (x === undefined || y === undefined || isNaN(x) || isNaN(y)) {
      console.error(`Invalid coordinates parsed: "${coordString}"`);
      return null;
    }
    return { x, y };
  } catch (error) {
    console.error(`Failed to parse coordinates: "${coordString}"`, error);
    return null;
  }
}

/**
 * Convert raw coordinate data into structured GridData format
 */
export function createGridData(mode: "diamond" | "box"): GridData {
  const modeData = gridCoordinates[mode];

  const parsePoints = (points: Record<string, string>) =>
    Object.fromEntries(
      Object.entries(points).map(([key, value]) => [
        key,
        { coordinates: parseCoordinates(value) },
      ]),
    );

  return {
    allHandPointsStrict: parsePoints(modeData.hand_points.strict),
    allHandPointsNormal: parsePoints(modeData.hand_points.normal),
    allLayer2PointsStrict: parsePoints(modeData.layer2_points.strict),
    allLayer2PointsNormal: parsePoints(modeData.layer2_points.normal),
    allOuterPoints: parsePoints(modeData.outer_points),
    centerPoint: { coordinates: parseCoordinates(modeData.center_point) },
  };
}

/**
 * Grid data interface matching the legacy system
 */
export interface GridData {
  allHandPointsStrict: Record<
    string,
    { coordinates: { x: number; y: number } | null }
  >;
  allHandPointsNormal: Record<
    string,
    { coordinates: { x: number; y: number } | null }
  >;
  allLayer2PointsStrict: Record<
    string,
    { coordinates: { x: number; y: number } | null }
  >;
  allLayer2PointsNormal: Record<
    string,
    { coordinates: { x: number; y: number } | null }
  >;
  allOuterPoints: Record<
    string,
    { coordinates: { x: number; y: number } | null }
  >;
  centerPoint: { coordinates: { x: number; y: number } | null };
}
