<!--
Beat Selector Component

Displays a grid of beat buttons for navigation between beats.
-->
<script lang="ts">
	// Props
	const {
		beats = [],
		currentBeat = 0,
		onBeatChange = (beat: number) => {}
	} = $props<{
		beats?: any[];
		currentBeat?: number;
		onBeatChange?: (beat: number) => void;
	}>();
</script>

{#if beats && beats.length > 0}
	<div class="beat-selector">
		{#each beats as _, index}
			<button
				class="beat-button"
				class:active={index === Math.floor(currentBeat)}
				onclick={() => onBeatChange(index)}
			>
				{index + 1}
			</button>
		{/each}
	</div>
{/if}

<style>
	.beat-selector {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		padding: 1rem;
		background: linear-gradient(135deg, 
			rgba(255, 255, 255, 0.06) 0%, 
			rgba(255, 255, 255, 0.03) 100%);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 16px;
		backdrop-filter: blur(15px);
	}

	.beat-button {
		background: rgba(255, 255, 255, 0.05);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.15);
		padding: 0.5rem 0.875rem;
		border-radius: 10px;
		cursor: pointer;
		font-size: 0.875rem;
		font-weight: 500;
		color: rgba(255, 255, 255, 0.8);
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		min-width: 44px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.beat-button:hover {
		background: rgba(255, 255, 255, 0.12);
		border-color: rgba(255, 255, 255, 0.25);
		color: rgba(255, 255, 255, 0.95);
		transform: translateY(-1px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
	}

	.beat-button.active {
		background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
		color: white;
		border-color: rgba(255, 255, 255, 0.3);
		box-shadow: 
			0 4px 16px rgba(99, 102, 241, 0.4),
			inset 0 1px 0 rgba(255, 255, 255, 0.2);
		transform: translateY(-1px);
	}

	/* Focus improvements for accessibility */
	.beat-button:focus-visible {
		outline: 2px solid #818cf8;
		outline-offset: 2px;
	}

	/* Reduced motion support */
	@media (prefers-reduced-motion: reduce) {
		.beat-button {
			transition: none;
		}
	}
</style>
