/**
 * ShortcutRegistryService Implementation
 *
 * Registry for storing and managing keyboard shortcuts.
 *
 * Domain: Keyboard Shortcuts
 */

import { injectable } from "inversify";
import type { IShortcutRegistryService } from "../contracts";
import { Shortcut } from "../../domain/models/Shortcut";
import type { KeyModifier, ShortcutContext, ShortcutScope } from "../../domain";

@injectable()
export class ShortcutRegistryService implements IShortcutRegistryService {
  private shortcuts: Map<string, Shortcut> = new Map();

  add(shortcut: Shortcut): void {
    this.shortcuts.set(shortcut.id, shortcut);
  }

  remove(id: string): void {
    this.shortcuts.delete(id);
  }

  get(id: string): Shortcut | undefined {
    return this.shortcuts.get(id);
  }

  has(id: string): boolean {
    return this.shortcuts.has(id);
  }

  getAll(): Shortcut[] {
    return Array.from(this.shortcuts.values());
  }

  findMatches(
    key: string,
    modifiers: KeyModifier[],
    ctrlOrMeta: boolean,
    context: ShortcutContext
  ): Shortcut[] {
    const matches: Shortcut[] = [];

    for (const shortcut of this.shortcuts.values()) {
      // Check if shortcut is active in current context
      if (!shortcut.isActiveInContext(context)) continue;

      // Check if shortcut matches the key and modifiers
      if (!shortcut.matches(key, modifiers, ctrlOrMeta)) continue;

      // Check if condition is met
      if (!shortcut.isConditionMet()) continue;

      matches.push(shortcut);
    }

    // Sort by priority (highest first)
    return matches.sort(
      (a, b) => b.getPriorityValue() - a.getPriorityValue()
    );
  }

  getByContext(context: ShortcutContext): Shortcut[] {
    return this.getAll().filter((shortcut) =>
      shortcut.isActiveInContext(context)
    );
  }

  getByScope(scope: string): Shortcut[] {
    return this.getAll().filter((shortcut) => shortcut.scope === scope);
  }

  clear(): void {
    this.shortcuts.clear();
  }

  count(): number {
    return this.shortcuts.size;
  }
}
