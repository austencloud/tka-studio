/**
 * Domain types for the landing project
 * This serves as a local replacement for @tka/domain package
 */

// Complete Letter enum from TKA desktop
export enum Letter {
  // Basic Latin letters
  A = "A",
  B = "B",
  C = "C",
  D = "D",
  E = "E",
  F = "F",
  G = "G",
  H = "H",
  I = "I",
  J = "J",
  K = "K",
  L = "L",
  M = "M",
  N = "N",
  O = "O",
  P = "P",
  Q = "Q",
  R = "R",
  S = "S",
  T = "T",
  U = "U",
  V = "V",
  W = "W",
  X = "X",
  Y = "Y",
  Z = "Z",

  // Greek letters
  Σ = "Σ",
  Δ = "Δ",
  θ = "θ",
  Ω = "Ω",
  Φ = "Φ",
  Ψ = "Ψ",
  Λ = "Λ",
  α = "α",
  β = "β",
  Γ = "Γ",

  // Dash variants
  W_DASH = "W-",
  X_DASH = "X-",
  Y_DASH = "Y-",
  Z_DASH = "Z-",
  Σ_DASH = "Σ-",
  Δ_DASH = "Δ-",
  θ_DASH = "θ-",
  Ω_DASH = "Ω-",
  Φ_DASH = "Φ-",
  Ψ_DASH = "Ψ-",
  Λ_DASH = "Λ-",
}

// Basic pictograph data interface
export interface PictographData {
  id?: string;
  name?: string;
  letter?: Letter | null;
  startPos?: any;
  endPos?: any;
  timing?: any;
  direction?: any;
  gridMode?: "box" | "diamond";
  motions?: any[];
  arrows?: any[];
  props?: any[];
  grid?: any;
  metadata?: any;
}

// Motion data interface (simplified)
export interface MotionData {
  id?: string;
  type?: string;
  startPos?: any;
  endPos?: any;
  direction?: any;
  timing?: any;
}

// Arrow data interface (simplified)
export interface ArrowData {
  id?: string;
  position?: any;
  rotation?: number;
  color?: string;
  type?: string;
}

// Prop data interface (simplified)
export interface PropData {
  id?: string;
  position?: any;
  rotation?: number;
  type?: string;
}

// Grid data interface (simplified)
export interface GridData {
  mode?: "box" | "diamond";
  size?: number;
  position?: any;
}

// Export commonly used enums
export enum GridMode {
  BOX = "box",
  DIAMOND = "diamond",
}

export enum Location {
  NE = "ne",
  SE = "se",
  SW = "sw",
  NW = "nw",
}

export enum Orientation {
  CLOCK = "clock",
  COUNTER = "counter",
}

export enum MotionType {
  STATIC = "static",
  SHIFT = "shift",
  DASH = "dash",
}

export enum PropType {
  FANS = "fans",
  HANDS = "hands",
}

export enum LetterType {
  LETTER = "letter",
}

export enum VTGMode {
  NONE = "none",
}
