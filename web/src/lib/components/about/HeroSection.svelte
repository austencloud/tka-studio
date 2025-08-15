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
    <p class="hero-subtitle">Innovation in Flow Arts Education</p>
  </div>
</section>

<!-- Philosophy Section -->
<section class="philosophy">
  <div class="container">
    <h2>Philosophy</h2>
    <div class="philosophy-content">
      <p>
        The Kinetic Alphabet represents a paradigm shift in how flow artists
        approach their craft. By providing a systematic framework for
        understanding movement, we enable practitioners to develop deeper
        technical skills while preserving the artistic freedom that defines flow
        arts.
      </p>
      <p>
        Our approach combines rigorous technical methodology with creative
        expression, allowing artists to build a solid foundation while exploring
        infinite possibilities for personal artistic development.
      </p>
    </div>
  </div>
</section>

<style>
  /* Hero Section */
  .hero {
    position: relative;
    color: var(--text-color);
    padding: var(--spacing-3xl) 0 var(--spacing-2xl) 0;
    text-align: center;
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.8s ease;
    z-index: 1;
    min-height: 40vh;
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
    padding: var(--spacing-3xl) 0;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
  }

  h2 {
    text-align: center;
    margin-bottom: var(--spacing-2xl);
    color: var(--text-color);
    font-size: 2.5rem;
    font-weight: 700;
  }

  .philosophy-content {
    max-width: 800px;
    margin: 0 auto;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    padding: var(--spacing-xl);
    border-radius: 1.5rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
  }

  .philosophy-content p {
    font-size: 1.125rem;
    line-height: 1.8;
    margin-bottom: var(--spacing-lg);
    color: rgba(255, 255, 255, 0.9);
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .hero {
      padding: var(--spacing-2xl) 0;
      min-height: 30vh;
      margin: var(--spacing-md);
    }

    .hero-title {
      font-size: 2.5rem;
    }

    .hero-subtitle {
      font-size: 1.125rem;
    }

    .philosophy {
      padding: var(--spacing-2xl) 0;
    }

    .container {
      padding: 0 var(--spacing-md);
    }

    h2 {
      font-size: 2rem;
    }

    .philosophy-content {
      padding: var(--spacing-lg);
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
