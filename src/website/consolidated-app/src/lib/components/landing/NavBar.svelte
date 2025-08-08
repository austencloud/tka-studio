<script lang="ts">
  import { ThemeToggle } from '../ui';

  interface Props {
    currentPage?: string;
  }

  let { currentPage = 'home' }: Props = $props();

  let mobileMenuOpen = $state(false);

  function toggleMobileMenu() {
    mobileMenuOpen = !mobileMenuOpen;
  }

  function closeMobileMenu() {
    mobileMenuOpen = false;
  }
</script>

<nav class="navbar">
  <div class="logo-container">
    <a href="/" class="logo-link">
      <h1 class="logo-text">TKA</h1>
      <span class="logo-subtitle">The Kinetic Alphabet</span>
    </a>
  </div>

  <!-- Mobile menu button -->
  <button
    class="mobile-menu-toggle"
    class:active={mobileMenuOpen}
    onclick={toggleMobileMenu}
    aria-label="Toggle navigation menu"
    aria-expanded={mobileMenuOpen}
  >
    <span></span>
    <span></span>
    <span></span>
  </button>

  <!-- Navigation links -->
  <div class="nav-links" class:mobile-open={mobileMenuOpen}>
    <a href="/" class:active={currentPage === 'home'} onclick={closeMobileMenu}>Home</a>
    <a href="/app" class:active={currentPage === 'app'} onclick={closeMobileMenu}>Constructor</a>
    <a href="/animator" class:active={currentPage === 'animator'} onclick={closeMobileMenu}>Animator</a>
    <a href="/about" class:active={currentPage === 'about'} onclick={closeMobileMenu}>About</a>
  </div>

  <div class="nav-controls">
    <ThemeToggle />
  </div>
</nav>

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

  .logo-container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }

  .logo-link {
    text-decoration: none;
    color: inherit;
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
    color: var(--text-secondary);
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

  .nav-links a.active {
    color: var(--primary-light);
    background: var(--surface-active);
    border: var(--glass-border-active);
    box-shadow: var(--shadow-glass-active);
  }

  .nav-links a:active {
    transform: translateY(-1px);
  }

  .nav-links a:focus-visible {
    outline: 2px solid var(--primary-color);
    outline-offset: 2px;
  }

  .nav-controls {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
  }

  /* Mobile menu toggle button */
  .mobile-menu-toggle {
    display: none;
    flex-direction: column;
    justify-content: space-between;
    width: 30px;
    height: 21px;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0;
    z-index: 10;
  }

  .mobile-menu-toggle span {
    width: 100%;
    height: 3px;
    background: var(--text-color);
    border-radius: 3px;
    transition: all var(--transition-fast);
    transform-origin: center;
  }

  .mobile-menu-toggle.active span:nth-child(1) {
    transform: translateY(9px) rotate(45deg);
  }

  .mobile-menu-toggle.active span:nth-child(2) {
    opacity: 0;
  }

  .mobile-menu-toggle.active span:nth-child(3) {
    transform: translateY(-9px) rotate(-45deg);
  }

  /* Reduced motion support for accessibility */
  @media (prefers-reduced-motion: reduce) {
    .navbar,
    .nav-links a,
    .mobile-menu-toggle span {
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
      position: relative;
    }

    .mobile-menu-toggle {
      display: flex;
    }

    .nav-links {
      position: absolute;
      top: 100%;
      left: 0;
      right: 0;
      flex-direction: column;
      background: var(--surface-color);
      backdrop-filter: var(--glass-backdrop-strong);
      -webkit-backdrop-filter: var(--glass-backdrop-strong);
      border: var(--glass-border);
      border-top: none;
      padding: var(--spacing-lg);
      gap: var(--spacing-md);
      transform: translateY(-100%);
      opacity: 0;
      pointer-events: none;
      transition: all var(--transition-normal);
      z-index: 9;
    }

    .nav-links.mobile-open {
      transform: translateY(0);
      opacity: 1;
      pointer-events: auto;
    }

    .nav-links a {
      padding: var(--spacing-md);
      text-align: center;
      font-size: var(--font-size-lg);
    }

    .logo-subtitle {
      display: none;
    }

    .nav-controls {
      position: absolute;
      right: 80px;
      top: 50%;
      transform: translateY(-50%);
    }
  }
</style>
