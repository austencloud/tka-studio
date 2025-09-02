import { createMotionData, createPictographData } from "$domain";
import { describe, expect, it } from "vitest";
import { TurnsTupleKeyGenerator } from "./TurnsTupleKeyGenerator";

describe("TurnsTupleKeyGenerator", () => {
  it("extracts blue and red turns from pictograph data", () => {
    const gen = new TurnsTupleKeyGenerator();
    const pg = createPictographData({
      motions: {
        blue: createMotionData({ turns: 1.5 }),
        red: createMotionData({ turns: 0.5 }),
      },
    });

    const tuple = gen.generateTurnsTuple(pg);
    expect(tuple).toEqual([1.5, 0.5]);
  });

  it("defaults to [0, 0] when data missing", () => {
    const gen = new TurnsTupleKeyGenerator();
    const pg = createPictographData({ motions: {} });

    const tuple = gen.generateTurnsTuple(pg);
    expect(tuple).toEqual([0, 0]);
  });
});
