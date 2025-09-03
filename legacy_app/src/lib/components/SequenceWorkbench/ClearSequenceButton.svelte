<!-- src/lib/components/SequenceWorkbench/ClearSequenceButton.svelte -->
<script lang="ts">
	import { fly, fade, scale } from 'svelte/transition';
	import { browser } from '$app/environment';
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { sequenceActions } from '$lib/state/machines/sequenceMachine';

	// User preference for confirmation dialogs
	let showConfirmation = $state(true);
	let isConfirmationModalOpen = $state(false);
	let dontAskAgain = $state(false);

	// Load user preference from localStorage
	$effect(() => {
		if (browser) {
			try {
				const savedPreference = localStorage.getItem('confirm_sequence_clear');
				if (savedPreference !== null) {
					showConfirmation = savedPreference === 'true';
				}
			} catch (error) {
				console.error('Error loading confirmation preference:', error);
			}
		}
	});

	// Save user preference to localStorage
	function savePreference(value: boolean) {
		if (browser) {
			try {
				localStorage.setItem('confirm_sequence_clear', value.toString());
				showConfirmation = value;
			} catch (error) {
				console.error('Error saving confirmation preference:', error);
			}
		}
	}

	function handleClick() {
		// Provide haptic feedback
		if (browser) {
			hapticFeedbackService.trigger('warning');
		}

		// Check if we should show confirmation
		if (showConfirmation) {
			isConfirmationModalOpen = true;
		} else {
			clearSequence();
		}
	}

	function clearSequence() {
		// Clear the sequence directly using the sequence actions
		sequenceActions.clearSequence();

		// Provide haptic feedback for deletion
		if (browser) {
			hapticFeedbackService.trigger('error');
		}
	}

	function handleConfirm() {
		// Save the user preference if "Don't ask again" is checked
		if (dontAskAgain) {
			savePreference(false);
		}

		// Clear the sequence
		clearSequence();

		// Close the modal
		closeModal();
	}

	function closeModal() {
		isConfirmationModalOpen = false;
		// Reset the checkbox
		dontAskAgain = false;
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape' && isConfirmationModalOpen) {
			closeModal();
		}
	}
</script>

<svelte:window onkeydown={handleKeydown} />

<button
	class="clear-button ripple"
	onclick={handleClick}
	aria-label="Clear sequence"
	data-mdb-ripple="true"
	data-mdb-ripple-color="light"
	in:fly={{ x: -20, duration: 300, delay: 200 }}
>
	<div class="icon-wrapper">
		<i class="fa-solid fa-eraser"></i>
	</div>
</button>

{#if isConfirmationModalOpen}
	<div
		class="modal-backdrop"
		onclick={(e) => e.target === e.currentTarget && closeModal()}
		onkeydown={(e) => e.key === 'Escape' && closeModal()}
		role="dialog"
		aria-modal="true"
		aria-labelledby="modal-title"
		tabindex="-1"
		transition:fade={{ duration: 200 }}
	>
		<div class="modal-container" transition:scale={{ duration: 200, start: 0.95 }}>
			<div class="modal-header">
				<h2 class="modal-title" id="modal-title">Clear Sequence</h2>
				<button class="close-button" onclick={closeModal} aria-label="Close modal">
					<i class="fa-solid fa-times"></i>
				</button>
			</div>

			<div class="modal-content">
				<p>
					Are you sure you want to clear the entire sequence? This will remove all beats and reset
					the start position.
				</p>

				<label class="dont-ask-option">
					<input type="checkbox" bind:checked={dontAskAgain} />
					<span>Don't ask me again</span>
				</label>
			</div>

			<div class="modal-footer">
				<button class="cancel-button" onclick={closeModal}> Cancel </button>
				<button class="confirm-button danger" onclick={handleConfirm}> Clear </button>
			</div>
		</div>
	</div>
{/if}

<style>
	/* Modal styles */
	.modal-backdrop {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.7);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 1000;
		backdrop-filter: blur(2px);
	}

	.modal-container {
		background-color: #2a2a2a;
		border-radius: 8px;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
		width: 90%;
		max-width: 500px;
		max-height: 90vh;
		display: flex;
		flex-direction: column;
		overflow: hidden;
	}

	.modal-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: 1rem;
		border-bottom: 1px solid #333;
	}

	.modal-title {
		margin: 0;
		font-size: 1.25rem;
		color: #e0e0e0;
		font-weight: 600;
	}

	.close-button {
		background: none;
		border: none;
		color: #999;
		cursor: pointer;
		padding: 0.25rem;
		border-radius: 4px;
		display: flex;
		align-items: center;
		justify-content: center;
		transition:
			color 0.2s,
			background-color 0.2s;
	}

	.close-button:hover {
		color: #fff;
		background-color: rgba(255, 255, 255, 0.1);
	}

	.modal-content {
		padding: 1.5rem;
		overflow-y: auto;
		color: #e0e0e0;
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	.modal-content p {
		margin: 0;
		line-height: 1.5;
	}

	.dont-ask-option {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		font-size: 0.875rem;
		color: #999;
		cursor: pointer;
		user-select: none;
	}

	.dont-ask-option input[type='checkbox'] {
		width: 16px;
		height: 16px;
		cursor: pointer;
	}

	.modal-footer {
		display: flex;
		justify-content: flex-end;
		gap: 0.75rem;
		padding: 1rem;
		border-top: 1px solid #333;
	}

	.cancel-button,
	.confirm-button {
		padding: 0.5rem 1rem;
		border-radius: 4px;
		font-size: 0.875rem;
		font-weight: 500;
		cursor: pointer;
		transition: background-color 0.2s;
		border: none;
	}

	.cancel-button {
		background-color: #3a3a3a;
		color: #e0e0e0;
	}

	.cancel-button:hover {
		background-color: #4a4a4a;
	}

	.confirm-button {
		color: white;
	}

	.confirm-button.danger {
		background-color: #e74c3c;
	}

	.confirm-button.danger:hover {
		background-color: #c0392b;
	}
	.clear-button {
		/* Define base sizes for dynamic scaling */
		--base-size: 45px; /* Base size of the button (was 56px) */
		--base-icon-size: 19px; /* Base size of the icon (was 24px) */
		--base-margin: 10px; /* Define base margin to match ToolsButton */

		position: absolute;
		/* Bottom inset is important as it affects the entire bottom edge */
		bottom: max(
			calc(var(--button-size-factor, 1) * var(--base-margin)),
			var(--safe-inset-bottom, 0px)
		);
		/* Left inset is rarely needed for corner buttons */
		left: calc(var(--button-size-factor, 1) * var(--base-margin));
		width: calc(var(--button-size-factor, 1) * var(--base-size)); /* Dynamic width */
		height: calc(var(--button-size-factor, 1) * var(--base-size)); /* Dynamic height */
		min-width: 38px; /* Minimum width to match ToolsButton (was 48px) */
		min-height: 38px; /* Minimum height to match ToolsButton (was 48px) */
		background-color: var(--tkc-button-panel-background, #2a2a2e); /* Dark background */
		border-radius: 50%; /* Perfectly round */
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition:
			transform 0.2s ease-out,
			background-color 0.2s ease-out,
			box-shadow 0.2s ease-out;
		z-index: 40; /* Ensure it's above most content but potentially below modals/side panels */
		box-shadow:
			0 3px 6px rgba(0, 0, 0, 0.16),
			0 3px 6px rgba(0, 0, 0, 0.23);
		border: none; /* Remove any default button border */
		padding: 0; /* Remove padding, icon centered by flex */
		color: var(--tkc-icon-color-orange, orange); /* Icon color */
		pointer-events: auto; /* Ensure it's clickable */
	}

	.clear-button:hover {
		background-color: var(
			--tkc-button-panel-background-hover,
			#3c3c41
		); /* Slightly lighter on hover */
		transform: translateY(-2px) scale(1.05);
		box-shadow:
			0 6px 12px rgba(0, 0, 0, 0.2),
			0 4px 8px rgba(0, 0, 0, 0.26);
	}

	.clear-button:active {
		transform: translateY(0px) scale(1); /* Click down effect */
		background-color: var(--tkc-button-panel-background-active, #1e1e21); /* Darker when pressed */
		box-shadow:
			0 1px 3px rgba(0, 0, 0, 0.12),
			0 1px 2px rgba(0, 0, 0, 0.24);
	}

	.icon-wrapper {
		background: transparent; /* Ensure wrapper doesn't obscure button background */
		display: flex;
		align-items: center;
		justify-content: center;
		width: auto;
		height: auto;
		color: inherit; /* Inherit color from .clear-button (orange) */
	}

	.icon-wrapper i.fa-eraser {
		font-size: calc(var(--button-size-factor, 1) * var(--base-icon-size)); /* Dynamic icon size */
		/* Color is inherited from .clear-button via .icon-wrapper */
	}
</style>
