export interface ModalState {
  isOpen: boolean;
  resourceName: string | null;
  isLoading: boolean;
}

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
  heroGradient?: string;
  creatorColor?: string;
}

// Modal state using Svelte 5 runes
class ModalManager {
  private _state = $state<ModalState>({
    isOpen: false,
    resourceName: null,
    isLoading: false,
  });

  private _data = $state<ResourceModalData | null>(null);

  // Getters for reactive access
  get state() {
    return this._state;
  }

  get data() {
    return this._data;
  }

  get isOpen() {
    return this._state.isOpen;
  }

  get resourceName() {
    return this._state.resourceName;
  }

  get isLoading() {
    return this._state.isLoading;
  }

  // Actions
  openModal(resourceName: string) {
    this._state.isOpen = true;
    this._state.resourceName = resourceName;
    this._state.isLoading = true;

    // Update URL hash for browser back button support
    if (typeof window !== "undefined") {
      window.location.hash = `#modal-${resourceName}`;
    }
  }

  closeModal() {
    this._state.isOpen = false;
    this._state.resourceName = null;
    this._state.isLoading = false;
    this._data = null;

    // Clear URL hash
    if (typeof window !== "undefined") {
      window.location.hash = "";
    }
  }

  setModalData(data: ResourceModalData) {
    this._data = data;
    this._state.isLoading = false;
  }

  setLoading(loading: boolean) {
    this._state.isLoading = loading;
  }

  // Utility function to check if a specific modal is open
  isModalOpen(resourceName: string) {
    return this._state.isOpen && this._state.resourceName === resourceName;
  }
}

// Create singleton instance
export const modalManager = new ModalManager();

// Handle browser back button
if (typeof window !== "undefined") {
  window.addEventListener("hashchange", () => {
    if (!window.location.hash) {
      modalManager.closeModal();
    }
  });

  // Handle initial page load with hash
  window.addEventListener("DOMContentLoaded", () => {
    const hash = window.location.hash;
    if (hash.startsWith("#modal-")) {
      const resourceName = hash.replace("#modal-", "");
      modalManager.openModal(resourceName);
    }
  });
}
