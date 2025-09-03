<!-- src/lib/components/GenerateTab/components/CAPButton.svelte -->
<script lang="ts">
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { browser } from '$app/environment';

	// Use Svelte 5 props rune
	const props = $props<{
		capType: {
			id: string;
			label: string;
			description: string;
		};
		selected?: boolean;
		onClick?: () => void;
	}>();

	// Default values with derived values
	const selected = $derived(props.selected ?? false);

	// Handle button click
	function handleClick() {
		// Provide haptic feedback when selecting a CAP type
		if (browser) {
			hapticFeedbackService.trigger('selection');
		}

		if (props.onClick) {
			props.onClick();
		}
	}
</script>

<button class="cap-button" class:selected onclick={handleClick} title={props.capType.description}>
	<div class="cap-button-content">
		<span class="cap-label">{props.capType.label}</span>
		{#if selected}
			<span class="selected-indicator">✓</span>
		{/if}
	</div>
</button>

<style>
	.cap-button {
		background: var(--color-surface, rgba(30, 40, 60, 0.85));
		border: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
		color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
		border-radius: 0.25rem;
		padding: 0.75rem 1rem;
		width: 100%;
		text-align: left;
		cursor: pointer;
		transition: all 0.2s ease;
		display: flex;
		align-items: center;
		justify-content: space-between;
	}

	.cap-button:hover {
		background: var(--color-surface-hover, rgba(255, 255, 255, 0.05));
		border-color: var(--color-border-hover, rgba(255, 255, 255, 0.2));
	}

	.cap-button.selected {
		background: var(--color-accent, #3a7bd5);
		color: white;
		border-color: var(--color-accent-hover, #2a5298);
	}

	.cap-button-content {
		display: flex;
		align-items: center;
		justify-content: space-between;
		width: 100%;
	}

	.cap-label {
		font-size: 0.875rem;
		font-weight: 500;
	}

	.selected-indicator {
		font-size: 0.75rem;
		margin-left: 0.5rem;
	}
</style>
