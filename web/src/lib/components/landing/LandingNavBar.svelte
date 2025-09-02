<script lang="ts">
  import { getLandingBackground, setLandingBackground } from "$state";
  import SettingsModal from "./SettingsModal.svelte";

  interface Props {
    currentBackground?: "deepOcean" | "snowfall" | "nightSky";
    onBackgroundChange?: (background: string) => void;
  }

  let { currentBackground = "nightSky", onBackgroundChange }: Props = $props();

  let showSettingsModal = $state(false);
  let landingBackground = $derived(getLandingBackground());

  function handleBackgroundChange(background: string) {
    if (
      background === "deepOcean" ||
      background === "snowfall" ||
      background === "nightSky"
    ) {
      setLandingBackground(background);
      onBackgroundChange?.(background);
    }
  }

  function toggleSettingsModal() {
    showSettingsModal = !showSettingsModal;
  }

  function closeSettingsModal() {
    showSettingsModal = false;
  }

  // Streamlined navigation links - Constructor as flagship, About for info
  const navLinks = [
    { href: "/constructor", label: "Constructor", primary: true },
    { href: "/about", label: "About", primary: false },
  ];
</script>

<nav class="landing-navbar">
  <div class="logo-container">
    <h1 class="logo-text">TKA</h1>
    <span class="logo-subtitle">The Kinetic Alphabet</span>
  </div>

  <div class="nav-links">
    {#each navLinks as link}
      <a href={link.href} class="nav-link" class:primary={link.primary}>
        {link.label}
      </a>
    {/each}
  </div>

  <div class="nav-controls">
    <button
      class="settings-toggle"
      onclick={toggleSettingsModal}
      title="Settings"
      aria-label="Open Settings"
    >
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
        <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2" />
        <path
          d="m12 1 2.09.87.87 2.09-2.09.87-.87-2.09L12 1zM12 23l-2.09-.87-.87-2.09 2.09-.87.87 2.09L12 23zM1 12l.87-2.09L3.96 9l.87 2.09L5.7 12l-.87 2.09L3.96 15l-.87-2.09L1 12zM23 12l-.87 2.09L20.04 15l-.87-2.09L18.3 12l.87-2.09L20.04 9l.87 2.09L23 12z"
          stroke="currentColor"
          stroke-width="2"
        />
      </svg>
    </button>
  </div>
</nav>

<!-- Settings Modal -->
{#if showSettingsModal}
  <SettingsModal
    isOpen={showSettingsModal}
    currentBackground={landingBackground}
    onClose={closeSettingsModal}
    onBackgroundChange={handleBackgroundChange}
  />
{/if}

<style>
  .landing-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-lg) var(--spacing-xl);

    /* Enhanced glassmorphism */
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);

    color: var(--text-color, white);
    position: relative;
    z-index: 100;

    /* Enhanced shadows */
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);

    transition: all 0.3s ease;
  }

  .logo-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  .logo-text {
    font-size: 1.8rem;
    font-weight: bold;
    margin: 0;
    color: #667eea;
    font-family: "Arial Black", Arial, sans-serif;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }

  .logo-subtitle {
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.7);
    margin-top: -0.2rem;
  }

  .nav-links {
    display: flex;
    gap: var(--spacing-lg);
    align-items: center;
  }

  .nav-link {
    position: relative;
    color: var(--text-color, white);
    text-decoration: none;
    font-weight: 600;
    font-size: var(--font-size-base);
    padding: var(--spacing-md) var(--spacing-lg);
    border-radius: var(--border-radius-lg);
    overflow: hidden;

    /* Glassmorphism styling */
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow:
      0 4px 16px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);

    transition: all 0.3s ease;
    will-change: transform, background, box-shadow;
  }

  /* Primary link (Constructor) - more prominent styling */
  .nav-link.primary {
    background: linear-gradient(
      135deg,
      rgba(102, 126, 234, 0.2) 0%,
      rgba(118, 75, 162, 0.2) 100%
    );
    border: 1px solid rgba(102, 126, 234, 0.3);
    color: #667eea;
    font-weight: 700;
    box-shadow:
      0 6px 20px rgba(102, 126, 234, 0.15),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }

  .nav-link:hover {
    color: #667eea;
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px) scale(1.02);
    box-shadow:
      0 8px 24px rgba(0, 0, 0, 0.15),
      0 4px 12px rgba(118, 75, 162, 0.2),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
    text-shadow: 0 2px 8px rgba(118, 75, 162, 0.3);
  }

  .nav-link.primary:hover {
    background: linear-gradient(
      135deg,
      rgba(102, 126, 234, 0.3) 0%,
      rgba(118, 75, 162, 0.3) 100%
    );
    border-color: rgba(102, 126, 234, 0.5);
    color: #667eea;
    box-shadow:
      0 10px 30px rgba(102, 126, 234, 0.3),
      0 4px 12px rgba(102, 126, 234, 0.2),
      inset 0 1px 0 rgba(255, 255, 255, 0.4);
  }

  .nav-link:active {
    transform: translateY(-1px);
  }

  .nav-link:focus-visible {
    outline: 2px solid #667eea;
    outline-offset: 2px;
  }

  .nav-controls {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
  }

  .settings-toggle {
    /* Glassmorphism button styling */
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius);
    padding: var(--spacing-sm);
    color: var(--text-color, white);
    cursor: pointer;
    font-size: var(--font-size-lg);
    transition: all 0.3s ease;
    box-shadow:
      0 4px 16px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);

    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
  }

  .settings-toggle:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-1px);
    box-shadow:
      0 6px 20px rgba(0, 0, 0, 0.15),
      0 2px 8px rgba(118, 75, 162, 0.2),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }

  .settings-toggle:active {
    transform: translateY(0);
  }

  .settings-toggle:focus-visible {
    outline: 2px solid #667eea;
    outline-offset: 2px;
  }

  /* Mobile responsive design */
  @media (max-width: 768px) {
    .landing-navbar {
      flex-direction: column;
      gap: var(--spacing-md);
      padding: var(--spacing-md);
    }

    .nav-links {
      gap: var(--spacing-md);
      flex-wrap: wrap;
      justify-content: center;
    }

    .nav-link {
      padding: var(--spacing-sm) var(--spacing-md);
      font-size: var(--font-size-sm);
    }

    .logo-subtitle {
      display: none;
    }

    .nav-controls {
      position: absolute;
      top: var(--spacing-md);
      right: var(--spacing-md);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .landing-navbar,
    .nav-link,
    .settings-toggle {
      transition: none;
    }

    .nav-link:hover,
    .settings-toggle:hover {
      transform: none;
    }
  }

  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .landing-navbar {
      background: rgba(0, 0, 0, 0.9);
      border-bottom: 2px solid white;
    }

    .nav-link {
      border: 1px solid white;
      background: rgba(0, 0, 0, 0.8);
    }

    .nav-link:hover {
      background: #667eea;
      border-color: white;
    }

    .settings-toggle {
      border: 1px solid white;
      background: rgba(0, 0, 0, 0.8);
    }
  }
</style>
