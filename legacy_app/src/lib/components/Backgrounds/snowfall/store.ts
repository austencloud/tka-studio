import { writable, derived } from 'svelte/store';
import type { Dimensions, PerformanceMetrics } from '../types/types';

export const dimensions = writable<Dimensions>({ width: 0, height: 0 });
export const performanceMetrics = writable<PerformanceMetrics>({ fps: 60, warnings: [] });
export const isActive = writable<boolean>(true);
export const isDecember = writable<boolean>(false);
export const qualityMode = writable<'high' | 'medium' | 'low'>('high');

export const shouldRender = derived(
	[performanceMetrics, isActive],
	([$metrics, $isActive]) => $isActive && $metrics.fps > 30
);
