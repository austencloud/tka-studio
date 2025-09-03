// src/lib/components/ConstructTab/OptionPicker/utils/a11y.ts
import { writable } from 'svelte/store';
import { browser } from '$app/environment';

/**
 * Store to track user's preference for reduced motion
 */
export const prefersReducedMotion = writable(false);

// Initialize the store based on user's system preference
if (browser) {
    // Check if the user prefers reduced motion
    const mediaQuery = window.matchMedia('(prefers-reduced-motion: reduce)');

    // Set initial value
    prefersReducedMotion.set(mediaQuery.matches);

    // Update when preference changes
    mediaQuery.addEventListener('change', () => {
        prefersReducedMotion.set(mediaQuery.matches);
    });
}

/**
 * Focus management utilities
 */
export const focusUtils = {
    /**
     * Focus the first interactive element within a container
     * @param container The container element to search within
     * @param preventScroll Whether to prevent scrolling when focusing (default: true)
     */
    focusFirstInteractive(container: HTMLElement | null, preventScroll: boolean = true) {
        if (!container) return;

        setTimeout(() => {
            const selector = 'button:not([disabled]), [tabindex="0"], a[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled])';
            const firstInteractive = container.querySelector<HTMLElement>(selector);

            if (firstInteractive) {
                firstInteractive.focus({ preventScroll });
            }
        }, 50);
    },

    /**
     * Trap focus within a container (for modals, etc.)
     * @param container The container to trap focus within
     * @returns A function to remove the trap
     */
    trapFocus(container: HTMLElement): () => void {
        if (!container) return () => {};

        const focusableElements = container.querySelectorAll<HTMLElement>(
            'button:not([disabled]), [tabindex="0"], a[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled])'
        );

        if (focusableElements.length === 0) return () => {};

        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        const handleKeyDown = (e: KeyboardEvent) => {
            if (e.key === 'Tab') {
                if (e.shiftKey && document.activeElement === firstElement) {
                    e.preventDefault();
                    lastElement.focus();
                } else if (!e.shiftKey && document.activeElement === lastElement) {
                    e.preventDefault();
                    firstElement.focus();
                }
            }
        };

        container.addEventListener('keydown', handleKeyDown);

        return () => {
            container.removeEventListener('keydown', handleKeyDown);
        };
    }
};
