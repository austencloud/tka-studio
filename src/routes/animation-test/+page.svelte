<script lang="ts">
  /**
   * Animation Test Page
   * Interactive demo for hero title animations and sparkle effects
   */

  type GradientAnimation = {
    id: string;
    name: string;
    description: string;
  };

  type SparkleStyle = {
    id: string;
    name: string;
    description: string;
  };

  const gradientAnimations: GradientAnimation[] = [
    { id: 'flow', name: 'Flowing Rainbow', description: 'Horizontal flow animation' },
    { id: 'wave', name: 'Wave Pulse', description: 'Pulsing wave effect' },
    { id: 'shimmer', name: 'Shimmer', description: 'Shimmering highlight sweep' },
    { id: 'rotate', name: 'Rotating Gradient', description: 'Circular gradient rotation' },
    { id: 'pulse', name: 'Rainbow Pulse', description: 'Breathing rainbow effect' },
    { id: 'diagonal', name: 'Diagonal Flow', description: 'Diagonal sweeping gradient' },
  ];

  const sparkleStyles: SparkleStyle[] = [
    { id: 'twinkle', name: 'Classic Twinkle', description: 'Rotating cross stars' },
    { id: 'burst', name: 'Starburst', description: '4-point star burst' },
    { id: 'float', name: 'Floating Dots', description: 'Floating particle effect' },
    { id: 'shimmer', name: 'Shimmer Trails', description: 'Trailing shimmer lines' },
    { id: 'none', name: 'No Sparkles', description: 'Just the gradient' },
  ];

  let selectedGradient = $state<string>('flow');
  let selectedSparkle = $state<string>('twinkle');
</script>

<div class="animation-test-page">
  <div class="controls-panel">
    <h2>Animation Test Studio</h2>
    <p class="subtitle">Pick your favorite combination!</p>

    <div class="control-section">
      <h3>Gradient Animation</h3>
      <div class="button-grid">
        {#each gradientAnimations as anim}
          <button
            class="option-button"
            class:active={selectedGradient === anim.id}
            onclick={() => selectedGradient = anim.id}
          >
            <span class="option-name">{anim.name}</span>
            <span class="option-desc">{anim.description}</span>
          </button>
        {/each}
      </div>
    </div>

    <div class="control-section">
      <h3>Sparkle Effect</h3>
      <div class="button-grid">
        {#each sparkleStyles as style}
          <button
            class="option-button"
            class:active={selectedSparkle === style.id}
            onclick={() => selectedSparkle = style.id}
          >
            <span class="option-name">{style.name}</span>
            <span class="option-desc">{style.description}</span>
          </button>
        {/each}
      </div>
    </div>

    <div class="current-selection">
      <strong>Current:</strong> {gradientAnimations.find(a => a.id === selectedGradient)?.name} +
      {sparkleStyles.find(s => s.id === selectedSparkle)?.name}
    </div>
  </div>

  <div class="preview-area">
    <div class="hero-preview">
      <h1 class="hero-title" data-gradient={selectedGradient}>
        <span class="gradient-text">The Kinetic Alphabet</span>

        {#if selectedSparkle !== 'none'}
          <span class="sparkle sparkle-1" data-style={selectedSparkle}></span>
          <span class="sparkle sparkle-2" data-style={selectedSparkle}></span>
          <span class="sparkle sparkle-3" data-style={selectedSparkle}></span>
          <span class="sparkle sparkle-4" data-style={selectedSparkle}></span>
          <span class="sparkle sparkle-5" data-style={selectedSparkle}></span>
          <span class="sparkle sparkle-6" data-style={selectedSparkle}></span>
        {/if}
      </h1>
      <p class="hero-subtitle">Master the art of poi spinning</p>
    </div>
  </div>
</div>

<style>
  .animation-test-page {
    min-height: 100vh;
    background: linear-gradient(135deg, rgba(20, 20, 30, 1) 0%, rgba(30, 30, 40, 1) 100%);
    display: grid;
    grid-template-columns: 400px 1fr;
    color: white;
  }

  @media (max-width: 1024px) {
    .animation-test-page {
      grid-template-columns: 1fr;
      grid-template-rows: auto 1fr;
    }
  }

  /* ============================================================================
     CONTROLS PANEL
     ============================================================================ */
  .controls-panel {
    background: rgba(0, 0, 0, 0.3);
    padding: 2rem;
    overflow-y: auto;
    border-right: 1px solid rgba(255, 255, 255, 0.1);
  }

  .controls-panel h2 {
    font-size: 1.75rem;
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  .subtitle {
    color: rgba(255, 255, 255, 0.7);
    margin-bottom: 2rem;
  }

  .control-section {
    margin-bottom: 2rem;
  }

  .control-section h3 {
    font-size: 1.125rem;
    margin-bottom: 1rem;
    color: rgba(255, 255, 255, 0.9);
  }

  .button-grid {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }

  .option-button {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 0.75rem;
    padding: 1rem;
    color: white;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .option-button:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(102, 126, 234, 0.5);
    transform: translateX(4px);
  }

  .option-button.active {
    background: rgba(102, 126, 234, 0.2);
    border-color: rgba(102, 126, 234, 0.8);
    box-shadow: 0 0 16px rgba(102, 126, 234, 0.3);
  }

  .option-name {
    font-weight: 600;
    font-size: 0.9375rem;
  }

  .option-desc {
    font-size: 0.8125rem;
    color: rgba(255, 255, 255, 0.6);
  }

  .current-selection {
    margin-top: 2rem;
    padding: 1rem;
    background: rgba(102, 126, 234, 0.1);
    border: 1px solid rgba(102, 126, 234, 0.3);
    border-radius: 0.75rem;
    font-size: 0.875rem;
    line-height: 1.6;
  }

  /* ============================================================================
     PREVIEW AREA
     ============================================================================ */
  .preview-area {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    position: relative;
  }

  .hero-preview {
    text-align: center;
    max-width: 800px;
  }

  .hero-title {
    font-size: clamp(2.5rem, 6vw, 4rem);
    font-weight: 900;
    margin-bottom: 1rem;
    line-height: 1.1;
    position: relative;
    display: inline-block;
  }

  .hero-subtitle {
    font-size: clamp(1rem, 2.5vw, 1.25rem);
    color: rgba(255, 255, 255, 0.8);
    margin: 0;
  }

  /* ============================================================================
     GRADIENT ANIMATIONS
     ============================================================================ */
  .gradient-text {
    background: linear-gradient(
      90deg,
      #667eea 0%,
      #764ba2 25%,
      #f43f5e 50%,
      #38bdf8 75%,
      #667eea 100%
    );
    background-size: 200% 100%;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
  }

  /* Flow Animation (Original) */
  [data-gradient="flow"] .gradient-text {
    animation: gradient-flow 8s linear infinite;
  }

  @keyframes gradient-flow {
    0% { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
  }

  /* Wave Pulse */
  [data-gradient="wave"] .gradient-text {
    background: linear-gradient(
      90deg,
      #667eea 0%,
      #764ba2 20%,
      #f43f5e 40%,
      #38bdf8 60%,
      #667eea 80%,
      #764ba2 100%
    );
    background-size: 300% 100%;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: wave-pulse 4s ease-in-out infinite;
  }

  @keyframes wave-pulse {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
  }

  /* Shimmer */
  [data-gradient="shimmer"] .gradient-text {
    background: linear-gradient(
      90deg,
      rgba(102, 126, 234, 0.3) 0%,
      rgba(102, 126, 234, 1) 45%,
      rgba(255, 255, 255, 1) 50%,
      rgba(56, 189, 248, 1) 55%,
      rgba(56, 189, 248, 0.3) 100%
    );
    background-size: 200% 100%;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shimmer 3s ease-in-out infinite;
  }

  @keyframes shimmer {
    0% { background-position: -100% 0%; }
    100% { background-position: 200% 0%; }
  }

  /* Rotate */
  [data-gradient="rotate"] .gradient-text {
    background: conic-gradient(
      from 0deg,
      #667eea 0deg,
      #764ba2 90deg,
      #f43f5e 180deg,
      #38bdf8 270deg,
      #667eea 360deg
    );
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: rotate-gradient 6s linear infinite;
  }

  @keyframes rotate-gradient {
    0% { filter: hue-rotate(0deg); }
    100% { filter: hue-rotate(360deg); }
  }

  /* Pulse */
  [data-gradient="pulse"] .gradient-text {
    background: radial-gradient(
      circle at center,
      #667eea 0%,
      #764ba2 25%,
      #f43f5e 50%,
      #38bdf8 75%,
      #667eea 100%
    );
    background-size: 200% 200%;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: pulse-gradient 3s ease-in-out infinite;
  }

  @keyframes pulse-gradient {
    0%, 100% {
      background-size: 200% 200%;
      opacity: 1;
    }
    50% {
      background-size: 150% 150%;
      opacity: 0.8;
    }
  }

  /* Diagonal Flow */
  [data-gradient="diagonal"] .gradient-text {
    background: linear-gradient(
      135deg,
      #667eea 0%,
      #764ba2 25%,
      #f43f5e 50%,
      #38bdf8 75%,
      #667eea 100%
    );
    background-size: 300% 300%;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: diagonal-flow 6s linear infinite;
  }

  @keyframes diagonal-flow {
    0% { background-position: 0% 0%; }
    100% { background-position: 100% 100%; }
  }

  /* ============================================================================
     SPARKLE STYLES
     ============================================================================ */

  /* Base Sparkle */
  .sparkle {
    position: absolute;
    pointer-events: none;
    opacity: 0;
  }

  /* Twinkle Style (Original) */
  [data-style="twinkle"] {
    width: 8px;
    height: 8px;
    animation: twinkle 2.5s ease-in-out infinite;
  }

  [data-style="twinkle"]::before,
  [data-style="twinkle"]::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, currentColor, transparent);
    transform: translate(-50%, -50%);
  }

  [data-style="twinkle"]::before {
    transform: translate(-50%, -50%) rotate(0deg);
  }

  [data-style="twinkle"]::after {
    transform: translate(-50%, -50%) rotate(90deg);
  }

  @keyframes twinkle {
    0%, 100% {
      opacity: 0;
      transform: scale(0) rotate(0deg);
      filter: brightness(1);
    }
    50% {
      opacity: 1;
      transform: scale(1) rotate(180deg);
      filter: brightness(2) drop-shadow(0 0 4px currentColor);
    }
  }

  /* Burst Style - 4-point star */
  [data-style="burst"] {
    width: 16px;
    height: 16px;
    animation: burst 2s ease-in-out infinite;
  }

  [data-style="burst"]::before,
  [data-style="burst"]::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100%;
    height: 3px;
    background: radial-gradient(ellipse at center, currentColor, transparent 70%);
    transform: translate(-50%, -50%);
    box-shadow: 0 0 8px currentColor;
  }

  [data-style="burst"]::before {
    transform: translate(-50%, -50%) rotate(45deg);
  }

  [data-style="burst"]::after {
    transform: translate(-50%, -50%) rotate(-45deg);
  }

  @keyframes burst {
    0%, 100% {
      opacity: 0;
      transform: scale(0);
    }
    50% {
      opacity: 1;
      transform: scale(1.5);
      filter: brightness(3);
    }
  }

  /* Float Style - Round particles */
  [data-style="float"] {
    width: 6px;
    height: 6px;
    background: radial-gradient(circle, currentColor, transparent);
    border-radius: 50%;
    animation: float 4s ease-in-out infinite;
    box-shadow: 0 0 12px currentColor;
  }

  @keyframes float {
    0%, 100% {
      opacity: 0;
      transform: translateY(0) scale(0);
    }
    50% {
      opacity: 1;
      transform: translateY(-20px) scale(1.2);
    }
  }

  /* Shimmer Style - Trailing lines */
  [data-style="shimmer"] {
    width: 20px;
    height: 2px;
    background: linear-gradient(90deg, transparent, currentColor, transparent);
    animation: shimmer-trail 3s ease-in-out infinite;
    box-shadow: 0 0 8px currentColor;
  }

  @keyframes shimmer-trail {
    0%, 100% {
      opacity: 0;
      transform: translateX(-30px) scaleX(0);
    }
    50% {
      opacity: 1;
      transform: translateX(30px) scaleX(1);
      filter: brightness(2);
    }
  }

  /* Sparkle Positioning */
  .sparkle-1 {
    top: 0;
    left: 15%;
    color: #667eea;
    animation-delay: 0s;
  }

  .sparkle-2 {
    top: 10%;
    right: 20%;
    color: #38bdf8;
    animation-delay: 0.8s;
  }

  .sparkle-3 {
    top: 15%;
    left: 50%;
    color: #f43f5e;
    animation-delay: 1.5s;
  }

  .sparkle-4 {
    bottom: 10%;
    left: 25%;
    color: #764ba2;
    animation-delay: 0.5s;
  }

  .sparkle-5 {
    bottom: 5%;
    right: 30%;
    color: #06b6d4;
    animation-delay: 2s;
  }

  .sparkle-6 {
    top: 50%;
    right: 10%;
    color: #ec4899;
    animation-delay: 1.2s;
  }

  /* Size variations */
  .sparkle-1 { width: 12px; height: 12px; }
  .sparkle-2 { width: 8px; height: 8px; }
  .sparkle-3 { width: 10px; height: 10px; }
  .sparkle-4 { width: 9px; height: 9px; }
  .sparkle-5 { width: 11px; height: 11px; }
  .sparkle-6 { width: 7px; height: 7px; }

  /* Float style needs different sizes */
  [data-style="float"].sparkle-1 { width: 8px; height: 8px; }
  [data-style="float"].sparkle-2 { width: 5px; height: 5px; }
  [data-style="float"].sparkle-3 { width: 7px; height: 7px; }
  [data-style="float"].sparkle-4 { width: 6px; height: 6px; }
  [data-style="float"].sparkle-5 { width: 8px; height: 8px; }
  [data-style="float"].sparkle-6 { width: 5px; height: 5px; }

  /* Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    .gradient-text,
    .sparkle {
      animation: none !important;
    }

    .gradient-text {
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .sparkle {
      display: none;
    }
  }
</style>
