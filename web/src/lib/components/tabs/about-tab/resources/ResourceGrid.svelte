<!--
Resource Grid Component

Grid layout for displaying filtered resources with responsive design and loading states.
-->
<script lang="ts">
  import type { Resource } from "./resourcesData";
  import ResourceCard from "./ResourceCard.svelte";

  // Props
  const {
    resources,
    isLoading = false,
    onOpenModal = () => {},
  } = $props<{
    resources: Resource[];
    isLoading?: boolean;
    onOpenModal?: (resource: Resource) => void;
  }>();
</script>

{#if isLoading}
  <div class="loading-state">
    <div class="loading-spinner"></div>
    <p>Loading resources...</p>
  </div>
{:else if resources.length === 0}
  <div class="empty-state">
    <div class="empty-icon">🔍</div>
    <h3>No resources found</h3>
    <p>Try adjusting your search criteria or filters.</p>
  </div>
{:else}
  <div class="resource-grid">
    {#each resources as resource, index (resource.id || `resource-${index}`)}
      <ResourceCard {resource} {onOpenModal} />
    {/each}
  </div>
{/if}

<style>
  .resource-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: var(--spacing-lg);
    margin-top: var(--spacing-lg);
  }

  .loading-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-xl) 0;
    color: var(--color-text-secondary);
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid var(--color-border);
    border-top: 3px solid var(--color-accent);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: var(--spacing-md);
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }

  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-xl) 0;
    text-align: center;
    color: var(--color-text-secondary);
  }

  .empty-icon {
    font-size: 48px;
    margin-bottom: var(--spacing-md);
    opacity: 0.5;
  }

  .empty-state h3 {
    margin: 0 0 var(--spacing-sm) 0;
    color: var(--color-text-primary);
    font-size: var(--font-size-lg);
  }

  .empty-state p {
    margin: 0;
    max-width: 400px;
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .resource-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-md);
    }
  }

  @media (max-width: 480px) {
    .resource-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-sm);
    }
  }

  /* Large screens - allow more columns */
  @media (min-width: 1400px) {
    .resource-grid {
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    }
  }

  /* Extra large screens */
  @media (min-width: 1800px) {
    .resource-grid {
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    }
  }
</style>
