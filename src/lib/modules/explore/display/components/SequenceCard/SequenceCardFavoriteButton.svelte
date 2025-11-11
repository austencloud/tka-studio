<!--
SequenceCardFavoriteButton - Favorite button component

Displays a star button that toggles favorite status.
Handles click events and accessibility.
-->
<script lang="ts">
  const {
    isFavorite = false,
    onToggle = () => {},
  } = $props<{
    isFavorite?: boolean;
    onToggle?: () => void;
  }>();

  function handleClick(e: MouseEvent) {
    e.stopPropagation();
    onToggle();
  }
</script>

<div class="icon-slot">
  <button
    type="button"
    class="favorite"
    aria-label={isFavorite ? "Remove from favorites" : "Add to favorites"}
    aria-pressed={isFavorite}
    onclick={handleClick}
  >
    {isFavorite ? "★" : "☆"}
  </button>
</div>

<style>
  .icon-slot {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .favorite {
    min-width: 44px;
    min-height: 44px;
    border: none;
    border-radius: 999px;
    background: rgba(17, 17, 23, 0.7);
    color: #fff;
    font-size: 1.25rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition:
      background 0.2s ease,
      transform 0.2s ease;
  }

  .favorite:hover,
  .favorite:focus-visible {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
    outline: none;
  }

  .favorite:active {
    transform: translateY(0);
  }

  /* Container query responsive sizing */
  @container sequence-card (max-width: 249px) {
    .favorite {
      min-width: 36px;
      min-height: 36px;
      font-size: 1rem;
    }
  }

  @container sequence-card (min-width: 250px) and (max-width: 299px) {
    .favorite {
      min-width: 40px;
      min-height: 40px;
      font-size: 1.15rem;
    }
  }
</style>
