<script lang="ts">
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";
  import { onMount } from "svelte";
  import type { LandingDevContent } from "../domain";

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
    copy: LandingDevContent;
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
        href={discordUrl}
        target="_blank"
        rel="noopener noreferrer"
        onclick={handleLinkClick}
      >
        <i class="fab fa-discord"></i>
        <div>
          <h3>Join Discord</h3>
          <p>Chat with the community and dev team</p>
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

      <a
        class="dev-card"
        href={`mailto:${contactEmail}?subject=TKA Development Inquiry`}
        onclick={handleLinkClick}
      >
        <i class="fas fa-envelope"></i>
        <div>
          <h3>Email Us</h3>
          <p>Direct email for partnerships or questions</p>
        </div>
      </a>
    </div>
  </div>
</div>

<style>
  .dev-links {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.75rem;
    width: 100%;
  }

  .dev-message {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: 0.75rem;
    line-height: 1.45;
    text-align: center;
    flex-shrink: 0;
  }

  @media (min-width: 640px) {
    .dev-message {
      font-size: clamp(0.875rem, 2vw, 1rem);
      margin-bottom: clamp(1rem, 2vh, 1.5rem);
      line-height: 1.5;
    }
  }

  @media (min-width: 640px) {
    .dev-links {
      gap: clamp(1rem, 2vh, 1.5rem);
    }
  }

  .dev-card {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0.75rem;
    text-decoration: none;
    color: inherit;
    transition: all 0.2s ease;
    cursor: pointer;
    width: 100%;
    text-align: left;
  }

  @media (min-width: 640px) {
    .dev-card {
      gap: clamp(1rem, 2vw, 1.5rem);
      padding: clamp(1rem, 2.5vh, 1.5rem);
      min-height: 80px;
    }
  }

  /* Hover only on devices that support it (desktop) */
  @media (hover: hover) and (pointer: fine) {
    .dev-card:hover {
      background: rgba(255, 255, 255, 0.08);
      border-color: rgba(34, 197, 94, 0.5);
      transform: translateY(-2px);
      box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
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
    font-size: 1.75rem;
    color: rgba(34, 197, 94, 0.9);
    flex-shrink: 0;
  }

  @media (min-width: 640px) {
    .dev-card i {
      font-size: clamp(2rem, 5vw, 2.5rem);
    }
  }

  .dev-card div {
    flex: 1;
    min-width: 0;
  }

  .dev-card h3 {
    font-size: 0.9375rem;
    font-weight: 600;
    color: white;
    margin: 0 0 0.125rem 0;
  }

  @media (min-width: 640px) {
    .dev-card h3 {
      font-size: clamp(1rem, 2.5vw, 1.125rem);
      margin: 0 0 0.25rem 0;
    }
  }

  .dev-card p {
    font-size: 0.8125rem;
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
    line-height: 1.35;
  }

  @media (min-width: 640px) {
    .dev-card p {
      font-size: clamp(0.875rem, 2vw, 1rem);
      line-height: 1.4;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .dev-card:hover,
    .dev-card:active {
      transform: none;
    }
  }
</style>
