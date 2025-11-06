/**
 * CreationMethodPersistenceService.ts
 *
 * Service implementation for persisting user's creation method selection state.
 * Uses sessionStorage to track whether user has selected a creation method in current session.
 *
 * Domain: Create module - Session State Management
 */

import { injectable } from "inversify";
import type { ICreationMethodPersistenceService } from "../contracts/ICreationMethodPersistenceService";

@injectable()
export class CreationMethodPersistenceService
  implements ICreationMethodPersistenceService
{
  private readonly STORAGE_KEY = "tka-create-method-selected";

  /**
   * Get sessionStorage if available, handling SSR and browser compatibility
   */
  private getSessionStorage(): Storage | null {
    if (typeof window === "undefined") {
      return null;
    }

    try {
      return window.sessionStorage;
    } catch {
      // SessionStorage may be unavailable in some contexts (private browsing, etc.)
      return null;
    }
  }

  /**
   * Check if user has selected a creation method in current session
   */
  hasUserSelectedMethod(): boolean {
    const storage = this.getSessionStorage();
    if (!storage) {
      return false;
    }

    return storage.getItem(this.STORAGE_KEY) === "true";
  }

  /**
   * Mark that user has selected a creation method
   */
  markMethodSelected(): void {
    const storage = this.getSessionStorage();
    if (!storage) {
      return;
    }

    storage.setItem(this.STORAGE_KEY, "true");
  }

  /**
   * Clear the creation method selection state
   */
  resetSelection(): void {
    const storage = this.getSessionStorage();
    if (!storage) {
      return;
    }

    storage.removeItem(this.STORAGE_KEY);
  }
}
