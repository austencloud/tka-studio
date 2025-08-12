<script lang="ts">
	interface Props {
		isPlaying: boolean;
		onPlayPause: () => void;
		onReset: () => void;
	}

	let { isPlaying, onPlayPause, onReset }: Props = $props();
</script>

<div class="control-group">
	<button 
		onclick={onReset} 
		class="control-button"
		aria-label="Reset animation"
	>
		⏮
	</button>
	<button 
		onclick={onPlayPause} 
		class="control-button primary"
		class:active={isPlaying}
		aria-label={isPlaying ? 'Pause animation' : 'Play animation'}
	>
		{isPlaying ? '⏸' : '▶️'}
	</button>
</div>

<style>
	.control-group {
		display: flex;
		gap: 0.75rem;
		align-items: center;
	}

	.control-button {
		padding: 0.75rem 1rem;
		border-radius: 0.5rem;
		border: 1px solid rgba(255, 255, 255, 0.3);
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s ease-in-out;
		background: rgba(255, 255, 255, 0.1);
		color: white;
		min-width: 3rem;
	}

	.control-button:hover:not(:disabled) {
		background: rgba(255, 255, 255, 0.2);
		transform: translateY(-1px);
	}

	.control-button.primary {
		background: rgba(34, 197, 94, 0.3);
		border-color: rgba(34, 197, 94, 0.5);
	}

	.control-button.primary:hover {
		background: rgba(34, 197, 94, 0.4);
	}

	.control-button.active {
		background: rgba(16, 185, 129, 0.4);
		border-color: rgba(16, 185, 129, 0.6);
	}
</style>
