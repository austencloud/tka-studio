// src/lib/components/OptionPicker/utils/layoutUtils.ts

import { writable } from 'svelte/store';
import { memoizeLRU } from '$lib/utils/memoizationUtils';
import {
	DEVICE_CONFIG,
	LAYOUT_TEMPLATES,
	GAP_ADJUSTMENTS,
	getContainerAspect,
	getDeviceType,
	getLayoutCategory
} from '../config';
import { DEFAULT_COLUMNS, LAYOUT_RULES, GRID_GAP_OVERRIDES } from './layoutConfig';
import { detectFoldableDevice, type FoldableDetectionResult } from '$lib/utils/deviceDetection';

import type {
	DeviceType,
	LayoutCategory,
	ContainerAspect,
	ResponsiveLayoutConfig
} from '../config';

export const activeLayoutRule = writable<any>(null);

export function getEnhancedDeviceType(
	width: number,
	isMobileUserAgent: boolean
): {
	deviceType: DeviceType;
	isFoldable: boolean;
	foldableInfo: FoldableDetectionResult;
} {
	const foldableInfo = detectFoldableDevice();
	const baseDeviceType = getDeviceType(width, isMobileUserAgent);

	if (foldableInfo.isFoldable && foldableInfo.isUnfolded && foldableInfo.foldableType === 'zfold') {
		return {
			deviceType: 'tablet',
			isFoldable: true,
			foldableInfo
		};
	}

	return {
		deviceType: baseDeviceType,
		isFoldable: foldableInfo.isFoldable,
		foldableInfo
	};
}

interface GridConfigParams {
	count: number;
	containerWidth: number;
	containerHeight: number;
	isMobileDevice: boolean;
	isPortraitMode: boolean;
	foldableInfo?: FoldableDetectionResult;
	containerAspect?: ContainerAspect; // Added containerAspect property
}

export const getResponsiveLayout = memoizeLRU(
	(
		count: number,
		containerHeight: number = 0,
		containerWidth: number = 0,
		isMobileDevice: boolean = false,
		isPortraitMode: boolean = false,
		foldableInfoParam?: FoldableDetectionResult
	): ResponsiveLayoutConfig => {
		// Provide sensible defaults when dimensions aren't available yet
		// This is common during initial rendering before layout is calculated
		if (containerHeight <= 0 || containerWidth <= 0) {
			// Only log in development to avoid console spam
			if (import.meta.env.DEV) {
				// Use debug level instead of warn to reduce noise
				console.debug(
					'getResponsiveLayout: Using default layout until container dimensions are available.'
				);
			}

			// Return sensible defaults based on device type
			return {
				gridColumns: 'repeat(auto-fit, minmax(100px, 1fr))',
				optionSize: isMobileDevice ? '80px' : '100px',
				gridGap: '8px',
				gridClass: '',
				aspectClass: '',
				scaleFactor: isMobileDevice ? 0.95 : 1.0
			};
		}

		const foldableInfo = foldableInfoParam || detectFoldableDevice();
		const { deviceType: enhancedDeviceType } = getEnhancedDeviceType(
			containerWidth,
			isMobileDevice
		);

		const gridConfig = calculateGridConfiguration({
			count,
			containerWidth,
			containerHeight,
			isMobileDevice,
			isPortraitMode,
			foldableInfo
		});

		const optionSize = calculateOptionSize({
			count,
			containerWidth,
			containerHeight,
			gridConfig,
			isMobileDevice,
			isPortraitMode,
			foldableInfo
		});

		const containerAspect = getContainerAspect(containerWidth, containerHeight);

		let gridGap = getGridGap({
			count,
			containerWidth,
			containerHeight,
			isMobileDevice,
			isPortraitMode,
			foldableInfo
		});

		const { gridClass, aspectClass } = getGridClasses(
			count,
			containerWidth,
			containerHeight,
			isPortraitMode,
			foldableInfo
		);

		const deviceConfig = DEVICE_CONFIG[enhancedDeviceType];
		let scaleFactor = deviceConfig?.scaleFactor ?? (isMobileDevice ? 0.95 : 1.0);

		if (foldableInfo.isFoldable && foldableInfo.isUnfolded) {
			scaleFactor = Math.max(0.9, scaleFactor * 0.95);
		}

		return {
			gridColumns: gridConfig.template,
			optionSize,
			gridGap,
			gridClass,
			aspectClass,
			scaleFactor
		};
	},
	100,
	(
		count,
		containerHeight = 0,
		containerWidth = 0,
		isMobileDevice,
		isPortraitMode,
		foldableInfo
	) => {
		const roundedWidth = Math.round(containerWidth / 10) * 10;
		const roundedHeight = Math.round(containerHeight / 10) * 10;
		const foldableKey = foldableInfo?.isFoldable
			? `${foldableInfo.foldableType}-${foldableInfo.isUnfolded ? 'unfolded' : 'folded'}`
			: 'none';
		return `${count}:${roundedHeight}:${roundedWidth}:${isMobileDevice}:${isPortraitMode}:${foldableKey}`;
	}
);

function doesRuleMatch(rule: any, params: GridConfigParams): boolean {
	if (rule.when.count !== undefined && rule.when.count !== params.count) return false;
	if (rule.when.minCount !== undefined && params.count < rule.when.minCount) return false;
	if (rule.when.maxCount !== undefined && params.count > rule.when.maxCount) return false;
	if (rule.when.device === 'desktop' && params.isMobileDevice) return false;
	if (rule.when.device === 'mobile' && !params.isMobileDevice) return false;
	if (rule.when.aspect && rule.when.aspect !== params.containerAspect) return false;
	if (rule.when.aspects && !rule.when.aspects.includes(params.containerAspect)) return false;
	if (rule.when.orientation === 'portrait' && !params.isPortraitMode) return false;
	if (rule.when.orientation === 'landscape' && params.isPortraitMode) return false;
	if (
		rule.when.extraCheck &&
		!rule.when.extraCheck(params.containerWidth, params.containerHeight, params)
	)
		return false;

	return true;
}

const calculateGridConfiguration = memoizeLRU(
	(params: GridConfigParams) => {
		const layoutCategory = getLayoutCategory(params.count);
		const containerAspect = getContainerAspect(params.containerWidth, params.containerHeight);

		let columns = getBaseColumnCount(layoutCategory, containerAspect, params.isPortraitMode);

		const fullParams = {
			...params,
			containerAspect,
			layoutCategory
		};

		activeLayoutRule.set(null);

		for (const rule of LAYOUT_RULES) {
			if (doesRuleMatch(rule, fullParams)) {
				activeLayoutRule.set(rule);

				if (rule.columns === '+1') {
					columns = Math.min(rule.maxColumns || 8, columns + 1);
				} else {
					columns = parseInt(rule.columns.toString(), 10);
				}

				break;
			}
		}

		columns = Math.max(1, columns);

		if (params.foldableInfo?.isFoldable && params.foldableInfo.isUnfolded) {
			if (params.foldableInfo.foldableType === 'zfold' && !params.isPortraitMode && columns > 2) {
				columns = Math.min(columns, 5);
			}
		}

		const template = `repeat(${columns}, minmax(0, 1fr))`;

		return { columns, template };
	},
	100,
	(params) => {
		const { count, containerWidth, containerHeight, isMobileDevice, isPortraitMode, foldableInfo } =
			params;
		const roundedWidth = Math.round(containerWidth / 10) * 10;
		const roundedHeight = Math.round(containerHeight / 10) * 10;
		const foldableKey = foldableInfo?.isFoldable
			? `${foldableInfo.foldableType}-${foldableInfo.isUnfolded ? 'unfolded' : 'folded'}`
			: 'none';
		return `${count}:${roundedHeight}:${roundedWidth}:${isMobileDevice}:${isPortraitMode}:${foldableKey}`;
	}
);

function getGridGap(params: {
	count: number;
	containerWidth: number;
	containerHeight: number;
	isMobileDevice: boolean;
	isPortraitMode: boolean;
	foldableInfo?: FoldableDetectionResult;
}): string {
	const layoutCategory = getLayoutCategory(params.count);
	const deviceType = getDeviceType(params.containerWidth, params.isMobileDevice);
	const containerAspect = getContainerAspect(params.containerWidth, params.containerHeight);

	for (const override of GRID_GAP_OVERRIDES) {
		const fullParams = {
			...params,
			containerAspect,
			layoutCategory
		};

		if (doesRuleMatch(override, fullParams)) {
			return override.gap;
		}
	}

	const deviceConfig =
		DEVICE_CONFIG[deviceType as keyof typeof DEVICE_CONFIG] || DEVICE_CONFIG.desktop;

	let gapSize =
		deviceConfig.gap + (GAP_ADJUSTMENTS[layoutCategory as keyof typeof GAP_ADJUSTMENTS] || 0);

	if (params.foldableInfo?.isFoldable && params.foldableInfo.isUnfolded) {
		gapSize = Math.max(2, gapSize - 2);
	}

	// Enforce a minimum gap size of 6px regardless of screen width to prevent options sticking together
	return `${Math.max(6, gapSize)}px`;
}

function getGridClasses(
	count: number,
	containerWidth: number,
	containerHeight: number,
	isPortraitMode: boolean,
	foldableInfo?: FoldableDetectionResult
): { gridClass: string; aspectClass: string } {
	const layoutCategory = getLayoutCategory(count);
	const containerAspect = getContainerAspect(containerWidth, containerHeight);

	let gridClass = '';

	if (layoutCategory === 'singleItem') {
		gridClass = LAYOUT_TEMPLATES.singleItem.class;
	} else if (layoutCategory === 'twoItems') {
		const useVerticalLayout =
			containerAspect === 'tall' || (containerAspect === 'square' && isPortraitMode);
		gridClass = useVerticalLayout
			? LAYOUT_TEMPLATES.twoItems.vertical.class
			: LAYOUT_TEMPLATES.twoItems.horizontal.class;
	} else {
		const deviceOrientation = isPortraitMode ? 'portraitDevice' : 'landscapeDevice';
		gridClass = LAYOUT_TEMPLATES[layoutCategory][deviceOrientation].class;
	}

	if (foldableInfo?.isFoldable) {
		gridClass += ` foldable-${foldableInfo.foldableType}`;
		gridClass += foldableInfo.isUnfolded ? ' unfolded' : ' folded';
	}

	const aspectClass = `${containerAspect}-aspect-container`;

	return { gridClass, aspectClass };
}

const calculateOptionSize = memoizeLRU(
	(config: {
		count: number;
		containerWidth: number;
		containerHeight: number;
		gridConfig: { columns: number; template: string };
		isMobileDevice: boolean;
		isPortraitMode: boolean;
		foldableInfo?: FoldableDetectionResult;
	}): string => {
		const { count, containerWidth, containerHeight, gridConfig, isMobileDevice, foldableInfo } =
			config;
		const { columns } = gridConfig;

		if (containerWidth <= 0 || containerHeight <= 0 || columns <= 0) {
			return isMobileDevice ? '80px' : '100px';
		}

		const { deviceType } = getEnhancedDeviceType(containerWidth, isMobileDevice);
		const deviceConfig =
			DEVICE_CONFIG[deviceType as keyof typeof DEVICE_CONFIG] || DEVICE_CONFIG.desktop;

		const horizontalPadding = deviceConfig.padding.horizontal * 2;
		const verticalPadding = deviceConfig.padding.vertical * 2;
		const gapSize = deviceConfig.gap;
		const totalHorizontalGap = Math.max(0, columns - 1) * gapSize;
		const totalVerticalGap = Math.max(0, Math.ceil(count / columns) - 1) * gapSize;
		const availableWidth = containerWidth - horizontalPadding - totalHorizontalGap;
		const availableHeight = containerHeight - verticalPadding - totalVerticalGap;

		const widthPerItem = availableWidth / columns;
		const heightPerItem = availableHeight / Math.ceil(count / columns);

		let calculatedSize = Math.min(widthPerItem, heightPerItem);

		let scaleFactor = deviceConfig.scaleFactor;

		if (foldableInfo?.isFoldable && foldableInfo.isUnfolded) {
			if (foldableInfo.foldableType === 'zfold') {
				scaleFactor *= 0.95;
			}
		}

		calculatedSize *= scaleFactor;

		calculatedSize = Math.max(deviceConfig.minItemSize, calculatedSize);
		calculatedSize = Math.min(deviceConfig.maxItemSize, calculatedSize);

		return `${Math.floor(calculatedSize)}px`;
	},
	100,
	(config) => {
		const { count, containerWidth, containerHeight, gridConfig, isMobileDevice, foldableInfo } =
			config;
		const roundedWidth = Math.round(containerWidth / 10) * 10;
		const roundedHeight = Math.round(containerHeight / 10) * 10;
		const foldableKey = foldableInfo?.isFoldable
			? `${foldableInfo.foldableType}-${foldableInfo.isUnfolded ? 'unfolded' : 'folded'}`
			: 'none';
		return `${count}:${roundedHeight}:${roundedWidth}:${gridConfig.columns}:${isMobileDevice}:${foldableKey}`;
	}
);
function getBaseColumnCount(
	layoutCategory: LayoutCategory,
	aspect: ContainerAspect,
	isPortrait: boolean
): number {
	if (layoutCategory === 'singleItem') {
		return DEFAULT_COLUMNS.singleItem;
	}

	if (layoutCategory === 'twoItems') {
		// Determine vertical vs horizontal layout
		const useVerticalLayout = aspect === 'tall' || (aspect === 'square' && isPortrait);
		return useVerticalLayout
			? DEFAULT_COLUMNS.twoItems.vertical
			: DEFAULT_COLUMNS.twoItems.horizontal;
	}

	// For grid layouts, just use the default column count
	return DEFAULT_COLUMNS[layoutCategory] || 4;
}
