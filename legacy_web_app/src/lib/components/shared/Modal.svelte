<script lang="ts">
	import { fade, scale } from 'svelte/transition';

	// Use Svelte 5 props rune
	const props = $props<{
		title?: string;
		isOpen?: boolean;
		showCloseButton?: boolean;
		onClose?: () => void;
		children?: any;
		footer?: any;
	}>();

	// Set default values
	const title = $derived(props.title ?? '');
	const isOpen = $derived(props.isOpen ?? false);
	const showCloseButton = $derived(props.showCloseButton ?? true);

	function close() {
		if (props.onClose) {
			props.onClose();
		}
	}

	function handleBackdropClick(event: MouseEvent) {
		// Only close if the backdrop itself was clicked (not its children)
		if (event.target === event.currentTarget) {
			close();
		}
	}

	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Escape') {
			close();
		}
	}

	// No need for default export in Svelte components
</script>

<svelte:window onkeydown={handleKeydown} />

{#if isOpen}
	<div
		class="modal-backdrop"
		onclick={handleBackdropClick}
		onkeydown={handleKeydown}
		role="dialog"
		aria-modal="true"
		aria-labelledby={title ? 'modal-title' : undefined}
		tabindex="-1"
		transition:fade={{ duration: 200 }}
	>
		<div class="modal-container" transition:scale={{ duration: 200, start: 0.95 }}>
			<div class="modal-header">
				{#if title}
					<h2 class="modal-title" id="modal-title">{title}</h2>
				{/if}

				{#if showCloseButton}
					<button class="close-button" onclick={close} aria-label="Close modal">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							width="20"
							height="20"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						>
							<line x1="18" y1="6" x2="6" y2="18"></line>
							<line x1="6" y1="6" x2="18" y2="18"></line>
						</svg>
					</button>
				{/if}
			</div>

			<div class="modal-content">
				{#if props.children}
					{props.children}
				{/if}
			</div>

			<div class="modal-footer">
				{#if props.footer}
					{props.footer}
				{/if}
			</div>
		</div>
	</div>
{/if}

<style>
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
	}

	.modal-footer {
		display: flex;
		justify-content: flex-end;
		gap: 0.75rem;
		padding: 1rem;
		border-top: 1px solid #333;
	}
</style>
