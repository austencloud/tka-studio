<!--
great  CreationMethodSelector.svelte

  Selector shown in tool panel area when workspace is empty.
  Allows user to choose how they want to create a sequence:
  - Construct (manual building)
  - Guided (step-by-step wizard)
  - Generate (auto-generation)
-->
<script lang="ts">
  import { fade, fly } from "svelte/transition";
  import type { BuildModeId } from "$shared";

  let {
    onMethodSelected,
  }: {
    onMethodSelected: (method: BuildModeId) => void;
  } = $props();

  // Creation method options with Font Awesome icons
  // Order matches navigation bar: Guided → Construct → Generate
  const methods = [
    {
      id: "guided" as BuildModeId,
      icon: "fa-compass",
      title: "Guided",
      description: "Step-by-step wizard",
      color: "#8b5cf6", // Purple
    },
    {
      id: "construct" as BuildModeId,
      icon: "fa-hammer",
      title: "Construct",
      description: "Full manual control",
      color: "#3b82f6", // Blue
    },
    {
      id: "generate" as BuildModeId,
      icon: "fa-wand-magic-sparkles",
      title: "Generate",
      description: "Auto-generate",
      color: "#f59e0b", // Gold/Amber (semantic: generation/creation)
    },
  ];

  function handleMethodClick(methodId: BuildModeId) {
    onMethodSelected(methodId);
  }
</script>

<div class="creation-method-selector" in:fade={{ duration: 200 }}>
  <div class="content-container">
    <!-- Title removed - now shown in top bar -->
    <div class="methods-container">
      {#each methods as method, index (method.id)}
        <button
          class="method-card"
          onclick={() => handleMethodClick(method.id)}
          in:fly={{ y: 20, delay: index * 100, duration: 300 }}
          style="--method-color: {method.color}"
        >
          <div class="method-icon">
            <i class="fas {method.icon}"></i>
          </div>
          <div class="method-content">
            <h3 class="method-title">{method.title}</h3>
            <p class="method-description">{method.description}</p>
          </div>
          <div class="method-arrow">
            <i class="fas fa-chevron-right"></i>
          </div>
        </button>
      {/each}
    </div>
  </div>
</div>

<style>
  .creation-method-selector {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    padding: clamp(0.75rem, 2vh, 1.25rem);
    overflow-y: auto;
    overflow-x: hidden;
    box-sizing: border-box;
    container-type: size;
    container-name: method-selector;
  }

  .content-container {
    display: flex;
    flex-direction: column;
    gap: clamp(0.875rem, 2.5vh, 1.5rem);
    width: 100%;
    height: 100%;
    max-width: 100%;
    margin: auto;
  }

  .methods-container {
    display: flex;
    flex-direction: column; /* Default: stack vertically */
    gap: clamp(0.625rem, 1.5vh, 0.875rem);
    width: 100%;
    flex: 1;
    min-height: 0;
    justify-content: center;
    /* Enable container queries for method cards */
    container-type: inline-size;
    container-name: methods-container;
  }

  /* Container query: Switch to row layout ONLY when very wide (desktop/landscape tablet) */
  @container method-selector (min-width: 600px) and (min-aspect-ratio: 1.8/1) {
    .methods-container {
      flex-direction: row;
    }
  }

  .method-card {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: clamp(0.75rem, 4cqi, 1.5rem);
    padding: clamp(0.625rem, 2.5cqi, 1rem) clamp(0.875rem, 5cqi, 1.5rem);
    background: rgba(255, 255, 255, 0.04);
    border: 1.5px solid rgba(255, 255, 255, 0.1);
    border-radius: 999px; /* Fully rounded pill shape */
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    text-align: left;
    flex: 1;
    min-height: 0;
    position: relative;
    overflow: hidden;
  }

  .method-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(
      circle at left,
      var(--method-color, rgba(255, 255, 255, 0.1)) 0%,
      transparent 70%
    );
    opacity: 0;
    transition: opacity 0.25s ease;
  }

  .method-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: var(--method-color, rgba(255, 255, 255, 0.2));
    transform: scale(1.02);
  }

  .method-card:hover::before {
    opacity: 0.15;
  }

  .method-card:active {
    transform: scale(0.98);
  }

  .method-icon {
    font-size: clamp(1.5rem, 6cqi, 2.25rem);
    line-height: 1;
    color: var(--method-color, rgba(255, 255, 255, 0.8));
    flex-shrink: 0;
    width: clamp(2rem, 8cqi, 3rem);
    height: clamp(2rem, 8cqi, 3rem);
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 50%;
    transition: all 0.25s ease;
  }

  .method-card:hover .method-icon {
    transform: scale(1.1);
  }

  .method-content {
    display: flex;
    flex-direction: column;
    gap: clamp(0.1875rem, 1cqi, 0.375rem);
    flex: 1;
    min-width: 0;
  }

  .method-title {
    font-size: clamp(1rem, 5cqi, 2rem);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
    line-height: 1.2;
  }

  .method-description {
    font-size: clamp(0.75rem, 3.5cqi, 1.125rem);
    font-weight: 400;
    color: rgba(255, 255, 255, 0.5);
    margin: 0;
    line-height: 1.3;
  }

  .method-arrow {
    font-size: clamp(0.625rem, 2.5cqi, 0.9375rem);
    color: rgba(255, 255, 255, 0.3);
    flex-shrink: 0;
    transition: all 0.25s ease;
  }

  .method-card:hover .method-arrow {
    color: var(--method-color, rgba(255, 255, 255, 0.6));
    transform: translateX(2px);
  }

  /* Container-aware responsive adjustments */
  @container methods-container (min-width: 400px) {
    .method-title {
      font-size: clamp(1.125rem, 5.5cqi, 2.25rem);
    }

    .method-description {
      font-size: clamp(0.8125rem, 4cqi, 1.25rem);
    }
  }

  @container methods-container (min-width: 600px) {
    .method-title {
      font-size: clamp(1.25rem, 6cqi, 2.5rem);
    }

    .method-description {
      font-size: clamp(0.875rem, 4.5cqi, 1.375rem);
    }

    .method-icon {
      font-size: clamp(1.75rem, 7cqi, 2.5rem);
      width: clamp(2.25rem, 9cqi, 3.25rem);
      height: clamp(2.25rem, 9cqi, 3.25rem);
    }
  }
</style>
