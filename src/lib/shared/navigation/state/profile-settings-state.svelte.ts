/**
 * Profile Settings State Management
 *
 * Centralized state for the profile settings feature.
 * Handles form state, UI state, and viewport adaptivity.
 */

import { authStore } from "$shared/auth";

// ============================================================================
// FORM STATE
// ============================================================================

export const personalInfoState = $state({
  displayName: "",
  email: "",
});

// Track original values to detect changes
export const originalPersonalInfoState = $state({
  displayName: "",
  email: "",
});

export const passwordState = $state({
  current: "",
  new: "",
  confirm: "",
});

export const emailChangeState = $state({
  newEmail: "",
  password: "", // For re-authentication
});

// ============================================================================
// UI STATE
// ============================================================================

export const uiState = $state({
  activeTab: "personal" as "personal" | "security" | "subscription",
  previousTab: "personal" as "personal" | "security" | "subscription",
  transitionDirection: 0 as -1 | 0 | 1, // -1 = left, 0 = none, 1 = right
  saving: false,
  uploadingPhoto: false,
  showPasswordSection: false,
  showDeleteConfirmation: false,
  showEmailChangeSection: false,
  changingEmail: false,
});

// ============================================================================
// VIEWPORT ADAPTIVE STATE
// ============================================================================

export const viewportState = $state({
  contentContainer: null as HTMLDivElement | null,
  availableHeight: 0,
});

// Export functions that return derived values (Svelte 5 requirement)
export function isCompactMode() {
  return (
    viewportState.availableHeight > 0 && viewportState.availableHeight < 600
  );
}

export function isVeryCompactMode() {
  return (
    viewportState.availableHeight > 0 && viewportState.availableHeight < 500
  );
}

// ============================================================================
// DERIVED STATE
// ============================================================================

// Export function that returns derived value (Svelte 5 requirement)
export function hasPasswordProvider() {
  if (!authStore.user?.providerData) return false;
  return authStore.user.providerData.some(
    (provider) => provider.providerId === "password"
  );
}

// Check if user can change email (only password-only users)
export function canChangeEmail() {
  if (!authStore.user?.providerData) return false;
  // Only allow email change if user ONLY has password authentication
  // Users with OAuth providers should manage email through those providers
  return (
    authStore.user.providerData.length === 1 &&
    authStore.user.providerData[0].providerId === "password"
  );
}

// Check if there are unsaved changes to personal info
export function hasPersonalInfoChanges() {
  return (
    personalInfoState.displayName !== originalPersonalInfoState.displayName
  );
}

// ============================================================================
// STATE SYNCHRONIZATION
// ============================================================================

/**
 * Sync form state with auth store when user changes
 */
export function syncWithAuthStore() {
  if (authStore.user) {
    const displayName = authStore.user.displayName || "";
    const email = authStore.user.email || "";

    personalInfoState.displayName = displayName;
    personalInfoState.email = email;

    // Also update original values to track changes
    originalPersonalInfoState.displayName = displayName;
    originalPersonalInfoState.email = email;
  }
}

/**
 * Reset personal info form to original values
 */
export function resetPersonalInfoForm() {
  personalInfoState.displayName = originalPersonalInfoState.displayName;
  personalInfoState.email = originalPersonalInfoState.email;
}

/**
 * Reset password form state
 */
export function resetPasswordForm() {
  passwordState.current = "";
  passwordState.new = "";
  passwordState.confirm = "";
}

/**
 * Reset email change form state
 */
export function resetEmailChangeForm() {
  emailChangeState.newEmail = "";
  emailChangeState.password = "";
}

/**
 * Reset all UI state
 */
export function resetUIState() {
  uiState.saving = false;
  uiState.uploadingPhoto = false;
  uiState.showPasswordSection = false;
  uiState.showDeleteConfirmation = false;
  uiState.showEmailChangeSection = false;
  uiState.changingEmail = false;
}

/**
 * Setup viewport tracking with ResizeObserver
 * Returns a cleanup function that should be called when done
 */
export function setupViewportTracking(): (() => void) | null {
  if (!viewportState.contentContainer) return null;

  const resizeObserver = new ResizeObserver((entries) => {
    for (const entry of entries) {
      viewportState.availableHeight = entry.contentRect.height;
    }
  });

  resizeObserver.observe(viewportState.contentContainer);

  return () => {
    resizeObserver.disconnect();
  };
}

// ============================================================================
// TAB TRANSITION HELPERS
// ============================================================================

const TAB_ORDER: Array<"personal" | "security" | "subscription"> = [
  "personal",
  "security",
  "subscription",
];

/**
 * Calculate and update transition direction when tab changes
 */
export function updateTabTransition(
  newTab: "personal" | "security" | "subscription"
) {
  const oldIndex = TAB_ORDER.indexOf(uiState.activeTab);
  const newIndex = TAB_ORDER.indexOf(newTab);

  uiState.previousTab = uiState.activeTab;
  uiState.transitionDirection =
    newIndex > oldIndex ? 1 : newIndex < oldIndex ? -1 : 0;
  uiState.activeTab = newTab;
}
