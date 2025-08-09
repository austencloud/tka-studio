<!--
Current Turn Display - Svelte Version
Displays the currently selected turn value with color-coded styling.
-->
<script lang="ts">
	// Props
	interface Props {
		color: 'blue' | 'red';
		initialValue?: string;
	}

	let { color, initialValue = '0' }: Props = $props();

	// State
	let currentValue = $state(initialValue);

	// Color-specific styling
	const colorStyles = {
		blue: {
			border: '#0066cc',
			background: 'rgba(0, 102, 204, 0.1)',
			text: '#0066cc',
		},
		red: {
			border: '#cc0000',
			background: 'rgba(204, 0, 0, 0.1)',
			text: '#cc0000',
		},
	};

	// Public methods
	export function setValue(value: string) {
		currentValue = value;
	}

	export function getValue(): string {
		return currentValue;
	}
</script>

<div
	class="current-turn-display"
	style="
		border-color: {colorStyles[color].border};
		background: {colorStyles[color].background};
		color: {colorStyles[color].text};
	"
>
	<div class="turn-label">{color.toUpperCase()} TURN</div>
	<div class="turn-value">{currentValue}</div>
</div>

<style>
	.current-turn-display {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: rgba(255, 255, 255, 0.9);
		border: 2px solid;
		border-radius: 8px;
		padding: 12px;
		text-align: center;
		min-height: 60px;
		flex-shrink: 0;
	}

	.turn-label {
		font-size: 0.7rem;
		font-weight: 600;
		opacity: 0.8;
		margin-bottom: 4px;
		text-transform: uppercase;
		letter-spacing: 0.5px;
	}

	.turn-value {
		font-size: 1.5rem;
		font-weight: bold;
		line-height: 1;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.current-turn-display {
			padding: 8px;
			min-height: 50px;
		}

		.turn-label {
			font-size: 0.6rem;
			margin-bottom: 2px;
		}

		.turn-value {
			font-size: 1.2rem;
		}
	}
</style>
