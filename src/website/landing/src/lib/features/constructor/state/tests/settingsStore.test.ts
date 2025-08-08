import { describe, it, expect, beforeEach } from 'vitest';
import { settingsStore } from '../stores/settingsStore.js';

describe('Settings Store', () => {
  beforeEach(() => {
    // Reset the store before each test
    settingsStore.resetSettings();
  });

  it('should have the correct initial state', () => {
    const state = settingsStore.getSnapshot();
    expect(state.generatorType).toBe('circular');
    expect(state.numBeats).toBe(8);
    expect(state.turnIntensity).toBe(2);
    expect(state.propContinuity).toBe('continuous');
    expect(state.capType).toBe('mirrored');
    expect(state.level).toBe(1);
    expect(state.theme).toBe('system');
    expect(state.animationsEnabled).toBe(true);
    expect(state.lastUsedGeneratorType).toBe('circular');
    expect(state.favoriteCapTypes).toEqual(['mirrored', 'rotated']);
  });

  it('should set generator type', () => {
    settingsStore.setGeneratorType('freeform');

    const state = settingsStore.getSnapshot();
    expect(state.generatorType).toBe('freeform');
    expect(state.lastUsedGeneratorType).toBe('freeform');
  });

  it('should set number of beats', () => {
    settingsStore.setNumBeats(16);

    const state = settingsStore.getSnapshot();
    expect(state.numBeats).toBe(16);
  });

  it('should clamp number of beats between 1 and 32', () => {
    settingsStore.setNumBeats(0);
    expect(settingsStore.getSnapshot().numBeats).toBe(1);

    settingsStore.setNumBeats(40);
    expect(settingsStore.getSnapshot().numBeats).toBe(32);
  });

  it('should set turn intensity', () => {
    settingsStore.setTurnIntensity(4);

    const state = settingsStore.getSnapshot();
    expect(state.turnIntensity).toBe(4);
  });

  it('should clamp turn intensity between 1 and 5', () => {
    settingsStore.setTurnIntensity(0);
    expect(settingsStore.getSnapshot().turnIntensity).toBe(1);

    settingsStore.setTurnIntensity(6);
    expect(settingsStore.getSnapshot().turnIntensity).toBe(5);
  });

  it('should set prop continuity', () => {
    settingsStore.setPropContinuity('random');

    const state = settingsStore.getSnapshot();
    expect(state.propContinuity).toBe('random');
  });

  it('should set CAP type', () => {
    settingsStore.setCAPType('rotated');

    const state = settingsStore.getSnapshot();
    expect(state.capType).toBe('rotated');
  });

  it('should set level', () => {
    settingsStore.setLevel(3);

    const state = settingsStore.getSnapshot();
    expect(state.level).toBe(3);
  });

  it('should clamp level between 1 and 5', () => {
    settingsStore.setLevel(0);
    expect(settingsStore.getSnapshot().level).toBe(1);

    settingsStore.setLevel(6);
    expect(settingsStore.getSnapshot().level).toBe(5);
  });

  it('should set theme', () => {
    settingsStore.setTheme('dark');

    const state = settingsStore.getSnapshot();
    expect(state.theme).toBe('dark');
  });

  it('should toggle animations', () => {
    const initialState = settingsStore.getSnapshot();
    settingsStore.toggleAnimations();

    const newState = settingsStore.getSnapshot();
    expect(newState.animationsEnabled).toBe(!initialState.animationsEnabled);
  });

  it('should add favorite CAP type', () => {
    settingsStore.addFavoriteCapType('strict_mirrored');

    const state = settingsStore.getSnapshot();
    expect(state.favoriteCapTypes).toContain('strict_mirrored');
  });

  it('should not add duplicate favorite CAP type', () => {
    const initialState = settingsStore.getSnapshot();
    const initialLength = initialState.favoriteCapTypes.length;

    settingsStore.addFavoriteCapType('mirrored');

    const newState = settingsStore.getSnapshot();
    expect(newState.favoriteCapTypes.length).toBe(initialLength);
  });

  it('should remove favorite CAP type', () => {
    settingsStore.removeFavoriteCapType('mirrored');

    const state = settingsStore.getSnapshot();
    expect(state.favoriteCapTypes).not.toContain('mirrored');
  });

  it('should reset settings to default values', () => {
    // Change some settings
    settingsStore.setGeneratorType('freeform');
    settingsStore.setNumBeats(16);
    settingsStore.setTheme('dark');

    // Reset settings
    settingsStore.resetSettings();

    // Check that settings are back to default
    const state = settingsStore.getSnapshot();
    expect(state.generatorType).toBe('circular');
    expect(state.numBeats).toBe(8);
    expect(state.theme).toBe('system');
  });
});
