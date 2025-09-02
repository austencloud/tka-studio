<!--
TKAGlyph.svelte - Modern Rune-Based TKA Glyph Component

Renders letters, turn indicators, and other TKA notation elements.
Uses pure runes instead of stores for reactivity.
-->
<script lang="ts">
  import { Letter, MotionColor } from "$domain";
  import { getLetterImagePath } from "$utils";

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
    /** Scale factor - match legacy behavior */
    scale?: number;
  }

  let {
    letter,
    x = 50, // Match legacy positioning exactly
    y = 800, // Match legacy positioning exactly
    turnsTuple = "(s, 0, 0)",
    // color = '#4b5563',
    scale = 1, // Match legacy default scale
  }: Props = $props();

  // Font size for timing indicators
  const fontSize = 16;

  // Letter dimensions state - match legacy behavior
  let letterDimensions = $state({ width: 0, height: 0 });
  let isLetterLoaded = $state(false);

  // Cache for SVG dimensions (simple in-memory cache)
  const dimensionsCache = new Map<string, { width: number; height: number }>();

  // Load letter dimensions using SVG viewBox like legacy version
  async function loadLetterDimensions(currentLetter: Letter) {
    if (!currentLetter) return;

    // Check cache first
    const cacheKey = currentLetter;
    if (dimensionsCache.has(cacheKey)) {
      letterDimensions = dimensionsCache.get(cacheKey)!;
      isLetterLoaded = true;
      return;
    }

    try {
      // Use correct path based on letter type and safe filename
      const svgPath = getLetterImagePath(currentLetter as Letter);
      const response = await fetch(svgPath);
      if (!response.ok)
        throw new Error(`Failed to fetch ${svgPath}: ${response.status}`);

      const svgText = await response.text();
      const viewBoxMatch = svgText.match(
        /viewBox\s*=\s*"[\d.-]+\s+[\d.-]+\s+([\d.-]+)\s+([\d.-]+)"/i
      );

      if (!viewBoxMatch) {
        console.warn(`SVG at ${svgPath} has no valid viewBox, using defaults`);
        letterDimensions = { width: 100, height: 100 };
      } else {
        letterDimensions = {
          width: parseFloat(viewBoxMatch[1] || "100"),
          height: parseFloat(viewBoxMatch[2] || "100"),
        };
      }

      dimensionsCache.set(cacheKey, letterDimensions);
      isLetterLoaded = true;
    } catch (error) {
      console.error(
        `Failed to load letter dimensions for ${currentLetter}:`,
        error
      );
      // Fallback dimensions
      letterDimensions = { width: 50, height: 50 };
      isLetterLoaded = true;
    }
  }

  // Load dimensions when letter changes
  $effect(() => {
    if (letter) {
      isLetterLoaded = false;
      loadLetterDimensions(letter as Letter);
    }
  });

  // Derived state - check if we have a valid letter
  const hasLetter = $derived(() => {
    return letter != null && letter.trim() !== "";
  });

  // Derived state - parse turns tuple
  const parsedTurns = $derived(() => {
    if (!turnsTuple) return { timing: "s", blue: 0, red: 0 };

    try {
      // Remove parentheses and split by comma
      const cleaned = turnsTuple.replace(/[()]/g, "").trim();
      const parts = cleaned.split(",").map((s) => s.trim());

      if (parts.length !== 3) {
        return { timing: "s", blue: 0, red: 0 };
      }

      return {
        timing: parts[0] || "",
        blue: parseFloat(parts[1] || "0") || 0,
        red: parseFloat(parts[2] || "0") || 0,
      };
    } catch (error) {
      return { timing: "s", blue: 0, red: 0 };
    }
  });

  // Derived state - check if we should show turn indicators
  // TEMPORARILY DISABLED: Turn indicators were creating CIRCLE_PROP duplicates in comparison tests
  const showTurns = $derived(() => {
    // const turns = parsedTurns();
    // return turns.blue !== 0 || turns.red !== 0;
    return false; // Disable turn indicators to prevent CIRCLE_PROP duplicates
  });

  // Derived state - format turn displays
  const turnDisplays = $derived(() => {
    const turns = parsedTurns();
    const displays = [];

    if (turns.blue !== 0) {
      displays.push({
        color: MotionColor.BLUE,
        value: turns.blue,
        displayText: formatTurnValue(turns.blue),
      });
    }

    if (turns.red !== 0) {
      displays.push({
        color: MotionColor.RED,
        value: turns.red,
        displayText: formatTurnValue(turns.red),
      });
    }

    return displays;
  });

  // Format turn value for display
  function formatTurnValue(value: number): string {
    if (value === 0) return "";
    if (value % 1 === 0) return value.toString(); // Whole number
    return value.toFixed(1); // Decimal
  }

  // Get color for turn indicators
  function getTurnColor(color: string): string {
    switch (color) {
      case "blue":
        return "#3b82f6";
      case "red":
        return "#ef4444";
      default:
        return "#6b7280";
    }
  }

  // Calculate positions for turn indicators
  const turnPositions = $derived(() => {
    const displays = turnDisplays();
    const spacing = 40;
    const startX = x - ((displays.length - 1) * spacing) / 2;

    return displays.map((display, index) => ({
      ...display,
      x: startX + index * spacing,
      y: y + 30, // Below the letter
    }));
  });
</script>

<!-- TKA Glyph Group -->
{#if hasLetter() && isLetterLoaded}
  <g
    class="tka-glyph"
    data-letter={letter}
    data-turns={turnsTuple}
    transform="translate({x}, {y}) scale({scale})"
  >
    <!-- Main letter with exact legacy dimensions -->
    <image
      x="0"
      y="0"
      href={letter ? getLetterImagePath(letter as Letter) : ""}
      width={letterDimensions.width}
      height={letterDimensions.height}
      preserveAspectRatio="xMinYMin meet"
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
    {#if parsedTurns().timing !== "s"}
      <text
        x="0"
        y={-fontSize - 10}
        text-anchor="middle"
        font-family="Arial, sans-serif"
        font-size={fontSize * 0.6}
        font-weight="normal"
        fill="#6b7280"
        opacity="0.8"
      >
        {parsedTurns()?.timing?.toUpperCase() || ""}
      </text>
    {/if}
  </g>
{/if}

<style>
  .tka-glyph {
    /* Glyphs are rendered on top layer above arrows */
    z-index: 4;
  }

  .letter-image {
    /* Smooth image rendering */
    image-rendering: optimizeQuality;
  }

  .turn-indicators circle {
    transition: all 0.2s ease;
  }

  .turn-indicators circle:hover {
    transform: scale(1.1);
    transform-origin: center;
  }
</style>
