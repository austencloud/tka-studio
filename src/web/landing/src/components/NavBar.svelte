<script lang="ts">
  import SettingsModal from '$lib/core/shared/components/SettingsModal.svelte';

  interface Props {
    currentBackground?: string;
    onBackgroundChange?: (background: string) => void;
  }

  let { currentBackground = 'deepOcean', onBackgroundChange }: Props = $props();

  let showSettingsModal = $state(false);

  function handleBackgroundChange(background: string) {
    onBackgroundChange?.(background);
  }

  function toggleSettingsModal() {
    showSettingsModal = !showSettingsModal;
  }

  function closeSettingsModal() {
    showSettingsModal = false;
  }
</script>

<nav class="navbar">
  <div class="logo-container">
    <h1 class="logo-text">TKA</h1>
    <span class="logo-subtitle">The Kinetic Alphabet</span>
  </div>
  <div class="nav-links">
    <a href="/">Home</a>
    <a href="/about">About</a>
    <a href="/constructor">Constructor</a>
    <a href="/animator">Animator</a>
    <a href="/links">Links</a>
    <a href="/contact">Contact</a>
  </div>
  <div class="nav-controls">
    <button class="settings-toggle" onclick={toggleSettingsModal} title="Settings">
      ⚙️
    </button>
  </div>
</nav>

<!-- Settings Modal -->
<SettingsModal
  isOpen={showSettingsModal}
  {currentBackground}
  onClose={closeSettingsModal}
  onBackgroundChange={handleBackgroundChange}
/>

<style>
  /*
   * Enhanced Navigation Bar with Glassmorphism
   *
   * Features:
   * - Glassmorphism effects with backdrop-blur
   * - Smooth micro-interactions and hover effects
   * - Enhanced typography and spacing
   * - Accessibility-compliant design
   * - Mobile-first responsive behavior
   */

  .navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: var(--spacing-lg) var(--spacing-xl);

    /* Advanced 2025 glassmorphism */
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop-strong);
    -webkit-backdrop-filter: var(--glass-backdrop-strong);
    border-bottom: var(--glass-border);

    color: var(--text-color);
    position: relative;

    /* Enhanced glassmorphism shadows */
    box-shadow: var(--shadow-glass);

    /* Smooth transitions */
    transition: all var(--transition-normal);
  }

  .nav-controls {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
  }

  .settings-toggle {
    /* Glassmorphism button styling */
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: var(--border-radius);
    padding: var(--spacing-sm);
    color: var(--text-color);
    cursor: pointer;
    font-size: var(--font-size-lg);
    transition: all var(--transition-normal);
    box-shadow: var(--shadow-glass);
  }

  .settings-toggle:hover {
    background: var(--surface-hover);
    transform: translateY(-1px);
    box-shadow: var(--shadow-glass-hover);
  }

  /* Settings modal styles are in SettingsModal.svelte */

  .logo-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  .logo-text {
    font-size: 1.8rem;
    font-weight: bold;
    margin: 0;
    color: var(--primary-color);
    font-family: 'Archivo Black', Arial, sans-serif;
  }

  .logo-subtitle {
    font-size: 0.8rem;
    color: #ccc;
    margin-top: -0.2rem;
  }

  .nav-links {
    display: flex;
    gap: var(--spacing-lg);
    align-items: center;
  }

  .nav-links a {
    position: relative;
    color: var(--text-color);
    text-decoration: none;
    font-weight: 600;
    font-size: var(--font-size-base);
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--border-radius-lg);
    overflow: hidden;

    /* Advanced glassmorphism styling */
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    box-shadow: var(--shadow-glass);

    /* Enhanced transitions */
    transition: all var(--transition-normal);
    will-change: transform, background, box-shadow;
  }

  .nav-links a:hover {
    color: var(--primary-light);
    background: var(--surface-hover);
    border: var(--glass-border-hover);
    transform: translateY(-2px) scale(1.02);
    box-shadow: var(--shadow-glass-hover);
    text-shadow: 0 2px 8px var(--shadow-colored);
  }

  .nav-links a:active {
    transform: translateY(-1px);
  }

  .nav-links a:focus-visible {
    outline: 2px solid var(--primary-color);
    outline-offset: 2px;
  }

  /* Reduced motion support for accessibility */
  @media (prefers-reduced-motion: reduce) {
    .navbar,
    .nav-links a {
      transition: none;
      animation: none;
    }

    .nav-links a:hover {
      transform: none;
    }
  }

  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .navbar {
      background: rgba(0, 0, 0, 0.9);
      border-bottom: 2px solid white;
    }

    .nav-links a {
      border: 1px solid white;
      background: rgba(0, 0, 0, 0.8);
    }

    .nav-links a:hover {
      background: var(--primary-color);
      border-color: white;
    }
  }

  /* Mobile responsive design */
  @media (max-width: 768px) {
    .navbar {
      flex-direction: column;
      gap: var(--spacing-md);
      padding: var(--spacing-md);
    }

    .nav-links {
      gap: var(--spacing-sm);
      flex-wrap: wrap;
      justify-content: center;
    }

    .nav-links a {
      padding: var(--spacing-xs) var(--spacing-sm);
      font-size: var(--font-size-sm);
    }

    .logo-subtitle {
      display: none;
    }
  }
</style>
