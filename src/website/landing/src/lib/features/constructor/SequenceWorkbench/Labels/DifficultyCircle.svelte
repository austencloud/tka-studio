<!--
  DifficultyCircle Component

  This component displays a circular difficulty indicator similar to the Python implementation.
  It uses the same gradient color scheme as the difficultyCircleDrawer.ts.
-->
<script lang="ts">
	// Gradient stop definition
	interface GradientStop {
		position: number;
		color: string;
	}

	// Gradient definitions for different difficulty levels
	const DIFFICULTY_GRADIENTS: Record<number, GradientStop[]> = {
		1: [
			{ position: 0, color: '#F5F5F5' } // Light gray/white
		],
		2: [
			{ position: 0, color: '#AAAAAA' },
			{ position: 0.15, color: '#D2D2D2' },
			{ position: 0.3, color: '#787878' },
			{ position: 0.4, color: '#B4B4B4' },
			{ position: 0.55, color: '#BEBEBE' },
			{ position: 0.75, color: '#828282' },
			{ position: 1, color: '#6E6E6E' }
		],
		3: [
			{ position: 0, color: '#FFD700' }, // Gold
			{ position: 0.2, color: '#EEC900' }, // Goldenrod
			{ position: 0.4, color: '#DAA520' }, // Goldenrod darker
			{ position: 0.6, color: '#B8860B' }, // Dark goldenrod
			{ position: 0.8, color: '#8B4513' }, // Saddle brown
			{ position: 1, color: '#556B2F' } // Dark olive green
		],
		4: [
			{ position: 0, color: '#C8A2C8' },
			{ position: 0.3, color: '#AA84AA' },
			{ position: 0.6, color: '#9400D3' },
			{ position: 1, color: '#640096' }
		],
		5: [
			{ position: 0, color: '#FF4500' },
			{ position: 0.4, color: '#FF0000' },
			{ position: 0.8, color: '#8B0000' },
			{ position: 1, color: '#640000' }
		]
	};

	// Props
	const { difficultyLevel = 1, size = 30, showBorder = true } = $props();

	// Validate difficulty level
	const level = $derived(Math.max(1, Math.min(5, Math.round(difficultyLevel))));

	// Calculate font size (65% of radius)
	const fontSize = $derived(Math.round((size * 0.65) / 2));

	// Determine text color based on difficulty level
	const textColor = $derived(level >= 4 ? 'white' : 'black');

	// Generate gradient CSS
	const gradientCSS = $derived(() => {
		const stops = DIFFICULTY_GRADIENTS[level] || DIFFICULTY_GRADIENTS[1];
		return stops.map((stop) => `${stop.color} ${stop.position * 100}%`).join(', ');
	});
</script>

<div
	class="difficulty-circle"
	style="
    --size: {size}px;
    --font-size: {fontSize}px;
    --text-color: {textColor};
    --gradient: linear-gradient(135deg, {gradientCSS});
    --border: {showBorder ? '1px solid black' : 'none'};
  "
>
	{level}
</div>

<style>
	.difficulty-circle {
		width: var(--size);
		height: var(--size);
		border-radius: 50%;
		background: var(--gradient);
		display: flex;
		align-items: center;
		justify-content: center;
		font-family: Georgia, serif;
		font-weight: bold;
		font-size: var(--font-size);
		color: var(--text-color);
		border: var(--border);
		box-sizing: border-box;

		/* Add text shadow for better readability on dark backgrounds */
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
	}
</style>
