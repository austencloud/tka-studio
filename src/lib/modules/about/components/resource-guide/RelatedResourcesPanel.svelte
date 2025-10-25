<script lang="ts">
  import type { RelatedResource } from "./types";

  interface Props {
    /** Related resources to display */
    resources: RelatedResource[];
    /** Callback when a related resource link is clicked */
    onNavigate?: () => void;
  }

  let { resources, onNavigate }: Props = $props();
</script>

{#if resources && resources.length > 0}
  <aside class="related-resources">
    <h3>Related Resources</h3>
    <div class="related-links">
      {#each resources as related}
        <a
          href={related.url}
          class="related-link"
          class:internal={related.type === "internal"}
          target={related.type === "external" ? "_blank" : "_self"}
          rel={related.type === "external" ? "noopener noreferrer" : ""}
          onclick={() => onNavigate?.()}
        >
          <span class="related-name">{related.name}</span>
          <span class="related-description">{related.description}</span>
        </a>
      {/each}
    </div>
  </aside>
{/if}

<style>
  .related-resources {
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding: var(--spacing-xl);
    background: rgba(255, 255, 255, 0.02);
  }

  .related-resources h3 {
    color: var(--text-color);
    margin-bottom: var(--spacing-md);
    font-size: var(--font-size-lg);
    font-weight: 600;
  }

  .related-links {
    display: grid;
    gap: var(--spacing-sm);
  }

  .related-link {
    display: flex;
    flex-direction: column;
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius);
    text-decoration: none;
    transition: all 0.3s ease;
  }

  .related-link:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: var(--primary-color);
    transform: translateY(-2px);
  }

  .related-name {
    color: var(--primary-color);
    font-weight: 600;
    margin-bottom: var(--spacing-xs);
  }

  .related-description {
    color: var(--text-secondary);
    font-size: var(--font-size-sm);
    line-height: 1.4;
  }

  @media (max-width: 768px) {
    .related-resources {
      padding: var(--spacing-md);
    }

    .related-links {
      grid-template-columns: 1fr;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .related-link {
      transition: none;
    }

    .related-link:hover {
      transform: none;
    }
  }
</style>
