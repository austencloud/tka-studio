<script lang="ts">
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";
  import { onMount } from "svelte";
  import type { InfoPanelContent, Resource } from "../domain";

  let {
    panelId,
    labelledBy,
    copy,
    resources = [],
    onLinkClick = () => {},
  }: {
    panelId: string;
    labelledBy: string;
    copy: InfoPanelContent;
    resources?: Resource[];
    onLinkClick?: (resource: Resource) => void;
  } = $props();

  // Services
  let hapticService: IHapticFeedbackService | null = $state(null);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  function handleResourceClick(resource: Resource) {
    // Trigger haptic feedback for resource link click
    hapticService?.trigger("selection");
    onLinkClick(resource);
  }
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
          onclick={() => handleResourceClick(resource)}
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
  .carousel-panel {
    display: flex;
    flex-direction: column;
  }

  .tab-panel {
    display: flex;
    flex-direction: column;
    padding: clamp(0.5rem, 1vh, 0.75rem);
  }

  @media (min-width: 1024px) {
    .tab-panel {
      padding: 0;
    }
  }

  .panel-title {
    flex-shrink: 0;
    font-size: clamp(0.75rem, 2cqh, 0.875rem);
    margin-bottom: clamp(0.25rem, 1cqh, 0.375rem);
  }

  @media (min-width: 1024px) {
    .panel-title {
      display: none;
    }
  }

  .resources-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: clamp(0.375rem, 1cqh, 0.5rem);
    width: 100%;
    max-width: 100%;
  }

  .resources-grid:has(> :nth-child(2)) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (min-width: 640px) {
    .resources-grid {
      gap: clamp(0.625rem, 2cqh, 0.875rem);
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
    gap: clamp(0.5rem, 1.5cqh, 0.75rem);
    padding: 0;
    text-decoration: none;
    color: inherit;
    transition: all 0.2s ease;
    text-align: center;
    min-height: 0;
    min-width: 0;
    width: 100%;
    height: 100%;
    box-sizing: border-box;
    overflow: hidden;
  }

  .resource-card:hover {
    opacity: 0.9;
  }

  .resource-icon {
    width: clamp(50px, 10cqh, 80px);
    height: clamp(50px, 10cqh, 80px);
    background: rgba(255, 255, 255, 0.95);
    border-radius: clamp(0.375rem, 1.25cqh, 0.625rem);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: clamp(1.25rem, 3.5cqh, 1.875rem);
    color: #667eea;
    padding: clamp(0.25rem, 0.5cqh, 0.375rem);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  /* Book covers/images scale responsively to container height */
  .resource-icon:has(img) {
    width: 100%;
    height: auto;
    aspect-ratio: 3 / 4;
    /* Use container query units to scale based on available space */
    max-height: clamp(35cqh, 50cqh, 60cqh);
    padding: clamp(0.25rem, 0.75cqh, 0.375rem);
    background: none;
    box-shadow: none;
  }

  .resource-icon img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    border-radius: clamp(0.25rem, 0.75cqh, 0.375rem);
  }

  .resource-content {
    display: flex;
    flex-direction: column;
    gap: clamp(0.125rem, 0.5cqh, 0.25rem);
    width: 100%;
    flex-shrink: 0;
  }

  .resource-content h3 {
    font-size: clamp(0.75rem, 1.875cqh, 0.875rem);
    font-weight: 600;
    color: white;
    margin: 0;
    line-height: 1.2;
  }

  .resource-content p {
    font-size: clamp(0.625rem, 1.5cqh, 0.75rem);
    color: rgba(255, 255, 255, 0.75);
    margin: 0;
    line-height: 1.25;
  }

  @media (prefers-reduced-motion: reduce) {
    .resource-card:hover {
      transform: none;
    }
  }
</style>
