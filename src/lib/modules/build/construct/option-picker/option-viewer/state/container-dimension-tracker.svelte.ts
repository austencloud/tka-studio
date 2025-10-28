/**
 * ContainerDimensionTracker - Reusable container dimension tracking state
 *
 * Provides reactive container dimension tracking with ResizeObserver.
 * Extracted from OptionViewer for reusability across components.
 */

export interface ContainerDimensionState {
  // State getters
  readonly width: number;
  readonly height: number;
  readonly isReady: boolean;

  // Actions
  attachToElement(element: HTMLElement): () => void;
  forceUpdate(): void;
}

/**
 * Creates container dimension tracking state
 */
export function createContainerDimensionTracker(): ContainerDimensionState {
  // Reactive state - use conservative mobile-friendly defaults
  let width = $state(320); // Conservative mobile width default
  let height = $state(400); // Conservative mobile height default
  let isReady = $state(false);

  let resizeObserver: ResizeObserver | null = null;
  let currentElement: HTMLElement | null = null;
  let resizeTimeout: number | null = null;

  function attachToElement(element: HTMLElement): () => void {
    // Clean up existing observer
    if (resizeObserver) {
      resizeObserver.disconnect();
    }

    currentElement = element;

    // Create new observer with debouncing
    let lastProcessedWidth = width;
    let lastProcessedHeight = height;

    resizeObserver = new ResizeObserver((entries) => {
      // Clear any existing timeout
      if (resizeTimeout !== null) {
        clearTimeout(resizeTimeout);
      }

      // Debounce resize events to prevent layout thrashing during device rotation
      resizeTimeout = window.setTimeout(() => {
        for (const entry of entries) {
          const newWidth = entry.contentRect.width;
          const newHeight = entry.contentRect.height;

          // Enhanced sanity checks
          const isValidDimension = newWidth > 0 && newHeight > 0 && newWidth < 10000 && newHeight < 10000;
          const isDramaticChange = Math.abs(newWidth - width) > (width * 2) || Math.abs(newHeight - height) > (height * 2);

          if (isValidDimension && !isDramaticChange) {
            width = newWidth;
            height = newHeight;
            lastProcessedWidth = newWidth;
            lastProcessedHeight = newHeight;

            // Mark as ready after first measurement
            if (!isReady && width > 0 && height > 0) {
              isReady = true;
            }
          } else if (isDramaticChange) {
            console.warn(`📐 ContainerDimensionTracker: Ignoring dramatic dimension change ${width}x${height} → ${newWidth}x${newHeight} (likely browser artifact)`);
          } else {
            console.warn(`📐 ContainerDimensionTracker: Ignoring invalid dimensions ${newWidth}x${newHeight}`);
          }
        }
        resizeTimeout = null;

        // After debounce settles, check if dimensions have stabilized
        // This ensures reactive updates trigger even if no more resize events come in
        setTimeout(() => {
          if (currentElement) {
            const rect = currentElement.getBoundingClientRect();
            const finalWidth = rect.width;
            const finalHeight = rect.height;

            // If dimensions changed since last update, trigger one more update
            if (Math.abs(finalWidth - lastProcessedWidth) > 1 || Math.abs(finalHeight - lastProcessedHeight) > 1) {
              width = finalWidth;
              height = finalHeight;
            }
          }
        }, 50); // Check again after 50ms to catch final stabilization
      }, 16); // ~1 frame delay (60fps) for snappier resize while still preventing layout thrashing
    });

    // Start observing
    resizeObserver.observe(element);

    // Delay initial measurement to ensure layout is fully calculated
    // This prevents issues where getBoundingClientRect() returns incorrect values during page load
    requestAnimationFrame(() => {
      setTimeout(() => {
        const rect = element.getBoundingClientRect();
        const initialWidth = rect.width;
        const initialHeight = rect.height;

        // Sanity check: ignore unrealistic dimensions
        if (initialWidth > 0 && initialHeight > 0 && initialWidth < 10000 && initialHeight < 10000) {
          width = initialWidth;
          height = initialHeight;
          isReady = true;
        } else {
          console.warn(`📐 ContainerDimensionTracker: Initial measurement ignoring invalid dimensions ${initialWidth}x${initialHeight}`);
        }
      }, 100); // Small delay to ensure layout is stable
    });

    // Return cleanup function
    return () => {
      if (resizeObserver) {
        resizeObserver.disconnect();
        resizeObserver = null;
      }
      if (resizeTimeout !== null) {
        clearTimeout(resizeTimeout);
        resizeTimeout = null;
      }
      currentElement = null;
      isReady = false;
    };
  }

  function forceUpdate(): void {
    if (currentElement) {
      const rect = currentElement.getBoundingClientRect();
      const newWidth = rect.width;
      const newHeight = rect.height;

      // Enhanced sanity checks
      const isValidDimension = newWidth > 0 && newHeight > 0 && newWidth < 10000 && newHeight < 10000;
      const isDramaticChange = Math.abs(newWidth - width) > (width * 2) || Math.abs(newHeight - height) > (height * 2);

      if (isValidDimension && !isDramaticChange) {
        width = newWidth;
        height = newHeight;
        isReady = true;
      } else if (isDramaticChange) {
        console.warn(`📐 ContainerDimensionTracker: Force update ignoring dramatic dimension change ${width}x${height} → ${newWidth}x${newHeight} (likely browser artifact)`);
      } else {
        console.warn(`📐 ContainerDimensionTracker: Force update ignoring invalid dimensions ${newWidth}x${newHeight}`);
      }
    }
  }

  return {
    get width() { return width; },
    get height() { return height; },
    get isReady() { return isReady; },
    attachToElement,
    forceUpdate
  };
}
