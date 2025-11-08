<!--
IconGrid.svelte - Premium icon picker component
Provides a beautiful, consistent icon selection experience
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  let {
    selectedIcon = $bindable(),
    availableIcons = [
      "⚙️",
      "⭐",
      "🎯",
      "🔥",
      "💫",
      "✨",
      "🎪",
      "🎭",
      "🎨",
      "🌟",
      "💎",
      "🏆",
    ],
    label = "Choose an Icon",
  } = $props<{
    selectedIcon: string;
    availableIcons?: string[];
    label?: string;
  }>();

  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  function selectIcon(icon: string) {
    hapticService?.trigger("selection");
    selectedIcon = icon;
  }
</script>

<div class="icon-picker">
  <div class="icon-label">{label}</div>
  <div class="icon-grid" role="group" aria-label="Icon selection">
    {#each availableIcons as icon}
      <button
        class="icon-button"
        class:selected={selectedIcon === icon}
        onclick={() => selectIcon(icon)}
        aria-label={`Select icon ${icon}`}
        aria-pressed={selectedIcon === icon}
      >
        <span class="icon-emoji">{icon}</span>
      </button>
    {/each}
  </div>
</div>

<style>
  .icon-picker {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .icon-label {
    color: rgba(255, 255, 255, 0.9);
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.01em;
  }

  .icon-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 10px;
  }

  .icon-button {
    aspect-ratio: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.08),
      rgba(255, 255, 255, 0.03)
    );
    border: 2px solid rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    padding: 0;
    position: relative;
    overflow: hidden;
  }

  .icon-button::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(
      circle at center,
      rgba(255, 255, 255, 0.1) 0%,
      transparent 70%
    );
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .icon-button:hover::before {
    opacity: 1;
  }

  .icon-button:hover {
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.12),
      rgba(255, 255, 255, 0.06)
    );
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
    box-shadow:
      0 4px 12px rgba(0, 0, 0, 0.15),
      0 0 0 1px rgba(255, 255, 255, 0.1) inset;
  }

  .icon-button:active {
    transform: translateY(0);
  }

  .icon-button.selected {
    background: linear-gradient(
      135deg,
      rgba(59, 130, 246, 0.3),
      rgba(37, 99, 235, 0.2)
    );
    border-color: rgba(59, 130, 246, 0.6);
    box-shadow:
      0 0 0 3px rgba(59, 130, 246, 0.2),
      0 4px 12px rgba(59, 130, 246, 0.3);
  }

  .icon-button.selected:hover {
    background: linear-gradient(
      135deg,
      rgba(59, 130, 246, 0.4),
      rgba(37, 99, 235, 0.3)
    );
    border-color: rgba(59, 130, 246, 0.7);
  }

  .icon-emoji {
    font-size: 28px;
    line-height: 1;
    position: relative;
    z-index: 1;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
  }

  @media (max-width: 640px) {
    .icon-grid {
      gap: 8px;
    }

    .icon-emoji {
      font-size: 24px;
    }

    .icon-button {
      border-radius: 10px;
    }
  }
</style>
