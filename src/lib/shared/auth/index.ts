/**
 * Authentication Module
 *
 * Central export point for all authentication-related functionality
 */

export { auth, app } from "./firebase";
export {
  authStore,
  user,
  isAuthenticated,
  isLoading,
  isInitialized,
} from "./stores/authStore";
