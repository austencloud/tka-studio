<!--
TKAGlyph.svelte - Modern Rune-Based TKA Glyph Component

Renders letters, turn indicators, and other TKA notation elements.
Uses pure runes instead of stores for reactivity.
-->
<script lang="ts">
	interface Props {
		/** The letter to display */
		letter: string | null | undefined;
		/** Position X coordinate */
		x?: number;
		/** Position Y coordinate */
		y?: number;
		/** Turns tuple in format "(s, 0, 0)" */
		turnsTuple?: string;
		/** Text color */
		color?: string;
		/** Debug mode */
		debug?: boolean;
	}

	let {
		letter,
		x = 63,
		y = 766,
		turnsTuple = "(s, 0, 0)",
		color = '#4b5563',
		debug = false
	}: Props = $props();

	// Derived state - check if we have a valid letter
	const hasLetter = $derived(() => {
		return letter != null && letter.trim() !== '';
	});

	// Derived state - parse turns tuple
	const parsedTurns = $derived(() => {
		if (!turnsTuple) return { timing: 's', blue: 0, red: 0 };
		
		try {
			// Remove parentheses and split by comma
			const cleaned = turnsTuple.replace(/[()]/g, '').trim();
			const parts = cleaned.split(',').map(s => s.trim());
			
			if (parts.length !== 3) {
				return { timing: 's', blue: 0, red: 0 };
			}

			return {
				timing: parts[0],
				blue: parseFloat(parts[1]) || 0,
				red: parseFloat(parts[2]) || 0
			};
		} catch (error) {
			if (debug) {
				console.warn('Failed to parse turns tuple:', turnsTuple, error);
			}
			return { timing: 's', blue: 0, red: 0 };
		}
	});

	// Derived state - check if we should show turn indicators
	const showTurns = $derived(() => {
		const turns = parsedTurns();
		return turns.blue !== 0 || turns.red !== 0;
	});

	// Derived state - format turn displays
	const turnDisplays = $derived(() => {
		const turns = parsedTurns();
		const displays = [];

		if (turns.blue !== 0) {
			displays.push({
				color: 'blue',
				value: turns.blue,
				displayText: formatTurnValue(turns.blue)
			});
		}

		if (turns.red !== 0) {
			displays.push({
				color: 'red',
				value: turns.red,
				displayText: formatTurnValue(turns.red)
			});
		}

		return displays;
	});

	// Format turn value for display
	function formatTurnValue(value: number): string {
		if (value === 0) return '';
		if (value % 1 === 0) return value.toString(); // Whole number
		return value.toFixed(1); // Decimal
	}

	// Get color for turn indicators
	function getTurnColor(color: string): string {
		switch (color) {
			case 'blue': return '#3b82f6';
			case 'red': return '#ef4444';
			default: return '#6b7280';
		}
	}

	// Calculate positions for turn indicators
	const turnPositions = $derived(() => {
		const displays = turnDisplays();
		const spacing = 40;
		const startX = x - (displays.length - 1) * spacing / 2;
		
		return displays.map((display, index) => ({
			...display,
			x: startX + index * spacing,
			y: y + 30 // Below the letter
		}));
	});
</script>

<!-- TKA Glyph Group -->
{#if hasLetter()}
	<g class="tka-glyph" data-letter={letter} data-turns={turnsTuple}>
		<!-- Main letter -->
		<image
			x={x - 30}
			y={y - 60}
			width="60"
			height="80"
			href="/images/letters_trimmed/Type1/{letter}.svg"
			class="letter-image"
		/>

		<!-- Turn indicators -->
		{#if showTurns()}
			<g class="turn-indicators">
				{#each turnPositions() as turn (turn.color)}
					<!-- Turn circle background -->
					<circle
						cx={turn.x}
						cy={turn.y}
						r="12"
						fill={getTurnColor(turn.color)}
						stroke="white"
						stroke-width="2"
						opacity="0.9"
					/>
					
					<!-- Turn value text -->
					<text
						x={turn.x}
						y={turn.y}
						text-anchor="middle"
						dominant-baseline="middle"
						font-family="Arial, sans-serif"
						font-size="11"
						font-weight="bold"
						fill="white"
					>
						{turn.displayText}
					</text>
				{/each}
			</g>
		{/if}

		<!-- Timing indicator (if not 's' - simultaneous) -->
		{#if parsedTurns().timing !== 's'}
			<text
				x={x}
				y={y - fontSize - 10}
				text-anchor="middle"
				font-family="Arial, sans-serif"
				font-size={fontSize * 0.6}
				font-weight="normal"
				fill="#6b7280"
				opacity="0.8"
			>
				{parsedTurns().timing.toUpperCase()}
			</text>
		{/if}

		{#if debug}
			<!-- Debug overlay -->
			<g class="debug-overlay">
				<!-- Position indicator -->
				<circle
					{x}
					{y}
					r="3"
					fill="#8b5cf6"
					opacity="0.8"
				/>
				
				<!-- Debug info -->
				<text
					x={x + 20}
					y={y - 20}
					font-size="8"
					fill="#8b5cf6"
					font-family="monospace"
				>
					Letter: {letter}
				</text>
				<text
					x={x + 20}
					y={y - 10}
					font-size="8"
					fill="#8b5cf6"
					font-family="monospace"
				>
					Turns: {turnsTuple}
				</text>
			</g>
		{/if}
	</g>
{/if}

<style>
	.tka-glyph {
		/* Glyphs are rendered on top layer above arrows */
		z-index: 4;
	}

	.letter-text {
		/* Smooth text rendering */
		text-rendering: optimizeLegibility;
		-webkit-font-smoothing: antialiased;
		-moz-osx-font-smoothing: grayscale;
	}

	.letter-text:hover {
		filter: brightness(1.1);
	}

	.turn-indicators circle {
		transition: all 0.2s ease;
	}

	.turn-indicators circle:hover {
		transform: scale(1.1);
		transform-origin: center;
	}

	.debug-overlay {
		pointer-events: none;
	}
</style>
