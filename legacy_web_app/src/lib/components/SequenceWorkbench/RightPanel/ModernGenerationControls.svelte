<!-- src/lib/components/SequenceWorkbench/RightPanel/ModernGenerationControls.svelte -->
<script lang="ts">
	import { sequenceActions, sequenceSelectors } from '$lib/state/machines/sequenceMachine';
	import { settingsStore, type CAPType } from '$lib/state/stores/settingsStore';
	import GenerateButton from '$lib/components/GenerateTab/components/GenerateButton.svelte';
	import CircularSequencer from '$lib/components/GenerateTab/components/CircularSequencer.svelte';
	import FreeformSequencer from '$lib/components/GenerateTab/components/FreeformSequencer.svelte';

	// Generator types for the toggle
	const generatorTypes = [
		{ id: 'circular', label: 'Circular' },
		{ id: 'freeform', label: 'Freeform' }
	];

	// Constants for intensity and beats
	const MIN_INTENSITY = 1;
	const MAX_INTENSITY = 5;
	const MIN_BEATS = 1;
	const MAX_BEATS = 32;

	// Labels for the intensity levels
	const intensityLabels = ['Minimal', 'Light', 'Moderate', 'Heavy', 'Extreme'];

	// Prop continuity options
	const continuityOptions = [
		{ id: 'continuous', label: 'Continuous' },
		{ id: 'random', label: 'Random' }
	];

	// State using Svelte 5 runes
	const generatorType = $derived(sequenceSelectors.generationType());
	const isGenerating = $derived(sequenceSelectors.isGenerating());
	const hasError = $derived(sequenceSelectors.hasError());
	const statusMessage = $derived(sequenceSelectors.message());

	// Get settings values using mutable state
	let numBeats = $state(8); // Default value
	let turnIntensity = $state(3); // Default value
	let propContinuity = $state<'continuous' | 'random'>('continuous'); // Default value
	let capType = $state<CAPType>('mirrored'); // Updated to use correct CAPType
	let level = $state<number>(3); // Default value (1-5)

	// Sync with settings store
	$effect(() => {
		// Get current settings from the store
		const settings = settingsStore.getSnapshot();
		numBeats = settings.numBeats;
		turnIntensity = settings.turnIntensity;
		propContinuity = settings.propContinuity;
		capType = settings.capType; // No need to cast since types match
		level = settings.level;
	});

	// Computed values
	const currentIntensityLabel = $derived(intensityLabels[turnIntensity - 1] || 'Moderate');

	// Input handling for beats
	let inputValue = $state('8');

	$effect(() => {
		inputValue = numBeats.toString();
	});

	// Handle generator type change
	function handleGeneratorTypeChange(type: string) {
		settingsStore.setGeneratorType(type as 'circular' | 'freeform');
	}

	// Handle beats change
	function incrementBeats() {
		if (numBeats < MAX_BEATS) {
			settingsStore.setNumBeats(numBeats + 1);
		}
	}

	function decrementBeats() {
		if (numBeats > MIN_BEATS) {
			settingsStore.setNumBeats(numBeats - 1);
		}
	}

	function handleBeatsInput(e: Event) {
		const target = e.target as HTMLInputElement;
		inputValue = target.value;
	}

	function processBeatsInput() {
		const parsed = parseInt(inputValue, 10);

		if (isNaN(parsed)) {
			inputValue = numBeats.toString();
			return;
		}

		const clamped = Math.max(MIN_BEATS, Math.min(MAX_BEATS, parsed));
		settingsStore.setNumBeats(clamped);
	}

	function handleBeatsKeyDown(e: KeyboardEvent) {
		if (e.key === 'Enter') {
			processBeatsInput();
			(e.target as HTMLInputElement).blur();
		}
	}

	// Handle intensity change
	function setIntensity(level: number) {
		if (level >= MIN_INTENSITY && level <= MAX_INTENSITY) {
			settingsStore.setTurnIntensity(level);
		}
	}

	// Handle prop continuity toggle
	function toggleContinuity() {
		const newValue = propContinuity === 'continuous' ? 'random' : 'continuous';
		settingsStore.setPropContinuity(newValue);
	}

	// Handle level change
	function setLevel(newLevel: number) {
		if (newLevel >= 1 && newLevel <= 5) {
			settingsStore.setLevel(newLevel);
		}
	}

	// Handle generate click
	function handleGenerate() {
		// Get current settings
		const settings = {
			numBeats,
			turnIntensity,
			propContinuity,
			capType,
			level
		};

		// Use the sequence machine to generate the sequence
		sequenceActions.generate(generatorType, settings);
	}
</script>

<div class="modern-generation-controls">
	<!-- Generator Type Toggle -->
	<div class="generator-type-container">
		<div class="generator-toggle-wrapper">
			<button
				class="generator-type-button"
				class:active={generatorType === 'circular'}
				onclick={() => handleGeneratorTypeChange('circular')}
			>
				<span class="generator-icon">⭕</span>
				<span>Circular</span>
			</button>
			<button
				class="generator-type-button"
				class:active={generatorType === 'freeform'}
				onclick={() => handleGeneratorTypeChange('freeform')}
			>
				<span class="generator-icon">🔀</span>
				<span>Freeform</span>
			</button>
		</div>
	</div>

	<!-- Main Controls Grid -->
	<div class="controls-grid">
		<!-- Sequence Length -->
		<div class="control-card">
			<label for="beat-length">Sequence Length</label>
			<div class="control-group">
				<button
					class="control-button decrement"
					onclick={decrementBeats}
					disabled={numBeats <= MIN_BEATS}
					aria-label="Decrease beats"
				>
					-
				</button>
				<input
					id="beat-length"
					type="text"
					class="beat-input"
					value={inputValue}
					oninput={handleBeatsInput}
					onblur={processBeatsInput}
					onkeydown={handleBeatsKeyDown}
					min={MIN_BEATS}
					max={MAX_BEATS}
					aria-label="Number of beats"
				/>
				<button
					class="control-button increment"
					onclick={incrementBeats}
					disabled={numBeats >= MAX_BEATS}
					aria-label="Increase beats"
				>
					+
				</button>
			</div>
		</div>

		<!-- Turn Intensity -->
		<div class="control-card">
			<div class="control-header">
				<label for="turn-intensity">Turn Intensity</label>
				<span class="current-level">{currentIntensityLabel}</span>
			</div>
			<div id="turn-intensity" class="intensity-buttons">
				{#each Array(MAX_INTENSITY) as _, i}
					{@const level = i + 1}
					<button
						class="intensity-button"
						class:active={turnIntensity === level}
						onclick={() => setIntensity(level)}
						aria-label="Set turn intensity to {intensityLabels[i]}"
						aria-pressed={turnIntensity === level}
					>
						{level}
					</button>
				{/each}
			</div>
		</div>

		<!-- Prop Continuity -->
		<div class="control-card">
			<label for="prop-continuity-toggle">Prop Continuity</label>
			<div class="toggle-control">
				<button
					id="prop-continuity-toggle"
					type="button"
					class="toggle-track"
					onclick={toggleContinuity}
					aria-label="Toggle Prop Continuity"
				>
					<div class="toggle-labels">
						{#each continuityOptions as option}
							<span class="toggle-label" class:selected={option.id === propContinuity}>
								{option.label}
							</span>
						{/each}
					</div>
					<div class="toggle-thumb" class:right={propContinuity === 'random'}></div>
				</button>
			</div>
			<div class="description">
				{#if propContinuity === 'continuous'}
					<p>Props maintain rotation direction</p>
				{:else}
					<p>Props may change rotation direction</p>
				{/if}
			</div>
		</div>

		<!-- Level Selector -->
		<div class="control-card">
			<label for="complexity-level">Complexity Level</label>
			<div id="complexity-level" class="level-buttons" role="radiogroup">
				<button class="level-button" class:active={level === 1} onclick={() => setLevel(1)}>
					Beginner
				</button>
				<button class="level-button" class:active={level === 3} onclick={() => setLevel(3)}>
					Intermediate
				</button>
				<button class="level-button" class:active={level === 5} onclick={() => setLevel(5)}>
					Advanced
				</button>
			</div>
		</div>
	</div>

	<!-- Generator Options -->
	<div class="generator-options">
		{#if generatorType === 'circular'}
			<CircularSequencer />
		{:else}
			<FreeformSequencer />
		{/if}
	</div>

	<!-- Generate Button -->
	<div class="generate-button-container">
		<GenerateButton isLoading={isGenerating} {hasError} {statusMessage} onClick={handleGenerate} />
	</div>
</div>

<style>
	.modern-generation-controls {
		display: flex;
		flex-direction: column;
		gap: 1rem;
		padding: 1rem;
		height: 100%;
		overflow-y: auto;
	}

	/* Generator Type Toggle */
	.generator-type-container {
		display: flex;
		justify-content: center;
		margin-bottom: 0.5rem;
	}

	.generator-toggle-wrapper {
		display: flex;
		background: var(--color-surface-800, rgba(20, 30, 50, 0.7));
		border-radius: 0.5rem;
		padding: 0.25rem;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.generator-type-button {
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.5rem;
		padding: 0.5rem 1rem;
		border: none;
		background: transparent;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
		border-radius: 0.375rem;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.generator-type-button.active {
		background: var(--color-accent, #3a7bd5);
		color: white;
	}

	.generator-icon {
		font-size: 1rem;
	}

	/* Controls Grid */
	.controls-grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
		gap: 1rem;
	}

	.control-card {
		background: var(--color-surface-700, rgba(30, 40, 60, 0.5));
		border-radius: 0.5rem;
		padding: 0.75rem;
		border: 1px solid rgba(255, 255, 255, 0.05);
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	label {
		font-size: 0.875rem;
		font-weight: 500;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
	}

	/* Sequence Length */
	.control-group {
		display: flex;
		align-items: center;
		gap: 0.25rem;
	}

	.control-button {
		background: var(--color-surface-800, rgba(20, 30, 50, 0.7));
		border: none;
		color: var(--color-text-primary, white);
		width: 2rem;
		height: 2rem;
		border-radius: 0.25rem;
		font-size: 1.25rem;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition: all 0.15s ease;
	}

	.control-button:hover:not(:disabled) {
		background: var(--color-accent, #3a7bd5);
	}

	.control-button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.beat-input {
		background: var(--color-surface-800, rgba(20, 30, 50, 0.7));
		border: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
		color: var(--color-text-primary, white);
		padding: 0.5rem;
		border-radius: 0.25rem;
		font-size: 1rem;
		text-align: center;
		width: 3rem;
	}

	/* Turn Intensity */
	.control-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
	}

	.current-level {
		font-size: 0.75rem;
		color: var(--color-text-primary, white);
		background: var(--color-surface-800, rgba(20, 30, 50, 0.7));
		padding: 0.125rem 0.5rem;
		border-radius: 1rem;
	}

	.intensity-buttons {
		display: flex;
		gap: 0.25rem;
		justify-content: space-between;
	}

	.intensity-button {
		flex: 1;
		background: var(--color-surface-800, rgba(20, 30, 50, 0.7));
		border: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
		border-radius: 0.25rem;
		padding: 0.5rem 0;
		cursor: pointer;
		transition: all 0.2s ease;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
	}

	.intensity-button:hover {
		background: var(--color-surface-hover, rgba(255, 255, 255, 0.1));
	}

	.intensity-button.active {
		background: var(--color-accent, #3a7bd5);
		border-color: var(--color-accent, #3a7bd5);
		color: white;
	}

	/* Prop Continuity */
	.toggle-control {
		display: flex;
		align-items: center;
	}

	.toggle-track {
		position: relative;
		width: 100%;
		height: 2rem;
		background: var(--color-surface-800, rgba(20, 30, 50, 0.7));
		border: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
		border-radius: 1rem;
		cursor: pointer;
		transition: background-color 0.2s ease;
		overflow: hidden;
	}

	.toggle-labels {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: space-between;
		z-index: 1;
	}

	.toggle-label {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
		font-size: 0.75rem;
		font-weight: 500;
		transition: color 0.2s ease;
	}

	.toggle-label.selected {
		color: var(--color-text-primary, white);
	}

	.toggle-thumb {
		position: absolute;
		top: 0.125rem;
		left: 0.125rem;
		width: calc(50% - 0.25rem);
		height: calc(100% - 0.25rem);
		background: var(--color-accent, #3a7bd5);
		border-radius: 0.875rem;
		transition: transform 0.2s ease;
		z-index: 0;
	}

	.toggle-thumb.right {
		transform: translateX(calc(100% + 0.25rem));
	}

	.description {
		font-size: 0.75rem;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.6));
		opacity: 0.8;
	}

	.description p {
		margin: 0;
	}

	/* Level Selector */
	.level-buttons {
		display: flex;
		gap: 0.25rem;
	}

	.level-button {
		flex: 1;
		background: var(--color-surface-800, rgba(20, 30, 50, 0.7));
		border: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
		border-radius: 0.25rem;
		padding: 0.5rem 0;
		font-size: 0.75rem;
		cursor: pointer;
		transition: all 0.2s ease;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
	}

	.level-button:hover {
		background: var(--color-surface-hover, rgba(255, 255, 255, 0.1));
	}

	.level-button.active {
		background: var(--color-accent, #3a7bd5);
		border-color: var(--color-accent, #3a7bd5);
		color: white;
	}

	/* Generator Options */
	.generator-options {
		background: var(--color-surface-700, rgba(30, 40, 60, 0.5));
		border-radius: 0.5rem;
		padding: 0.75rem;
		border: 1px solid rgba(255, 255, 255, 0.05);
		overflow-y: auto;
	}

	/* Generate Button */
	.generate-button-container {
		padding: 1rem;
		background: linear-gradient(
			135deg,
			var(--color-surface-800, rgba(20, 30, 50, 0.7)),
			var(--color-surface-700, rgba(30, 40, 60, 0.7))
		);
		border-radius: 0.5rem;
		border: 1px solid rgba(255, 255, 255, 0.05);
		display: flex;
		justify-content: center;
	}

	/* Scrollbar styling */
	.modern-generation-controls::-webkit-scrollbar {
		width: 4px;
	}

	.modern-generation-controls::-webkit-scrollbar-track {
		background: transparent;
	}

	.modern-generation-controls::-webkit-scrollbar-thumb {
		background-color: var(--color-accent, #3a7bd5);
		border-radius: 2px;
	}

	/* Firefox scrollbar */
	.modern-generation-controls {
		scrollbar-width: thin;
		scrollbar-color: var(--color-accent, #3a7bd5) transparent;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.controls-grid {
			grid-template-columns: 1fr;
		}
	}

	/* Touch device optimizations */
	@media (hover: none) {
		.control-button:active,
		.intensity-button:active,
		.level-button:active,
		.generator-type-button:active {
			transform: scale(0.95);
		}
	}
</style>
