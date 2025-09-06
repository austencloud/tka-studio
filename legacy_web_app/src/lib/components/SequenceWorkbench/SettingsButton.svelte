<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher<{ click: void }>();

	function handleClick() {
		dispatch('click');
	}
</script>

<button
	class="settings-button ripple"
	on:click={handleClick}
	aria-label="Open settings"
	data-mdb-ripple="true"
	data-mdb-ripple-color="light"
>
	<div class="icon-wrapper">
		<i class="fa-solid fa-cog"></i>
	</div>
</button>

<style>
	.settings-button {
		/* Base sizes for dynamic scaling - consistent with other FABs */
		--base-size: 45px;
		--base-icon-size: 19px;
		--base-margin: 10px;

		position: absolute;
		/* Will be positioned by parent, but defaults can be set if needed */
		width: calc(var(--button-size-factor, 1) * var(--base-size));
		height: calc(var(--button-size-factor, 1) * var(--base-size));
		min-width: 38px;
		min-height: 38px;

		background-color: var(--tkc-button-panel-background, #2a2a2e);
		color: var(--tkc-icon-color-settings, #00bcd4); /* Similar to share button color */

		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition:
			transform 0.2s ease-out,
			background-color 0.2s ease-out,
			box-shadow 0.2s ease-out;
		z-index: 40; /* Consistent with other FABs */
		box-shadow:
			0 3px 6px rgba(0, 0, 0, 0.16),
			0 3px 6px rgba(0, 0, 0, 0.23);
		border: none;
		padding: 0;
		pointer-events: auto;
	}

	.settings-button:hover {
		background-color: var(--tkc-button-panel-background-hover, #3c3c41);
		transform: translateY(-2px) scale(1.05);
		box-shadow:
			0 6px 12px rgba(0, 0, 0, 0.2),
			0 4px 8px rgba(0, 0, 0, 0.26);
	}

	.settings-button:active {
		transform: translateY(0px) scale(1);
		background-color: var(--tkc-button-panel-background-active, #1e1e21);
		box-shadow:
			0 1px 3px rgba(0, 0, 0, 0.12),
			0 1px 2px rgba(0, 0, 0, 0.24);
	}

	.icon-wrapper {
		background: transparent;
		display: flex;
		align-items: center;
		justify-content: center;
		width: auto;
		height: auto;
		color: inherit;
	}

	.icon-wrapper i.fa-cog {
		font-size: calc(var(--button-size-factor, 1) * var(--base-icon-size));
	}
</style>
