<!--
SequenceCardMedia - Media display component for SequenceCard

Displays either an image or a placeholder based on whether coverUrl is provided.
Handles image dimensions for layout shift prevention.
-->
<script lang="ts">
  const {
    coverUrl = undefined,
    word,
    width = undefined,
    height = undefined,
  } = $props<{
    coverUrl?: string | undefined;
    word: string;
    width?: number | undefined;
    height?: number | undefined;
  }>();
</script>

<div class="media">
  {#if coverUrl}
    <img
      src={coverUrl}
      alt={`Preview of ${word}`}
      width={width}
      height={height}
      loading="lazy"
    />
  {:else}
    <div class="media-placeholder" aria-label="Sequence preview missing">
      <span>{word.slice(0, 1) ?? "?"}</span>
    </div>
  {/if}
</div>

<style>
  .media {
    position: relative;
    width: 100%;
    background: rgba(255, 255, 255, 0.05);
    flex: 1;
    min-height: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .media img {
    width: 100%;
    height: auto;
    display: block;
    max-width: 100%;
  }

  .media-placeholder {
    width: 100%;
    aspect-ratio: 4 / 3;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #1f2937, #111827);
    font-size: 4rem;
    font-weight: 700;
  }

  /* Container query responsive sizing */
  @container sequence-card (max-width: 249px) {
    .media-placeholder {
      font-size: 2.5rem;
    }
  }

  @container sequence-card (min-width: 250px) and (max-width: 299px) {
    .media-placeholder {
      font-size: 3.25rem;
    }
  }
</style>
