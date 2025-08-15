<script lang="ts">
  import HeroSection from "./HeroSection.svelte";
  import QuickAccess from "./QuickAccess.svelte";
  import ProjectOverview from "./ProjectOverview.svelte";
  import Features from "./Features.svelte";
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
  <nav class="quick-nav" aria-label="About page navigation">
    <div class="nav-content">
      <span class="nav-title">Quick Navigation:</span>
      <div class="nav-links">
        <button onclick={() => scrollToSection("hero")} class="nav-link"
          >Philosophy</button
        >
        <button onclick={() => scrollToSection("quick-access")} class="nav-link"
          >Quick Access</button
        >
        <button onclick={() => scrollToSection("overview")} class="nav-link"
          >Overview</button
        >
        <button onclick={() => scrollToSection("features")} class="nav-link"
          >Features</button
        >
        <button
          onclick={() => scrollToSection("getting-started")}
          class="nav-link">Getting Started</button
        >
        <button onclick={() => scrollToSection("resources")} class="nav-link"
          >Resources</button
        >
        <button onclick={() => scrollToSection("contact")} class="nav-link"
          >Contact</button
        >
      </div>
    </div>
  </nav>

  <!-- Hero Section -->
  <section id="hero" class="section-container">
    <HeroSection />
  </section>

  <!-- Quick Access -->
  <section id="quick-access" class="section-container">
    <QuickAccess />
  </section>

  <!-- Project Overview -->
  <section id="overview" class="section-container">
    <ProjectOverview />
  </section>

  <!-- Features -->
  <section id="features" class="section-container">
    <Features />
  </section>

  <!-- Getting Started -->
  <section id="getting-started" class="section-container">
    <GettingStarted />
  </section>

  <!-- Resources & Links -->
  <section id="resources" class="section-container">
    <ResourcesHistorian />
  </section>

  <!-- Contact -->
  <section id="contact" class="section-container">
    <ContactSection />
  </section>
</div>

<style>
  /* About Container */
  .about-container {
    min-height: 100vh;
    background: var(--cosmic-gradient);
    color: var(--text-color);
    position: relative;
  }

  /* Quick Navigation */
  .quick-nav {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding: var(--spacing-sm) 0;
  }

  .nav-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
    display: flex;
    align-items: center;
    gap: var(--spacing-lg);
    flex-wrap: wrap;
  }

  .nav-title {
    font-weight: 600;
    color: var(--text-secondary);
    font-size: var(--font-size-sm);
    white-space: nowrap;
  }

  .nav-links {
    display: flex;
    gap: var(--spacing-sm);
    flex-wrap: wrap;
    flex: 1;
  }

  .nav-link {
    padding: var(--spacing-xs) var(--spacing-sm);
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-sm);
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

  /* Section Separators */
  .section-container:not(:last-child)::after {
    content: "";
    display: block;
    width: 100px;
    height: 2px;
    background: linear-gradient(
      90deg,
      transparent 0%,
      var(--primary-color) 50%,
      transparent 100%
    );
    margin: var(--spacing-2xl) auto;
  }

  /* Mobile Responsive */
  @media (max-width: 768px) {
    .nav-content {
      padding: 0 var(--spacing-md);
      flex-direction: column;
      align-items: flex-start;
      gap: var(--spacing-sm);
    }

    .nav-title {
      font-size: var(--font-size-xs);
    }

    .nav-links {
      justify-content: center;
      width: 100%;
    }

    .nav-link {
      padding: var(--spacing-xs);
      font-size: var(--font-size-xs);
      flex: 1;
      min-width: 80px;
      text-align: center;
    }

    .section-container {
      scroll-margin-top: 120px; /* More space for mobile nav */
    }
  }

  @media (max-width: 480px) {
    .nav-links {
      grid-template-columns: repeat(auto-fit, minmax(70px, 1fr));
      display: grid;
      gap: var(--spacing-xs);
    }

    .nav-link {
      min-width: 0;
      padding: var(--spacing-xs);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .nav-link {
      transition: none;
    }
  }

  /* Focus management for accessibility */
  .about-container:focus-within .nav-link:focus {
    z-index: 1;
  }

  /* Print styles */
  @media print {
    .quick-nav {
      display: none;
    }

    .section-container::after {
      display: none;
    }
  }
</style>
