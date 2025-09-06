<!-- src/lib/components/BrowseTab/SequenceGrid/Thumbnail.svelte -->
<script lang="ts">
  import { createEventDispatcher } from 'svelte';
  import type { SequenceData } from '$lib/stores/browseTab/browseTabStore';

  // Props
  export let sequence: SequenceData;
  export let isSelected = false;

  // Create event dispatcher
  const dispatch = createEventDispatcher();

  // Compute if any variation is a favorite
  $: hasFavorite = sequence.variations.some(v => v.metadata.isFavorite);

  // Get the first variation's thumbnail for display
  $: thumbnailPath = sequence.variations[0]?.thumbnailPath || '';

  // Get difficulty level
  $: difficultyLevel = sequence.metadata.level || 1;

  // Handle click
  function handleClick() {
    dispatch('click');
  }

  // Placeholder image for development
  const placeholderImage = `https://via.placeholder.com/150x150/333333/FFFFFF?text=${sequence.word}`;
</script>

<div
  class="thumbnail"
  class:selected={isSelected}
  on:click={handleClick}
  role="button"
  tabindex="0"
  on:keydown={(e) => e.key === 'Enter' && handleClick()}
>
  <div class="thumbnail-image-container">
    <!-- Use placeholder for development, would use actual thumbnails in production -->
    <img
      src={placeholderImage}
      alt={`Thumbnail for ${sequence.word}`}
      class="thumbnail-image"
    />

    <!-- Difficulty indicator -->
    <div class="difficulty-badge" data-level={difficultyLevel}>
      {difficultyLevel}
    </div>

    <!-- Favorite indicator -->
    {#if hasFavorite}
      <div class="favorite-badge">
        ★
      </div>
    {/if}

    <!-- Variations count badge -->
    {#if sequence.variations.length > 1}
      <div class="variations-badge">
        {sequence.variations.length}
      </div>
    {/if}
  </div>

  <div class="thumbnail-info">
    <h4 class="thumbnail-title">{sequence.word}</h4>
    <div class="thumbnail-metadata">
      <span class="thumbnail-length">{sequence.metadata.length || 0} beats</span>
      {#if sequence.metadata.gridMode}
        <span class="thumbnail-grid-mode">{sequence.metadata.gridMode}</span>
      {/if}
    </div>
  </div>
</div>

<style>
  .thumbnail {
    display: flex;
    flex-direction: column;
    background-color: var(--card-background, #2a2a2a);
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
    cursor: pointer;
    border: 2px solid transparent;
  }

  .thumbnail:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }

  .thumbnail.selected {
    border-color: var(--primary-color, #4a90e2);
    box-shadow: 0 0 0 2px var(--primary-color-transparent, rgba(74, 144, 226, 0.3));
  }

  .thumbnail-image-container {
    position: relative;
    aspect-ratio: 1;
    overflow: hidden;
  }

  .thumbnail-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s;
  }

  .thumbnail:hover .thumbnail-image {
    transform: scale(1.05);
  }

  .difficulty-badge {
    position: absolute;
    top: 8px;
    left: 8px;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: var(--background-color, #1e1e1e);
    color: var(--text-color, #ffffff);
    border-radius: 50%;
    font-size: 0.8rem;
    font-weight: bold;
  }

  .difficulty-badge[data-level="1"] {
    background-color: #4caf50; /* Green */
  }

  .difficulty-badge[data-level="2"] {
    background-color: #8bc34a; /* Light Green */
  }

  .difficulty-badge[data-level="3"] {
    background-color: #ffc107; /* Amber */
  }

  .difficulty-badge[data-level="4"] {
    background-color: #ff9800; /* Orange */
  }

  .difficulty-badge[data-level="5"] {
    background-color: #f44336; /* Red */
  }

  .favorite-badge {
    position: absolute;
    top: 8px;
    right: 8px;
    color: #ffc107; /* Amber */
    font-size: 1.2rem;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
  }

  .variations-badge {
    position: absolute;
    bottom: 8px;
    right: 8px;
    background-color: var(--background-color, #1e1e1e);
    color: var(--text-color, #ffffff);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: bold;
  }

  .thumbnail-info {
    padding: 0.75rem;
  }

  .thumbnail-title {
    margin: 0 0 0.25rem 0;
    font-size: 1rem;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .thumbnail-metadata {
    display: flex;
    gap: 0.5rem;
    font-size: 0.8rem;
    color: var(--text-color-secondary, #aaaaaa);
  }

  .thumbnail-length,
  .thumbnail-grid-mode {
    display: inline-block;
    padding: 2px 6px;
    background-color: var(--tag-background, #2a3a4a);
    border-radius: 4px;
  }
</style>
