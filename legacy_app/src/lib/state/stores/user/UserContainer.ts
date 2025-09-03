/**
 * User Container
 *
 * This module provides a container for managing user information
 * using the modern container-based approach with Svelte 5 runes.
 */

import { createContainer } from '$lib/state/core/container';
import { browser } from '$app/environment';

// Storage keys
const USER_STORAGE_KEY = 'user_data';
const FIRST_VISIT_KEY = 'first_visit_completed';

// Define the user state interface
export interface UserState {
  currentUser: string;
  hasCompletedSetup: boolean;
  lastUpdated: number;
}

// Initial state
const initialState: UserState = {
  currentUser: 'User', // Default username
  hasCompletedSetup: false,
  lastUpdated: Date.now()
};

/**
 * Create the user container
 */
function createUserContainer() {
  // Try to load saved state from localStorage
  let savedState = { ...initialState };

  if (browser) {
    try {
      const userData = localStorage.getItem(USER_STORAGE_KEY);
      if (userData) {
        const parsed = JSON.parse(userData);
        savedState = {
          ...initialState,
          ...parsed,
          lastUpdated: Date.now()
        };
      }

      // Check if first visit setup has been completed
      const setupCompleted = localStorage.getItem(FIRST_VISIT_KEY);
      if (setupCompleted === 'true') {
        savedState.hasCompletedSetup = true;
      }
    } catch (error) {
      console.error('Failed to load user data from localStorage:', error);
    }
  }

  // Create the container with the loaded or initial state
  return createContainer(savedState, (state, update) => ({
    /**
     * Set the current username
     */
    setUsername: (username: string) => {
      if (!username || typeof username !== 'string') {
        console.warn('Invalid username provided, using default');
        username = 'User';
      }

      // Trim and limit length
      username = username.trim().substring(0, 50);

      // Use default if empty after trimming
      if (username === '') {
        username = 'User';
      }

      update((state) => {
        state.currentUser = username;
        state.lastUpdated = Date.now();
      });

      // Save to localStorage
      if (browser) {
        try {
          localStorage.setItem(USER_STORAGE_KEY, JSON.stringify({
            currentUser: username,
            hasCompletedSetup: state.hasCompletedSetup
          }));
        } catch (error) {
          console.error('Failed to save username to localStorage:', error);
        }
      }
    },

    /**
     * Mark the first-time setup as completed
     */
    completeSetup: (username?: string) => {
      // If username is provided, set it
      if (username) {
        userContainer.setUsername(username);
      }

      update((state) => {
        state.hasCompletedSetup = true;
        state.lastUpdated = Date.now();
      });

      // Save to localStorage
      if (browser) {
        try {
          localStorage.setItem(FIRST_VISIT_KEY, 'true');
          localStorage.setItem(USER_STORAGE_KEY, JSON.stringify({
            currentUser: state.currentUser,
            hasCompletedSetup: true
          }));
        } catch (error) {
          console.error('Failed to save setup completion to localStorage:', error);
        }
      }
    },

    /**
     * Reset the user data to defaults
     */
    resetUser: () => {
      update((state) => {
        state.currentUser = initialState.currentUser;
        state.lastUpdated = Date.now();
      });

      // Save to localStorage
      if (browser) {
        try {
          localStorage.setItem(USER_STORAGE_KEY, JSON.stringify({
            currentUser: initialState.currentUser,
            hasCompletedSetup: state.hasCompletedSetup
          }));
        } catch (error) {
          console.error('Failed to reset user data in localStorage:', error);
        }
      }
    },

    /**
     * Check if this is the first visit
     */
    isFirstVisit: (): boolean => {
      return !state.hasCompletedSetup;
    }
  }));
}

// Create and export the user container
export const userContainer = createUserContainer();

// For backward compatibility with existing code
export default userContainer;
