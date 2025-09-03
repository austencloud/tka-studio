<script lang="ts">
	import hapticFeedbackService from '$lib/services/HapticFeedbackService';
	import { browser } from '$app/environment';

	// Use Svelte 5 props rune
	const { onClick = () => {} } = $props<{
		onClick?: () => void;
	}>();

	// Function to handle settings button click
	function handleClick() {
		// Provide haptic feedback when opening settings
		if (browser && hapticFeedbackService.isAvailable()) {
			hapticFeedbackService.trigger('selection');
		}

		onClick();
	}
</script>

<button
	class="settings-button ripple"
	onclick={handleClick}
	aria-label="Settings"
	data-mdb-ripple="true"
	data-mdb-ripple-color="light"
>
	<div class="icon-wrapper">
		<i class="fa-solid fa-gear settings-icon" aria-hidden="true"></i>
	</div>
</button>

<style>
	:global(.sequence-widget > .main-layout > .settings-button) {
		position: absolute;
		top: calc(var(--button-size-factor, 1) * 10px); /* Consistent with other buttons */
		left: calc(var(--button-size-factor, 1) * 10px);
		width: calc(var(--button-size-factor, 1) * 45px); /* Base size from ShareButton */
		height: calc(var(--button-size-factor, 1) * 45px);
		z-index: 40; /* Consistent with other FABs */
		/* Override default margin from SettingsButton's own style if necessary */
		margin: 0 !important;
	}

	/* Ensure the icon inside scales correctly if its internal styling doesn't use a factor */
	:global(.sequence-widget > .main-layout > .settings-button .settings-icon) {
		font-size: calc(var(--button-size-factor, 1) * 19px); /* Base icon size from ShareButton */
	}

	.settings-button {
		display: flex;
		align-items: center;
		justify-content: center;

		background-color: var(--tkc-button-panel-background, #2a2a2e);
		color: var(
			--tkc-icon-color-settings,
			var(--tkc-icon-color-share, #00bcd4)
		); /* Default to share color if specific not set */

		border-radius: 50%; /* Round button */
		cursor: pointer;
		transition:
			transform 0.2s ease-out,
			background-color 0.2s ease-out,
			box-shadow 0.2s ease-out;
		box-shadow:
			0 3px 6px rgba(0, 0, 0, 0.16),
			0 3px 6px rgba(0, 0, 0, 0.23);
		border: none;
		padding: 0;
		pointer-events: auto;
		position: relative;
		overflow: hidden;
		/* Width and height will be controlled by consuming component, e.g., SequenceWidget */
		/* Remove fixed margin, let consumer handle spacing */
	}

	.settings-button:hover {
		background-color: var(--tkc-button-panel-background-hover, #3c3c41);
		transform: translateY(-2px) scale(1.05); /* Keep hover effect */
		box-shadow:
			0 6px 12px rgba(0, 0, 0, 0.2),
			0 4px 8px rgba(0, 0, 0, 0.26);
		color: var(--tkc-icon-color-settings-hover, #6c9ce9); /* Keep original hover color for icon */
	}

	.settings-button:active {
		transform: translateY(0px) scale(1);
		background-color: var(--tkc-button-panel-background-active, #1e1e21);
		box-shadow:
			0 1px 3px rgba(0, 0, 0, 0.12),
			0 1px 2px rgba(0, 0, 0, 0.24);
	}

	.settings-button:focus-visible {
		outline: none;
		box-shadow: 0 0 0 2px var(--tkc-focus-ring-color, rgba(108, 156, 233, 0.6));
	}

	.icon-wrapper {
		background: transparent;
		display: flex;
		align-items: center;
		justify-content: center;
		width: 100%; /* Ensure wrapper fills button for icon centering */
		height: 100%;
		color: inherit;
	}

	.settings-icon {
		/* Font size will be controlled by consuming component, e.g., SequenceWidget */
		line-height: 1;
		transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
		display: block;
	}

	.settings-button:hover .settings-icon {
		transform: rotate(90deg); /* Keep icon rotation */
	}
</style>
