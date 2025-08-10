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
	import { OptionDataService } from '$lib/services/implementations/OptionDataService';
	import { getCurrentSequence } from '$lib/stores/sequenceState.svelte';
	import type { DifficultyLevel } from '$services/interfaces';
	import { onMount } from 'svelte';
	import { resize } from './option-picker/actions/resize';
	import { BREAKPOINTS } from './option-picker/config';
	import OptionPickerHeader from './option-picker/OptionPickerHeader.svelte';
	import { OptionPickerLayoutManager } from './option-picker/OptionPickerLayoutManager';
	import OptionPickerScroll from './option-picker/OptionPickerScroll.svelte';
	import { createOptionPickerState } from './option-picker/OptionPickerSectionState.svelte.js';
	import { LetterType } from './option-picker/types/LetterType';
	import { detectFoldableDevice } from './option-picker/utils/deviceDetection';
	import { getEnhancedDeviceType, getResponsiveLayout } from './option-picker/utils/layoutUtils';

	console.log('🎯 OptionPicker script is being processed with PURE RUNES');

	// Helper function to get the end position from the current sequence
	function getCurrentSequenceEndPosition(): string | null {
		const currentSequence = getCurrentSequence();
		console.log(
			'🔍 getCurrentSequence() returned:',
			currentSequence
				? {
						id: currentSequence.id,
						name: currentSequence.name,
						beats: currentSequence.beats?.length || 0,
						hasStartPosition: !!currentSequence.start_position,
					}
				: 'null'
		);

		if (!currentSequence) {
			console.warn('⚠️ No current sequence found');
			return null;
		}

		// First, check if there's a start position (for new sequences)
		if (currentSequence.start_position?.pictograph_data) {
			const startEndPosition = extractEndPositionFromPictograph(
				currentSequence.start_position.pictograph_data
			);
			console.log(`🎯 Using start position as end position: ${startEndPosition}`);
			return startEndPosition;
		}

		// Then, find the last non-blank beat (for sequences with beats)
		if (currentSequence.beats && currentSequence.beats.length > 0) {
			for (let i = currentSequence.beats.length - 1; i >= 0; i--) {
				type LegacyBeat = { is_blank: boolean; pictograph_data?: PictographData | null };
				type NewBeat = { isBlank?: boolean; pictographData?: PictographData | null };
				const rawBeat = currentSequence.beats[i] as LegacyBeat | NewBeat | undefined;
				if (!rawBeat) continue;
				const isBlank = 'is_blank' in rawBeat ? rawBeat.is_blank : rawBeat.isBlank === true;
				const pictograph =
					'pictograph_data' in rawBeat ? rawBeat.pictograph_data : rawBeat.pictographData;
				if (!isBlank && pictograph) {
					// Extract end position from the pictograph data
					const endPosition = extractEndPositionFromPictograph(pictograph);
					console.log(`🎯 Found end position from beat ${i}: ${endPosition}`);
					return endPosition;
				}
			}
		}

		console.warn('⚠️ No end position found in sequence');
		return null;
	}

	// Helper function to extract end position from pictograph data
	function extractEndPositionFromPictograph(pictographData: PictographData): string | null {
		console.log('🔍 Extracting end position from pictograph:', {
			id: pictographData.id,
			letter: pictographData.letter,
			end_position: pictographData.end_position,
			metadata: pictographData.metadata,
			motions: pictographData.motions,
		});

		// Try to get from end_position field first
		if (pictographData.end_position) {
			console.log(`✅ Found end_position field: ${pictographData.end_position}`);
			return pictographData.end_position;
		}

		// Try to get from metadata
		if (pictographData.metadata?.endPosition) {
			console.log(`✅ Found metadata.endPosition: ${pictographData.metadata.endPosition}`);
			return pictographData.metadata.endPosition;
		}

		// For start positions, try to extract from the ID or letter
		if (pictographData.id?.includes('start-pos-')) {
			// Extract from start position ID like "start-pos-gamma11_gamma11-2"
			const match = pictographData.id.match(/start-pos-([^_]+)_/);
			if (match && match[1]) {
				const endPos = match[1];
				console.log(`✅ Extracted from start position ID: ${endPos}`);
				return endPos;
			}
		}

		// Try to get from motion data as fallback
		if (pictographData.motions?.blue?.end_loc) {
			const mapped = mapLocationToPosition(pictographData.motions.blue.end_loc);
			console.log(`⚠️ Using blue motion end_loc fallback: ${mapped}`);
			return mapped;
		}
		if (pictographData.motions?.red?.end_loc) {
			const mapped = mapLocationToPosition(pictographData.motions.red.end_loc);
			console.log(`⚠️ Using red motion end_loc fallback: ${mapped}`);
			return mapped;
		}

		console.warn('⚠️ No end position found, defaulting to alpha1');
		return 'alpha1';
	}

	// Helper function to map location to position string
	function mapLocationToPosition(location: string | Location): string {
		// Basic mapping - this matches the legacy system
		const locationMap: Record<string, string> = {
			n: 'alpha1',
			s: 'alpha1',
			e: 'gamma11',
			w: 'alpha1',
			ne: 'beta5',
			se: 'gamma11',
			sw: 'alpha1',
			nw: 'beta5',
		};

		const locationStr = typeof location === 'string' ? location : location?.toString() || '';
		return locationMap[locationStr.toLowerCase()] || 'alpha1';
	}

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
	const optionPickerState = createOptionPickerState();

	// Simple reactive state for options (backup solution)
	let simpleOptionsData = $state<PictographData[]>([]);

	// Derived state that uses backup when main state is empty
	let effectiveOptions = $derived.by(() => {
		const mainOptions = optionPickerState.allOptions || [];
		const backupOptions = simpleOptionsData || [];
		const result = mainOptions.length > 0 ? mainOptions : backupOptions;
		console.log('🔧 effectiveOptions:', {
			mainLength: mainOptions.length,
			backupLength: backupOptions.length,
			resultLength: result.length,
			usingBackup: mainOptions.length === 0 && backupOptions.length > 0,
		});
		return result;
	});

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

	const currentLayoutConfig = $derived(() => {
		const optionsCount = effectiveOptions.length;

		return getResponsiveLayout(
			optionsCount,
			optionPickerState.containerHeight,
			optionPickerState.containerWidth,
			optionPickerState.isMobile,
			optionPickerState.isPortrait,
			foldableInfo
		);
	});

	// Advanced layout calculation using the sophisticated layout manager
	const advancedLayoutCalculation = $derived(() => {
		return OptionPickerLayoutManager.calculateLayout({
			count: effectiveOptions.length,
			containerWidth: optionPickerState.containerWidth,
			containerHeight: optionPickerState.containerHeight,
			windowWidth,
			windowHeight,
			isMobileUserAgent:
				typeof navigator !== 'undefined' &&
				/Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent),
		});
	});

	// Initialize data service and load options
	async function initializeAndLoadOptions() {
		try {
			console.log('🎯 OptionPicker: initializeAndLoadOptions called with PURE RUNES');
			optionPickerState.setLoading(true);

			// Get the current sequence's end position
			const endPosition = getCurrentSequenceEndPosition();
			if (!endPosition) {
				console.warn('⚠️ No end position found, cannot load options');
				optionPickerState.setOptions([]);
				optionPickerState.setError(null);
				return;
			}

			console.log(`🎯 Loading real options for end position: ${endPosition}`);

			// Create OptionDataService instance and load real data
			const optionDataService = new OptionDataService();
			await optionDataService.initialize();

			// Get real options from CSV data
			const realOptions = await optionDataService.getNextOptionsFromEndPosition(
				endPosition,
				'diamond', // Default to diamond mode for now
				{} // No filters - show all options
			);

			console.log(`✅ Loaded ${realOptions.length} real options from CSV data`);

			// Debug: Test the LetterType.getLetterType function with real data
			console.log('🔍 Testing LetterType.getLetterType function with real data:');
			realOptions.slice(0, 10).forEach((option) => {
				const letterType = LetterType.getLetterType(option.letter || '');
				console.log(`  Letter "${option.letter}" -> Type "${letterType}"`);
			});

			console.log('🔧 About to set options in state:', {
				optionsCount: realOptions.length,
				firstOption: realOptions[0]?.letter,
				stateType: typeof optionPickerState,
				hasSetOptions: typeof optionPickerState.setOptions === 'function',
			});

			optionPickerState.setOptions(realOptions);
			console.log(
				'🔧 Options set in state, current allOptions length:',
				optionPickerState.allOptions?.length
			);

			// Also set the simple backup state
			simpleOptionsData = realOptions;
			console.log('🔧 Simple backup state set with length:', simpleOptionsData.length);

			// Check state after a brief delay to see if it's a reactivity timing issue
			setTimeout(() => {
				console.log(
					'🔧 Options state after timeout:',
					optionPickerState.allOptions?.length
				);
				console.log('🔧 Simple backup state after timeout:', simpleOptionsData.length);
			}, 100);

			optionPickerState.setError(null);
		} catch (error) {
			console.error('❌ Error loading real options:', error);
			optionPickerState.setError(error instanceof Error ? error.message : 'Unknown error');
			optionPickerState.setOptions([]);
		} finally {
			optionPickerState.setLoading(false);
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
		optionPickerState.setWindowDimensions(windowWidth, windowHeight);
	}

	// Initialize on mount using effect (Svelte 5 approach)
	let mounted = $state(false);

	$effect(() => {
		if (!mounted) {
			mounted = true;
			console.log('🎯 OptionPicker mounted via effect with PURE RUNES - initializing...');

			// Initialize and load options
			try {
				console.log('🎯 About to call initializeAndLoadOptions...');
				initializeAndLoadOptions().catch((error) => {
					console.error('❌ Error in initializeAndLoadOptions:', error);
				});
			} catch (error) {
				console.error('❌ Sync error in initializeAndLoadOptions:', error);
			}
		}
	});

	// Initialize on mount (backup approach)
	onMount(() => {
		console.log('🎯 OptionPicker mounted with PURE RUNES - initializing...');

		// Add event listener for start position selection
		const handleStartPositionSelected = () => {
			console.log('🎯 Start position selected - reloading options');
			initializeAndLoadOptions();
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
				<button class="retry-button" onclick={initializeAndLoadOptions}> Retry </button>
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
			<!-- Sectioned scroll area with sophisticated responsive layout using PURE RUNES -->
			<OptionPickerScroll
				pictographs={effectiveOptions}
				onPictographSelected={handlePictographSelected}
				containerWidth={optionPickerState.containerWidth}
				containerHeight={optionPickerState.containerHeight}
				layoutConfig={currentLayoutConfig}
				deviceInfo={enhancedDeviceInfo}
				{foldableInfo}
			/>
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
</style>
