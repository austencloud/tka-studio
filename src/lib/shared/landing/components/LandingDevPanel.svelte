<script lang="ts">
  import type { LandingDevContent } from "../domain";

  let {
    panelId,
    labelledBy,
    copy,
    contactEmail,
    onContact = () => {},
    isContactLoading = false,
    enableSmartContact = false,
  }: {
    panelId: string;
    labelledBy: string;
    copy: LandingDevContent;
    contactEmail: string;
    onContact?: () => void;
    isContactLoading?: boolean;
    enableSmartContact?: boolean;
  } = $props();
</script>

<div class="carousel-panel" id={panelId} role="presentation">
  <div class="tab-panel" role="tabpanel" aria-labelledby={labelledBy}>
    <h2 class="panel-title">{copy.subtitle}</h2>
    <p class="dev-message">{copy.message}</p>
    <div class="dev-links">
      <a
        class="dev-card"
        href="https://github.com/austencloud/tka-sequence-constructor"
        target="_blank"
        rel="noopener noreferrer"
      >
        <i class="fab fa-github"></i>
        <div>
          <h3>View on GitHub</h3>
          <p>Explore the source code and contribute</p>
        </div>
      </a>

      <a
        class="dev-card"
        href={`mailto:${contactEmail}?subject=Development Collaboration`}
      >
        <i class="fas fa-envelope"></i>
        <div>
          <h3>Contact for Dev Work</h3>
          <p>Want to collaborate or contribute? Get in touch</p>
        </div>
      </a>

      {#if enableSmartContact}
        <button
          class="dev-card contact-card"
          type="button"
          onclick={onContact}
          disabled={isContactLoading}
        >
          <i
            class={`fas ${isContactLoading ? "fa-circle-notch fa-spin" : "fa-paper-plane"}`}
          ></i>
          <div>
            <h3>
              {isContactLoading ? "Preparing Gmail..." : "Compose in Gmail"}
            </h3>
            <p>
              {isContactLoading
                ? "Hang tight while we open a Gmail compose window"
                : "Prefer Gmail? We can auto-fill a message for you"}
            </p>
          </div>
        </button>
      {/if}
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

  .dev-card:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none !important;
  }

  @media (min-width: 640px) {
    .dev-card {
      gap: clamp(1rem, 2vw, 1.5rem);
      padding: clamp(1rem, 2.5vh, 1.5rem);
      min-height: 80px;
    }
  }

  .dev-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(34, 197, 94, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
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

  .contact-card {
    border-color: rgba(34, 197, 94, 0.4);
    background: rgba(34, 197, 94, 0.08);
  }

  .contact-card:disabled {
    opacity: 0.75;
    cursor: progress;
  }

  @media (prefers-reduced-motion: reduce) {
    .dev-card:hover {
      transform: none;
    }
  }
</style>
