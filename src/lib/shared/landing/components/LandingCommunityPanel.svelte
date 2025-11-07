<script lang="ts">
  import type { LandingPanelContent, SocialLink } from "../domain";

  let {
    panelId,
    labelledBy,
    copy,
    socialLinks = [],
    onSocialClick = () => {},
  }: {
    panelId: string;
    labelledBy: string;
    copy: LandingPanelContent;
    socialLinks?: SocialLink[];
    onSocialClick?: (event: MouseEvent, social: SocialLink) => void;
  } = $props();
</script>

<div class="carousel-panel" id={panelId} role="presentation">
  <div
    class="tab-panel"
    role="tabpanel"
    aria-labelledby={labelledBy}
    aria-label={copy.title}
  >
    <div class="social-grid">
      {#each socialLinks as social}
        <a
          class="social-button"
          href={social.url}
          target="_blank"
          rel="noopener noreferrer"
          style="--brand-color: {social.color}"
          title={social.name}
          onclick={(event) => onSocialClick(event, social)}
        >
          <i class={social.icon}></i>
          <span>{social.name}</span>
        </a>
      {/each}
    </div>
  </div>
</div>

<style>
  .social-grid {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    width: 100%;
  }

  .social-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.375rem;
    padding: 0.625rem 0.5rem;
    min-height: 70px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0.75rem;
    text-decoration: none;
    color: white;
    transition: all 0.2s ease;
  }

  .social-button:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: var(--brand-color);
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  }

  .social-button i {
    font-size: 1.5rem;
    color: var(--brand-color);
    filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.3));
  }

  .social-button span {
    font-size: 0.8125rem;
    font-weight: 600;
  }

  @media (min-width: 640px) {
    .social-grid {
      flex-direction: row;
      gap: clamp(1rem, 2vw, 1.5rem);
    }

    .social-button {
      flex: 1;
      min-height: 108px;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .social-button:hover {
      transform: none;
    }
  }
</style>
