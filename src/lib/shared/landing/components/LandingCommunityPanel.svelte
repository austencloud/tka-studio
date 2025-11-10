<script lang="ts">
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";
  import { onMount } from "svelte";
  import type {
    LandingPanelContent,
    SocialLink,
    SupportOption,
  } from "../domain";

  let {
    panelId,
    labelledBy,
    copy,
    socialLinks = [],
    supportOptions = [],
    onSocialClick = () => {},
    onSupportClick = () => {},
  }: {
    panelId: string;
    labelledBy: string;
    copy: LandingPanelContent;
    socialLinks?: SocialLink[];
    supportOptions?: SupportOption[];
    onSocialClick?: (event: MouseEvent, social: SocialLink) => void;
    onSupportClick?: (event: MouseEvent, support: SupportOption) => void;
  } = $props();

  // Services
  let hapticService: IHapticFeedbackService | null = $state(null);

  // State for copy feedback
  let copiedEmail = $state(false);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  function handleSocialClick(event: MouseEvent, social: SocialLink) {
    hapticService?.trigger("selection");
    onSocialClick(event, social);
  }

  async function handleSupportClick(event: MouseEvent, support: SupportOption) {
    hapticService?.trigger("selection");

    // Special handling for Zelle - copy email to clipboard
    if (support.name === "Zelle") {
      event.preventDefault(); // Prevent default link behavior

      try {
        await navigator.clipboard.writeText(support.url);
        copiedEmail = true;

        // Reset after 2.5 seconds
        setTimeout(() => {
          copiedEmail = false;
        }, 2500);
      } catch (error) {
        console.error("Failed to copy email:", error);
        // Fallback: open mailto as original behavior
        window.location.href = `mailto:${support.url}?subject=Zelle%20Donation`;
      }
      return;
    }

    onSupportClick(event, support);
  }
</script>

<div class="carousel-panel" id={panelId} role="presentation">
  <div
    class="tab-panel"
    role="tabpanel"
    aria-labelledby={labelledBy}
    aria-label={copy.title}
  >
    <div class="community-content">
      <!-- Social Media Section -->
      <section class="community-section">
        <h3 class="section-title">Follow & Share</h3>
        <p class="section-description">Stay connected and spread the word</p>
        <div class="button-grid">
          {#each socialLinks as social}
            <a
              class="community-button"
              href={social.url}
              target="_blank"
              rel="noopener noreferrer"
              style="--brand-color: {social.color}"
              title={social.name}
              onclick={(event) => handleSocialClick(event, social)}
            >
              <div class="icon-circle">
                <i class={social.icon}></i>
              </div>
              <span class="button-label">{social.name}</span>
            </a>
          {/each}
        </div>
      </section>

      <!-- Support Section -->
      <section class="community-section">
        <h3 class="section-title">Support with a Donation</h3>
        <p class="section-description">Help fund hosting and development</p>
        <div class="button-grid">
          {#each supportOptions as support}
            <a
              class="community-button"
              class:copied={support.name === "Zelle" && copiedEmail}
              href={support.name === "Zelle" ? "#" : support.url}
              target={support.name === "Zelle" ? undefined : "_blank"}
              rel={support.name === "Zelle" ? undefined : "noopener noreferrer"}
              style="--brand-color: {support.color}"
              title={support.name === "Zelle"
                ? copiedEmail
                  ? "Email copied! Paste in your bank's Zelle app"
                  : "Copy email to use in your bank's Zelle app"
                : support.name}
              onclick={(event) => handleSupportClick(event, support)}
            >
              <div class="icon-circle">
                <i class={support.icon}></i>
              </div>
              <span class="button-label">
                {#if support.name === "Zelle" && copiedEmail}
                  <span class="copied-label">
                    <i class="fas fa-check-circle"></i>
                    Email Copied!
                  </span>
                {:else if support.name === "Zelle"}
                  <span class="zelle-label">
                    Zelle
                    <span class="copy-hint">(tap to copy)</span>
                  </span>
                {:else}
                  {support.name}
                {/if}
              </span>
            </a>
          {/each}
        </div>
      </section>
    </div>
  </div>
</div>

<style>
  .community-content {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    padding: 1rem;
    height: 100%;
    overflow-y: auto;
  }

  .community-section {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .section-title {
    font-size: 1.125rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    margin: 0;
    padding-left: 0.25rem;
    text-align: center;
  }

  .section-description {
    font-size: 0.875rem;
    font-weight: 400;
    color: rgba(255, 255, 255, 0.6);
    margin: -0.5rem 0 0 0;
    padding-left: 0.25rem;
    font-style: italic;
    text-align: center;
  }

  .button-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
  }

  .community-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    padding: 1.25rem 0.75rem;
    text-decoration: none;
    color: white;
    position: relative;

    /* Simplified glass card */
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.08) 0%,
      rgba(255, 255, 255, 0.04) 100%
    );
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1rem;

    /* Unified smooth transition - no bounce chaos */
    transition: all 0.3s ease;
  }

  /* Hover only on devices that support it (desktop) */
  @media (hover: hover) and (pointer: fine) {
    .community-button:hover {
      background: linear-gradient(
        135deg,
        rgba(255, 255, 255, 0.12) 0%,
        rgba(255, 255, 255, 0.06) 100%
      );
      border-color: var(--brand-color);
      transform: translateY(-4px);
      box-shadow:
        0 8px 24px rgba(0, 0, 0, 0.2),
        0 0 0 1px var(--brand-color);
    }
  }

  /* Visual feedback for copied state */
  .community-button.copied {
    background: linear-gradient(
      135deg,
      rgba(40, 167, 69, 0.2) 0%,
      rgba(40, 167, 69, 0.1) 100%
    );
    border-color: #28a745;
    box-shadow:
      0 4px 16px rgba(40, 167, 69, 0.3),
      0 0 0 1px #28a745;
  }

  .community-button.copied .icon-circle {
    background: linear-gradient(135deg, #28a745 0%, #20893a 100%);
    box-shadow: 0 0 20px rgba(40, 167, 69, 0.5);
  }

  /* Active state - brief feedback that auto-reverts */
  .community-button:active {
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.15) 0%,
      rgba(255, 255, 255, 0.08) 100%
    );
    transform: translateY(-1px) scale(0.98);
    transition-duration: 0.05s;
  }

  .community-button:active .icon-circle {
    transform: scale(0.95);
    transition-duration: 0.05s;
  }

  /* Simple circular icon container */
  .icon-circle {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 3.5rem;
    height: 3.5rem;
    font-size: 1.75rem;
    color: white;
    background: var(--brand-color);
    border-radius: 50%;
    box-shadow:
      0 2px 12px rgba(0, 0, 0, 0.2),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);

    /* Single smooth transition */
    transition: all 0.3s ease;
  }

  /* Icon hover effect only on desktop */
  @media (hover: hover) and (pointer: fine) {
    .community-button:hover .icon-circle {
      transform: scale(1.1);
      box-shadow:
        0 4px 16px rgba(0, 0, 0, 0.3),
        0 0 20px var(--brand-color),
        inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
  }

  .button-label {
    font-size: 0.875rem;
    font-weight: 500;
    text-align: center;
    transition: color 0.3s ease;
  }

  .community-button:hover .button-label {
    color: var(--brand-color);
  }

  /* Zelle-specific styling */
  .zelle-label {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.125rem;
  }

  .copy-hint {
    font-size: 0.625rem;
    font-weight: 400;
    color: rgba(255, 255, 255, 0.6);
    font-style: italic;
  }

  .copied-label {
    display: flex;
    align-items: center;
    gap: 0.375rem;
    color: #28a745;
    font-weight: 600;
  }

  .copied-label i {
    font-size: 1rem;
  }

  /* Responsive adjustments */
  @media (min-width: 640px) {
    .community-content {
      padding: 1.5rem;
      gap: 2.5rem;
    }

    .section-title {
      font-size: 1.25rem;
    }

    .button-grid {
      gap: 1.25rem;
    }

    .community-button {
      padding: 1.5rem 1rem;
    }

    .icon-circle {
      width: 4rem;
      height: 4rem;
      font-size: 2rem;
    }

    .button-label {
      font-size: 0.9375rem;
    }
  }

  @media (min-width: 1024px) {
    .community-content {
      padding: 2rem;
    }

    .button-grid {
      gap: 1.5rem;
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .community-button,
    .icon-circle,
    .button-label {
      transition: none !important;
    }

    .community-button:hover,
    .community-button:hover .icon-circle {
      transform: none;
    }
  }
</style>
