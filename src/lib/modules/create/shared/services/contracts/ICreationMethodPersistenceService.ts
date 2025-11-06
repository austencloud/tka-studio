/**
 * ICreationMethodPersistenceService.ts
 *
 * Service interface for persisting user's creation method selection state.
 * Uses sessionStorage to track whether user has selected a creation method in current session.
 *
 * Domain: Create module - Session State Management
 */

export interface ICreationMethodPersistenceService {
  /**
   * Check if user has selected a creation method in current session
   * @returns true if user has previously selected a method, false otherwise
   */
  hasUserSelectedMethod(): boolean;

  /**
   * Mark that user has selected a creation method
   * Persists this state to sessionStorage
   */
  markMethodSelected(): void;

  /**
   * Clear the creation method selection state
   * Used when sequence is cleared and user needs to select method again
   */
  resetSelection(): void;
}
