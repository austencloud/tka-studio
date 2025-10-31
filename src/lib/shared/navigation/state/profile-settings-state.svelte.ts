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

export const passwordState = $state({
  current: "",
  new: "",
  confirm: "",
});

// ============================================================================
// UI STATE
// ============================================================================

export const uiState = $state({
  activeTab: "personal" as "personal" | "account",
  saving: false,
  uploadingPhoto: false,
  showPasswordSection: false,
  showDeleteConfirmation: false,
});

// ============================================================================
// VIEWPORT ADAPTIVE STATE
// ============================================================================

export const viewportState = $state({
  contentContainer: null as HTMLDivElement | null,
  availableHeight: 0,
});

export const isCompactMode = $derived(
  viewportState.availableHeight > 0 && viewportState.availableHeight < 600
);

export const isVeryCompactMode = $derived(
  viewportState.availableHeight > 0 && viewportState.availableHeight < 500
);

// ============================================================================
// DERIVED STATE
// ============================================================================

export const hasPasswordProvider = $derived.by(() => {
  if (!authStore.user?.providerData) return false;
  return authStore.user.providerData.some(
    (provider) => provider.providerId === "password"
  );
});

// ============================================================================
// STATE SYNCHRONIZATION
// ============================================================================

/**
 * Sync form state with auth store when user changes
 */
export function syncWithAuthStore() {
  if (authStore.user) {
    personalInfoState.displayName = authStore.user.displayName || "";
    personalInfoState.email = authStore.user.email || "";
  }
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
 * Reset all UI state
 */
export function resetUIState() {
  uiState.saving = false;
  uiState.uploadingPhoto = false;
  uiState.showPasswordSection = false;
  uiState.showDeleteConfirmation = false;
}

/**
 * Setup viewport tracking with ResizeObserver
 */
export function setupViewportTracking() {
  return $effect(() => {
    if (!viewportState.contentContainer) return;

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        viewportState.availableHeight = entry.contentRect.height;
      }
    });

    resizeObserver.observe(viewportState.contentContainer);

    return () => {
      resizeObserver.disconnect();
    };
  });
}
