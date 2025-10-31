/**
 * Authentication Store
 *
 * Manages authentication state across the application using Firebase Auth.
 * Provides reactive user data and auth status.
 */

import { writable, derived } from "svelte/store";
import {
  onAuthStateChanged,
  signOut as firebaseSignOut,
  type User,
} from "firebase/auth";
import { auth } from "../firebase";

interface AuthState {
  user: User | null;
  loading: boolean;
  initialized: boolean;
}

function createAuthStore() {
  const { subscribe, set, update } = writable<AuthState>({
    user: null,
    loading: true,
    initialized: false,
  });

  // Set up auth state listener
  let unsubscribeAuth: (() => void) | null = null;

  return {
    subscribe,

    /**
     * Initialize the auth listener
     * Call this once when your app starts
     */
    initialize: () => {
      if (unsubscribeAuth) {
        return; // Already initialized
      }

      unsubscribeAuth = onAuthStateChanged(
        auth,
        (user) => {
          set({
            user,
            loading: false,
            initialized: true,
          });
        },
        (error) => {
          console.error("Auth state change error:", error);
          set({
            user: null,
            loading: false,
            initialized: true,
          });
        }
      );
    },

    /**
     * Sign out the current user
     */
    signOut: async () => {
      try {
        await firebaseSignOut(auth);
        // State will be updated automatically by onAuthStateChanged
      } catch (error) {
        console.error("Sign out error:", error);
        throw error;
      }
    },

    /**
     * Clean up the auth listener
     * Call this when your app unmounts (if ever)
     */
    cleanup: () => {
      if (unsubscribeAuth) {
        unsubscribeAuth();
        unsubscribeAuth = null;
      }
    },
  };
}

export const authStore = createAuthStore();

/**
 * Derived stores for convenience
 */
export const user = derived(authStore, ($auth) => $auth.user);
export const isAuthenticated = derived(authStore, ($auth) => !!$auth.user);
export const isLoading = derived(authStore, ($auth) => $auth.loading);
export const isInitialized = derived(authStore, ($auth) => $auth.initialized);
