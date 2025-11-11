<script lang="ts">
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";
  import { onMount } from "svelte";
  import type { InfoDevContent } from "../domain";

  let {
    panelId,
    labelledBy,
    copy,
    githubUrl,
    discordUrl,
    contactEmail,
  }: {
    panelId: string;
    labelledBy: string;
    copy: InfoDevContent;
    githubUrl: string;
    discordUrl: string;
    contactEmail: string;
  } = $props();

  // Services
  let hapticService: IHapticFeedbackService | null = $state(null);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  function handleLinkClick() {
    hapticService?.trigger("selection");
  }
</script>

<div class="carousel-panel" id={panelId} role="presentation">
  <div class="tab-panel" role="tabpanel" aria-labelledby={labelledBy}>
    <h2 class="panel-title">{copy.subtitle}</h2>
    <p class="dev-message">{copy.message}</p>
    <div class="dev-links">
    <a
      class="dev-card discord-highlight"
      href={discordUrl}
      target="_blank"
      rel="noopener noreferrer"
      onclick={handleLinkClick}
    >
      <i class="fab fa-discord"></i>
      <div>
        <h3>Join Our Discord Community</h3>
        <p>Get help, share feedback, and chat directly with the developer</p>
      </div>
    </a>

    <a
      class="dev-card"
      href={githubUrl}
      target="_blank"
      rel="noopener noreferrer"
      onclick={handleLinkClick}
    >
      <i class="fab fa-github"></i>
      <div>
        <h3>View on GitHub</h3>
        <p>Explore the source code and contribute</p>
      </div>
    </a>

    <a
      class="dev-card"
      href={`${githubUrl}/issues/new`}
      target="_blank"
      rel="noopener noreferrer"
      onclick={handleLinkClick}
    >
      <i class="fas fa-bug"></i>
      <div>
        <h3>Report Bug or Request Feature</h3>
        <p>Help improve TKA with your feedback</p>
      </div>
    </a>
  </div>
  </div>
</div>

<style>
  .carousel-panel {
    display: flex;
    flex-direction: column;
  }

  .tab-panel {
    display: flex;
    flex-direction: column;
    padding: clamp(0.5rem, 1vh, 0.75rem);
  }

  @media (min-width: 1024px) {
    .tab-panel {
      padding: 0;
    }
  }

  .panel-title {
    font-size: clamp(0.75rem, 2cqh, 0.875rem);
    margin-bottom: clamp(0.25rem, 1cqh, 0.375rem);
  }

  @media (min-width: 1024px) {
    .panel-title {
      display: none;
    }
  }

  .dev-message {
    font-size: clamp(0.625rem, 1.5cqh, 0.75rem);
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: clamp(0.25rem, 1cqh, 0.375rem);
    line-height: 1.25;
    text-align: center;
    flex-shrink: 0;
  }

  .dev-links {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: clamp(0.625rem, 2cqh, 1rem);
    width: 100%;
  }

  @media (min-width: 1024px) {
    .dev-links {
      flex: 1;
      justify-content: center;
    }
  }

  .dev-card {
    display: flex;
    align-items: center;
    gap: clamp(0.5rem, 1.5cqh, 0.625rem);
    padding: clamp(0.5rem, 1.5cqh, 0.625rem) clamp(0.625rem, 1.75cqh, 0.75rem);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: clamp(0.375rem, 1.25cqh, 0.5rem);
    text-decoration: none;
    color: inherit;
    transition: all 0.2s ease;
    cursor: pointer;
    width: 100%;
    text-align: left;
  }

  /* Hover only on devices that support it (desktop) */
  @media (hover: hover) and (pointer: fine) {
    .dev-card:hover {
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(34, 197, 94, 0.5);
      transform: translateY(-2px);
      box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }

    .discord-highlight:hover {
      border-color: rgba(88, 101, 242, 0.6);
      box-shadow:
        0 8px 16px rgba(0, 0, 0, 0.2),
        0 0 20px rgba(88, 101, 242, 0.3);
    }
  }

  /* Discord highlight styling */
  .discord-highlight {
    background: rgba(88, 101, 242, 0.08);
    border-color: rgba(88, 101, 242, 0.3);
  }

  .discord-highlight i {
    color: rgba(88, 101, 242, 0.9) !important;
  }

  /* Active state - brief feedback that auto-reverts */
  .dev-card:active {
    background: rgba(255, 255, 255, 0.12);
    transform: translateY(-1px) scale(0.98);
    transition-duration: 0.05s;
  }

  .dev-card:focus-visible {
    outline: 2px solid rgba(34, 197, 94, 0.7);
    outline-offset: 2px;
  }

  .dev-card i {
    font-size: clamp(1.25rem, 3.5cqh, 1.75rem);
    color: rgba(34, 197, 94, 0.9);
    flex-shrink: 0;
  }

  .dev-card div {
    flex: 1;
    min-width: 0;
  }

  .dev-card h3 {
    font-size: clamp(0.6875rem, 1.75cqh, 0.8125rem);
    font-weight: 600;
    color: white;
    margin: 0 0 0.125rem 0;
    line-height: 1.2;
  }

  .dev-card p {
    font-size: clamp(0.625rem, 1.5cqh, 0.75rem);
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
    line-height: 1.25;
  }

  @media (prefers-reduced-motion: reduce) {
    .dev-card:hover,
    .dev-card:active {
      transform: none;
    }
  }
</style>
