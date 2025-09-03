/**
 * Quick Glass Scrollbar Application Utility
 *
 * Simple function to apply glass scrollbars to any existing scrollable element.
 * No complex setup required - just import and apply.
 */

/**
 * Apply glass scrollbar to any scrollable element
 * @param element - The scrollable element
 * @param variant - The scrollbar style variant
 */
export function applyQuickGlassScrollbar(
  element: HTMLElement | null,
  variant:
    | "primary"
    | "secondary"
    | "minimal"
    | "hover"
    | "gradient" = "primary"
): void {
  if (!element) return;

  // Remove any existing glass scrollbar classes
  element.classList.remove(
    "quick-glass-primary",
    "quick-glass-secondary",
    "quick-glass-minimal",
    "quick-glass-hover",
    "quick-glass-gradient"
  );

  // Add the new variant class
  element.classList.add(`quick-glass-${variant}`);

  // Ensure the element is scrollable
  if (!element.style.overflow && !element.style.overflowY) {
    element.style.overflowY = "auto";
  }

  console.log(`✨ Applied ${variant} glass scrollbar to element`);
}

/**
 * Initialize glass scrollbars for all elements with data-glass attribute
 */
export function initQuickGlassScrollbars(): void {
  // Apply to elements with data-glass attribute
  const elements = document.querySelectorAll("[data-glass]");

  elements.forEach((element) => {
    const variantAttr = element.getAttribute("data-glass");
    const variant =
      variantAttr === "primary" ||
      variantAttr === "secondary" ||
      variantAttr === "minimal" ||
      variantAttr === "hover" ||
      variantAttr === "gradient"
        ? variantAttr
        : "primary";
    applyQuickGlassScrollbar(element as HTMLElement, variant);
  });

  console.log(`🎨 Applied glass scrollbars to ${elements.length} elements`);
}

/**
 * Remove glass scrollbar from element
 */
export function removeQuickGlassScrollbar(element: HTMLElement | null): void {
  if (!element) return;

  element.classList.remove(
    "quick-glass-primary",
    "quick-glass-secondary",
    "quick-glass-minimal",
    "quick-glass-hover",
    "quick-glass-gradient"
  );
}

// Auto-initialize when DOM is ready
if (typeof window !== "undefined") {
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initQuickGlassScrollbars);
  } else {
    initQuickGlassScrollbars();
  }
}
