<!--
SequenceCard.svelte

Prototype card for the Explore grid that focuses on a single primary action,
lightweight metadata, and a compact overflow menu for secondary operations.
-->
<script lang="ts">
  import type { SequenceData } from "$shared";
  import { onMount } from "svelte";

  const {
    sequence,
    coverUrl,
    isFavorite = false,
    badges = [],
    onPrimaryAction = () => {},
    onFavoriteToggle = () => {},
    onOverflowAction = () => {},
  } = $props<{
    sequence: SequenceData;
    coverUrl?: string;
    isFavorite?: boolean;
    badges?: string[];
    onPrimaryAction?: (sequence: SequenceData) => void;
    onFavoriteToggle?: (sequence: SequenceData) => void;
    onOverflowAction?: (action: string, sequence: SequenceData) => void;
  }>();

  let menuOpen = $state(false);
  let overflowId = $state(`sequence-menu-${sequence.id}`);

  function handlePrimaryAction() {
    onPrimaryAction(sequence);
  }

  function handleFavoriteToggle() {
    onFavoriteToggle(sequence);
  }

  function handleOverflowClick() {
    menuOpen = !menuOpen;
  }

  function handleOverflowItem(action: string) {
    menuOpen = false;
    onOverflowAction(action, sequence);
  }

  onMount(() => {
    // Ensure each instance gets a unique id in Storybook hot reloads
    overflowId = `${overflowId}-${Math.random().toString(36).slice(2, 6)}`;
  });

  const difficultyLabel = $derived(() => {
    switch (sequence.difficultyLevel) {
      case "beginner":
        return "Beginner";
      case "intermediate":
        return "Intermediate";
      case "advanced":
        return "Advanced";
      default:
        return "Unrated";
    }
  });

  const beatsLabel = $derived(() => {
    const beats = sequence.beats?.length ?? sequence.sequenceLength ?? 0;
    return beats === 1 ? "1 beat" : `${beats} beats`;
  });
</script>

<article class="sequence-card">
  <div class="media">
    {#if coverUrl}
      <img src={coverUrl} alt={`Preview of ${sequence.word}`} loading="lazy" />
    {:else}
      <div class="media-placeholder" aria-label="Sequence preview missing">
        <span>{sequence.word.slice(0, 1) ?? "?"}</span>
      </div>
    {/if}

    <button
      type="button"
      class="primary-action"
      aria-label="Play sequence preview"
      onclick={handlePrimaryAction}
    >
      ▶
    </button>

    <button
      type="button"
      class="favorite"
      aria-label={isFavorite ? "Remove from favorites" : "Add to favorites"}
      aria-pressed={isFavorite}
      onclick={handleFavoriteToggle}
    >
      {isFavorite ? "★" : "☆"}
    </button>

    <button
      type="button"
      class="overflow"
      aria-haspopup="true"
      aria-expanded={menuOpen}
      aria-controls={overflowId}
      onclick={handleOverflowClick}
    >
      ⋮
    </button>

    {#if menuOpen}
      <ul class="menu" role="menu" id={overflowId}>
        <li role="presentation">
          <button role="menuitem" onclick={() => handleOverflowItem("edit")}>
            Edit
          </button>
        </li>
        <li role="presentation">
          <button role="menuitem" onclick={() => handleOverflowItem("animate")}>
            Animate
          </button>
        </li>
        <li role="presentation">
          <button role="menuitem" onclick={() => handleOverflowItem("delete")}>
            Delete
          </button>
        </li>
      </ul>
    {/if}
  </div>

  <div class="metadata">
    <div class="title-row">
      <p class="title">{sequence.word}</p>
      <span class="difficulty">{difficultyLabel}</span>
    </div>
    <p class="beats">{beatsLabel}</p>

    {#if badges.length > 0}
      <div class="badges">
        {#each badges.slice(0, 2) as badge}
          <span class="badge">{badge}</span>
        {/each}
      </div>
    {/if}
  </div>
</article>

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
  }

  .media {
    position: relative;
    aspect-ratio: 4 / 3;
    background: rgba(255, 255, 255, 0.05);
  }

  .media img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }

  .media-placeholder {
    width: 100%;
    height: 100%;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, #1f2937, #111827);
    font-size: 4rem;
    font-weight: 700;
  }

  .primary-action {
    position: absolute;
    inset: auto auto 16px 16px;
    width: 56px;
    height: 56px;
    border-radius: 50%;
    border: none;
    background: rgba(255, 255, 255, 0.95);
    color: #111;
    font-size: 1.5rem;
    cursor: pointer;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
  }

  .primary-action:hover,
  .primary-action:focus-visible {
    transform: scale(1.05);
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.4);
  }

  .favorite,
  .overflow {
    position: absolute;
    top: 12px;
    width: 40px;
    height: 40px;
    border: none;
    border-radius: 999px;
    background: rgba(17, 17, 23, 0.7);
    color: #fff;
    font-size: 1.1rem;
    cursor: pointer;
    transition: background 0.2s ease, transform 0.2s ease;
  }

  .favorite {
    right: 12px;
  }

  .overflow {
    right: 60px;
  }

  .favorite:hover,
  .favorite:focus-visible,
  .overflow:hover,
  .overflow:focus-visible {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
    outline: none;
  }

  .menu {
    position: absolute;
    top: 56px;
    right: 60px;
    background: rgba(10, 10, 14, 0.95);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.45);
    list-style: none;
    padding: 4px;
    margin: 0;
    min-width: 140px;
  }

  .menu button {
    width: 100%;
    background: transparent;
    color: #fff;
    border: none;
    padding: 8px 12px;
    text-align: left;
    cursor: pointer;
    border-radius: 8px;
  }

  .menu button:hover,
  .menu button:focus-visible {
    background: rgba(255, 255, 255, 0.1);
    outline: none;
  }

  .metadata {
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .title-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 12px;
  }

  .title {
    font-size: 1.1rem;
    font-weight: 600;
    margin: 0;
  }

  .difficulty {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: rgba(255, 255, 255, 0.7);
  }

  .beats {
    margin: 0;
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.75);
  }

  .badges {
    display: flex;
    gap: 8px;
  }

  .badge {
    font-size: 0.7rem;
    padding: 4px 8px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }
</style>
