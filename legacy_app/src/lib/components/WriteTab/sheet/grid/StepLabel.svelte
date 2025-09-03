<script lang="ts">
	import { actStore } from '../../stores/actStore';

	export let row: number;
	export let col: number;
	export let label: string = '';

	let isEditing = false;
	let inputElement: HTMLInputElement;
	let currentLabel = label;

	// Update the current label when the prop changes
	$: currentLabel = label;

	function startEditing() {
		isEditing = true;

		// Focus the input after the DOM updates
		setTimeout(() => {
			if (inputElement) {
				inputElement.focus();
				inputElement.select();
			}
		}, 0);
	}

	function saveLabel() {
		actStore.updateBeat(row, col, { step_label: currentLabel });
		isEditing = false;
	}

	function handleKeyDown(event: KeyboardEvent) {
		if (event.key === 'Enter') {
			saveLabel();
		} else if (event.key === 'Escape') {
			// Revert to the original label
			currentLabel = label;
			isEditing = false;
		}
	}

	function handleBlur() {
		saveLabel();
	}

	// Prevent click events from bubbling to the beat cell
	function handleClick(event: MouseEvent | KeyboardEvent) {
		event.stopPropagation();
		startEditing();
	}

	// Handle keyboard events for accessibility
	function handleKeyPress(event: KeyboardEvent) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			handleClick(event);
		}
	}
</script>

<div
	class="step-label"
	on:click={handleClick}
	on:keydown={handleKeyPress}
	tabindex="0"
	role="button"
	aria-label="Edit step label"
>
	{#if isEditing}
		<input
			bind:this={inputElement}
			bind:value={currentLabel}
			on:keydown={handleKeyDown}
			on:blur={handleBlur}
			class="label-input"
			type="text"
			placeholder="Step label"
			on:click={(e) => e.stopPropagation()}
		/>
	{:else}
		<div class="label-text">
			{currentLabel || `Step ${row * 8 + col + 1}`}
		</div>
	{/if}
</div>

<style>
	.step-label {
		position: absolute;
		top: 0;
		left: 0;
		background-color: rgba(0, 0, 0, 0.6);
		padding: 2px 4px;
		border-radius: 0 0 4px 0;
		font-size: 0.75rem;
		color: #ccc;
		z-index: 2;
		cursor: text;
	}

	.label-text {
		max-width: 100px;
		white-space: nowrap;
		overflow: hidden;
		text-overflow: ellipsis;
	}

	.label-input {
		font-size: 0.75rem;
		padding: 2px 4px;
		background-color: #333;
		color: #fff;
		border: 1px solid #555;
		border-radius: 2px;
		width: 100px;
		outline: none;
	}

	.label-input:focus {
		border-color: #3498db;
	}
</style>
