<!--
  MethodCard.svelte

  A single creation method card for the method selector.
  Displays an icon, title, and description for a creation mode option.
-->
<script lang="ts">
  import { fly } from "svelte/transition";
  import type { BuildModeId } from "$shared";

  let {
    id,
    icon,
    title,
    description,
    color,
    index,
    isDisabled = false,
    onclick,
  }: {
    id: BuildModeId;
    icon: string;
    title: string;
    description: string;
    color: string;
    index: number;
    isDisabled?: boolean;
    onclick: (event: MouseEvent) => void;
  } = $props();
</script>

<button
  class="method-card"
  class:disabled={isDisabled}
  data-method-id={id}
  data-method-index={index}
  {onclick}
  in:fly={{ y: 20, delay: 200 + index * 100, duration: 300 }}
  style="--method-color: {color}"
  aria-disabled={isDisabled}
  disabled={isDisabled}
>
  <div class="method-icon">
    <i class="fas {icon}"></i>
  </div>
  <div class="method-content">
    <h3 class="method-title">{title}</h3>
    <p class="method-description">{description}</p>
  </div>
  {#if isDisabled}
    <div class="coming-soon-badge">Coming Soon</div>
  {:else}
    <div class="method-arrow">
      <i class="fas fa-chevron-right"></i>
    </div>
  {/if}
</button>

<style>
  .method-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: clamp(0.75rem, 2vh, 1rem);
    padding: clamp(1.25rem, 3vh, 1.75rem) clamp(1rem, 2.5vh, 1.5rem);

    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;

    cursor: pointer;
    transition: all 220ms cubic-bezier(0.4, 0, 0.2, 1);
    text-align: center;
    position: relative;
    overflow: hidden;
    aspect-ratio: 1 / 1.1;

    /* Consistent sizing that scales with container */
    width: clamp(180px, 22vw, 250px);
    min-width: 180px;
    max-width: 250px;
  }

  .method-card::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(
      circle at 50% 30%,
      var(--method-color, rgba(255, 255, 255, 0.1)) 0%,
      transparent 65%
    );
    opacity: 0;
    transition: opacity 220ms ease;
  }

  .method-card::after {
    content: "";
    position: absolute;
    inset: -1px;
    background: linear-gradient(
      135deg,
      var(--method-color, rgba(255, 255, 255, 0.2)) 0%,
      transparent 50%
    );
    border-radius: 16px;
    opacity: 0;
    transition: opacity 220ms ease;
    z-index: -1;
  }

  .method-card:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.15);
    transform: translateY(-2px);
  }

  .method-card:hover::before {
    opacity: 0.12;
  }

  .method-card:hover::after {
    opacity: 1;
  }

  .method-card:active {
    transform: translateY(0);
  }

  .method-icon {
    font-size: clamp(2rem, 6cqi, 2.75rem);
    line-height: 1;
    color: var(--method-color, rgba(255, 255, 255, 0.9));
    flex-shrink: 0;
    width: clamp(3.5rem, 12cqi, 4.5rem);
    height: clamp(3.5rem, 12cqi, 4.5rem);
    display: grid;
    place-items: center;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 12px;
    transition: all 220ms cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
  }

  .method-icon::before {
    content: "";
    position: absolute;
    inset: 0;
    background: var(--method-color, rgba(255, 255, 255, 0.1));
    opacity: 0.08;
    border-radius: 12px;
  }

  .method-card:hover .method-icon {
    transform: scale(1.05);
    background: rgba(255, 255, 255, 0.08);
  }

  .method-content {
    display: flex;
    flex-direction: column;
    gap: clamp(0.25rem, 1cqi, 0.375rem);
    flex: 1;
    justify-content: center;
  }

  .method-title {
    font-size: clamp(1.125rem, 5cqi, 1.5rem);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
    line-height: 1.3;
  }

  .method-description {
    font-size: clamp(0.8125rem, 3.5cqi, 0.9375rem);
    font-weight: 400;
    color: rgba(255, 255, 255, 0.5);
    margin: 0;
    line-height: 1.4;
  }

  .method-arrow {
    position: absolute;
    bottom: clamp(0.875rem, 2vh, 1.125rem);
    right: clamp(0.875rem, 2vh, 1.125rem);
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.2);
    transition: all 220ms ease;
  }

  .method-card:hover .method-arrow {
    color: var(--method-color, rgba(255, 255, 255, 0.5));
    transform: translate(2px, -2px);
  }

  /* Disabled state */
  .method-card.disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  .method-card.disabled:hover {
    background: rgba(255, 255, 255, 0.03);
    border-color: rgba(255, 255, 255, 0.08);
    transform: none;
  }

  .method-card.disabled::before,
  .method-card.disabled::after {
    display: none;
  }

  .method-card.disabled .method-icon {
    opacity: 0.7;
  }

  .coming-soon-badge {
    position: absolute;
    top: clamp(0.875rem, 2vh, 1.125rem);
    right: clamp(0.875rem, 2vh, 1.125rem);
    font-size: 0.6875rem;
    font-weight: 700;
    text-transform: uppercase;
    padding: 0.375rem 0.625rem;
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.12);
    color: rgba(255, 255, 255, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.2);
    letter-spacing: 0.5px;
  }

  /* Mobile: constrain width and remove aspect ratio */
  @media (max-width: 599px) {
    .method-card {
      max-width: 280px;
      margin: 0 auto;
      aspect-ratio: auto;
    }
  }

  /* Extra small screens: horizontal layout */
  @media (max-width: 400px) {
    .method-card {
      flex-direction: row;
      aspect-ratio: auto;
      text-align: left;
      padding: 1rem 1.25rem;
      max-width: 100%;
    }

    .method-content {
      align-items: flex-start;
    }

    .method-arrow {
      position: static;
      margin-left: auto;
    }

    .coming-soon-badge {
      position: static;
      margin-left: auto;
      font-size: 0.625rem;
      padding: 0.25rem 0.5rem;
    }
  }
</style>
