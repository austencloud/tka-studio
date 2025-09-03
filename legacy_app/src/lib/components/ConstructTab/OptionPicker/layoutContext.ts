// src/lib/components/OptionPicker/layoutContext.ts
import type { Readable } from 'svelte/store';
import type { DeviceType, ContainerAspect, ResponsiveLayoutConfig } from './config';
import type { detectFoldableDevice } from '$lib/utils/deviceDetection';

export const LAYOUT_CONTEXT_KEY = Symbol('layout-context');

export interface LayoutContextValue {
	deviceType: DeviceType;
	isMobile: boolean;
	isTablet: boolean;
	isPortrait: boolean;
	containerWidth: number;
	containerHeight: number; // Renamed from ht for clarity
	ht: number; // Keep for backward compatibility
	containerAspect: ContainerAspect;
	layoutConfig: ResponsiveLayoutConfig;
	foldableInfo?: ReturnType<typeof detectFoldableDevice>;
}

// Type helper for consuming the context
export type LayoutContext = Readable<LayoutContextValue>;
