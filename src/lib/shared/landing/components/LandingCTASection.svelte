<script lang="ts">
  let {
    ctaLabel,
    onEnterStudio = () => {},
  }: {
    ctaLabel: string;
    onEnterStudio?: () => void;
  } = $props();
</script>

<div class="cta-section">
  <button class="cta-button" type="button" onclick={onEnterStudio}>
    <i class="fas fa-rocket"></i>
    {ctaLabel}
  </button>
</div>

<style>
  .cta-section {
    flex-shrink: 0;
    padding: clamp(0.75rem, 2vh, 1rem);
    text-align: center;
  }

  .cta-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    padding: clamp(1rem, 2.5vh, 1.25rem) clamp(2rem, 5vw, 3rem);
    width: 100%;
    max-width: 400px;
    min-height: 56px;
    margin: 0 auto;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 2rem;
    font-size: clamp(1.125rem, 4vw, 1.375rem);
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
  }

  .cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(102, 126, 234, 0.6);
  }

  .cta-button:active {
    transform: translateY(0);
  }

  .cta-button:focus-visible {
    outline: 2px solid rgba(99, 102, 241, 0.7);
    outline-offset: 2px;
  }

  .cta-button i {
    font-size: clamp(1.125rem, 3vw, 1.375rem);
  }

  @media (max-height: 600px) {
    .cta-section {
      padding: 0.5rem 0;
    }

    .cta-button {
      min-height: 48px;
      padding: 0.75rem 1.5rem;
      font-size: 0.9375rem;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .cta-button:hover,
    .cta-button:active {
      transform: none;
    }
  }
</style>
