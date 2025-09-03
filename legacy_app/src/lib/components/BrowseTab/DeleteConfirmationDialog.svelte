<!-- src/lib/components/BrowseTab/DeleteConfirmationDialog.svelte -->
<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { fade } from 'svelte/transition';
	import { onMount } from 'svelte';

	// Props
	export let type: 'sequence' | 'variation' = 'variation';
	export let sequenceName: string = '';

	// Create event dispatcher
	const dispatch = createEventDispatcher<{
		confirm: void;
		cancel: void;
	}>();

	// Handle confirm
	function handleConfirm() {
		dispatch('confirm');
	}

	// Handle cancel
	function handleCancel() {
		dispatch('cancel');
	}

	// Handle backdrop click
	function handleBackdropClick(event: MouseEvent) {
		if (event.target === event.currentTarget) {
			handleCancel();
		}
	}

	// Handle keydown for entire component
	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape') {
			handleCancel();
		}
	}

	// Handle keydown for backdrop specifically
	function handleBackdropKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter' || event.key === ' ') {
			handleCancel();
			event.preventDefault();
		}
	}

	let cancelButton: HTMLButtonElement;

	onMount(() => {
		// Set focus to cancel button when dialog opens
		cancelButton?.focus();
	});
</script>

<svelte:window on:keydown={handleKeydown} />

<div
	class="dialog-backdrop"
	on:click={handleBackdropClick}
	on:keydown={handleBackdropKeydown}
	role="presentation"
	transition:fade={{ duration: 200 }}
>
	<div
		class="dialog-container"
		role="dialog"
		aria-labelledby="dialog-title"
		aria-describedby="dialog-description"
		transition:fade={{ duration: 200, delay: 50 }}
	>
		<div class="dialog-header">
			<h2 id="dialog-title" class="dialog-title">Confirm Deletion</h2>
		</div>

		<div class="dialog-content">
			<p id="dialog-description" class="dialog-message">
				{#if type === 'sequence'}
					Are you sure you want to delete the entire sequence "{sequenceName}" and all its
					variations?
					<br /><br />
					<strong>This action cannot be undone.</strong>
				{:else}
					Are you sure you want to delete this variation of "{sequenceName}"?
					<br /><br />
					<strong>This action cannot be undone.</strong>
				{/if}
			</p>
		</div>

		<div class="dialog-actions">
			<button class="dialog-button cancel" on:click={handleCancel} bind:this={cancelButton}>
				Cancel
			</button>

			<button class="dialog-button confirm" on:click={handleConfirm}> Delete </button>
		</div>
	</div>
</div>

<style>
	.dialog-backdrop {
		position: fixed;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: rgba(0, 0, 0, 0.7);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
	}

	.dialog-container {
		width: 90%;
		max-width: 400px;
		background-color: var(--background-color-secondary, #252525);
		border-radius: 8px;
		overflow: hidden;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
	}

	.dialog-header {
		padding: 1rem;
		background-color: var(--danger-color, #ff5555);
		color: white;
	}

	.dialog-title {
		margin: 0;
		font-size: 1.2rem;
		font-weight: 600;
	}

	.dialog-content {
		padding: 1.5rem;
	}

	.dialog-message {
		margin: 0;
		line-height: 1.5;
	}

	.dialog-actions {
		display: flex;
		justify-content: flex-end;
		gap: 1rem;
		padding: 1rem;
		background-color: var(--background-color, #1e1e1e);
	}

	.dialog-button {
		padding: 0.5rem 1rem;
		border: none;
		border-radius: 4px;
		font-weight: 500;
		cursor: pointer;
	}

	.dialog-button.cancel {
		background-color: var(--button-background, #333333);
		color: var(--text-color, #ffffff);
	}

	.dialog-button.confirm {
		background-color: var(--danger-color, #ff5555);
		color: white;
	}

	.dialog-button:hover {
		filter: brightness(1.1);
	}
</style>
