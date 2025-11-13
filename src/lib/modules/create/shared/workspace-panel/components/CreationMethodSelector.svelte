<!--
  CreationMethodSelector.svelte

  Unified creation method selector screen.
  Shows welcome cue, undo button, and method selection buttons
  in a single vertically-stacked layout.

  Allows user to choose how they want to create a sequence:
  - Guided (step-by-step wizard)
  - Construct (manual building)
  - Generate (auto-generation)
-->
<script lang="ts">
  import {
    resolve,
    TYPES,
    type BuildModeId,
    type IHapticFeedbackService,
  } from "$shared";
  import { onMount } from "svelte";
  import { authStore } from "$shared/auth";
  import CreationWelcomeCue from "../../components/CreationWelcomeCue.svelte";
  import MethodCard from "./MethodCard.svelte";
  import SelectorUndoButton from "./SelectorUndoButton.svelte";

  let {
    onMethodSelected,
  }: {
    onMethodSelected: (method: BuildModeId) => void;
  } = $props();

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
      id: "constructor" as BuildModeId,
      icon: "fa-hammer",
      title: "Constructor",
      description: "Full manual control",
      color: "#3b82f6", // Blue
    },
    {
      id: "generator" as BuildModeId,
      icon: "fa-wand-magic-sparkles",
      title: "Generate",
      description: "Auto-generate",
      color: "#f59e0b", // Gold/Amber (semantic: generation/creation)
    },
  ];

  async function handleMethodClick(
    methodId: BuildModeId,
    event: MouseEvent,
    isDisabled: boolean = false
  ) {
    // Don't allow selection of disabled methods
    if (isDisabled) {
      event.preventDefault();
      event.stopPropagation();
      return;
    }

    // Trigger selection haptic feedback for creation mode selection
    hapticService?.trigger("selection");

    // Trigger the navigation (tab change + crossfade will happen in handler)
    onMethodSelected(methodId);
  }
</script>

<div class="creation-method-selector">
  <!-- Undo button - top-left corner -->
  <SelectorUndoButton />

  <div class="content-container">
    <!-- Welcome cue at the top - always vertical -->
    <div class="welcome-section">
      <CreationWelcomeCue orientation="vertical" mood="fresh" />
    </div>

    <!-- Method selection cards below -->
    <div class="methods-container">
      {#each methods as method, index (method.id)}
        {@const isDisabled = method.id === "guided" && !authStore.isAdmin}
        <MethodCard
          id={method.id}
          icon={method.icon}
          title={method.title}
          description={method.description}
          color={method.color}
          {index}
          {isDisabled}
          onclick={(e) => handleMethodClick(method.id, e, isDisabled)}
        />
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
    padding: 1.5rem;
    overflow: auto;
    box-sizing: border-box;
    container-type: size;
    container-name: method-selector;
  }

  .content-container {
    display: flex;
    flex-direction: column;
    gap: 2.5rem;
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
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    gap: 1rem;
    width: 100%;
    max-width: 900px;
    margin: 0 auto;
    justify-content: center;
  }
</style>
