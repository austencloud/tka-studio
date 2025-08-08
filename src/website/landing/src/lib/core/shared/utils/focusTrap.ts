/**
 * Focus trap utility for modal accessibility
 * Ensures keyboard navigation stays within the modal when open
 */

export interface FocusTrapOptions {
  initialFocus?: HTMLElement | string;
  returnFocus?: HTMLElement;
  escapeCallback?: () => void;
}

export class FocusTrap {
  private container: HTMLElement;
  private options: FocusTrapOptions;
  private previouslyFocusedElement: HTMLElement | null = null;
  private isActive = false;

  constructor(container: HTMLElement, options: FocusTrapOptions = {}) {
    this.container = container;
    this.options = options;
  }

  /**
   * Get all focusable elements within the container
   */
  private getFocusableElements(): HTMLElement[] {
    const focusableSelectors = [
      'button:not([disabled])',
      'input:not([disabled])',
      'select:not([disabled])',
      'textarea:not([disabled])',
      'a[href]',
      '[tabindex]:not([tabindex="-1"])',
      '[contenteditable="true"]'
    ].join(', ');

    return Array.from(this.container.querySelectorAll(focusableSelectors))
      .filter((element) => {
        const el = element as HTMLElement;
        return el.offsetWidth > 0 && el.offsetHeight > 0 && !el.hidden;
      }) as HTMLElement[];
  }

  /**
   * Handle keydown events for focus management
   */
  private handleKeyDown = (event: KeyboardEvent) => {
    if (!this.isActive) return;

    // Handle Escape key
    if (event.key === 'Escape') {
      event.preventDefault();
      if (this.options.escapeCallback) {
        this.options.escapeCallback();
      }
      return;
    }

    // Handle Tab key for focus cycling
    if (event.key === 'Tab') {
      const focusableElements = this.getFocusableElements();

      if (focusableElements.length === 0) {
        event.preventDefault();
        return;
      }

      const firstElement = focusableElements[0];
      const lastElement = focusableElements[focusableElements.length - 1];
      const currentElement = document.activeElement as HTMLElement;

      if (event.shiftKey) {
        // Shift + Tab (backward)
        if (currentElement === firstElement || !focusableElements.includes(currentElement)) {
          event.preventDefault();
          lastElement.focus();
        }
      } else {
        // Tab (forward)
        if (currentElement === lastElement || !focusableElements.includes(currentElement)) {
          event.preventDefault();
          firstElement.focus();
        }
      }
    }
  };

  /**
   * Activate the focus trap
   */
  activate(): void {
    if (this.isActive) return;

    // Store the currently focused element to restore later
    this.previouslyFocusedElement = document.activeElement as HTMLElement;

    // Add event listener for keyboard navigation
    document.addEventListener('keydown', this.handleKeyDown);

    // Set initial focus
    this.setInitialFocus();

    this.isActive = true;
  }

  /**
   * Deactivate the focus trap
   */
  deactivate(): void {
    if (!this.isActive) return;

    // Remove event listener
    document.removeEventListener('keydown', this.handleKeyDown);

    // Restore focus to the previously focused element
    if (this.options.returnFocus) {
      this.options.returnFocus.focus();
    } else if (this.previouslyFocusedElement) {
      this.previouslyFocusedElement.focus();
    }

    this.isActive = false;
  }

  /**
   * Set initial focus when the trap is activated
   */
  private setInitialFocus(): void {
    let elementToFocus: HTMLElement | null = null;

    // Use specified initial focus element
    if (this.options.initialFocus) {
      if (typeof this.options.initialFocus === 'string') {
        elementToFocus = this.container.querySelector(this.options.initialFocus);
      } else {
        elementToFocus = this.options.initialFocus;
      }
    }

    // Fallback to first focusable element
    if (!elementToFocus) {
      const focusableElements = this.getFocusableElements();
      elementToFocus = focusableElements[0] || this.container;
    }

    // Focus the element
    if (elementToFocus) {
      elementToFocus.focus();
    }
  }

  /**
   * Update the container element
   */
  updateContainer(newContainer: HTMLElement): void {
    this.container = newContainer;
  }

  /**
   * Check if the focus trap is currently active
   */
  isActivated(): boolean {
    return this.isActive;
  }
}

/**
 * Svelte action for focus trap
 * Usage: <div use:focusTrap={options}>
 */
export function focusTrap(node: HTMLElement, options: FocusTrapOptions = {}) {
  const trap = new FocusTrap(node, options);

  return {
    update(newOptions: FocusTrapOptions) {
      trap.deactivate();
      Object.assign(options, newOptions);
      if (trap.isActivated()) {
        trap.activate();
      }
    },
    destroy() {
      trap.deactivate();
    }
  };
}
