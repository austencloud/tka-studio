<!--
OptionPickerScroll.svelte - Advanced scrollable container with sophisticated layout

Enhanced with complete legacy layout system:
- Vertical layout with individual sections first (Types 1, 2, 3)
- Horizontal group widget for grouped sections (Types 4, 5, 6)
- Sophisticated responsive layout calculations
- Advanced device detection integration
- Performance optimizations from legacy system
- Transparent background and proper spacing
- Scrollable content area with advanced layout context
-->
<script lang="ts">
	import type { PictographData } from '$lib/domain/PictographData';
	import type { ResponsiveLayoutConfig } from './config';
	import OptionPickerSection from './OptionPickerSection.svelte';
	import type { FoldableDetectionResult } from './utils/deviceDetection';

	// Enhanced props with sophisticated layout system
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

	// Layout info available for debugging if needed

	// Organize sections like desktop: individual sections first, then grouped
	// Temporarily use string literals to avoid LetterType initialization issues
	const individualSections = ['Type1', 'Type2', 'Type3'];
	const groupedSections = ['Type4', 'Type5', 'Type6'];

	// Advanced pictograph filtering and organization
	const organizedPictographs = $derived.by(() => {
		const organized = {
			individual: {} as Record<string, PictographData[]>,
			grouped: {} as Record<string, PictographData[]>,
			totalCount: pictographs.length,
			hasIndividual: false,
			hasGrouped: false,
		};

		// Initialize sections
		individualSections.forEach((section) => {
			organized.individual[section] = [];
		});
		groupedSections.forEach((section) => {
			organized.grouped[section] = [];
		});

		// Organize pictographs by type (with error handling)
		pictographs.forEach((pictograph) => {
			try {
				// Simple letter type detection to avoid LetterType class issues
				let pictographType = 'Type1'; // Default fallback

				const letter = pictograph.letter || '';
				// Check longer patterns first to avoid partial matches
				if (letter.match(/^[WXYZ]-$|^[ΣΔθΩ]-$/)) pictographType = 'Type3';
				else if (letter.match(/^[ΦΨΛ]-$/)) pictographType = 'Type5';
				else if (letter.match(/^[A-V]$/)) pictographType = 'Type1';
				else if (letter.match(/^[WXYZ]$|^[ΣΔθΩ]$/)) pictographType = 'Type2';
				else if (letter.match(/^[ΦΨΛ]$/)) pictographType = 'Type4';
				else if (letter.match(/^[αβΓ]$/)) pictographType = 'Type6';

				if (individualSections.includes(pictographType)) {
					organized.individual[pictographType].push(pictograph);
					organized.hasIndividual = true;
				} else if (groupedSections.includes(pictographType)) {
					organized.grouped[pictographType].push(pictograph);
					organized.hasGrouped = true;
				}
			} catch (error) {
				console.warn('LetterType error for pictograph:', pictograph.letter, error);
				// Fallback: put all options in Type1 section
				organized.individual['Type1'].push(pictograph);
				organized.hasIndividual = true;
			}
		});

		return organized;
	});

	// Calculate sophisticated layout metrics
	const layoutMetrics = $derived(() => {
		const metrics = {
			shouldUseCompactLayout: containerHeight < 400,
			shouldUseMobileLayout:
				deviceInfo.deviceType === 'mobile' || deviceInfo.deviceType === 'smallMobile',
			shouldUseTabletLayout: deviceInfo.deviceType === 'tablet',
			isFoldableDevice: foldableInfo.isFoldable,
			isUnfoldedFoldable: foldableInfo.isFoldable && foldableInfo.isUnfolded,
			shouldAdjustForFoldable:
				foldableInfo.isFoldable && foldableInfo.foldableType === 'zfold',
			aspectRatio: containerWidth / containerHeight,
			isLandscape: containerWidth > containerHeight,
			isPortrait: containerHeight > containerWidth,
			effectiveScaleFactor: layoutConfig.scaleFactor,
			contentPadding: 8,
			sectionSpacing: 12,
		};

		// Adjust metrics for foldable devices
		if (metrics.shouldAdjustForFoldable) {
			metrics.contentPadding = metrics.isUnfoldedFoldable ? 12 : 6;
			metrics.sectionSpacing = metrics.isUnfoldedFoldable ? 16 : 8;
		}

		// Adjust for mobile devices
		if (metrics.shouldUseMobileLayout) {
			metrics.contentPadding = 6;
			metrics.sectionSpacing = 8;
		}

		return metrics;
	});

	// Check if we have any pictographs for grouped sections
	const hasGroupedPictographs = $derived(organizedPictographs.hasGrouped);

	// Advanced scroll behavior for different devices
	const scrollBehavior = $derived(() => {
		return {
			smoothScrolling: !layoutMetrics.shouldUseMobileLayout || foldableInfo.isUnfolded,
			scrollbarWidth: layoutMetrics.shouldUseMobileLayout ? '4px' : '8px',
			scrollbarOpacity: foldableInfo.isFoldable ? 0.3 : 0.2,
		};
	});
</script>

<div
	class="option-picker-scroll"
	class:mobile={layoutMetrics.shouldUseMobileLayout}
	class:tablet={layoutMetrics.shouldUseTabletLayout}
	class:foldable={layoutMetrics.isFoldableDevice}
	class:unfolded={layoutMetrics.isUnfoldedFoldable}
	class:compact={layoutMetrics.shouldUseCompactLayout}
	class:landscape={layoutMetrics.isLandscape}
	class:portrait={layoutMetrics.isPortrait}
	style:height="{containerHeight}px"
	style:--scroll-width={scrollBehavior.scrollbarWidth}
	style:--scroll-opacity={scrollBehavior.scrollbarOpacity}
	style:--content-padding="{layoutMetrics.contentPadding}px"
	style:--section-spacing="{layoutMetrics.sectionSpacing}px"
	style:--scale-factor={layoutMetrics.effectiveScaleFactor}
>
	<div class="scroll-container">
		<div class="content-layout">
			<!-- Debug info for development -->
			{#if import.meta.env.DEV}
				<div class="debug-info">
					<small>
						Layout: {layoutConfig.gridColumns} | Device: {deviceInfo.deviceType} |
						{foldableInfo.isFoldable
							? `Foldable (${foldableInfo.foldableType})`
							: 'Standard'} | Options: {organizedPictographs.totalCount}
					</small>
				</div>
			{/if}

			<!-- Sectioned layout with proper organization -->
			{#if pictographs.length > 0}
				<div class="sections-container">
					<!-- Individual sections (Type1, Type2, Type3) -->
					{#if organizedPictographs.hasIndividual}
						{#each individualSections as letterType (letterType)}
							{#if organizedPictographs.individual[letterType].length > 0}
								<OptionPickerSection
									{letterType}
									pictographs={organizedPictographs.individual[letterType]}
									{onPictographSelected}
									{containerWidth}
									isExpanded={true}
								/>
							{/if}
						{/each}
					{/if}

					<!-- Grouped sections (Type4, Type5, Type6) -->
					{#if organizedPictographs.hasGrouped}
						{#each groupedSections as letterType (letterType)}
							{#if organizedPictographs.grouped[letterType].length > 0}
								<OptionPickerSection
									{letterType}
									pictographs={organizedPictographs.grouped[letterType]}
									{onPictographSelected}
									{containerWidth}
									isExpanded={true}
								/>
							{/if}
						{/each}
					{/if}
				</div>
			{/if}

			<!-- Empty state with layout info -->
			{#if pictographs.length === 0}
				<div class="empty-state">
					<p>No options available for current sequence</p>
					<small>
						Container: {containerWidth}×{containerHeight} | Layout: {layoutConfig.gridClass ||
							'default'}
					</small>
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	.option-picker-scroll {
		width: 100%;
		/* Transparent background like desktop */
		background: transparent;
		border: none;
		/* Enable scrolling with sophisticated behavior */
		overflow-y: auto;
		overflow-x: hidden;
		/* Remove default margins */
		margin: 0;
		padding: 0;
		/* Apply scale factor for advanced device support */
		transform: scale(var(--scale-factor, 1));
		transform-origin: top left;
		/* Smooth scrolling for supported devices */
		scroll-behavior: smooth;
	}

	.scroll-container {
		width: 100%;
		min-height: 100%;
		/* Transparent background */
		background: transparent;
		/* Expanding size policy like desktop */
		display: flex;
		flex-direction: column;
		/* Apply content padding from sophisticated layout */
		padding: var(--content-padding, 8px);
	}

	.content-layout {
		/* Vertical layout with sophisticated spacing */
		display: flex;
		flex-direction: column;
		gap: var(--section-spacing, 12px);
		/* No margins like desktop */
		margin: 0;
		/* Fill available space */
		flex: 1;
		/* Transparent background */
		background: transparent;
	}

	/* Sections container styling */
	.sections-container {
		display: flex;
		flex-direction: column;
		gap: 16px;
		padding: 8px;
	}

	/* Debug info styling */
	.debug-info {
		padding: 4px 8px;
		background: rgba(0, 0, 0, 0.1);
		border-radius: 4px;
		font-size: 10px;
		color: #666;
		font-family: monospace;
		margin-bottom: 8px;
	}

	/* Empty state styling */
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 32px;
		text-align: center;
		color: var(--muted-foreground, #666);
		min-height: 200px;
	}

	.empty-state small {
		margin-top: 8px;
		font-size: 11px;
		opacity: 0.7;
		font-family: monospace;
	}

	/* Advanced scrollbar styling based on device type */
	.option-picker-scroll::-webkit-scrollbar {
		width: var(--scroll-width, 8px);
	}

	.option-picker-scroll::-webkit-scrollbar-track {
		background: transparent;
	}

	.option-picker-scroll::-webkit-scrollbar-thumb {
		background: rgba(0, 0, 0, var(--scroll-opacity, 0.2));
		border-radius: 4px;
		transition: background-color 0.2s ease;
	}

	.option-picker-scroll::-webkit-scrollbar-thumb:hover {
		background: rgba(0, 0, 0, calc(var(--scroll-opacity, 0.2) + 0.1));
	}

	/* Firefox scrollbar styling */
	.option-picker-scroll {
		scrollbar-width: thin;
		scrollbar-color: rgba(0, 0, 0, var(--scroll-opacity, 0.2)) transparent;
	}

	/* Device-specific adjustments */
	.option-picker-scroll.mobile {
		scroll-behavior: auto; /* Disable smooth scrolling on mobile for performance */
	}

	.option-picker-scroll.mobile .content-layout {
		gap: 8px;
	}

	.option-picker-scroll.tablet .content-layout {
		gap: 10px;
	}

	.option-picker-scroll.foldable {
		/* Special handling for foldable devices */
	}

	.option-picker-scroll.foldable.unfolded {
		/* Adjustments for unfolded foldable devices */
		scroll-behavior: smooth;
	}

	.option-picker-scroll.compact .content-layout {
		gap: 6px;
	}

	.option-picker-scroll.compact .scroll-container {
		padding: 4px;
	}

	/* Pictograph grid styles */
	.pictographs-grid {
		display: grid;
		width: 100%;
		box-sizing: border-box;
	}

	.pictograph-container {
		position: relative;
		cursor: pointer;
		border: 2px solid transparent;
		border-radius: 8px;
		transition: all 0.2s ease;
		background: rgba(255, 255, 255, 0.05);
		overflow: hidden;
	}

	.pictograph-container:hover {
		border-color: #4a90e2;
		background: rgba(255, 255, 255, 0.1);
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
	}

	.pictograph-container:focus {
		outline: none;
		border-color: #4a90e2;
		box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.3);
	}

	.pictograph-container:active {
		transform: translateY(0);
	}

	/* Landscape vs Portrait optimizations */
	.option-picker-scroll.landscape {
		/* Landscape-specific optimizations */
	}

	.option-picker-scroll.portrait {
		/* Portrait-specific optimizations */
	}

	/* Responsive breakpoints matching the sophisticated layout system */
	@media (max-width: 768px) {
		.option-picker-scroll {
			--scroll-width: 6px;
			--content-padding: 6px;
			--section-spacing: 8px;
		}
	}

	@media (max-width: 480px) {
		.option-picker-scroll {
			--scroll-width: 4px;
			--content-padding: 4px;
			--section-spacing: 6px;
		}
	}

	/* High DPI display optimizations */
	@media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {
		.option-picker-scroll::-webkit-scrollbar-thumb {
			background: rgba(0, 0, 0, calc(var(--scroll-opacity, 0.2) + 0.05));
		}
	}
</style>
