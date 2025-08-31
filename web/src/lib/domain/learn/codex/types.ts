/**
 * Codex Domain Types
 *
 * Clean domain types for the codex system, separated from business logic.
 */

import { MotionType } from "../../enums";

export interface LetterMapping {
  startPosition: string;
  endPosition: string;
  blueMotionType: MotionType;
  redMotionType: MotionType;
}

export interface CodexLetter {
  letter: string;
  mapping: LetterMapping;
  category: LetterCategory;
  row: number;
  position: number;
}

export type LetterCategory =
  | "basic" // A-F, G-L, M-R, S-V
  | "extended" // W-Z
  | "greek" // Σ, Δ, θ, Ω
  | "dash" // W-, X-, Y-, Z-, Σ-, Δ-, θ-, Ω-
  | "special" // Φ, Ψ, Λ
  | "dual_dash" // Φ-, Ψ-, Λ-
  | "static"; // α, β, Γ

export interface LetterRow {
  index: number;
  category: LetterCategory;
  letters: string[];
}

export interface CodexConfiguration {
  letters: Record<string, LetterMapping>;
  rows: LetterRow[];
  categories: Record<LetterCategory, string[]>;
}

export interface LessonConfiguration {
  type: string;
  name: string;
  description: string;
  includedCategories: LetterCategory[];
  includedLetters?: string[];
  excludedLetters?: string[];
}

export type PictographTransformOperation = "rotate" | "mirror" | "colorSwap";
