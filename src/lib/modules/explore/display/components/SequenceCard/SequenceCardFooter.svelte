<!--
SequenceCardFooter - Footer component for SequenceCard

Contains the metadata section with:
- Overflow menu (left)
- Title (center)
- Favorite button (right)

Applies difficulty-based background styling.
-->
<script lang="ts">
  import SequenceCardOverflowMenu from "./SequenceCardOverflowMenu.svelte";
  import SequenceCardFavoriteButton from "./SequenceCardFavoriteButton.svelte";

  const {
    title,
    levelStyle,
    isFavorite = false,
    menuOpen = false,
    menuId,
    onFavoriteToggle = () => {},
    onMenuToggle = () => {},
    onMenuItemSelect = () => {},
  } = $props<{
    title: string;
    levelStyle: { background: string; textColor: string };
    isFavorite?: boolean;
    menuOpen?: boolean;
    menuId: string;
    onFavoriteToggle?: () => void;
    onMenuToggle?: () => void;
    onMenuItemSelect?: (action: string) => void;
  }>();
</script>

<div
  class="metadata"
  style="background: {levelStyle.background}; color: {levelStyle.textColor};"
>
  <div class="actions-row">
    <SequenceCardOverflowMenu
      isOpen={menuOpen}
      {menuId}
      onToggle={onMenuToggle}
      onSelectItem={onMenuItemSelect}
    />

    <div class="title-slot">
      <p class="title" title={title}>{title}</p>
    </div>

    <SequenceCardFavoriteButton
      {isFavorite}
      onToggle={onFavoriteToggle}
    />
  </div>
</div>

<style>
  .metadata {
    padding: 12px;
    display: flex;
    flex-direction: column;
    gap: 0;
  }

  .actions-row {
    display: grid;
    grid-template-columns: 44px 1fr 44px;
    align-items: center;
    gap: 12px;
  }

  .title-slot {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .title {
    font-size: 1.35rem;
    font-weight: 700;
    text-align: center;
    margin: 0;
    line-height: 1.2;
  }

  /* Container query responsive sizing */
  @container sequence-card (max-width: 249px) {
    .title {
      font-size: 1rem;
    }

    .actions-row {
      grid-template-columns: 36px 1fr 36px;
      gap: 8px;
    }

    .metadata {
      padding: 10px;
    }
  }

  @container sequence-card (min-width: 250px) and (max-width: 299px) {
    .title {
      font-size: 1.15rem;
    }

    .actions-row {
      grid-template-columns: 40px 1fr 40px;
      gap: 10px;
    }

    .metadata {
      padding: 11px;
    }
  }

  @container sequence-card (min-width: 300px) {
    .title {
      font-size: 1.35rem;
    }
  }
</style>
