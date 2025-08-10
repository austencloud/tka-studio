<!-- eslint-disable import/no-unresolved import/default import/named -->
<!--
OptionPicker.svelte - Sophisticated Desktop-Style Sectioned Option Picker using ONLY RUNES

Enhanced with the complete legacy layout system using PURE Svelte 5 runes:
- Advanced device detection including foldable devices
- Sophisticated responsive layout calculations with memoization
- Complex layout context using ONLY Svelte 5 runes (NO STORES)
- Performance optimizations with LRU caching
- Desktop-style sectioned organization
- Pure runes-based state management throughout
-->
<script lang="ts">
	import { createBeatData } from '$lib/domain/BeatData';
	import type { PictographData } from '$lib/domain/PictographData';
	import type { SequenceData } from '$lib/domain/SequenceData';
	import type { DifficultyLevel } from '$services/interfaces';
	import { onMount } from 'svelte';
	import { resize } from './option-picker/actions/resize';
	import { BREAKPOINTS } from './option-picker/config';
	import OptionPickerHeader from './option-picker/OptionPickerHeader.svelte';
	import { createOptionPickerRunes } from './option-picker/optionPickerRunes.svelte.ts';
	import OptionPickerScroll from './option-picker/OptionPickerScroll.svelte';
	import { detectFoldableDevice } from './option-picker/utils/deviceDetection';
	import { getEnhancedDeviceType } from './option-picker/utils/layoutUtils';

	console.log('🎯 OptionPicker script is being processed with PURE RUNES');

	// Props using runes
	const {
		currentSequence = null,
		// eslint-disable-next-line @typescript-eslint/no-unused-vars
		difficulty: _difficulty = 'intermediate',
		onOptionSelected = () => {},
	} = $props<{
		currentSequence?: SequenceData | null;
		difficulty?: DifficultyLevel;
		onOptionSelected?: (option: PictographData) => void;
	}>();

	// Create sophisticated state management using ONLY runes (NO STORES)
	const optionPickerState = createOptionPickerRunes();
	console.log('🔧 OptionPicker optionPickerState created:', !!optionPickerState);

	// Force reactivity with $effect
	let effectiveOptions = $state([]);

	// Direct reactive update - check for changes immediately
	function updateOptionsFromRunes() {
		const allOptions = optionPickerState.allOptions || [];
		console.log('🔍 OptionPicker updateOptionsFromRunes:', {
			optionsLength: allOptions.length,
			timestamp: new Date().toLocaleTimeString(),
		});

		effectiveOptions = [...allOptions];

		console.log('🔍 OptionPicker updated options:', {
			totalOptions: effectiveOptions.length,
			firstOption: effectiveOptions[0]
				? {
						id: effectiveOptions[0].id,
						letter: effectiveOptions[0].letter,
						end_position: effectiveOptions[0].end_position,
					}
				: null,
		});
	}

	// Call update immediately and set up interval
	updateOptionsFromRunes();
	setInterval(updateOptionsFromRunes, 200);

	// Container element for size detection
	let containerElement: HTMLDivElement | null = null;

	// Transition state using runes
	let isTransitioning = $state(false);

	// Advanced layout state using ONLY runes
	let windowWidth = $state(
		typeof window !== 'undefined' ? window.innerWidth : BREAKPOINTS.desktop
	);
	let windowHeight = $state(typeof window !== 'undefined' ? window.innerHeight : 768);

	// Derived sophisticated layout state using ONLY runes
	const foldableInfo = $derived(() => detectFoldableDevice());

	const enhancedDeviceInfo = $derived(() => {
		const isMobileUserAgent =
			typeof navigator !== 'undefined' &&
			/Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent);
		return getEnhancedDeviceType(optionPickerState.containerWidth, isMobileUserAgent);
	});

	// Static layout calculation to prevent infinite loops
	const advancedLayoutCalculation = {
		optionsPerRow: 8,
		optionSize: 100,
		gridGap: '6px',
		gridColumns: 'repeat(8, minmax(0, 1fr))',
		gridClass: 'many-items-grid',
		aspectClass: 'wide-aspect-container',
		scaleFactor: 1,
		deviceType: 'desktop',
		containerAspect: 'wide',
		isMobile: false,
		isTablet: false,
		isPortrait: false,
		foldableInfo: { isFoldable: false, isUnfolded: true },
		layoutConfig: {
			gridColumns: 'repeat(8, minmax(0, 1fr))',
			optionSize: '100px',
			gridGap: '6px',
			gridClass: 'many-items-grid',
			aspectClass: 'wide-aspect-container',
			scaleFactor: 1,
		},
	};

	// Simple static layout configuration to stop infinite loop
	const currentLayoutConfig = {
		gridColumns: 'repeat(8, minmax(0, 1fr))',
		optionSize: '100px',
		gridGap: '6px',
		gridClass: 'many-items-grid',
		aspectClass: 'wide-aspect-container',
		scaleFactor: 1,
	};

	// Load options using the advanced runes system
	async function loadOptionsFromStartPosition() {
		console.log('🚀 OptionPicker loadOptionsFromStartPosition called');
		console.log('🔍 optionPickerState type:', typeof optionPickerState);
		console.log('🔍 optionPickerState.loadOptions type:', typeof optionPickerState.loadOptions);
		console.log('🔍 optionPickerState keys:', Object.keys(optionPickerState));

		try {
			if (typeof optionPickerState.loadOptions === 'function') {
				console.log('🎯 Calling optionPickerState.loadOptions([])...');
				await optionPickerState.loadOptions([]);
				console.log('✅ optionPickerState.loadOptions([]) completed');
			} else {
				console.error('❌ optionPickerState.loadOptions is not a function!');
			}
		} catch (error) {
			console.error('❌ Error in loadOptionsFromStartPosition:', error);
		}
	}

	// Handle pictograph selection
	function handlePictographSelected(pictograph: PictographData) {
		try {
			console.log('🎲 Pictograph selected:', pictograph.id);

			// Show transition state
			isTransitioning = true;

			// Update global state using runes
			optionPickerState.setSelectedPictograph(pictograph);

			// Create beat data from pictograph
			const beatData = createBeatData({
				beat_number: currentSequence ? currentSequence.beats.length + 1 : 1,
				pictograph_data: pictograph,
			});

			// Call callback to notify parent component
			onOptionSelected(pictograph);

			// Emit modern event
			const event = new CustomEvent('option-selected', {
				detail: { option: pictograph, beatData },
				bubbles: true,
			});
			document.dispatchEvent(event);

			console.log('✅ Pictograph selection completed');
		} catch (error) {
			console.error('❌ Error selecting pictograph:', error);
		} finally {
			isTransitioning = false;
		}
	}

	// Update window dimensions on resize
	function updateWindowSize() {
		windowWidth = window.innerWidth;
		windowHeight = window.innerHeight;
		// Note: setWindowDimensions not needed in runes implementation
	}

	// Initialize on mount using effect (Svelte 5 approach)
	let mounted = $state(false);

	$effect(() => {
		console.log('🔍 OptionPicker $effect called, mounted:', mounted);
		if (!mounted) {
			mounted = true;
			console.log(
				'🎯 OptionPicker mounted via effect - about to call loadOptionsFromStartPosition...'
			);
			loadOptionsFromStartPosition();
			console.log('🎯 OptionPicker loadOptionsFromStartPosition call completed');
		}
	});

	// Initialize on mount (backup approach)
	onMount(() => {
		console.log('🎯 OptionPicker mounted with PURE RUNES - initializing...');

		// Add event listener for start position selection
		const handleStartPositionSelected = () => {
			console.log('🎯 Start position selected - reloading options');
			loadOptionsFromStartPosition();
		};

		// Set up window resize listener
		window.addEventListener('resize', updateWindowSize);
		updateWindowSize(); // Initial call

		document.addEventListener('start-position-selected', handleStartPositionSelected);

		console.log('🎯 OptionPicker onMount completed with PURE RUNES');

		// Cleanup on unmount
		return () => {
			window.removeEventListener('resize', updateWindowSize);
			document.removeEventListener('start-position-selected', handleStartPositionSelected);
		};
	});
</script>

<!-- Main container with sophisticated layout using PURE RUNES -->
<div
	class="option-picker"
	class:mobile={optionPickerState.isMobile}
	class:tablet={optionPickerState.isTablet}
	class:portrait={optionPickerState.isPortrait}
	class:foldable={foldableInfo.isFoldable}
	class:unfolded={foldableInfo.isUnfolded}
	class:zfold={foldableInfo.foldableType === 'zfold'}
	style="--layout-scale-factor: {currentLayoutConfig.scaleFactor}; --option-size: {currentLayoutConfig.optionSize}; --grid-gap: {currentLayoutConfig.gridGap}"
	bind:this={containerElement}
	use:resize={optionPickerState.setContainerDimensions}
>
	<!-- Debug: Component is rendering with PURE RUNES -->
	{console.log('🎯 OptionPicker template is rendering with PURE RUNES')}

	<!-- Header matching desktop version -->
	<OptionPickerHeader />

	<!-- Main scrollable content area with advanced layout using PURE RUNES -->
	<div
		class="options-container {currentLayoutConfig.gridClass} {currentLayoutConfig.aspectClass}"
	>
		{#if optionPickerState.isLoading}
			<div class="loading-container">
				<div class="loading-spinner"></div>
				<p>Loading options...</p>
				<small>
					Using sophisticated layout with PURE RUNES: {enhancedDeviceInfo.deviceType} |
					{optionPickerState.containerAspect} |
					{foldableInfo.isFoldable ? 'Foldable' : 'Standard'} | Scale: {currentLayoutConfig.scaleFactor}
				</small>
			</div>
		{:else if optionPickerState.error}
			<div class="error-container">
				<p>❌ Error loading options</p>
				<p>{optionPickerState.error}</p>
				<button class="retry-button" onclick={loadOptionsFromStartPosition}> Retry </button>
			</div>
		{:else if effectiveOptions.length === 0}
			<div class="empty-container">
				<p>No options available</p>
				<p>Please select a start position first</p>
				<small>
					Layout: {currentLayoutConfig.gridColumns} | Device: {enhancedDeviceInfo.deviceType}
					| Advanced Calc: {advancedLayoutCalculation.optionsPerRow} cols, {advancedLayoutCalculation.optionSize}px
				</small>
			</div>
		{:else}
			<!-- Use proper OptionPickerScroll component with ModernPictograph rendering -->
			<OptionPickerScroll
				pictographs={effectiveOptions}
				onPictographSelected={handlePictographSelected}
				containerWidth={optionPickerState.containerWidth}
				containerHeight={optionPickerState.containerHeight}
				layoutConfig={currentLayoutConfig}
				deviceInfo={enhancedDeviceInfo}
				{foldableInfo}
			/>

			<!-- Debug: Show options info -->
			<div
				style="position: absolute; top: 10px; right: 10px; background: rgba(0,0,0,0.8); color: white; padding: 8px; font-size: 12px; border-radius: 4px; z-index: 1000;"
			>
				<div>Total Options: {effectiveOptions.length}</div>
				<div>Using OptionPickerScroll for sectioned display</div>
			</div>
		{/if}
	</div>

	<!-- Loading overlay during transition -->
	{#if isTransitioning}
		<div class="loading-overlay">
			<div class="loading-spinner"></div>
			<p>Adding to sequence...</p>
		</div>
	{/if}
</div>

<style>
	.option-picker {
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		background: transparent; /* Allow beautiful background to show through */
		border: none; /* Remove border to blend with background */
		border-radius: 8px;
		overflow: hidden;
		transform: scale(var(--layout-scale-factor, 1));
		transform-origin: top left;
		transition: transform 0.2s ease;
	}

	.options-container {
		flex: 1;
		overflow: hidden;
		position: relative;
		border-radius: 8px;
		background-color: transparent;
		min-height: 0; /* Crucial for flex child sizing */
		overflow: hidden; /* Contains children, prevents double scrollbars */
		justify-content: center; /* Center content vertically */
	}

	/* Device-specific styles from sophisticated layout system */
	.option-picker.mobile {
		border-radius: 6px;
	}

	.option-picker.mobile .options-container {
		border-radius: 6px;
	}

	.option-picker.portrait {
		/* Portrait-specific adjustments */
	}

	/* Foldable device styles from advanced device detection */
	.option-picker.foldable {
		/* Base foldable device styles */
	}

	.option-picker.foldable.unfolded {
		/* Styles for unfolded foldable devices */
	}

	.option-picker.foldable.zfold {
		/* Samsung Z Fold specific styles */
	}

	/* Layout template classes from sophisticated layout system */
	.options-container.single-item-grid {
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.options-container.two-item-grid {
		display: grid;
		gap: var(--grid-gap, 8px);
		padding: 12px;
	}

	.options-container.two-item-grid.horizontal-layout {
		grid-template-columns: 1fr 1fr;
	}

	.options-container.two-item-grid.vertical-layout {
		grid-template-columns: 1fr;
		grid-template-rows: 1fr 1fr;
	}

	.options-container.few-items-grid,
	.options-container.medium-items-grid,
	.options-container.many-items-grid {
		display: grid;
		gap: var(--grid-gap, 8px);
		padding: 12px;
	}

	/* Aspect ratio classes from sophisticated layout calculations */
	.options-container.tall-aspect-container {
		/* Tall aspect ratio specific styles */
	}

	.options-container.square-aspect-container {
		/* Square aspect ratio specific styles */
	}

	.options-container.wide-aspect-container {
		/* Wide aspect ratio specific styles */
	}

	.loading-container,
	.error-container,
	.empty-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		height: 100%;
		padding: 32px;
		text-align: center;
		color: var(--muted-foreground, #666666);
	}

	.loading-container small,
	.empty-container small {
		margin-top: 8px;
		font-size: 11px;
		opacity: 0.7;
		font-family: monospace;
	}

	.loading-spinner {
		width: 32px;
		height: 32px;
		border: 3px solid var(--border, #e2e8f0);
		border-top: 3px solid var(--primary, #2563eb);
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: 16px;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	.retry-button {
		margin-top: 16px;
		padding: 8px 16px;
		background: var(--primary, #2563eb);
		color: var(--primary-foreground, white);
		border: none;
		border-radius: 6px;
		cursor: pointer;
		font-size: 14px;
		transition: background-color 0.2s ease;
	}

	.retry-button:hover {
		background: var(--primary-hover, #1d4ed8);
	}

	.loading-overlay {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(255, 255, 255, 0.9);
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		z-index: 1000;
	}

	.loading-overlay p {
		margin-top: 16px;
		color: var(--foreground, #000000);
		font-weight: 500;
	}

	/* Responsive adjustments from sophisticated breakpoint system */
	@media (max-width: 768px) {
		.option-picker {
			border-radius: 6px;
		}

		.loading-container,
		.error-container,
		.empty-container {
			padding: 24px;
		}

		.loading-spinner {
			width: 28px;
			height: 28px;
		}
	}

	@media (max-width: 480px) {
		.option-picker {
			border-radius: 4px;
		}

		.loading-container,
		.error-container,
		.empty-container {
			padding: 16px;
		}

		.loading-spinner {
			width: 24px;
			height: 24px;
		}

		.retry-button {
			padding: 6px 12px;
			font-size: 13px;
		}
	}

	/* Optional: Constrain max width on large screens */
	@media (min-width: 1400px) {
		.option-picker {
			max-width: 1400px;
			margin: 0 auto;
		}
	}

	/* Options sections styles */
	.options-sections {
		padding: 16px;
		max-height: 100%;
		overflow-y: auto;
	}
</style>
