<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { selectionStore, selectedBeat } from '../../stores/selectionStore';
	import { actStore } from '../../stores/actStore';
	import { uiStore } from '../../stores/uiStore';
	import ConfirmationModal from '../../../shared/ConfirmationModal.svelte';
	import type { Beat } from '../../models/Act';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { browser } from '$app/environment';

	export let row: number;
	export let col: number;
	export let beat: Beat | undefined = undefined;

	const dispatch = createEventDispatcher();

	// Modal state
	let isEraseBeatModalOpen = false;

	// Determine if this cell is selected
	$: isSelected = $selectedBeat?.row === row && $selectedBeat?.col === col;

	// Determine if this cell has content
	$: isFilled = beat?.is_filled || !!beat?.pictograph_data;

	// Handle click events
	function handleClick() {
		// Provide haptic feedback when selecting a beat
		if (browser) {
			hapticFeedbackService.trigger('selection');
		}

		dispatch('click', { row, col });
	}

	// Handle erase click
	function handleEraseClick(event: MouseEvent) {
		event.stopPropagation(); // Prevent selection

		// Provide warning haptic feedback for deletion
		if (browser) {
			hapticFeedbackService.trigger('warning');
		}

		if ($uiStore.preferences.confirmDeletions) {
			isEraseBeatModalOpen = true;
		} else {
			actStore.eraseBeat(row, col);
		}
	}

	// Handle confirmation from modal
	function confirmEraseBeat() {
		// Provide warning haptic feedback for confirmed deletion
		if (browser) {
			hapticFeedbackService.trigger('warning');
		}

		actStore.eraseBeat(row, col);
		isEraseBeatModalOpen = false;
	}

	// Generate beat number for display
	$: beatNumber = beat?.beat_number || row * 8 + col + 1;
</script>

<div
	class="beat-cell"
	class:filled={isFilled}
	class:selected={isSelected}
	data-row={row}
	data-col={col}
	on:click={handleClick}
	on:keydown={(e) => e.key === 'Enter' && handleClick()}
	tabindex="0"
	role="button"
	aria-label={`Beat ${beatNumber}`}
>
	{#if isFilled}
		<div class="beat-content">
			<!-- Placeholder for pictograph visualization -->
			<div class="pictograph-placeholder">
				<span class="beat-number">{beatNumber}</span>
				<button class="erase-button" on:click={handleEraseClick} aria-label="Erase beat">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="12"
						height="12"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					>
						<path d="M3 6h18"></path>
						<path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
						<path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
						<line x1="10" y1="11" x2="10" y2="17"></line>
						<line x1="14" y1="11" x2="14" y2="17"></line>
					</svg>
				</button>
			</div>
		</div>
	{:else}
		<div class="empty-cell">
			<span class="beat-number">{beatNumber}</span>
		</div>
	{/if}
</div>

<ConfirmationModal
	isOpen={isEraseBeatModalOpen}
	title="Erase Beat"
	message={`Are you sure you want to erase beat ${beatNumber}?`}
	confirmText="Erase"
	cancelText="Cancel"
	confirmButtonClass="danger"
	on:confirm={confirmEraseBeat}
	on:close={() => (isEraseBeatModalOpen = false)}
/>

<style>
	.beat-cell {
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		background-color: #222;
		border-radius: 4px;
		cursor: pointer;
		transition:
			background-color 0.2s,
			transform 0.1s;
		user-select: none;
	}

	.beat-cell:hover {
		background-color: #2a2a2a;
	}

	.beat-cell.filled {
		background-color: #2c3e50;
	}

	.beat-cell.filled:hover {
		background-color: #34495e;
	}

	.beat-cell.selected {
		background-color: #2980b9;
		transform: scale(0.95);
		box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.5);
		z-index: 1;
	}

	.beat-content {
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.pictograph-placeholder {
		width: 90%;
		height: 90%;
		background-color: #3498db;
		border-radius: 4px;
		display: flex;
		align-items: center;
		justify-content: center;
		color: white;
		font-weight: bold;
		position: relative; /* For absolute positioning of beat number */
	}

	.empty-cell {
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
		color: #555;
	}

	.beat-number {
		font-size: clamp(0.6rem, 1vw, 1rem); /* Responsive font size */
		opacity: 0.7;
		position: absolute;
		top: 4px;
		left: 4px;
		background-color: transparent; /* Transparent background */
	}

	.erase-button {
		position: absolute;
		top: 4px;
		right: 4px;
		width: 20px;
		height: 20px;
		border-radius: 50%;
		background-color: rgba(0, 0, 0, 0.3);
		border: none;
		color: white;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		opacity: 0;
		transition:
			opacity 0.2s,
			background-color 0.2s;
	}

	.pictograph-placeholder:hover .erase-button {
		opacity: 1;
	}

	.erase-button:hover {
		background-color: rgba(231, 76, 60, 0.8);
	}
</style>
