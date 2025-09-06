<script lang="ts">
	import type { ViewOption } from './types';

	// Props using Svelte 5 runes
	const props = $props<{
		selectedViewOption: ViewOption;
		isOpen: boolean;
		onClick: () => void;
		compact?: boolean;
		onButtonRef?: (element: HTMLButtonElement) => void;
	}>();

	// Local state
	let isCompact = $state(false);
	let buttonRef = $state<HTMLButtonElement | null>(null);

	// Update compact mode based on props
	$effect(() => {
		isCompact = props.compact || false;
	});

	// Use the buttonRef to call the callback prop
	$effect(() => {
		if (buttonRef && props.onButtonRef) {
			props.onButtonRef(buttonRef);
		}
	});
</script>

<button
	class="view-button"
	class:compact={isCompact}
	bind:this={buttonRef}
	onclick={props.onClick}
	aria-label="Change view mode"
	aria-expanded={props.isOpen}
	aria-haspopup="listbox"
	title={props.selectedViewOption.description}
>
	<span class="view-icon" aria-hidden="true">{props.selectedViewOption.icon}</span>
	{#if !isCompact}
		<span class="view-label">{props.selectedViewOption.label}</span>
		<span class="dropdown-arrow" aria-hidden="true">{props.isOpen ? '▲' : '▼'}</span>
	{/if}
</button>

<style>
	/* Base variables for sizing, mirroring other Sequence Widget buttons */
	:root {
		--view-button-base-size: 45px;
		--view-button-icon-size: 19px;
		/* Define a specific icon color for the view button, defaulting to a vibrant blue */
		--tkc-icon-color-view: var(--tkc-icon-color-fullscreen, #4cc9f0);
	}

	.view-button {
		/* Base sizing variables - identical to other sequence buttons */
		--base-size: 45px;
		--base-icon-size: 19px;
		--base-margin: 10px;

		/* Sizing and Shape */
		width: calc(var(--button-size-factor, 1) * var(--base-size));
		height: calc(var(--button-size-factor, 1) * var(--base-size));
		min-width: 38px;
		min-height: 38px;
		border-radius: 50%;
		padding: 0;

		/* Display and Alignment */
		display: flex;
		align-items: center;
		justify-content: center;

		/* Appearance */
		background-color: var(--tkc-button-panel-background, #2a2a2e);
		color: var(--tkc-icon-color-view, var(--tkc-icon-color-fullscreen, #4cc9f0));
		border: none;
		box-shadow:
			0 3px 6px rgba(0, 0, 0, 0.16),
			0 3px 6px rgba(0, 0, 0, 0.23);
		cursor: pointer;
		overflow: hidden;
		user-select: none;
		position: relative;
		z-index: 40;

		/* Transitions for effects - exact match with other buttons */
		transition:
			transform 0.2s ease-out,
			background-color 0.2s ease-out,
			box-shadow 0.2s ease-out;
	}

	.view-button:hover {
		background-color: var(--tkc-button-panel-background-hover, #3c3c41);
		transform: translateY(-2px) scale(1.05);
		box-shadow:
			0 6px 12px rgba(0, 0, 0, 0.2),
			0 4px 8px rgba(0, 0, 0, 0.26);
	}

	.view-button:active {
		transform: translateY(0px) scale(1);
		background-color: var(--tkc-button-panel-background-active, #1e1e21);
		box-shadow:
			0 1px 3px rgba(0, 0, 0, 0.12),
			0 1px 2px rgba(0, 0, 0, 0.24);
	}

	.view-button:focus-visible {
		outline: none;
		box-shadow:
			0 0 0 2px var(--tkc-focus-ring-color, rgba(108, 156, 233, 0.6)),
			0 3px 6px rgba(0, 0, 0, 0.16),
			0 3px 6px rgba(0, 0, 0, 0.23);
	}

	.view-icon {
		font-size: calc(var(--button-size-factor, 1) * var(--base-icon-size));
		line-height: 1; /* Ensure consistent icon alignment */
		/* Removed previous specific icon styles like filter, transform, custom transitions */
	}

	/* Hide label and dropdown arrow to make it an icon-only button */
	.view-label,
	.dropdown-arrow {
		display: none;
	}

	/*
		The ::after pseudo-element for glow is removed as it's not typical for SequenceWidget buttons.
		The .view-button.compact class styles are removed as the base style now dictates the compact, round look.
		Responsive media queries (@media) that previously handled compactness are removed for the same reason.
	*/

	/* Responsive adjustments - match other buttons */
	@media (max-width: 768px) {
		.view-button {
			--button-size-factor: 0.9;
		}
	}

	@media (max-width: 480px) {
		.view-button {
			--button-size-factor: 0.8;
		}
	}
</style>
