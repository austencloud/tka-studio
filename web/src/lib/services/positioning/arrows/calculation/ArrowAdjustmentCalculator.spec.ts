import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  createMotionData,
  createPictographData,
  createGridData,
} from "$lib/domain";
import {
  MotionType,
  Location,
  RotationDirection,
  GridMode,
} from "$lib/domain/enums";
import { ArrowAdjustmentCalculator } from "./ArrowAdjustmentCalculator";

describe("ArrowAdjustmentCalculator (end-to-end positioning)", () => {
  const originalFetch = global.fetch;

  beforeEach(() => {
    vi.useRealTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    global.fetch = originalFetch as typeof fetch;
  });

  it("calculates full arrow adjustment (base + directional) for diamond grid", async () => {
    // Mock special placement data
    global.fetch = vi.fn(async (url: string | URL) => {
      const u = String(url);
      if (u.includes("arrow_placement")) {
        const data = u.includes("special") ? {} : { pro: { "0": [50, 25] } };
        return new Response(JSON.stringify(data), { status: 200 });
      }
      return new Response("Not Found", { status: 404 });
    }) as unknown as typeof fetch;

    const calc = new ArrowAdjustmentCalculator();

    const motion = createMotionData({
      motionType: MotionType.PRO,
      start_loc: Location.NORTHEAST,
      end_loc: Location.SOUTHWEST,
      rotationDirection: RotationDirection.CLOCKWISE,
      turns: 0,
    });

    const pictograph = createPictographData({
      letter: "A",
      gridData: createGridData({ gridMode: GridMode.DIAMOND }),
      motions: { blue: motion, red: motion },
    });

    const result = await calc.calculateAdjustment(
      pictograph,
      motion,
      "A",
      Location.NORTHEAST,
      "blue"
    );

    // Should return some adjustment (base + directional tuple)
    expect(result).toBeDefined();
    expect(typeof result.x).toBe("number");
    expect(typeof result.y).toBe("number");
  });
});
