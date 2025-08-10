<!--
OptionPickerScrollContainer.svelte - Clean, focused scroll container component

Refactored from the large OptionPickerScroll.svelte with extracted responsibilities:
- State management moved to optionPickerScrollState.svelte.ts
- Pictograph organization moved to PictographOrganizerService
- Layout calculations moved to scrollLayoutMetrics utility
- Maintains all original functionality with cleaner separation of concerns
-->
<script lang="ts">
	import type { PictographData } from '$lib/domain/PictographData';
	import type { ResponsiveLayoutConfig } from './config';
	import type { FoldableDetectionResult } from './utils/deviceDetection';
	import type { DeviceInfo } from './utils/scrollLayoutMetrics';
	import OptionPickerSection from './OptionPickerSection.svelte';
	import { createOptionPickerScrollState, type ScrollContainerProps } from './optionPickerScrollState.svelte.ts';

	// ===== Props =====
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
		deviceInfo?: DeviceInfo;
		foldableInfo?: FoldableDetectionResult;
	}>();

	// ===== State Management =====
	const scrollState = createOptionPickerScrollState({
		pictographs,
		onPictographSelected,
		containerWidth,
		containerHeight,
		layoutConfig,
		deviceInfo,
		foldableInfo,
	});

	// ===== Reactive Updates =====
	// Update state when props change
	$effect(() => {
		scrollState.updateProps({
			pictographs,
			containerWidth,
			containerHeight,
			layoutConfig,
			deviceInfo,
			foldableInfo,
		});
	});

	// ===== Derived Values =====
	// Individual sections configuration
	const individualSections = ['Type1', 'Type2', 'Type3'];
	const groupedSections = ['Type4', 'Type5', 'Type6'];

	// ===== Debug Logging (Development Only) =====
	if (import.meta.env.DEV) {
		$effect(() => {
			if (scrollState.debugInfo) {
				console.log('🔍 OptionPickerScrollContainer debug info:', scrollState.debugInfo);
			}
		});
	}
</script>

<div
	class="option-picker-scroll {scrollState.cssClasses.join(' ')}"
	style:height="{containerHeight}px"
	style:--scroll-width={scrollState.cssProperties['--scroll-width']}
	style:--scroll-opacity={scrollState.cssProperties['--scroll-opacity']}
	style:--content-padding={scrollState.cssProperties['--content-padding']}
	style:--section-spacing={scrollState.cssProperties['--section-spacing']}
	style:--scale-factor={scrollState.cssProperties['--scale-factor']}
>
	<div class="scroll-container">
		<div class="content-layout">
			<!-- Main Content: Sectioned Layout -->
			{#if !scrollState.isEmpty}
				<div class="sections-container">
					<!-- Individual sections (Type1, Type2, Type3) -->
					{#if scrollState.hasIndividualSections}
						{#each individualSections as letterType (letterType)}
							{#if scrollState.organizedPictographs.individual[letterType]?.length > 0}
								<OptionPickerSection
									{letterType}
									pictographs={scrollState.organizedPictographs.individual[letterType]}
									{onPictographSelected}
									{containerWidth}
									isExpanded={true}
								/>
							{/if}
						{/each}
					{/if}

					<!-- Grouped sections (Type4, Type5, Type6) -->
					{#if scrollState.hasGroupedSections}
						{#each groupedSections as letterType (letterType)}
							{#if scrollState.organizedPictographs.grouped[letterType]?.length > 0}
								<OptionPickerSection
									{letterType}
									pictographs={scrollState.organizedPictographs.grouped[letterType]}
									{onPictographSelected}
									{containerWidth}
									isExpanded={true}
								/>
							{/if}
						{/each}
					{/if}
				</div>
			{/if}

			<!-- Empty State -->
			{#if scrollState.isEmpty}
				<div class="empty-state">
					<p>No options available for current sequence</p>
					{#if import.meta.env.DEV}
						<small>
							Container: {containerWidth}×{containerHeight} | 
							Layout: {layoutConfig.gridClass || 'default'} |
							Device: {deviceInfo.deviceType}
						</small>
					{/if}
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
