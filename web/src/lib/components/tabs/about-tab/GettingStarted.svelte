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
          The web-based constructor allows creation and visualization of custom
          sequences.
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

<style>
  /* Getting Started Section */
  .getting-started {
    padding: var(--spacing-lg) 0;
  }

  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-lg);
  }

  .getting-started h2 {
    text-align: center;
    margin-bottom: var(--spacing-lg);
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
    transition: all 0.3s ease;
  }

  .step:hover {
    background: rgba(255, 255, 255, 0.06);
    transform: translateY(-3px);
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

  /* Mobile responsive */
  @media (max-width: 768px) {
    .getting-started {
      padding: var(--spacing-2xl) 0;
    }

    .container {
      padding: 0 var(--spacing-md);
    }

    .getting-started h2 {
      font-size: 2rem;
    }

    .steps-grid {
      grid-template-columns: 1fr;
      gap: var(--spacing-lg);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .step {
      transition: none;
    }

    .step:hover {
      transform: none;
    }
  }
</style>
