<script lang="ts">
  import { onMount } from "svelte";
  import { fade, fly } from "svelte/transition";
  import { cubicOut, quartOut } from "svelte/easing";
  import { browser } from "$app/environment";
  import type { EmblaCarouselType } from "embla-carousel";

  import {
    resolve,
    TYPES,
    type IHapticFeedbackService,
    HorizontalSwipeContainer,
  } from "$shared";
  import {
    infoUIState,
    closeInfo,
  } from "../state/info-state.svelte";
  import {
    CONTACT_EMAIL,
    INFO_SECTIONS,
    INFO_TEXT,
    type InfoTab,
    RESOURCES,
    SOCIAL_LINKS,
    SUPPORT_OPTIONS,
  } from "../domain";

  import InfoHeroSection from "./InfoHeroSection.svelte";
  import InfoTabNavigation from "./InfoTabNavigation.svelte";
  import InfoResourcesPanel from "./InfoResourcesPanel.svelte";
  import InfoCommunityPanel from "./InfoCommunityPanel.svelte";
  import InfoDevPanel from "./InfoDevPanel.svelte";
  import InfoCTASection from "./InfoCTASection.svelte";

  const showCloseButton = $derived(!infoUIState.isAutoOpened);

  let activeTab = $state<InfoTab>("resources");
  let emblaApi: EmblaCarouselType | undefined = $state(undefined);

  // Track if we're on desktop for responsive layout
  let isDesktop = $state(false);

  // Services
  let hapticService: IHapticFeedbackService | null = $state(null);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );

    document.addEventListener("keydown", handleKeydown);

    // Check if desktop on mount and on resize
    const checkDesktop = () => {
      isDesktop = window.innerWidth >= 1024;
    };
    checkDesktop();
    window.addEventListener("resize", checkDesktop);

    return () => {
      document.removeEventListener("keydown", handleKeydown);
      window.removeEventListener("resize", checkDesktop);
    };
  });

  function handleTabChange(tabId: InfoTab) {
    const index = INFO_SECTIONS.findIndex((section) => section.id === tabId);
    if (index !== -1 && emblaApi) {
      emblaApi.scrollTo(index);
    }
  }

  function handlePanelChange(panelIndex: number) {
    const section = INFO_SECTIONS[panelIndex];
    if (section) {
      activeTab = section.id as InfoTab;
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (
      event.key === "Escape" &&
      infoUIState.isOpen &&
      !infoUIState.isAutoOpened
    ) {
      handleCloseClick();
    }
  }

  function handleBackdropClick() {
    if (!infoUIState.isAutoOpened) {
      handleCloseClick();
    }
  }

  function handleCloseClick() {
    // Trigger haptic feedback for modal close
    hapticService?.trigger("selection");
    closeInfo(false);
  }

  function handleEnterStudio() {
    if (infoUIState.isAutoOpened) {
      closeInfo(true);
    } else {
      closeInfo(false);
    }
  }

  function handleModalClick(event: MouseEvent) {
    event.stopPropagation();
  }

  function handleResourceNavigate(resource: (typeof RESOURCES)[number]) {
    handleLinkClick(resource.url, resource.type);
  }

  function handleLinkClick(
    url: string,
    type: (typeof RESOURCES)[number]["type"]
  ) {
    if (browser && (type === "download" || type === "external")) {
      window.open(url, "_blank", "noopener,noreferrer");
    }
  }

  function handleSocialClick(
    event: MouseEvent,
    social: (typeof SOCIAL_LINKS)[number]
  ) {
    // Let browser handle all social/payment links naturally
    // No special handling needed
  }
</script>

{#if infoUIState.isOpen}
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <div
    class="info-backdrop"
    role="button"
    tabindex="-1"
    onclick={handleBackdropClick}
    transition:fade={{ duration: 300, easing: cubicOut }}
  ></div>

  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <div
    class="info-modal"
    role="dialog"
    aria-modal="true"
    aria-labelledby="info-title"
    tabindex="-1"
    onclick={handleModalClick}
    in:fly={{ y: isDesktop ? 30 : 100, duration: 400, easing: quartOut, opacity: 0 }}
    out:fade={{ duration: 250, easing: cubicOut }}
  >
    {#if showCloseButton}
      <button
        class="close-button"
        type="button"
        aria-label="Close info page"
        title="Close (Esc)"
        onclick={handleCloseClick}
      >
        <i class="fas fa-times"></i>
      </button>
    {/if}

    <div class="info-content" class:desktop={isDesktop}>
      <InfoHeroSection hero={INFO_TEXT.hero} />

      {#if !isDesktop}
        <!-- Mobile: Swipeable tabs -->
        <InfoTabNavigation
          sections={INFO_SECTIONS}
          {activeTab}
          onSelect={handleTabChange}
        />

        <div class="tab-content">
          <HorizontalSwipeContainer
            panels={INFO_SECTIONS}
            initialPanelIndex={0}
            onPanelChange={handlePanelChange}
            showArrows={false}
            showIndicators={false}
            height="100%"
            width="100%"
            bind:emblaApiRef={emblaApi}
          >
            <InfoResourcesPanel
              panelId="panel-resources"
              labelledBy="tab-resources"
              copy={INFO_TEXT.resources}
              resources={RESOURCES}
              onLinkClick={handleResourceNavigate}
            />

            <InfoCommunityPanel
              panelId="panel-support"
              labelledBy="tab-support"
              copy={INFO_TEXT.support}
              socialLinks={SOCIAL_LINKS}
              supportOptions={SUPPORT_OPTIONS}
              onSocialClick={handleSocialClick}
              onSupportClick={handleSocialClick}
            />

            <InfoDevPanel
              panelId="panel-dev"
              labelledBy="tab-dev"
              copy={INFO_TEXT.dev}
              githubUrl="https://github.com/austencloud/tka-studio"
              discordUrl={SOCIAL_LINKS.find((link) => link.name === "Discord")
                ?.url || "https://discord.gg/tka"}
              contactEmail={CONTACT_EMAIL}
            />
          </HorizontalSwipeContainer>
        </div>
      {:else}
        <!-- Desktop: All panels visible in grid -->
        <div class="desktop-panels-grid">
          <div class="desktop-panel">
            <h2 class="desktop-panel-title">{INFO_TEXT.resources.title}</h2>
            <InfoResourcesPanel
              panelId="panel-resources"
              labelledBy="desktop-resources"
              copy={INFO_TEXT.resources}
              resources={RESOURCES}
              onLinkClick={handleResourceNavigate}
            />
          </div>

          <div class="desktop-panel">
            <h2 class="desktop-panel-title">{INFO_TEXT.support.title}</h2>
            <InfoCommunityPanel
              panelId="panel-support"
              labelledBy="desktop-support"
              copy={INFO_TEXT.support}
              socialLinks={SOCIAL_LINKS}
              supportOptions={SUPPORT_OPTIONS}
              onSocialClick={handleSocialClick}
              onSupportClick={handleSocialClick}
            />
          </div>

          <div class="desktop-panel">
            <h2 class="desktop-panel-title">{INFO_TEXT.dev.title}</h2>
            <InfoDevPanel
              panelId="panel-dev"
              labelledBy="desktop-dev"
              copy={INFO_TEXT.dev}
              githubUrl="https://github.com/austencloud/tka-studio"
              discordUrl={SOCIAL_LINKS.find((link) => link.name === "Discord")
                ?.url || "https://discord.gg/tka"}
              contactEmail={CONTACT_EMAIL}
            />
          </div>
        </div>
      {/if}

      <InfoCTASection
        ctaLabel={INFO_TEXT.hero.cta}
        onEnterStudio={handleEnterStudio}
      />
    </div>
  </div>
{/if}

<style>
  .info-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(12px);
    z-index: 10000;
  }

  .info-modal {
    position: fixed;
    inset: 0;
    background: linear-gradient(
      135deg,
      rgba(20, 20, 30, 0.98) 0%,
      rgba(30, 30, 40, 0.98) 100%
    );
    z-index: 10001;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }

  .close-button {
    position: absolute;
    top: clamp(0.5rem, 1.5vh, 1rem);
    right: clamp(0.5rem, 1.5vw, 1rem);
    width: 44px;
    height: 44px;
    min-width: 44px;
    min-height: 44px;
    border-radius: 50%;
    border: 1px solid rgba(255, 255, 255, 0.2);
    background: rgba(255, 255, 255, 0.1);
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    font-size: 1.125rem;
    z-index: 10002;
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.18);
    border-color: rgba(255, 255, 255, 0.35);
    transform: scale(1.08);
  }

  .close-button:active {
    transform: scale(0.95);
  }

  .close-button:focus-visible {
    outline: 2px solid rgba(99, 102, 241, 0.7);
    outline-offset: 2px;
  }

  .info-content {
    width: 100%;
    height: 100vh;
    height: 100dvh;
    margin: 0 auto;
    padding: 0 clamp(0.5rem, 2vw, 1rem) clamp(0.5rem, 2vh, 1rem);
    padding-top: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .tab-content {
    flex: 1;
    min-height: 0;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .tab-content :global(.carousel-panel) {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
  }

  :global(.tab-panel) {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 0.75rem;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 1rem;
    overflow-y: auto;
    overflow-x: hidden;
  }

  @media (min-width: 640px) {
    :global(.tab-panel) {
      padding: 1rem;
    }
  }

  :global(.panel-title) {
    font-size: 0.9375rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    margin-bottom: 0.625rem;
    text-align: center;
    flex-shrink: 0;
  }

  @media (min-width: 640px) {
    :global(.panel-title) {
      font-size: 1rem;
      margin-bottom: 0.75rem;
    }
  }

  /* ============================================================================
     DESKTOP LAYOUT (1024px+)
     ============================================================================ */
  @media (min-width: 1024px) {
    .info-modal {
      /* Maximize width to show all content */
      inset: 5vh 5vw;
      max-height: 90vh;
      max-width: 90vw;
      margin: auto;
      border-radius: 1.5rem;
      border: 1px solid rgba(255, 255, 255, 0.15);
      box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    }

    .info-content.desktop {
      height: 100%;
      max-height: none;
      padding: clamp(0.75rem, 1.5vh, 1.25rem) clamp(0.75rem, 1.25vw, 1.25rem);
      gap: clamp(0.5rem, 1vh, 0.75rem);
    }

    .desktop-panels-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: clamp(0.75rem, 1vw, 1.25rem);
      flex: 1;
      min-height: 0;
      overflow: hidden;
      align-items: stretch;
      justify-content: center;
      align-content: center;
    }

    .desktop-panel {
      display: flex;
      flex-direction: column;
      overflow: visible;
      container-type: inline-size;
      container-name: info-panel;
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 1rem;
      padding: clamp(0.75rem, 1.5vh, 1rem);
    }

    .desktop-panel-title {
      font-size: clamp(0.875rem, 2.5cqh, 1.0625rem);
      font-weight: 700;
      color: rgba(255, 255, 255, 0.95);
      margin: 0 0 clamp(0.375rem, 1.5cqh, 0.5rem) 0;
      text-align: center;
      flex-shrink: 0;
      padding-bottom: clamp(0.25rem, 1cqh, 0.375rem);
      border-bottom: 2px solid rgba(255, 255, 255, 0.1);
    }

    /* Each panel's content is naturally sized based on content */
    .desktop-panel :global(.carousel-panel) {
      overflow: visible;
      display: flex;
      flex-direction: column;
    }

    .desktop-panel :global(.tab-panel) {
      overflow: visible !important;
      display: flex;
      flex-direction: column;
    }
  }

  /* Extra large screens - make it even more spacious */
  @media (min-width: 1440px) {
    .desktop-panels-grid {
      gap: 2rem;
    }

    .info-content.desktop {
      padding: 2.5rem 3rem;
    }
  }

  @media (prefers-contrast: high) {
    .info-modal {
      background: rgba(0, 0, 0, 0.98);
      border: 2px solid white;
    }

    :global(.tab-panel),
    :global(.resource-card),
    :global(.social-button),
    :global(.support-button),
    :global(.dev-card) {
      border: 2px solid white;
    }
  }

  @media (max-height: 600px) {
    :global(.panel-title) {
      margin-bottom: 0.5rem;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .close-button:hover,
    .close-button:active {
      transform: none;
    }
  }
</style>
