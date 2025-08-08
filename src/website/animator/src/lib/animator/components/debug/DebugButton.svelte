<script lang="ts">
	import type { SequenceData } from '../../types/core.js';
	import SequenceDebugModal from './SequenceDebugModal.svelte';

	// Props
	let {
		sequenceData = null,
		disabled = false,
		position = 'inline'
	}: {
		sequenceData?: SequenceData | null;
		disabled?: boolean;
		position?: 'inline' | 'bottom-right' | 'bottom-left' | 'top-right' | 'top-left';
	} = $props();

	// State
	let isDebugModalOpen = $state(false);

	function openDebugModal(): void {
		if (!disabled && sequenceData) {
			isDebugModalOpen = true;
		}
	}

	function closeDebugModal(): void {
		isDebugModalOpen = false;
	}

	// Keyboard shortcut
	function handleKeydown(event: KeyboardEvent): void {
		if (event.key === 'F12' && event.shiftKey) {
			event.preventDefault();
			if (isDebugModalOpen) {
				closeDebugModal();
			} else {
				openDebugModal();
			}
		}
	}
</script>

<svelte:window on:keydown={handleKeydown} />

<!-- Debug Button -->
<button
	class="debug-button {position}"
	class:disabled
	onclick={openDebugModal}
	title="Open Sequence Debugger (Shift+F12)"
	disabled={disabled || !sequenceData}
>
	🔍
	<span class="debug-label">Debug</span>
</button>

{#if isDebugModalOpen}
	<SequenceDebugModal
		{sequenceData}
		isOpen={isDebugModalOpen}
		onClose={closeDebugModal}
		onApplyOverrides={() => {}}
	/>
{/if}

<style>
	.debug-button {
		background: var(--color-primary);
		color: white;
		border: none;
		border-radius: 8px;
		padding: 0.75rem 1rem;
		cursor: pointer;
		transition: all 0.2s ease;
		font-size: 0.875rem;
		font-weight: 600;
		display: flex;
		align-items: center;
		gap: 0.5rem;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
	}

	.debug-button.inline {
		/* Inline positioning - no fixed positioning */
		position: relative;
		z-index: 1;
	}

	.debug-button:not(.inline) {
		/* Fixed positioning for floating buttons */
		position: fixed;
		z-index: 100;
		backdrop-filter: blur(8px);
	}

	.debug-button:hover:not(.disabled) {
		background: var(--color-primary-hover);
		transform: translateY(-2px);
		box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
	}

	.debug-button.disabled {
		background: var(--color-border);
		color: var(--color-text-secondary);
		cursor: not-allowed;
		opacity: 0.6;
	}

	/* Position variants */
	.debug-button.bottom-right {
		bottom: 1rem;
		right: 1rem;
	}

	.debug-button.bottom-left {
		bottom: 1rem;
		left: 1rem;
	}

	.debug-button.top-right {
		top: 1rem;
		right: 1rem;
	}

	.debug-button.top-left {
		top: 1rem;
		left: 1rem;
	}

	.debug-label {
		font-size: 0.875rem;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.debug-button:not(.inline) {
			padding: 0.5rem;
			border-radius: 50%;
			width: 48px;
			height: 48px;
			justify-content: center;
		}

		.debug-button:not(.inline) .debug-label {
			display: none;
		}

		.debug-button.bottom-right {
			bottom: 5rem; /* Above other floating buttons */
			right: 1rem;
		}
	}
</style>
