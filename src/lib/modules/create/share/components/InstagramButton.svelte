<!--
InstagramButton.svelte

Button component for Instagram integration.
Shows different states: no link, has link, opening link.
-->
<script lang="ts">
  import { onMount } from "svelte";
  import type { IInstagramLinkService, IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import type { InstagramLink } from "../domain";

  let {
    instagramLink = null,
    disabled = false,
    onAddLink,
    onEditLink,
  }: {
    instagramLink?: InstagramLink | null;
    disabled?: boolean;
    onAddLink?: () => void;
    onEditLink?: () => void;
  } = $props();

  // Services
  let instagramService: IInstagramLinkService;
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    instagramService = resolve<IInstagramLinkService>(TYPES.IInstagramLinkService);
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

  // Handle button click
  function handleClick() {
    if (disabled) return;

    hapticService?.trigger("selection");

    if (instagramLink) {
      // Open Instagram link
      instagramService.openInstagramPost(instagramLink.url, true);
    } else {
      // Open add link modal
      onAddLink?.();
    }
  }

  // Handle edit button click
  function handleEdit(event: MouseEvent) {
    event.stopPropagation();
    hapticService?.trigger("selection");
    onEditLink?.();
  }

  // Computed properties
  let hasLink = $derived(() => instagramLink !== null);
  let buttonText = $derived(() => {
    if (hasLink()) {
      return "View on Instagram";
    }
    return "Link Instagram";
  });
</script>

<div class="instagram-button-container">
  <button
    class="instagram-button"
    class:has-link={hasLink()}
    class:disabled
    onclick={handleClick}
    {disabled}
  >
    <i class="fa-brands fa-instagram"></i>
    <span class="button-text">{buttonText()}</span>
  </button>

  {#if hasLink() && !disabled}
    <button
      class="edit-button"
      onclick={handleEdit}
      aria-label="Edit Instagram link"
      title="Edit Instagram link"
    >
      <i class="fa-solid fa-pencil"></i>
    </button>
  {/if}
</div>

<style>
  .instagram-button-container {
    display: flex;
    gap: 0.5rem;
    align-items: stretch;
  }

  .instagram-button {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.625rem 1rem;
    border: 1px solid var(--border-color);
    border-radius: 6px;
    background: var(--bg-secondary);
    color: var(--text-primary);
    font-size: 0.9rem;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
    flex: 1;
  }

  .instagram-button:hover:not(.disabled) {
    background: var(--bg-tertiary);
    border-color: #E4405F;
    color: #E4405F;
  }

  .instagram-button.has-link {
    background: linear-gradient(45deg, #f09433 0%, #e6683c 25%, #dc2743 50%, #cc2366 75%, #bc1888 100%);
    color: white;
    border: none;
  }

  .instagram-button.has-link:hover:not(.disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(228, 64, 95, 0.3);
  }

  .instagram-button.disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
  }

  .instagram-button i {
    font-size: 1.1rem;
  }

  .button-text {
    white-space: nowrap;
  }

  .edit-button {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0.625rem;
    border: 1px solid var(--border-color);
    border-radius: 6px;
    background: var(--bg-secondary);
    color: var(--text-secondary);
    font-size: 0.9rem;
    cursor: pointer;
    transition: all 0.2s;
    min-width: 40px;
  }

  .edit-button:hover {
    background: var(--bg-tertiary);
    color: var(--text-primary);
    border-color: var(--accent-color);
  }

  /* Mobile responsive */
  @media (max-width: 640px) {
    .button-text {
      display: none;
    }

    .instagram-button {
      padding: 0.625rem;
      min-width: 40px;
      justify-content: center;
    }
  }
</style>

