import { writable } from 'svelte/store';
import type { PictographData } from '../types/PictographData.js';

export const selectedPictograph = writable<PictographData | null>(null);