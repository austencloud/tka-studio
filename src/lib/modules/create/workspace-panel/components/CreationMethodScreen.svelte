<!--
  CreationMethodScreen.svelte
  
  Full-page screen shown when workspace is empty.
  Allows user to choose how they want to create a sequence:
  - Construct (manual building)
  - Guided (step-by-step wizard)
  - Generate (auto-generation)
-->
<script lang="ts">
  import { fade } from "svelte/transition";
  import type { BuildModeId } from "$shared";

  let {
    onMethodSelected,
  }: {
    onMethodSelected: (method: BuildModeId) => void;
  } = $props();

  // Creation method options
  const methods = [
    {
      id: "construct" as BuildModeId,
      icon: "🔨",
      title: "Construct",
      description: "Full manual control - build beat by beat",
    },
    {
      id: "guided" as BuildModeId,
      icon: "🧭",
      title: "Guided Builder",
      description: "Step-by-step wizard - Blue hand then Red hand",
    },
    {
      id: "generate" as BuildModeId,
      icon: "✨",
      title: "Generate",
      description: "Auto-generate sequences with parameters",
    },
  ];

  function handleMethodClick(methodId: BuildModeId) {
    onMethodSelected(methodId);
  }
</script>

<div class="creation-method-screen" in:fade={{ duration: 200 }}>
  <div class="content-container">
    <h2 class="title">How would you like to build?</h2>
    <p class="subtitle">Choose your creation method</p>

    <div class="methods-grid">
      {#each methods as method (method.id)}
        <button
          class="method-card"
          onclick={() => handleMethodClick(method.id)}
        >
          <div class="method-icon">{method.icon}</div>
          <h3 class="method-title">{method.title}</h3>
          <p class="method-description">{method.description}</p>
        </button>
      {/each}
    </div>
  </div>
</div>

<style>
  .creation-method-screen {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
    width: 100%;
    padding: clamp(1rem, 3vh, 2rem);
    overflow-y: auto;
    overflow-x: hidden;
    box-sizing: border-box;
  }

  .content-container {
    display: flex;
    flex-direction: column;
    gap: 2rem;
    width: 100%;
    max-width: 800px;
    margin: auto;
  }

  .title {
    font-size: clamp(1.5rem, 5vw, 2rem);
    font-weight: 700;
    color: white;
    text-align: center;
    margin: 0;
    line-height: 1.2;
  }

  .subtitle {
    font-size: clamp(1rem, 3vw, 1.25rem);
    color: rgba(255, 255, 255, 0.7);
    text-align: center;
    margin: 0;
    line-height: 1.4;
  }

  .methods-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    width: 100%;
  }

  .method-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
    padding: 2rem 1.5rem;
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.1),
      rgba(255, 255, 255, 0.05)
    );
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: center;
  }

  .method-card:hover {
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.15),
      rgba(255, 255, 255, 0.08)
    );
    border-color: rgba(255, 255, 255, 0.4);
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  }

  .method-card:active {
    transform: translateY(-2px);
  }

  .method-icon {
    font-size: clamp(2.5rem, 8vw, 3.5rem);
    line-height: 1;
  }

  .method-title {
    font-size: clamp(1.125rem, 3.5vw, 1.5rem);
    font-weight: 600;
    color: white;
    margin: 0;
    line-height: 1.2;
  }

  .method-description {
    font-size: clamp(0.875rem, 2.5vw, 1rem);
    color: rgba(255, 255, 255, 0.6);
    margin: 0;
    line-height: 1.4;
  }

  /* Mobile optimizations */
  @media (max-width: 640px) {
    .methods-grid {
      grid-template-columns: 1fr;
      gap: 1rem;
    }

    .method-card {
      padding: 1.5rem 1rem;
    }
  }

  /* Tablet optimizations */
  @media (min-width: 641px) and (max-width: 1024px) {
    .methods-grid {
      grid-template-columns: repeat(2, 1fr);
    }
  }

  /* Desktop - 3 columns */
  @media (min-width: 1025px) {
    .methods-grid {
      grid-template-columns: repeat(3, 1fr);
    }
  }
</style>

