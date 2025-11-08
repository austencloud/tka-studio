<script lang="ts">
  /**
   * CapTypeIndicators.svelte
   *
   * Displays icons indicating which CAP (Continuous Assembly Pattern) types
   * the current sequence satisfies. Shows meaningful, educational indicators
   * for completed circular sequences.
   *
   * CAP Types:
   * - 'rotated': 90° rotation (quartered)
   * - 'mirrored': 180° / reflection (halved)
   * - 'rotated-mirrored': Both rotation and mirroring
   * - 'static': Same position (complementary)
   */

  import type { StrictCapType } from "$create/shared/services/contracts";

  let { capTypes = [] } = $props<{
    capTypes?: readonly StrictCapType[];
  }>();

  // Icon and tooltip data for each CAP type
  const capTypeInfo: Record<
    StrictCapType,
    { faIcon: string; label: string; description: string; color: string }
  > = {
    rotated: {
      faIcon: "rotate-right",
      label: "90° Rotated",
      description:
        "This is a 90° Rotated CAP - the end position is 90° clockwise from the start",
      color: "#3b82f6", // blue
    },
    mirrored: {
      faIcon: "left-right",
      label: "180° Mirrored",
      description:
        "This is a 180° Mirrored CAP - the end position is opposite the start position",
      color: "#8b5cf6", // purple
    },
    "rotated-mirrored": {
      faIcon: "arrows-rotate",
      label: "Rotated + Mirrored",
      description:
        "This CAP combines both rotation and mirroring transformations",
      color: "#ec4899", // pink
    },
    static: {
      faIcon: "circle-dot",
      label: "Static Loop",
      description:
        "This is a Static CAP - it returns to the same position (complementary)",
      color: "#10b981", // green
    },
  };

  // Show tooltip state
  let hoveredType = $state<StrictCapType | null>(null);

  function handleMouseEnter(type: StrictCapType) {
    hoveredType = type;
  }

  function handleMouseLeave() {
    hoveredType = null;
  }
</script>

{#if capTypes.length > 0}
  <div class="cap-indicators">
    {#each capTypes as capType (capType)}
      {@const info = capTypeInfo[capType as StrictCapType]}
      <div
        class="cap-icon"
        style:--icon-color={info.color}
        onmouseenter={() => handleMouseEnter(capType)}
        onmouseleave={handleMouseLeave}
        role="img"
        aria-label={info.label}
        title={info.description}
      >
        <i class="icon fas fa-{info.faIcon}"></i>
        <span class="label">{info.label}</span>

        {#if hoveredType === capType}
          <div class="tooltip">
            {info.description}
          </div>
        {/if}
      </div>
    {/each}
  </div>
{/if}

<style>
  .cap-indicators {
    display: flex;
    gap: 12px;
    align-items: center;
    justify-content: center;
  }

  .cap-icon {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 4px;
    padding: 8px 12px;
    background: linear-gradient(
      135deg,
      var(--icon-color),
      color-mix(in srgb, var(--icon-color) 80%, black)
    );
    border-radius: 8px;
    cursor: help;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .cap-icon:hover {
    transform: translateY(-2px) scale(1.05);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  }

  .icon {
    font-size: 24px;
    color: white;
    line-height: 1;
    display: inline-block;
  }

  .label {
    font-size: 10px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    text-align: center;
    white-space: nowrap;
    letter-spacing: 0.3px;
  }

  .tooltip {
    position: absolute;
    top: calc(100% + 8px);
    left: 50%;
    transform: translateX(-50%);
    background: rgba(30, 30, 30, 0.95);
    color: white;
    padding: 10px 14px;
    border-radius: 8px;
    font-size: 13px;
    white-space: normal;
    word-break: break-word;
    overflow-wrap: break-word;
    max-width: 300px;
    min-width: 200px;
    text-align: center;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    z-index: 1000;
    pointer-events: none;
    animation: tooltipFadeIn 0.15s ease-out;
  }

  .tooltip::before {
    content: "";
    position: absolute;
    top: -6px;
    left: 50%;
    transform: translateX(-50%);
    width: 0;
    height: 0;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-bottom: 6px solid rgba(30, 30, 30, 0.95);
  }

  @keyframes tooltipFadeIn {
    from {
      opacity: 0;
      transform: translateX(-50%) translateY(-4px);
    }
    to {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
  }

  /* Responsive adjustments */
  @media (max-width: 600px) {
    .cap-indicators {
      gap: 8px;
    }

    .cap-icon {
      padding: 6px 10px;
    }

    .icon {
      font-size: 20px;
    }

    .label {
      font-size: 9px;
    }

    .tooltip {
      white-space: normal;
      word-break: break-word;
      overflow-wrap: break-word;
      max-width: 200px;
      min-width: 150px;
      font-size: 12px;
    }
  }

  /* Hide text labels when space is very constrained (long sequences) */
  @media (max-width: 500px) {
    .label {
      display: none;
    }

    .cap-icon {
      padding: 8px;
      min-width: 40px;
      min-height: 40px;
    }
  }

  /* Also hide labels when height is constrained (landscape mode with long sequences) */
  @media (max-height: 500px) {
    .label {
      display: none;
    }

    .cap-icon {
      padding: 6px;
      min-width: 36px;
      min-height: 36px;
    }

    .icon {
      font-size: 20px;
    }
  }
</style>
