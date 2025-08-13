import { Orientation } from "$lib/domain/enums";

/**
 * PropRotAngleManager - Calculates prop rotation angles based on location and orientation
 * Ported from legacy web app to ensure rotation parity
 */
export class PropRotAngleManager {
  private loc: string;
  private ori: Orientation | null;

  constructor({ loc, ori }: { loc: string; ori: Orientation | null }) {
    this.loc = loc;
    this.ori = ori;
  }

  /**
   * Get rotation angle based on location and orientation
   * Uses diamond vs box grid mode detection and appropriate angle maps
   */
  getRotationAngle(): number {
    const isDiamondLocation = ["n", "e", "s", "w"].includes(this.loc);

    const diamondAngleMap: Partial<
      Record<Orientation, Partial<Record<string, number>>>
    > = {
      [Orientation.IN]: { n: 90, s: 270, w: 0, e: 180 },
      [Orientation.OUT]: { n: 270, s: 90, w: 180, e: 0 },
      [Orientation.CLOCK]: { n: 0, s: 180, w: 270, e: 90 },
      [Orientation.COUNTER]: { n: 180, s: 0, w: 90, e: 270 },
    };

    const boxAngleMap: Partial<
      Record<Orientation, Partial<Record<string, number>>>
    > = {
      [Orientation.IN]: { ne: 135, nw: 45, sw: 315, se: 225 },
      [Orientation.OUT]: { ne: 315, nw: 225, sw: 135, se: 45 },
      [Orientation.CLOCK]: { ne: 45, nw: 315, sw: 225, se: 135 },
      [Orientation.COUNTER]: { ne: 225, nw: 135, sw: 45, se: 315 },
    };

    const angleMap = isDiamondLocation ? diamondAngleMap : boxAngleMap;
    const orientationAngles = angleMap[this.ori as Orientation];

    return orientationAngles?.[this.loc] ?? 0;
  }

  /**
   * Static helper method for quick rotation calculation
   */
  static calculateRotation(loc: string, ori: Orientation | null): number {
    const manager = new PropRotAngleManager({ loc, ori });
    return manager.getRotationAngle();
  }
}

export default PropRotAngleManager;
