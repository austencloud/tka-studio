<!--
  EnhancedPWAInstallGuide.svelte

  Polished PWA installation guide with:
  - Intelligent device/browser detection
  - Platform-specific screenshots
  - Font Awesome icons
  - Glass morphism styling
  - Step-by-step visual guidance
  - Container-aware responsive layout
  - Runes-based reactive sizing
-->
<script lang="ts">
  import { onMount } from "svelte";
  import { fade, fly } from "svelte/transition";

  // Props
  let {
    showGuide = $bindable(false),
  }: {
    showGuide?: boolean;
  } = $props();

  // State
  type Platform = "ios" | "android" | "desktop";
  type Browser = "chrome" | "safari" | "edge" | "firefox" | "samsung" | "other";

  let platform = $state<Platform>("desktop");
  let browser = $state<Browser>("other");

  // Container measurements for intelligent sizing
  let sheetElement = $state<HTMLElement | null>(null);
  let contentElement = $state<HTMLElement | null>(null);
  let needsCompactMode = $state(false);

  onMount(() => {
    detectPlatformAndBrowser();

    // Delay measurement to allow DOM to render
    setTimeout(() => {
      measureAndAdapt();

      // Set up resize observer for continuous adaptation
      const resizeObserver = new ResizeObserver(() => {
        measureAndAdapt();
      });

      if (sheetElement) {
        resizeObserver.observe(sheetElement);
      }

      return () => {
        resizeObserver.disconnect();
      };
    }, 100);
  });

  function measureAndAdapt() {
    if (!sheetElement || !contentElement) return;

    try {
      // Get actual viewport height
      const viewportHeight = window.visualViewport?.height || window.innerHeight;

      // Calculate fixed elements height (header + footer + handle + padding)
      const headerHeight = sheetElement.querySelector('.guide-header')?.clientHeight || 70;
      const footerHeight = sheetElement.querySelector('.guide-footer')?.clientHeight || 70;
      const handleHeight = 25; // Handle + margins

      // Available space for scrollable content
      const available = viewportHeight * 0.95 - headerHeight - footerHeight - handleHeight;

      // Measure actual content height
      if (contentElement) {
        const scrollHeight = contentElement.scrollHeight;

        // Determine if we need compact mode
        needsCompactMode = scrollHeight > available;
      }
    } catch (error) {
      // Silently fail if measurement doesn't work
      console.warn('PWA guide measurement failed:', error);
    }
  }

  function detectPlatformAndBrowser() {
    const ua = navigator.userAgent.toLowerCase();

    // Detect platform
    if (/iphone|ipad|ipod/.test(ua)) {
      platform = "ios";
    } else if (/android/.test(ua)) {
      platform = "android";
    } else {
      platform = "desktop";
    }

    // Detect browser
    const isSamsung = ua.includes("samsungbrowser");
    const isEdge = ua.includes("edg/");
    const isFirefox = ua.includes("firefox") || ua.includes("fxios");
    const isChrome =
      (ua.includes("chrome") || ua.includes("crios")) &&
      !isEdge &&
      !isSamsung;
    const isSafari =
      !isChrome && !isEdge && !isFirefox && ua.includes("safari");

    if (isSamsung) browser = "samsung";
    else if (isEdge) browser = "edge";
    else if (isFirefox) browser = "firefox";
    else if (isChrome) browser = "chrome";
    else if (isSafari) browser = "safari";
    else browser = "other";
  }

  function handleClose() {
    showGuide = false;
  }

  // Platform-specific instructions
  const instructions = $derived(() => {
    if (platform === "ios" && browser === "safari") {
      return {
        title: "Install TKA on iPhone/iPad",
        icon: "fab fa-apple",
        steps: [
          {
            text: 'Tap the <strong>Share</strong> button at the bottom of Safari',
            icon: "fas fa-share",
            image: null, // TODO: Add screenshot to /static/images/install-guides/ios-safari-step1.png
          },
          {
            text: 'Scroll down and tap <strong>"Add to Home Screen"</strong>',
            icon: "fas fa-plus-square",
            image: null, // TODO: Add screenshot to /static/images/install-guides/ios-safari-step2.png
          },
          {
            text: 'Tap <strong>"Add"</strong> in the top-right corner',
            icon: "fas fa-check-circle",
            image: null, // TODO: Add screenshot to /static/images/install-guides/ios-safari-step3.png
          },
          {
            text: "Find the TKA icon on your home screen and tap it to launch",
            icon: "fas fa-mobile-alt",
            image: null,
          },
        ],
        benefits: [
          "Opens in fullscreen without Safari UI",
          "Faster loading with offline support",
          "Quick access from home screen",
        ],
      };
    }

    if (platform === "ios" && browser !== "safari") {
      return {
        title: "Install TKA on iPhone/iPad",
        icon: "fab fa-apple",
        steps: [
          {
            text: 'Open this page in <strong>Safari</strong> (iOS only supports PWA installation in Safari)',
            icon: "fab fa-safari",
            image: null,
          },
          {
            text: 'Tap the <strong>Share</strong> button at the bottom',
            icon: "fas fa-share",
            image: null, // TODO: Add screenshot
          },
          {
            text: 'Tap <strong>"Add to Home Screen"</strong>',
            icon: "fas fa-plus-square",
            image: null, // TODO: Add screenshot
          },
        ],
        benefits: [
          "Fullscreen app-like experience",
          "Works offline",
          "No browser UI distractions",
        ],
      };
    }

    if (platform === "android" && (browser === "chrome" || browser === "edge")) {
      return {
        title: "Install TKA on Android",
        icon: "fab fa-android",
        steps: [
          {
            text: 'Tap the <strong>menu (⋮)</strong> in the top-right corner',
            icon: "fas fa-ellipsis-v",
            image: null, // TODO: Add screenshot to /static/images/install-guides/android-chrome-step1.png
          },
          {
            text: 'Select <strong>"Add to Home screen"</strong> or <strong>"Install app"</strong>',
            icon: "fas fa-download",
            image: null, // TODO: Add screenshot to /static/images/install-guides/android-chrome-step2.png
          },
          {
            text: 'Tap <strong>"Install"</strong> or <strong>"Add"</strong> to confirm',
            icon: "fas fa-check-circle",
            image: null, // TODO: Add screenshot to /static/images/install-guides/android-chrome-step3.png
          },
          {
            text: "Launch TKA from your home screen or app drawer",
            icon: "fas fa-rocket",
            image: null,
          },
        ],
        benefits: [
          "Native app-like experience",
          "Automatic fullscreen",
          "Works offline",
        ],
      };
    }

    if (platform === "android" && browser === "samsung") {
      return {
        title: "Install TKA on Android (Samsung Internet)",
        icon: "fab fa-android",
        steps: [
          {
            text: 'Tap the <strong>menu (☰)</strong> at the bottom',
            icon: "fas fa-bars",
            image: null, // TODO: Add screenshot to /static/images/install-guides/android-samsung-step1.png
          },
          {
            text: 'Select <strong>"Add page to"</strong> → <strong>"Home screen"</strong>',
            icon: "fas fa-plus-circle",
            image: null, // TODO: Add screenshot to /static/images/install-guides/android-samsung-step2.png
          },
          {
            text: 'Tap <strong>"Add"</strong> to confirm',
            icon: "fas fa-check",
            image: null,
          },
          {
            text: "Launch from your home screen",
            icon: "fas fa-mobile-alt",
            image: null,
          },
        ],
        benefits: [
          "Fullscreen experience",
          "Quick home screen access",
          "Offline support",
        ],
      };
    }

    if (platform === "desktop" && (browser === "chrome" || browser === "edge")) {
      return {
        title: "Install TKA on Desktop",
        icon: "fas fa-desktop",
        steps: [
          {
            text: 'Look for the <strong>install icon (⊕)</strong> in the address bar',
            icon: "fas fa-plus-circle",
            image: null, // TODO: Add screenshot to /static/images/install-guides/desktop-chrome-step1.png
          },
          {
            text: 'Click the icon and select <strong>"Install"</strong>',
            icon: "fas fa-download",
            image: null, // TODO: Add screenshot to /static/images/install-guides/desktop-chrome-step2.png
          },
          {
            text: "Or open the menu (⋮) and select <strong>\"Install TKA\"</strong>",
            icon: "fas fa-ellipsis-v",
            image: null,
          },
          {
            text: "Launch TKA from your desktop, taskbar, or start menu",
            icon: "fas fa-window-maximize",
            image: null,
          },
        ],
        benefits: [
          "Standalone window without browser chrome",
          "Pin to taskbar or dock",
          "Faster startup",
        ],
      };
    }

    // Fallback for unsupported browsers
    return {
      title: "Installation Not Available",
      icon: "fas fa-info-circle",
      steps: [
        {
          text: "Your current browser doesn't fully support PWA installation",
          icon: "fas fa-exclamation-triangle",
          image: null,
        },
        {
          text: platform === "ios"
            ? "On iOS, please use Safari for installation"
            : "Try using Chrome, Edge, or Samsung Internet",
          icon: "fas fa-browser",
          image: null,
        },
      ],
      benefits: [
        "Better user experience",
        "Offline support",
        "App-like interface",
      ],
    };
  });
</script>

{#if showGuide}
  <!-- Backdrop -->
  <div
    class="guide-backdrop"
    onclick={handleClose}
    transition:fade={{ duration: 250 }}
    role="presentation"
  ></div>

  <!-- Guide Bottom Sheet -->
  <div
    class="guide-sheet"
    class:compact={needsCompactMode}
    bind:this={sheetElement}
    transition:fly={{ y: 500, duration: 350 }}
  >
    <!-- Handle bar for swipe affordance -->
    <div class="sheet-handle"></div>

    <div class="guide-header">
      <div class="header-title">
        <i class="{instructions().icon} title-icon"></i>
        <h2>{instructions().title}</h2>
      </div>
      <button class="close-btn" onclick={handleClose} aria-label="Close guide">
        <i class="fas fa-times"></i>
      </button>
    </div>

    <div class="guide-content" bind:this={contentElement}>
      <!-- Steps with Screenshots -->
      <div class="steps-section">
        <h3 class="section-heading">
          <i class="fas fa-list-ol"></i>
          <span>Follow These Steps</span>
        </h3>
        <div class="steps-grid">
          {#each instructions().steps as step, index}
            <div class="step-card">
              <div class="step-header">
                <div class="step-number">{index + 1}</div>
                <div class="step-text">{@html step.text}</div>
              </div>
              <!-- Show placeholder for future screenshots (only when not in compact mode) -->
              {#if !needsCompactMode}
                <div class="step-image-container">
                  <div class="image-placeholder">
                    <i class="fas fa-image"></i>
                    <span class="placeholder-text">Screenshot coming soon</span>
                  </div>
                </div>
              {/if}
            </div>
          {/each}
        </div>
      </div>

      <!-- Benefits -->
      <div class="benefits-section">
        <h3 class="section-heading">
          <i class="fas fa-star"></i>
          <span>Why Install?</span>
        </h3>
        <div class="benefits-grid">
          {#each instructions().benefits as benefit}
            <div class="benefit-item">
              <i class="fas fa-check-circle"></i>
              <span>{benefit}</span>
            </div>
          {/each}
        </div>
      </div>
    </div>

    <!-- Sticky Footer -->
    <div class="guide-footer">
      <button class="got-it-btn" onclick={handleClose}>
        <i class="fas fa-check"></i>
        <span>Got It</span>
      </button>
    </div>
  </div>
{/if}

<style>
  /* Backdrop */
  .guide-backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.75);
    backdrop-filter: blur(8px);
    z-index: 10000;
  }

  /* Bottom Sheet - Container for container queries */
  .guide-sheet {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 10001;

    /* Use dynamic viewport height for true adaptability */
    max-height: 95vh;
    max-height: 95dvh;
    display: flex;
    flex-direction: column;
    overflow: hidden;

    /* Enable container queries */
    container-type: size;
    container-name: install-guide;

    /* Glass morphism matching app design */
    background: rgba(26, 26, 46, 0.95);
    backdrop-filter: blur(24px) saturate(180%);
    border-top-left-radius: clamp(16px, 3cqw, 24px);
    border-top-right-radius: clamp(16px, 3cqw, 24px);
    border-top: 1px solid rgba(255, 255, 255, 0.15);
    border-left: 1px solid rgba(255, 255, 255, 0.1);
    border-right: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow:
      0 -8px 32px rgba(0, 0, 0, 0.4),
      0 -2px 8px rgba(0, 0, 0, 0.2),
      0 0 0 1px rgba(255, 255, 255, 0.05) inset;

    padding-bottom: env(safe-area-inset-bottom);
    transform: translateZ(0);
    will-change: transform;
  }

  /* Compact mode - reduce all spacing */
  .guide-sheet.compact {
    max-height: 98vh;
    max-height: 98dvh;
  }

  /* Handle bar for swipe affordance */
  .sheet-handle {
    width: clamp(40px, 12cqw, 48px);
    height: clamp(4px, 1cqh, 5px);
    background: rgba(255, 255, 255, 0.3);
    border-radius: 3px;
    margin: clamp(8px, 2cqh, 12px) auto clamp(6px, 1.5cqh, 8px);
    flex-shrink: 0;
    cursor: grab;
    transition: background 0.2s ease;
  }

  .sheet-handle:hover {
    background: rgba(255, 255, 255, 0.5);
  }

  /* Header - Fluid sizing */
  .guide-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: clamp(12px, 3cqh, 18px) clamp(16px, 5cqw, 24px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  /* Compact mode header */
  .compact .guide-header {
    padding: clamp(10px, 2cqh, 14px) clamp(14px, 4cqw, 20px);
  }

  .header-title {
    display: flex;
    align-items: center;
    gap: clamp(8px, 2cqw, 12px);
  }

  .title-icon {
    font-size: clamp(18px, 4cqw, 22px);
    color: rgba(139, 92, 246, 1);
  }

  .guide-header h2 {
    margin: 0;
    font-size: clamp(16px, 3.5cqw, 19px);
    font-weight: 700;
    color: rgba(255, 255, 255, 0.95);
  }

  .compact .guide-header h2 {
    font-size: clamp(15px, 3cqw, 17px);
  }

  .close-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: clamp(32px, 8cqw, 36px);
    height: clamp(32px, 8cqw, 36px);
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: clamp(6px, 1.5cqw, 8px);
    color: rgba(255, 255, 255, 0.7);
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .close-btn:hover {
    background: rgba(255, 255, 255, 0.12);
    color: rgba(255, 255, 255, 0.95);
  }

  /* Scrollable Content - Fluid spacing */
  .guide-content {
    flex: 1;
    overflow-y: auto;
    padding: clamp(12px, 3cqh, 20px) clamp(16px, 5cqw, 24px);
    min-height: 0;
    overscroll-behavior: contain;
  }

  /* Compact mode content */
  .compact .guide-content {
    padding: clamp(8px, 2cqh, 12px) clamp(12px, 4cqw, 16px);
  }

  /* Section Headings - Fluid sizing */
  .section-heading {
    display: flex;
    align-items: center;
    gap: clamp(8px, 2cqw, 10px);
    margin: 0 0 clamp(10px, 2cqh, 14px) 0;
    font-size: clamp(13px, 3cqw, 15px);
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
  }

  .compact .section-heading {
    font-size: clamp(12px, 2.5cqw, 14px);
    margin-bottom: clamp(8px, 1.5cqh, 10px);
  }

  .section-heading i {
    color: rgba(139, 92, 246, 1);
    font-size: clamp(14px, 3cqw, 16px);
  }

  /* Steps Section */
  .steps-section {
    margin-bottom: clamp(12px, 3cqh, 20px);
  }

  .compact .steps-section {
    margin-bottom: clamp(8px, 2cqh, 12px);
  }

  /* Steps Grid - Uses container queries for responsive columns */
  .steps-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: clamp(8px, 2cqh, 12px);
  }

  @container install-guide (min-width: 600px) {
    .steps-grid {
      grid-template-columns: repeat(2, 1fr);
      gap: clamp(10px, 2cqh, 14px);
    }
  }

  .compact .steps-grid {
    gap: clamp(6px, 1.5cqh, 8px);
  }

  .step-card {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: clamp(8px, 2cqw, 12px);
    padding: clamp(10px, 2.5cqh, 14px);
    transition: all 0.2s ease;
  }

  .compact .step-card {
    padding: clamp(8px, 2cqh, 10px);
  }

  .step-card:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.15);
  }

  .step-header {
    display: flex;
    align-items: flex-start;
    gap: clamp(8px, 2cqw, 12px);
    margin-bottom: clamp(6px, 1.5cqh, 10px);
  }

  .compact .step-header {
    margin-bottom: 0;
  }

  .step-number {
    display: flex;
    align-items: center;
    justify-content: center;
    width: clamp(26px, 6cqw, 30px);
    height: clamp(26px, 6cqw, 30px);
    flex-shrink: 0;
    border-radius: clamp(6px, 1.5cqw, 8px);
    background: linear-gradient(
      135deg,
      rgba(99, 102, 241, 0.3) 0%,
      rgba(139, 92, 246, 0.3) 100%
    );
    border: 1px solid rgba(99, 102, 241, 0.4);
    color: rgba(139, 92, 246, 1);
    font-weight: 700;
    font-size: clamp(13px, 3cqw, 15px);
  }

  .step-text {
    flex: 1;
    margin: 0;
    color: rgba(255, 255, 255, 0.88);
    line-height: 1.5;
    font-size: clamp(12px, 3cqw, 14px);
  }

  .compact .step-text {
    font-size: clamp(11px, 2.5cqw, 13px);
    line-height: 1.4;
  }

  .step-text :global(strong) {
    color: rgba(255, 255, 255, 0.98);
    font-weight: 600;
  }

  /* Step Screenshot Thumbnails - Fluid sizing */
  .step-image-container {
    position: relative;
    margin-top: clamp(6px, 1.5cqh, 8px);
    border-radius: clamp(6px, 1.5cqw, 8px);
    overflow: hidden;
    border: 1px solid rgba(255, 255, 255, 0.12);
    max-width: clamp(150px, 40cqw, 200px);
  }

  .step-image {
    width: 100%;
    height: auto;
    display: block;
  }

  .image-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: clamp(6px, 1.5cqh, 8px);
    padding: clamp(12px, 3cqh, 20px);
    background: rgba(255, 255, 255, 0.03);
    color: rgba(255, 255, 255, 0.3);
    min-height: 80px;
  }

  .image-placeholder i {
    font-size: clamp(18px, 4cqw, 24px);
    opacity: 0.5;
  }

  .placeholder-text {
    font-size: clamp(10px, 2cqw, 11px);
    opacity: 0.6;
    font-style: italic;
  }

  /* Benefits Section - Fluid sizing */
  .benefits-section {
    padding: clamp(10px, 2.5cqh, 16px);
    background: rgba(99, 102, 241, 0.1);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: clamp(8px, 2cqw, 12px);
  }

  .compact .benefits-section {
    padding: clamp(8px, 2cqh, 12px);
  }

  .benefits-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: clamp(6px, 1.5cqh, 10px);
  }

  @container install-guide (min-width: 600px) {
    .benefits-grid {
      grid-template-columns: repeat(2, 1fr);
      gap: clamp(8px, 2cqh, 12px);
    }
  }

  .compact .benefits-grid {
    gap: clamp(5px, 1cqh, 8px);
  }

  .benefit-item {
    display: flex;
    align-items: center;
    gap: clamp(8px, 2cqw, 12px);
    color: rgba(255, 255, 255, 0.88);
    font-size: clamp(11px, 2.5cqw, 13px);
    line-height: 1.5;
  }

  .compact .benefit-item {
    font-size: clamp(10px, 2cqw, 12px);
    line-height: 1.4;
  }

  .benefit-item i {
    color: rgba(139, 92, 246, 1);
    font-size: clamp(13px, 3cqw, 15px);
    flex-shrink: 0;
  }

  /* Sticky Footer - Fluid sizing */
  .guide-footer {
    flex-shrink: 0;
    display: flex;
    justify-content: center;
    padding: clamp(10px, 2.5cqh, 16px) clamp(14px, 4cqw, 20px);
    background: rgba(26, 26, 46, 0.98);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
  }

  .compact .guide-footer {
    padding: clamp(8px, 2cqh, 12px) clamp(12px, 3cqw, 16px);
  }

  .got-it-btn {
    display: flex;
    align-items: center;
    gap: clamp(6px, 1.5cqw, 8px);
    padding: clamp(10px, 2.5cqh, 12px) clamp(20px, 6cqw, 32px);
    background: linear-gradient(
      135deg,
      rgba(99, 102, 241, 0.9) 0%,
      rgba(139, 92, 246, 0.9) 100%
    );
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: clamp(8px, 2cqw, 10px);
    font-size: clamp(13px, 3cqw, 15px);
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
  }

  .compact .got-it-btn {
    padding: clamp(8px, 2cqh, 10px) clamp(16px, 5cqw, 24px);
    font-size: clamp(12px, 2.5cqw, 14px);
  }

  .got-it-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
  }

  .got-it-btn:active {
    transform: translateY(0);
  }
</style>
