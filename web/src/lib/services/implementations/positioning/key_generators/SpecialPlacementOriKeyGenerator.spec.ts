import { createMotionData, createPictographData, Orientation } from "$domain";
import { describe, expect, it } from "vitest";
import { SpecialPlacementOriKeyGenerator } from "./SpecialPlacementOriKeyGenerator";

describe("SpecialPlacementOriKeyGenerator", () => {
  it("returns from_layer1 for in/out orientations", () => {
    const gen = new SpecialPlacementOriKeyGenerator();
    const pictograph = createPictographData({
      motions: {
        blue: createMotionData({ endOrientation: Orientation.IN }),
        red: createMotionData({ endOrientation: Orientation.OUT }),
      },
    });

    const key = gen.generateOrientationKey(createMotionData(), pictograph);
    expect(key).toBe("from_layer1");
  });

  it("returns from_layer3_blue1_red2 for mixed orientations", () => {
    const gen = new SpecialPlacementOriKeyGenerator();
    const pictograph = createPictographData({
      motions: {
        blue: createMotionData({ endOrientation: Orientation.IN }),
        red: createMotionData({ endOrientation: Orientation.CLOCK }),
      },
    });

    const key = gen.generateOrientationKey(createMotionData(), pictograph);
    expect(key).toBe("from_layer3_blue1_red2");
  });

  it("returns from_layer2 for alpha/beta orientations", () => {
    const gen = new SpecialPlacementOriKeyGenerator();
    const pictograph = createPictographData({
      motions: {
        blue: createMotionData({ endOrientation: Orientation.CLOCK }),
        red: createMotionData({ endOrientation: Orientation.COUNTER }),
      },
    });

    const key = gen.generateOrientationKey(createMotionData(), pictograph);
    expect(key).toBe("from_layer2");
  });
});
