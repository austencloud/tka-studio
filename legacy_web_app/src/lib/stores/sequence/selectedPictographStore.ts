import { writable } from 'svelte/store';
import type { PictographData } from '$lib/types/PictographData';

export const selectedPictograph = writable<PictographData | null>(null);