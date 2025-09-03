// src/stores/layoutStore.ts
import { writable } from 'svelte/store';

// Define a store for the number of beats
export const numBeatsStore = writable(16);

// Define a store for the current layout (rows and columns)
export const currentLayoutStore = writable({ rows: 4, cols: 4 });
