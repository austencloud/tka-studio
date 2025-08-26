// Resource Modal Helper Functions
// Browser interaction helpers for resource modals

import { browser } from "$app/environment";

// ============================================================================
// MODAL ACTIONS (Pure functions)
// ============================================================================

export function openModal(resourceName: string) {
  if (browser) {
    // Prevent body scroll when modal is open
    document.body.style.overflow = "hidden";

    // Add to browser history for back button support
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set("modal", resourceName);
    window.history.pushState(
      { modal: resourceName },
      "",
      currentUrl.toString()
    );
  }
}

export function closeModal() {
  if (browser) {
    // Restore body scroll
    document.body.style.overflow = "";

    // Handle browser history
    const currentUrl = new URL(window.location.href);
    if (currentUrl.searchParams.has("modal")) {
      currentUrl.searchParams.delete("modal");
      window.history.replaceState({}, "", currentUrl.toString());
    }
  }
}

// ============================================================================
// BROWSER EVENT HANDLERS
// ============================================================================

export function initializeModalEventHandlers(
  isOpen: () => boolean,
  onClose: () => void
) {
  if (browser) {
    // Handle browser back button
    window.addEventListener("popstate", (event) => {
      if (isOpen() && !event.state?.modal) {
        onClose();
      }
    });

    // Handle escape key
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && isOpen()) {
        onClose();
      }
    });
  }
}
