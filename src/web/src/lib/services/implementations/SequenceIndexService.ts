/**
 * Sequence Index Service Implementation
 *
 * Handles loading, building, and searching sequence indices for fast browse operations.
 * Provides search capabilities across sequence metadata.
 */

import type {
  BrowseSequenceMetadata,
  ISequenceIndexService,
} from "$lib/services/interfaces";

interface SearchIndex {
  wordIndex: Map<string, Set<string>>; // word -> sequence IDs
  authorIndex: Map<string, Set<string>>; // author -> sequence IDs
  tagIndex: Map<string, Set<string>>; // tag -> sequence IDs
  metadataIndex: Map<string, Set<string>>; // combined metadata -> sequence IDs
}

export class SequenceIndexService implements ISequenceIndexService {
  private sequenceIndex: BrowseSequenceMetadata[] | null = null;
  private searchIndex: SearchIndex | null = null;
  private sequenceMap = new Map<string, BrowseSequenceMetadata>();

  async loadSequenceIndex(): Promise<BrowseSequenceMetadata[]> {
    if (this.sequenceIndex !== null) {
      return this.sequenceIndex;
    }

    try {
      // Load sequences if not already loaded
      if (this.sequenceIndex === null) {
        this.sequenceIndex = await this.scanSequenceDirectory();
      }

      // Build search index
      if (this.sequenceIndex) {
        await this.buildSearchIndex(this.sequenceIndex);
      }

      return this.sequenceIndex || [];
    } catch (error) {
      console.error("Failed to load sequence index:", error);
      // Return empty array as fallback
      this.sequenceIndex = [];
      return [];
    }
  }

  async buildSearchIndex(sequences: BrowseSequenceMetadata[]): Promise<void> {
    this.searchIndex = {
      wordIndex: new Map(),
      authorIndex: new Map(),
      tagIndex: new Map(),
      metadataIndex: new Map(),
    };

    this.sequenceMap.clear();

    for (const sequence of sequences) {
      this.sequenceMap.set(sequence.id, sequence);

      // Index by word/name
      this.addToIndex(
        this.searchIndex.wordIndex,
        sequence.word.toLowerCase(),
        sequence.id,
      );
      this.addToIndex(
        this.searchIndex.wordIndex,
        sequence.name.toLowerCase(),
        sequence.id,
      );

      // Index by author
      if (sequence.author) {
        this.addToIndex(
          this.searchIndex.authorIndex,
          sequence.author.toLowerCase(),
          sequence.id,
        );
      }

      // Index by tags
      for (const tag of sequence.tags) {
        this.addToIndex(
          this.searchIndex.tagIndex,
          tag.toLowerCase(),
          sequence.id,
        );
      }

      // Index by metadata (combined searchable text)
      const searchableText = this.buildSearchableText(sequence);
      for (const term of searchableText.split(/\s+/)) {
        if (term.length > 2) {
          // Only index terms longer than 2 characters
          this.addToIndex(
            this.searchIndex.metadataIndex,
            term.toLowerCase(),
            sequence.id,
          );
        }
      }
    }
  }

  async searchSequences(query: string): Promise<BrowseSequenceMetadata[]> {
    if (!this.searchIndex || !query.trim()) {
      return this.sequenceIndex || [];
    }

    const searchTerms = query
      .toLowerCase()
      .split(/\s+/)
      .filter((term) => term.length > 0);
    const resultIds = new Set<string>();

    for (const term of searchTerms) {
      const matchingIds = this.searchTerm(term);

      // For multiple terms, use intersection (AND logic)
      if (resultIds.size === 0) {
        matchingIds.forEach((id) => resultIds.add(id));
      } else {
        const currentIds = new Set(resultIds);
        resultIds.clear();
        matchingIds.forEach((id) => {
          if (currentIds.has(id)) {
            resultIds.add(id);
          }
        });
      }
    }

    // Convert IDs back to sequences and sort by relevance
    const results = Array.from(resultIds)
      .map((id) => this.sequenceMap.get(id))
      .filter((seq): seq is BrowseSequenceMetadata => seq !== undefined);

    return this.sortByRelevance(results, query);
  }

  async refreshIndex(): Promise<void> {
    this.sequenceIndex = null;
    this.searchIndex = null;
    this.sequenceMap.clear();
    await this.loadSequenceIndex();
  }

  // Additional utility methods
  getIndexStats(): {
    totalSequences: number;
    indexedWords: number;
    indexedAuthors: number;
    indexedTags: number;
    indexedMetadata: number;
  } {
    return {
      totalSequences: this.sequenceMap.size,
      indexedWords: this.searchIndex?.wordIndex.size || 0,
      indexedAuthors: this.searchIndex?.authorIndex.size || 0,
      indexedTags: this.searchIndex?.tagIndex.size || 0,
      indexedMetadata: this.searchIndex?.metadataIndex.size || 0,
    };
  }

  async getSequenceById(id: string): Promise<BrowseSequenceMetadata | null> {
    if (!this.sequenceMap.has(id)) {
      await this.loadSequenceIndex();
    }
    return this.sequenceMap.get(id) || null;
  }

  async getSuggestions(
    partialQuery: string,
    maxSuggestions = 10,
  ): Promise<string[]> {
    if (!this.searchIndex || partialQuery.length < 2) {
      return [];
    }

    const suggestions = new Set<string>();
    const query = partialQuery.toLowerCase();

    // Search in words/names
    for (const [word] of this.searchIndex.wordIndex) {
      if (word.includes(query)) {
        suggestions.add(word);
        if (suggestions.size >= maxSuggestions) break;
      }
    }

    // Search in authors if not enough suggestions
    if (suggestions.size < maxSuggestions) {
      for (const [author] of this.searchIndex.authorIndex) {
        if (author.includes(query)) {
          suggestions.add(author);
          if (suggestions.size >= maxSuggestions) break;
        }
      }
    }

    return Array.from(suggestions).slice(0, maxSuggestions);
  }

  // Private helper methods
  private addToIndex(
    index: Map<string, Set<string>>,
    key: string,
    sequenceId: string,
  ): void {
    if (!index.has(key)) {
      index.set(key, new Set());
    }
    const keySet = index.get(key);
    if (keySet) {
      keySet.add(sequenceId);
    }
  }

  private searchTerm(term: string): Set<string> {
    const results = new Set<string>();

    if (!this.searchIndex) return results;

    // Exact matches in words
    const wordMatches = this.searchIndex.wordIndex.get(term) || new Set();
    wordMatches.forEach((id) => results.add(id));

    // Partial matches in words
    for (const [word, ids] of this.searchIndex.wordIndex) {
      if (word.includes(term)) {
        ids.forEach((id) => results.add(id));
      }
    }

    // Author matches
    const authorMatches = this.searchIndex.authorIndex.get(term) || new Set();
    authorMatches.forEach((id) => results.add(id));

    // Tag matches
    const tagMatches = this.searchIndex.tagIndex.get(term) || new Set();
    tagMatches.forEach((id) => results.add(id));

    // Metadata matches
    const metadataMatches =
      this.searchIndex.metadataIndex.get(term) || new Set();
    metadataMatches.forEach((id) => results.add(id));

    return results;
  }

  private buildSearchableText(sequence: BrowseSequenceMetadata): string {
    const parts = [
      sequence.word,
      sequence.name,
      sequence.author || "",
      sequence.difficultyLevel || "",
      sequence.gridMode || "",
      sequence.propType || "",
      ...sequence.tags,
    ];

    return parts.filter(Boolean).join(" ");
  }

  private sortByRelevance(
    sequences: BrowseSequenceMetadata[],
    query: string,
  ): BrowseSequenceMetadata[] {
    const queryLower = query.toLowerCase();

    return sequences.sort((a, b) => {
      const scoreA = this.calculateRelevanceScore(a, queryLower);
      const scoreB = this.calculateRelevanceScore(b, queryLower);
      return scoreB - scoreA; // Higher score first
    });
  }

  private calculateRelevanceScore(
    sequence: BrowseSequenceMetadata,
    query: string,
  ): number {
    let score = 0;

    // Exact word match gets highest score
    if (sequence.word.toLowerCase() === query) {
      score += 100;
    }

    // Word starts with query
    if (sequence.word.toLowerCase().startsWith(query)) {
      score += 50;
    }

    // Word contains query
    if (sequence.word.toLowerCase().includes(query)) {
      score += 25;
    }

    // Name matches
    if (sequence.name.toLowerCase().includes(query)) {
      score += 15;
    }

    // Author matches
    if (sequence.author?.toLowerCase().includes(query)) {
      score += 10;
    }

    // Tag matches
    for (const tag of sequence.tags) {
      if (tag.toLowerCase().includes(query)) {
        score += 5;
      }
    }

    // Favorites get bonus points
    if (sequence.isFavorite) {
      score += 2;
    }

    return score;
  }

  private async scanSequenceDirectory(): Promise<BrowseSequenceMetadata[]> {
    // This is a fallback method that would scan the static directory
    // In a real implementation, this would require server-side support
    // For now, return a comprehensive set of sample data based on the copied files

    console.warn("Scanning directory - using fallback sample data");

    // Generate sequences based on common pattern from the copied dictionary
    const sequences: BrowseSequenceMetadata[] = [];

    // Sample sequences that should exist based on the dictionary copy
    const knownSequences = [
      "A",
      "AABB",
      "AAKE",
      "AB",
      "ABC",
      "AJEΦ-",
      "AKE",
      "AKIΦ",
      "ALFALGGF",
      "B",
      "BA",
      "BBKE",
      "BBLF",
      "BC",
      "BJEA",
      "BJFA",
      "BKEΦ-",
      "C",
      "CAKE",
      "CCCΦ-",
      "CCKE",
      "CCKΦ",
      // Add more as needed...
    ];

    for (let i = 0; i < knownSequences.length; i++) {
      const word = knownSequences[i];
      if (!word) continue; // Skip undefined entries

      const authors = ["TKA User", "Demo Author", "Expert User"];
      const gridModes = ["diamond", "box"];
      const difficulties = ["beginner", "intermediate", "advanced"];

      const author = authors[i % authors.length];
      const gridMode = gridModes[i % gridModes.length];
      const difficulty = difficulties[i % difficulties.length];

      const result: BrowseSequenceMetadata = {
        id: word.toLowerCase().replace(/[^a-z0-9]/g, "_"),
        name: `${word} Sequence`,
        word,
        thumbnails: [`${word}_ver1.png`],
        isFavorite: Math.random() > 0.8,
        isCircular: false,
        tags: ["flow", "practice", "generated"].slice(
          0,
          Math.floor(Math.random() * 3) + 1,
        ),
        metadata: { scanned: true, index: i },
      };

      // Add optional properties conditionally
      if (author) result.author = author;
      if (gridMode) result.gridMode = gridMode;
      if (difficulty) result.difficultyLevel = difficulty;

      result.sequenceLength = Math.floor(Math.random() * 8) + 3;
      result.level = Math.floor(Math.random() * 4) + 1;
      result.dateAdded = new Date(
        Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000,
      );
      result.propType = "fans";
      result.startingPosition = "center";

      sequences.push(result);
    }

    return sequences;
  }
}
