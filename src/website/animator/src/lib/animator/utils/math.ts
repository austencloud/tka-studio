// utils/math.ts - Mathematical utilities with VALIDATED fixes
const PI = Math.PI;
const TWO_PI = 2 * PI;
const HALF_PI = PI / 2;

// Location angles (validated from HTML)
const LOCATION_ANGLES = {
  e: 0,
  s: HALF_PI,
  w: PI,
  n: -HALF_PI,
} as const;

export function normalizeAnglePositive(angle: number): number {
  return ((angle % TWO_PI) + TWO_PI) % TWO_PI;
}

export function normalizeAngleSigned(angle: number): number {
  let norm = normalizeAnglePositive(angle);
  return norm > PI ? norm - TWO_PI : norm;
}

export function mapPositionToAngle(loc: string): number {
  const l = loc?.toLowerCase() as keyof typeof LOCATION_ANGLES;
  return LOCATION_ANGLES[l] ?? 0;
}

export function mapOrientationToAngle(
  ori: string,
  centerPathAngle: number
): number {
  const l = ori.toLowerCase();

  if (LOCATION_ANGLES.hasOwnProperty(l)) {
    return LOCATION_ANGLES[l as keyof typeof LOCATION_ANGLES];
  }

  if (l === "in") return normalizeAnglePositive(centerPathAngle + PI);
  if (l === "out") return normalizeAnglePositive(centerPathAngle);

  return normalizeAnglePositive(centerPathAngle + PI);
}

export function lerp(a: number, b: number, t: number): number {
  return a * (1 - t) + b * t;
}

// ✅ IMPROVED: Angular interpolation with shortest path option
export function lerpAngle(
  a: number,
  b: number,
  t: number,
  preferShortest = true
): number {
  let d = normalizeAngleSigned(b - a);

  if (preferShortest && Math.abs(d) > PI) {
    d = d > 0 ? d - TWO_PI : d + TWO_PI;
  }

  return normalizeAnglePositive(a + d * t);
}

// ✅ FIXED: Turn calculation uses 2π not π
export function calculateTurnAngle(turns: number): number {
  return TWO_PI * turns; // Full rotations are 360° = 2π
}
