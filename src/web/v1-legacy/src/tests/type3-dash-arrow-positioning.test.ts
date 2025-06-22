// src/tests/type3-dash-arrow-positioning.test.ts
import { describe, it, expect, beforeEach } from "vitest";
import { PictographService } from "$lib/components/Pictograph/PictographService";
import type { PictographData } from "$lib/types/PictographData";
import type { MotionData } from "$lib/components/objects/Motion/MotionData";
import type { ArrowData } from "$lib/components/objects/Arrow/ArrowData";
import { Letter } from "$lib/types/Letter";
import { LetterType } from "$lib/types/LetterType";
import { DASH, PRO, RED, BLUE } from "$lib/types/Constants";
import ArrowLocationManager, {
  calculateDashLocation,
} from "$lib/components/objects/Arrow/ArrowLocationManager";
import { Motion } from "$lib/components/objects/Motion/Motion";

// Mock grid data
const mockGridData = {
  allHandPointsNormal: {
    n_diamond_hand_point: { coordinates: { x: 475, y: 330 } },
    e_diamond_hand_point: { coordinates: { x: 620, y: 475 } },
    s_diamond_hand_point: { coordinates: { x: 475, y: 620 } },
    w_diamond_hand_point: { coordinates: { x: 330, y: 475 } },
    ne_diamond_hand_point: { coordinates: { x: 618, y: 331 } },
    se_diamond_hand_point: { coordinates: { x: 618, y: 619 } },
    sw_diamond_hand_point: { coordinates: { x: 332, y: 619 } },
    nw_diamond_hand_point: { coordinates: { x: 332, y: 331 } },
  },
  allHandPointsStrict: {},
  allLayer2PointsNormal: {},
  allLayer2PointsStrict: {},
  allOuterPoints: {},
  centerPoint: { coordinates: { x: 475, y: 475 } },
};

// Create a Type 3 letter pictograph data
const createType3PictographData = (): PictographData => {
  // Using W- as a Type 3 letter
  return {
    letter: Letter.W_DASH,
    gridMode: "diamond",
    startPos: null,
    endPos: null,
    timing: null,
    direction: null,
    gridData: mockGridData,
    redMotionData: {
      id: "red-motion",
      color: RED,
      motionType: DASH,
      startLoc: "n",
      endLoc: "s",
      startOri: "in",
      endOri: "in",
      turns: 0,
      propRotDir: "cw",
      leadState: null,
      prefloatMotionType: null,
      prefloatPropRotDir: null,
    },
    blueMotionData: {
      id: "blue-motion",
      color: BLUE,
      motionType: PRO,
      startLoc: "e",
      endLoc: "w",
      startOri: "in",
      endOri: "in",
      turns: 0,
      propRotDir: "cw",
      leadState: null,
      prefloatMotionType: null,
      prefloatPropRotDir: null,
    },
    redPropData: null,
    bluePropData: null,
    redArrowData: null,
    blueArrowData: null,
    redMotion: null,
    blueMotion: null,
    motions: [],
    props: [],
    grid: "diamond",
  };
};

describe("Type 3 Dash Arrow Positioning", () => {
  let pictographData: PictographData;
  let pictographService: PictographService;
  let redArrowData: ArrowData;
  let blueArrowData: ArrowData;

  beforeEach(() => {
    // Create fresh pictograph data for each test
    pictographData = createType3PictographData();

    // Create a new PictographService with the pictograph data
    pictographService = new PictographService(pictographData);

    // Ensure the Motion objects have gridMode set
    if (pictographData.redMotion) {
      pictographData.redMotion.gridMode = "diamond";
    }

    if (pictographData.blueMotion) {
      pictographData.blueMotion.gridMode = "diamond";
    }

    // Create arrow data for testing
    if (pictographData.redMotionData) {
      redArrowData = pictographService.createArrowData(
        pictographData.redMotionData,
        RED,
      );
    }

    if (pictographData.blueMotionData) {
      blueArrowData = pictographService.createArrowData(
        pictographData.blueMotionData,
        BLUE,
      );
    }
  });

  it("should correctly identify Type 3 letters", () => {
    const letterType = LetterType.getLetterType(pictographData.letter!);
    expect(letterType).toBe(LetterType.Type3);
  });

  it("should correctly calculate dash location for Type 3 motions", () => {
    // Ensure we have motion objects
    expect(pictographData.redMotion).not.toBeNull();
    expect(pictographData.blueMotion).not.toBeNull();

    // Get the expected location from the ArrowLocationManager
    const locationManager = new ArrowLocationManager(pictographService);
    const expectedLocation = locationManager.getArrowLocation(
      pictographData.redMotion!,
      (m) => pictographService.getOtherMotion(m),
      () => pictographService.getShiftMotion(),
      pictographData.letter,
    );

    // Verify the expected location is not null
    expect(expectedLocation).not.toBeNull();

    // Verify the red arrow location matches the expected location
    expect(redArrowData.loc).toBe(expectedLocation);

    // Log the locations for debugging
    console.log("Expected dash location:", expectedLocation);
    console.log("Actual red arrow location:", redArrowData.loc);
  });

  it("should correctly position the dash arrow in the beat frame", () => {
    // Position the arrows using the PictographService
    pictographService.positionComponents(
      pictographData.redPropData,
      pictographData.bluePropData,
      redArrowData,
      blueArrowData,
      mockGridData,
    );

    // Get the expected location from the ArrowLocationManager
    const locationManager = new ArrowLocationManager(pictographService);
    const expectedLocation = locationManager.getArrowLocation(
      pictographData.redMotion!,
      (m) => pictographService.getOtherMotion(m),
      () => pictographService.getShiftMotion(),
      pictographData.letter,
    );

    // Verify the red arrow location still matches the expected location after positioning
    expect(redArrowData.loc).toBe(expectedLocation);

    // Verify the coordinates are not at the origin
    expect(redArrowData.coords.x).not.toBe(0);
    expect(redArrowData.coords.y).not.toBe(0);

    // Log the final positions for debugging
    console.log("Final red arrow location:", redArrowData.loc);
    console.log("Final red arrow coordinates:", redArrowData.coords);
  });

  it("should use calculateDashLocationBasedOnShift for Type 3 dash motions", () => {
    // Create a mock Motion object for testing
    const redMotion = new Motion(pictographData, pictographData.redMotionData!);
    const blueMotion = new Motion(
      pictographData,
      pictographData.blueMotionData!,
    );

    // Directly test the calculateDashLocation function
    const dashLocation = calculateDashLocation(
      redMotion,
      (m) => (m === redMotion ? blueMotion : null),
      () => blueMotion,
      pictographData.letter,
    );

    // Verify the dash location is calculated correctly
    expect(dashLocation).not.toBeNull();

    // Verify the red arrow location matches the calculated dash location
    expect(redArrowData.loc).toBe(dashLocation);

    // Log the locations for debugging
    console.log("Calculated dash location:", dashLocation);
    console.log("Red arrow location:", redArrowData.loc);
  });

  it("should maintain the correct dash location after updateData is called", () => {
    // Get the initial location
    const initialLocation = redArrowData.loc;

    // Update the pictograph data
    const updatedData = { ...pictographData };
    pictographService.updateData(updatedData);

    // Create new arrow data after the update
    const newRedArrowData = pictographService.createArrowData(
      pictographData.redMotionData!,
      RED,
    );

    // Verify the location is still correct
    expect(newRedArrowData.loc).toBe(initialLocation);

    // Log the locations for debugging
    console.log("Initial location:", initialLocation);
    console.log("New location after update:", newRedArrowData.loc);
  });
});
