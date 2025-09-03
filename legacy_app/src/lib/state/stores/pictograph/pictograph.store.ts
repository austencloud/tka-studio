/**
 * Pictograph Store
 *
 * This store manages the state of pictographs in the application.
 */

import { createStore } from '$lib/state/core';
import type { PictographData } from '$lib/types/PictographData';
import type { ArrowData } from '$lib/components/objects/Arrow/ArrowData';

// Define the store state interface
export interface PictographStoreState {
  status:
    | 'idle'
    | 'initializing'
    | 'grid_loading'
    | 'props_loading'
    | 'arrows_loading'
    | 'complete'
    | 'error';
  data: PictographData | null;
  error: { message: string; component?: string; timestamp: number } | null;
  loadProgress: number;
  components: {
    grid: boolean;
    redProp: boolean;
    blueProp: boolean;
    redArrow: boolean;
    blueArrow: boolean;
  };
  stateHistory: {
    from: string;
    to: string;
    reason?: string;
    timestamp: number;
  }[];
}

// Initial state
const initialState: PictographStoreState = {
  status: 'idle',
  data: null,
  error: null,
  loadProgress: 0,
  components: {
    grid: false,
    redProp: false,
    blueProp: false,
    redArrow: false,
    blueArrow: false
  },
  stateHistory: []
};

// Helper function to calculate progress
function calculateProgress(components: PictographStoreState['components']): number {
  const total = Object.keys(components).length;
  const loaded = Object.values(components).filter(Boolean).length;
  return Math.floor((loaded / Math.max(total, 1)) * 100);
}

// Create the store
export const pictographStore = createStore<PictographStoreState, {
  setData: (data: PictographData) => void;
  updateComponentLoaded: (component: keyof PictographStoreState['components']) => void;
  setError: (message: string, component?: string) => void;
  updatePropData: (color: 'red' | 'blue', propData: any) => void;
  updateArrowData: (color: 'red' | 'blue', arrowData: ArrowData) => void;
  transitionTo: (newState: PictographStoreState['status'], reason?: string) => void;
}>(
  'pictograph',
  initialState,
  (set, update, get) => {
    // Helper function to transition between states
    function transitionTo(newState: PictographStoreState['status'], reason?: string) {
      update(state => {
        if (state.status === newState) return state;

        const newTransition = {
          from: state.status,
          to: newState,
          reason,
          timestamp: Date.now()
        };

        const updatedHistory = [...state.stateHistory, newTransition].slice(-10);

        return {
          ...state,
          status: newState,
          stateHistory: updatedHistory
        };
      });
    }

    return {
      setData: (data: PictographData) => {
        transitionTo('initializing', 'Starting to load pictograph');
        update(state => ({ ...state, data, status: 'grid_loading' }));
      },

      updateComponentLoaded: (component: keyof PictographStoreState['components']) => {
        update(state => {
          const updatedComponents = {
            ...state.components,
            [component]: true
          };
          const newProgress = calculateProgress(updatedComponents);
          const allLoaded = Object.values(updatedComponents).every(Boolean);
          const newState = allLoaded ? 'complete' : state.status;
          if (allLoaded && newState !== 'complete') transitionTo('complete', 'All components loaded');
          return {
            ...state,
            components: updatedComponents,
            loadProgress: newProgress,
            status: newState
          };
        });
      },

      setError: (message: string, component?: string) => {
        update(state => ({
          ...state,
          status: 'error',
          error: {
            message,
            component,
            timestamp: Date.now()
          }
        }));
      },

      updatePropData: (color: 'red' | 'blue', propData: any) => {
        update(state => {
          if (!state.data) return state;
          const key = color === 'red' ? 'redPropData' : 'bluePropData';
          const componentKey = color === 'red' ? 'redProp' : 'blueProp';
          return {
            ...state,
            data: { ...state.data, [key]: propData },
            components: { ...state.components, [componentKey]: true }
          };
        });
      },

      updateArrowData: (color: 'red' | 'blue', arrowData: ArrowData) => {
        update(state => {
          if (!state.data) return state;
          const key = color === 'red' ? 'redArrowData' : 'blueArrowData';
          const componentKey = color === 'red' ? 'redArrow' : 'blueArrow';
          return {
            ...state,
            data: { ...state.data, [key]: arrowData },
            components: { ...state.components, [componentKey]: true }
          };
        });
      },

      transitionTo
    };
  },
  {
    persist: false,
    description: 'Manages the state of pictographs in the application'
  }
);
