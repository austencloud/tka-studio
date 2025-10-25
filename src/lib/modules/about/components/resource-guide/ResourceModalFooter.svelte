<script lang="ts">
  interface Props {
    /** URL to the original resource */
    url: string;
    /** Callback when the link is clicked */
    onNavigate?: () => void;
    /** Custom text for the CTA button */
    ctaText?: string;
  }

  let { url, onNavigate, ctaText = "Visit Original Resource →" }: Props = $props();
</script>

<footer class="resource-footer">
  <a
    href={url}
    target="_blank"
    rel="noopener noreferrer"
    class="visit-original"
    onclick={() => onNavigate?.()}
  >
    {ctaText}
  </a>
</footer>

<style>
  .resource-footer {
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding: var(--spacing-lg) var(--spacing-xl);
    display: flex;
    justify-content: center;
  }

  .visit-original {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-sm) var(--spacing-lg);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-decoration: none;
    border-radius: var(--border-radius-lg);
    font-weight: 600;
    transition: all 0.3s ease;
  }

  .visit-original:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  }

  @media (max-width: 768px) {
    .resource-footer {
      padding: var(--spacing-md);
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .visit-original {
      transition: none;
    }

    .visit-original:hover {
      transform: none;
    }
  }
</style>
