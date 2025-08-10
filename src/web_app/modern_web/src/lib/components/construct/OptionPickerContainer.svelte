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

	// Handle start position selection events
	function handleStartPositionSelected(event: CustomEvent) {
		console.log('🎯 OptionPickerContainer received start-position-selected:', event.detail);
		optionPickerState.loadOptions([]); // Empty array loads from start position
	}

	// Initialize on mount
	onMount(() => {
		console.log('🎯 OptionPickerContainer mounted - using sophisticated systems');
		optionPickerState.loadOptions([]); // Empty array loads from start position

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
			// For now, just reload from start position when sequence changes
			optionPickerState.loadOptions([]);
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
	<OptionPickerHeader
		totalOptions={optionPickerState.optionsData.length}
		isLoading={optionPickerState.isLoading}
		deviceInfo={deviceInfo()}
		layoutConfig={layoutConfig()}
	/>

	<!-- Main content area -->
	<div class="content-area">
		{#if optionPickerState.isLoading}
			<div class="loading-container">
				<div class="loading-spinner"></div>
				<p>Loading options...</p>
				<small>
					Layout: {deviceInfo().deviceType} |
					{foldableInfo().isFoldable ? 'Foldable' : 'Standard'} | Scale: {layoutConfig()
						.scaleFactor}
				</small>
			</div>
		{:else if optionPickerState.error}
			<div class="error-container">
				<p>❌ Error loading options</p>
				<p>{optionPickerState.error}</p>
				<button class="retry-button" onclick={() => optionPickerState.loadOptions([])}>
					Retry
				</button>
			</div>
		{:else if optionPickerState.optionsData.length === 0}
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
				pictographs={optionPickerState.optionsData}
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
		background: var(--background-color, #f8f9fa);
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
