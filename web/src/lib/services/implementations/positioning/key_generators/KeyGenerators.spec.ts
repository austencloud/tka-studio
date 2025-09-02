import {
  createMotionData,
  createPictographData,
  MotionType,
  Orientation,
} from "$domain";
import { describe, expect, it } from "vitest";
import { SpecialPlacementOriKeyGenerator } from "./SpecialPlacementOriKeyGenerator";
import { TurnsTupleKeyGenerator } from "./TurnsTupleKeyGenerator";

describe("Key Generators", () => {
  it("SpecialPlacementOriKeyGenerator generates from_layer2 for layer2 orientations", () => {
    const gen = new SpecialPlacementOriKeyGenerator();
    const motion = createMotionData({ motionType: MotionType.PRO });
    const pictograph = createPictographData({
      motions: {
        blue: createMotionData({ endOrientation: Orientation.CLOCK }),
        red: createMotionData({ endOrientation: Orientation.COUNTER }),
      },
    });

    const key = gen.generateOrientationKey(motion, pictograph);
    expect(key).toBe("from_layer2");
  });

  it("TurnsTupleKeyGenerator returns [blueTurns, redTurns] array", () => {
    const gen = new TurnsTupleKeyGenerator();
    const pictograph = createPictographData({
      motions: {
        blue: createMotionData({ turns: 1.5 }),
        red: createMotionData({ turns: 0.5 }),
      },
    });

    const tuple = gen.generateTurnsTuple(pictograph);
    expect(tuple).toEqual([1.5, 0.5]);
  });
});
