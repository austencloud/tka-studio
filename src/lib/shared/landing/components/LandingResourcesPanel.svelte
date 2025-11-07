<script lang="ts">
  import type { LandingPanelContent, Resource } from "../domain";

  let {
    panelId,
    labelledBy,
    copy,
    resources = [],
    onLinkClick = () => {},
  }: {
    panelId: string;
    labelledBy: string;
    copy: LandingPanelContent;
    resources?: Resource[];
    onLinkClick?: (resource: Resource) => void;
  } = $props();
</script>

<div class="carousel-panel" id={panelId} role="presentation">
  <div class="tab-panel" role="tabpanel" aria-labelledby={labelledBy}>
    <h2 class="panel-title">{copy.subtitle}</h2>
    <div class="resources-grid">
      {#each resources as resource}
        <a
          class="resource-card"
          href={resource.url}
          target={resource.type === "internal" ? "_self" : "_blank"}
          rel={resource.type !== "internal" ? "noopener noreferrer" : undefined}
          onclick={() => onLinkClick(resource)}
        >
          <div class="resource-icon">
            {#if resource.icon.startsWith("/")}
              <img src={resource.icon} alt={resource.title} />
            {:else}
              <i class={resource.icon}></i>
            {/if}
          </div>
          <div class="resource-content">
            <h3>{resource.title}</h3>
            <p>{resource.description}</p>
          </div>
        </a>
      {/each}
    </div>
  </div>
</div>

<style>
  .resources-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 0.75rem;
    width: 100%;
  }

  .resources-grid:has(> :nth-child(2)) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (min-width: 640px) {
    .resources-grid {
      gap: 1rem;
    }

    .resources-grid:has(> :nth-child(3)) {
      grid-template-columns: repeat(3, 1fr);
    }
  }

  .resource-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    gap: 0.75rem;
    padding: 1rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1rem;
    text-decoration: none;
    color: inherit;
    transition: all 0.2s ease;
    text-align: center;
    min-height: 0;
  }

  @media (min-width: 640px) {
    .resource-card {
      gap: 1rem;
      padding: 1.25rem;
    }
  }

  .resource-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(102, 126, 234, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  }

  .resource-icon {
    width: 100px;
    height: 100px;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 2.25rem;
    color: #667eea;
    padding: 0.375rem;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  @media (min-width: 640px) {
    .resource-icon {
      width: 120px;
      height: 120px;
      font-size: 2.75rem;
      padding: 0.5rem;
    }
  }

  .resource-icon img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  .resource-content {
    display: flex;
    flex-direction: column;
    gap: 0.375rem;
    width: 100%;
  }

  @media (min-width: 640px) {
    .resource-content {
      gap: 0.5rem;
    }
  }

  .resource-content h3 {
    font-size: 1rem;
    font-weight: 600;
    color: white;
    margin: 0;
    line-height: 1.3;
  }

  @media (min-width: 640px) {
    .resource-content h3 {
      font-size: 1.125rem;
      line-height: 1.2;
    }
  }

  .resource-content p {
    font-size: 0.8125rem;
    color: rgba(255, 255, 255, 0.75);
    margin: 0;
    line-height: 1.4;
  }

  @media (min-width: 640px) {
    .resource-content p {
      font-size: 0.875rem;
      line-height: 1.45;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .resource-card:hover {
      transform: none;
    }
  }
</style>
