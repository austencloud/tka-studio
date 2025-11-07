<script lang="ts">
  import type { LandingHeroContent } from "../domain";

  let {
    hero,
    titleId = "landing-title",
  }: {
    hero: LandingHeroContent;
    titleId?: string;
  } = $props();
</script>

<section class="hero-section">
  <h1 id={titleId} class="hero-title">
    <span class="gradient-text">{hero.title}</span>
    <span class="sparkle sparkle-1"></span>
    <span class="sparkle sparkle-2"></span>
    <span class="sparkle sparkle-3"></span>
    <span class="sparkle sparkle-4"></span>
    <span class="sparkle sparkle-5"></span>
    <span class="sparkle sparkle-6"></span>
  </h1>
  <p class="hero-subtitle">{hero.subtitle}</p>
</section>

<style>
  .hero-section {
    text-align: center;
    padding: clamp(3.5rem, 8vh, 5rem) 0 clamp(0.5rem, 2vh, 1rem) 0;
    flex-shrink: 0;
  }

  .hero-title {
    font-size: clamp(1.75rem, 5vw, 3rem);
    font-weight: 900;
    margin-bottom: clamp(0.25rem, 1vh, 0.5rem);
    line-height: 1.1;
    position: relative;
    display: inline-block;
  }

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
    animation: gradient-flow 8s linear infinite;
  }

  @keyframes gradient-flow {
    0% {
      background-position: 0% 50%;
    }
    100% {
      background-position: 200% 50%;
    }
  }

  .sparkle {
    position: absolute;
    width: 8px;
    height: 8px;
    opacity: 0;
    pointer-events: none;
  }

  .sparkle::before,
  .sparkle::after {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, transparent, currentColor, transparent);
    transform: translate(-50%, -50%);
  }

  .sparkle::before {
    transform: translate(-50%, -50%) rotate(0deg);
  }

  .sparkle::after {
    transform: translate(-50%, -50%) rotate(90deg);
  }

  .sparkle-1 {
    top: 0;
    left: 15%;
    color: #ffd700;
    animation-delay: 0s;
    width: 12px;
    height: 12px;
  }

  .sparkle-2 {
    top: 10%;
    right: 20%;
    color: #ffed4e;
    animation-delay: 0.8s;
    width: 8px;
    height: 8px;
  }

  .sparkle-3 {
    top: 15%;
    left: 50%;
    color: #ffc700;
    animation-delay: 1.5s;
    width: 10px;
    height: 10px;
  }

  .sparkle-4 {
    bottom: 10%;
    left: 25%;
    color: #ffbf00;
    animation-delay: 0.5s;
    width: 9px;
    height: 9px;
  }

  .sparkle-5 {
    bottom: 5%;
    right: 30%;
    color: #ffe55c;
    animation-delay: 2s;
    width: 11px;
    height: 11px;
  }

  .sparkle-6 {
    top: 50%;
    right: 10%;
    color: #ffa500;
    animation-delay: 1.2s;
    width: 7px;
    height: 7px;
  }

  .sparkle-1,
  .sparkle-4 {
    animation: twinkle 2.5s ease-in-out infinite;
  }

  .sparkle-2,
  .sparkle-5 {
    animation: twinkle 3s ease-in-out infinite;
  }

  .sparkle-3,
  .sparkle-6 {
    animation: twinkle 2.8s ease-in-out infinite;
  }

  @keyframes twinkle {
    0%,
    100% {
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

  .hero-subtitle {
    font-size: clamp(0.875rem, 2vw, 1.125rem);
    color: rgba(255, 255, 255, 0.8);
    margin: 0;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }

  @media (max-height: 600px) {
    .hero-section {
      padding: 0.25rem 0;
    }

    .hero-title {
      font-size: clamp(1.25rem, 4vw, 1.75rem);
    }

    .hero-subtitle {
      font-size: clamp(0.75rem, 1.5vw, 0.875rem);
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .gradient-text {
      animation: none;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }

    .sparkle {
      display: none;
    }
  }
</style>
