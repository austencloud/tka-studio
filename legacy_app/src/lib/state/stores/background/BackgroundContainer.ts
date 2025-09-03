/**
 * Modern Background Container
 *
 * This module provides a modern container-based implementation for managing
 * background state in the application.
 */

import { createContainer } from '$lib/state/core/container';
import type {
  BackgroundType,
  QualityLevel,
  PerformanceMetrics
} from '$lib/components/Backgrounds/types/types';
import { browser } from '$app/environment';

// Define the container state interface
export interface BackgroundState {
  currentBackground: BackgroundType;
  isReady: boolean;
  isVisible: boolean;
  quality: QualityLevel;
  performanceMetrics: PerformanceMetrics | null;
  availableBackgrounds: BackgroundType[];
  error: Error | null;
}

// Initial state
const initialState: BackgroundState = {
  currentBackground: 'snowfall',
  isReady: false,
  isVisible: true,
  quality: 'medium',
  performanceMetrics: null,
  availableBackgrounds: ['snowfall', 'nightSky'],
  error: null
};

// Load persisted state from localStorage if available
function loadPersistedState(): Partial<BackgroundState> {
  if (!browser) return {};

  try {
    const persisted = localStorage.getItem('background_state');
    if (persisted) {
      return JSON.parse(persisted);
    }
  } catch (error) {
    console.error('Failed to load persisted background state:', error);
  }

  return {};
}

// Merge initial state with persisted state
const mergedInitialState: BackgroundState = {
  ...initialState,
  ...loadPersistedState()
};

/**
 * Create the background container
 */
export const backgroundContainer = createContainer(
  mergedInitialState,
  (state, update) => {
    // Save state to localStorage when it changes
    if (browser) {
      const saveState = () => {
        try {
          localStorage.setItem(
            'background_state',
            JSON.stringify({
              currentBackground: state.currentBackground,
              isVisible: state.isVisible,
              quality: state.quality
            })
          );
        } catch (error) {
          console.error('Failed to save background state:', error);
        }
      };

      // Set up a subscription to save state changes
      const unsubscribe = backgroundContainer.subscribe(() => {
        saveState();
      });

      // Clean up subscription when the container is destroyed
      if (typeof window !== 'undefined') {
        window.addEventListener('beforeunload', unsubscribe);
      }
    }

    return {
      setBackground: (background: BackgroundType) => {
        update((state) => {
          // Validate background type
          if (!state.availableBackgrounds.includes(background)) {
            console.warn(`Invalid background type: ${background}. Using default.`);
            return state;
          }

          return {
            ...state,
            currentBackground: background,
            isReady: false // Reset ready state when changing background
          };
        });
      },

      setReady: (isReady: boolean) => {
        update((state) => ({
          ...state,
          isReady
        }));
      },

      setVisible: (isVisible: boolean) => {
        update((state) => ({
          ...state,
          isVisible
        }));
      },

      setQuality: (quality: QualityLevel) => {
        update((state) => ({
          ...state,
          quality
        }));
      },

      updatePerformanceMetrics: (metrics: PerformanceMetrics) => {
        update((state) => ({
          ...state,
          performanceMetrics: metrics
        }));
      },

      setError: (error: Error | null) => {
        update((state) => ({
          ...state,
          error
        }));
      },

      addAvailableBackground: (background: BackgroundType) => {
        update((state) => {
          if (state.availableBackgrounds.includes(background)) {
            return state;
          }

          return {
            ...state,
            availableBackgrounds: [...state.availableBackgrounds, background]
          };
        });
      },

      removeAvailableBackground: (background: BackgroundType) => {
        update((state) => {
          if (!state.availableBackgrounds.includes(background)) {
            return state;
          }

          return {
            ...state,
            availableBackgrounds: state.availableBackgrounds.filter(bg => bg !== background)
          };
        });
      }
    };
  }
);

// Export types
export type BackgroundContainer = typeof backgroundContainer;
