import {
  Location,
  MotionType,
  Orientation,
  RotationDirection,
} from "$lib/domain/enums";
import type { MotionData } from "$lib/domain/MotionData";
import { describe, expect, it } from "vitest";
import {
  DirectionalTupleCalculator,
  DirectionalTupleProcessor,
  QuadrantIndexCalculator,
} from "./DirectionalTupleProcessor";

function makeMotion(partial: Partial<MotionData>): MotionData {
  return {
    motion_type: MotionType.PRO,
    prop_rot_dir: RotationDirection.CLOCKWISE,
    start_loc: Location.NORTHEAST,
    end_loc: Location.SOUTHEAST,
    turns: 0,
    start_ori: Orientation.IN,
    end_ori: Orientation.IN,
    is_visible: true,
    prefloat_motion_type: null,
    prefloat_prop_rot_dir: null,
    ...partial,
  };
}

describe("DirectionalTupleProcessor (legacy parity)", () => {
  it("selects NE tuple for NE location in diamond grid (pro cw)", () => {
    const motion = makeMotion({
      motion_type: MotionType.PRO,
      prop_rot_dir: RotationDirection.CLOCKWISE,
      start_loc: Location.NORTHEAST,
      end_loc: Location.SOUTHEAST,
    });

    const calc = new DirectionalTupleCalculator();
    const quad = new QuadrantIndexCalculator();
    const proc = new DirectionalTupleProcessor(calc, quad);

    const base = { x: 3, y: 1 };
    const result = proc.processDirectionalTuples(
      base,
      motion,
      Location.NORTHEAST,
    );

    // For pro cw diamond, NE tuple should equal [base.x, base.y]
    expect(result).toEqual({ x: 3, y: 1 });
  });

  it("selects SE tuple for SE location in diamond grid (pro cw)", () => {
    const motion = makeMotion({
      motion_type: MotionType.PRO,
      prop_rot_dir: RotationDirection.CLOCKWISE,
      start_loc: Location.NORTHEAST,
      end_loc: Location.SOUTHEAST,
    });

    const calc = new DirectionalTupleCalculator();
    const quad = new QuadrantIndexCalculator();
    const proc = new DirectionalTupleProcessor(calc, quad);

    const base = { x: 2, y: 1 };
    const result = proc.processDirectionalTuples(
      base,
      motion,
      Location.SOUTHEAST,
    );

    // For pro cw diamond, SE tuple should equal [-base.y, base.x]
    expect(result).toEqual({ x: -1, y: 2 });
  });
});
