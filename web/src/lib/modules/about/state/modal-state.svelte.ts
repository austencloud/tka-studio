// Modal State using Svelte 5 Runes
// Proper runes-based state management for modal functionality

import { type ResourceModalData } from "../components";
import {
  closeModal,
  initializeModalEventHandlers,
  openModal,
} from "../services";

// ============================================================================
// MODAL STATE FACTORY
// ============================================================================

export function createModalState() {
  // Reactive state using Svelte 5 runes
  let isOpen = $state(false);
  let resourceName = $state<string | null>(null);
  let modalData = $state<ResourceModalData | null>(null);

  // Actions that update state
  function openModalWithResource(name: string) {
    resourceName = name;
    isOpen = true;
    openModal(name); // Handle browser-specific logic
  }

  function closeModalAndCleanup() {
    isOpen = false;
    resourceName = null;
    modalData = null;
    closeModal(); // Handle browser-specific logic
  }

  function setModalData(data: ResourceModalData) {
    modalData = data;
  }

  // Initialize event handlers
  function initialize() {
    initializeModalEventHandlers(() => isOpen, closeModalAndCleanup);
  }

  return {
    // Reactive getters
    get isOpen() {
      return isOpen;
    },
    get resourceName() {
      return resourceName;
    },
    get modalData() {
      return modalData;
    },

    // Actions
    openModal: openModalWithResource,
    closeModal: closeModalAndCleanup,
    setModalData,
    initialize,
  };
}
