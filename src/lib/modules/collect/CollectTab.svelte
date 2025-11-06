<!--
  CollectTab.svelte - Personal Collect Interface

  Sections:
  - Gallery: User-created and saved sequences
  - Achievements: Progress, stats, and unlocked achievements
  - Challenges: Daily challenges and active quests

  Navigation via bottom tabs (mobile-first UX pattern)
-->
<script lang="ts">
  import { navigationState, AnimationSheetCoordinator } from "$shared";
  import type { SequenceData } from "$shared";
  import { onMount } from "svelte";
  import GallerySection from "./components/GallerySection.svelte";
  import AchievementsSection from "./components/AchievementsSection.svelte";
  import ChallengesSection from "./components/ChallengesSection.svelte";

  type CollectMode = "gallery" | "achievements" | "challenges";

  // Active mode synced with navigation state
  let activeMode = $state<CollectMode>("gallery");

  // Animation sheet state
  let showAnimator = $state<boolean>(false);
  let sequenceToAnimate = $state<SequenceData | null>(null);

  // Sync with navigation state
  $effect(() => {
    const section = navigationState.currentSection;
    if (
      section === "gallery" ||
      section === "achievements" ||
      section === "challenges"
    ) {
      activeMode = section;
    }
  });

  // Initialize on mount
  onMount(() => {
    // Set default mode if none persisted
    const section = navigationState.currentSection;
    if (
      !section ||
      (section !== "gallery" &&
        section !== "achievements" &&
        section !== "challenges")
    ) {
      navigationState.setCurrentSection("gallery");
    }
  });

  // Check if mode is active
  function isModeActive(mode: CollectMode): boolean {
    return activeMode === mode;
  }
</script>

<div class="collect-tab">
  <!-- Content area (all modes) -->
  <div class="content-container">
    <!-- Gallery Mode -->
    <div class="mode-panel" class:active={isModeActive("gallery")}>
      <GallerySection />
    </div>

    <!-- Achievements Mode -->
    <div class="mode-panel" class:active={isModeActive("achievements")}>
      <AchievementsSection />
    </div>

    <!-- Challenges Mode -->
    <div class="mode-panel" class:active={isModeActive("challenges")}>
      <ChallengesSection />
    </div>
  </div>
</div>

<!-- Animation Sheet Coordinator -->
<AnimationSheetCoordinator
  sequence={sequenceToAnimate}
  bind:isOpen={showAnimator}
/>

<style>
  .collect-tab {
    position: relative;
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
    background: transparent;
    color: var(--foreground, #ffffff);

    /* Enable container queries for responsive design */
    container-type: size;
    container-name: collection-tab;
  }

  /* Content container */
  .content-container {
    position: relative;
    flex: 1;
    width: 100%;
    height: 100%;
    overflow: hidden;
  }

  /* Mode panels */
  .mode-panel {
    position: absolute;
    inset: 0;
    display: none;
    width: 100%;
    height: 100%;
    overflow: hidden;
  }

  .mode-panel.active {
    display: flex;
    flex-direction: column;
  }
</style>
