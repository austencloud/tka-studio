import { writable } from 'svelte/store';

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
  tableOfContents: Array<{id: string, label: string}>;
  relatedResources: Array<{name: string, url: string, description: string, type: 'internal' | 'external'}>;
  heroGradient?: string;
  creatorColor?: string;
}

// Modal state store
export const modalState = writable<ModalState>({
  isOpen: false,
  resourceName: null,
  isLoading: false
});

// Current modal data store
export const modalData = writable<ResourceModalData | null>(null);

// Modal actions
export const modalActions = {
  openModal: (resourceName: string) => {
    modalState.update(state => ({
      ...state,
      isOpen: true,
      resourceName,
      isLoading: true
    }));

    // Update URL hash for browser back button support
    if (typeof window !== 'undefined') {
      window.location.hash = `#modal-${resourceName}`;
    }
  },

  closeModal: () => {
    modalState.update(state => ({
      ...state,
      isOpen: false,
      resourceName: null,
      isLoading: false
    }));

    modalData.set(null);

    // Clear URL hash
    if (typeof window !== 'undefined') {
      window.location.hash = '';
    }
  },

  setModalData: (data: ResourceModalData) => {
    modalData.set(data);
    modalState.update(state => ({
      ...state,
      isLoading: false
    }));
  },

  setLoading: (loading: boolean) => {
    modalState.update(state => ({
      ...state,
      isLoading: loading
    }));
  }
};

// Utility function to check if a specific modal is open
export const isModalOpen = (resourceName: string) => {
  let currentState: ModalState;
  modalState.subscribe(state => currentState = state)();
  return currentState.isOpen && currentState.resourceName === resourceName;
};

// Handle browser back button
if (typeof window !== 'undefined') {
  window.addEventListener('hashchange', () => {
    if (!window.location.hash) {
      modalActions.closeModal();
    }
  });

  // Handle initial page load with hash
  window.addEventListener('DOMContentLoaded', () => {
    const hash = window.location.hash;
    if (hash.startsWith('#modal-')) {
      const resourceName = hash.replace('#modal-', '');
      modalActions.openModal(resourceName);
    }
  });
}
