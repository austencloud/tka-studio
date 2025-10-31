<!-- PropTypeTab.svelte - Prop type selection with actual desktop app files -->
<script lang="ts">
  import type { AppSettings, IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import SettingCard from "../SettingCard.svelte";

  let { settings, onUpdate } = $props<{
    settings: AppSettings;
    onUpdate?: (event: { key: string; value: unknown }) => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Exact prop types from desktop app prop_type_tab.py
  const propTypes = [
    { id: "Staff", label: "Staff", image: "/images/props/staff.svg" },
    {
      id: "Simplestaff",
      label: "Simple Staff",
      image: "/images/props/simple_staff.svg",
    },
    { id: "Club", label: "Club", image: "/images/props/club.svg" },
    { id: "Fan", label: "Fan", image: "/images/props/fan.svg" },
    { id: "Triad", label: "Triad", image: "/images/props/triad.svg" },
    { id: "Minihoop", label: "Mini Hoop", image: "/images/props/minihoop.svg" },
    { id: "Buugeng", label: "Buugeng", image: "/images/props/buugeng.svg" },
    {
      id: "Triquetra",
      label: "Triquetra",
      image: "/images/props/triquetra.svg",
    },
    { id: "Sword", label: "Sword", image: "/images/props/sword.svg" },
    { id: "Chicken", label: "Chicken", image: "/images/props/chicken.png" },
    { id: "Hand", label: "Hand", image: "/images/props/hand.svg" },
    { id: "Guitar", label: "Guitar", image: "/images/props/guitar.svg" },
  ];

  let selectedPropType = $state(settings.propType || "Staff");

  function selectPropType(propType: string) {
    // Trigger selection haptic feedback for prop type selection
    hapticService?.trigger("selection");

    selectedPropType = propType;
    onUpdate?.({ key: "propType", value: propType });
  }
</script>

<div class="tab-content">
  <SettingCard
    title="Select Prop"
    helpText="Your prop type determines the visual appearance of movements in pictographs. Different props have unique shapes and rotation patterns."
  >
    <div class="prop-grid">
      {#each propTypes as prop}
        <button
          class="prop-button"
          class:selected={selectedPropType === prop.id}
          onclick={() => selectPropType(prop.id)}
          onkeydown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              e.preventDefault();
              selectPropType(prop.id);
            }
          }}
          aria-label={`Select ${prop.label} prop type`}
          aria-pressed={selectedPropType === prop.id}
          title={`${prop.label} - Click to select this prop type`}
        >
          <div class="prop-image-container">
            <img
              src={prop.image}
              alt={prop.label}
              class="prop-image"
              loading="lazy"
            />
          </div>
          <span class="prop-label">{prop.label}</span>
        </button>
      {/each}
    </div>
  </SettingCard>
</div>

<style>
  .tab-content {
    width: 100%;
    max-width: var(--max-content-width, 100%);
    margin: 0 auto;
    container-type: inline-size;
  }

  .prop-grid {
    display: grid;
    grid-template-columns: repeat(
      auto-fill,
      minmax(110px, 1fr)
    ); /* Changed to auto-fill for more consistent layouts */
    gap: clamp(
      14px,
      2.2vw,
      24px
    ); /* Slightly increased gap for better visual separation */
    margin-top: clamp(20px, 2.5vw, 32px);
    width: 100%;
  }

  /* Mobile portrait - larger touch targets, better spacing */
  @media (max-width: 480px) {
    .prop-grid {
      /* 3 columns on mobile portrait for better balance */
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-top: 16px;
      padding: 0;
    }
  }

  /* Ultra-narrow screens - maintain 3 column layout */
  @media (max-width: 390px) {
    .prop-grid {
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      margin-top: 12px;
    }
  }

  @media (min-width: 481px) and (max-width: 768px) {
    .prop-grid {
      grid-template-columns: repeat(
        auto-fit,
        minmax(clamp(100px, 20vw, 130px), 1fr)
      );
      gap: clamp(10px, 1.5vw, 16px);
      margin-top: clamp(16px, 2vw, 24px);
    }
  }

  /* Container queries for better space utilization */
  @container (min-width: 400px) {
    .prop-grid {
      grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
      gap: clamp(16px, 2.2vw, 24px);
    }
  }

  @container (min-width: 600px) {
    .prop-grid {
      grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));
      gap: clamp(18px, 2.5vw, 26px);
    }
  }

  @container (min-width: 800px) {
    .prop-grid {
      grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
      gap: 22px;
    }
  }

  @container (min-width: 1000px) {
    .prop-grid {
      grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
      gap: 26px;
    }
  }

  .prop-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: clamp(6px, 1vw, 12px);
    padding: clamp(
      10px,
      1.5vw,
      18px
    ); /* Increased padding for better touch targets */
    background: rgba(255, 255, 255, 0.06);
    border: 2px solid rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease-out;
    color: rgba(255, 255, 255, 0.85);
    min-height: clamp(
      90px,
      16vw,
      120px
    ); /* Increased min-height for better touch targets */
    aspect-ratio: 1;
    /* Ensure minimum touch target size */
    min-width: 90px; /* Increased from 48px to ensure comfortable touch targets */
    position: relative;
  }

  /* Mobile portrait - larger, more tappable buttons */
  @media (max-width: 480px) {
    .prop-button {
      min-height: 90px; /* Larger touch targets */
      padding: 10px;
      gap: 6px;
      border-radius: 10px;
      /* Ensure proper touch target size */
      min-width: 80px;
    }
  }

  /* Ultra-narrow screens - still maintain good touch targets */
  @media (max-width: 390px) {
    .prop-button {
      min-height: 85px;
      padding: 8px;
      gap: 5px;
      border-radius: 8px;
      min-width: 75px;
    }
  }

  @media (min-width: 481px) and (max-width: 768px) {
    .prop-button {
      min-height: clamp(75px, 12vw, 95px);
      padding: clamp(8px, 1.2vw, 12px);
      gap: clamp(5px, 0.8vw, 8px);
      border-radius: clamp(8px, 1.5vw, 12px);
    }
  }

  /* Height-constrained devices (landscape mode, browser chrome) */
  @media (max-height: 600px) and (max-width: 768px) {
    .prop-button {
      min-height: clamp(45px, 8vh, 65px);
      padding: clamp(3px, 0.5vw, 6px);
      gap: clamp(2px, 0.4vw, 4px);
    }
  }

  .prop-button:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.35);
    color: #ffffff;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .prop-button.selected {
    background: rgba(99, 102, 241, 0.25);
    border-color: #6366f1;
    color: #ffffff;
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.4);
  }

  .prop-button:focus-visible {
    outline: 2px solid #6366f1;
    outline-offset: 2px;
    border-color: rgba(99, 102, 241, 0.6);
  }

  .prop-button:active {
    transform: scale(0.98);
  }

  .prop-image-container {
    width: clamp(60%, 4vw, 85%);
    height: clamp(60%, 4vw, 85%);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  /* Mobile portrait - larger, more visible icons */
  @media (max-width: 480px) {
    .prop-image-container {
      width: 60%;
      height: 60%;
      min-width: 32px;
      min-height: 32px;
    }
  }

  /* Ultra-narrow screens - still visible */
  @media (max-width: 390px) {
    .prop-image-container {
      width: 55%;
      height: 55%;
      min-width: 28px;
      min-height: 28px;
    }
  }

  @media (min-width: 481px) and (max-width: 768px) {
    .prop-image-container {
      width: clamp(60%, 4vw, 75%);
      height: clamp(60%, 4vw, 75%);
    }
  }

  /* Height-constrained devices */
  @media (max-height: 600px) and (max-width: 768px) {
    .prop-image-container {
      width: clamp(50%, 3.5vw, 70%);
      height: clamp(50%, 3.5vw, 70%);
    }
  }

  .prop-image {
    max-width: 100%;
    max-height: 100%;
    opacity: 0.85;
    transition: opacity 0.2s ease;
  }

  .prop-button:hover .prop-image {
    opacity: 1;
  }

  .prop-button.selected .prop-image {
    opacity: 1;
  }

  .prop-label {
    font-size: clamp(10px, 1.1vw, 14px);
    font-weight: 500;
    text-align: center;
    line-height: 1.2;
    word-break: break-word;
    margin-top: 2px;
  }

  /* Mobile portrait - more readable labels */
  @media (max-width: 480px) {
    .prop-label {
      font-size: 11px;
      line-height: 1.1;
      margin-top: 2px;
      font-weight: 600;
      letter-spacing: 0.01em;
    }
  }

  /* Ultra-narrow screens - maintain readability */
  @media (max-width: 390px) {
    .prop-label {
      font-size: 10px;
      line-height: 1.05;
      margin-top: 2px;
      font-weight: 600;
      letter-spacing: 0.02em;
      /* Wrap text if needed instead of hiding */
      white-space: normal;
      word-break: break-word;
      max-width: 100%;
    }
  }

  @media (min-width: 481px) and (max-width: 768px) {
    .prop-label {
      font-size: clamp(9px, 1.1vw, 12px);
      line-height: 1.1;
      margin-top: clamp(1px, 0.3vw, 3px);
      font-weight: 500;
    }
  }

  /* Height-constrained devices */
  @media (max-height: 600px) and (max-width: 768px) {
    .prop-label {
      font-size: clamp(7px, 0.8vw, 9px);
      line-height: 0.95;
      margin-top: 1px;
      font-weight: 600;
    }
  }

  /* Remove old responsive styles - replaced with container queries */
</style>
