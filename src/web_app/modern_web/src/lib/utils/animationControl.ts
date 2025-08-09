/**
 * Simple Animation Control
 * Integrates with app settings to enable/disable animations
 */

import { setAnimationsEnabled } from './simpleFade';
import { getSettings } from '$stores/appState.svelte';

// Initialize animation state from settings
export function initializeAnimationControl() {
    const settings = getSettings();
    setAnimationsEnabled(settings.animationsEnabled ?? true);
}

// Update animation state when settings change
export function updateAnimationState(enabled: boolean) {
    setAnimationsEnabled(enabled);
}

// Utility to check if animations should run
export function shouldAnimate(): boolean {
    const settings = getSettings();
    return settings.animationsEnabled ?? true;
}
