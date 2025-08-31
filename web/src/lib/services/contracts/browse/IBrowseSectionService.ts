import type {
  SectionConfiguration,
  SequenceData,
  SequenceSection,
} from "$domain";

export interface IBrowseSectionService {
  /** Organize sequences into sections based on configuration */
  organizeSections(
    sequences: SequenceData[],
    config: SectionConfiguration
  ): Promise<SequenceSection[]>;

  /** Toggle section expansion state */
  toggleSectionExpansion(
    sectionId: string,
    sections: SequenceSection[]
  ): SequenceSection[];

  /** Get default section configuration */
  getDefaultSectionConfiguration(): SectionConfiguration;

  /** Update section configuration */
  updateSectionConfiguration(
    config: SectionConfiguration,
    updates: Partial<SectionConfiguration>
  ): SectionConfiguration;

  /** Get section statistics */
  getSectionStatistics(sections: SequenceSection[]): {
    totalSections: number;
    totalSequences: number;
    expandedSections: number;
    averageSequencesPerSection: number;
  };
}
