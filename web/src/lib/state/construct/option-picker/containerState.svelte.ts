/**
 * Container State - Pure Svelte 5 Runes
 *
 * Handles container dimensions and aspect ratio calculations
 */

import { BREAKPOINTS, type ContainerAspect } from "./config";
import { getContainerAspect } from "./utils/layoutUtils";

export interface ContainerState {
  containerWidth: number;
  containerHeight: number;
  containerAspect: ContainerAspect;
}

export function createContainerState() {
  // Container dimensions state using runes
  let containerWidth = $state(
    typeof window !== "undefined"
      ? Math.max(300, window.innerWidth * 0.8)
      : BREAKPOINTS.desktop
  );
  let containerHeight = $state(
    typeof window !== "undefined"
      ? Math.max(200, window.innerHeight * 0.6)
      : 768
  );

  // Derived container aspect using runes
  const containerAspect = $derived(() =>
    getContainerAspect(containerWidth, containerHeight)
  );

  // Debounced resize handler
  const debouncedUpdateDimensions = (() => {
    let timeoutId: ReturnType<typeof setTimeout> | null = null;

    return (newContainerWidth: number, newContainerHeight: number) => {
      if (timeoutId !== null) {
        clearTimeout(timeoutId);
      }

      timeoutId = setTimeout(() => {
        // Ensure we never set invalid dimensions (0 or negative values)
        if (newContainerWidth > 0 && newContainerHeight > 0) {
          containerWidth = newContainerWidth;
          containerHeight = newContainerHeight;
        } else {
          // Use fallback values based on window size
          if (newContainerWidth <= 0) {
            const fallbackWidth =
              typeof window !== "undefined"
                ? Math.max(300, window.innerWidth * 0.8)
                : BREAKPOINTS.desktop;
            containerWidth = fallbackWidth;
          }

          if (newContainerHeight <= 0) {
            const fallbackHeight =
              typeof window !== "undefined"
                ? Math.max(200, window.innerHeight * 0.6)
                : 768;
            containerHeight = fallbackHeight;
          }
        }
        timeoutId = null;
      }, 100);
    };
  })();

  function updateContainerDimensions(width: number, height: number) {
    debouncedUpdateDimensions(width, height);
  }

  return {
    // State accessors
    get containerWidth() {
      return containerWidth;
    },
    get containerHeight() {
      return containerHeight;
    },
    get containerAspect() {
      return containerAspect();
    },

    // Actions
    updateContainerDimensions,

    // Derived state object
    get state(): ContainerState {
      return {
        containerWidth,
        containerHeight,
        containerAspect: containerAspect(),
      };
    },
  };
}
