/**
 * Keyboard Shortcut Composable
 *
 * Provides reactive keyboard event handling with automatic cleanup.
 * Useful for components that need to respond to keyboard shortcuts
 * like Escape, Enter, etc.
 */

export interface KeyboardShortcutConfig {
  /**
   * The key to listen for (e.g., "Escape", "Enter", "ArrowUp")
   */
  key: string;

  /**
   * Callback when key is pressed
   */
  onKeyPress: (event: KeyboardEvent) => void;

  /**
   * Whether the shortcut is currently active
   * @default true
   */
  enabled?: boolean;

  /**
   * Optional modifier keys that must be pressed
   */
  modifiers?: {
    ctrl?: boolean;
    shift?: boolean;
    alt?: boolean;
    meta?: boolean;
  };
}

/**
 * Creates a keyboard shortcut handler with automatic cleanup
 * Returns a cleanup function that should be called when the component unmounts
 */
export function useKeyboardShortcut(
  config: KeyboardShortcutConfig
): () => void {
  const handleKeydown = (event: KeyboardEvent) => {
    // Check if shortcut is enabled
    if (config.enabled === false) {
      return;
    }

    // Check if key matches
    if (event.key !== config.key) {
      return;
    }

    // Check modifiers if specified
    if (config.modifiers) {
      const { ctrl, shift, alt, meta } = config.modifiers;
      if (ctrl !== undefined && event.ctrlKey !== ctrl) return;
      if (shift !== undefined && event.shiftKey !== shift) return;
      if (alt !== undefined && event.altKey !== alt) return;
      if (meta !== undefined && event.metaKey !== meta) return;
    }

    // Call the handler
    config.onKeyPress(event);
  };

  // Add event listener
  document.addEventListener("keydown", handleKeydown);

  // Return cleanup function
  return () => {
    document.removeEventListener("keydown", handleKeydown);
  };
}

/**
 * Simplified version for Escape key handling (common use case)
 */
export function useEscapeKey(onEscape: () => void, enabled: boolean = true): () => void {
  return useKeyboardShortcut({
    key: "Escape",
    onKeyPress: onEscape,
    enabled,
  });
}
