// src/lib/components/ConstructTab/OptionPicker/components/OptionPickerHeader/useResponsiveLayout.svelte.ts
import type { LayoutContext } from '../../layoutContext';

/**
 * Hook to manage responsive layout state
 * @param layoutContext The layout context from the parent component
 * @returns An object containing responsive layout state and functions
 */
export function useResponsiveLayout(layoutContext: LayoutContext | null) {
  // Local state
  let isMobileDevice = $state(false);
  let useShortLabels = $state(false);
  let tabsContainerRef = $state<HTMLDivElement | null>(null);
  let isScrollable = $state(false);
  let compactMode = $state(false);
  let showScrollIndicator = $state(false);

  // Update mobile device state from context and set compact mode
  $effect(() => {
    // Get the layout context value safely
    const contextValue = layoutContext;

    // Check if the context exists and has the isMobile property
    if (contextValue && typeof contextValue === 'object' && 'isMobile' in contextValue) {
      // Use type assertion to ensure TypeScript knows this is a boolean
      isMobileDevice = Boolean(contextValue.isMobile);

      // Proactively set compact mode on mobile devices
      if (isMobileDevice) {
        compactMode = true;
      }
    } else {
      // Fallback to window width if context is not available
      isMobileDevice = window.innerWidth <= 640;
      if (isMobileDevice) {
        compactMode = true;
      }
    }

    // Add resize listener to update mobile state when window size changes
    const handleResize = () => {
      // Check if window width is mobile size
      const isMobile = window.innerWidth <= 640;
      if (isMobile) {
        isMobileDevice = true;
        compactMode = true;
      } else if (contextValue && typeof contextValue === 'object' && 'isMobile' in contextValue) {
        isMobileDevice = Boolean(contextValue.isMobile);
      } else {
        isMobileDevice = false;
      }

      // Force a re-check of tab overflow
      if (tabsContainerRef) {
        checkTabsOverflow();
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  });

  // Determine when to use short labels - always use short labels on mobile
  $effect(() => {
    useShortLabels = isMobileDevice || compactMode;
  });

  // Check if tabs are scrollable
  $effect(() => {
    if (tabsContainerRef) {
      checkTabsOverflow();
    }
  });

  // Function to check if tabs are overflowing
  function checkTabsOverflow() {
    if (!tabsContainerRef) return;

    const { scrollWidth, clientWidth } = tabsContainerRef;

    // Check if content is wider than container
    isScrollable = scrollWidth > clientWidth;

    // Check if we're close to overflowing (within 20px)
    const isNearlyOverflowing = scrollWidth > clientWidth - 20;

    // Switch to compact mode if we're overflowing or nearly overflowing
    if ((isScrollable || isNearlyOverflowing) && !compactMode) {
      compactMode = true;

      // Force a re-check after a short delay to see if compact mode fixed the overflow
      setTimeout(() => {
        if (tabsContainerRef) {
          const { scrollWidth, clientWidth } = tabsContainerRef;
          isScrollable = scrollWidth > clientWidth;
          showScrollIndicator = isScrollable;
        }
      }, 50);
    }

    // Show scroll indicator when scrollable
    showScrollIndicator = isScrollable;
  }

  // Handle scroll events to update scroll indicator
  function handleScroll() {
    if (!tabsContainerRef) return;

    const { scrollLeft, scrollWidth, clientWidth } = tabsContainerRef;

    // Show indicator when not at the end of scroll
    showScrollIndicator = scrollLeft + clientWidth < scrollWidth - 10;
  }

  // Add resize observer to check for overflow
  $effect(() => {
    if (!tabsContainerRef) return;

    const resizeObserver = new ResizeObserver(() => {
      checkTabsOverflow();
    });

    resizeObserver.observe(tabsContainerRef);

    return () => {
      resizeObserver.disconnect();
    };
  });

  return {
    isMobileDevice,
    useShortLabels,
    tabsContainerRef,
    isScrollable,
    compactMode,
    showScrollIndicator,
    handleScroll,
    checkTabsOverflow
  };
}
