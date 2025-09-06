// src/lib/components/OptionPicker/utils/layoutConfig.ts (Simplified Aspects)

// --- Interfaces ---
interface FoldableInfo {
	foldableType: 'zfold' | 'other' | 'unknown';
	isFoldable: boolean;
	isUnfolded: boolean;
	confidence?: number;
	detectionMethod?: string;
}

interface LayoutParams {
	count: number;
	foldableInfo?: FoldableInfo;
	isMobileDevice?: boolean;
	isPortraitMode?: boolean;
	device?: 'desktop' | 'mobile';
	// --- Simplified aspect type ---
	aspect?: 'tall' | 'wide' | 'square';
	orientation?: 'landscape' | 'portrait';
	containerWidth: number;
	containerHeight: number;
	layoutCategory?: string;
}

type ExtraCheck = (width: number, height: number, params: LayoutParams) => boolean;

interface LayoutRule {
	description: string;
	columns: number | '+1';
	maxColumns?: number;
	when: {
		count?: number;
		minCount?: number;
		maxCount?: number;
		device?: 'desktop' | 'mobile';
		// --- Use simplified aspect type ---
		aspect?: 'tall' | 'wide' | 'square';
		// Use 'aspects' only if multiple specific aspects are needed (e.g., wide and square)
		aspects?: Array<'tall' | 'wide' | 'square'>;
		orientation?: 'landscape' | 'portrait';
		extraCheck?: ExtraCheck;
	};
}

interface GridGapOverride {
	description: string;
	gap: string;
	when: {
		count?: number;
		minCount?: number;
		maxCount?: number;
		// --- Use simplified aspect type ---
		aspect?: 'tall' | 'wide' | 'square';
		orientation?: 'portrait' | 'landscape';
		extraCheck?: ExtraCheck;
	};
}

// --- Default Columns ---
export const DEFAULT_COLUMNS = {
	singleItem: 1,
	twoItems: { vertical: 1, horizontal: 2 },
	fewItems: 4,
	mediumItems: 4,
	manyItems: 4
};

// --- Layout Rules (Simplified Aspects) ---
export const LAYOUT_RULES: LayoutRule[] = [
	// --- Rules for Unfolded Foldable Devices ---
	// (Keep the workaround for foldableType)
	{
		description: 'Unfolded Foldable - Landscape, Few Items (<=8)',
		columns: 2,
		when: {
			maxCount: 8,
			extraCheck: (w, h, params) =>
				params?.foldableInfo?.isFoldable === true &&
				params?.foldableInfo?.isUnfolded === true &&
				params.isPortraitMode === false
		}
	},
	{
		description: 'Two items on foldable in portrait mode = 1 column',
		columns: 1,
		when: {
			count: 2,
			extraCheck: (w, h, params) =>
				params?.foldableInfo?.isFoldable === true &&
				params?.foldableInfo?.isUnfolded === true &&
				params.isPortraitMode === true
		}
	},

	{
		description: 'Unfolded Foldable - Portrait, Few Items (<=8)',
		columns: 2,
		when: {
			minCount: 3,
			maxCount: 8,
			extraCheck: (w, h, params) =>
				params?.foldableInfo?.isFoldable === true &&
				params?.foldableInfo?.isUnfolded === true &&
				params.isPortraitMode === true
		}
	},
	{
		description: 'Unfolded Foldable - Landscape, Medium Items (9-16)',
		columns: 4,
		when: {
			minCount: 9,
			maxCount: 16,
			extraCheck: (w, h, params) =>
				params?.foldableInfo?.isFoldable === true &&
				params?.foldableInfo?.isUnfolded === true &&
				params.isPortraitMode === false
		}
	},
	{
		description: 'Unfolded Foldable - Portrait, Medium Items (9-16)',
		columns: 4,
		when: {
			minCount: 9,
			maxCount: 16,
			extraCheck: (w, h, params) =>
				params?.foldableInfo?.isFoldable === true &&
				params?.foldableInfo?.isUnfolded === true &&
				params.isPortraitMode === true
		}
	},
	{
		description: 'Unfolded Foldable - Landscape, Many Items (17+)',
		columns: 4,
		when: {
			minCount: 17,
			extraCheck: (w, h, params) =>
				params?.foldableInfo?.isFoldable === true &&
				params?.foldableInfo?.isUnfolded === true &&
				params.isPortraitMode === false
		}
	},
	{
		description: 'Unfolded Foldable - Portrait, Many Items (17+)',
		columns: 4,
		when: {
			minCount: 17,
			extraCheck: (w, h, params) =>
				params?.foldableInfo?.isFoldable === true &&
				params?.foldableInfo?.isUnfolded === true &&
				params.isPortraitMode === true
		}
	},
	{
		description: 'Folded Foldable - Use Standard Mobile Layout',
		columns: 4,
		when: {
			minCount: 3,
			extraCheck: (w, h, params) =>
				params?.foldableInfo?.isFoldable === true && params?.foldableInfo?.isUnfolded === false
		}
	},

	// --- Standard Layout Rules (Simplified Aspects) ---
	{ description: '1 item = 1 column', columns: 1, when: { count: 1 } },
	{
		description: 'Two items, wide/square landscape = 2 columns',
		columns: 2,
		when: { count: 2, aspects: ['wide', 'square'], orientation: 'landscape' } // Removed 'widish'
	},
	{
		description: 'Two items, tall/square portrait = 1 column',
		columns: 1,
		when: { count: 2, aspects: ['tall', 'square'], orientation: 'portrait' }
	},
	{
		description: 'Few items (3-8) on mobile = 4 columns',
		columns: 4,
		when: { minCount: 3, maxCount: 8, device: 'mobile' }
	},
	{
		description: 'Medium items (9-16) on mobile = 4 columns',
		columns: 4,
		when: { minCount: 9, maxCount: 16, device: 'mobile' }
	},
	{
		description: 'Small window width forces 4 columns',
		columns: 4,
		when: {
			minCount: 17,
			device: 'desktop',
			aspect: 'square',
			extraCheck: (w) => w <= 700 // Enforce 4 columns for small window widths
		}
	},

	{
		description: 'Many items (17+) on mobile, tall = 4 columns',
		columns: 4,
		when: { minCount: 17, device: 'mobile', aspect: 'tall' }
	},
	{
		description: 'Many items (17+) on mobile, square = 4 columns',
		columns: 4,
		when: { minCount: 17, device: 'mobile', aspect: 'square' }
	},
	{
		description: 'Many items (17+) on mobile, wide = 6 columns',
		columns: 4,
		when: { minCount: 17, device: 'mobile', aspect: 'wide' }
	},
	{
		description: 'Few/Medium items (3-16) on desktop, tall = 2 columns',
		columns: 4,
		when: { minCount: 3, maxCount: 16, device: 'desktop', aspect: 'tall' }
	},
	{
		description: 'Few/Medium items (3-16) on desktop, square = 4 columns',
		columns: 4,
		when: { minCount: 3, maxCount: 16, device: 'desktop', aspect: 'square' }
	},
	{
		description: 'Few/Medium items (3-16) on desktop, wide = 4 columns',
		columns: 4,
		when: { minCount: 3, maxCount: 16, device: 'desktop', aspect: 'wide' }
	},
	{
		description: 'Many items (17+) on desktop, tall = 4 columns',
		columns: 4,
		when: { minCount: 17, device: 'desktop', aspect: 'tall' }
	},
	{
		description: 'Many items (17+) on desktop, square = 6 columns',
		columns: 8,
		when: { minCount: 17, device: 'desktop', aspect: 'square' }
	},
	{
		description: 'Many items (17+) on desktop, wide = 8 columns',
		columns: 8,
		when: { minCount: 17, device: 'desktop', aspect: 'wide' }
	},
	{
		description: 'Very wide desktop gets +1 column',
		columns: '+1',
		maxColumns: 8,
		when: {
			device: 'desktop',
			orientation: 'landscape',
			extraCheck: (w) => w > 1600
		}
	}
];

// --- Grid Gap Overrides (Simplified Aspects if needed) ---
// Check if any overrides relied on 'widish' - these seem okay as they are based on count or foldable state.
export const GRID_GAP_OVERRIDES: GridGapOverride[] = [
	{
		description: 'Unfolded Foldable with many items = smaller 6px gap',
		gap: '6px',
		when: {
			minCount: 12,
			extraCheck: (w, h, params) =>
				params?.foldableInfo?.isFoldable === true && params?.foldableInfo?.isUnfolded === true
		}
	},
	{
		description: 'Unfolded Foldable with few items = 8px gap',
		gap: '8px',
		when: {
			maxCount: 11,
			extraCheck: (w, h, params) =>
				params?.foldableInfo?.isFoldable === true && params?.foldableInfo?.isUnfolded === true
		}
	},
	{
		description: 'Wide desktop screens = 12px minimum gap',
		gap: '12px',
		when: {
			aspect: 'wide',
			extraCheck: (w, h, params) => w > 1400 && params?.device === 'desktop'
		}
	},
	{
		description: 'Example: 16 items in wide landscape = 10px gap',
		gap: '10px',
		when: { count: 16, aspect: 'wide', orientation: 'landscape' }
	},
	{
		description: 'Few/Medium items (3-16) on desktop, square aspect = 16px gap',
		gap: '16px',
		when: {
			minCount: 3,
			maxCount: 16,
			aspect: 'square',
			extraCheck: (w, h, params) =>
				params?.foldableInfo?.isFoldable !== true && // Not a foldable device
				params?.device === 'desktop' // Desktop only
		}
	}
];
