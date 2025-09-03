// src/lib/components/ConstructTab/OptionPicker/store/scrollStore.ts
import { writable } from 'svelte/store';

// Store to track scroll positions for different tabs/views
export const scrollPositions = writable<Record<string, number>>({});

/**
 * Helper functions for managing scroll positions
 */
export const scrollActions = {
    /**
     * Save the scroll position for a specific key
     * @param key Unique identifier (usually tab name)
     * @param position Scroll position to save
     */
    savePosition(key: string, position: number) {
        scrollPositions.update(positions => ({
            ...positions,
            [key]: position
        }));
    },

    /**
     * Get the saved scroll position for a specific key
     * @param key Unique identifier (usually tab name)
     * @returns The saved scroll position or 0 if not found
     */
    getPosition(key: string): number {
        let position = 0;
        const unsubscribe = scrollPositions.subscribe(positions => {
            position = positions[key] || 0;
        });
        unsubscribe();
        return position;
    },

    /**
     * Restore the scroll position for an element
     * @param element The DOM element to scroll
     * @param key Unique identifier (usually tab name)
     * @param delay Optional delay before restoring (default: 50ms)
     */
    restorePosition(element: HTMLElement | null, key: string, delay: number = 50) {
        if (!element) return;

        const savedPosition = this.getPosition(key);
        setTimeout(() => {
            if (element) {
                element.scrollTop = savedPosition;
            }
        }, delay);
    },

    /**
     * Clear all saved scroll positions
     */
    clearAll() {
        scrollPositions.set({});
    }
};
