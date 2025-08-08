/**
 * Settings Store Tests
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { get } from 'svelte/store';
import { settingsStore } from './settings.store.js';
import {
  selectTheme,
  selectBackground,
  selectEffectiveTheme,
  selectShowGridDebug
} from './settings.selectors.js';

describe('Settings Store', () => {
  beforeEach(() => {
    // Reset the store before each test
    settingsStore.reset();
  });

  it('should have the correct initial state', () => {
    const state = get(settingsStore);
    expect(state.theme).toBe('system');
    expect(state.background).toBe('snowfall');
    expect(state.backgroundQuality).toBe('medium');
    expect(state.defaultGridMode).toBe('diamond');
    expect(state.showGridDebug).toBe(false);
    expect(state.enableAnimations).toBe(true);
    expect(state.enableTransitions).toBe(true);
    expect(state.autoSave).toBe(true);
    expect(state.showTutorials).toBe(true);
    expect(state.highContrast).toBe(false);
    expect(state.reducedMotion).toBe(false);
    expect(state.lastUpdated).toBeGreaterThan(0);
  });

  it('should set theme', () => {
    settingsStore.setTheme('dark');

    const state = get(settingsStore);
    expect(state.theme).toBe('dark');
    expect(get(selectTheme)).toBe('dark');
  });

  it('should set background', () => {
    settingsStore.setBackground('nightSky');

    const state = get(settingsStore);
    expect(state.background).toBe('nightSky');
    expect(get(selectBackground)).toBe('nightSky');
  });

  it('should set background quality', () => {
    settingsStore.setBackgroundQuality('high');

    const state = get(settingsStore);
    expect(state.backgroundQuality).toBe('high');
  });

  it('should set default grid mode', () => {
    settingsStore.setDefaultGridMode('box');

    const state = get(settingsStore);
    expect(state.defaultGridMode).toBe('box');
  });

  it('should set show grid debug', () => {
    settingsStore.setShowGridDebug(true);

    const state = get(settingsStore);
    expect(state.showGridDebug).toBe(true);
    expect(get(selectShowGridDebug)).toBe(true);
  });

  it('should set enable animations', () => {
    settingsStore.setEnableAnimations(false);

    const state = get(settingsStore);
    expect(state.enableAnimations).toBe(false);
  });

  it('should set enable transitions', () => {
    settingsStore.setEnableTransitions(false);

    const state = get(settingsStore);
    expect(state.enableTransitions).toBe(false);
  });

  it('should set auto save', () => {
    settingsStore.setAutoSave(false);

    const state = get(settingsStore);
    expect(state.autoSave).toBe(false);
  });

  it('should set show tutorials', () => {
    settingsStore.setShowTutorials(false);

    const state = get(settingsStore);
    expect(state.showTutorials).toBe(false);
  });

  it('should set high contrast', () => {
    settingsStore.setHighContrast(true);

    const state = get(settingsStore);
    expect(state.highContrast).toBe(true);
  });

  it('should set reduced motion', () => {
    settingsStore.setReducedMotion(true);

    const state = get(settingsStore);
    expect(state.reducedMotion).toBe(true);
  });

  it('should update multiple settings at once', () => {
    settingsStore.updateSettings({
      theme: 'light',
      background: 'nightSky',
      enableAnimations: false
    });

    const state = get(settingsStore);
    expect(state.theme).toBe('light');
    expect(state.background).toBe('nightSky');
    expect(state.enableAnimations).toBe(false);
    // Other settings should remain unchanged
    expect(state.backgroundQuality).toBe('medium');
  });

  it('should update lastUpdated timestamp when settings change', () => {
    const initialTimestamp = get(settingsStore).lastUpdated;

    // Mock Date.now to return a specific value
    const mockNow = initialTimestamp + 1000;
    vi.spyOn(Date, 'now').mockImplementation(() => mockNow);

    settingsStore.setTheme('dark');

    const newTimestamp = get(settingsStore).lastUpdated;
    expect(newTimestamp).toBe(mockNow);
    expect(newTimestamp).toBeGreaterThan(initialTimestamp);

    // Restore Date.now
    vi.restoreAllMocks();
  });

  it('should resolve system theme preference', () => {
    // Mock window.matchMedia
    Object.defineProperty(window, 'matchMedia', {
      writable: true,
      value: vi.fn().mockImplementation(query => ({
        matches: query === '(prefers-color-scheme: dark)',
        media: query
      }))
    });

    // With system theme and dark preference
    settingsStore.setTheme('system');
    expect(get(selectEffectiveTheme)).toBe('dark');

    // With explicit theme
    settingsStore.setTheme('light');
    expect(get(selectEffectiveTheme)).toBe('light');
  });
});
