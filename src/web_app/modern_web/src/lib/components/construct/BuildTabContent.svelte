<!--
	BuildTabContent.svelte

	Build tab content component extracted from ConstructTab.
	Handles the conditional logic for showing either StartPositionPicker or OptionPicker
	based on the current sequence state.
-->
<script lang="ts">
	import { constructTabEventService } from '$services/implementations/ConstructTabEventService';
	import type { BeatData, PictographData } from '$services/interfaces';
	import { constructTabState } from '$stores/constructTabState.svelte';
	import OptionPickerContainer from './OptionPickerContainer.svelte';
	import StartPositionPicker from './StartPositionPicker.svelte';
	// Import fade transition for smooth switching
	import { GridMode } from '$domain/enums';
	import { getSettings } from '$lib/state/appState.svelte';
	import { resolve } from '$services/bootstrap';
	import { OptionDataService } from '$services/implementations/OptionDataService';
	import { fade } from 'svelte/transition';

	console.log('🎯 BuildTabContent script is being processed');

	// Simple debugging
	console.log('🎯 constructTabState available:', !!constructTabState);

	// Reactive state from store
	let shouldShowStartPositionPicker = $derived(constructTabState.shouldShowStartPositionPicker);
	let currentSequence = $derived(constructTabState.currentSequence);
	let gridMode = $derived(constructTabState.gridMode);
	let settings = $derived(getSettings());

	// Add debugging for the reactive values
	$effect(() => {
		console.log(
			'🔍 BuildTabContent shouldShowStartPositionPicker:',
			shouldShowStartPositionPicker
		);
		console.log('🔍 BuildTabContent currentSequence exists:', !!currentSequence);
	});

	// Preload all options for default start positions when component loads
	let isPreloading = $state(false);
	let preloadingComplete = $state(false);

	$effect(() => {
		// Only preload once when component first loads and we should show start position picker
		if (shouldShowStartPositionPicker && !preloadingComplete && !isPreloading) {
			preloadAllDefaultOptions();
		}
	});

	async function preloadAllDefaultOptions() {
		try {
			isPreloading = true;
			console.log('🚀 Preloading ALL options for ALL default start positions...');

			// Get the start position service to fetch default start positions
			const startPositionService = resolve('IStartPositionService') as {
				getDefaultStartPositions: (gridMode: GridMode) => Promise<PictographData[]>;
			};
			const defaultStartPositions = await startPositionService.getDefaultStartPositions(
				gridMode === 'diamond' ? GridMode.DIAMOND : GridMode.BOX
			);

			// Create and initialize option data service
			const optionDataService = new OptionDataService();
			await optionDataService.initialize();

			// Preload options for all default start positions
			const allPreloadedOptions: Record<string, PictographData[]> = {};

			for (const startPos of defaultStartPositions) {
				try {
					// Extract end position (similar to how StartPositionPicker does it)
					const endPosition = extractEndPosition(startPos);

					// Load options for this start position
					const options = await optionDataService.getNextOptionsFromEndPosition(
						endPosition,
						gridMode === 'diamond' ? GridMode.DIAMOND : GridMode.BOX,
						{}
					);

					// Store with end position as key for quick lookup
					allPreloadedOptions[endPosition] = options || [];
					console.log(
						`✅ Preloaded ${options?.length || 0} options for start position: ${endPosition}`
					);
				} catch (error) {
					console.warn(`Failed to preload options for start position:`, startPos, error);
				}
			}

			// Store all preloaded options in localStorage
			localStorage.setItem('all_preloaded_options', JSON.stringify(allPreloadedOptions));
			preloadingComplete = true;

			console.log(
				`🎉 Successfully preloaded options for ${Object.keys(allPreloadedOptions).length} start positions`,
				{
					startPositions: Object.keys(allPreloadedOptions),
					totalOptions: Object.values(allPreloadedOptions).reduce(
						(sum, opts) => sum + opts.length,
						0
					),
				}
			);
		} catch (error) {
			console.error('❌ Failed to preload default start position options:', error);
		} finally {
			isPreloading = false;
		}
	}

	// Helper function to extract end position from pictograph (same logic as StartPositionPicker)
	function extractEndPosition(pictograph: PictographData): string {
		try {
			// Extract end position based on motion data
			const blueMotion = pictograph.motions?.blue;
			const redMotion = pictograph.motions?.red;

			if (blueMotion && redMotion) {
				const blueEndLoc = blueMotion.end_loc || blueMotion.start_loc;
				const blueEndOri = blueMotion.end_ori || blueMotion.start_ori;
				const redEndLoc = redMotion.end_loc || redMotion.start_loc;
				const redEndOri = redMotion.end_ori || redMotion.start_ori;

				return `${blueEndLoc}_${blueEndOri}-${redEndLoc}_${redEndOri}`;
			}

			// Fallback to ID-based extraction
			if (pictograph.id) {
				const match = pictograph.id.match(/start-pos-(.+)/);
				return match?.[1] ?? 'alpha1_alpha1-0';
			}

			return 'alpha1_alpha1-0';
		} catch (error) {
			console.warn('Failed to extract end position:', error);
			return 'alpha1_alpha1-0';
		}
	}

	// Transition functions that respect animation settings - same as main interface
	const contentOut = (node: Element) => {
		const animationsEnabled = settings.animationsEnabled !== false;
		return fade(node, {
			duration: animationsEnabled ? 250 : 0,
		});
	};

	const contentIn = (node: Element) => {
		const animationsEnabled = settings.animationsEnabled !== false;
		return fade(node, {
			duration: animationsEnabled ? 300 : 0,
			delay: animationsEnabled ? 250 : 0, // Wait for out transition
		});
	};

	// Event handlers
	async function handleStartPositionSelected(startPosition: BeatData) {
		await constructTabEventService.handleStartPositionSelected(startPosition);
	}

	async function handleOptionSelected(option: PictographData) {
		await constructTabEventService.handleOptionSelected(option);
	}
</script>

<div class="build-tab-content" data-testid="build-tab-content">
	<!-- Start Position Picker -->
	{#if shouldShowStartPositionPicker}
		<div class="content-container" in:contentIn out:contentOut>
			<div class="panel-content">
				<StartPositionPicker
					{gridMode}
					onStartPositionSelected={handleStartPositionSelected}
				/>
			</div>
		</div>
	{/if}

	<!-- Option Picker -->
	{#if !shouldShowStartPositionPicker}
		<div class="content-container" in:contentIn out:contentOut>
			<div class="panel-content transparent-scroll">
				<OptionPickerContainer onOptionSelected={handleOptionSelected} />
			</div>
		</div>
	{/if}
</div>

<style>
	.build-tab-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		height: 100%;
		width: 100%;
		position: relative; /* Needed for absolute positioning of content */
	}

	.content-container {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		height: 100%;
		width: 100%;
	}

	.panel-content {
		flex: 1;
		overflow: auto;
		padding: var(--spacing-lg);
	}

	.panel-content.transparent-scroll {
		background: transparent;
	}

	/* Hide scrollbars for transparent scroll area while maintaining functionality */
	.panel-content.transparent-scroll::-webkit-scrollbar {
		width: 8px;
	}

	.panel-content.transparent-scroll::-webkit-scrollbar-track {
		background: transparent;
	}

	.panel-content.transparent-scroll::-webkit-scrollbar-thumb {
		background: rgba(255, 255, 255, 0.2);
		border-radius: 4px;
	}

	.panel-content.transparent-scroll::-webkit-scrollbar-thumb:hover {
		background: rgba(255, 255, 255, 0.3);
	}
</style>
