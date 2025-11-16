/**
 * KeyboardShortcutService Implementation
 *
 * Main service for managing keyboard shortcuts globally.
 * Handles registration, event listening, and execution of shortcuts.
 *
 * Domain: Keyboard Shortcuts
 */

import { inject, injectable } from "inversify";
import type { IShortcutRegistryService } from "../contracts";
import type { IKeyboardShortcutService } from "../contracts";
import type {
  ShortcutContext,
  ShortcutRegistrationOptions,
} from "../../domain";
import { Shortcut } from "../../domain/models/Shortcut";
import { NormalizedKeyboardEvent } from "../../domain/models/KeyboardEvent";
import { TYPES } from "$shared/inversify";

@injectable()
export class KeyboardShortcutService implements IKeyboardShortcutService {
  private currentContext: ShortcutContext = "global";
  private isInitialized = false;
  private keydownHandler: ((event: KeyboardEvent) => void) | null = null;

  constructor(
    @inject(TYPES.IShortcutRegistryService)
    private registry: IShortcutRegistryService
  ) {}

  initialize(): void {
    if (this.isInitialized) return;

    this.keydownHandler = this.handleKeydown.bind(this);
    // Use capture phase to intercept events BEFORE browser defaults
    window.addEventListener("keydown", this.keydownHandler, true);
    this.isInitialized = true;
  }

  dispose(): void {
    if (this.keydownHandler) {
      window.removeEventListener("keydown", this.keydownHandler, true);
      this.keydownHandler = null;
    }
    this.registry.clear();
    this.isInitialized = false;

    console.log("⌨️ KeyboardShortcutService disposed");
  }

  register(options: ShortcutRegistrationOptions): () => void {
    // Validate options
    if (!options.id) {
      throw new Error("Shortcut ID is required");
    }

    if (!options.key) {
      throw new Error("Shortcut key is required");
    }

    if (!options.action) {
      throw new Error("Shortcut action is required");
    }

    // Check if already registered
    if (this.registry.has(options.id)) {
      console.warn(`Shortcut with ID "${options.id}" is already registered`);
      return () => this.unregister(options.id);
    }

    // Create shortcut with defaults
    const shortcutDefinition: any = {
      id: options.id,
      label: options.label,
      key: options.key,
      modifiers: options.modifiers ?? [],
      context: options.context ?? "global",
      scope: options.scope ?? "action",
      priority: options.priority ?? "medium",
      preventDefault: options.preventDefault ?? true,
      stopPropagation: options.stopPropagation ?? false,
      action: options.action,
      enabled: options.enabled ?? true,
      isSingleKey: (options.modifiers ?? []).length === 0,
    };

    // Only add description if it's defined
    if (options.description !== undefined) {
      shortcutDefinition.description = options.description;
    }

    // Only add condition if it's defined
    if (options.condition !== undefined) {
      shortcutDefinition.condition = options.condition;
    }

    const shortcut = new Shortcut(shortcutDefinition);

    // Add to registry
    this.registry.add(shortcut);

    // Return unregister function
    return () => this.unregister(options.id);
  }

  unregister(id: string): void {
    this.registry.remove(id);
  }

  enable(id: string): void {
    const shortcut = this.registry.get(id);
    if (shortcut) {
      shortcut.enabled = true;
    }
  }

  disable(id: string): void {
    const shortcut = this.registry.get(id);
    if (shortcut) {
      shortcut.enabled = false;
    }
  }

  setContext(context: ShortcutContext): void {
    this.currentContext = context;
  }

  getContext(): ShortcutContext {
    return this.currentContext;
  }

  isRegistered(id: string): boolean {
    return this.registry.has(id);
  }

  getAllShortcuts(): ShortcutRegistrationOptions[] {
    return this.registry.getAll().map((shortcut) => ({
      id: shortcut.id,
      label: shortcut.label,
      ...(shortcut.description !== undefined && {
        description: shortcut.description,
      }),
      key: shortcut.key,
      modifiers: shortcut.modifiers,
      context: shortcut.context,
      scope: shortcut.scope,
      priority: shortcut.priority,
      preventDefault: shortcut.preventDefault,
      stopPropagation: shortcut.stopPropagation,
      ...(shortcut.condition !== undefined && {
        condition: shortcut.condition,
      }),
      action: shortcut.action,
      enabled: shortcut.enabled,
    }));
  }

  getShortcutsForContext(
    context: ShortcutContext
  ): ShortcutRegistrationOptions[] {
    return this.registry.getByContext(context).map((shortcut) => ({
      id: shortcut.id,
      label: shortcut.label,
      ...(shortcut.description !== undefined && {
        description: shortcut.description,
      }),
      key: shortcut.key,
      modifiers: shortcut.modifiers,
      context: shortcut.context,
      scope: shortcut.scope,
      priority: shortcut.priority,
      preventDefault: shortcut.preventDefault,
      stopPropagation: shortcut.stopPropagation,
      ...(shortcut.condition !== undefined && {
        condition: shortcut.condition,
      }),
      action: shortcut.action,
      enabled: shortcut.enabled,
    }));
  }

  /**
   * Handle keydown events
   */
  private handleKeydown(event: KeyboardEvent): void {
    // Normalize the event
    const normalized = new NormalizedKeyboardEvent(event);

    // Debug Backspace specifically
    if (normalized.key === "Backspace") {
      console.log(`⌨️ Backspace pressed! Context: ${this.currentContext}`);
    }

    // Find matching shortcuts
    const matches = this.registry.findMatches(
      normalized.key,
      normalized.modifiers,
      normalized.ctrlOrMeta,
      this.currentContext
    );

    if (normalized.key === "Backspace") {
      console.log(
        `⌨️ Backspace matches found: ${matches.length}`,
        matches.map((m) => m.id)
      );
    }

    if (matches.length === 0) return;

    // Get the highest priority match
    const shortcut = matches[0];
    if (!shortcut) return;

    // Check if we should ignore (e.g., typing in input)
    if (normalized.shouldIgnore(shortcut.isSingleKey)) return;

    // Log for debugging
    console.log(`⌨️ Executing shortcut: ${shortcut.id}`, {
      key: normalized.key,
      modifiers: normalized.modifiers,
      context: this.currentContext,
    });

    // Execute the shortcut (this will call preventDefault if configured)
    shortcut.execute(event).catch((error) => {
      console.error(`Error executing shortcut "${shortcut.id}":`, error);
    });
  }
}
