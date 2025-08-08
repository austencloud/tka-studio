<!--
TKA Glyph Component for TKA Pictographs
Based on v1-legacy implementation using Svelte 5 runes
-->
<script lang="ts">
	// Props using runes
	const props = $props<{
		letter: string;
		turnsTuple: string;
		x: number;
		y: number;
		scale?: number;
	}>();

	// State using runes
	let letterLoaded = $state(false);

	// Derived values
	const effectiveScale = $derived.by(() => props.scale ?? 1);
	const transform = $derived.by(() => `translate(${props.x}, ${props.y}) scale(${effectiveScale})`);

	// Parse turns tuple
	const parsedTurns = $derived.by(() => {
		if (!props.turnsTuple) return { direction: null, top: 0, bottom: 0 };

		// Simple parsing - real implementation would be more sophisticated
		const match = props.turnsTuple.match(/\((\w+),\s*(\d+),\s*(\d+)\)/);
		if (match) {
			return {
				direction: match[1],
				top: parseInt(match[2]),
				bottom: parseInt(match[3])
			};
		}

		return { direction: null, top: 0, bottom: 0 };
	});

	const shouldShowDots = $derived.by(() => parsedTurns.top > 0 || parsedTurns.bottom > 0);

	// Letter SVG path mapping - using correct letter names from legacy
	const letterSvgPath = $derived.by(() => {
		const letterMap: Record<string, string> = {
			'α': '/images/letters_trimmed/Type6/Alpha.svg',
			'β': '/images/letters_trimmed/Type6/Beta.svg',
			'Γ': '/images/letters_trimmed/Type6/Gamma.svg',
			'Δ': '/images/letters_trimmed/Type6/Delta.svg',
			'ε': '/images/letters_trimmed/Type6/Epsilon.svg',
			'ζ': '/images/letters_trimmed/Type6/Zeta.svg',
			'η': '/images/letters_trimmed/Type6/Eta.svg',
			'θ': '/images/letters_trimmed/Type6/Theta.svg',
			// Add more common letters
			'A': '/images/letters_trimmed/Type6/Alpha.svg',
			'B': '/images/letters_trimmed/Type6/Beta.svg',
			'G': '/images/letters_trimmed/Type6/Gamma.svg'
		};

		return letterMap[props.letter] || null;
	});

	function handleLetterLoad() {
		console.log(`✅ TKA Glyph: Letter loaded successfully: ${props.letter}`);
		letterLoaded = true;
	}

	function handleLetterError() {
		console.warn(`❌ TKA Glyph: Failed to load letter: ${props.letter} from path: ${letterSvgPath}`);
		letterLoaded = true; // Still show other elements
	}
</script>

<g class="tka-glyph" {transform}>
	<!-- Letter -->
	{#if letterSvgPath}
		<image
			href={letterSvgPath}
			x="0"
			y="0"
			width="50"
			height="50"
			onload={handleLetterLoad}
			onerror={handleLetterError}
		/>
	{:else}
		<!-- Fallback text representation -->
		<rect
			x="0"
			y="0"
			width="50"
			height="50"
			fill="white"
			stroke="#333"
			stroke-width="2"
			rx="6"
		/>
		<text
			x="25"
			y="32"
			text-anchor="middle"
			font-family="Arial, sans-serif"
			font-size="24"
			font-weight="bold"
			fill="#333"
		>
			{props.letter}
		</text>
	{/if}

	{#if letterLoaded}
		<!-- Dash (horizontal line to the right of letter) -->
		<line
			x1="55"
			y1="25"
			x2="75"
			y2="25"
			stroke="#333"
			stroke-width="3"
			stroke-linecap="round"
		/>

		{#if shouldShowDots}
			<!-- Same direction dot -->
			{#if parsedTurns.direction === 's'}
				<circle cx="85" cy="20" r="3" fill="#333" />
			{:else}
				<circle cx="85" cy="30" r="3" fill="#333" />
			{/if}

			<!-- Opposite direction dot -->
			{#if parsedTurns.direction === 's'}
				<circle cx="85" cy="30" r="3" fill="none" stroke="#333" stroke-width="2" />
			{:else}
				<circle cx="85" cy="20" r="3" fill="none" stroke="#333" stroke-width="2" />
			{/if}
		{/if}

		<!-- Turn numbers -->
		{#if parsedTurns.top > 0}
			<text
				x="100"
				y="15"
				text-anchor="middle"
				font-family="Arial, sans-serif"
				font-size="14"
				font-weight="bold"
				fill="#333"
			>
				{parsedTurns.top}
			</text>
		{/if}

		{#if parsedTurns.bottom > 0}
			<text
				x="100"
				y="40"
				text-anchor="middle"
				font-family="Arial, sans-serif"
				font-size="14"
				font-weight="bold"
				fill="#333"
			>
				{parsedTurns.bottom}
			</text>
		{/if}
	{/if}
</g>
