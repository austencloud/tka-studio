// src/lib/components/GenerateTab/store/settings.ts
import { writable, derived } from 'svelte/store';

// Generator types
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

// Default settings
const DEFAULT_SETTINGS = {
	generatorType: 'circular' as GeneratorType,
	numBeats: 8,
	turnIntensity: 2, // Scale of 1-5
	propContinuity: 'continuous' as PropContinuityType,
	capType: 'mirrored' as CAPType,
	level: 1 // Difficulty level 1-5
};

// Create writable store with defaults
const { subscribe, set, update } = writable({ ...DEFAULT_SETTINGS });

// Derived stores for individual settings
export const generatorType = derived({ subscribe }, ($settings) => $settings.generatorType);

export const numBeats = derived({ subscribe }, ($settings) => $settings.numBeats);

export const turnIntensity = derived({ subscribe }, ($settings) => $settings.turnIntensity);

export const propContinuity = derived({ subscribe }, ($settings) => $settings.propContinuity);

export const capType = derived({ subscribe }, ($settings) => $settings.capType);

export const level = derived({ subscribe }, ($settings) => $settings.level);

// Helper functions to update individual settings
function setGeneratorType(type: GeneratorType) {
	update((settings) => ({ ...settings, generatorType: type }));
}

function setNumBeats(beats: number) {
	if (beats < 1) beats = 1;
	if (beats > 32) beats = 32;
	update((settings) => ({ ...settings, numBeats: beats }));
}

function setTurnIntensity(intensity: number) {
	if (intensity < 1) intensity = 1;
	if (intensity > 5) intensity = 5;
	update((settings) => ({ ...settings, turnIntensity: intensity }));
}

function setPropContinuity(continuity: PropContinuityType) {
	update((settings) => ({ ...settings, propContinuity: continuity }));
}

function setCAPType(type: CAPType) {
	update((settings) => ({ ...settings, capType: type }));
}

function setLevel(newLevel: number) {
	if (newLevel < 1) newLevel = 1;
	if (newLevel > 5) newLevel = 5;
	update((settings) => ({ ...settings, level: newLevel }));
}

function resetSettings() {
	set({ ...DEFAULT_SETTINGS });
}

// Export the store and its actions
export const settingsStore = {
	subscribe,
	setGeneratorType,
	setNumBeats,
	setTurnIntensity,
	setPropContinuity,
	setCAPType,
	setLevel,
	resetSettings
};
