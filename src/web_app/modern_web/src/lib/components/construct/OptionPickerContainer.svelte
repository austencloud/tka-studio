<!--
	OptionPickerContainer.svelte

	Main orchestrator component that leverages existing sophisticated systems:
	- Uses optionPickerRunes.svelte.ts for state management
	- Uses OptionPickerLayoutManager.ts for layout calculations
	- Delegates rendering to existing well-designed sub-components

	This replaces the 562-line monolithic OptionPicker.svelte
-->
<script lang="ts">
	import type { PictographData } from '$lib/domain/PictographData';
	import type { SequenceData } from '$lib/domain/SequenceData';
	import { onMount } from 'svelte';
	// Import sophisticated existing systems
	import { OptionPickerLayoutManager } from './option-picker/OptionPickerLayoutManager';
	import { createOptionPickerRunes } from './option-picker/optionPickerRunes.svelte';
	import { detectFoldableDevice } from './option-picker/utils/deviceDetection';
	import { getEnhancedDeviceType } from './option-picker/utils/layoutUtils';
	// Import well-designed sub-components
	import OptionPickerHeader from './option-picker/OptionPickerHeader.svelte';
	import OptionPickerScroll from './option-picker/OptionPickerScroll.svelte';
	import { resize } from './option-picker/actions/resize';

	// Props
	interface Props {
		currentSequence?: SequenceData | null;
		onOptionSelected?: (option: PictographData) => void;
	}

	let { currentSequence = null, onOptionSelected }: Props = $props();

	// Container dimensions for layout calculations
	let containerWidth = $state(800);
	let containerHeight = $state(600);

	// Use sophisticated state management system
	const optionPickerState = createOptionPickerRunes();

	// Helper to check if preloaded data exists
	const hasPreloadedData = $derived(() => {
		if (typeof window === 'undefined') return false;

		// Check for individual preloaded data
		const preloadedData = localStorage.getItem('preloaded_options');
		if (preloadedData) {
			try {
				const options = JSON.parse(preloadedData);
				return Array.isArray(options) && options.length > 0;
			} catch {
				return false;
			}
		}

		// Check for bulk preloaded data
		const allPreloadedData = localStorage.getItem('all_preloaded_options');
		if (allPreloadedData) {
			try {
				const allOptions = JSON.parse(allPreloadedData);
				return Object.keys(allOptions).length > 0;
			} catch {
				return false;
			}
		}

		return false;
	});

	// Only show loading if we're actually loading AND don't have preloaded data
	const shouldShowLoading = $derived(() => {
		return (
			optionPickerState.isLoading &&
			!hasPreloadedData() &&
			optionPickerState.optionsData.length === 0
		);
	});

	// Derived device and layout information
	const foldableInfo = $derived(() => detectFoldableDevice());
	const deviceInfo = $derived(() => getEnhancedDeviceType(containerWidth, containerWidth < 768));

	// Calculate layout using sophisticated system
	const layoutConfig = $derived(() => {
		return OptionPickerLayoutManager.calculateLayout({
			count: optionPickerState.optionsData.length,
			containerWidth,
			containerHeight,
			windowWidth: containerWidth,
			windowHeight: containerHeight,
			isMobileUserAgent: containerWidth < 768,
		});
	});

	// Reactive access to options data
	const optionsData = $derived(() => optionPickerState.optionsData);
	const error = $derived(() => optionPickerState.error);

	// Handle container resize
	function handleResize(width: number, height: number) {
		containerWidth = width;
		containerHeight = height;
	}

	// Handle option selection
	function handleOptionSelected(option: PictographData) {
		optionPickerState.selectOption(option);
		onOptionSelected?.(option);
	}

	// Helper function to load preloaded data directly into state
	function loadPreloadedData() {
		if (typeof window === 'undefined') return false;

		try {
			// Check for individual preloaded data first
			const preloadedData = localStorage.getItem('preloaded_options');
			if (preloadedData) {
				const options = JSON.parse(preloadedData);
				if (Array.isArray(options) && options.length > 0) {
					console.log('✨ Loading individually preloaded options directly into state');
					optionPickerState.setOptions(options);
					localStorage.removeItem('preloaded_options'); // Clear after use
					return true;
				}
			}

			// Check for bulk preloaded data
			const allPreloadedData = localStorage.getItem('all_preloaded_options');
			if (allPreloadedData) {
				const allOptions = JSON.parse(allPreloadedData);
				console.log('🔍 Available bulk preloaded keys:', Object.keys(allOptions));

				// Determine the current end position we need options for
				let targetEndPosition: string | null = null;
				const startPositionData = localStorage.getItem('start_position');
				if (startPositionData) {
					const startPosition = JSON.parse(startPositionData);
					// Look for endPos in metadata (StartPositionPicker format)
					targetEndPosition =
						startPosition.metadata?.endPos || startPosition.endPos || null;
					console.log('🎯 Looking for end position:', targetEndPosition);
					console.log(
						'📋 Start position data structure:',
						JSON.stringify(startPosition, null, 2)
					);
				}

				// If we have preloaded options for this end position, use them
				if (targetEndPosition && allOptions[targetEndPosition]) {
					const optionsForPosition = allOptions[targetEndPosition];
					console.log(
						`✨ Loading bulk preloaded options for ${targetEndPosition} directly into state`
					);
					optionPickerState.setOptions(optionsForPosition);
					return true;
				} else {
					console.log(
						`❌ No bulk preloaded options found for end position: ${targetEndPosition}`
					);
					console.log('📦 All available bulk keys:', Object.keys(allOptions));
				}
			} else {
				console.log('❌ No bulk preloaded data found in localStorage');
			}
		} catch (error) {
			console.warn('Failed to load preloaded data:', error);
		}

		return false;
	}

	// Handle start position selection events
	function handleStartPositionSelected(event: Event) {
		const customEvent = event as CustomEvent;
		console.log(
			'🎯 OptionPickerContainer received start-position-selected:',
			customEvent.detail
		);

		// Try to load preloaded data first
		if (!loadPreloadedData()) {
			console.log('🎯 No preloaded data for start position change, loading options normally');
			optionPickerState.loadOptions([]); // Empty array loads from start position
		}
	}

	// Initialize on mount
	onMount(() => {
		console.log('🎯 OptionPickerContainer mounted - using sophisticated systems');

		// Add debug logging for localStorage contents
		if (typeof window !== 'undefined') {
			const startPosData = localStorage.getItem('start_position');
			const allPreloadedData = localStorage.getItem('all_preloaded_options');
			console.log('🔍 localStorage DEBUG:');
			console.log('  - start_position:', startPosData ? JSON.parse(startPosData) : null);
			console.log(
				'  - all_preloaded_options keys:',
				allPreloadedData ? Object.keys(JSON.parse(allPreloadedData)) : null
			);
		}

		// Try to load preloaded data first, fallback to normal loading
		if (!loadPreloadedData()) {
			console.log('🎯 No preloaded data found, loading options normally');
			optionPickerState.loadOptions([]); // Empty array loads from start position
		}

		// Listen for start position selection events
		document.addEventListener('start-position-selected', handleStartPositionSelected);

		// Cleanup on unmount
		return () => {
			document.removeEventListener('start-position-selected', handleStartPositionSelected);
		};
	});

	// Reactive loading when sequence changes
	$effect(() => {
		if (currentSequence) {
			console.log('🔄 OptionPickerContainer sequence changed, reloading options');
			// Try to load preloaded data first, fallback to normal loading
			if (!loadPreloadedData()) {
				console.log('🎯 No preloaded data for sequence change, loading options normally');
				optionPickerState.loadOptions([]);
			}
		}
	});
</script>

<!-- Container with resize detection -->
<div
	class="option-picker-container"
	class:mobile={deviceInfo().deviceType === 'mobile' || deviceInfo().deviceType === 'smallMobile'}
	class:tablet={deviceInfo().deviceType === 'tablet'}
	class:foldable={foldableInfo().isFoldable}
	use:resize={handleResize}
	style="--layout-scale-factor: {layoutConfig().scaleFactor}; --option-size: {layoutConfig()
		.optionSize}px; --grid-gap: {layoutConfig().gridGap}px"
>
	<!-- Header -->
	<OptionPickerHeader />

	<!-- Main content area -->
	<div class="content-area">
		{#if shouldShowLoading()}
			<div class="loading-container">
				<div class="loading-spinner"></div>
				<p>Loading options...</p>
				<small>
					Layout: {deviceInfo().deviceType} |
					{foldableInfo().isFoldable ? 'Foldable' : 'Standard'} | Scale: {layoutConfig()
						.scaleFactor}
				</small>
			</div>
		{:else if error()}
			<div class="error-container">
				<p>❌ Error loading options</p>
				<p>{error()}</p>
				<button class="retry-button" onclick={() => optionPickerState.loadOptions([])}>
					Retry
				</button>
			</div>
		{:else if optionsData().length === 0}
			<div class="empty-container">
				<p>No options available</p>
				<p>Please select a start position first</p>
				<small>
					Layout: {layoutConfig().gridColumns} | Device: {deviceInfo().deviceType}
				</small>
			</div>
		{:else}
			<!-- Use existing well-designed scroll component -->
			<OptionPickerScroll
				pictographs={optionsData()}
				onPictographSelected={handleOptionSelected}
				{containerWidth}
				{containerHeight}
				layoutConfig={layoutConfig().layoutConfig}
				deviceInfo={deviceInfo()}
				foldableInfo={foldableInfo()}
			/>
		{/if}
	</div>
</div>

<style>
	.option-picker-container {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
		position: relative;
		border-radius: 8px;
		overflow: hidden;
	}

	.content-area {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}

	.loading-container,
	.error-container,
	.empty-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		flex: 1;
		padding: 2rem;
		text-align: center;
	}

	.loading-spinner {
		width: 40px;
		height: 40px;
		border: 4px solid #f3f3f3;
		border-top: 4px solid #007bff;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: 1rem;
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
		padding: 0.5rem 1rem;
		background: #007bff;
		color: white;
		border: none;
		border-radius: 4px;
		cursor: pointer;
		margin-top: 1rem;
	}

	.retry-button:hover {
		background: #0056b3;
	}

	/* Responsive adjustments */
	.option-picker-container.mobile {
		/* Mobile-specific styles can be added here */
		font-size: 14px;
	}

	.option-picker-container.tablet {
		/* Tablet-specific styles can be added here */
		font-size: 16px;
	}

	.option-picker-container.foldable {
		/* Foldable device styles can be added here */
		transition: all 0.3s ease;
	}
</style>
