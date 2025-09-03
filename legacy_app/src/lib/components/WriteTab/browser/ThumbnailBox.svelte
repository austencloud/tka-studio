<script lang="ts">
  import { onMount } from 'svelte';
	import ThumbnailImage from './ThumbnailImage.svelte';

  export let word: string;
  export let thumbnails: string[] = [];

  let currentIndex = 0;

  function nextThumbnail() {
    if (thumbnails.length > 1) {
      currentIndex = (currentIndex + 1) % thumbnails.length;
    }
  }

  function prevThumbnail() {
    if (thumbnails.length > 1) {
      currentIndex = (currentIndex - 1 + thumbnails.length) % thumbnails.length;
    }
  }
</script>

<div class="thumbnail-box">
  <div class="thumbnail-header">
    <h3 class="thumbnail-title">{word}</h3>

    {#if thumbnails.length > 1}
      <div class="thumbnail-nav">
        <button
          class="nav-button"
          on:click={prevThumbnail}
          aria-label="Previous thumbnail"
        >
          ◀
        </button>
        <span class="thumbnail-counter">{currentIndex + 1}/{thumbnails.length}</span>
        <button
          class="nav-button"
          on:click={nextThumbnail}
          aria-label="Next thumbnail"
        >
          ▶
        </button>
      </div>
    {/if}
  </div>

  <div class="thumbnail-container">
    {#if thumbnails.length > 0}
      <ThumbnailImage
        src={thumbnails[currentIndex]}
        alt={`${word} thumbnail ${currentIndex + 1}`}
        {word}
      />
    {:else}
      <div class="empty-thumbnail">
        <span>No thumbnail available</span>
      </div>
    {/if}
  </div>
</div>

<style>
  .thumbnail-box {
    display: flex;
    flex-direction: column;
    background-color: #2a2a2a;
    border-radius: 6px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    transition: transform 0.2s, box-shadow 0.2s;
  }

  .thumbnail-box:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
  }

  .thumbnail-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0.75rem;
    background-color: #333;
  }

  .thumbnail-title {
    font-size: 1rem;
    font-weight: 500;
    margin: 0;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .thumbnail-nav {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    font-size: 0.75rem;
  }

  .nav-button {
    background: none;
    border: none;
    color: #ccc;
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 4px;
    line-height: 1;
    transition: color 0.2s, background-color 0.2s;
  }

  .nav-button:hover {
    color: #fff;
    background-color: rgba(255, 255, 255, 0.1);
  }

  .thumbnail-counter {
    color: #999;
    font-size: 0.75rem;
  }

  .thumbnail-container {
    position: relative;
    aspect-ratio: 4/3;
    background-color: #222;
  }

  .empty-thumbnail {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    color: #666;
    font-style: italic;
  }
</style>
