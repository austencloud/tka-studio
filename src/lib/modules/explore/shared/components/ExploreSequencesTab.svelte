<script lang="ts">
  import type { SequenceData } from "$shared";
  import { SequenceDisplayPanel } from "../../display/components";
  import ExploreLayout from "./ExploreLayout.svelte";
  import ExploreControls from "./ExploreControls.svelte";
  import SequenceDrawers from "./SequenceDrawers.svelte";
  import { galleryPanelManager } from "../state/gallery-panel-state.svelte";

  interface Props {
    isMobile: boolean;
    isUIVisible: boolean;
    showDesktopSidebar: boolean;
    drawerWidth: string;
    galleryState: any;
    error: string | null;
    onSequenceAction: (action: string, sequence: SequenceData) => Promise<void>;
    onDetailPanelAction: (action: string, sequence: SequenceData) => Promise<void>;
    onCloseDetailPanel: () => void;
    onContainerScroll: (event: CustomEvent<{ scrollTop: number }>) => void;
  }

  let {
    isMobile,
    isUIVisible,
    showDesktopSidebar,
    drawerWidth,
    galleryState,
    error,
    onSequenceAction,
    onDetailPanelAction,
    onCloseDetailPanel,
    onContainerScroll,
  }: Props = $props();
</script>

<ExploreLayout {isUIVisible} hideTopSection={showDesktopSidebar}>
  {#snippet viewPresetsDropdown()}
    <ExploreControls
      {isMobile}
      currentFilter={galleryState.currentFilter}
      currentSortMethod={galleryState.currentSortMethod}
      availableSections={galleryState.availableNavigationSections}
      onFilterChange={galleryState.handleFilterChange}
      onSortMethodChange={(method) => galleryState.handleSortChange(method, "asc")}
      onSectionClick={galleryState.scrollToSection}
    />
  {/snippet}

  {#snippet sortAndJumpDropdown()}
    <!-- This snippet is now handled by ExploreControls -->
  {/snippet}

  {#snippet advancedFilterButton()}
    <!-- This snippet is now handled by ExploreControls -->
  {/snippet}

  {#snippet centerPanel()}
    <div class="sequences-with-detail">
      <div
        class="sequences-main"
        class:panel-open={galleryPanelManager.isDetailOpen && !isMobile}
        style:--drawer-width={drawerWidth}
      >
        <SequenceDisplayPanel
          sequences={galleryState.displayedSequences}
          sections={galleryState.sequenceSections}
          isLoading={galleryState.isLoading}
          {error}
          showSections={galleryState.showSections}
          onAction={onSequenceAction}
          onScroll={onContainerScroll}
        />
      </div>
    </div>
  {/snippet}
</ExploreLayout>

<!-- Drawers -->
<SequenceDrawers
  {isMobile}
  {drawerWidth}
  currentFilter={galleryState.currentFilter}
  currentSortMethod={galleryState.currentSortMethod}
  availableSections={galleryState.availableNavigationSections}
  availableSequenceLengths={galleryState.availableSequenceLengths}
  onFilterChange={galleryState.handleFilterChange}
  onSortMethodChange={(method) => galleryState.handleSortChange(method, "asc")}
  onSectionClick={(sectionId) => {
    galleryState.scrollToSection(sectionId);
    galleryPanelManager.close();
  }}
  {onDetailPanelAction}
  {onCloseDetailPanel}
/>

<style>
  /* Container for sequences grid + detail panel */
  .sequences-with-detail {
    display: flex;
    flex: 1;
    overflow: hidden;
    height: 100%;
    transition: all 0.3s ease;
  }

  /* Main sequences area (grid) */
  .sequences-main {
    flex: 1;
    overflow-y: auto; /* Allow scrolling */
    overflow-x: hidden;
    min-width: 0; /* Allow flexbox shrinking */
    --drawer-width: min(
      600px,
      90vw
    ); /* Default width, overridden by inline style */
    /* Smooth transition - matches sidebar and drawer timing for cohesive animation */
    transition: padding-right 300ms cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* Add padding when panel is open (desktop only) - simple, standard approach */
  .sequences-main.panel-open {
    padding-right: var(--drawer-width);
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .sequences-with-detail,
    .sequences-main {
      transition: none;
    }
  }
</style>
