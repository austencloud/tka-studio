/**
 * Keyboard Event Domain Model
 *
 * Represents a normalized keyboard event with cross-platform support.
 *
 * Domain: Keyboard Shortcuts
 */

import type {
  KeyModifier,
  KeyboardEventDetails,
} from "../types/keyboard-types";

export class NormalizedKeyboardEvent implements KeyboardEventDetails {
  key: string;
  modifiers: KeyModifier[];
  ctrlOrMeta: boolean;
  originalEvent: KeyboardEvent;
  target: EventTarget | null;
  isInputTarget: boolean;

  constructor(event: KeyboardEvent) {
    this.originalEvent = event;
    this.target = event.target;
    this.key = this.normalizeKey(event.key);
    this.modifiers = this.extractModifiers(event);
    this.ctrlOrMeta = this.detectCtrlOrMeta();
    this.isInputTarget = this.checkIfInputTarget(event.target);
  }

  /**
   * Normalize the key value for consistent comparison
   */
  private normalizeKey(key: string): string {
    // Handle special key mappings
    const keyMap: Record<string, string> = {
      " ": "Space",
      Esc: "Escape",
    };

    return keyMap[key] || key;
  }

  /**
   * Extract active modifiers from the event
   */
  private extractModifiers(event: KeyboardEvent): KeyModifier[] {
    const modifiers: KeyModifier[] = [];

    if (event.ctrlKey) modifiers.push("ctrl");
    if (event.altKey) modifiers.push("alt");
    if (event.shiftKey) modifiers.push("shift");
    if (event.metaKey) modifiers.push("meta");

    return modifiers;
  }

  /**
   * Detect if Ctrl (Windows/Linux) or Meta (Mac) was pressed
   * This allows shortcuts defined with "ctrl" to work with Cmd on Mac
   */
  private detectCtrlOrMeta(): boolean {
    return (
      this.originalEvent.ctrlKey ||
      this.originalEvent.metaKey ||
      this.modifiers.includes("ctrl") ||
      this.modifiers.includes("meta")
    );
  }

  /**
   * Check if the target is an input element
   * Single-key shortcuts should be disabled when typing
   */
  private checkIfInputTarget(target: EventTarget | null): boolean {
    if (!(target instanceof HTMLElement)) return false;

    const tagName = target.tagName.toLowerCase();
    const isEditable =
      target.getAttribute("contenteditable") === "true" ||
      target.hasAttribute("contenteditable");

    return (
      tagName === "input" ||
      tagName === "textarea" ||
      tagName === "select" ||
      isEditable
    );
  }

  /**
   * Check if this event should be ignored for shortcuts
   * (e.g., when typing in an input field)
   */
  shouldIgnore(isSingleKeyShortcut: boolean): boolean {
    // Always allow modifier+key shortcuts
    if (!isSingleKeyShortcut) return false;

    // Single-key shortcuts should be ignored when typing
    return this.isInputTarget;
  }

  /**
   * Check if this is a navigation key (arrows, page up/down, etc.)
   */
  isNavigationKey(): boolean {
    const navigationKeys = [
      "ArrowUp",
      "ArrowDown",
      "ArrowLeft",
      "ArrowRight",
      "PageUp",
      "PageDown",
      "Home",
      "End",
    ];

    return navigationKeys.includes(this.key);
  }

  /**
   * Check if this is a special key (Enter, Escape, Tab, etc.)
   */
  isSpecialKey(): boolean {
    const specialKeys = [
      "Enter",
      "Escape",
      "Tab",
      "Space",
      "Backspace",
      "Delete",
    ];

    return specialKeys.includes(this.key);
  }

  /**
   * Get a string representation for debugging
   */
  toString(): string {
    const modifierStr =
      this.modifiers.length > 0 ? this.modifiers.join("+") + "+" : "";
    return `${modifierStr}${this.key}`;
  }
}
