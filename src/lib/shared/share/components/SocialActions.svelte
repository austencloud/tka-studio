<!-- SocialActions.svelte - Social media sharing actions -->
<script lang="ts">
  let {
    canShare = false,
    onInstagramPost,
  }: {
    canShare?: boolean;
    onInstagramPost?: () => void;
  } = $props();
</script>

<div class="social-actions">
  <button
    class="action-btn social instagram"
    disabled={!canShare}
    onclick={onInstagramPost}
  >
    <i class="fab fa-instagram"></i>
    <span>Post to Instagram</span>
  </button>

  <button class="action-btn social facebook" disabled>
    <i class="fab fa-facebook"></i>
    <span>Post to Facebook</span>
  </button>
</div>

<style>
  .social-actions {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 12px;
  }

  .action-btn {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    padding: 16px 28px;
    border: none;
    border-radius: 14px;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    overflow: hidden;
    isolation: isolate;
  }

  .action-btn > * {
    position: relative;
    z-index: 2;
  }

  .action-btn::before {
    content: "";
    position: absolute;
    inset: 0;
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
    z-index: 0;
  }

  .action-btn::after {
    z-index: 1;
  }

  .action-btn:hover::before {
    opacity: 1;
  }

  .action-btn.social {
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.08),
      rgba(255, 255, 255, 0.04)
    );
    color: rgba(255, 255, 255, 0.95);
    border: 1.5px solid rgba(255, 255, 255, 0.18);
    box-shadow:
      0 2px 8px rgba(0, 0, 0, 0.08),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }

  .action-btn.social::before {
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.12),
      rgba(255, 255, 255, 0.06)
    );
  }

  .action-btn.social:hover:not(:disabled) {
    transform: scale(1.02) translateY(-1px);
    border-color: rgba(255, 255, 255, 0.28);
    box-shadow:
      0 4px 12px rgba(0, 0, 0, 0.12),
      inset 0 1px 0 rgba(255, 255, 255, 0.15);
  }

  /* Instagram button - colorful gradient */
  .action-btn.instagram {
    background: linear-gradient(
      135deg,
      #f09433 0%,
      #e6683c 25%,
      #dc2743 50%,
      #cc2366 75%,
      #bc1888 100%
    );
    border: none;
    color: white;
    box-shadow:
      0 4px 16px rgba(188, 24, 136, 0.35),
      0 2px 8px rgba(0, 0, 0, 0.15),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }

  .action-btn.instagram::before {
    background: linear-gradient(
      135deg,
      #e6683c 0%,
      #dc2743 25%,
      #cc2366 50%,
      #bc1888 75%,
      #8a0868 100%
    );
  }

  .action-btn.instagram:hover:not(:disabled) {
    transform: scale(1.03) translateY(-2px);
    box-shadow:
      0 8px 24px rgba(188, 24, 136, 0.5),
      0 4px 12px rgba(0, 0, 0, 0.2),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }

  .action-btn.instagram i {
    font-size: 18px;
    filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.3));
  }

  /* Facebook button styling */
  .action-btn.facebook {
    position: relative;
  }

  .action-btn.facebook i {
    color: #1877f2;
    font-size: 18px;
  }

  .action-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
  }

  .action-btn:disabled::before {
    display: none;
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
    }

    .action-btn:hover {
      transform: none !important;
    }
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .social-actions {
      grid-template-columns: 1fr;
    }
  }
</style>
