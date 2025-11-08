<script lang="ts">
  import { onMount } from "svelte";
  import { fade, scale } from "svelte/transition";
  import { cubicOut } from "svelte/easing";
  import { browser } from "$app/environment";
  import type { EmblaCarouselType } from "embla-carousel";

  import { HorizontalSwipeContainer } from "$shared";
  import { landingUIState, closeLanding } from "../state/landing-state.svelte";
  import {
    CONTACT_EMAIL,
    LANDING_SECTIONS,
    LANDING_TEXT,
    RESOURCES,
    SOCIAL_LINKS,
    SUPPORT_OPTIONS,
    type LandingTab,
  } from "../domain";
  import {
    smartContact,
    smartEmailContact,
    DEV_CONTACT_OPTIONS,
  } from "../utils/smart-contact";

  import LandingHeroSection from "./LandingHeroSection.svelte";
  import LandingTabNavigation from "./LandingTabNavigation.svelte";
  import LandingResourcesPanel from "./LandingResourcesPanel.svelte";
  import LandingCommunityPanel from "./LandingCommunityPanel.svelte";
  import LandingSupportPanel from "./LandingSupportPanel.svelte";
  import LandingDevPanel from "./LandingDevPanel.svelte";
  import LandingCTASection from "./LandingCTASection.svelte";

  const showCloseButton = $derived(!landingUIState.isAutoOpened);

  let activeTab = $state<LandingTab>("resources");
  let emblaApi: EmblaCarouselType | undefined = $state(undefined);
  let isContactLoading = $state(false);

  function handleTabChange(tabId: LandingTab) {
    const index = LANDING_SECTIONS.findIndex((section) => section.id === tabId);
    if (index !== -1 && emblaApi) {
      emblaApi.scrollTo(index);
    }
  }

  function handlePanelChange(panelIndex: number) {
    const section = LANDING_SECTIONS[panelIndex];
    if (section) {
      activeTab = section.id as LandingTab;
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (
      event.key === "Escape" &&
      landingUIState.isOpen &&
      !landingUIState.isAutoOpened
    ) {
      closeLanding(false);
    }
  }

  function handleBackdropClick() {
    if (!landingUIState.isAutoOpened) {
      closeLanding(false);
    }
  }

  function handleEnterStudio() {
    if (landingUIState.isAutoOpened) {
      closeLanding(true);
    } else {
      closeLanding(false);
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

  async function handleDevContact() {
    if (browser && !isContactLoading) {
      isContactLoading = true;
      try {
        await smartContact(DEV_CONTACT_OPTIONS);
      } catch (error) {
        console.error("Failed to initiate contact:", error);
      } finally {
        setTimeout(() => {
          isContactLoading = false;
        }, 1000);
      }
    }
  }

  async function handleSocialClick(
    event: MouseEvent,
    social: (typeof SOCIAL_LINKS)[number]
  ) {
    if (social.url.startsWith("mailto:")) {
      event.preventDefault();
      const email = social.url.replace("mailto:", "");
      await smartEmailContact(email);
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
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <div
    class="landing-backdrop"
    role="button"
    tabindex="-1"
    onclick={handleBackdropClick}
    transition:fade={{ duration: 350, easing: cubicOut }}
  ></div>

  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <!-- svelte-ignore a11y_click_events_have_key_events -->
  <div
    class="landing-modal"
    role="dialog"
    aria-modal="true"
    aria-labelledby="landing-title"
    tabindex="-1"
    onclick={handleModalClick}
    transition:scale={{ duration: 400, easing: cubicOut, start: 0.95 }}
  >
    {#if showCloseButton}
      <button
        class="close-button"
        type="button"
        aria-label="Close landing page"
        title="Close (Esc)"
        onclick={() => closeLanding(false)}
      >
        <i class="fas fa-times"></i>
      </button>
    {/if}

    <div class="landing-content">
      <LandingHeroSection hero={LANDING_TEXT.hero} />

      <LandingTabNavigation
        sections={LANDING_SECTIONS}
        {activeTab}
        onSelect={handleTabChange}
      />

      <div class="tab-content">
        <HorizontalSwipeContainer
          panels={LANDING_SECTIONS}
          initialPanelIndex={0}
          onPanelChange={handlePanelChange}
          showArrows={false}
          showIndicators={false}
          height="100%"
          width="100%"
          bind:emblaApiRef={emblaApi}
        >
          <LandingResourcesPanel
            panelId="panel-resources"
            labelledBy="tab-resources"
            copy={LANDING_TEXT.resources}
            resources={RESOURCES}
            onLinkClick={handleResourceNavigate}
          />

          <LandingCommunityPanel
            panelId="panel-community"
            labelledBy="tab-community"
            copy={LANDING_TEXT.community}
            socialLinks={SOCIAL_LINKS}
            onSocialClick={handleSocialClick}
          />

          <LandingSupportPanel
            panelId="panel-support"
            labelledBy="tab-support"
            copy={LANDING_TEXT.support}
            supportOptions={SUPPORT_OPTIONS}
          />

          <LandingDevPanel
            panelId="panel-dev"
            labelledBy="tab-dev"
            copy={LANDING_TEXT.dev}
            contactEmail={CONTACT_EMAIL}
            onContact={handleDevContact}
            {isContactLoading}
            enableSmartContact={browser}
          />
        </HorizontalSwipeContainer>
      </div>

      <LandingCTASection
        ctaLabel={LANDING_TEXT.hero.cta}
        onEnterStudio={handleEnterStudio}
      />
    </div>
  </div>
{/if}

<style>
  .landing-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(8px);
    z-index: 10000;
  }

  .landing-modal {
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

  .landing-content {
    width: 100%;
    height: 100vh;
    height: 100dvh;
    max-width: min(1200px, 100vw);
    margin: 0 auto;
    padding: 0 clamp(1rem, 3vw, 2rem) clamp(1rem, 3vh, 2rem);
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

  @media (prefers-contrast: high) {
    .landing-modal {
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
