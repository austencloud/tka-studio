<script lang="ts">
	interface Props {
		turns: number;
		propColor: string;
		onTurnsChange: (turns: number) => void;
	}

	let { turns, propColor, onTurnsChange }: Props = $props();

	function increment() {
		if (turns < 3) {
			onTurnsChange(turns + 1);
		}
	}

	function decrement() {
		if (turns > 1) {
			onTurnsChange(turns - 1);
		}
	}
</script>

<div class="turns-control">
	<div class="prop-row">
		<div class="prop-label" style="color: {propColor}">
			Turns
		</div>
		<div class="turns-selector">
			<button 
				type="button"
				onclick={decrement}
				disabled={turns <= 1}
				class="turn-btn"
			>
				-
			</button>
			<span class="turn-value">{turns}</span>
			<button 
				type="button"
				onclick={increment}
				disabled={turns >= 3}
				class="turn-btn"
			>
				+
			</button>
		</div>
	</div>
</div>

<style>
	.turns-control {
		width: 100%;
	}

	.prop-row {
		display: grid;
		grid-template-columns: 60px 1fr;
		gap: 10px;
		align-items: center;
	}

	.prop-label {
		font-weight: 600;
		font-size: 0.9rem;
	}

	.turns-selector {
		display: flex;
		align-items: center;
		gap: 8px;
	}

	.turn-btn {
		width: 28px;
		height: 28px;
		border: 1px solid rgba(255, 255, 255, 0.3);
		border-radius: 4px;
		background: rgba(255, 255, 255, 0.1);
		color: white;
		font-size: 16px;
		font-weight: bold;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all 0.2s ease;
	}

	.turn-btn:hover:not(:disabled) {
		background: rgba(255, 255, 255, 0.2);
		border-color: rgba(255, 255, 255, 0.5);
	}

	.turn-btn:disabled {
		opacity: 0.5;
		cursor: not-allowed;
	}

	.turn-value {
		min-width: 20px;
		text-align: center;
		font-weight: 600;
		color: #fbbf24;
	}
</style>
