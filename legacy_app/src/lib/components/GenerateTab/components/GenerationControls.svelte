<script lang="ts">
	import { onMount, onDestroy } from 'svelte';

	// Import the CAPType from the settings store
	import type { CAPType } from '$lib/state/machines/sequenceMachine/types';

	// Assume these child components are available and styled appropriately
	// You would import them from their respective file paths
	// For this example, their basic structure might be included below or assumed
	import GeneratorToggle from './GeneratorToggle.svelte'; // Placeholder, use your actual component
	import LengthSelector from './LengthSelector.svelte'; // Assumed existing
	import TurnIntensity from './TurnIntensity.svelte'; // Assumed existing
	import PropContinuity from './PropContinuity.svelte'; // Assumed existing
	import LevelSelector from './LevelSelector.svelte'; // Assumed existing
	import CircularSequencer from './CircularSequencer.svelte'; // Refactored version below
	import FreeformSequencer from './FreeformSequencer.svelte'; // Refactored version below
	import GenerateButton from './GenerateButton.svelte'; // Assumed existing

	// --- Svelte 5 State ---
	let currentScreenSize = $state<'mobile' | 'tablet' | 'desktop'>('desktop');
	let windowWidth = $state(typeof window !== 'undefined' ? window.innerWidth : 1200);

	// --- XState Integration (Assumed selectors & actions) ---
	// Example: import { sequenceSelectors, sequenceActions } from '$lib/state/machines/sequenceMachine';
	// Mocked for this example
	const mockSequenceSelectors = {
		generationType: () => generatorType,
		isGenerating: () => isGenerating,
		hasError: () => hasError,
		message: () => statusMessage
	};
	const mockSequenceActions = {
		generate: (settings: any, type: string) => {
			console.log('Generate action called with:', settings, type);
			isGenerating = true;
			statusMessage = 'Generating...';
			setTimeout(() => {
				isGenerating = false;
				statusMessage = 'Generation Complete!';
			}, 2000);
		}
	};

	let generatorType = $state<'circular' | 'freeform'>('circular');
	let numBeats = $state<number>(8);
	let turnIntensity = $state<number>(3);
	let propContinuity = $state<'continuous' | 'random'>('continuous');
	let capType = $state<CAPType>('mirrored'); // Using the full CAPType
	let level = $state<number>(3);

	let isGenerating = $state(false);
	let hasError = $state(false);
	let statusMessage = $state('Ready');

	// --- Responsive Layout Logic ---
	function updateScreenSize() {
		windowWidth = window.innerWidth;
		if (windowWidth < 768) {
			currentScreenSize = 'mobile';
		} else if (windowWidth < 1200) {
			currentScreenSize = 'tablet';
		} else {
			currentScreenSize = 'desktop';
		}
	}

	onMount(() => {
		if (typeof window !== 'undefined') {
			updateScreenSize();
			window.addEventListener('resize', updateScreenSize);
		}
	});

	onDestroy(() => {
		if (typeof window !== 'undefined') {
			window.removeEventListener('resize', updateScreenSize);
		}
	});

	// --- Event Handlers ---
	function handleGeneratorTypeChange(newType: string) {
		// Validate that the type is one of the allowed values
		if (newType === 'circular' || newType === 'freeform') {
			generatorType = newType;
			// Potentially send to XState machine if it manages this part of settings
			// settingsStore.setGeneratorType(newType);
		}
	}

	function handleGenerateClick() {
		const settings = {
			numBeats,
			turnIntensity,
			propContinuity,
			capType, // This would be more complex depending on circular/freeform
			level
			// Include generator-specific settings from CircularSequencer/FreeformSequencer if needed
		};
		// Use your actual XState actions
		mockSequenceActions.generate(settings, generatorType);
	}

	const generatorToggleOptions = [
		{ id: 'circular', label: 'Circular', icon: '⭕' },
		{ id: 'freeform', label: 'Freeform', icon: '🔀' }
	];
</script>

<div class="smart-generator-controls layout-{currentScreenSize}">
	<div class="primary-controls-area">
		<section class="control-section generator-type-selector">
			<GeneratorToggle
				options={generatorToggleOptions}
				value={generatorType}
				on:change={(e) => handleGeneratorTypeChange(e.detail)}
			/>
		</section>

		<section
			class="control-section common-parameters {currentScreenSize === 'desktop'
				? 'desktop-grid'
				: ''}"
		>
			<div class="parameter-item">
				<LengthSelector bind:value={numBeats} />
			</div>
			<div class="parameter-item">
				<TurnIntensity bind:value={turnIntensity} />
			</div>
			<div class="parameter-item">
				<PropContinuity bind:value={propContinuity} />
			</div>
			<div class="parameter-item">
				<LevelSelector bind:value={level} />
			</div>
		</section>

		{#if currentScreenSize === 'mobile'}
			<section class="control-section generator-specific-options-mobile">
				{#if generatorType === 'circular'}
					<CircularSequencer
						selectedCapType={capType}
						onCapTypeChange={(newCapType) => (capType = newCapType)}
					/>
				{:else}
					<FreeformSequencer />
				{/if}
			</section>
		{/if}

		<section class="control-section generate-action-area">
			<GenerateButton
				isLoading={mockSequenceSelectors.isGenerating()}
				hasError={mockSequenceSelectors.hasError()}
				statusMessage={mockSequenceSelectors.message()}
				onClick={handleGenerateClick}
			/>
		</section>
	</div>

	{#if currentScreenSize !== 'mobile'}
		<div class="secondary-options-area">
			<section class="control-section generator-specific-options-desktop">
				{#if generatorType === 'circular'}
					<CircularSequencer
						selectedCapType={capType}
						onCapTypeChange={(newCapType) => (capType = newCapType)}
					/>
				{:else}
					<FreeformSequencer />
				{/if}
			</section>
		</div>
	{/if}
</div>

<style>
	/* Global CSS Variables (mimicking your theme) */
	:global(:root) {
		--color-surface-900: rgba(15, 25, 40, 0.95);
		--color-surface-800: rgba(20, 30, 50, 0.7);
		--color-surface-700: rgba(30, 40, 60, 0.5);
		--color-surface-600: rgba(40, 50, 70, 0.7);
		--color-surface-hover: rgba(255, 255, 255, 0.1);
		--color-border: rgba(255, 255, 255, 0.1);
		--color-text-primary: white;
		--color-text-secondary: rgba(255, 255, 255, 0.7);
		--color-accent: #3a7bd5;
		--spacing-md: 1rem; /* Example spacing unit */
		--border-radius-md: 0.5rem;
	}

	.smart-generator-controls {
		display: flex;
		flex-direction: column; /* Mobile-first: single column */
		gap: var(--spacing-md);
		height: 100%;
		padding: var(--spacing-md);
		box-sizing: border-box;
		overflow-y: auto; /* Allow scrolling for the entire controls panel if content overflows */
		background-color: var(--color-surface-900); /* Dark background for the whole panel */
	}

	/* Tablet and Desktop Layout: Two Columns */
	.layout-tablet,
	.layout-desktop {
		flex-direction: row;
		overflow-y: hidden; /* Each column will handle its own scroll */
	}

	.primary-controls-area {
		display: flex;
		flex-direction: column;
		gap: var(--spacing-md);
		flex-grow: 1;
		flex-shrink: 1; /* Allow shrinking */
		min-width: 0; /* Important for flexbox children */
	}

	.layout-tablet .primary-controls-area,
	.layout-desktop .primary-controls-area {
		flex-basis: 50%; /* Adjust basis as needed, e.g., 60% */
		overflow-y: auto; /* This column can scroll if its content is too long */
		padding-right: calc(var(--spacing-md) / 2); /* Gutter between columns */
	}
	.layout-desktop .primary-controls-area {
		flex-basis: 40%; /* More space for options on wide screens */
	}

	.secondary-options-area {
		display: flex;
		flex-direction: column;
		gap: var(--spacing-md);
		flex-grow: 1;
		flex-shrink: 1;
		min-width: 0;
		overflow-y: auto; /* This column can scroll */
	}

	.layout-tablet .secondary-options-area,
	.layout-desktop .secondary-options-area {
		flex-basis: 50%; /* Adjust basis */
		padding-left: calc(var(--spacing-md) / 2);
	}
	.layout-desktop .secondary-options-area {
		flex-basis: 60%;
	}

	/* Styling for individual control sections */
	.control-section {
		background-color: var(--color-surface-800);
		border-radius: var(--border-radius-md);
		padding: var(--spacing-md);
		border: 1px solid var(--color-border);
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.generator-type-selector {
		/* Special styling if needed, e.g., centered toggle */
		display: flex;
		justify-content: center;
	}

	.common-parameters {
		display: flex;
		flex-direction: column; /* Stacked on mobile */
		gap: var(--spacing-md);
	}

	.common-parameters.desktop-grid {
		display: grid;
		grid-template-columns: repeat(2, 1fr); /* 2x2 grid on desktop */
		gap: var(--spacing-md);
	}
	.layout-tablet .common-parameters.desktop-grid {
		/* Also apply grid to tablet */
		display: grid;
		grid-template-columns: repeat(2, 1fr);
		gap: var(--spacing-md);
	}

	.parameter-item {
		/* Styling for individual parameter controls if needed */
		min-width: 0; /* Prevent overflow in grid/flex items */
	}

	.generator-specific-options-mobile,
	.generator-specific-options-desktop {
		display: flex;
		flex-direction: column;
		gap: var(--spacing-md);
		height: 100%; /* Allow child (sequencer) to fill space */
	}
	.generator-specific-options-desktop {
		/* Ensure it can grow if primary controls are shorter */
		flex-grow: 1;
	}

	.generate-action-area {
		/* Ensure button is prominent */
		margin-top: auto; /* Pushes to bottom in mobile view if primary controls scroll */
		padding-top: var(--spacing-md);
	}
	.layout-tablet .generate-action-area,
	.layout-desktop .generate-action-area {
		margin-top: var(--spacing-md); /* Regular spacing in multi-column */
	}

	/* Minimalist Scrollbar for columns */
	.primary-controls-area::-webkit-scrollbar,
	.secondary-options-area::-webkit-scrollbar,
	.smart-generator-controls::-webkit-scrollbar {
		width: 6px;
		height: 6px;
	}
	.primary-controls-area::-webkit-scrollbar-track,
	.secondary-options-area::-webkit-scrollbar-track,
	.smart-generator-controls::-webkit-scrollbar-track {
		background: transparent;
	}
	.primary-controls-area::-webkit-scrollbar-thumb,
	.secondary-options-area::-webkit-scrollbar-thumb,
	.smart-generator-controls::-webkit-scrollbar-thumb {
		background-color: var(--color-accent);
		border-radius: 3px;
	}
	.primary-controls-area,
	.secondary-options-area,
	.smart-generator-controls {
		scrollbar-width: thin;
		scrollbar-color: var(--color-accent) transparent;
	}
</style>
