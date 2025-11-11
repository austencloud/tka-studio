<!--
SequenceCardOverflowMenu - Overflow menu component

Displays a three-dot menu with Edit, Animate, and Delete options.
Handles click-outside behavior and accessibility.
-->
<script lang="ts">
  const {
    isOpen = false,
    menuId,
    onToggle = () => {},
    onSelectItem = () => {},
  } = $props<{
    isOpen?: boolean;
    menuId: string;
    onToggle?: () => void;
    onSelectItem?: (action: string) => void;
  }>();

  function handleMenuClick(e: MouseEvent) {
    e.stopPropagation();
    onToggle();
  }

  function handleItemClick(action: string, e: MouseEvent) {
    e.stopPropagation();
    onSelectItem(action);
  }
</script>

<div class="icon-slot">
  <button
    type="button"
    class="overflow"
    aria-haspopup="true"
    aria-expanded={isOpen}
    aria-controls={menuId}
    onclick={handleMenuClick}
  >
    ⋮
  </button>

  {#if isOpen}
    <ul class="menu" role="menu" id={menuId}>
      <li role="presentation">
        <button
          role="menuitem"
          onclick={(e) => handleItemClick("edit", e)}
        >
          Edit
        </button>
      </li>
      <li role="presentation">
        <button
          role="menuitem"
          onclick={(e) => handleItemClick("animate", e)}
        >
          Animate
        </button>
      </li>
      <li role="presentation">
        <button
          role="menuitem"
          onclick={(e) => handleItemClick("delete", e)}
        >
          Delete
        </button>
      </li>
    </ul>
  {/if}
</div>

<style>
  .icon-slot {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .overflow {
    min-width: 44px;
    min-height: 44px;
    border: none;
    border-radius: 999px;
    background: rgba(17, 17, 23, 0.7);
    color: #fff;
    font-size: 1.5rem;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition:
      background 0.2s ease,
      transform 0.2s ease;
  }

  .overflow:hover,
  .overflow:focus-visible {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
    outline: none;
  }

  .overflow:active {
    transform: translateY(0);
  }

  .menu {
    position: absolute;
    top: calc(100% + 8px);
    right: 0;
    background: rgba(10, 10, 14, 0.98);
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
    list-style: none;
    padding: 6px;
    margin: 0;
    min-width: 160px;
    z-index: 10;
    animation: menuSlideIn 0.15s ease-out;
  }

  @keyframes menuSlideIn {
    from {
      opacity: 0;
      transform: translateY(-8px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .menu button {
    width: 100%;
    background: transparent;
    color: #fff;
    border: none;
    padding: 10px 14px;
    text-align: left;
    cursor: pointer;
    border-radius: 8px;
    font-size: 0.95rem;
    transition: background 0.15s ease;
  }

  .menu button:hover,
  .menu button:focus-visible {
    background: rgba(255, 255, 255, 0.12);
    outline: 2px solid rgba(255, 255, 255, 0.2);
    outline-offset: -2px;
  }

  .menu button:active {
    background: rgba(255, 255, 255, 0.08);
  }

  /* Container query responsive sizing */
  @container sequence-card (max-width: 249px) {
    .overflow {
      min-width: 36px;
      min-height: 36px;
      font-size: 1.2rem;
    }
  }

  @container sequence-card (min-width: 250px) and (max-width: 299px) {
    .overflow {
      min-width: 40px;
      min-height: 40px;
      font-size: 1.35rem;
    }
  }
</style>
