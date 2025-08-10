<!--
Increment Adjuster Button - Svelte Version
A custom perfectly round button with hover effects and dynamic styling.
-->
<script lang="ts">
	interface Props {
		symbol: string;
		disabled?: boolean;
	}

	let { symbol, disabled = false }: Props = $props();

	// Handle click event
	function handleClick(): CustomEvent | undefined {
		if (!disabled) {
			// Emit custom event that parent can listen to
			const event = new CustomEvent('click');
			return event;
		}
		return undefined;
	}
</script>

<button
	class="increment-adjuster-button"
	class:disabled
	{disabled}
	onclick={handleClick}
	type="button"
>
	{symbol}
</button>

<style>
	.increment-adjuster-button {
		width: 35px;
		height: 35px;
		background-color: rgba(46, 46, 46, 0.8);
		border: 2px solid rgba(170, 170, 170, 0.6);
		color: white;
		font-weight: bold;
		font-size: 16px;
		border-radius: 50%;
		text-align: center;
		padding: 0;
		margin: 0;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		font-family: Georgia, serif;
		transition: all 0.2s ease;
		user-select: none;
	}

	.increment-adjuster-button:hover:not(:disabled) {
		background-color: rgba(68, 68, 68, 0.8);
		border: 2px solid rgba(255, 255, 255, 0.8);
	}

	.increment-adjuster-button:active:not(:disabled) {
		background-color: rgba(85, 85, 85, 0.8);
		border: 2px solid rgba(221, 221, 221, 0.8);
	}

	.increment-adjuster-button:disabled {
		opacity: 0.5;
		cursor: not-allowed;
		background-color: rgba(30, 30, 30, 0.8);
		border: 2px solid rgba(100, 100, 100, 0.6);
	}
</style>
