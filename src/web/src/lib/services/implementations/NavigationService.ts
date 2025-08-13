/**
 * Navigation Service - Manages browse tab navigation
 *
 * Handles sidebar navigation sections, organization, and state management
 * following the microservices architecture pattern.
 */

import type { BrowseSequenceMetadata } from "../interfaces";

export interface NavigationSection {
  id: string;
  title: string;
  type: "date" | "length" | "letter" | "level" | "author" | "favorites";
  items: NavigationItem[];
  isExpanded: boolean;
  totalCount: number;
}

export interface NavigationItem {
  id: string;
  label: string;
  value: string | number;
  count: number;
  isActive: boolean;
}

export interface INavigationService {
  /** Generate navigation sections from sequences */
  generateNavigationSections(
    sequences: BrowseSequenceMetadata[],
    favorites: string[],
  ): Promise<NavigationSection[]>;

  /** Toggle section expansion state */
  toggleSectionExpansion(
    sectionId: string,
    sections: NavigationSection[],
  ): NavigationSection[];

  /** Set active navigation item */
  setActiveItem(
    sectionId: string,
    itemId: string,
    sections: NavigationSection[],
  ): NavigationSection[];

  /** Clear all active states */
  clearActiveStates(sections: NavigationSection[]): NavigationSection[];

  /** Get sequences for navigation item */
  getSequencesForNavigationItem(
    item: NavigationItem,
    sectionType: NavigationSection["type"],
    allSequences: BrowseSequenceMetadata[],
  ): BrowseSequenceMetadata[];

  /** Update section counts based on current sequences */
  updateSectionCounts(
    sections: NavigationSection[],
    sequences: BrowseSequenceMetadata[],
    favorites: string[],
  ): NavigationSection[];
}

export class NavigationService implements INavigationService {
  async generateNavigationSections(
    sequences: BrowseSequenceMetadata[],
    favorites: string[],
  ): Promise<NavigationSection[]> {
    const sections: NavigationSection[] = [
      await this.generateFavoritesSection(sequences, favorites),
      await this.generateDateSection(sequences),
      await this.generateLengthSection(sequences),
      await this.generateLetterSection(sequences),
      await this.generateLevelSection(sequences),
      await this.generateAuthorSection(sequences),
    ];

    return sections;
  }

  toggleSectionExpansion(
    sectionId: string,
    sections: NavigationSection[],
  ): NavigationSection[] {
    return sections.map((section) => ({
      ...section,
      isExpanded:
        section.id === sectionId ? !section.isExpanded : section.isExpanded,
    }));
  }

  setActiveItem(
    sectionId: string,
    itemId: string,
    sections: NavigationSection[],
  ): NavigationSection[] {
    return sections.map((section) => ({
      ...section,
      items: section.items.map((item) => ({
        ...item,
        isActive: section.id === sectionId && item.id === itemId,
      })),
    }));
  }

  clearActiveStates(sections: NavigationSection[]): NavigationSection[] {
    return sections.map((section) => ({
      ...section,
      items: section.items.map((item) => ({
        ...item,
        isActive: false,
      })),
    }));
  }

  getSequencesForNavigationItem(
    item: NavigationItem,
    sectionType: NavigationSection["type"],
    allSequences: BrowseSequenceMetadata[],
  ): BrowseSequenceMetadata[] {
    switch (sectionType) {
      case "length": {
        const length = parseInt(item.value as string);
        return allSequences.filter((seq) => seq.sequenceLength === length);
      }

      case "letter":
        return allSequences.filter((seq) =>
          seq.word.startsWith(item.value as string),
        );

      case "level":
        return allSequences.filter((seq) => seq.difficultyLevel === item.value);

      case "author":
        return allSequences.filter((seq) => seq.author === item.value);

      case "date":
        // Implementation depends on date format
        return allSequences.filter((seq) => {
          if (!seq.dateAdded) return false;
          const itemDate = new Date(item.value as string);
          const seqDate = new Date(seq.dateAdded);
          return seqDate.toDateString() === itemDate.toDateString();
        });

      case "favorites":
        // Will be handled by favorites filter
        return allSequences;

      default:
        return allSequences;
    }
  }

  updateSectionCounts(
    sections: NavigationSection[],
    sequences: BrowseSequenceMetadata[],
    favorites: string[],
  ): NavigationSection[] {
    return sections.map((section) => ({
      ...section,
      totalCount: this.calculateSectionCount(section, sequences, favorites),
      items: section.items.map((item) => ({
        ...item,
        count: this.getSequencesForNavigationItem(item, section.type, sequences)
          .length,
      })),
    }));
  }

  // Private helper methods
  private async generateFavoritesSection(
    sequences: BrowseSequenceMetadata[],
    favorites: string[],
  ): Promise<NavigationSection> {
    const favoriteSequences = sequences.filter((seq) =>
      favorites.includes(seq.id),
    );

    return {
      id: "favorites",
      title: "⭐ Favorites",
      type: "favorites",
      items: [
        {
          id: "all-favorites",
          label: "All Favorites",
          value: "favorites",
          count: favoriteSequences.length,
          isActive: false,
        },
      ],
      isExpanded: false,
      totalCount: favoriteSequences.length,
    };
  }

  private async generateDateSection(
    sequences: BrowseSequenceMetadata[],
  ): Promise<NavigationSection> {
    const dateGroups = new Map<string, BrowseSequenceMetadata[]>();

    sequences.forEach((seq) => {
      if (seq.dateAdded) {
        const date = new Date(seq.dateAdded);
        const dateKey = date.toDateString();
        if (!dateGroups.has(dateKey)) {
          dateGroups.set(dateKey, []);
        }
        const group = dateGroups.get(dateKey);
        if (group) {
          group.push(seq);
        }
      }
    });

    const items: NavigationItem[] = Array.from(dateGroups.entries())
      .sort(([a], [b]) => new Date(b).getTime() - new Date(a).getTime())
      .slice(0, 10) // Show last 10 dates
      .map(([date, seqs]) => ({
        id: `date-${date}`,
        label: this.formatDateLabel(new Date(date)),
        value: date,
        count: seqs.length,
        isActive: false,
      }));

    return {
      id: "date",
      title: "📅 Recently Added",
      type: "date",
      items,
      isExpanded: false,
      totalCount: sequences.filter((seq) => seq.dateAdded).length,
    };
  }

  private async generateLengthSection(
    sequences: BrowseSequenceMetadata[],
  ): Promise<NavigationSection> {
    const lengthGroups = new Map<number, BrowseSequenceMetadata[]>();

    sequences.forEach((seq) => {
      const length = seq.sequenceLength || seq.word.length;
      if (!lengthGroups.has(length)) {
        lengthGroups.set(length, []);
      }
      const group = lengthGroups.get(length);
      if (group) {
        group.push(seq);
      }
    });

    const items: NavigationItem[] = Array.from(lengthGroups.entries())
      .sort(([a], [b]) => a - b)
      .map(([length, seqs]) => ({
        id: `length-${length}`,
        label: `${length} beats`,
        value: length,
        count: seqs.length,
        isActive: false,
      }));

    return {
      id: "length",
      title: "📏 Length",
      type: "length",
      items,
      isExpanded: false,
      totalCount: sequences.length,
    };
  }

  private async generateLetterSection(
    sequences: BrowseSequenceMetadata[],
  ): Promise<NavigationSection> {
    const letterGroups = new Map<string, BrowseSequenceMetadata[]>();

    sequences.forEach((seq) => {
      const firstLetter = seq.word.charAt(0).toUpperCase();
      if (!letterGroups.has(firstLetter)) {
        letterGroups.set(firstLetter, []);
      }
      const group = letterGroups.get(firstLetter);
      if (group) {
        group.push(seq);
      }
    });

    const items: NavigationItem[] = Array.from(letterGroups.entries())
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([letter, seqs]) => ({
        id: `letter-${letter}`,
        label: letter,
        value: letter,
        count: seqs.length,
        isActive: false,
      }));

    return {
      id: "letter",
      title: "🔤 Starting Letter",
      type: "letter",
      items,
      isExpanded: true, // Default expanded like desktop
      totalCount: sequences.length,
    };
  }

  private async generateLevelSection(
    sequences: BrowseSequenceMetadata[],
  ): Promise<NavigationSection> {
    const levelGroups = new Map<string, BrowseSequenceMetadata[]>();

    sequences.forEach((seq) => {
      const level = seq.difficultyLevel || "unknown";
      if (!levelGroups.has(level)) {
        levelGroups.set(level, []);
      }
      const group = levelGroups.get(level);
      if (group) {
        group.push(seq);
      }
    });

    const levelOrder = ["beginner", "intermediate", "advanced", "unknown"];
    const items: NavigationItem[] = levelOrder
      .filter((level) => levelGroups.has(level))
      .map((level) => ({
        id: `level-${level}`,
        label: level.charAt(0).toUpperCase() + level.slice(1),
        value: level,
        count: levelGroups.get(level)?.length || 0,
        isActive: false,
      }));

    return {
      id: "level",
      title: "📊 Difficulty",
      type: "level",
      items,
      isExpanded: false,
      totalCount: sequences.length,
    };
  }

  private async generateAuthorSection(
    sequences: BrowseSequenceMetadata[],
  ): Promise<NavigationSection> {
    const authorGroups = new Map<string, BrowseSequenceMetadata[]>();

    sequences.forEach((seq) => {
      const author = seq.author || "Unknown";
      if (!authorGroups.has(author)) {
        authorGroups.set(author, []);
      }
      const group = authorGroups.get(author);
      if (group) {
        group.push(seq);
      }
    });

    const items: NavigationItem[] = Array.from(authorGroups.entries())
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([author, seqs]) => ({
        id: `author-${author}`,
        label: author,
        value: author,
        count: seqs.length,
        isActive: false,
      }));

    return {
      id: "author",
      title: "👤 Author",
      type: "author",
      items,
      isExpanded: false,
      totalCount: sequences.length,
    };
  }

  private calculateSectionCount(
    section: NavigationSection,
    sequences: BrowseSequenceMetadata[],
    favorites: string[],
  ): number {
    switch (section.type) {
      case "favorites":
        return sequences.filter((seq) => favorites.includes(seq.id)).length;
      default:
        return sequences.length;
    }
  }

  private formatDateLabel(date: Date): string {
    const now = new Date();
    const diffTime = now.getTime() - date.getTime();
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return "Today";
    if (diffDays === 1) return "Yesterday";
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;

    return date.toLocaleDateString();
  }
}
