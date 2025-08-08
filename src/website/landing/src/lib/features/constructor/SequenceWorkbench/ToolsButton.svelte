<script lang="ts">
	import { fly } from 'svelte/transition';

	// Props
	export let isToolsPanelOpen = false;

	// Handle click event
	function handleClick() {
		// Create and dispatch a custom event
		const event = new CustomEvent('toggleToolsPanel', {
			bubbles: true,
			composed: true
		});
		document.dispatchEvent(event);
	}
</script>

<button
	class="tools-button ripple"
	on:click={handleClick}
	aria-label={isToolsPanelOpen ? 'Close Tools Panel' : 'Open Tools Panel'}
	aria-expanded={isToolsPanelOpen}
	data-mdb-ripple="true"
	data-mdb-ripple-color="light"
	in:fly={{ x: 20, duration: 300, delay: 200 }}
>
	<div class="icon-wrapper">
		<i class="fa-solid fa-screwdriver-wrench"></i>
	</div>
</button>

<style>
	.tools-button {
		/* Base sizes - increased for better touch targets */
		--base-size: 45px; /* Was 56px */
		--base-margin: 10px;
		--base-icon-size: 19px; /* Was 24px */

		position: absolute;
		bottom: calc(var(--button-size-factor, 1) * var(--base-margin));
		right: calc(var(--button-size-factor, 1) * var(--base-margin));
		z-index: 10;
		width: calc(var(--button-size-factor, 1) * var(--base-size));
		height: calc(var(--button-size-factor, 1) * var(--base-size));
		border: none;
		border-radius: 50%; /* Perfectly circular */
		padding: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		box-shadow:
			0 4px 12px rgba(0, 0, 0, 0.15),
			0 0 0 1px rgba(255, 255, 255, 0.1);
		transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* Bouncy animation */
		color: white;
		background: linear-gradient(135deg, #6a11cb, #2575fc);
		pointer-events: auto;
		/* Ensure minimum size for small screens */
		min-width: 38px; /* Was 48px */
		min-height: 38px; /* Was 48px */
		overflow: hidden; /* Ensure content stays within the circle */
	}

	.tools-button:hover {
		transform: translateY(-4px) scale(1.05);
		box-shadow:
			0 8px 24px rgba(0, 0, 0, 0.2),
			0 0 0 2px rgba(255, 255, 255, 0.2);
	}

	.tools-button:active {
		transform: scale(0.95);
	}

	.icon-wrapper {
		display: flex;
		justify-content: center;
		align-items: center;
		width: 100%;
		height: 100%;
		font-size: calc(var(--button-size-factor, 1) * var(--base-icon-size));
		/* Add a subtle pulse animation */
		animation: pulse 2s infinite ease-in-out;
	}

	@keyframes pulse {
		0% {
			transform: scale(1);
		}
		50% {
			transform: scale(1.05);
		}
		100% {
			transform: scale(1);
		}
	}

	/* Responsive adjustments for small screens */
	@media (max-width: 480px) {
		.tools-button {
			/* Increase size on small screens for better touch targets */
			--base-margin: 10px;
			/* --base-padding: 10px; */ /* Padding is 0 for these buttons */
			--base-icon-size: 24px; /* Icon size can be larger on small screens if desired, or keep 19px */
			/* --base-icon-font-size: 16px; */ /* Not used directly, icon size is base-icon-size */
		}
	}
</style>
