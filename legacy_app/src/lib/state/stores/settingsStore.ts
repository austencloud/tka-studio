/**
 * Settings Store
 *
 * Centralized store for application settings, including sequence generation settings.
 */

import { createStore } from '../core/store';

// Types
export type GeneratorType = 'circular' | 'freeform';
export type PropContinuityType = 'continuous' | 'random';
export type CAPType =
  | 'mirrored'
  | 'rotated'
  | 'mirrored_complementary'
  | 'rotated_complementary'
  | 'mirrored_swapped'
  | 'rotated_swapped'
  | 'strict_mirrored'
  | 'strict_rotated'
  | 'strict_complementary'
  | 'strict_swapped'
  | 'swapped_complementary';

// Settings state interface
export interface SettingsState {
  // Generator settings
  generatorType: GeneratorType;
  numBeats: number;
  turnIntensity: number; // Scale of 1-5
  propContinuity: PropContinuityType;
  capType: CAPType;
  level: number; // Difficulty level 1-5

  // UI settings
  theme: 'light' | 'dark' | 'system';
  animationsEnabled: boolean;

  // User preferences
  lastUsedGeneratorType: GeneratorType;
  favoriteCapTypes: CAPType[];
}

// Default settings
const DEFAULT_SETTINGS: SettingsState = {
  generatorType: 'circular',
  numBeats: 8,
  turnIntensity: 2,
  propContinuity: 'continuous',
  capType: 'mirrored',
  level: 1,

  theme: 'system',
  animationsEnabled: true,

  lastUsedGeneratorType: 'circular',
  favoriteCapTypes: ['mirrored', 'rotated']
};

// Create the settings store
export const settingsStore = createStore<
  SettingsState,
  {
    setGeneratorType: (type: GeneratorType) => void;
    setNumBeats: (beats: number) => void;
    setTurnIntensity: (intensity: number) => void;
    setPropContinuity: (continuity: PropContinuityType) => void;
    setCAPType: (type: CAPType) => void;
    setLevel: (level: number) => void;
    setTheme: (theme: 'light' | 'dark' | 'system') => void;
    toggleAnimations: () => void;
    addFavoriteCapType: (type: CAPType) => void;
    removeFavoriteCapType: (type: CAPType) => void;
    resetSettings: () => void;
  }
>(
  'settings',
  DEFAULT_SETTINGS,
  (set, update) => ({
    setGeneratorType: (type: GeneratorType) => {
      update((state) => ({
        ...state,
        generatorType: type,
        lastUsedGeneratorType: type
      }));
    },

    setNumBeats: (beats: number) => {
      update((state) => ({
        ...state,
        numBeats: Math.max(1, Math.min(32, beats)) // Clamp between 1-32
      }));
    },

    setTurnIntensity: (intensity: number) => {
      update((state) => ({
        ...state,
        turnIntensity: Math.max(1, Math.min(5, intensity)) // Clamp between 1-5
      }));
    },

    setPropContinuity: (continuity: PropContinuityType) => {
      update((state) => ({
        ...state,
        propContinuity: continuity
      }));
    },

    setCAPType: (type: CAPType) => {
      update((state) => ({
        ...state,
        capType: type
      }));
    },

    setLevel: (level: number) => {
      update((state) => ({
        ...state,
        level: Math.max(1, Math.min(5, level)) // Clamp between 1-5
      }));
    },

    setTheme: (theme: 'light' | 'dark' | 'system') => {
      update((state) => ({
        ...state,
        theme
      }));
    },

    toggleAnimations: () => {
      update((state) => ({
        ...state,
        animationsEnabled: !state.animationsEnabled
      }));
    },

    addFavoriteCapType: (type: CAPType) => {
      update((state) => {
        if (state.favoriteCapTypes.includes(type)) {
          return state;
        }
        return {
          ...state,
          favoriteCapTypes: [...state.favoriteCapTypes, type]
        };
      });
    },

    removeFavoriteCapType: (type: CAPType) => {
      update((state) => ({
        ...state,
        favoriteCapTypes: state.favoriteCapTypes.filter((t) => t !== type)
      }));
    },

    resetSettings: () => {
      set(DEFAULT_SETTINGS);
    }
  }),
  {
    persist: true,
    description: 'Application settings including sequence generation parameters'
  }
);

// Export individual settings as getters for convenience
export const getGeneratorType = () => settingsStore.getSnapshot().generatorType;
export const getNumBeats = () => settingsStore.getSnapshot().numBeats;
export const getTurnIntensity = () => settingsStore.getSnapshot().turnIntensity;
export const getPropContinuity = () => settingsStore.getSnapshot().propContinuity;
export const getCAPType = () => settingsStore.getSnapshot().capType;
export const getLevel = () => settingsStore.getSnapshot().level;
