// src/stores/settingsStore.ts
import { writable } from 'svelte/store';

// Default tab is 'User'
export const activeTabStore = writable('User');
