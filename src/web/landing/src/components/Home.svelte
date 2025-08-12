<script>
  import CallToAction from "./CallToAction.svelte";
  import { onMount } from 'svelte';

  let isVisible = false;

  onMount(() => {
    isVisible = true;
  });
</script>

<svelte:head>
  <title>The Kinetic Alphabet - Flow Arts Choreography Toolbox</title>
  <meta name="description" content="The Kinetic Alphabet is a revolutionary flow arts choreography toolbox for poi, staff, fans, and other flow arts. Learn, create, and share movement sequences." />
</svelte:head>

<main class="home-container">
  <!-- Hero Section with Flow Arts Background -->
  <section class="hero" class:visible={isVisible}>
    <div class="hero-content">
      <h1 class="hero-title">The Kinetic Alphabet</h1>
      <p class="hero-subtitle">A Revolutionary Flow Arts Choreography Toolbox</p>
      <p class="hero-description">
        A systematic approach to flow arts that provides structured methods for learning,
        creating, and sharing movement sequences. Supports poi, staff, fans, and other flow arts.
      </p>

      <div class="cta-group">
        <CallToAction
          text="Download Level 1 PDF Book"
          link="https://drive.google.com/file/d/1cgAWbrFiLgUSDEsCB0Mmu2d7Bu5PW45a/view?usp=drive_link"
          primary={true}
        />
        <CallToAction
          text="Get The Kinetic Constructor v0.1.2"
          link="https://github.com/austencloud/tka-sequence-constructor/releases/download/v0.1.2/TKA_Setup.exe"
          primary={false}
        />
      </div>
    </div>
  </section>

  <!-- Features Section -->
  <section class="features">
    <div class="container">
      <h2>The Kinetic Alphabet Features</h2>
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">📚</div>
          <h3>Systematic Learning</h3>
          <p>Complex movements are broken down into understandable components through a structured notation system.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">🎯</div>
          <h3>Precision Training</h3>
          <p>The system supports muscle memory development and technical precision through methodical movement approaches.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">🔧</div>
          <h3>Digital Tools</h3>
          <p>The Kinetic Constructor software enables visualization, creation, and sharing of choreographic sequences.</p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">🌟</div>
          <h3>Creative Framework</h3>
          <p>The system provides foundational knowledge that enables exploration of infinite sequence possibilities.</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Getting Started Section -->
  <section class="getting-started">
    <div class="container">
      <h2>Getting Started</h2>
      <div class="steps-grid">
        <div class="step">
          <div class="step-number">1</div>
          <h3>Download the PDF</h3>
          <p>The comprehensive Level 1 guide introduces core concepts and foundational principles.</p>
        </div>

        <div class="step">
          <div class="step-number">2</div>
          <h3>Practice the Basics</h3>
          <p>Fundamental movements and notation system can be learned through guided exercises.</p>
        </div>

        <div class="step">
          <div class="step-number">3</div>
          <h3>Use the Constructor</h3>
          <p>The digital tool allows creation and visualization of custom sequences.</p>
        </div>

        <div class="step">
          <div class="step-number">4</div>
          <h3>Community Platform</h3>
          <p>Flow artists connect and share creations through the available social platforms.</p>
        </div>
      </div>
    </div>
  </section>
</main>

<style>
  .home-container {
    min-height: 100vh;
  }

  /* Hero Section with Glassmorphism */
  .hero {
    /* Position relative for background positioning */
    position: relative;
    color: var(--text-color);
    padding: var(--spacing-2xl) 0;
    text-align: center;
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.8s ease;
    /* Ensure content is above background */
    z-index: 1;
    /* Optimized height for better space utilization */
    min-height: 55vh;
    display: flex;
    align-items: center;

    /* Glassmorphism styling - no hardcoded background */
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-glass);
    margin: var(--spacing-lg);
  }

  .hero.visible {
    opacity: 1;
    transform: translateY(0);
  }

  /* Background removed - using dynamic backgrounds through glassmorphism */

  /* Reduced motion support for accessibility */
  @media (prefers-reduced-motion: reduce) {
    .hero {
      /* Simplify hero transitions for reduced motion */
      transition: opacity 0.3s ease;
    }
  }

  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .hero-content {
      /* Increase text shadow for better readability in high contrast mode */
      text-shadow: 0 3px 6px rgba(0, 0, 0, 0.8);
    }

    .feature-card {
      /* Stronger border for high contrast mode */
      border: 2px solid var(--text-color);
    }
  }

  .hero-content {
    /* Relative positioning to stay above background */
    position: relative;
    max-width: 800px;
    margin: 0 auto;
    padding: 0 var(--container-padding);
    /* Ensure content is readable with text shadow for accessibility */
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    z-index: 2;
  }

  /* Ultra-wide hero optimization */
  @media (min-width: 1600px) {
    .hero-content {
      max-width: 1000px;
    }
  }

  .hero-title {
    font-size: var(--font-size-4xl);
    margin-bottom: var(--spacing-md);
    font-weight: 900;
  }

  .hero-subtitle {
    font-size: var(--font-size-xl);
    margin-bottom: var(--spacing-lg);
    opacity: 0.9;
    font-weight: 300;
  }

  .hero-description {
    font-size: var(--font-size-lg);
    margin-bottom: var(--spacing-2xl);
    opacity: 0.8;
    line-height: 1.6;
  }

  .cta-group {
    display: flex;
    gap: var(--spacing-md);
    justify-content: center;
    flex-wrap: wrap;
  }

  /* Features Section with Dark Mode Support */
  .features {
    padding: var(--spacing-3xl) 0;
    background: var(--surface-color);
  }

  .features h2 {
    text-align: center;
    margin-bottom: var(--spacing-2xl);
    color: var(--text-color);
  }

  /*
   * Features Grid Layout - 2x2 Grid System
   *
   * Design Decision: Using CSS Grid for precise control over layout
   * - Desktop: 2 columns x 2 rows (4 cards total)
   * - Tablet: 2 columns x 2 rows (maintained for consistency)
   * - Mobile: 1 column x 4 rows (stacked vertically)
   *
   * Benefits:
   * - Equal card heights automatically
   * - Better visual balance than auto-fit
   * - Consistent spacing and alignment
   * - Responsive without complex media queries
   */
  .features-grid {
    display: grid;
    /* Fixed 2-column layout for desktop/tablet */
    grid-template-columns: 1fr 1fr;
    /* Fixed 2-row layout ensures 2x2 grid */
    grid-template-rows: 1fr 1fr;
    gap: var(--spacing-xl);
    margin-top: var(--spacing-2xl);
    /* Ensure equal heights across all cards */
    align-items: stretch;
  }

  /*
   * Feature Card Styling with Dark Mode Compatibility
   *
   * Dark Mode Implementation:
   * - Uses CSS custom properties for automatic theme switching
   * - Maintains proper contrast ratios (WCAG AA compliant)
   * - Smooth transitions between light/dark modes
   */
  .feature-card {
    position: relative;
    /* Advanced 2025 glassmorphism */
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    padding: var(--spacing-xl);
    border-radius: var(--border-radius-lg);
    text-align: center;

    /* Enhanced glassmorphism styling */
    border: var(--glass-border);
    box-shadow: var(--shadow-glass);

    /* Layout and transitions */
    display: flex;
    flex-direction: column;
    justify-content: center;
    overflow: hidden;
    transition: all var(--transition-normal);
    will-change: transform, box-shadow, background;

    /* Enhanced entrance animation */
    opacity: 0;
    transform: translateY(30px);
    animation: cardSlideIn 0.8s ease-out forwards;
  }

  /* Staggered entrance animations for cards */
  .feature-card:nth-child(1) { animation-delay: 0.1s; }
  .feature-card:nth-child(2) { animation-delay: 0.2s; }
  .feature-card:nth-child(3) { animation-delay: 0.3s; }
  .feature-card:nth-child(4) { animation-delay: 0.4s; }

  @keyframes cardSlideIn {
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .feature-card:hover {
    transform: translateY(-10px) scale(1.03);
    background: var(--surface-hover);
    border: var(--glass-border-hover);
    box-shadow: var(--shadow-glass-hover);
  }

  .feature-card:active {
    transform: translateY(-6px) scale(1.02);
    background: var(--surface-active);
  }

  /* Advanced cosmic glassmorphism overlay */
  .feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--gradient-cosmic);
    opacity: 0;
    transition: opacity var(--transition-normal);
    pointer-events: none;
    border-radius: var(--border-radius-lg);
  }

  .feature-card:hover::before {
    opacity: 0.05;
  }

  /* Floating animation for enhanced interactivity */
  .feature-card:hover .feature-icon {
    animation: var(--animation-float);
  }

  .feature-icon {
    font-size: 3rem;
    margin-bottom: var(--spacing-md);
    position: relative;
    z-index: 1;
    display: inline-block;

    /* Enhanced cosmic icon styling */
    background: var(--gradient-primary);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    filter: drop-shadow(0 2px 4px var(--shadow-colored));

    /* Smooth transitions */
    transition: all var(--transition-normal);
  }

  .feature-card:hover .feature-icon {
    transform: scale(1.15) rotate(8deg);
    filter: drop-shadow(0 4px 8px rgba(118, 75, 162, 0.5));
  }

  .feature-card h3 {
    color: var(--text-color);
    margin-bottom: var(--spacing-md);
    position: relative;
    z-index: 1;
    font-weight: 700;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: all var(--transition-normal);
  }

  .feature-card:hover h3 {
    color: var(--primary-light);
    text-shadow: 0 2px 8px var(--shadow-colored);
    transform: translateY(-2px);
  }

  .feature-card p {
    color: var(--text-secondary);
    line-height: 1.6;
    position: relative;
    z-index: 1;
  }

  /* Getting Started Section */
  .getting-started {
    padding: var(--spacing-3xl) 0;
    background: var(--background-color);
  }

  .getting-started h2 {
    text-align: center;
    margin-bottom: var(--spacing-2xl);
    color: var(--text-color);
  }

  .steps-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--spacing-xl);
    margin-top: var(--spacing-2xl);
  }

  .step {
    text-align: center;
    padding: var(--spacing-lg);
  }

  .step-number {
    width: 60px;
    height: 60px;
    background: var(--primary-color);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: var(--font-size-xl);
    font-weight: bold;
    margin: 0 auto var(--spacing-md) auto;
  }

  .step h3 {
    color: var(--primary-color);
    margin-bottom: var(--spacing-md);
  }

  .step p {
    color: var(--text-secondary);
    line-height: 1.6;
  }

  /* Reduced motion support for accessibility */
  @media (prefers-reduced-motion: reduce) {
    .feature-card {
      animation: none;
      opacity: 1;
      transform: none;
    }

    .feature-card:hover {
      transform: none;
    }

    .feature-card:hover .feature-icon {
      transform: none;
    }

    .feature-card::before {
      transition: none;
    }

    .feature-icon {
      transition: none;
    }

    .feature-card h3 {
      transition: none;
    }
  }

  /* High contrast mode support */
  @media (prefers-contrast: high) {
    .feature-card {
      border: 2px solid var(--text-color);
      background: var(--surface-color);
    }

    .feature-card:hover {
      border-color: var(--primary-color);
    }
  }

  /*
   * Responsive Design Implementation
   *
   * Breakpoint Strategy:
   * - 768px and below: Mobile-first approach
   * - Above 768px: Tablet and desktop layouts
   *
   * Key Responsive Features:
   * - Hero section adapts height and text sizes
   * - Feature cards stack vertically on mobile (1 column)
   * - Maintain 2x2 grid on tablet and desktop
   * - Optimized spacing for touch interfaces
   */

  /* Mobile Optimization - 768px and below */
  @media (max-width: 768px) {
    /* Hero Section Mobile Adjustments */
    .hero {
      padding: var(--spacing-2xl) 0;
      /* Reduce minimum height for mobile screens */
      min-height: 60vh;
    }

    /* Background removed - using dynamic backgrounds */

    /* Typography scaling for mobile readability */
    .hero-title {
      font-size: var(--font-size-3xl);
    }

    .hero-subtitle {
      font-size: var(--font-size-lg);
    }

    .hero-description {
      font-size: var(--font-size-base);
    }

    /* CTA buttons stack vertically on mobile */
    .cta-group {
      flex-direction: column;
      align-items: center;
    }

    /* Section padding optimization for mobile */
    .features,
    .getting-started {
      padding: var(--spacing-2xl) 0;
    }

    /*
     * Mobile Grid Layout - Single Column
     *
     * Features grid changes from 2x2 to 1x4 (single column)
     * This ensures optimal readability and touch interaction
     * on mobile devices while maintaining card consistency
     */
    .features-grid {
      /* Single column layout for mobile */
      grid-template-columns: 1fr;
      /* Auto rows to accommodate 4 cards vertically */
      grid-template-rows: repeat(4, auto);
      /* Reduced gap for mobile to save space */
      gap: var(--spacing-lg);
    }

    /* Steps grid also becomes single column */
    .steps-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-lg);
    }

    /* Feature cards mobile optimization */
    .feature-card {
      /* Slightly reduced padding for mobile */
      padding: var(--spacing-lg);
    }
  }

  /*
   * Desktop Optimization - 1200px and above
   *
   * Enhanced spacing and layout for large screens
   */
  @media (min-width: 1200px) {
    .features-grid {
      gap: var(--spacing-2xl);
      max-width: var(--container-max-width-wide);
      margin: var(--spacing-2xl) auto 0;
    }

    .features,
    .getting-started {
      padding: var(--spacing-3xl) var(--container-padding);
    }
  }

  /*
   * Ultra-wide Optimization - 1600px and above
   */
  @media (min-width: 1600px) {
    .features-grid {
      gap: var(--spacing-3xl);
      max-width: var(--container-max-width-ultra);
    }
  }

  /*
   * Tablet Optimization - 769px to 1199px
   *
   * Maintains 2x2 grid but with adjusted spacing
   * for optimal tablet viewing experience
   */
  @media (min-width: 769px) and (max-width: 1199px) {
    .features-grid {
      /* Maintain 2x2 grid on tablets */
      grid-template-columns: 1fr 1fr;
      grid-template-rows: 1fr 1fr;
      /* Slightly reduced gap for tablet screens */
      gap: var(--spacing-lg);
    }
  }
</style>
