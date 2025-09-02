/**
 * Codex Models
 *
 * Interface definitions for the codex system.
 */

import type { LetterCategory } from "$domain";
import { MotionType } from "$domain";

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

export interface LetterRow {
  index: number;
  category: LetterCategory;
  letters: string[];
}

export interface CodexConfiguration {
  version: string;
  letters: Record<string, LetterMapping>;
  rows: LetterRow[];
  categories: Record<LetterCategory, string[]>;
}

export interface LessonConfiguration {
  id?: string; // Added for LessonRepository usage
  type: string;
  name: string;
  description: string;
  includedCategories: LetterCategory[];
  includedLetters?: string[];
  excludedLetters?: string[];
  categories?: LetterCategory[]; // Added for LessonRepository usage
  letters?: string[]; // Added for LessonRepository usage
  difficulty?: number; // Added for LessonRepository usage
}

// Factory functions
export function createLetterRow(data: Partial<LetterRow>): LetterRow {
  return {
    index: data.index ?? 0,
    category: data.category ?? ("BASIC" as LetterCategory),
    letters: data.letters ?? [],
  };
}

export function createLetterMapping(
  data: Partial<LetterMapping>
): LetterMapping {
  return {
    startPosition: data.startPosition ?? "",
    endPosition: data.endPosition ?? "",
    blueMotionType: data.blueMotionType ?? ("STATIC" as MotionType),
    redMotionType: data.redMotionType ?? ("STATIC" as MotionType),
  };
}

export function createCodexLetter(data: Partial<CodexLetter>): CodexLetter {
  return {
    letter: data.letter ?? "",
    mapping: data.mapping ?? createLetterMapping({}),
    category: data.category ?? ("BASIC" as LetterCategory),
    row: data.row ?? 0,
    position: data.position ?? 0,
  };
}
