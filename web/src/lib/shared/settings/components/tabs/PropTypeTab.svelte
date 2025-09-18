<!-- PropTypeTab.svelte - Prop type selection with actual desktop app files -->
<script lang="ts">
  import type { AppSettings } from "$shared";
  import SettingCard from "../SettingCard.svelte";

  let { settings, onUpdate } = $props<{
    settings: AppSettings;
    onUpdate?: (event: { key: string; value: unknown }) => void;
  }>();

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
    selectedPropType = propType;
    onUpdate?.({ key: "propType", value: propType });
  }
</script>

<div class="tab-content">
  <SettingCard
    title="Select Prop Type"
    description="Choose your primary prop type for sequences"
  >
    <div class="prop-grid">
      {#each propTypes as prop}
        <button
          class="prop-button"
          class:selected={selectedPropType === prop.id}
          onclick={() => selectPropType(prop.id)}
          onkeydown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
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
    grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
    gap: clamp(16px, 2vw, 24px);
    margin-top: clamp(20px, 2.5vw, 32px);
    width: 100%;
  }

  /* Container queries for better space utilization */
  @container (min-width: 400px) {
    .prop-grid {
      grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
      gap: clamp(18px, 2.2vw, 26px);
    }
  }

  @container (min-width: 600px) {
    .prop-grid {
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: clamp(20px, 2.5vw, 28px);
    }
  }

  @container (min-width: 800px) {
    .prop-grid {
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
      gap: 24px;
    }
  }

  @container (min-width: 1000px) {
    .prop-grid {
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 28px;
    }
  }

  .prop-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: clamp(8px, 1vw, 14px);
    padding: clamp(12px, 1.5vw, 20px);
    background: rgba(255, 255, 255, 0.06);
    border: 2px solid rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.2s ease-out;
    color: rgba(255, 255, 255, 0.85);
    min-height: clamp(90px, 10vw, 120px);
    aspect-ratio: 1;
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
    width: clamp(40px, 5vw, 60px);
    height: clamp(40px, 5vw, 60px);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
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
    font-size: clamp(11px, 1.3vw, 15px);
    font-weight: 500;
    text-align: center;
    line-height: 1.3;
    word-break: break-word;
  }

  /* Remove old responsive styles - replaced with container queries */
</style>
