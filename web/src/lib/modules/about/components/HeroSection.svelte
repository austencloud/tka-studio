<script lang="ts">
  import { onMount } from "svelte";

  let isVisible = $state(false);

  onMount(() => {
    isVisible = true;
  });
</script>

<!-- Hero Section -->
<section class="hero" class:visible={isVisible}>
  <div class="hero-content">
    <h1 class="hero-title">About The Kinetic Alphabet</h1>
    <p class="hero-subtitle">A movement notation system for flow arts</p>
  </div>
</section>

<!-- Philosophy Section -->
<section class="philosophy">
  <div class="container">
    <h2>Why TKA?</h2>
    <div class="philosophy-content">
      <div class="problem-solution">
        <div class="problem">
          <h4>❌ The Problem:</h4>
          <p>Flow arts movements are hard to communicate precisely</p>
        </div>
        <div class="solution">
          <h4>✅ The Solution:</h4>
          <p>
            A systematic way to break them down, write them out, and share them
          </p>
        </div>
      </div>
      <div class="key-benefit">
        <p>
          <strong>Result:</strong> Learn underlying patterns instead of just copying
          moves. It's like having a common language for movement.
        </p>
      </div>
    </div>
  </div>
</section>

<style>
  /* Hero Section */
  .hero {
    position: relative;
    color: var(--text-color);
    padding: var(--spacing-xl) 0 var(--spacing-lg) 0;
    text-align: center;
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.8s ease;
    z-index: 1;
    min-height: 25vh;
    display: flex;
    align-items: center;

    /* Glassmorphism styling */
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
    max-width: 800px;
    margin: 0 auto;
    padding: 0 var(--spacing-xl);
  }

  .hero-title {
    font-size: 3rem;
    margin-bottom: var(--spacing-md);
    font-weight: 900;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .hero-subtitle {
    font-size: 1.25rem;
    opacity: 0.9;
    font-weight: 300;
  }

  /* Philosophy Section */
  .philosophy {
    padding: var(--spacing-lg) 0;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
  }

  h2 {
    text-align: center;
    margin-bottom: var(--spacing-lg);
    color: var(--text-color);
    font-size: 2rem;
    font-weight: 700;
  }

  .philosophy-content {
    max-width: 800px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    padding: var(--spacing-lg);
    border-radius: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .problem-solution {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: var(--spacing-lg);
    margin-bottom: var(--spacing-lg);
  }

  .problem,
  .solution {
    padding: var(--spacing-md);
    border-radius: 0.75rem;
    text-align: center;
  }

  .problem {
    background: rgba(255, 100, 100, 0.1);
    border: 1px solid rgba(255, 100, 100, 0.2);
  }

  .solution {
    background: rgba(100, 255, 100, 0.1);
    border: 1px solid rgba(100, 255, 100, 0.2);
  }

  .problem h4,
  .solution h4 {
    margin: 0 0 var(--spacing-sm) 0;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-color);
  }

  .problem p,
  .solution p {
    margin: 0;
    color: rgba(255, 255, 255, 0.9);
    line-height: 1.5;
  }

  .key-benefit {
    text-align: center;
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.08);
    border-radius: 0.75rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .key-benefit p {
    margin: 0;
    color: rgba(255, 255, 255, 0.95);
    line-height: 1.6;
    font-size: 1.1rem;
  }

  .key-benefit strong {
    color: var(--primary-color);
    font-weight: 600;
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .hero {
      padding: var(--spacing-2xl) 0;
      min-height: 30vh;
      margin: var(--spacing-md);
    }

    .hero-content {
      padding: 0 var(--spacing-md);
    }

    .hero-title {
      font-size: 2.5rem;
    }

    .hero-subtitle {
      font-size: 1.1rem;
    }

    .philosophy {
      padding: var(--spacing-md) 0;
    }

    .container {
      padding: 0 var(--spacing-md);
    }

    h2 {
      font-size: 1.75rem;
    }

    .problem-solution {
      grid-template-columns: 1fr;
      gap: var(--spacing-md);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .hero {
      transition: none;
      opacity: 1;
      transform: none;
    }
  }
</style>
