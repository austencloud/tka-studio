<script lang="ts">
  import { onMount, untrack } from "svelte";

  type Orientation = "horizontal" | "vertical";
  type CueMood = "fresh" | "default";

  const { orientation = "vertical", mood = "default" } = $props<{
    orientation?: Orientation;
    mood?: CueMood;
  }>();

  const messagePool: Record<CueMood, string[]> = {
    fresh: [
      "Ready to begin?",
      "Start something new?",
      "How do you want to create?",
      "Pick a creation path.",
    ],
    default: [
      "Ready to create?",
      "How do you want to create?",
      "Select your creation mode.",
      "Ready to begin?",
    ],
  };

  let message = $state(messagePool.default[0]);
  let lastMessage = $state<string | null>(null);
  let isMounted = false;

  function chooseRandom<T>(options: T[], lastValue: T | null): T {
    if (options.length === 0) {
      throw new Error("CreationWelcomeCue: options array is empty.");
    }

    if (options.length === 1) {
      return options[0]!;
    }

    let next: T;
    do {
      const index = Math.floor(Math.random() * options.length);
      next = options[index]!;
    } while (next === lastValue);

    return next;
  }

  function updateMessage(selectedMood: CueMood) {
    const pool = messagePool[selectedMood] ?? messagePool.default;
    message = chooseRandom(pool, lastMessage);
    lastMessage = message;
  }

  onMount(() => {
    updateMessage(mood);
    isMounted = true;
  });

  $effect(() => {
    if (!isMounted) return;
    mood;
    untrack(() => updateMessage(mood));
  });
</script>

<div class="creation-cue" data-orientation={orientation}>
  <p class="cue-message">{message}</p>
  <div class="cue-pointer" aria-hidden="true">
    <svg
      class="pointer-base"
      viewBox={orientation === "horizontal" ? "0 0 96 24" : "0 0 24 96"}
      preserveAspectRatio="none"
    >
      {#if orientation === "horizontal"}
        <path d="M6 12 C30 12 54 12 78 12" vector-effect="non-scaling-stroke" />
        <path d="M70 6 L90 12 L70 18" vector-effect="non-scaling-stroke" />
      {:else}
        <path d="M12 6 C12 30 12 54 12 78" vector-effect="non-scaling-stroke" />
        <path d="M6 70 L12 90 L18 70" vector-effect="non-scaling-stroke" />
      {/if}
    </svg>
  </div>
</div>

<style>
  .creation-cue {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.875rem;
    padding: 0;
    max-width: 100%;
    width: 100%;
    text-align: center;
  }

  .cue-message {
    margin: 0;
    font-size: clamp(1rem, 2.5vw, 1.25rem);
    font-weight: 500;
    letter-spacing: -0.01em;
    color: rgba(255, 255, 255, 0.45);
    line-height: 1.4;
  }

  .cue-pointer {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
  }

  .pointer-base {
    width: 100%;
    height: auto;
    overflow: visible;
  }

  .pointer-base path {
    fill: none;
    stroke: rgba(255, 255, 255, 0.2);
    stroke-width: 2.5;
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  .creation-cue[data-orientation="horizontal"] {
    flex-direction: row;
    text-align: left;
    gap: 1.25rem;
    justify-content: center;
  }

  .creation-cue[data-orientation="horizontal"] .cue-pointer {
    flex-direction: row;
    align-items: center;
    animation: pointerGlideX 2.8s ease-in-out infinite;
  }

  .creation-cue[data-orientation="horizontal"] .pointer-base {
    width: 5rem;
    height: auto;
  }

  .creation-cue[data-orientation="vertical"] .cue-pointer {
    animation: pointerGlideY 2.8s ease-in-out infinite;
  }

  .creation-cue[data-orientation="vertical"] .pointer-base {
    width: 1.25rem;
    height: auto;
  }

  @keyframes pointerGlideX {
    0%,
    100% {
      transform: translateX(0);
      opacity: 0.4;
    }
    50% {
      transform: translateX(8px);
      opacity: 0.7;
    }
  }

  @keyframes pointerGlideY {
    0%,
    100% {
      transform: translateY(0);
      opacity: 0.4;
    }
    50% {
      transform: translateY(8px);
      opacity: 0.7;
    }
  }

  @media (max-width: 640px) {
    .cue-message {
      font-size: 0.9375rem;
    }

    .creation-cue[data-orientation="horizontal"] .pointer-base {
      width: 4rem;
    }
  }
</style>
