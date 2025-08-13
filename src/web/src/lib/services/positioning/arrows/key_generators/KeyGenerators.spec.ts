import { describe, expect, it } from "vitest";
import { PlacementKeyGenerator } from "./PlacementKeyGenerator";
import { SpecialPlacementOriKeyGenerator } from "./SpecialPlacementOriKeyGenerator";
import { TurnsTupleKeyGenerator } from "./TurnsTupleKeyGenerator";

type MotionData = any;
type PictographData = any;

describe("Key Generators", () => {
  it("PlacementKeyGenerator selects first available key from candidates", () => {
    const gen = new PlacementKeyGenerator();
    const motion: MotionData = { motion_type: "pro" };
    const pictograph: PictographData = { letter: "A" };
    const available = { pro_to_layer1_alpha_A: true, pro: true };

    const key = gen.generatePlacementKey(motion, pictograph, available);
    expect(key).toBe("pro_to_layer1_alpha_A");
  });

  it("SpecialPlacementOriKeyGenerator generates from_layer2 for layer2 orientations", () => {
    const gen = new SpecialPlacementOriKeyGenerator();
    const motion: MotionData = { motion_type: "pro" };
    const pictograph: PictographData = {
      motions: {
        blue: { end_ori: "alpha" },
        red: { end_ori: "beta" },
      },
    };

    const key = gen.generateOrientationKey(motion, pictograph);
    expect(key).toBe("from_layer2");
  });

  it("TurnsTupleKeyGenerator returns [blueTurns, redTurns] array", () => {
    const gen = new TurnsTupleKeyGenerator();
    const pictograph: PictographData = {
      motions: {
        blue: { turns: 1.5 },
        red: { turns: 0.5 },
      },
    };

    const tuple = gen.generateTurnsTuple(pictograph);
    expect(tuple).toEqual([1.5, 0.5]);
  });
});
