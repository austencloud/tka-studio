<!--
great  CreationMethodSelector.svelte

  Unified creation method selector screen.
  Shows welcome cue, undo button, and method selection buttons
  in a single vertically-stacked layout.

  Allows user to choose how they want to create a sequence:
  - Guided (step-by-step wizard)
  - Construct (manual building)
  - Generate (auto-generation)

  FUTURE ANIMATION:
  Each method card has data-method-id and data-method-index attributes.
  These will be used to implement a morphing animation where the selected
  card animates/transforms into its corresponding tab position in the
  bottom navigation bar, creating visual continuity and communicating
  the relationship between creation modes and navigation tabs.
-->
<script lang="ts">
  import { fly } from "svelte/transition";
  import {
    resolve,
    TYPES,
    type BuildModeId,
    type IHapticFeedbackService,
  } from "$shared";
  import { onMount } from "svelte";
  import CreationWelcomeCue from "../../shared/components/CreationWelcomeCue.svelte";
  import { getCreateModuleContext } from "../../shared/context";

  let {
    onMethodSelected,
  }: {
    onMethodSelected: (method: BuildModeId) => void;
  } = $props();

  // Get context for undo functionality
  const ctx = getCreateModuleContext();
  const { CreateModuleState } = ctx;

  // Services
  let hapticService: IHapticFeedbackService | null = $state(null);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

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

  async function handleMethodClick(methodId: BuildModeId, event: MouseEvent) {
    // Trigger selection haptic feedback for creation mode selection
    hapticService?.trigger("selection");

    // Trigger the navigation (tab change + crossfade will happen in handler)
    onMethodSelected(methodId);
  }

  async function performTabMorphAnimation(
    button: HTMLButtonElement,
    methodId: BuildModeId
  ) {
    console.log("🎯 Starting tab morph animation for:", methodId);

    // Find the target tab in the navigation bar
    // Try multiple selectors to find the tab
    const capitalized = methodId.charAt(0).toUpperCase() + methodId.slice(1);

    let targetTab = document.querySelector(
      `.primary-navigation .sections button[aria-label="${capitalized}"]`
    ) as HTMLButtonElement;

    // Fallback: try finding by icon or text content
    if (!targetTab) {
      const allTabs = Array.from(
        document.querySelectorAll(".primary-navigation .sections button")
      ) as HTMLButtonElement[];

      console.log("📍 Found tabs:", allTabs.length);

      targetTab = allTabs.find((tab) => {
        const label = tab.textContent?.trim().toLowerCase();
        return label === methodId || label === capitalized.toLowerCase();
      }) || allTabs.find((tab, index) => {
        // Fallback to positional matching: guided=0, construct=1, generate=2
        const methodIndex = ["guided", "construct", "generate"].indexOf(methodId);
        return index === methodIndex;
      }) as HTMLButtonElement;
    }

    if (!targetTab) {
      console.warn("❌ Target tab not found for morphing animation:", methodId);
      return;
    }

    console.log("✅ Found target tab:", targetTab);

    // Simple visual feedback - pulse the target tab
    const originalTransform = targetTab.style.transform;
    const originalTransition = targetTab.style.transition;

    targetTab.style.transition = "transform 200ms ease-out";
    targetTab.style.transform = "scale(1.2)";

    await new Promise((resolve) => setTimeout(resolve, 200));

    targetTab.style.transform = "scale(1)";

    await new Promise((resolve) => setTimeout(resolve, 200));

    targetTab.style.transform = originalTransform;
    targetTab.style.transition = originalTransition;
  }
</script>

<div class="creation-method-selector">
  <!-- Undo button - top-right corner -->
  {#if CreateModuleState?.canUndo}
    <button
      class="selector-undo-button"
      onclick={() => CreateModuleState?.undo()}
      title={CreateModuleState.undoHistory[
        CreateModuleState.undoHistory.length - 1
      ]?.metadata?.description || "Undo last action"}
    >
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-hidden="true"
      >
        <path
          d="M9 14L4 9L9 4"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
        <path
          d="M4 9H15A6 6 0 0 1 15 21H13"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
      <span>Undo</span>
    </button>
  {/if}

  <div class="content-container">
    <!-- Welcome cue at the top - always vertical -->
    <div class="welcome-section">
      <CreationWelcomeCue orientation="vertical" mood="fresh" />
    </div>

    <!-- Method selection buttons below -->
    <div class="methods-container">
      {#each methods as method, index (method.id)}
        <button
          class="method-card"
          data-method-id={method.id}
          data-method-index={index}
          onclick={(e) => handleMethodClick(method.id, e)}
          in:fly={{ y: 20, delay: 200 + index * 100, duration: 300 }}
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
    position: relative;
    display: grid;
    place-items: center;
    height: 100%;
    width: 100%;
    padding: clamp(1rem, 3vh, 2rem);
    overflow: auto;
    box-sizing: border-box;
    container-type: size;
    container-name: method-selector;
  }

  /* Undo button - top-right corner */
  .selector-undo-button {
    position: absolute;
    top: clamp(1rem, 2vh, 1.5rem);
    left: clamp(1rem, 2vh, 1.5rem);
    z-index: 10;

    padding: 0.625rem 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;

    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 10px;
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.8125rem;
    font-weight: 500;
    cursor: pointer;

    transition: all 180ms cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(12px);
  }

  .selector-undo-button:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    color: rgba(255, 255, 255, 0.95);
    transform: translateY(-1px);
  }

  .selector-undo-button:active {
    transform: translateY(0);
    background: rgba(255, 255, 255, 0.08);
  }

  .selector-undo-button svg {
    flex-shrink: 0;
    opacity: 0.9;
  }

  .selector-undo-button span {
    white-space: nowrap;
  }

  .content-container {
    display: flex;
    flex-direction: column;
    gap: clamp(2rem, 5vh, 3rem);
    width: 100%;
    max-width: 100%;
    align-items: center;
  }

  .welcome-section {
    width: 100%;
    display: flex;
    justify-content: center;
  }

  .methods-container {
    display: grid;
    grid-template-columns: 1fr;
    gap: clamp(0.75rem, 2vh, 1rem);
    width: 100%;
    container-type: inline-size;
    container-name: methods-container;
  }

  /* Desktop: 3-column grid layout */
  @container method-selector (min-width: 600px) {
    .methods-container {
      grid-template-columns: repeat(3, 1fr);
      gap: clamp(1rem, 2.5vh, 1.5rem);
    }
  }

  /* Tablet: 3 columns but tighter */
  @container method-selector (min-width: 450px) and (max-width: 599px) {
    .methods-container {
      grid-template-columns: repeat(3, 1fr);
      gap: 0.875rem;
    }
  }

  .method-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: clamp(0.75rem, 2vh, 1rem);
    padding: clamp(1.25rem, 3vh, 1.75rem) clamp(1rem, 2.5vh, 1.5rem);

    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;

    cursor: pointer;
    transition: all 220ms cubic-bezier(0.4, 0, 0.2, 1);
    text-align: center;
    position: relative;
    overflow: hidden;
    aspect-ratio: 1 / 1.1;
  }

  .method-card::before {
    content: "";
    position: absolute;
    inset: 0;
    background: radial-gradient(
      circle at 50% 30%,
      var(--method-color, rgba(255, 255, 255, 0.1)) 0%,
      transparent 65%
    );
    opacity: 0;
    transition: opacity 220ms ease;
  }

  .method-card::after {
    content: "";
    position: absolute;
    inset: -1px;
    background: linear-gradient(
      135deg,
      var(--method-color, rgba(255, 255, 255, 0.2)) 0%,
      transparent 50%
    );
    border-radius: 16px;
    opacity: 0;
    transition: opacity 220ms ease;
    z-index: -1;
  }

  .method-card:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(255, 255, 255, 0.15);
    transform: translateY(-2px);
  }

  .method-card:hover::before {
    opacity: 0.12;
  }

  .method-card:hover::after {
    opacity: 1;
  }

  .method-card:active {
    transform: translateY(0);
  }

  .method-icon {
    font-size: clamp(2rem, 6cqi, 2.75rem);
    line-height: 1;
    color: var(--method-color, rgba(255, 255, 255, 0.9));
    flex-shrink: 0;
    width: clamp(3.5rem, 12cqi, 4.5rem);
    height: clamp(3.5rem, 12cqi, 4.5rem);
    display: grid;
    place-items: center;
    background: rgba(255, 255, 255, 0.04);
    border-radius: 12px;
    transition: all 220ms cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
  }

  .method-icon::before {
    content: "";
    position: absolute;
    inset: 0;
    background: var(--method-color, rgba(255, 255, 255, 0.1));
    opacity: 0.08;
    border-radius: 12px;
  }

  .method-card:hover .method-icon {
    transform: scale(1.05);
    background: rgba(255, 255, 255, 0.08);
  }

  .method-content {
    display: flex;
    flex-direction: column;
    gap: clamp(0.25rem, 1cqi, 0.375rem);
    flex: 1;
    justify-content: center;
  }

  .method-title {
    font-size: clamp(1.125rem, 5cqi, 1.5rem);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
    line-height: 1.3;
  }

  .method-description {
    font-size: clamp(0.8125rem, 3.5cqi, 0.9375rem);
    font-weight: 400;
    color: rgba(255, 255, 255, 0.5);
    margin: 0;
    line-height: 1.4;
  }

  .method-arrow {
    position: absolute;
    bottom: clamp(0.875rem, 2vh, 1.125rem);
    right: clamp(0.875rem, 2vh, 1.125rem);
    font-size: 0.75rem;
    color: rgba(255, 255, 255, 0.2);
    transition: all 220ms ease;
  }

  .method-card:hover .method-arrow {
    color: var(--method-color, rgba(255, 255, 255, 0.5));
    transform: translate(2px, -2px);
  }

  /* Mobile optimizations */
  @media (max-width: 449px) {
    .method-card {
      flex-direction: row;
      aspect-ratio: auto;
      text-align: left;
      padding: 1rem 1.25rem;
    }

    .method-content {
      align-items: flex-start;
    }

    .method-arrow {
      position: static;
      margin-left: auto;
    }
  }

  @media (max-width: 640px) {
    .selector-undo-button {
      top: 0.75rem;
      left: 0.75rem;
      padding: 0.5rem 0.875rem;
      font-size: 0.75rem;
    }

    .selector-undo-button svg {
      width: 16px;
      height: 16px;
    }
  }
</style>
