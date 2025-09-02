<script lang="ts">
  import { enterAppMode, switchTab } from "$state";
  import { onMount } from "svelte";
  import CallToAction from "./CallToAction.svelte";

  let isVisible = $state(false);

  onMount(() => {
    isVisible = true;
  });

  // Enhanced constructor button - enters app mode
  async function handleConstructorClick() {
    console.log("🔧 Entering constructor mode...");
    await enterAppMode();
    // Switch to construct tab after entering app mode
    switchTab("construct");
  }

  // External links for downloads
  const pdfBookLink =
    "https://drive.google.com/file/d/1cgAWbrFiLgUSDEsCB0Mmu2d7Bu5PW45a/view?usp=drive_link";
  const desktopAppLink =
    "https://github.com/austencloud/tka-sequence-constructor/releases/download/v0.1.2/TKA_Setup.exe";
</script>

<svelte:head>
  <title>The Kinetic Alphabet - Flow Arts Choreography Toolbox</title>
  <meta
    name="description"
    content="The Kinetic Alphabet is a revolutionary flow arts choreography toolbox for poi, staff, fans, and other flow arts. Learn, create, and share movement sequences."
  />
</svelte:head>

<main class="home-container">
  <!-- Hero Section with Flow Arts Background -->
  <section class="hero" class:visible={isVisible}>
    <div class="hero-content">
      <h1 class="hero-title">The Kinetic Alphabet</h1>
      <p class="hero-subtitle">
        A Revolutionary Flow Arts Choreography Toolbox
      </p>
      <p class="hero-description">
        A systematic approach to flow arts that provides structured methods for
        learning, creating, and sharing movement sequences. Supports poi, staff,
        fans, and other flow arts.
      </p>

      <div class="cta-group">
        <CallToAction
          text="Enter The Constructor"
          onclick={handleConstructorClick}
          primary={true}
          internal={true}
        />
        <CallToAction
          text="Download Level 1 PDF Book"
          link={pdfBookLink}
          primary={false}
          internal={false}
        />
        <CallToAction
          text="Get Desktop App v0.1.2"
          link={desktopAppLink}
          primary={false}
          internal={false}
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
          <p>
            Complex movements are broken down into understandable components
            through a structured notation system.
          </p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">🎯</div>
          <h3>Precision Training</h3>
          <p>
            The system supports muscle memory development and technical
            precision through methodical movement approaches.
          </p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">🔧</div>
          <h3>Digital Tools</h3>
          <p>
            The Kinetic Constructor enables visualization, creation, and sharing
            of choreographic sequences.
          </p>
        </div>

        <div class="feature-card">
          <div class="feature-icon">🌟</div>
          <h3>Creative Framework</h3>
          <p>
            The system provides foundational knowledge that enables exploration
            of infinite sequence possibilities.
          </p>
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
          <p>
            The comprehensive Level 1 guide introduces core concepts and
            foundational principles.
          </p>
        </div>

        <div class="step">
          <div class="step-number">2</div>
          <h3>Practice the Basics</h3>
          <p>
            Fundamental movements and notation system can be learned through
            guided exercises.
          </p>
        </div>

        <div class="step">
          <div class="step-number">3</div>
          <h3>Use the Constructor</h3>
          <p>
            The web-based constructor allows creation and visualization of
            custom sequences.
          </p>
        </div>

        <div class="step">
          <div class="step-number">4</div>
          <h3>Join the Community</h3>
          <p>
            Connect with flow artists and share creations through our growing
            community platform.
          </p>
        </div>
      </div>
    </div>
  </section>
</main>

<style>
  .home-container {
    min-height: 100vh;
    padding: 0;
  }

  /* Hero Section with Glassmorphism */
  .hero {
    position: relative;
    color: var(--text-color);
    padding: var(--spacing-2xl) 0;
    text-align: center;
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.8s ease;
    z-index: 1;
    min-height: 60vh;
    display: flex;
    align-items: center;

    /* Enhanced glassmorphism styling */
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 2rem;
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    margin: var(--spacing-lg);
  }

  .hero.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .hero-content {
    position: relative;
    max-width: 900px;
    margin: 0 auto;
    padding: 0 var(--spacing-xl);
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    z-index: 2;
  }

  .hero-title {
    font-size: 3.5rem;
    margin-bottom: var(--spacing-md);
    font-weight: 900;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .hero-subtitle {
    font-size: 1.5rem;
    margin-bottom: var(--spacing-lg);
    opacity: 0.9;
    font-weight: 300;
    color: var(--text-color);
  }

  .hero-description {
    font-size: 1.125rem;
    margin-bottom: var(--spacing-2xl);
    opacity: 0.8;
    line-height: 1.6;
    max-width: 700px;
    margin-left: auto;
    margin-right: auto;
  }

  .cta-group {
    display: flex;
    gap: var(--spacing-md);
    justify-content: center;
    flex-wrap: wrap;
  }

  /* Features Section */
  .features {
    padding: var(--spacing-3xl) 0;
    background: transparent;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
  }

  .features h2 {
    text-align: center;
    margin-bottom: var(--spacing-2xl);
    color: var(--text-color);
    font-size: 2.5rem;
    font-weight: 700;
  }

  .features-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 1fr 1fr;
    gap: var(--spacing-xl);
    margin-top: var(--spacing-2xl);
    align-items: stretch;
  }

  .feature-card {
    position: relative;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    padding: var(--spacing-xl);
    border-radius: 1.5rem;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    display: flex;
    flex-direction: column;
    justify-content: center;
    overflow: hidden;
    transition: all 0.3s ease;
    opacity: 0;
    transform: translateY(30px);
    animation: cardSlideIn 0.8s ease-out forwards;
  }

  .feature-card:nth-child(1) {
    animation-delay: 0.1s;
  }
  .feature-card:nth-child(2) {
    animation-delay: 0.2s;
  }
  .feature-card:nth-child(3) {
    animation-delay: 0.3s;
  }
  .feature-card:nth-child(4) {
    animation-delay: 0.4s;
  }

  @keyframes cardSlideIn {
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .feature-card:hover {
    transform: translateY(-10px) scale(1.02);
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
    box-shadow:
      0 20px 40px rgba(118, 75, 162, 0.2),
      0 8px 20px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.3);
  }

  .feature-icon {
    font-size: 3rem;
    margin-bottom: var(--spacing-md);
    display: inline-block;
    transition: all 0.3s ease;
  }

  .feature-card:hover .feature-icon {
    transform: scale(1.1) rotate(5deg);
  }

  .feature-card h3 {
    color: var(--text-color);
    margin-bottom: var(--spacing-md);
    font-weight: 700;
    font-size: 1.25rem;
  }

  .feature-card p {
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.6;
  }

  /* Getting Started Section */
  .getting-started {
    padding: var(--spacing-3xl) 0;
    background: transparent;
  }

  .getting-started h2 {
    text-align: center;
    margin-bottom: var(--spacing-2xl);
    color: var(--text-color);
    font-size: 2.5rem;
    font-weight: 700;
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
    background: rgba(255, 255, 255, 0.03);
    border-radius: 1rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .step-number {
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0 auto var(--spacing-md) auto;
  }

  .step h3 {
    color: var(--text-color);
    margin-bottom: var(--spacing-md);
    font-weight: 600;
  }

  .step p {
    color: rgba(255, 255, 255, 0.8);
    line-height: 1.6;
  }

  /* Mobile responsive design */
  @media (max-width: 768px) {
    .hero {
      padding: var(--spacing-xl) 0;
      min-height: 50vh;
      margin: var(--spacing-md);
    }

    .hero-title {
      font-size: 2.5rem;
    }

    .hero-subtitle {
      font-size: 1.25rem;
    }

    .hero-description {
      font-size: 1rem;
    }

    .cta-group {
      flex-direction: column;
      align-items: center;
      gap: var(--spacing-sm);
    }

    .features,
    .getting-started {
      padding: var(--spacing-2xl) 0;
    }

    .features-grid {
      grid-template-columns: 1fr;
      grid-template-rows: repeat(4, auto);
      gap: var(--spacing-lg);
    }

    .steps-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-lg);
    }

    .container {
      padding: 0 var(--spacing-md);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .feature-card {
      animation: none;
      opacity: 1;
      transform: none;
    }

    .hero {
      transition: none;
      opacity: 1;
      transform: none;
    }

    .feature-card:hover,
    .feature-card:hover .feature-icon {
      transform: none;
    }
  }
</style>
