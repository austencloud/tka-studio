/**
 * Codex Service Implementation
 *
 * Handles codex data operations with specific pictograph mapping like the desktop app.
 * Only loads the specific pictographs defined in the codex mapping (39 letters).
 */

import { GridMode } from "$lib/domain";
import type { PictographData } from "$lib/domain/PictographData";
import {
  CsvDataService,
  type ParsedCsvRow,
} from "../implementations/CsvDataService";
import { OptionDataService } from "../implementations/OptionDataService";
import type { ICodexService } from "./ICodexService";

// Codex letter mapping (from desktop app's CodexDataService)
const CODEX_LETTER_MAPPING = {
  // A-Z Basic letters
  A: {
    startPos: "alpha1",
    endPos: "alpha3",
    blueMotion: "pro",
    redMotion: "pro",
  },
  B: {
    startPos: "alpha1",
    endPos: "alpha3",
    blueMotion: "anti",
    redMotion: "anti",
  },
  C: {
    startPos: "alpha1",
    endPos: "alpha3",
    blueMotion: "anti",
    redMotion: "pro",
  },
  D: {
    startPos: "beta1",
    endPos: "alpha3",
    blueMotion: "pro",
    redMotion: "pro",
  },
  E: {
    startPos: "beta1",
    endPos: "alpha3",
    blueMotion: "anti",
    redMotion: "anti",
  },
  F: {
    startPos: "beta1",
    endPos: "alpha3",
    blueMotion: "anti",
    redMotion: "pro",
  },
  G: {
    startPos: "beta3",
    endPos: "beta5",
    blueMotion: "pro",
    redMotion: "pro",
  },
  H: {
    startPos: "beta3",
    endPos: "beta5",
    blueMotion: "anti",
    redMotion: "anti",
  },
  I: {
    startPos: "beta3",
    endPos: "beta5",
    blueMotion: "anti",
    redMotion: "pro",
  },
  J: {
    startPos: "alpha3",
    endPos: "beta5",
    blueMotion: "pro",
    redMotion: "pro",
  },
  K: {
    startPos: "alpha3",
    endPos: "beta5",
    blueMotion: "anti",
    redMotion: "anti",
  },
  L: {
    startPos: "alpha3",
    endPos: "beta5",
    blueMotion: "anti",
    redMotion: "pro",
  },
  M: {
    startPos: "gamma11",
    endPos: "gamma1",
    blueMotion: "pro",
    redMotion: "pro",
  },
  N: {
    startPos: "gamma11",
    endPos: "gamma1",
    blueMotion: "anti",
    redMotion: "anti",
  },
  O: {
    startPos: "gamma11",
    endPos: "gamma1",
    blueMotion: "anti",
    redMotion: "pro",
  },
  P: {
    startPos: "gamma1",
    endPos: "gamma15",
    blueMotion: "pro",
    redMotion: "pro",
  },
  Q: {
    startPos: "gamma1",
    endPos: "gamma15",
    blueMotion: "anti",
    redMotion: "anti",
  },
  R: {
    startPos: "gamma1",
    endPos: "gamma15",
    blueMotion: "anti",
    redMotion: "pro",
  },
  S: {
    startPos: "gamma13",
    endPos: "gamma11",
    blueMotion: "pro",
    redMotion: "pro",
  },
  T: {
    startPos: "gamma13",
    endPos: "gamma11",
    blueMotion: "anti",
    redMotion: "anti",
  },
  U: {
    startPos: "gamma13",
    endPos: "gamma11",
    blueMotion: "anti",
    redMotion: "pro",
  },
  V: {
    startPos: "gamma13",
    endPos: "gamma11",
    blueMotion: "pro",
    redMotion: "anti",
  },
  W: {
    startPos: "gamma13",
    endPos: "alpha3",
    blueMotion: "static",
    redMotion: "pro",
  },
  X: {
    startPos: "gamma13",
    endPos: "alpha3",
    blueMotion: "static",
    redMotion: "anti",
  },
  Y: {
    startPos: "gamma11",
    endPos: "beta5",
    blueMotion: "static",
    redMotion: "pro",
  },
  Z: {
    startPos: "gamma11",
    endPos: "beta5",
    blueMotion: "static",
    redMotion: "anti",
  },

  // Greek letters
  Σ: {
    startPos: "alpha3",
    endPos: "gamma13",
    blueMotion: "static",
    redMotion: "pro",
  },
  Δ: {
    startPos: "alpha3",
    endPos: "gamma13",
    blueMotion: "static",
    redMotion: "anti",
  },
  θ: {
    startPos: "beta5",
    endPos: "gamma11",
    blueMotion: "static",
    redMotion: "pro",
  },
  Ω: {
    startPos: "beta5",
    endPos: "gamma11",
    blueMotion: "static",
    redMotion: "anti",
  },

  // Dash variants
  "W-": {
    startPos: "gamma5",
    endPos: "alpha3",
    blueMotion: "dash",
    redMotion: "pro",
  },
  "X-": {
    startPos: "gamma5",
    endPos: "alpha3",
    blueMotion: "dash",
    redMotion: "anti",
  },
  "Y-": {
    startPos: "gamma3",
    endPos: "beta5",
    blueMotion: "dash",
    redMotion: "pro",
  },
  "Z-": {
    startPos: "gamma3",
    endPos: "beta5",
    blueMotion: "dash",
    redMotion: "anti",
  },
  "Σ-": {
    startPos: "beta3",
    endPos: "gamma13",
    blueMotion: "dash",
    redMotion: "pro",
  },
  "Δ-": {
    startPos: "beta3",
    endPos: "gamma13",
    blueMotion: "dash",
    redMotion: "anti",
  },
  "θ-": {
    startPos: "alpha5",
    endPos: "gamma11",
    blueMotion: "dash",
    redMotion: "pro",
  },
  "Ω-": {
    startPos: "alpha5",
    endPos: "gamma11",
    blueMotion: "dash",
    redMotion: "anti",
  },

  // Special letters (Type 4 - Dash)
  Φ: {
    startPos: "beta7",
    endPos: "alpha3",
    blueMotion: "static",
    redMotion: "dash",
  },
  Ψ: {
    startPos: "alpha1",
    endPos: "beta5",
    blueMotion: "static",
    redMotion: "dash",
  },
  Λ: {
    startPos: "gamma7",
    endPos: "gamma11",
    blueMotion: "static",
    redMotion: "dash",
  },

  // Type 5 - Dual-Dash letters
  "Φ-": {
    startPos: "alpha3",
    endPos: "alpha7",
    blueMotion: "dash",
    redMotion: "dash",
  },
  "Ψ-": {
    startPos: "beta1",
    endPos: "beta5",
    blueMotion: "dash",
    redMotion: "dash",
  },
  "Λ-": {
    startPos: "gamma15",
    endPos: "gamma11",
    blueMotion: "dash",
    redMotion: "dash",
  },

  // Type 6 - Static letters
  α: {
    startPos: "alpha3",
    endPos: "alpha3",
    blueMotion: "static",
    redMotion: "static",
  },
  β: {
    startPos: "beta5",
    endPos: "beta5",
    blueMotion: "static",
    redMotion: "static",
  },
  Γ: {
    startPos: "gamma11",
    endPos: "gamma11",
    blueMotion: "static",
    redMotion: "static",
  },
} as const;

export class CodexService implements ICodexService {
  private csvDataService: CsvDataService;
  private optionDataService: OptionDataService;
  private initialized = false;
  private codexPictographs: PictographData[] = [];

  // Letter organization by rows (matches desktop ROWS structure)
  private readonly LETTER_ROWS = [
    ["A", "B", "C", "D", "E", "F"],
    ["G", "H", "I", "J", "K", "L"],
    ["M", "N", "O", "P", "Q", "R"],
    ["S", "T", "U", "V"],
    ["W", "X", "Y", "Z"],
    ["Σ", "Δ", "θ", "Ω"],
    ["W-", "X-", "Y-", "Z-"],
    ["Σ-", "Δ-", "θ-", "Ω-"],
    ["Φ", "Ψ", "Λ"],
    ["Φ-", "Ψ-", "Λ-"],
    ["α", "β", "Γ"],
  ];

  constructor() {
    this.csvDataService = new CsvDataService();
    this.optionDataService = new OptionDataService();
    console.log(
      "🔧 CodexService initialized with specific letter mapping and desktop functionality",
    );
  }

  /**
   * Load all pictographs in alphabetical order
   */
  async loadAllPictographs(): Promise<PictographData[]> {
    if (!this.initialized) {
      await this.initializePictographs();
    }

    return [...this.codexPictographs].sort((a, b) => {
      const letterA = a.letter || "";
      const letterB = b.letter || "";
      return letterA.localeCompare(letterB);
    });
  }

  /**
   * Search pictographs by letter or pattern
   */
  async searchPictographs(searchTerm: string): Promise<PictographData[]> {
    const allPictographs = await this.loadAllPictographs();

    if (!searchTerm.trim()) {
      return allPictographs;
    }

    const term = searchTerm.toLowerCase();

    return allPictographs.filter((pictograph) => {
      const letter = pictograph.letter?.toLowerCase() || "";
      const id = pictograph.id?.toLowerCase() || "";

      return (
        letter.includes(term) || id.includes(term) || letter.startsWith(term)
      );
    });
  }

  /**
   * Get a specific pictograph by letter
   */
  async getPictographByLetter(letter: string): Promise<PictographData | null> {
    const allPictographs = await this.loadAllPictographs();

    return (
      allPictographs.find(
        (pictograph) =>
          pictograph.letter?.toLowerCase() === letter.toLowerCase(),
      ) || null
    );
  }

  /**
   * Get pictographs for a specific lesson type
   */
  async getPictographsForLesson(lessonType: string): Promise<PictographData[]> {
    const allPictographs = await this.loadAllPictographs();

    // For now, return all pictographs
    // This could be filtered based on lesson requirements in the future
    console.log(`📚 Getting pictographs for lesson type: ${lessonType}`);
    return allPictographs;
  }

  /**
   * Initialize pictographs from CSV data using codex mapping
   */
  private async initializePictographs(): Promise<void> {
    try {
      console.log("🚀 Starting CodexService initialization...");

      // Load real CSV data using existing infrastructure
      await this.csvDataService.loadCsvData();
      console.log("📄 CSV data loaded in CodexService");

      // Get specific pictographs only from diamond mode (like desktop app)
      this.codexPictographs = this.getCodexPictographsForGridMode(
        GridMode.DIAMOND,
      );

      this.initialized = true;
      console.log(
        `✅ CodexService initialized with ${this.codexPictographs.length} diamond pictographs from mapping`,
      );
    } catch (error) {
      console.error("❌ Failed to initialize CodexService:", error);
      this.initialized = false;
    }
  }

  /**
   * Get codex pictographs for a specific grid mode using the letter mapping
   */
  private getCodexPictographsForGridMode(gridMode: GridMode): PictographData[] {
    console.log(`🔍 Getting codex pictographs for ${gridMode} mode...`);
    const csvRows = this.csvDataService.getParsedData(gridMode);
    console.log(
      `📊 Found ${csvRows.length} total CSV rows for ${gridMode} mode`,
    );

    const codexPictographs: PictographData[] = [];

    // For each letter in our codex mapping, find matching CSV row
    Object.entries(CODEX_LETTER_MAPPING).forEach(([letter, mapping]) => {
      console.log(`🔤 Looking for letter "${letter}" with mapping:`, mapping);

      const matchingRow = csvRows.find(
        (row) =>
          row.letter === letter &&
          row.startPos === mapping.startPos &&
          row.endPos === mapping.endPos &&
          row.blueMotionType === mapping.blueMotion &&
          row.redMotionType === mapping.redMotion,
      );

      if (matchingRow) {
        console.log(
          `✅ Found matching row for letter "${letter}":`,
          matchingRow,
        );
        const pictograph = this.convertCsvRowToPictographData(
          matchingRow,
          gridMode,
          codexPictographs.length, // Use codex index for unique IDs
        );
        if (pictograph) {
          codexPictographs.push(pictograph);
          console.log(
            `📊 Added pictograph for letter "${letter}":`,
            pictograph.id,
          );
        } else {
          console.warn(
            `⚠️ Failed to convert CSV row to pictograph for letter "${letter}"`,
          );
        }
      } else {
        console.warn(
          `⚠️ No CSV data found for codex letter ${letter} in ${gridMode} mode`,
        );
        // Log what we're looking for vs what's available
        const letterRows = csvRows.filter((row) => row.letter === letter);
        console.log(
          `Available rows for letter "${letter}":`,
          letterRows.length > 0 ? letterRows.slice(0, 3) : "none",
        );
      }
    });

    console.log(`🎯 Total codex pictographs found: ${codexPictographs.length}`);
    return codexPictographs;
  }

  /**
   * Convert CSV row to PictographData using existing infrastructure
   */
  private convertCsvRowToPictographData(
    row: ParsedCsvRow,
    gridMode: GridMode,
    index: number,
  ): PictographData | null {
    try {
      // Use the public conversion method from OptionDataService
      return this.optionDataService.convertCsvRowToPictographData(
        row,
        gridMode,
        index,
      );
    } catch (error) {
      console.error(
        "❌ Error converting CSV row to PictographData:",
        error,
        row,
      );
      return null;
    }
  }

  /**
   * Get letters organized by rows for grid display (matches desktop layout)
   */
  getLettersByRow(): string[][] {
    return [...this.LETTER_ROWS]; // Return a copy to prevent mutation
  }

  /**
   * Apply rotate operation to all pictographs
   */
  async rotateAllPictographs(
    pictographs: PictographData[],
  ): Promise<PictographData[]> {
    // For now, return unchanged pictographs
    // In a full implementation, this would apply rotation transformations
    console.log(
      "🔄 Rotate operation applied to",
      pictographs.length,
      "pictographs",
    );
    return [...pictographs];
  }

  /**
   * Apply mirror operation to all pictographs
   */
  async mirrorAllPictographs(
    pictographs: PictographData[],
  ): Promise<PictographData[]> {
    // For now, return unchanged pictographs
    // In a full implementation, this would apply mirror transformations
    console.log(
      "🪞 Mirror operation applied to",
      pictographs.length,
      "pictographs",
    );
    return [...pictographs];
  }

  /**
   * Apply color swap operation to all pictographs
   */
  async colorSwapAllPictographs(
    pictographs: PictographData[],
  ): Promise<PictographData[]> {
    // For now, return unchanged pictographs
    // In a full implementation, this would swap red and blue motion types
    console.log(
      "⚫⚪ Color swap operation applied to",
      pictographs.length,
      "pictographs",
    );
    return [...pictographs];
  }

  /**
   * Get all pictograph data organized by letter
   */
  async getAllPictographData(): Promise<Record<string, PictographData | null>> {
    const allPictographs = await this.loadAllPictographs();
    const result: Record<string, PictographData | null> = {};

    // Initialize all letters from LETTER_ROWS to null
    this.LETTER_ROWS.flat().forEach((letter) => {
      result[letter] = null;
    });

    // Fill in the pictographs we have
    allPictographs.forEach((pictograph) => {
      if (pictograph.letter) {
        result[pictograph.letter] = pictograph;
      }
    });

    return result;
  }
}
