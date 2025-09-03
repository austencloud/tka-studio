// src/lib/components/ConstructTab/OptionPicker/store/navigationStore.ts
import { writable, derived } from 'svelte/store';
import type { SortMethod } from '../config';

export type NavigationDirection = 'forward' | 'backward' | 'initial';

interface NavigationState {
    currentTab: string | null;
    previousTab: string | null;
    direction: NavigationDirection;
    transitionLock: boolean;
    tabOrder: string[];
}

// Create the base navigation store
const createNavigationStore = () => {
    const initialState: NavigationState = {
        currentTab: null,
        previousTab: null,
        direction: 'initial',
        transitionLock: false,
        tabOrder: ['all'] // Will be populated dynamically
    };

    const { subscribe, update, set } = writable<NavigationState>(initialState);

    return {
        subscribe,

        /**
         * Navigate to a new tab with direction awareness
         */
        selectTab: (newTab: string | null, sortMethod: SortMethod) => {
            update(state => {
                // Prevent rapid navigation during transitions
                if (state.transitionLock) return state;

                // If same tab, no navigation needed
                if (state.currentTab === newTab) return state;

                // Determine direction based on tab order
                let direction: NavigationDirection = 'initial';

                if (state.currentTab && newTab) {
                    const prevIndex = state.tabOrder.indexOf(state.currentTab);
                    const newIndex = state.tabOrder.indexOf(newTab);

                    if (prevIndex !== -1 && newIndex !== -1) {
                        direction = prevIndex < newIndex ? 'forward' : 'backward';
                    }
                }

                // Set transition lock
                setTimeout(() => {
                    update(s => ({ ...s, transitionLock: false }));
                }, 350); // Slightly longer than transition duration

                return {
                    ...state,
                    previousTab: state.currentTab,
                    currentTab: newTab,
                    direction,
                    transitionLock: true
                };
            });
        },

        /**
         * Update the tab order based on available tabs
         */
        setTabOrder: (tabOrder: string[]) => {
            update(state => ({
                ...state,
                tabOrder
            }));
        },

        /**
         * Reset the navigation state
         */
        reset: () => {
            set(initialState);
        }
    };
};

export const navigationStore = createNavigationStore();

// Derived store for transition parameters
export const transitionParams = derived(
    navigationStore,
    ($nav) => ({
        direction: $nav.direction,
        duration: 300,
        delay: 0
    })
);
