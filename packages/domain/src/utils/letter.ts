/**
 * Letter Type Classifier - Legacy Compatible Classification System
 * 
 * This module implements Legacy's exact letter type classification system for sectional assignment
 * in the option picker. The classifications are based on Legacy's letter_condition_mappings.py.
 * 
 * Source: src/desktop/modern/src/domain/models/letter_type_classifier.py
 */

import { LetterType } from '../models/core.js';

// ============================================================================
// LETTER TYPE CLASSIFICATIONS
// ============================================================================

// Legacy's exact letter type classifications from letter_condition_mappings.py
export const TYPE1_LETTERS = [
  "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
  "N", "O", "P", "Q", "R", "S", "T", "U", "V"
];

export const TYPE2_LETTERS = ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"];

export const TYPE3_LETTERS = ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"];

export const TYPE4_LETTERS = ["Φ", "Ψ", "Λ"];

export const TYPE5_LETTERS = ["Φ-", "Ψ-", "Λ-"];

export const TYPE6_LETTERS = ["α", "β", "Γ"];

// ============================================================================
// LETTER TYPE CLASSIFIER
// ============================================================================

/**
 * Legacy-compatible letter type classifier for option picker sectional assignment.
 * 
 * This classifier uses Legacy's exact letter type definitions to ensure identical
 * sectional assignment behavior in Modern's option picker.
 */
export class LetterTypeClassifier {
  /**
   * Get the letter type for sectional assignment using Legacy's classification.
   * 
   * @param letter - The letter to classify (e.g., "D", "W", "Φ-", etc.)
   * @returns Letter type string ("Type1", "Type2", "Type3", "Type4", "Type5", "Type6")
   *          Defaults to "Type1" for unknown letters (Legacy behavior)
   */
  static getLetterType(letter: string): string {
    if (TYPE1_LETTERS.includes(letter)) {
      return "Type1";
    } else if (TYPE2_LETTERS.includes(letter)) {
      return "Type2";
    } else if (TYPE3_LETTERS.includes(letter)) {
      return "Type3";
    } else if (TYPE4_LETTERS.includes(letter)) {
      return "Type4";
    } else if (TYPE5_LETTERS.includes(letter)) {
      return "Type5";
    } else if (TYPE6_LETTERS.includes(letter)) {
      return "Type6";
    } else {
      // Legacy default fallback behavior
      return "Type1";
    }
  }

  /**
   * Get the letter type as enum for sectional assignment using Legacy's classification.
   */
  static getLetterTypeEnum(letter: string): LetterType {
    const typeString = this.getLetterType(letter);
    switch (typeString) {
      case "Type1": return LetterType.TYPE1;
      case "Type2": return LetterType.TYPE2;
      case "Type3": return LetterType.TYPE3;
      case "Type4": return LetterType.TYPE4;
      case "Type5": return LetterType.TYPE5;
      case "Type6": return LetterType.TYPE6;
      default: return LetterType.TYPE1;
    }
  }

  /**
   * Get all available letter types.
   */
  static getAllLetterTypes(): string[] {
    return ["Type1", "Type2", "Type3", "Type4", "Type5", "Type6"];
  }

  /**
   * Get all letters that belong to a specific type.
   */
  static getLettersForType(letterType: string): string[] {
    const typeMapping: Record<string, string[]> = {
      "Type1": TYPE1_LETTERS,
      "Type2": TYPE2_LETTERS,
      "Type3": TYPE3_LETTERS,
      "Type4": TYPE4_LETTERS,
      "Type5": TYPE5_LETTERS,
      "Type6": TYPE6_LETTERS
    };
    return typeMapping[letterType] || [];
  }

  /**
   * Get statistics about letter type classifications.
   */
  static getClassificationStats(): Record<string, number> {
    return {
      "Type1": TYPE1_LETTERS.length,
      "Type2": TYPE2_LETTERS.length,
      "Type3": TYPE3_LETTERS.length,
      "Type4": TYPE4_LETTERS.length,
      "Type5": TYPE5_LETTERS.length,
      "Type6": TYPE6_LETTERS.length
    };
  }
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

/**
 * Get the letter type for a given letter (convenience function).
 */
export function getLetterType(letter: string): string {
  return LetterTypeClassifier.getLetterType(letter);
}

/**
 * Get the letter type as enum for a given letter (convenience function).
 */
export function getLetterTypeEnum(letter: string): LetterType {
  return LetterTypeClassifier.getLetterTypeEnum(letter);
}

/**
 * Check if a letter belongs to a specific type.
 */
export function isLetterOfType(letter: string, letterType: string): boolean {
  return LetterTypeClassifier.getLetterType(letter) === letterType;
}

/**
 * Get all letters for a specific type (convenience function).
 */
export function getLettersForType(letterType: string): string[] {
  return LetterTypeClassifier.getLettersForType(letterType);
}
