<script lang="ts">
  import { onMount } from "svelte";
  import emblaCarouselSvelte from "embla-carousel-svelte";
  import type { EmblaCarouselType } from "embla-carousel";
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { CallToAction } from ".";
  import AboutTheSystem from "./AboutTheSystem.svelte";
  import GettingStarted from "./GettingStarted.svelte";
  import ResourcesHistorian from "./ResourcesHistorian.svelte";

  // Landing sections configuration - the 4 tabs you originally had
  const sections = [
    { id: "home", label: "Home", icon: '<i class="fas fa-home"></i>' },
    {
      id: "about",
      label: "About the System",
      icon: '<i class="fas fa-info-circle"></i>',
    },
    {
      id: "getting-started",
      label: "Getting Started",
      icon: '<i class="fas fa-play-circle"></i>',
    },
    {
      id: "resources",
      label: "Resources",
      icon: '<i class="fas fa-book"></i>',
    },
  ];

  let emblaRef = $state<HTMLDivElement>();
  let emblaApi = $state<EmblaCarouselType>();
  let selectedIndex = $state(0);
  let hapticService: IHapticFeedbackService;

  // External links
  const pdfBookLink =
    "https://drive.google.com/file/d/1cgAWbrFiLgUSDEsCB0Mmu2d7Bu5PW45a/view?usp=drive_link";
  const desktopAppLink =
    "https://github.com/austencloud/tka-sequence-constructor/releases/download/v0.1.2/TKA_Setup.exe";

  function onSelect() {
    if (!emblaApi) return;
    selectedIndex = emblaApi.selectedScrollSnap();
  }

  function scrollTo(index: number) {
    if (!emblaApi) return;
    hapticService?.trigger("selection");
    emblaApi.scrollTo(index);
  }

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );

    if (emblaRef) {
      emblaApi = emblaCarouselSvelte(emblaRef, {
        align: "start",
        dragFree: false,
        containScroll: "trimSnaps",
      });

      emblaApi.on("select", onSelect);
      emblaApi.on("reInit", onSelect);

      return () => {
        emblaApi?.destroy();
      };
    }
  });
</script>

<svelte:head>
  <title>The Kinetic Alphabet - Flow Arts Movement Notation System</title>
  <meta
    name="description"
    content="The Kinetic Alphabet (TKA) is a revolutionary movement notation system for flow arts. Learn, create, and share choreographic sequences using TKA Studio."
  />
</svelte:head>

<div class="landing-page">
  <!-- Top Header with Sparkly Gradient -->
  <header class="landing-header">
    <div class="header-content">
      <h1 class="main-title">The Kinetic Alphabet</h1>
      <p class="subtitle">TKA Studio</p>
    </div>

    <!-- Tab Navigation -->
    <div class="tab-navigation" role="tablist">
      {#each sections as section, index}
        <button
          class="tab-button"
          class:active={selectedIndex === index}
          onclick={() => scrollTo(index)}
          role="tab"
          aria-selected={selectedIndex === index}
          aria-controls={`panel-${section.id}`}
        >
          <span class="tab-icon" aria-hidden="true">{@html section.icon}</span>
          <span class="tab-label">{section.label}</span>
        </button>
      {/each}
    </div>
  </header>

  <!-- Swipeable Content -->
  <div class="embla" bind:this={emblaRef}>
    <div class="embla__container">
      <!-- Section 1: Home -->
      <div class="embla__slide" id="panel-home" role="tabpanel">
        <section class="hero-section">
          <div class="hero-content">
            <h2 class="hero-title">Welcome to The Kinetic Alphabet</h2>
            <p class="hero-description">
              A revolutionary movement notation system for flow arts. TKA
              provides structured methods for learning, creating, and sharing
              choreographic sequences. Like sheet music for dance - write down
              any flow art movement.
            </p>

            <div class="cta-group">
              <CallToAction
                text="Enter TKA Studio"
                primary={true}
                internal={true}
              />
              <CallToAction
                text="Download Level 1 PDF"
                link={pdfBookLink}
                primary={false}
                internal={false}
              />
              <CallToAction
                text="Get Desktop App v0.1.2"
                link={desktopAppLink}
                primary={false}
                internal={false}
              />
            </div>

            <div class="quick-features">
              <div class="feature-pill">
                <i class="fas fa-music"></i>
                <span>Movement Notation</span>
              </div>
              <div class="feature-pill">
                <i class="fas fa-palette"></i>
                <span>Sequence Builder</span>
              </div>
              <div class="feature-pill">
                <i class="fas fa-graduation-cap"></i>
                <span>Learning System</span>
              </div>
              <div class="feature-pill">
                <i class="fas fa-share-nodes"></i>
                <span>Community Sharing</span>
              </div>
            </div>
          </div>
        </section>
      </div>

      <!-- Section 2: About the System -->
      <div class="embla__slide" id="panel-about" role="tabpanel">
        <AboutTheSystem />
      </div>

      <!-- Section 3: Getting Started -->
      <div class="embla__slide" id="panel-getting-started" role="tabpanel">
        <GettingStarted />
      </div>

      <!-- Section 4: Resources -->
      <div class="embla__slide" id="panel-resources" role="tabpanel">
        <div class="resources-wrapper">
          <ResourcesHistorian />
        </div>
      </div>
    </div>
  </div>

  <!-- Section Indicators -->
  <div class="section-indicators">
    {#each sections as section, index}
      <button
        class="indicator"
        class:active={selectedIndex === index}
        onclick={() => scrollTo(index)}
        aria-label={`Go to ${section.label}`}
      ></button>
    {/each}
  </div>
</div>

<style>
  .landing-page {
    width: 100%;
    height: 100vh;
    height: 100dvh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background: var(--cosmic-gradient);
  }

  /* Top Header with Sparkly Gradient */
  .landing-header {
    display: flex;
    flex-direction: column;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    z-index: 100;
    flex-shrink: 0;
  }

  .header-content {
    padding: var(--spacing-lg) var(--spacing-xl);
    text-align: center;
    background: linear-gradient(
      135deg,
      rgba(102, 126, 234, 0.15) 0%,
      rgba(118, 75, 162, 0.15) 50%,
      rgba(237, 100, 166, 0.15) 100%
    );
    position: relative;
    overflow: hidden;
  }

  .header-content::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background:
      radial-gradient(
        circle at 20% 50%,
        rgba(255, 255, 255, 0.1) 0%,
        transparent 50%
      ),
      radial-gradient(
        circle at 80% 50%,
        rgba(255, 255, 255, 0.1) 0%,
        transparent 50%
      );
    animation: sparkle 3s ease-in-out infinite;
    pointer-events: none;
  }

  @keyframes sparkle {
    0%,
    100% {
      opacity: 0.3;
    }
    50% {
      opacity: 0.6;
    }
  }

  .main-title {
    font-size: 2.5rem;
    font-weight: 900;
    margin: 0;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #ed64a6 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
    position: relative;
    z-index: 1;
  }

  .subtitle {
    font-size: 1rem;
    color: rgba(255, 255, 255, 0.8);
    margin: 0.25rem 0 0 0;
    font-weight: 600;
    position: relative;
    z-index: 1;
  }

  /* Tab Navigation - styled like Settings tabs */
  .tab-navigation {
    display: flex;
    gap: 0;
    padding: 0 var(--spacing-lg);
    background: rgba(0, 0, 0, 0.2);
    overflow-x: auto;
    scrollbar-width: none;
  }

  .tab-navigation::-webkit-scrollbar {
    display: none;
  }

  .tab-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.25rem;
    padding: var(--spacing-md) var(--spacing-lg);
    background: transparent;
    border: none;
    border-bottom: 3px solid transparent;
    color: rgba(255, 255, 255, 0.6);
    cursor: pointer;
    transition: all 0.3s ease;
    font-size: 0.875rem;
    font-weight: 600;
    white-space: nowrap;
    flex: 1;
    min-width: fit-content;
  }

  .tab-button:hover {
    background: rgba(255, 255, 255, 0.05);
    color: rgba(255, 255, 255, 0.9);
  }

  .tab-button.active {
    color: #667eea;
    border-bottom-color: #667eea;
    background: rgba(102, 126, 234, 0.1);
  }

  .tab-icon {
    font-size: 1.25rem;
    display: block;
  }

  .tab-label {
    font-size: 0.75rem;
    display: block;
  }

  /* Embla Carousel */
  .embla {
    flex: 1;
    overflow: hidden;
    position: relative;
  }

  .embla__container {
    display: flex;
    height: 100%;
    touch-action: pan-y pinch-zoom;
  }

  .embla__slide {
    flex: 0 0 100%;
    min-width: 0;
    overflow-y: auto;
    overflow-x: hidden;
  }

  /* Hero Section */
  .hero-section {
    min-height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-2xl) var(--spacing-lg);
  }

  .hero-content {
    max-width: 900px;
    text-align: center;
    padding: var(--spacing-2xl);
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 2rem;
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }

  .hero-title {
    font-size: 2.5rem;
    margin-bottom: var(--spacing-lg);
    font-weight: 800;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .hero-description {
    font-size: 1.125rem;
    margin-bottom: var(--spacing-2xl);
    color: rgba(255, 255, 255, 0.9);
    line-height: 1.8;
  }

  .cta-group {
    display: flex;
    gap: var(--spacing-md);
    justify-content: center;
    flex-wrap: wrap;
    margin-bottom: var(--spacing-2xl);
  }

  .quick-features {
    display: flex;
    gap: var(--spacing-md);
    justify-content: center;
    flex-wrap: wrap;
    margin-top: var(--spacing-xl);
  }

  .feature-pill {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-sm) var(--spacing-lg);
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 2rem;
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.875rem;
    font-weight: 600;
  }

  .feature-pill i {
    color: #667eea;
  }

  /* Resources Wrapper */
  .resources-wrapper {
    padding: var(--spacing-xl) var(--spacing-lg);
    max-width: 1400px;
    margin: 0 auto;
  }

  /* Section Indicators */
  .section-indicators {
    display: flex;
    justify-content: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  .indicator {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    padding: 0;
  }

  .indicator.active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    width: 30px;
    border-radius: 5px;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.4);
  }

  .indicator:hover {
    background: rgba(102, 126, 234, 0.7);
  }

  /* Mobile Responsive */
  @media (max-width: 768px) {
    .header-content {
      padding: var(--spacing-md) var(--spacing-lg);
    }

    .main-title {
      font-size: 2rem;
    }

    .subtitle {
      font-size: 0.875rem;
    }

    .tab-navigation {
      padding: 0 var(--spacing-sm);
      gap: 0;
    }

    .tab-button {
      padding: var(--spacing-sm) var(--spacing-md);
      min-width: 80px;
    }

    .tab-icon {
      font-size: 1.125rem;
    }

    .tab-label {
      font-size: 0.65rem;
    }

    .hero-section {
      padding: var(--spacing-lg);
    }

    .hero-content {
      padding: var(--spacing-lg);
    }

    .hero-title {
      font-size: 1.75rem;
    }

    .hero-description {
      font-size: 1rem;
    }

    .quick-features {
      gap: var(--spacing-sm);
    }

    .feature-pill {
      font-size: 0.75rem;
      padding: var(--spacing-xs) var(--spacing-md);
    }

    .resources-wrapper {
      padding: var(--spacing-lg) var(--spacing-md);
    }
  }

  /* Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    .header-content::before {
      animation: none;
    }

    .tab-button,
    .indicator {
      transition: none;
    }
  }
</style>
