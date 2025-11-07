<script lang="ts">
  import type { LandingSupportContent, SupportOption } from "../domain";

  let {
    panelId,
    labelledBy,
    copy,
    supportOptions = [],
  }: {
    panelId: string;
    labelledBy: string;
    copy: LandingSupportContent;
    supportOptions?: SupportOption[];
  } = $props();
</script>

<div class="carousel-panel" id={panelId} role="presentation">
  <div class="tab-panel" role="tabpanel" aria-labelledby={labelledBy}>
    <h2 class="panel-title">{copy.subtitle}</h2>
    <p class="support-message">{copy.message}</p>
    <div class="support-grid">
      {#each supportOptions as option}
        <a
          class="support-button"
          href={option.url}
          target="_blank"
          rel="noopener noreferrer"
          style="--brand-color: {option.color}"
        >
          <i class={option.icon}></i>
          <span>Donate via {option.name}</span>
        </a>
      {/each}
    </div>
  </div>
</div>

<style>
  .support-message {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: 0.75rem;
    line-height: 1.45;
    text-align: center;
    flex-shrink: 0;
  }

  @media (min-width: 640px) {
    .support-message {
      font-size: clamp(0.875rem, 2vw, 1rem);
      margin-bottom: clamp(1rem, 2vh, 1.5rem);
      line-height: 1.5;
    }
  }

  .support-grid {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    width: 100%;
  }

  @media (min-width: 640px) {
    .support-grid {
      gap: clamp(1rem, 2.5vh, 1.5rem);
    }
  }

  .support-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.625rem;
    padding: 1rem 1.5rem;
    min-height: 56px;
    width: 100%;
    background: linear-gradient(
      135deg,
      var(--brand-color) 0%,
      color-mix(in srgb, var(--brand-color) 80%, black) 100%
    );
    border: 2px solid color-mix(in srgb, var(--brand-color) 60%, white);
    border-radius: 1rem;
    text-decoration: none;
    color: white;
    font-weight: 700;
    font-size: 0.9375rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow:
      0 6px 20px color-mix(in srgb, var(--brand-color) 40%, transparent),
      0 2px 8px rgba(0, 0, 0, 0.3),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    position: relative;
    overflow: hidden;
  }

  @media (min-width: 640px) {
    .support-button {
      gap: clamp(0.75rem, 2vw, 1rem);
      padding: clamp(1.25rem, 3vh, 1.75rem) clamp(2rem, 4vw, 2.5rem);
      min-height: 68px;
      font-size: clamp(1rem, 2.75vw, 1.1875rem);
    }
  }

  .support-button::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.2),
      transparent
    );
    transition: left 0.5s ease;
  }

  .support-button:hover::before {
    left: 100%;
  }

  .support-button:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow:
      0 10px 30px color-mix(in srgb, var(--brand-color) 50%, transparent),
      0 4px 12px rgba(0, 0, 0, 0.4),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
    border-color: color-mix(in srgb, var(--brand-color) 80%, white);
    filter: brightness(1.15) saturate(1.1);
  }

  .support-button:active {
    transform: translateY(-1px) scale(1.01);
    box-shadow:
      0 6px 20px color-mix(in srgb, var(--brand-color) 40%, transparent),
      0 2px 8px rgba(0, 0, 0, 0.3),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }

  .support-button:focus-visible {
    outline: 3px solid rgba(255, 255, 255, 0.6);
    outline-offset: 3px;
  }

  .support-button i {
    font-size: 1.25rem;
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
    transition: transform 0.3s ease;
  }

  @media (min-width: 640px) {
    .support-button i {
      font-size: clamp(1.5rem, 3.5vw, 1.875rem);
    }
  }

  .support-button:hover i {
    transform: scale(1.15) rotate(-5deg);
  }

  @media (min-width: 640px) {
    .support-grid {
      flex-direction: row;
      gap: clamp(1rem, 2vw, 1.5rem);
    }

    .support-button {
      flex: 1;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .support-button:hover,
    .support-button:active,
    .support-button:hover i {
      transform: none;
    }

    .support-button::before {
      display: none;
    }
  }
</style>
