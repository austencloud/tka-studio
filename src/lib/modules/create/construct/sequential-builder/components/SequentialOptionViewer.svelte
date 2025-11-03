<!--
SequentialOptionViewer.svelte - Display 6 motion options for Guided Construct

Shows the 6 valid options from current position:
- STATIC, DASH, Direction1+PRO, Direction1+ANTI, Direction2+PRO, Direction2+ANTI

Responsive grid layout: 2×3 or 3×2 depending on viewport
-->
<script lang="ts">
  import type { IHapticFeedbackService, MotionColor, PictographData } from "$shared";
  import { Pictograph, resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  const {
    options,
    onOptionSelected,
    visibleHand,
    isTransitioning = false,
  } = $props<{
    options: PictographData[];
    onOptionSelected: (option: PictographData) => void;
    visibleHand: MotionColor;
    isTransitioning?: boolean;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  // Animation state
  let shouldAnimate = $state(true);
  let animatedOptions = $state(new Set<string>());

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);

    // Trigger staggered animation
    setTimeout(() => {
      shouldAnimate = true;
    }, 100);
  });

  // Check if option should animate
  function shouldOptionAnimate(optionId: string): boolean {
    return shouldAnimate && !animatedOptions.has(optionId);
  }

  // Handle animation end
  function handleAnimationEnd(optionId: string) {
    animatedOptions.add(optionId);
    animatedOptions = new Set(animatedOptions);
  }

  // Handle option selection
  function handleOptionClick(option: PictographData) {
    if (isTransitioning) return;

    hapticService?.trigger("selection");
    onOptionSelected(option);
  }

  // Get descriptive label for each option type
  function getOptionLabel(option: PictographData, index: number): string {
    const motion = option.motions[visibleHand];
    if (!motion) return `Option ${index + 1}`;

    const motionType = motion.motionType;
    const startLoc = motion.startLocation;
    const endLoc = motion.endLocation;

    if (motionType === 'static') return 'Stay';
    if (motionType === 'dash') return 'Dash';

    // For shifts, show direction + rotation
    const direction = endLoc.split('_')[0]; // e.g., "NORTH" from "NORTH"
    const rotation = motionType === 'pro' ? 'Pro' : 'Anti';

    return `${direction} ${rotation}`;
  }
</script>

<div class="option-viewer" class:transitioning={isTransitioning}>
  <div class="option-grid">
    {#each options as option, index (option.id)}
      <button
        class="option-button"
        class:animate={shouldOptionAnimate(option.id)}
        style:--animation-delay="{index * 60}ms"
        onclick={() => handleOptionClick(option)}
        onanimationend={() => handleAnimationEnd(option.id)}
        disabled={isTransitioning}
        aria-label={getOptionLabel(option, index)}
      >
        <div class="pictograph-wrapper">
          <Pictograph
            pictographData={option}
            visibleHand={visibleHand}
            disableContentTransitions={false}
          />
        </div>
        <span class="option-label">{getOptionLabel(option, index)}</span>
      </button>
    {/each}
  </div>
</div>

<style>
  .option-viewer {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    padding: 1rem;
    overflow: hidden; /* Changed from auto to hidden to prevent scrolling */
  }

  .option-viewer.transitioning {
    pointer-events: none;
    opacity: 0.7;
  }

  .option-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(2, 1fr); /* Force 2 rows to constrain height */
    gap: 1rem;
    width: 100%;
    height: 100%; /* Take full height of parent */
    max-width: 900px;
    margin: 0 auto;
  }

  .option-button {
    background: rgba(255, 255, 255, 0.03);
    border: 2px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 0.75rem;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    position: relative;
    overflow: hidden;
    width: 100%;
    height: 100%; /* Fill the grid cell */
    min-height: 0; /* Allow flexbox to shrink */
    min-width: 0; /* Allow flexbox to shrink */

    /* Initial state for animation */
    opacity: 0;
    transform: scale(0.8) translateY(20px);
  }

  /* After animation completes, ensure visible state */
  .option-button:not(.animate) {
    opacity: 1;
    transform: scale(1) translateY(0);
  }

  /* Staggered entrance animation */
  .option-button.animate {
    animation: optionFadeIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
    animation-delay: var(--animation-delay, 0ms);
  }

  .option-button::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(
      135deg,
      rgba(100, 200, 255, 0.08),
      rgba(100, 150, 255, 0.03)
    );
    opacity: 0;
    transition: opacity 0.3s ease;
  }

  .pictograph-wrapper {
    flex: 1;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
  }

  .option-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.6);
    text-align: center;
    text-transform: capitalize;
  }

  /* Hover effects */
  @media (hover: hover) {
    .option-button:not(:disabled):hover {
      border-color: rgba(100, 200, 255, 0.4);
      transform: translateY(-4px) scale(1.03);
      box-shadow:
        0 8px 20px rgba(0, 0, 0, 0.15),
        0 0 16px rgba(100, 200, 255, 0.15);
    }

    .option-button:not(:disabled):hover::before {
      opacity: 1;
    }

    .option-button:not(:disabled):hover .option-label {
      color: rgba(147, 197, 253, 1);
    }
  }

  .option-button:not(:disabled):active {
    transform: translateY(-2px) scale(0.99);
    transition: transform 0.1s ease;
  }

  .option-button:disabled {
    cursor: not-allowed;
    opacity: 0.5;
  }

  /* Responsive: switch to 2×3 on smaller screens */
  @media (max-width: 768px) {
    .option-grid {
      grid-template-columns: repeat(2, 1fr);
      grid-template-rows: repeat(3, 1fr); /* 3 rows for 2×3 layout */
      gap: 0.75rem;
    }

    .option-button {
      padding: 0.5rem;
    }

    .option-label {
      font-size: 0.7rem;
    }
  }

  @media (max-width: 480px) {
    .option-viewer {
      padding: 0.5rem;
    }

    .option-grid {
      grid-template-columns: repeat(2, 1fr);
      grid-template-rows: repeat(3, 1fr); /* Maintain 3 rows */
      gap: 0.5rem;
    }

    .option-button {
      padding: 0.375rem;
    }

    .option-label {
      font-size: 0.65rem;
    }
  }

  /* Entrance animation */
  @keyframes optionFadeIn {
    0% {
      opacity: 0;
      transform: scale(0.8) translateY(20px);
    }
    60% {
      opacity: 0.9;
      transform: scale(1.05) translateY(-5px);
    }
    100% {
      opacity: 1;
      transform: scale(1) translateY(0);
    }
  }
</style>
