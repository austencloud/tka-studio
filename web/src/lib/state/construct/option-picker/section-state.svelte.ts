
// Section state management for option picker
export function createSectionState() {
  let currentSection = $state('letters');
  let sections = $state(['letters', 'positions', 'motions']);
  
  return {
    get currentSection() { return currentSection; },
    get sections() { return sections; },
    setSection(section: string) {
      currentSection = section;
    }
  };
}

export type SectionState = ReturnType<typeof createSectionState>;

// Legacy export for compatibility
export const createSectionStateFromFile = createSectionState;
