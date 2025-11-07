<script lang="ts">
  import type { EmblaCarouselType } from "embla-carousel";
  import emblaCarouselSvelte from "embla-carousel-svelte";
  import { onDestroy, onMount } from "svelte";

  // Props - Compatible with old API
  interface Props {
    children?: import("svelte").Snippet;
    panels?: any[]; // For compatibility with old API
    showArrows?: boolean;
    showIndicators?: boolean;
    className?: string;
    height?: string;
    width?: string;
    onPanelChange?: (panelIndex: number) => void;
    onContentAreaChange?: (bounds: any) => void; // For compatibility
    initialPanelIndex?: number;
    freezeNavigation?: boolean; // Prevent navigation button recreation during transitions
    loop?: boolean; // Enable infinite scrolling - wraps from last to first and vice versa
    topPadding?: number; // Dynamic padding for content that extends above viewport (e.g., type labels)
    preservePosition?: boolean; // Preserve scroll position across reInit (default: false)
    storageKey?: string; // SessionStorage key for position persistence (required if preservePosition is true)
    emblaApiRef?: EmblaCarouselType | undefined; // Bindable ref to the embla API for programmatic control
  }

  let {
    children,
    panels = [],
    showArrows = true,
    showIndicators = true,
    className = "",
    height = "100%",
    width = "100%",
    onPanelChange,
    onContentAreaChange,
    initialPanelIndex = 0,
    freezeNavigation = false,
    loop = false,
    topPadding = 0,
    preservePosition = false,
    storageKey = undefined,
    emblaApiRef = $bindable(),
  }: Props = $props();

  // Embla state
  let emblaApi: EmblaCarouselType;
  let emblaNode: HTMLElement;
  let currentIndex = $state(initialPanelIndex);
  let canScrollPrev = $state(false);
  let canScrollNext = $state(false);
  let slides = $state<HTMLElement[]>([]);

  // Reactive values
  let totalSlides = $derived(slides.length);
  let hasMultipleSlides = $derived(totalSlides > 1);

  // Freeze navigation state during transitions to prevent button recreation
  let frozenHasMultipleSlides = $state(false);

  // Initialize frozen state on mount
  $effect(() => {
    // Initialize frozen state to current value on first run
    if (frozenHasMultipleSlides === false && hasMultipleSlides) {
      frozenHasMultipleSlides = hasMultipleSlides;
    }
  });

  // Update frozen state when not frozen
  $effect(() => {
    if (!freezeNavigation) {
      frozenHasMultipleSlides = hasMultipleSlides;
    }
  });

  // Use frozen state for navigation rendering
  let shouldShowNavigation = $derived(
    freezeNavigation ? frozenHasMultipleSlides : hasMultipleSlides
  );

  // Arrow dimensions for content area calculation
  const DEFAULT_ARROW_WIDTH = 40; // Fallback when buttons have not rendered yet
  const ARROW_SPACING = 0; // Additional spacing buffer if needed

  let measuredArrowWidth = $state(DEFAULT_ARROW_WIDTH);

  // Use the measured arrow width only when arrows render
  let navPadding = $derived(() =>
    showArrows && shouldShowNavigation ? measuredArrowWidth + ARROW_SPACING : 0
  );

  let prevArrowButton: HTMLButtonElement | undefined;
  let nextArrowButton: HTMLButtonElement | undefined;

  let resizeObserver: ResizeObserver | undefined;
  let resizeFallback: (() => void) | undefined;

  // Embla initialization
  function onEmblaInit(event: CustomEvent<EmblaCarouselType>) {
    emblaApi = event.detail;
    emblaApiRef = emblaApi; // Expose to parent via bindable prop

    // Set up event listeners
    emblaApi.on("select", onSelect);
    emblaApi.on("init", onInit);
    emblaApi.on("reInit", onInit);

    // Initial state
    onInit();
    onSelect();
  }

  // Calculate content area bounds between arrows
  function calculateContentAreaBounds() {
    if (onContentAreaChange && emblaNode) {
      const viewportRect = emblaNode.getBoundingClientRect();

      // Calculate navigation state directly to avoid reactivity timing issues
      // Use slides.length directly instead of derived shouldShowNavigation
      const currentSlideCount = slides.length;
      const shouldShowNav = currentSlideCount > 1;

      // Calculate the actual content area between the arrows
      const navPaddingValue =
        showArrows && shouldShowNav ? measuredArrowWidth + ARROW_SPACING : 0;
      const leftOffset = navPaddingValue;
      const rightOffset = navPaddingValue;

      const contentBounds = {
        left: viewportRect.left + leftOffset,
        right: viewportRect.right - rightOffset,
        width: viewportRect.width - leftOffset - rightOffset,
        top: viewportRect.top,
        bottom: viewportRect.bottom,
        height: viewportRect.height,
      };

      onContentAreaChange(contentBounds);
    }
  }

  function onInit() {
    if (!emblaApi) return;
    slides = emblaApi.slideNodes();

    // Restore scroll position after reInit if preservePosition is enabled
    if (preservePosition && storageKey && typeof window !== "undefined") {
      try {
        const stored = sessionStorage.getItem(storageKey);
        if (stored) {
          const savedIndex = parseInt(stored, 10);
          if (
            !isNaN(savedIndex) &&
            savedIndex >= 0 &&
            savedIndex < slides.length
          ) {
            // Use jump: true to instantly restore position without animation
            emblaApi.scrollTo(savedIndex, true);
          }
        }
      } catch (error) {
        console.warn(
          "Failed to restore scroll position from sessionStorage:",
          error
        );
      }
    }

    // Calculate initial content area bounds to ensure they're available early
    calculateContentAreaBounds();
  }

  function onSelect() {
    if (!emblaApi) return;
    currentIndex = emblaApi.selectedScrollSnap();
    canScrollPrev = emblaApi.canScrollPrev();
    canScrollNext = emblaApi.canScrollNext();

    // Notify parent of panel change
    onPanelChange?.(currentIndex);

    // Calculate content area bounds between arrows
    calculateContentAreaBounds();
  }

  // Navigation functions
  function scrollPrev() {
    if (emblaApi && canScrollPrev) {
      emblaApi.scrollPrev();
    }
  }

  function scrollNext() {
    if (emblaApi && canScrollNext) {
      emblaApi.scrollNext();
    }
  }

  function scrollTo(index: number) {
    if (emblaApi) {
      emblaApi.scrollTo(index);
    }
  }

  function updateArrowPadding() {
    const prevWidth = prevArrowButton?.getBoundingClientRect().width ?? 0;
    const nextWidth = nextArrowButton?.getBoundingClientRect().width ?? 0;
    const maxWidth = Math.max(prevWidth, nextWidth);

    measuredArrowWidth = maxWidth > 0 ? maxWidth : DEFAULT_ARROW_WIDTH;

    // Update content bounds whenever arrow sizing changes
    calculateContentAreaBounds();
  }

  onMount(() => {
    updateArrowPadding();

    if (typeof ResizeObserver !== "undefined") {
      resizeObserver = new ResizeObserver(() => updateArrowPadding());
    } else {
      resizeFallback = () => updateArrowPadding();
      window.addEventListener("resize", resizeFallback);
    }
  });

  onDestroy(() => {
    resizeObserver?.disconnect();

    if (resizeFallback) {
      window.removeEventListener("resize", resizeFallback);
    }
  });

  $effect(() => {
    const prev = prevArrowButton;
    const next = nextArrowButton;

    updateArrowPadding();

    if (!resizeObserver) return;

    if (prev) resizeObserver.observe(prev);
    if (next) resizeObserver.observe(next);

    return () => {
      if (prev) resizeObserver?.unobserve(prev);
      if (next) resizeObserver?.unobserve(next);
    };
  });
</script>

<!-- Embla Carousel Container -->
<div
  class="embla {className}"
  style="height: {height}; width: {width}; --nav-padding: {navPadding}px;"
>
  <!-- Navigation Arrows -->
  {#if showArrows && shouldShowNavigation}
    <button
      class="embla__button embla__button--prev"
      onclick={scrollPrev}
      disabled={!canScrollPrev}
      aria-label="Previous slide"
      bind:this={prevArrowButton}
    >
      <svg class="embla__button__svg" viewBox="0 0 532 532">
        <path
          fill="currentColor"
          d="M355.66 11.354c13.793-13.805 36.208-13.805 50.001 0 13.785 13.804 13.785 36.238 0 50.034L201.22 266l204.442 204.61c13.785 13.805 13.785 36.239 0 50.044-13.793 13.796-36.208 13.796-50.002 0a5994246.277 5994246.277 0 0 0-229.332-229.454 35.065 35.065 0 0 1-10.326-25.126c0-9.2 3.393-18.26 10.326-25.2C172.192 194.973 332.731 34.31 355.66 11.354Z"
        />
      </svg>
    </button>
  {/if}

  <!-- Embla Viewport -->
  <div
    class="embla__viewport"
    bind:this={emblaNode}
    use:emblaCarouselSvelte={{
      options: { loop, startIndex: initialPanelIndex },
      plugins: [],
    }}
    onemblaInit={onEmblaInit}
    style="--top-padding: {topPadding}px"
  >
    <div class="embla__container">
      {#if children}
        {@render children()}
      {/if}
    </div>
  </div>

  <!-- Navigation Arrows -->
  {#if showArrows && shouldShowNavigation}
    <button
      class="embla__button embla__button--next"
      onclick={scrollNext}
      disabled={!canScrollNext}
      aria-label="Next slide"
      bind:this={nextArrowButton}
    >
      <svg class="embla__button__svg" viewBox="0 0 532 532">
        <path
          fill="currentColor"
          d="M176.34 520.646c-13.793 13.805-36.208 13.805-50.001 0-13.785-13.804-13.785-36.238 0-50.034L330.78 266 126.34 61.391c-13.785-13.805-13.785-36.239 0-50.044 13.793-13.796 36.208-13.796 50.002 0 22.928 22.947 206.395 206.507 229.332 229.454a35.065 35.065 0 0 1 10.326 25.126c0 9.2-3.393 18.26-10.326 25.2-45.865 45.901-206.404 206.564-229.332 229.52Z"
        />
      </svg>
    </button>
  {/if}

  <!-- Indicators -->
  {#if showIndicators && hasMultipleSlides}
    <div class="embla__dots">
      {#each slides as _, index}
        <button
          class="embla__dot"
          class:embla__dot--selected={index === currentIndex}
          onclick={() => scrollTo(index)}
          aria-label="Go to slide {index + 1}"
        >
        </button>
      {/each}
    </div>
  {/if}
</div>

<style>
  .embla {
    position: relative;
    overflow: hidden;
  }

  .embla__viewport {
    overflow: hidden;
    width: 100%;
    height: 100%;
    /* Dynamic padding to prevent content from being clipped at top and bottom
       The panel-content applies a translateY transform to center content,
       which can push headers/labels above the viewport and bottom content below.
       This padding creates space at both ends, calculated dynamically based on
       actual header heights to ensure all content is fully visible. */
  }

  .embla__container {
    display: flex;
    height: 100%;
    touch-action: pan-y pinch-zoom;
  }

  .embla__container :global(> *) {
    transform: translate3d(0, 0, 0);
    flex: 0 0 100%; /* Each panel takes full width */
    min-width: 0;
    /* Add padding to each panel that matches the rendered arrow size */
    padding-left: var(--nav-padding, 40px);
    padding-right: var(--nav-padding, 40px);
    box-sizing: border-box;
  }

  .embla__button {
    -webkit-tap-highlight-color: rgba(0, 0, 0, 0.5);
    -webkit-appearance: none;
    appearance: none;
    touch-action: manipulation;
    display: flex;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    cursor: pointer;
    border: none;
    padding: 0;
    margin: 0;
    width: 48px;
    height: 48px;
    z-index: 1;
    border-radius: 50%;
    position: absolute;
    top: 50%;
    transform: translateY(-50%);

    /* Modern glassmorphism styling matching app buttons */
    background: rgba(100, 116, 139, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(148, 163, 184, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    color: #ffffff;

    /* Smooth transitions matching app design system */
    transition: all var(--transition-normal, 0.3s cubic-bezier(0.4, 0, 0.2, 1));

    /* Ensure opacity stays at 1 and doesn't inherit transition effects */
    opacity: 1 !important;
  }

  .embla__button:hover:not(:disabled) {
    background: rgba(100, 116, 139, 0.9);
    border-color: rgba(148, 163, 184, 0.4);
    transform: translateY(-50%) scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .embla__button:active:not(:disabled) {
    transform: translateY(-50%) scale(0.95);
    transition: all 0.1s ease;
  }

  .embla__button:focus-visible {
    outline: 2px solid var(--primary-light, #818cf8);
    outline-offset: 2px;
  }

  .embla__button:disabled {
    color: rgba(255, 255, 255, 0.3);
    cursor: not-allowed;
    opacity: 0.5 !important;
  }

  .embla__button--prev {
    left: 0rem;
  }

  .embla__button--next {
    right: 0rem;
  }

  .embla__button__svg {
    width: 40%;
    height: 40%;
  }

  /* Mobile responsive - 44px minimum per iOS/Android guidelines */
  @media (max-width: 768px) {
    .embla__button {
      width: 40px;
      height: 40px;
    }
  }

  /* Reduced motion accessibility */
  @media (prefers-reduced-motion: reduce) {
    .embla__button {
      transition: none;
    }

    .embla__button:hover:not(:disabled) {
      transform: translateY(-50%);
    }

    .embla__button:active:not(:disabled) {
      transform: translateY(-50%);
    }
  }

  .embla__dots {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: center;
    margin-top: 1.8rem;
  }

  .embla__dot {
    -webkit-tap-highlight-color: rgba(0, 0, 0, 0.5);
    -webkit-appearance: none;
    appearance: none;
    background-color: transparent;
    touch-action: manipulation;
    display: inline-flex;
    text-decoration: none;
    cursor: pointer;
    border: 0;
    padding: 0;
    margin: 0;
    width: 2.4rem;
    height: 2.4rem;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
  }

  .embla__dot:after {
    box-shadow: inset 0 0 0 0.2rem rgba(0, 0, 0, 0.2);
    width: 1.4rem;
    height: 1.4rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    content: "";
  }

  .embla__dot--selected:after {
    box-shadow: inset 0 0 0 0.2rem rgba(0, 0, 0, 0.8);
  }
</style>
