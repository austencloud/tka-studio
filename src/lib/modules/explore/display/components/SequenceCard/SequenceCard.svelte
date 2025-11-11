<!--
SequenceCard.svelte

Card component for the Explore grid. Displays sequence preview with metadata.
Clicking the card opens the sequence detail viewer.

Composed from smaller sub-components for better maintainability:
- SequenceCardMedia: Image/placeholder display
- SequenceCardFooter: Metadata section with title and actions
  - SequenceCardOverflowMenu: Three-dot menu (Edit/Animate/Delete)
  - SequenceCardFavoriteButton: Star button

Enhanced with Svelte 5 runes for reactive state management.
-->
<script lang="ts">
  import type { SequenceData } from "$shared";
  import SequenceCardMedia from "./SequenceCardMedia.svelte";
  import SequenceCardFooter from "./SequenceCardFooter.svelte";

  const {
    sequence,
    coverUrl = undefined,
    isFavorite = false,
    onPrimaryAction = () => {},
    onFavoriteToggle = () => {},
    onOverflowAction = () => {},
  }: {
    sequence: SequenceData;
    coverUrl?: string;
    isFavorite?: boolean;
    onPrimaryAction?: (sequence: SequenceData) => void;
    onFavoriteToggle?: (sequence: SequenceData) => void;
    onOverflowAction?: (action: string, sequence: SequenceData) => void;
  } = $props();

  // Extract image dimensions from metadata for layout shift prevention
  const imageDimensions = $derived({
    width: (sequence.metadata as any)?.width,
    height: (sequence.metadata as any)?.height,
  });

  let menuOpen = $state(false);
  let overflowId = $state(
    `sequence-menu-${sequence?.id ?? crypto.randomUUID()}-${Math.random().toString(36).slice(2, 6)}`
  );

  function handlePrimaryAction() {
    onPrimaryAction(sequence);
  }

  function handleFavoriteToggle() {
    onFavoriteToggle(sequence);
  }

  function handleMenuToggle() {
    menuOpen = !menuOpen;
  }

  function handleMenuItemSelect(action: string) {
    menuOpen = false;
    onOverflowAction(action, sequence);
  }

  function handleClickOutside(event: MouseEvent) {
    if (menuOpen && !(event.target as Element).closest(".icon-slot")) {
      menuOpen = false;
    }
  }

  const levelStyles: Record<number, { background: string; textColor: string }> =
    {
      1: {
        background: `linear-gradient(
        135deg,
        rgba(247, 249, 252, 0.98) 0%,
        rgba(232, 235, 240, 0.92) 40%,
        rgba(222, 228, 238, 0.9) 100%
      )`,
        textColor: "#0f172a",
      },
      2: {
        background: `linear-gradient(
        135deg,
        rgba(207, 216, 230, 0.95) 0%,
        rgba(175, 188, 209, 0.9) 45%,
        rgba(141, 154, 177, 0.88) 100%
      )`,
        textColor: "#f8fafc",
      },
      3: {
        background: `linear-gradient(
        135deg,
        rgba(255, 244, 214, 0.95) 0%,
        rgba(250, 221, 128, 0.9) 35%,
        rgba(236, 185, 67, 0.85) 70%,
        rgba(210, 149, 45, 0.8) 100%
      )`,
        textColor: "#1c1917",
      },
      4: {
        background: `linear-gradient(
        135deg,
        rgba(255, 229, 214, 0.95) 0%,
        rgba(247, 158, 129, 0.9) 40%,
        rgba(221, 88, 69, 0.85) 70%,
        rgba(163, 27, 45, 0.85) 100%
      )`,
        textColor: "#fff5f5",
      },
      5: {
        background: `linear-gradient(
        130deg,
        rgba(205, 180, 255, 0.95) 0%,
        rgba(124, 58, 237, 0.9) 45%,
        rgba(59, 130, 246, 0.85) 100%
      )`,
        textColor: "#f8fafc",
      },
    };

  const difficultyToLevel: Record<string, number> = {
    beginner: 1,
    intermediate: 2,
    advanced: 3,
    mythic: 4,
    legendary: 5,
  };

  const defaultStyle = {
    background: "linear-gradient(135deg, #1f2937, #111827)",
    textColor: "#f8fafc",
  };

  // Derived reactive values using $derived
  const sequenceLevel = $derived(
    sequence?.level ??
      difficultyToLevel[sequence?.difficultyLevel?.toLowerCase?.() ?? ""] ??
      0
  );

  const levelStyle = $derived(levelStyles[sequenceLevel] ?? defaultStyle);

  // Truncate title to 16 characters (excluding dashes)
  const displayTitle = $derived(() => {
    const word = sequence?.word ?? "";
    const withoutDashes = word.replace(/-/g, "");

    if (withoutDashes.length <= 16) {
      return word; // Return original including dashes
    }

    // Truncate to 16 non-dash characters
    let charCount = 0;
    let result = "";

    for (const char of word) {
      if (char === "-") {
        result += char;
      } else {
        if (charCount < 16) {
          result += char;
          charCount++;
        } else {
          break;
        }
      }
    }

    return result + "…";
  });

  // Effect to close menu when clicking outside
  $effect(() => {
    if (menuOpen) {
      document.addEventListener("click", handleClickOutside);
      return () => {
        document.removeEventListener("click", handleClickOutside);
      };
    }
    return undefined;
  });
</script>

<button
  class="sequence-card"
  onclick={handlePrimaryAction}
>
  <SequenceCardMedia
    {coverUrl}
    word={sequence.word}
    width={imageDimensions.width}
    height={imageDimensions.height}
  />

  <SequenceCardFooter
    title={displayTitle()}
    {levelStyle}
    {isFavorite}
    {menuOpen}
    menuId={overflowId}
    onFavoriteToggle={handleFavoriteToggle}
    onMenuToggle={handleMenuToggle}
    onMenuItemSelect={handleMenuItemSelect}
  />
</button>

<style>
  .sequence-card {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    background: rgba(8, 8, 12, 0.9);
    border: 1px solid rgba(255, 255, 255, 0.08);
    color: #fff;
    display: flex;
    flex-direction: column;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.35);
    max-width: 360px;
    height: 100%; /* Fill grid cell height */

    /* Enable container queries */
    container-type: inline-size;
    container-name: sequence-card;

    /* Make card clickable */
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .sequence-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 16px 48px rgba(0, 0, 0, 0.45);
    border-color: rgba(255, 255, 255, 0.15);
  }

  .sequence-card:focus {
    outline: 2px solid rgba(255, 255, 255, 0.4);
    outline-offset: 2px;
  }

  /* Desktop refinement for larger viewports - works with container queries */
  @media (min-width: 768px) {
    .sequence-card {
      /* Allow card to adapt to larger grid cells */
      max-width: 100%;
    }
  }
</style>
