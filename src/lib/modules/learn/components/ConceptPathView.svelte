<!--
ConceptPathView - Main learning path display

Shows all TKA concepts grouped by category in a scrollable view.
Displays progression from Foundation → Letters → Combinations → Advanced.
-->
<script lang="ts">
  import { onMount } from "svelte";
  import {
    TKA_CONCEPTS,
    CONCEPT_CATEGORIES,
    getConceptsByCategory,
    type LearnConcept,
    type ConceptCategory,
  } from "../domain";
  import { conceptProgressService } from "../services/ConceptProgressService";
  import ConceptCard from "./ConceptCard.svelte";

  let { onConceptClick } = $props<{
    onConceptClick?: (concept: LearnConcept) => void;
  }>();

  // Progress state
  let progress = $state(conceptProgressService.getProgress());

  // Subscribe to progress updates
  onMount(() => {
    const unsubscribe = conceptProgressService.subscribe((newProgress) => {
      progress = newProgress;
    });

    return unsubscribe;
  });

  // Categories in order
  const categories: ConceptCategory[] = [
    "foundation",
    "letters",
    "combinations",
    "advanced",
  ];
</script>

<div class="concept-path">
  {#each categories as category}
    {@const categoryInfo = CONCEPT_CATEGORIES[category]}
    {@const concepts = getConceptsByCategory(category)}

    <section class="category-section" data-category={category}>
      <!-- Category header -->
      <div class="category-header">
        <span class="category-icon" aria-hidden="true">{categoryInfo.icon}</span
        >
        <div class="category-title-group">
          <h2 class="category-title">{categoryInfo.name}</h2>
          <p class="category-description">{categoryInfo.description}</p>
        </div>
      </div>

      <!-- Concept cards -->
      <div class="concept-list">
        {#each concepts as concept (concept.id)}
          {@const status = conceptProgressService.getConceptStatus(concept.id)}
          {@const conceptProgress = conceptProgressService.getConceptProgress(
            concept.id
          )}

          <ConceptCard
            {concept}
            {status}
            progress={conceptProgress}
            onClick={onConceptClick}
          />
        {/each}
      </div>
    </section>
  {/each}

  <!-- Empty state at the end -->
  <div class="path-complete">
    {#if progress.overallProgress >= 100}
      <div class="completion-celebration">
        <span class="celebration-icon">🎉</span>
        <h3 class="celebration-title">Congratulations!</h3>
        <p class="celebration-text">
          You've completed the entire Kinetic Alphabet Level 1 curriculum. Keep
          practicing to maintain mastery!
        </p>
      </div>
    {:else}
      <div class="motivational-message">
        <span class="message-icon">🚀</span>
        <p class="message-text">
          Keep going! {28 - progress.completedConcepts.size} concepts remaining.
        </p>
      </div>
    {/if}
  </div>
</div>

<style>
  .concept-path {
    display: flex;
    flex-direction: column;
    gap: 3rem;
    padding: 1.5rem;
    max-width: 800px;
    margin: 0 auto;
    width: 100%;
  }

  /* Category section */
  .category-section {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    opacity: 0;
    animation: fadeIn 0.4s ease forwards;
  }

  .category-section[data-category="foundation"] {
    animation-delay: 0.1s;
  }

  .category-section[data-category="letters"] {
    animation-delay: 0.2s;
  }

  .category-section[data-category="combinations"] {
    animation-delay: 0.3s;
  }

  .category-section[data-category="advanced"] {
    animation-delay: 0.4s;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  /* Category header */
  .category-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding-bottom: 0.75rem;
    border-bottom: 2px solid rgba(255, 255, 255, 0.1);
  }

  .category-icon {
    font-size: 2rem;
    flex-shrink: 0;
  }

  .category-title-group {
    flex: 1;
  }

  .category-title {
    font-size: 1.5rem;
    font-weight: 800;
    color: white;
    margin: 0 0 0.25rem 0;
    background: linear-gradient(135deg, #ffffff, #e0e0e0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .category-description {
    font-size: 0.875rem;
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
  }

  /* Concept list */
  .concept-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  /* Path completion */
  .path-complete {
    padding: 2rem;
    text-align: center;
  }

  .completion-celebration {
    background: linear-gradient(
      135deg,
      rgba(80, 200, 120, 0.2),
      rgba(74, 144, 226, 0.2)
    );
    border: 2px solid rgba(80, 200, 120, 0.3);
    border-radius: 16px;
    padding: 2rem;
  }

  .celebration-icon {
    font-size: 4rem;
    display: block;
    margin-bottom: 1rem;
    animation: bounce 1s ease infinite;
  }

  @keyframes bounce {
    0%,
    100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-10px);
    }
  }

  .celebration-title {
    font-size: 1.75rem;
    font-weight: 800;
    color: white;
    margin: 0 0 0.75rem 0;
  }

  .celebration-text {
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.9);
    margin: 0;
    line-height: 1.6;
  }

  .motivational-message {
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
  }

  .message-icon {
    font-size: 2rem;
    display: block;
    margin-bottom: 0.5rem;
  }

  .message-text {
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.8);
    margin: 0;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .concept-path {
      gap: 2rem;
      padding: 1rem;
    }

    .category-header {
      gap: 0.75rem;
    }

    .category-icon {
      font-size: 1.5rem;
    }

    .category-title {
      font-size: 1.25rem;
    }

    .category-description {
      font-size: 0.8125rem;
    }

    .concept-list {
      gap: 0.625rem;
    }

    .celebration-icon {
      font-size: 3rem;
    }

    .celebration-title {
      font-size: 1.5rem;
    }

    .celebration-text {
      font-size: 0.9375rem;
    }
  }

  @media (max-width: 480px) {
    .concept-path {
      gap: 1.5rem;
      padding: 0.75rem;
    }

    .category-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 0.5rem;
    }

    .category-icon {
      font-size: 1.25rem;
    }

    .category-title {
      font-size: 1.125rem;
    }

    .category-description {
      font-size: 0.75rem;
    }

    .path-complete {
      padding: 1.5rem;
    }

    .completion-celebration {
      padding: 1.5rem;
    }

    .celebration-icon {
      font-size: 2.5rem;
    }

    .celebration-title {
      font-size: 1.25rem;
    }

    .celebration-text {
      font-size: 0.875rem;
    }
  }

  /* Smooth scrolling */
  @media (prefers-reduced-motion: no-preference) {
    .concept-path {
      scroll-behavior: smooth;
    }
  }
</style>
