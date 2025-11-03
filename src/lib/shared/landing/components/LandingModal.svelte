<script lang="ts">
  /**
   * Landing Modal Component
   *
   * Full-screen tabbed landing page overlay with resources, community, and support.
   */

  import { onMount } from "svelte";
  import { fade, scale } from "svelte/transition";
  import { cubicOut } from "svelte/easing";
  import { landingUIState, closeLanding } from "../state/landing-state.svelte";
  import {
    LANDING_TEXT,
    SOCIAL_LINKS,
    RESOURCES,
    SUPPORT_OPTIONS,
    CONTACT_EMAIL,
  } from "../landing-content";
  import { browser } from "$app/environment";
  import PrimaryNavigation from "../../navigation/components/PrimaryNavigation.svelte";
  import type { Section } from "../../navigation/domain/types";
  import { HorizontalSwipeContainer } from "$shared";
  import type EmblaCarouselType from "embla-carousel";

  // Whether to show the close button (only show if manually opened)
  const showCloseButton = $derived(!landingUIState.isAutoOpened);

  // Tab state
  type LandingTab = "resources" | "community" | "support" | "dev";
  let activeTab = $state<LandingTab>("resources");

  // Define landing page sections for navigation with unique colors
  const landingSections: Section[] = [
    {
      id: "resources",
      label: "Resources",
      icon: '<i class="fas fa-book"></i>',
      color: "rgba(102, 126, 234, 1)",
      gradient: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    },
    {
      id: "community",
      label: "Community",
      icon: '<i class="fas fa-users"></i>',
      color: "rgba(56, 189, 248, 1)",
      gradient: "linear-gradient(135deg, #38bdf8 0%, #06b6d4 100%)",
    },
    {
      id: "support",
      label: "Support",
      icon: '<i class="fas fa-heart"></i>',
      color: "rgba(244, 63, 94, 1)",
      gradient: "linear-gradient(135deg, #f43f5e 0%, #ec4899 100%)",
    },
    {
      id: "dev",
      label: "Dev",
      icon: '<i class="fas fa-code"></i>',
      color: "rgba(34, 197, 94, 1)",
      gradient: "linear-gradient(135deg, #22c55e 0%, #16a34a 100%)",
    },
  ];

  // Carousel state
  let currentPanelIndex = $state(0);
  let emblaApi: EmblaCarouselType | undefined = $state(undefined);

  // Handle tab change from PrimaryNavigation - scroll carousel to panel
  function handleTabChange(tabId: string) {
    const index = landingSections.findIndex(s => s.id === tabId);
    if (index !== -1 && emblaApi) {
      emblaApi.scrollTo(index);
    }
  }

  // Handle panel change from carousel - update activeTab
  function handlePanelChange(panelIndex: number) {
    currentPanelIndex = panelIndex;
    activeTab = landingSections[panelIndex].id as LandingTab;
  }

  // Handle escape key (only allow if not auto-opened)
  function handleKeydown(e: KeyboardEvent) {
    if (e.key === "Escape" && landingUIState.isOpen && !landingUIState.isAutoOpened) {
      closeLanding(false);
    }
  }

  // Handle backdrop click (only allow if not auto-opened)
  function handleBackdropClick() {
    if (!landingUIState.isAutoOpened) {
      closeLanding(false);
    }
  }

  // Handle Enter Studio button click
  function handleEnterStudio() {
    // If auto-opened (first visit), use the special entry animation
    if (landingUIState.isAutoOpened) {
      closeLanding(true); // true = with studio entry animation
    } else {
      closeLanding(false); // Standard close
    }
  }

  // Prevent clicks inside modal from closing it
  function handleModalClick(e: MouseEvent) {
    e.stopPropagation();
  }

  // Handle external link clicks
  function handleLinkClick(url: string, type: string) {
    if (browser && (type === "download" || type === "external")) {
      window.open(url, "_blank", "noopener,noreferrer");
    }
  }

  onMount(() => {
    document.addEventListener("keydown", handleKeydown);
    return () => {
      document.removeEventListener("keydown", handleKeydown);
    };
  });
</script>

{#if landingUIState.isOpen}
  <!-- Backdrop -->
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div
    class="landing-backdrop"
    onclick={handleBackdropClick}
    transition:fade={{ duration: 350, easing: cubicOut }}
  ></div>

  <!-- Modal -->
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div
    class="landing-modal"
    onclick={handleModalClick}
    role="dialog"
    aria-modal="true"
    aria-labelledby="landing-title"
    tabindex="-1"
    transition:scale={{ duration: 400, easing: cubicOut, start: 0.95 }}
  >
    <!-- Close Button (only show if manually opened) -->
    {#if showCloseButton}
      <button
        class="close-button"
        onclick={() => closeLanding(false)}
        aria-label="Close landing page"
        title="Close (Esc)"
      >
        <i class="fas fa-times"></i>
      </button>
    {/if}

    <!-- Content Container (no scroll, fits viewport) -->
    <div class="landing-content">
      <!-- Compact Hero Section -->
      <section class="hero-section">
        <h1 id="landing-title" class="hero-title">
          <span class="gradient-text">{LANDING_TEXT.hero.title}</span>
          <span class="sparkle sparkle-1"></span>
          <span class="sparkle sparkle-2"></span>
          <span class="sparkle sparkle-3"></span>
          <span class="sparkle sparkle-4"></span>
          <span class="sparkle sparkle-5"></span>
          <span class="sparkle sparkle-6"></span>
        </h1>
        <p class="hero-subtitle">{LANDING_TEXT.hero.subtitle}</p>
      </section>

      <!-- Tab Content with Swipe Carousel -->
      <div class="tab-content">
        <HorizontalSwipeContainer
          panels={landingSections}
          initialPanelIndex={0}
          onPanelChange={handlePanelChange}
          showArrows={false}
          showIndicators={false}
          height="100%"
          width="100%"
          bind:emblaApiRef={emblaApi}
        >
          <!-- Resources Panel -->
          <div class="carousel-panel">
            <div class="tab-panel" role="tabpanel">
              <h2 class="panel-title">{LANDING_TEXT.resources.subtitle}</h2>
              <div class="resources-grid">
                {#each RESOURCES as resource}
                  <a
                    href={resource.url}
                    target={resource.type === "internal" ? "_self" : "_blank"}
                    rel={resource.type !== "internal" ? "noopener noreferrer" : ""}
                    class="resource-card"
                    onclick={() => handleLinkClick(resource.url, resource.type)}
                  >
                    <div class="resource-icon">
                      {#if resource.icon.startsWith('/')}
                        <img src={resource.icon} alt={resource.title} />
                      {:else}
                        <i class={resource.icon}></i>
                      {/if}
                    </div>
                    <div class="resource-content">
                      <h3>{resource.title}</h3>
                      <p>{resource.description}</p>
                    </div>
                    <i class="fas fa-arrow-right resource-arrow"></i>
                  </a>
                {/each}
              </div>
            </div>
          </div>

          <!-- Community Panel -->
          <div class="carousel-panel">
            <div class="tab-panel" role="tabpanel">
              <h2 class="panel-title">{LANDING_TEXT.community.subtitle}</h2>
              <div class="social-grid">
                {#each SOCIAL_LINKS as social}
                  <a
                    href={social.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    class="social-button"
                    style="--brand-color: {social.color}"
                    title={social.name}
                  >
                    <i class={social.icon}></i>
                    <span>{social.name}</span>
                  </a>
                {/each}
              </div>
              <div class="contact-section">
                <h3 class="contact-title">
                  <i class="fas fa-envelope"></i>
                  {LANDING_TEXT.contact.title}
                </h3>
                <a href="mailto:{CONTACT_EMAIL}" class="contact-email">
                  {CONTACT_EMAIL}
                </a>
              </div>
            </div>
          </div>

          <!-- Support Panel -->
          <div class="carousel-panel">
            <div class="tab-panel" role="tabpanel">
              <h2 class="panel-title">{LANDING_TEXT.support.subtitle}</h2>
              <p class="support-message">{LANDING_TEXT.support.message}</p>
              <div class="support-grid">
                {#each SUPPORT_OPTIONS as option}
                  <a
                    href={option.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    class="support-button"
                    style="--brand-color: {option.color}"
                  >
                    <i class={option.icon}></i>
                    <span>Donate via {option.name}</span>
                  </a>
                {/each}
              </div>
            </div>
          </div>

          <!-- Dev Panel -->
          <div class="carousel-panel">
            <div class="tab-panel" role="tabpanel">
              <h2 class="panel-title">{LANDING_TEXT.dev.subtitle}</h2>
              <p class="support-message">{LANDING_TEXT.dev.message}</p>
              <div class="dev-links">
                <a
                  href="https://github.com/austencloud/tka-sequence-constructor"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="dev-card"
                >
                  <i class="fab fa-github"></i>
                  <div>
                    <h3>View on GitHub</h3>
                    <p>Explore the source code and contribute</p>
                  </div>
                </a>
                <a
                  href="mailto:tkaflowarts@gmail.com?subject=Development Collaboration"
                  class="dev-card"
                >
                  <i class="fas fa-envelope"></i>
                  <div>
                    <h3>Contact for Dev Work</h3>
                    <p>Want to collaborate or contribute? Get in touch</p>
                  </div>
                </a>
              </div>
            </div>
          </div>
        </HorizontalSwipeContainer>
      </div>

      <!-- CTA Button (Always Visible) -->
      <div class="cta-section">
        <button class="cta-button" onclick={handleEnterStudio}>
          <i class="fas fa-rocket"></i>
          {LANDING_TEXT.hero.cta}
        </button>
      </div>

      <!-- Bottom Navigation using PrimaryNavigation component -->
      <div class="landing-navigation">
        <PrimaryNavigation
          sections={landingSections}
          currentSection={activeTab}
          onSectionChange={handleTabChange}
          showModuleSwitcher={false}
          showSettings={false}
        />
      </div>
    </div>
  </div>
{/if}

<style>
  /* ============================================================================
     BACKDROP & MODAL BASE
     ============================================================================ */
  .landing-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(8px);
    z-index: 10000;
  }

  .landing-modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(20, 20, 30, 0.98) 0%, rgba(30, 30, 40, 0.98) 100%);
    z-index: 10001;
    overflow: hidden; /* No scrolling */
    display: flex;
    flex-direction: column;
  }

  /* ============================================================================
     CLOSE BUTTON
     ============================================================================ */
  .close-button {
    position: absolute;
    top: clamp(0.5rem, 1.5vh, 1rem);
    right: clamp(0.5rem, 1.5vw, 1rem);
    width: 44px;
    height: 44px;
    min-width: 44px; /* WCAG AAA */
    min-height: 44px;
    border-radius: 50%;
    border: 1px solid rgba(255, 255, 255, 0.2);
    background: rgba(255, 255, 255, 0.1);
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    font-size: 1.125rem;
    z-index: 10002;
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
    transform: scale(1.05);
  }

  .close-button:active {
    transform: scale(0.95);
  }

  .close-button:focus-visible {
    outline: 2px solid rgba(99, 102, 241, 0.7);
    outline-offset: 2px;
  }

  /* ============================================================================
     CONTENT LAYOUT (Viewport-aware, no scroll)
     ============================================================================ */
  .landing-content {
    width: 100%;
    height: 100vh;
    height: 100dvh; /* Dynamic viewport height for mobile */
    max-width: min(1200px, 100vw);
    margin: 0 auto;
    padding: clamp(1rem, 3vh, 2rem) clamp(1rem, 3vw, 2rem);
    /* Account for bottom navigation bar */
    padding-bottom: max(72px, calc(clamp(1rem, 3vh, 2rem) + 64px + env(safe-area-inset-bottom)));
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  /* ============================================================================
     HERO SECTION (Compact)
     ============================================================================ */
  .hero-section {
    text-align: center;
    padding: clamp(3.5rem, 8vh, 5rem) 0 clamp(0.5rem, 2vh, 1rem) 0;
    flex-shrink: 0;
  }

  .hero-title {
    font-size: clamp(1.75rem, 5vw, 3rem);
    font-weight: 900;
    margin-bottom: clamp(0.25rem, 1vh, 0.5rem);
    line-height: 1.1;
    position: relative;
    display: inline-block;
  }

  .gradient-text {
    background: linear-gradient(
      90deg,
      #667eea 0%,
      #764ba2 25%,
      #f43f5e 50%,
      #38bdf8 75%,
      #667eea 100%
    );
    background-size: 200% 100%;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient-flow 8s linear infinite;
  }

  @keyframes gradient-flow {
    0% {
      background-position: 0% 50%;
    }
    100% {
      background-position: 200% 50%;
    }
  }

  /* CSS Sparkles - Create star/cross shapes with pseudo-elements */
  .sparkle {
    position: absolute;
    width: 8px;
    height: 8px;
    opacity: 0;
    pointer-events: none;
    animation: twinkle 2.5s ease-in-out infinite;
  }

  /* Create cross shape with two lines */
  .sparkle::before,
  .sparkle::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg,
      transparent,
      currentColor,
      transparent
    );
    transform: translate(-50%, -50%);
  }

  .sparkle::before {
    transform: translate(-50%, -50%) rotate(0deg);
  }

  .sparkle::after {
    transform: translate(-50%, -50%) rotate(90deg);
  }

  /* Individual sparkle positioning and colors - Golden sparkles */
  .sparkle-1 {
    top: 0;
    left: 15%;
    color: #FFD700;
    animation-delay: 0s;
    width: 12px;
    height: 12px;
  }

  .sparkle-2 {
    top: 10%;
    right: 20%;
    color: #FFED4E;
    animation-delay: 0.8s;
    width: 8px;
    height: 8px;
  }

  .sparkle-3 {
    top: 15%;
    left: 50%;
    color: #FFC700;
    animation-delay: 1.5s;
    width: 10px;
    height: 10px;
  }

  .sparkle-4 {
    bottom: 10%;
    left: 25%;
    color: #FFBF00;
    animation-delay: 0.5s;
    width: 9px;
    height: 9px;
  }

  .sparkle-5 {
    bottom: 5%;
    right: 30%;
    color: #FFE55C;
    animation-delay: 2s;
    width: 11px;
    height: 11px;
  }

  .sparkle-6 {
    top: 50%;
    right: 10%;
    color: #FFA500;
    animation-delay: 1.2s;
    width: 7px;
    height: 7px;
  }

  @keyframes twinkle {
    0%, 100% {
      opacity: 0;
      transform: scale(0) rotate(0deg);
      filter: brightness(1);
    }
    50% {
      opacity: 1;
      transform: scale(1) rotate(180deg);
      filter: brightness(2) drop-shadow(0 0 4px currentColor);
    }
  }

  /* Add some that pulse at different rates for variety */
  .sparkle-1,
  .sparkle-4 {
    animation: twinkle 2.5s ease-in-out infinite;
  }

  .sparkle-2,
  .sparkle-5 {
    animation: twinkle 3s ease-in-out infinite;
  }

  .sparkle-3,
  .sparkle-6 {
    animation: twinkle 2.8s ease-in-out infinite;
  }

  .hero-subtitle {
    font-size: clamp(0.875rem, 2vw, 1.125rem);
    color: rgba(255, 255, 255, 0.8);
    margin: 0;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }

  /* ============================================================================
     CTA SECTION (Prominent, Always Visible)
     ============================================================================ */
  .cta-section {
    flex-shrink: 0;
    padding: clamp(0.75rem, 2vh, 1rem) 0;
    text-align: center;
  }

  .cta-button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.75rem;
    padding: clamp(1rem, 2.5vh, 1.25rem) clamp(2rem, 5vw, 3rem);
    min-height: 56px; /* Larger, more prominent */
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 2rem;
    font-size: clamp(1.0625rem, 3vw, 1.25rem);
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
  }

  .cta-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(102, 126, 234, 0.6);
  }

  .cta-button:active {
    transform: translateY(0);
  }

  .cta-button:focus-visible {
    outline: 2px solid rgba(99, 102, 241, 0.7);
    outline-offset: 2px;
  }

  .cta-button i {
    font-size: clamp(1.125rem, 3vw, 1.375rem);
  }

  /* ============================================================================
     TAB CONTENT (Fills remaining space)
     ============================================================================ */
  .tab-content {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  /* Carousel panel wrapper - ensures all panels are same size */
  .tab-content :global(.carousel-panel) {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  .tab-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center; /* Center content vertically */
    padding: clamp(0.75rem, 2vh, 1.5rem);
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1rem;
    overflow-y: auto;
    overflow-x: hidden;
  }

  .panel-title {
    font-size: clamp(1rem, 2.5vw, 1.25rem);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: clamp(0.75rem, 2vh, 1.5rem);
    text-align: center;
  }

  /* ============================================================================
     RESOURCES GRID
     ============================================================================ */
  .resources-grid {
    display: flex;
    flex-direction: column;
    gap: clamp(1.5rem, 3vh, 2rem);
    width: 100%;
  }

  .resource-card {
    display: flex;
    align-items: center;
    gap: clamp(1.25rem, 3vw, 1.75rem);
    padding: clamp(1.5rem, 3.5vh, 2.5rem) clamp(1.25rem, 3vw, 2rem);
    min-height: 120px; /* Much larger for better visibility */
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1.25rem;
    text-decoration: none;
    color: inherit;
    transition: all 0.2s ease;
  }

  .resource-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(102, 126, 234, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  }

  .resource-icon {
    width: clamp(80px, 15vw, 120px);
    height: clamp(80px, 15vw, 120px);
    background: rgba(255, 255, 255, 0.95);
    border-radius: 1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: clamp(2rem, 6vw, 3rem);
    color: #667eea;
    padding: clamp(0.5rem, 2vw, 1rem);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .resource-icon img {
    width: 100%;
    height: 100%;
    object-fit: contain;
  }

  .resource-content {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: column;
    gap: clamp(0.375rem, 1vh, 0.625rem);
  }

  .resource-content h3 {
    font-size: clamp(1.125rem, 3vw, 1.5rem);
    font-weight: 600;
    color: white;
    margin: 0;
    line-height: 1.2;
  }

  .resource-content p {
    font-size: clamp(0.9375rem, 2.25vw, 1.0625rem);
    color: rgba(255, 255, 255, 0.75);
    margin: 0;
    line-height: 1.5;
    /* Allow text to wrap naturally instead of clamping */
  }

  .resource-arrow {
    font-size: clamp(1.5rem, 4vw, 1.875rem);
    color: rgba(255, 255, 255, 0.5);
    transition: all 0.2s ease;
    flex-shrink: 0;
  }

  .resource-card:hover .resource-arrow {
    color: rgba(102, 126, 234, 0.9);
    transform: translateX(4px);
  }

  /* ============================================================================
     SOCIAL GRID (Expanded for better space utilization)
     ============================================================================ */
  .social-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: clamp(1rem, 2.5vw, 1.5rem);
    margin-bottom: clamp(1.5rem, 3vh, 2rem);
  }

  .social-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: clamp(0.625rem, 1.5vh, 0.875rem);
    padding: clamp(1.25rem, 3vh, 1.75rem) clamp(1rem, 2vw, 1.5rem);
    min-height: 96px; /* Larger touch target for better UX */
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1rem;
    text-decoration: none;
    color: white;
    transition: all 0.2s ease;
  }

  .social-button:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: var(--brand-color);
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  }

  .social-button i {
    font-size: clamp(2.25rem, 6vw, 3rem);
    color: var(--brand-color);
    filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.3));
  }

  .social-button span {
    font-size: clamp(0.9375rem, 2.25vw, 1.125rem);
    font-weight: 600;
  }

  /* Single row on larger screens for better horizontal space use */
  @media (min-width: 640px) {
    .social-grid {
      grid-template-columns: repeat(4, 1fr);
      gap: clamp(1rem, 2vw, 1.5rem);
    }

    .social-button {
      min-height: 108px;
    }
  }

  /* ============================================================================
     SUPPORT SECTION
     ============================================================================ */
  .support-message {
    font-size: clamp(0.875rem, 2vw, 1rem);
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: clamp(1rem, 2vh, 1.5rem);
    line-height: 1.5;
    text-align: center;
  }

  .support-grid {
    display: flex;
    flex-direction: column;
    gap: clamp(1rem, 2.5vh, 1.5rem);
    width: 100%;
  }

  .support-button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: clamp(0.75rem, 2vw, 1rem);
    padding: clamp(1.25rem, 3vh, 1.75rem) clamp(2rem, 4vw, 2.5rem);
    min-height: 68px; /* Larger, more prominent touch target */
    width: 100%; /* Fill container width */
    background: linear-gradient(135deg, var(--brand-color) 0%, color-mix(in srgb, var(--brand-color) 80%, black) 100%);
    border: 2px solid color-mix(in srgb, var(--brand-color) 60%, white);
    border-radius: 1rem;
    text-decoration: none;
    color: white;
    font-weight: 700;
    font-size: clamp(1rem, 2.75vw, 1.1875rem);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow:
      0 6px 20px color-mix(in srgb, var(--brand-color) 40%, transparent),
      0 2px 8px rgba(0, 0, 0, 0.3),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    position: relative;
    overflow: hidden;
  }

  /* Animated shine effect */
  .support-button::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.2),
      transparent
    );
    transition: left 0.5s ease;
  }

  .support-button:hover::before {
    left: 100%;
  }

  .support-button:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow:
      0 10px 30px color-mix(in srgb, var(--brand-color) 50%, transparent),
      0 4px 12px rgba(0, 0, 0, 0.4),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
    border-color: color-mix(in srgb, var(--brand-color) 80%, white);
    filter: brightness(1.15) saturate(1.1);
  }

  .support-button:active {
    transform: translateY(-1px) scale(1.01);
    box-shadow:
      0 6px 20px color-mix(in srgb, var(--brand-color) 40%, transparent),
      0 2px 8px rgba(0, 0, 0, 0.3),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
  }

  .support-button:focus-visible {
    outline: 3px solid rgba(255, 255, 255, 0.6);
    outline-offset: 3px;
  }

  .support-button i {
    font-size: clamp(1.5rem, 3.5vw, 1.875rem);
    filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
    transition: transform 0.3s ease;
  }

  .support-button:hover i {
    transform: scale(1.15) rotate(-5deg);
  }

  @media (min-width: 640px) {
    .support-grid {
      flex-direction: row;
      gap: clamp(1rem, 2vw, 1.5rem);
    }

    .support-button {
      flex: 1; /* Equal width buttons on desktop */
    }
  }

  /* ============================================================================
     DEV SECTION
     ============================================================================ */
  .dev-links {
    display: flex;
    flex-direction: column;
    gap: clamp(1rem, 2vh, 1.5rem);
  }

  .dev-card {
    display: flex;
    align-items: center;
    gap: clamp(1rem, 2vw, 1.5rem);
    padding: clamp(1rem, 2.5vh, 1.5rem);
    min-height: 80px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0.75rem;
    text-decoration: none;
    color: inherit;
    transition: all 0.2s ease;
  }

  .dev-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(34, 197, 94, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
  }

  .dev-card i {
    font-size: clamp(2rem, 5vw, 2.5rem);
    color: rgba(34, 197, 94, 0.9);
    flex-shrink: 0;
  }

  .dev-card div {
    flex: 1;
    min-width: 0;
  }

  .dev-card h3 {
    font-size: clamp(1rem, 2.5vw, 1.125rem);
    font-weight: 600;
    color: white;
    margin: 0 0 0.25rem 0;
  }

  .dev-card p {
    font-size: clamp(0.875rem, 2vw, 1rem);
    color: rgba(255, 255, 255, 0.7);
    margin: 0;
    line-height: 1.4;
  }

  /* ============================================================================
     CONTACT SECTION
     ============================================================================ */
  .contact-section {
    margin-top: auto;
    padding-top: clamp(1rem, 2vh, 1.5rem);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    text-align: center;
  }

  .contact-title {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    font-size: clamp(0.9375rem, 2vw, 1.125rem);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: 0.75rem;
  }

  .contact-title i {
    font-size: clamp(1rem, 2.5vw, 1.25rem);
    color: rgba(102, 126, 234, 0.9);
  }

  .contact-email {
    display: inline-block;
    font-size: clamp(0.875rem, 2vw, 1rem);
    color: rgba(102, 126, 234, 0.9);
    text-decoration: none;
    padding: clamp(0.625rem, 1.5vh, 0.875rem) clamp(1rem, 2vw, 1.5rem);
    background: rgba(102, 126, 234, 0.1);
    border: 1px solid rgba(102, 126, 234, 0.3);
    border-radius: 0.5rem;
    transition: all 0.2s ease;
  }

  .contact-email:hover {
    background: rgba(102, 126, 234, 0.15);
    border-color: rgba(102, 126, 234, 0.5);
    transform: translateY(-1px);
  }

  /* ============================================================================
     LANDING NAVIGATION OVERRIDES
     ============================================================================ */
  /* With only 3 tabs, always show labels for better UX */
  .landing-navigation :global(.primary-navigation.layout-bottom .nav-label-full) {
    display: block;
  }

  .landing-navigation :global(.primary-navigation.layout-bottom .nav-button) {
    max-width: 120px;
    gap: 4px;
  }

  /* Increase button size for better touch targets */
  .landing-navigation :global(.primary-navigation.layout-bottom .nav-button) {
    min-width: 80px;
    padding: 8px 12px;
  }

  /* Ensure icons and labels are properly sized */
  .landing-navigation :global(.primary-navigation.layout-bottom .nav-icon) {
    font-size: 22px;
  }

  .landing-navigation :global(.primary-navigation.layout-bottom .nav-label) {
    font-size: 11px;
    font-weight: 600;
  }

  /* ============================================================================
     ACCESSIBILITY & RESPONSIVE
     ============================================================================ */

  /* Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
      transition: none !important;
      animation: none !important;
    }

    .gradient-text {
      animation: none;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .sparkle {
      display: none;
    }

    .support-button::before {
      display: none;
    }

    .cta-button:hover,
    .cta-button:active,
    .resource-card:hover,
    .social-button:hover,
    .support-button:hover,
    .support-button:active,
    .support-button:hover i,
    .dev-card:hover,
    .contact-email:hover,
    .close-button:hover {
      transform: none;
    }
  }

  /* High Contrast */
  @media (prefers-contrast: high) {
    .landing-modal {
      background: rgba(0, 0, 0, 0.98);
      border: 2px solid white;
    }

    .tab-panel,
    .resource-card,
    .social-button,
    .support-button,
    .dev-card {
      border: 2px solid white;
    }
  }

  /* Very small screens - extra compact */
  @media (max-height: 600px) {
    .hero-section {
      padding: 0.25rem 0;
    }

    .hero-title {
      font-size: clamp(1.25rem, 4vw, 1.75rem);
    }

    .hero-subtitle {
      font-size: clamp(0.75rem, 1.5vw, 0.875rem);
    }

    .cta-section {
      padding: 0.5rem 0;
    }

    .cta-button {
      min-height: 48px;
      padding: 0.75rem 1.5rem;
      font-size: 0.9375rem;
    }

    .panel-title {
      margin-bottom: 0.5rem;
    }
  }
</style>
