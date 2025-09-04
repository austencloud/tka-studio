/**
 * Codex Models
 *
 * Interface definitions for the codex system.
 */

import { MotionType } from "$shared/domain";
import type { LetterCategory } from "../types/CodexTypes";

export interface CodexLetterMapping {
  startPosition: string;
  endPosition: string;
  blueMotionType: MotionType;
  redMotionType: MotionType;
}

export interface CodexLetter {
  letter: string;
  mapping: CodexLetterMapping;
  category: LetterCategory;
  row: number;
  position: number;
}

export interface CodexLetterRow {
  index: number;
  category: LetterCategory;
  letters: string[];
}

export interface CodexConfiguration {
  version: string;
  letters: Record<string, CodexLetterMapping>;
  rows: CodexLetterRow[];
  categories: Record<LetterCategory, string[]>;
}

export interface QuizLessonConfiguration {
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
export function createLetterRow(data: Partial<CodexLetterRow>): CodexLetterRow {
  return {
    index: data.index ?? 0,
    category: data.category ?? ("BASIC" as LetterCategory),
    letters: data.letters ?? [],
  };
}

export function createLetterMapping(
  data: Partial<CodexLetterMapping>
): CodexLetterMapping {
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
