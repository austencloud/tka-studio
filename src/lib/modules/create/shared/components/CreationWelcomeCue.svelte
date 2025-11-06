<script lang="ts">
  import { onMount, untrack } from "svelte";

  type Orientation = "horizontal" | "vertical";
  type CueMood = "fresh" | "returning" | "redo" | "default";

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
    returning: [
      "Welcome back.",
      "Ready for another round?",
      "Continue creating?",
      "Jump back in?",
    ],
    redo: [
      "Need a do-over?",
      "Reset and try again?",
      "Ready to revise?",
      "Take another pass?",
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
    gap: 1rem;
    padding: 1.25rem 1.5rem;
    border-radius: 18px;
    background: linear-gradient(
      145deg,
      rgba(27, 34, 56, 0.8),
      rgba(18, 22, 40, 0.6)
    );
    box-shadow:
      inset 0 0 0 1px rgba(120, 160, 255, 0.1),
      0 18px 40px rgba(4, 8, 24, 0.55);
    max-width: 22rem;
    width: 100%;
    text-align: center;
    backdrop-filter: blur(18px);
    color: rgba(255, 255, 255, 0.98);
    overflow: hidden;
  }

  .creation-cue::after {
    content: "";
    position: absolute;
    inset: -45% -55%;
    background: radial-gradient(
      circle,
      rgba(90, 140, 255, 0.12),
      transparent 60%
    );
    pointer-events: none;
    animation: cueGlow 6s ease-in-out infinite alternate;
  }

  .cue-message {
    position: relative;
    z-index: 1;
    margin: 0;
    font-size: clamp(1.35rem, 2vw, 1.75rem);
    font-weight: 600;
    letter-spacing: 0.01em;
    color: rgba(234, 238, 255, 0.95);
  }

  .cue-pointer {
    position: relative;
    z-index: 1;
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
    stroke: rgba(158, 208, 255, 0.75);
    stroke-width: 4;
    stroke-linecap: round;
    stroke-linejoin: round;
    filter: drop-shadow(0 0 6px rgba(136, 188, 255, 0.35));
  }

  .creation-cue[data-orientation="horizontal"] {
    flex-direction: row;
    text-align: left;
    max-width: 26rem;
    padding: 1.5rem 1.75rem;
    gap: 1.5rem;
  }

  .creation-cue[data-orientation="horizontal"] .cue-pointer {
    flex-direction: row;
    align-items: center;
    animation: pointerGlideX 2.4s ease-in-out infinite;
  }

  .creation-cue[data-orientation="horizontal"] .pointer-base {
    width: 7.5rem;
    height: auto;
  }

  .creation-cue[data-orientation="vertical"] .cue-pointer {
    animation: pointerGlideY 2.4s ease-in-out infinite;
  }

  .creation-cue[data-orientation="vertical"] .pointer-base {
    width: 1.5rem;
    height: auto;
  }

  @keyframes cueGlow {
    from {
      opacity: 0.6;
      transform: translate3d(0, 0, 0);
    }
    to {
      opacity: 0.35;
      transform: translate3d(2%, -2%, 0);
    }
  }

  @keyframes pointerGlideX {
    0%,
    100% {
      transform: translateX(0);
    }
    50% {
      transform: translateX(6px);
    }
  }

  @keyframes pointerGlideY {
    0%,
    100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(6px);
    }
  }

  @media (max-width: 640px) {
    .creation-cue {
      max-width: min(100%, 20rem);
      padding: 1rem 1.25rem;
      gap: 0.75rem;
    }

    .cue-message {
      font-size: 1.2rem;
    }
  }
</style>
