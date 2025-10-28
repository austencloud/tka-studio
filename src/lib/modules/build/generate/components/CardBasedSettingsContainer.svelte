<!--
CardBasedSettingsContainer - Minimal card grid renderer
Delegates ALL logic to services (SRP compliant)
-->
<script lang="ts">
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { flip } from "svelte/animate";
  import { quintOut } from "svelte/easing";
  import { scale } from "svelte/transition";
  import type {
    CardDescriptor,
    ICardConfigurationService,
    ILevelConversionService,
    IResponsiveTypographyService,
    ITurnIntensityManagerService
  } from "../shared/services/contracts";
  import type { UIGenerationConfig } from "../state/generate-config.svelte";
// Card components
  import CAPCard from "./cards/CAPCard.svelte";
  import GenerationModeCard from "./cards/GenerationModeCard.svelte";
  import GridModeCard from "./cards/GridModeCard.svelte";
  import LengthCard from "./cards/LengthCard.svelte";
  import LevelCard from "./cards/LevelCard.svelte";
  import PropContinuityCard from "./cards/PropContinuityCard.svelte";
  import SliceSizeCard from "./cards/SliceSizeCard.svelte";
  import TurnIntensityCard from "./cards/TurnIntensityCard.svelte";
  import GenerateButtonCard from "./cards/GenerateButtonCard.svelte";

  // Props
  let { config, isFreeformMode, updateConfig, isGenerating, onGenerateClicked } = $props<{
    config: UIGenerationConfig;
    isFreeformMode: boolean;
    updateConfig: (updates: Partial<UIGenerationConfig>) => void;
    isGenerating: boolean;
    onGenerateClicked: (options: any) => Promise<void>;
  }>();

  // Services - use $state to make them reactive
  let levelService = $state<ILevelConversionService | null>(null);
  let typographyService = $state<IResponsiveTypographyService | null>(null);
  let cardConfigService = $state<ICardConfigurationService | null>(null);
  let turnIntensityService = $state<ITurnIntensityManagerService | null>(null);

  // State
  let headerFontSize = $state("9px");

  // Derived values - now safe because services are reactive $state
  let currentLevel = $derived(levelService?.numberToDifficulty(config.level) ?? null);
  let allowedIntensityValues = $derived(
    currentLevel && turnIntensityService
      ? turnIntensityService.getAllowedValuesForLevel(currentLevel)
      : []
  );

  // Initialize services
  onMount(() => {
    levelService = resolve<ILevelConversionService>(TYPES.ILevelConversionService);
    typographyService = resolve<IResponsiveTypographyService>(TYPES.IResponsiveTypographyService);
    cardConfigService = resolve<ICardConfigurationService>(TYPES.ICardConfigurationService);
    turnIntensityService = resolve<ITurnIntensityManagerService>(TYPES.ITurnIntensityManagerService);

    updateFontSize();
    window.addEventListener("resize", updateFontSize);

    return () => window.removeEventListener("resize", updateFontSize);
  });

  function updateFontSize() {
    if (!typographyService) return;
    // Desktop gets larger header text (11-18px) for better readability
    // Mobile/tablet stays at (9-14px)
    const isDesktop = window.innerWidth >= 1280;
    headerFontSize = isDesktop
      ? typographyService.calculateResponsiveFontSize(11, 18, 1.2)
      : typographyService.calculateResponsiveFontSize(9, 14, 1.2);
  }

  // Event handlers - safe because we check levelService exists
  function handleLevelChange(level: any) {
    if (!levelService) return;
    updateConfig({ level: levelService.difficultyToNumber(level) });
  }

  function handleLengthChange(length: number) {
    updateConfig({ length });
  }

  function handleTurnIntensityChange(turnIntensity: number) {
    updateConfig({ turnIntensity });
  }

  function handlePropContinuityChange(propContinuity: string) {
    updateConfig({ propContinuity });
  }

  function handleGridModeChange(gridMode: any) {
    updateConfig({ gridMode });
  }

  function handleGenerationModeChange(mode: any) {
    updateConfig({ mode });
  }

  function handleCAPTypeChange(capType: any) {
    updateConfig({ capType });
  }

  function handleSliceSizeChange(sliceSize: any) {
    updateConfig({ sliceSize });
  }

  // Build cards using service - reactive to all dependencies
  let cards = $derived.by((): CardDescriptor[] => {
    if (!cardConfigService || !currentLevel) return [];

    return cardConfigService.buildCardDescriptors(
      config,
      currentLevel,
      isFreeformMode,
      {
        handleLevelChange,
        handleLengthChange,
        handleTurnIntensityChange,
        handlePropContinuityChange,
        handleGridModeChange,
        handleGenerationModeChange,
        handleCAPTypeChange,
        handleSliceSizeChange,
        handleGenerateClick: onGenerateClicked
      },
      headerFontSize,
      allowedIntensityValues,
      isGenerating
    );
  });
</script>

<div class="card-settings-container">
  {#each cards as card (card.id)}
    <div
      class="card-wrapper"
      style:grid-column="span {card.gridColumnSpan}"
      animate:flip={{ duration: 300, easing: quintOut }}
      in:scale={{ start: 0.95, duration: 300, easing: quintOut }}
      out:scale={{ start: 0.95, duration: 250, easing: quintOut }}
    >
      <!-- Props are dynamically typed by CardConfigurationService - type assertion needed -->
      {#if card.id === 'level'}
        <LevelCard {...(card.props as any)} />
      {:else if card.id === 'length'}
        <LengthCard {...(card.props as any)} />
      {:else if card.id === 'generation-mode'}
        <GenerationModeCard {...(card.props as any)} />
      {:else if card.id === 'grid-mode'}
        <GridModeCard {...(card.props as any)} />
      {:else if card.id === 'prop-continuity'}
        <PropContinuityCard {...(card.props as any)} />
      {:else if card.id === 'slice-size'}
        <SliceSizeCard {...(card.props as any)} />
      {:else if card.id === 'turn-intensity'}
        <TurnIntensityCard {...(card.props as any)} />
      {:else if card.id === 'cap-type'}
        <CAPCard {...(card.props as any)} />
      {:else if card.id === 'generate-button'}
        <GenerateButtonCard {...(card.props as any)} />
      {/if}
    </div>
  {/each}
</div>

<style>
  .card-settings-container {
    /* No position property - allows modals to escape and position relative to tool-panel */
    container-type: size; /* Enable both inline and block size container queries */
    container-name: settings-grid; /* Name the container for explicit targeting */
    flex: 1 1 auto; /* Grow to fill available space, allow shrink, auto basis */
    display: grid;

    /* Use programmatic element spacing from parent */
    gap: var(--element-spacing);

    min-height: 0; /* Allow flex to shrink */
    overflow: visible; /* Allow modals to escape, grid won't overflow with pure fr units */

    /* MOBILE APPROACH: Flexible heights that adapt to available space */
    /* 6-subcolumn grid for flexible last-row spanning
       - Normal cards span 2 subcolumns (2/6 = 1/3 width)
       - 1 card in last row spans 6 subcolumns (full width)
       - 2 cards in last row each span 3 subcolumns (half width each)
    */
    grid-template-columns: repeat(6, minmax(0, 1fr));
    grid-auto-rows: 1fr; /* Pure fr units - rows divide space equally, NO minimums */
    grid-auto-flow: row;
    align-content: stretch; /* Stretch to fill available vertical space */
  }

  .card-wrapper {
    display: flex;
    flex-direction: column;
    min-height: 0;
    min-width: 0;
    transition: grid-column 350ms ease;
  }

  .card-wrapper > :global(*) {
    flex: 1;
    min-height: 0;
    min-width: 0;
  }

  /* Container query for medium-width containers (tablets, landscape phones) */
  @container (min-width: 400px) {
    .card-settings-container {
      grid-template-columns: repeat(4, minmax(0, 1fr)); /* 4 subcolumns for 2-column layout */
      grid-auto-rows: 1fr; /* Pure fr units - equal height rows */
      /* Use programmatic element spacing */
      gap: var(--element-spacing);
    }
  }

  /* Container query for wide containers (desktop side-by-side) */
  /* Use width query - height is guaranteed by parent flex layout */
  @container (min-width: 600px) {
    .card-settings-container {
      /* DESKTOP APPROACH: Flexible heights that fill space */
      grid-template-columns: repeat(6, minmax(0, 1fr)); /* Back to 6 subcolumns for 3-column layout */
      grid-auto-rows: 1fr; /* Pure fr units - equal height rows */
      /* Use programmatic element spacing */
      gap: var(--element-spacing);
    }
  }

  /* Desktop optimization: Let cards breathe and use full available space */
  /* Standard desktop (1280px+): Cards share space equally */
  @media (min-width: 1280px) {
    .card-settings-container {
      /* Equal row heights - cards share space proportionally */
      grid-auto-rows: 1fr;

      /* Let cards use the full space available */
      /* No max-height constraint */

      /* Moderate spacing */
      gap: calc(var(--element-spacing) * 0.75);

      /* Fill all available space */
      align-content: stretch;
    }
  }

  /* Large desktop (1600px+): Same approach with tighter gaps */
  @media (min-width: 1600px) {
    .card-settings-container {
      grid-auto-rows: 1fr;
      gap: calc(var(--element-spacing) * 0.7);
    }
  }

  /* Ultra-wide desktop (1920px+): Keep 6-column layout, just tighter spacing */
  @media (min-width: 1920px) {
    .card-settings-container {
      /* Keep 6 columns - don't change to 8! */
      grid-template-columns: repeat(6, minmax(0, 1fr));
      grid-auto-rows: 1fr;
      gap: calc(var(--element-spacing) * 0.6);
    }
  }

  /* Accessibility: Respect reduced motion preference */
  @media (prefers-reduced-motion: reduce) {
    .card-wrapper {
      transition: none;
    }
  }
</style>
