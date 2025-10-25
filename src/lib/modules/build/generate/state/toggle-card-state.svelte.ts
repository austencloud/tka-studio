/**
 * Toggle Card State - Svelte 5 runes
 *
 * Reactive state management for toggle card behavior.
 * Handles service resolution, event handling, and responsive state.
 * Follows TKA architecture: services handle business logic, runes handle reactivity.
 */

import type { IDeviceDetector, IHapticFeedbackService, IRippleEffectService } from "$shared";
import { resolve, TYPES } from "$shared";

/**
 * Creates reactive state for toggle card behavior
 */
export function createToggleCardState(props: {
  option1: { value: any };
  option2: { value: any };
  getActiveOption: () => any; // Changed to getter for reactivity
  onToggle: (value: any) => void;
}) {
  // Services
  let hapticService = $state<IHapticFeedbackService | null>(null);
  let rippleService = $state<IRippleEffectService | null>(null);
  let deviceDetector = $state<IDeviceDetector | null>(null);

  // Reactive state
  let isLandscapeMobile = $state(false);
  let cardElement = $state<HTMLButtonElement | null>(null);

  /**
   * Initialize services and setup listeners
   * Returns cleanup function
   */
  async function initialize(): Promise<() => void> {
    try {
      // Resolve services from DI container
      hapticService = await resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
      rippleService = await resolve<IRippleEffectService>(TYPES.IRippleEffectService);
      deviceDetector = await resolve<IDeviceDetector>(TYPES.IDeviceDetector);

      // Set initial layout state
      isLandscapeMobile = deviceDetector.isLandscapeMobile();

      // Subscribe to device capability changes
      const cleanupDeviceListener = deviceDetector.onCapabilitiesChanged(() => {
        if (deviceDetector) {
          isLandscapeMobile = deviceDetector.isLandscapeMobile();
        }
      });

      // Attach ripple effect to card
      const cleanupRipple = cardElement && rippleService
        ? rippleService.attachRipple(cardElement, {
            color: 'rgba(255, 255, 255, 0.4)',
            duration: 600,
            opacity: 0.5
          })
        : () => {};

      // Return consolidated cleanup function
      return () => {
        cleanupDeviceListener();
        cleanupRipple();
      };
    } catch (error) {
      console.warn("ToggleCardState: Failed to initialize services:", error);
      // Return empty cleanup function on error
      return () => {};
    }
  }

  /**
   * Handle toggle to a specific value
   */
  function handleToggle(value: any) {
    const activeOption = props.getActiveOption();
    if (value !== activeOption) {
      hapticService?.trigger("selection");
      props.onToggle(value);
    }
  }

  /**
   * Handle card click - toggles to inactive option
   */
  function handleCardClick() {
    hapticService?.trigger("selection");
    const activeOption = props.getActiveOption(); // Get current value reactively
    const newValue = activeOption === props.option1.value
      ? props.option2.value
      : props.option1.value;
    props.onToggle(newValue);
  }

  /**
   * Handle keyboard navigation
   */
  function handleKeydown(event: KeyboardEvent, value?: any) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      if (value !== undefined) {
        handleToggle(value);
      } else {
        handleCardClick();
      }
    }
  }

  return {
    // State getters/setters
    get cardElement() {
      return cardElement;
    },
    set cardElement(value: HTMLButtonElement | null) {
      cardElement = value;
    },
    get isLandscapeMobile() {
      return isLandscapeMobile;
    },

    // Event handlers
    handleToggle,
    handleCardClick,
    handleKeydown,

    // Initialization
    initialize,
  };
}

