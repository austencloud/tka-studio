<!--
Resource Card Component

Individual resource item display with metadata, actions, and modal integration.
-->
<script lang="ts">
  import type { Resource } from "./resourcesData";
  import { categories, getCategoryDisplayName } from "./resourcesData";

  // Props
  const { resource, onOpenModal = () => {} } = $props<{
    resource: Resource;
    onOpenModal?: (resource: Resource) => void;
  }>();

  function handleOpenModal() {
    onOpenModal(resource);
  }

  function getStatusIcon(status: string): string {
    switch (status) {
      case "vendor":
        return "🏪";
      case "historical":
        return "📚";
      default:
        return "✨";
    }
  }

  function getCategoryLabel(categoryValue: string): string {
    return (
      categories.find((c) => c.value === categoryValue)?.label || categoryValue
    );
  }
</script>

<article class="resource-card">
  <div class="resource-header">
    <div class="resource-title-row">
      <h3 class="resource-title">
        <a href={resource.url} target="_blank" rel="noopener noreferrer">
          {resource.name}
        </a>
      </h3>
      <span class="status-indicator status-{resource.status}">
        {getStatusIcon(resource.status)}
      </span>
    </div>
    <div class="resource-meta">
      <span class="category-badge category-{resource.category}">
        {getCategoryLabel(resource.category)}
      </span>
      {#if resource.status === "vendor" && resource.foundingYear}
        <span class="founding-badge">Est. {resource.foundingYear}</span>
      {/if}
      {#if resource.lastUpdated}
        <span class="last-updated-indicator"
          >Updated {resource.lastUpdated}</span
        >
      {/if}
    </div>
  </div>

  <p class="resource-description">{resource.description}</p>

  {#if resource.status === "vendor" && resource.specialties}
    <div class="vendor-specialties">
      <strong>Specialties:</strong>
      <div class="specialty-tags">
        {#each resource.specialties as specialty}
          <span class="specialty-tag">{specialty}</span>
        {/each}
      </div>
    </div>
  {/if}

  <div class="resource-value">
    <strong
      >{resource.status === "vendor"
        ? "Why shop here:"
        : "Why it's essential:"}</strong
    >
    {resource.value}
  </div>

  <div class="resource-actions">
    <a
      href={resource.url}
      target="_blank"
      rel="noopener noreferrer"
      class="visit-btn"
    >
      Visit {resource.status === "vendor"
        ? "Store"
        : resource.status === "historical"
          ? "Archive"
          : "Site"}
    </a>

    {#if resource.hasLandingPage}
      <button type="button" onclick={handleOpenModal} class="learn-more-btn">
        Learn More
      </button>
    {/if}
  </div>
</article>

<style>
  .resource-card {
    background: var(--color-bg-secondary);
    border: 2px solid var(--color-border);
    border-radius: var(--radius-lg);
    padding: var(--spacing-lg);
    transition: all 0.3s ease;
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .resource-card:hover {
    border-color: var(--color-accent);
    transform: translateY(-2px);
    box-shadow: 0 8px 25px var(--shadow-lg);
  }

  .resource-header {
    margin-bottom: var(--spacing-md);
  }

  .resource-title-row {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: var(--spacing-sm);
  }

  .resource-title {
    margin: 0;
    font-size: var(--font-size-lg);
    font-weight: 700;
    flex: 1;
  }

  .resource-title a {
    color: var(--color-text-primary);
    text-decoration: none;
    transition: color 0.2s ease;
  }

  .resource-title a:hover {
    color: var(--color-accent);
    text-decoration: underline;
  }

  .status-indicator {
    font-size: var(--font-size-lg);
    margin-left: var(--spacing-sm);
  }

  .resource-meta {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-sm);
    align-items: center;
  }

  .category-badge {
    background: var(--color-accent-alpha);
    color: var(--color-accent);
    padding: 2px 8px;
    border-radius: var(--radius-sm);
    font-size: var(--font-size-xs);
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .category-active-learning {
    background: var(--color-success-alpha);
    color: var(--color-success);
  }
  .category-active-community {
    background: var(--color-info-alpha);
    color: var(--color-info);
  }
  .category-vendors {
    background: var(--color-warning-alpha);
    color: var(--color-warning);
  }
  .category-historical-archives {
    background: var(--color-neutral-alpha);
    color: var(--color-neutral);
  }

  .founding-badge {
    background: var(--color-bg-tertiary);
    color: var(--color-text-secondary);
    padding: 2px 8px;
    border-radius: var(--radius-sm);
    font-size: var(--font-size-xs);
  }

  .last-updated-indicator {
    color: var(--color-text-secondary);
    font-size: var(--font-size-xs);
  }

  .resource-description {
    color: var(--color-text-secondary);
    line-height: 1.6;
    margin-bottom: var(--spacing-md);
    flex: 1;
  }

  .vendor-specialties {
    margin-bottom: var(--spacing-md);
  }

  .vendor-specialties strong {
    color: var(--color-text-primary);
    font-size: var(--font-size-sm);
  }

  .specialty-tags {
    display: flex;
    flex-wrap: wrap;
    gap: var(--spacing-xs);
    margin-top: var(--spacing-xs);
  }

  .specialty-tag {
    background: var(--color-bg-tertiary);
    color: var(--color-text-secondary);
    padding: 2px 6px;
    border-radius: var(--radius-sm);
    font-size: var(--font-size-xs);
  }

  .resource-value {
    background: var(--color-bg-tertiary);
    padding: var(--spacing-md);
    border-radius: var(--radius-md);
    margin-bottom: var(--spacing-md);
    border-left: 4px solid var(--color-accent);
  }

  .resource-value strong {
    color: var(--color-text-primary);
  }

  .resource-actions {
    display: flex;
    gap: var(--spacing-sm);
    margin-top: auto;
  }

  .visit-btn,
  .learn-more-btn {
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--radius-md);
    font-weight: 600;
    text-decoration: none;
    text-align: center;
    transition: all 0.2s ease;
    font-size: var(--font-size-sm);
    flex: 1;
  }

  .visit-btn {
    background: var(--color-accent);
    color: white;
    border: 2px solid var(--color-accent);
  }

  .visit-btn:hover {
    background: var(--color-accent-dark);
    border-color: var(--color-accent-dark);
    transform: translateY(-1px);
  }

  .learn-more-btn {
    background: transparent;
    color: var(--color-accent);
    border: 2px solid var(--color-accent);
    cursor: pointer;
  }

  .learn-more-btn:hover {
    background: var(--color-accent-alpha);
    transform: translateY(-1px);
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .resource-card {
      padding: var(--spacing-md);
    }

    .resource-title {
      font-size: var(--font-size-md);
    }

    .resource-actions {
      flex-direction: column;
    }

    .specialty-tags {
      gap: 4px;
    }
  }
</style>
