<!-- src/lib/components/GenerateTab/ui/LengthSelector.svelte -->
<script lang="ts">
	import { settingsStore } from '../store/settings';

	// Export the value property for binding
	export let value: number = 8;

	// Constants
	const MIN_BEATS = 1;
	const MAX_BEATS = 32;

	// Local state for input validation
	let inputValue = value.toString();

	// Update the input value when the value prop changes
	$: {
		inputValue = value.toString();
	}

	// Handle increment
	function increment() {
		if (value < MAX_BEATS) {
			value = value + 1;
			settingsStore.setNumBeats(value);
		}
	}

	// Handle decrement
	function decrement() {
		if (value > MIN_BEATS) {
			value = value - 1;
			settingsStore.setNumBeats(value);
		}
	}

	// Handle direct input
	function handleInput(e: Event) {
		const target = e.target as HTMLInputElement;
		inputValue = target.value;
	}

	// Process input on blur or enter key
	function processInput() {
		const parsed = parseInt(inputValue, 10);

		if (isNaN(parsed)) {
			// Reset to current value if invalid
			inputValue = value.toString();
			return;
		}

		// Clamp within range
		const clamped = Math.max(MIN_BEATS, Math.min(MAX_BEATS, parsed));
		value = clamped;
		settingsStore.setNumBeats(clamped);
	}

	// Handle keydown events
	function handleKeyDown(e: KeyboardEvent) {
		if (e.key === 'Enter') {
			processInput();
			(e.target as HTMLInputElement).blur();
		}
	}
</script>

<div class="length-selector">
	<label for="beat-length">Sequence Length</label>

	<div class="control-group">
		<button
			class="control-button decrement"
			on:click={decrement}
			disabled={value <= MIN_BEATS}
			aria-label="Decrease beats"
		>
			-
		</button>

		<input
			id="beat-length"
			type="text"
			class="beat-input"
			value={inputValue}
			on:input={handleInput}
			on:blur={processInput}
			on:keydown={handleKeyDown}
			min={MIN_BEATS}
			max={MAX_BEATS}
			aria-label="Number of beats"
		/>

		<button
			class="control-button increment"
			on:click={increment}
			disabled={value >= MAX_BEATS}
			aria-label="Increase beats"
		>
			+
		</button>
	</div>

	<div class="range">
		<span class="min">{MIN_BEATS}</span>
		<input type="range" min={MIN_BEATS} max={MAX_BEATS} bind:value class="range-input" />
		<span class="max">{MAX_BEATS}</span>
	</div>
</div>

<style>
	.length-selector {
		display: flex;
		flex-direction: column;
		gap: 0.5rem;
	}

	label {
		font-size: 0.875rem;
		font-weight: 500;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
	}

	.control-group {
		display: flex;
		align-items: center;
		gap: 0.25rem;
	}

	.control-button {
		background: var(--color-surface, rgba(30, 40, 60, 0.85));
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
		background: var(--color-surface-hover, rgba(255, 255, 255, 0.15));
	}

	.control-button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.beat-input {
		background: var(--color-input-bg, rgba(20, 30, 50, 0.6));
		border: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
		color: var(--color-text-primary, white);
		padding: 0.5rem;
		border-radius: 0.25rem;
		font-size: 1rem;
		text-align: center;
		width: 3rem;
	}

	.range {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		margin-top: 0.25rem;
	}

	.min,
	.max {
		font-size: 0.75rem;
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.5));
	}

	.range-input {
		flex: 1;
		height: 0.25rem;
		-webkit-appearance: none;
		appearance: none;
		background: var(--color-surface, rgba(30, 40, 60, 0.85));
		border-radius: 0.125rem;
		cursor: pointer;
	}

	.range-input::-webkit-slider-thumb {
		-webkit-appearance: none;
		width: 0.75rem;
		height: 0.75rem;
		border-radius: 50%;
		background: var(--color-accent, #3a7bd5);
		cursor: pointer;
	}

	.range-input::-moz-range-thumb {
		width: 0.75rem;
		height: 0.75rem;
		border-radius: 50%;
		background: var(--color-accent, #3a7bd5);
		cursor: pointer;
		border: none;
	}
</style>
