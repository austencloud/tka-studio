/**
 * User Store Adapter
 *
 * This module provides an adapter between the modern user container
 * and the legacy store-based API. This allows for a gradual migration
 * to the new container-based approach.
 */

import { derived, type Readable } from 'svelte/store';
import { userContainer, type UserState } from './UserContainer';

// Create a derived store for the current user
export const currentUserStore: Readable<string> = derived(
  userContainer,
  ($userContainer) => $userContainer.currentUser
);

// Create a derived store for the setup completion status
export const hasCompletedSetupStore: Readable<boolean> = derived(
  userContainer,
  ($userContainer) => $userContainer.hasCompletedSetup
);

// Export the userStore with a compatible API
export const userStore = {
  // Provide a getSnapshot method for compatibility with existing code
  getSnapshot: () => userContainer.state,

  // Provide methods that match the container's API
  setUsername: userContainer.setUsername,
  completeSetup: userContainer.completeSetup,
  resetUser: userContainer.resetUser,
  isFirstVisit: userContainer.isFirstVisit,

  // Subscribe method for Svelte store compatibility
  subscribe: userContainer.subscribe
};

// Export the container for modern usage
export { userContainer };

// Default export for backward compatibility
export default userStore;
