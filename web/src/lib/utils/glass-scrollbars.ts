/**
 * Glass Scrollbar Utilities
 *
 * Utility functions for applying and managing glassmorphism scrollbars
 * across the application. Provides programmatic control over scrollbar
 * styling and behavior.
 */

export type ScrollbarVariant =
  | "primary"
  | "secondary"
  | "minimal"
  | "hover"
  | "gradient";

export type ScrollDirection = "vertical" | "horizontal" | "both" | "auto";

export interface ScrollbarConfig {
  variant: ScrollbarVariant;
  direction?: ScrollDirection;
  smooth?: boolean;
  responsive?: boolean;
}

/**
 * Apply glassmorphism scrollbar to an element
 */
export function applyGlassScrollbar(
  element: HTMLElement,
  config: ScrollbarConfig
): void {
  if (!element) {
    console.warn("Glass scrollbar: Element is null or undefined");
    return;
  }

  // Remove any existing glass scrollbar classes
  removeGlassScrollbar(element);

  // Apply the new scrollbar variant
  const scrollbarClass = `glass-scrollbar-${config.variant}`;
  element.classList.add(scrollbarClass);

  // Apply scroll direction
  if (config.direction) {
    applyScrollDirection(element, config.direction);
  }

  // Apply smooth scrolling if requested
  if (config.smooth !== false) {
    element.style.scrollBehavior = "smooth";
  }

  // Apply responsive behavior if requested
  if (config.responsive !== false) {
    element.classList.add("glass-scrollbar-responsive");
  }

  console.log(`✨ Glass scrollbar '${config.variant}' applied to element`);
}

/**
 * Remove glassmorphism scrollbar from an element
 */
export function removeGlassScrollbar(element: HTMLElement): void {
  if (!element) return;

  // Remove all glass scrollbar classes
  const classesToRemove = [
    "glass-scrollbar-primary",
    "glass-scrollbar-secondary",
    "glass-scrollbar-minimal",
    "glass-scrollbar-hover",
    "glass-scrollbar-gradient",
    "glass-scrollbar-responsive",
  ];

  classesToRemove.forEach((className) => {
    element.classList.remove(className);
  });

  // Reset scroll behavior
  element.style.scrollBehavior = "";
}

/**
 * Apply scroll direction styling to an element
 */
export function applyScrollDirection(
  element: HTMLElement,
  direction: ScrollDirection
): void {
  if (!element) return;

  // Remove existing overflow classes
  const overflowClasses = [
    "overflow-y-scroll",
    "overflow-x-scroll",
    "overflow-scroll",
    "overflow-y-auto",
    "overflow-x-auto",
    "overflow-auto",
    "overflow-y-hidden",
    "overflow-x-hidden",
    "overflow-hidden",
  ];

  overflowClasses.forEach((className) => {
    element.classList.remove(className);
  });

  // Apply new direction
  switch (direction) {
    case "vertical":
      element.classList.add("overflow-y-auto", "overflow-x-hidden");
      break;
    case "horizontal":
      element.classList.add("overflow-x-auto", "overflow-y-hidden");
      break;
    case "both":
      element.classList.add("overflow-auto");
      break;
    case "auto":
      element.classList.add("overflow-auto");
      break;
  }
}

/**
 * Get recommended scrollbar variant based on context
 */
export function getRecommendedVariant(context: string): ScrollbarVariant {
  switch (context.toLowerCase()) {
    case "codex":
    case "main-content":
    case "primary":
      return "primary";

    case "sidebar":
    case "panel":
    case "secondary":
      return "secondary";

    case "modal":
    case "dropdown":
    case "tooltip":
      return "minimal";

    case "background":
    case "overlay":
      return "hover";

    case "feature":
    case "highlight":
    case "special":
      return "gradient";

    default:
      return "primary";
  }
}

/**
 * Create a scroll event listener with throttling
 */
export function createScrollListener(
  callback: (event: Event) => void,
  _throttleMs: number = 16
): (event: Event) => void {
  let ticking = false;

  return (event: Event) => {
    if (!ticking) {
      requestAnimationFrame(() => {
        callback(event);
        ticking = false;
      });
      ticking = true;
    }
  };
}

/**
 * Smooth scroll to element with glassmorphism styling
 */
export function smoothScrollToElement(
  container: HTMLElement,
  target: HTMLElement,
  options: {
    offset?: number;
    duration?: number;
    variant?: ScrollbarVariant;
  } = {}
): Promise<void> {
  return new Promise((resolve) => {
    const { offset = 0, duration = 500, variant = "primary" } = options;

    // Apply glass scrollbar if not already present
    if (!container.classList.contains(`glass-scrollbar-${variant}`)) {
      applyGlassScrollbar(container, { variant });
    }

    // Calculate target position
    const containerRect = container.getBoundingClientRect();
    const targetRect = target.getBoundingClientRect();
    const targetPosition =
      targetRect.top - containerRect.top + container.scrollTop - offset;

    // Perform smooth scroll
    container.scrollTo({
      top: targetPosition,
      behavior: "smooth",
    });

    // Resolve after animation completes
    setTimeout(resolve, duration);
  });
}

/**
 * Auto-apply glass scrollbars to elements with data attributes
 */
export function autoApplyGlassScrollbars(): void {
  const elements = document.querySelectorAll("[data-glass-scrollbar]");

  elements.forEach((element) => {
    if (element instanceof HTMLElement) {
      const variant = element.dataset.glassScrollbar as ScrollbarVariant;
      const direction = element.dataset.scrollDirection as ScrollDirection;
      const smooth = element.dataset.smoothScroll !== "false";
      const responsive = element.dataset.responsive !== "false";

      applyGlassScrollbar(element, {
        variant: variant || "primary",
        direction,
        smooth,
        responsive,
      });
    }
  });

  console.log(
    `🎨 Auto-applied glass scrollbars to ${elements.length} elements`
  );
}

/**
 * Initialize glass scrollbars system
 */
export function initializeGlassScrollbars(): void {
  // Auto-apply to existing elements
  autoApplyGlassScrollbars();

  // Set up mutation observer for dynamic elements
  if (typeof window !== "undefined" && "MutationObserver" in window) {
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node instanceof HTMLElement) {
            // Check if the added element has glass scrollbar data attribute
            if (node.hasAttribute("data-glass-scrollbar")) {
              const variant = node.dataset.glassScrollbar as ScrollbarVariant;
              applyGlassScrollbar(node, { variant: variant || "primary" });
            }

            // Check child elements
            const childElements = node.querySelectorAll(
              "[data-glass-scrollbar]"
            );
            childElements.forEach((child) => {
              if (child instanceof HTMLElement) {
                const variant = child.dataset
                  .glassScrollbar as ScrollbarVariant;
                applyGlassScrollbar(child, { variant: variant || "primary" });
              }
            });
          }
        });
      });
    });

    observer.observe(document.body, {
      childList: true,
      subtree: true,
    });

    console.log("🔄 Glass scrollbars mutation observer initialized");
  }

  console.log("✨ Glass scrollbars system initialized");
}

/**
 * Scroll position utilities
 */
export const scrollUtils = {
  /**
   * Check if element is scrolled to top
   */
  isAtTop(element: HTMLElement): boolean {
    return element.scrollTop === 0;
  },

  /**
   * Check if element is scrolled to bottom
   */
  isAtBottom(element: HTMLElement): boolean {
    return element.scrollTop + element.clientHeight >= element.scrollHeight - 1;
  },

  /**
   * Get scroll percentage (0-100)
   */
  getScrollPercentage(element: HTMLElement): number {
    const scrollTop = element.scrollTop;
    const scrollHeight = element.scrollHeight - element.clientHeight;
    return scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
  },

  /**
   * Scroll to percentage
   */
  scrollToPercentage(element: HTMLElement, percentage: number): void {
    const scrollHeight = element.scrollHeight - element.clientHeight;
    const targetScroll = (percentage / 100) * scrollHeight;
    element.scrollTo({ top: targetScroll, behavior: "smooth" });
  },
};

/**
 * Export all utilities as default object
 */
export default {
  applyGlassScrollbar,
  removeGlassScrollbar,
  applyScrollDirection,
  getRecommendedVariant,
  createScrollListener,
  smoothScrollToElement,
  autoApplyGlassScrollbars,
  initializeGlassScrollbars,
  scrollUtils,
};
