<script lang="ts">
	import Modal from './Modal.svelte';
	import { uiStore } from '../../components/WriteTab/stores/uiStore';

	// Define props with the correct Svelte 5 rune syntax
	// Each prop is defined individually
	const isOpen = $props(false);
	const title = $props('Confirm Action');
	const message = $props('Are you sure you want to proceed?');
	const confirmText = $props('Confirm');
	const cancelText = $props('Cancel');
	const confirmButtonClass = $props('danger');
	const showDontAskOption = $props(true);
	const onConfirm = $props<((event: { dontAskAgain: boolean }) => void) | undefined>(undefined);
	const onClose = $props<(() => void) | undefined>(undefined);

	// Component state
	let dontAskAgain = $state(false);

	function handleConfirm() {
		if (dontAskAgain && showDontAskOption) {
			uiStore.toggleConfirmDeletions(false);
		}

		// Call the onConfirm callback if provided
		if (onConfirm) {
			onConfirm({ dontAskAgain });
		}

		close();
	}

	function close() {
		// Reset the checkbox when closing
		dontAskAgain = false;

		// Call the onClose callback if provided
		if (onClose) {
			onClose();
		}
	}
</script>

<Modal {isOpen} {title} onClose={close}>
	<!-- Use the default slot for content -->
	<div class="confirmation-content">
		<p>{message}</p>

		{#if showDontAskOption}
			<label class="dont-ask-option">
				<input type="checkbox" bind:checked={dontAskAgain} />
				<span>Don't ask me again</span>
			</label>
		{/if}
	</div>

	<!-- Use a named slot for the footer -->
	<div class="modal-footer-buttons" slot="footer">
		<button class="cancel-button" on:click={close}>
			{cancelText}
		</button>
		<button class="confirm-button {confirmButtonClass}" on:click={handleConfirm}>
			{confirmText}
		</button>
	</div>
</Modal>

<style>
	.confirmation-content {
		display: flex;
		flex-direction: column;
		gap: 1rem;
	}

	p {
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

	.confirm-button.primary {
		background-color: #3498db;
	}

	.confirm-button.primary:hover {
		background-color: #2980b9;
	}

	.confirm-button.secondary {
		background-color: #2ecc71;
	}

	.confirm-button.secondary:hover {
		background-color: #27ae60;
	}
</style>
