<!--
OptionPickerScroll.svelte - Backward compatibility wrapper

This file has been refactored for better maintainability. The original functionality 
has been split into focused components following the established system patterns:

- PictographOrganizerService: Handles pictograph organization logic
- scrollLayoutMetrics: Manages sophisticated layout calculations  
- optionPickerScrollState: Provides state management using Svelte 5 runes
- OptionPickerScrollContainer: Clean UI component with all functionality

This wrapper maintains backward compatibility while providing the new architecture.
-->
<script lang="ts">
	import type { PictographData } from '$lib/domain/PictographData';
	import type { ResponsiveLayoutConfig } from './config';
	import type { FoldableDetectionResult } from './utils/deviceDetection';
	import OptionPickerScrollContainer from './OptionPickerScrollContainer.svelte';

	// ===== Props (unchanged interface for backward compatibility) =====
	const {
		pictographs = [],
		onPictographSelected = () => {},
		containerWidth = 800,
		containerHeight = 600,
		layoutConfig = {
			gridColumns: 'repeat(4, minmax(0, 1fr))',
			optionSize: '100px',
			gridGap: '8px',
			gridClass: '',
			aspectClass: '',
			scaleFactor: 1.0,
		},
		deviceInfo = {
			deviceType: 'desktop' as const,
			isFoldable: false,
			foldableInfo: {
				isFoldable: false,
				isUnfolded: false,
				foldableType: 'unknown' as const,
				confidence: 0,
			},
		},
		foldableInfo = {
			isFoldable: false,
			isUnfolded: false,
			foldableType: 'unknown' as const,
			confidence: 0,
		},
	} = $props<{
		pictographs?: PictographData[];
		onPictographSelected?: (pictograph: PictographData) => void;
		containerWidth?: number;
		containerHeight?: number;
		layoutConfig?: ResponsiveLayoutConfig;
		deviceInfo?: {
			deviceType: string;
			isFoldable: boolean;
			foldableInfo: FoldableDetectionResult;
		};
		foldableInfo?: FoldableDetectionResult;
	}>();
</script>

<!-- 
   Delegate to the new OptionPickerScrollContainer with all the same props.
   This maintains exact backward compatibility while using the new architecture.
-->
<OptionPickerScrollContainer
	{pictographs}
	{onPictographSelected}
	{containerWidth}
	{containerHeight}
	{layoutConfig}
	{deviceInfo}
	{foldableInfo}
/>
