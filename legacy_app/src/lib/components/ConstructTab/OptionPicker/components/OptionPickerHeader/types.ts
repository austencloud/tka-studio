// src/lib/components/ConstructTab/OptionPicker/components/OptionPickerHeader/types.ts

/**
 * Props for the OptionPickerHeader component
 */
export interface OptionPickerHeaderProps {
	selectedTab?: string | null;
	categoryKeys?: string[];
	showTabs?: boolean;
}

/**
 * Props for the TabsContainer component
 */
export interface TabsContainerProps {
	selectedTab: string | null;
	categoryKeys: string[];
	isScrollable: boolean;
	showScrollIndicator: boolean;
	useShortLabels: boolean;
	isMobileDevice: boolean;
	compactMode: boolean;
}

/**
 * Props for the TabButton component
 */
export interface TabButtonProps {
	categoryKey: string;
	isActive: boolean;
	isFirstTab: boolean;
	isLastTab: boolean;
	useShortLabels: boolean;
	tabFlexBasis: string;
	index: number;
	totalTabs: number;
}

/**
 * Props for the ScrollIndicator component
 */
export interface ScrollIndicatorProps {
	show: boolean;
}

/**
 * Mapping for tab labels
 */
export interface TabLabelMappings {
	long: Record<string, string>;
	short: Record<string, string>;
}
