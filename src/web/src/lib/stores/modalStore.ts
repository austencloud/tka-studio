// Modal Store using Svelte 5 Runes
// Replaces the old Svelte 4 store pattern with modern runes-based state management

import { browser } from "$app/environment";

export interface ResourceModalData {
  title: string;
  subtitle: string;
  creator: string;
  category: string;
  level: string;
  description: string;
  keywords: string;
  url: string;
  resourceName: string;
  tableOfContents: Array<{ id: string; label: string }>;
  relatedResources: Array<{
    name: string;
    url: string;
    description: string;
    type: "internal" | "external";
  }>;
  heroGradient: string;
  creatorColor: string;
}

class ModalManager {
  isOpen = $state(false);
  resourceName = $state<string | null>(null);
  modalData = $state<ResourceModalData | null>(null);

  openModal(resourceName: string) {
    this.resourceName = resourceName;
    this.isOpen = true;

    if (browser) {
      // Prevent body scroll when modal is open
      document.body.style.overflow = "hidden";

      // Add to browser history for back button support
      const currentUrl = new URL(window.location.href);
      currentUrl.searchParams.set("modal", resourceName);
      window.history.pushState(
        { modal: resourceName },
        "",
        currentUrl.toString(),
      );
    }
  }

  closeModal() {
    this.isOpen = false;
    this.resourceName = null;
    this.modalData = null;

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

  setModalData(data: ResourceModalData) {
    this.modalData = data;
  }

  // Initialize browser event listeners
  initialize() {
    if (browser) {
      // Handle browser back button
      window.addEventListener("popstate", (event) => {
        if (this.isOpen && !event.state?.modal) {
          this.closeModal();
        }
      });

      // Handle escape key
      document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && this.isOpen) {
          this.closeModal();
        }
      });
    }
  }
}

// Create and export the modal manager instance
export const modalManager = new ModalManager();

// Initialize browser features
if (browser) {
  modalManager.initialize();
}
