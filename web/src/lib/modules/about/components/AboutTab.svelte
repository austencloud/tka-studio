<script lang="ts">
  import HeroSection from "./HeroSection.svelte";
  import QuickAccess from "./QuickAccess.svelte";
  import AboutTheSystem from "./AboutTheSystem.svelte";
  import GettingStarted from "./GettingStarted.svelte";
  import ResourcesHistorian from "./ResourcesHistorian.svelte";
  import ContactSection from "./ContactSection.svelte";

  // Smooth scrolling utility for section navigation
  function scrollToSection(sectionId: string) {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }
</script>

<!-- About Tab - Modular Architecture -->
<div class="about-container">
  <!-- Quick Navigation -->
  <nav class="page-nav" aria-label="About page sections">
    <div class="nav-content">
      <div class="nav-links">
        <button onclick={() => scrollToSection("hero")} class="nav-link"
          >About</button
        >
        <button onclick={() => scrollToSection("quick-access")} class="nav-link"
          >Get Started</button
        >
        <button onclick={() => scrollToSection("system")} class="nav-link"
          >How It Works</button
        >
        <button onclick={() => scrollToSection("contact")} class="nav-link"
          >Contact</button
        >
      </div>
    </div>
  </nav>

  <!-- Hero Section -->
  <section id="hero" class="section-container hero-section">
    <HeroSection />
  </section>

  <!-- Action Section -->
  <div class="section-group action-group">
    <section id="quick-access" class="section-container">
      <QuickAccess />
    </section>
  </div>

  <!-- Support Section -->
  <div class="section-group support-group">
    <section id="contact" class="section-container">
      <ContactSection />
    </section>
  </div>
</div>

<style>
  /* About Container */
  .about-container {
    min-height: 100vh;
    min-width: 100vw;
    background: var(--cosmic-gradient);
    color: var(--text-color);
    position: relative;
  }

  /* Page Navigation */
  .page-nav {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding: var(--spacing-sm) 0;
  }

  .nav-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
    display: flex;
    justify-content: center;
  }

  .nav-links {
    display: flex;
    gap: var(--spacing-md);
    flex-wrap: wrap;
    justify-content: center;
  }

  .nav-link {
    padding: var(--spacing-sm) var(--spacing-lg);
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: var(--border-radius-md);
    color: var(--text-secondary);
    font-family: inherit;
    font-size: var(--font-size-sm);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
    white-space: nowrap;
  }

  .nav-link:hover {
    background: rgba(255, 255, 255, 0.1);
    color: var(--text-color);
    border-color: var(--primary-color);
  }

  .nav-link:focus {
    outline: 2px solid var(--primary-color);
    outline-offset: 2px;
  }

  /* Section Containers */
  .section-container {
    scroll-margin-top: 80px; /* Account for sticky nav */
  }

  /* Section Groups */
  .section-group {
    position: relative;
    margin: var(--spacing-xl) 0;
  }

  .hero-section {
    margin-bottom: var(--spacing-lg);
  }

  .action-group {
    background: rgba(255, 255, 255, 0.02);
    border-radius: 1.5rem;
    padding: var(--spacing-lg);
    margin: var(--spacing-xl) auto;
    max-width: 1200px;
  }

  .support-group {
    background: rgba(255, 255, 255, 0.02);
    border-radius: 1.5rem;
    padding: var(--spacing-lg);
    margin: var(--spacing-xl) auto;
    max-width: 1200px;
  }

  /* Group Separators */
  .section-group:not(:last-child)::after {
    content: "";
    display: block;
    width: 150px;
    height: 1px;
    background: linear-gradient(
      90deg,
      transparent 0%,
      var(--primary-color) 50%,
      transparent 100%
    );
    margin: var(--spacing-lg) auto 0;
  }

  /* Mobile Responsive */
  @media (max-width: 768px) {
    .nav-content {
      padding: 0 var(--spacing-md);
    }

    .nav-links {
      gap: var(--spacing-sm);
      width: 100%;
      justify-content: space-between;
    }

    .nav-link {
      padding: var(--spacing-sm);
      font-size: var(--font-size-sm);
      flex: 1;
      text-align: center;
      min-width: 0;
    }

    .section-container {
      scroll-margin-top: 80px;
    }

    .section-group {
      margin: var(--spacing-lg) var(--spacing-md);
      padding: var(--spacing-md);
    }

    .hero-section {
      margin-bottom: var(--spacing-md);
    }
  }

  @media (max-width: 480px) {
    .nav-links {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: var(--spacing-xs);
    }

    .nav-link {
      padding: var(--spacing-xs);
      font-size: var(--font-size-xs);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .nav-link {
      transition: none;
    }
  }
</style>
