import type { BrowseState } from "$lib/state/browse-state.svelte";

/**
 * Navigation-specific event handlers for the Browse tab
 * Handles navigation sidebar interactions and filtering
 */
export function createNavigationEventHandlers(
  browseState: BrowseState,
  setPanelIndex: (index: number) => void,
  toggleNavigationCollapsed: () => void,
) {
  // Navigation sidebar handlers
  function handleNavigationSectionToggle(sectionId: string) {
    browseState.toggleNavigationSection(sectionId);
  }

  async function handleNavigationItemClick(sectionId: string, itemId: string) {
    browseState.setActiveNavigationItem(sectionId, itemId);

    // Apply filter based on navigation selection
    try {
      const navigationSections = browseState.navigationSections;
      const activeSection = navigationSections.find(
        (section) => section.id === sectionId,
      );
      const activeItem = activeSection?.items.find(
        (item) => item.id === itemId,
      );

      if (activeSection && activeItem) {
        // Use NavigationService to filter sequences
        const filteredSequences = await browseState.filterSequencesByNavigation(
          activeSection.type,
          activeItem,
        );

        // Switch to browser panel to show results
        if (filteredSequences.length > 0) {
          setPanelIndex(1);
          console.log(
            `🧭 Navigation filter applied: ${activeSection.title} > ${activeItem.label} (${filteredSequences.length} sequences)`,
          );
        } else {
          console.warn(
            `No sequences found for navigation filter: ${activeSection.title} > ${activeItem.label}`,
          );
        }
      }
    } catch (error) {
      console.error("Failed to apply navigation filter:", error);
    }
  }

  // Navigation collapse handlers
  function handleToggleNavigationCollapse() {
    // The collapse state is managed in the parent component, not in browseState
    // We just call the callback to toggle it
    toggleNavigationCollapsed();
  }

  return {
    handleNavigationSectionToggle,
    handleNavigationItemClick,
    handleToggleNavigationCollapse,
  };
}
