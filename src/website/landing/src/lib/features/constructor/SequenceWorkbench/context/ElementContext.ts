/**
 * ElementContext.ts
 *
 * This module provides shared context keys and utilities for element references
 * across components in the SequenceWorkbench.
 */

// Create a context key for the beat frame element
export const BEAT_FRAME_CONTEXT_KEY = Symbol('beat-frame-element');

// Create a context key for the sequence widget element
export const SEQUENCE_WIDGET_CONTEXT_KEY = Symbol('sequence-widget-element');

// Create a context key for the current word label element
export const CURRENT_WORD_LABEL_CONTEXT_KEY = Symbol('current-word-label-element');

/**
 * Type definition for element context
 */
export interface ElementContext {
  getElement: () => HTMLElement | null;
  setElement?: (element: HTMLElement | null) => boolean;
}
