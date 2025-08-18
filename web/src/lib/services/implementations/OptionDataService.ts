/**
 * Option Data Service - Fixed implementation with proper CSV data loading
 *
 * Bridges legacy option loading logic with web's actual pictograph data from CSV files.
 * No more fake service resolution - loads real data from static files.
 */

import type { PictographData } from "$lib/domain/PictographData";
import type { BeatData } from "$lib/domain/BeatData";
import { createPictographData } from "$lib/domain/PictographData";
import type { GridMode } from "$lib/domain";
import {
  MotionType,
  Location,
  Orientation,
  RotationDirection,
} from "$lib/domain/enums";
import { createMotionData } from "$lib/domain/MotionData";

export interface OptionDataServiceInterface {
  initialize(): Promise<void>;
  getNextOptions(sequence: BeatData[]): Promise<PictographData[]>;
  getNextOptionsFromEndPosition(
    endPosition: string,
    gridMode: GridMode,
    options: Record<string, unknown>
  ): Promise<PictographData[]>;
  filterOptionsByLetterTypes(
    options: PictographData[],
    letterTypes: string[]
  ): PictographData[];
  filterOptionsByRotation(
    options: PictographData[],
    blueRotDir: string,
    redRotDir: string
  ): PictographData[];
}

export class OptionDataService implements OptionDataServiceInterface {
  private pictographCache: PictographData[] | null = null;
  private loadingPromise: Promise<PictographData[]> | null = null;

  /**
   * Initialize the service - loads CSV data
   */
  async initialize(): Promise<void> {
    try {
      if (!this.loadingPromise) {
        this.loadingPromise = this.loadPictographsFromCSV();
      }
      this.pictographCache = await this.loadingPromise;
      console.log(
        `✅ OptionDataService initialized with ${this.pictographCache.length} pictographs`
      );
    } catch (error) {
      console.error("❌ Failed to initialize OptionDataService:", error);
      throw error;
    }
  }

  /**
   * Get next options from end position - compatibility method
   */
  async getNextOptionsFromEndPosition(
    endPosition: string,
    gridMode: GridMode,
    _options: Record<string, unknown>
  ): Promise<PictographData[]> {
    try {
      // Ensure service is initialized
      if (!this.pictographCache) {
        await this.initialize();
      }

      // For now, return all available options
      // TODO: Filter by end position and grid mode
      console.log(
        `🔍 Getting options for end position: ${endPosition}, grid: ${gridMode}`
      );
      return this.pictographCache || [];
    } catch (error) {
      console.error("❌ Failed to get options from end position:", error);
      return this.createFallbackPictographs();
    }
  }

  /**
   * Get next options - loads real pictograph data from CSV files
   */
  async getNextOptions(sequence: BeatData[]): Promise<PictographData[]> {
    try {
      // Load pictographs from CSV if not already cached
      if (!this.pictographCache) {
        if (!this.loadingPromise) {
          this.loadingPromise = this.loadPictographsFromCSV();
        }
        this.pictographCache = await this.loadingPromise;
      }

      console.log(
        `📊 Loaded ${this.pictographCache.length} pictographs from CSV`
      );

      // TODO: In full implementation, filter by position based on last beat
      // For now, return all available pictographs
      if (sequence.length > 0) {
        // Could filter by end position of last beat here
        console.log(
          `🔍 Sequence has ${sequence.length} beats - position filtering not yet implemented`
        );
      }

      return this.pictographCache;
    } catch (error) {
      console.error("❌ Failed to load pictographs:", error);
      return this.createFallbackPictographs();
    }
  }

  /**
   * Load pictographs from CSV files (real data)
   */
  private async loadPictographsFromCSV(): Promise<PictographData[]> {
    try {
      console.log("📁 Loading pictograph data from CSV files");

      // Load both diamond and box data
      const [diamondResponse, boxResponse] = await Promise.all([
        fetch("/DiamondPictographDataframe.csv"),
        fetch("/BoxPictographDataframe.csv"),
      ]);

      if (!diamondResponse.ok || !boxResponse.ok) {
        throw new Error("Failed to load CSV files");
      }

      const [diamondCSV, boxCSV] = await Promise.all([
        diamondResponse.text(),
        boxResponse.text(),
      ]);

      // Parse CSV data
      const diamondPictographs = this.parseCSVToPictographs(
        diamondCSV,
        "diamond"
      );
      const boxPictographs = this.parseCSVToPictographs(boxCSV, "box");

      const allPictographs = [...diamondPictographs, ...boxPictographs];
      console.log(
        `✅ Loaded ${allPictographs.length} pictographs (${diamondPictographs.length} diamond, ${boxPictographs.length} box)`
      );

      return allPictographs;
    } catch (error) {
      console.error("❌ Failed to load CSV data:", error);
      throw error;
    }
  }

  /**
   * Parse CSV to PictographData objects
   */
  private parseCSVToPictographs(
    csvText: string,
    gridMode: string
  ): PictographData[] {
    const lines = csvText.trim().split("\n");
    if (lines.length < 2) return []; // Need header + data

    const headers = lines[0].split(",").map((h) => h.trim());
    const pictographs: PictographData[] = [];

    for (let i = 1; i < lines.length; i++) {
      try {
        const values = lines[i].split(",").map((v) => v.trim());
        const row: Record<string, string> = {};

        headers.forEach((header, index) => {
          row[header] = values[index] || "";
        });

        // Create pictograph from CSV row
        const pictograph = this.createPictographFromCSVRow(row, gridMode);
        if (pictograph) {
          pictographs.push(pictograph);
        }
      } catch (error) {
        console.warn(`⚠️ Failed to parse CSV row ${i}:`, error);
      }
    }

    return pictographs;
  }

  /**
   * Create PictographData from CSV row
   */
  private createPictographFromCSVRow(
    row: Record<string, string>,
    gridMode: string
  ): PictographData | null {
    try {
      // Extract letter (most important field)
      const letter = row.letter || row.Letter || null;
      if (!letter) {
        return null; // Skip rows without letters
      }

      // Create basic motion data from CSV fields with enum conversion
      const blueMotion = createMotionData({
        motion_type: this.mapMotionType(
          row.blue_motion_type || row.BlueMotionType || "static"
        ),
        prop_rot_dir: this.mapRotationDirection(
          row.blue_prop_rot_dir || row.BluePropRotDir || "no_rot"
        ),
        start_loc: this.mapLocation(
          row.blue_start_loc || row.BlueStartLoc || "n"
        ),
        end_loc: this.mapLocation(row.blue_end_loc || row.BlueEndLoc || "n"),
        turns:
          (this.parseNumber(row.blue_turns || row.BlueTurns) as number) || 0,
        start_ori: this.mapOrientation(
          row.blue_start_ori || row.BlueStartOri || "in"
        ),
        end_ori: this.mapOrientation(
          row.blue_end_ori || row.BlueEndOri || "in"
        ),
        is_visible: true,
      });

      const redMotion = createMotionData({
        motion_type: this.mapMotionType(
          row.red_motion_type || row.RedMotionType || "static"
        ),
        prop_rot_dir: this.mapRotationDirection(
          row.red_prop_rot_dir || row.RedPropRotDir || "no_rot"
        ),
        start_loc: this.mapLocation(
          row.red_start_loc || row.RedStartLoc || "n"
        ),
        end_loc: this.mapLocation(row.red_end_loc || row.RedEndLoc || "n"),
        turns: (this.parseNumber(row.red_turns || row.RedTurns) as number) || 0,
        start_ori: this.mapOrientation(
          row.red_start_ori || row.RedStartOri || "in"
        ),
        end_ori: this.mapOrientation(row.red_end_ori || row.RedEndOri || "in"),
        is_visible: true,
      });

      // Create pictograph with proper domain structure
      return createPictographData({
        letter,
        motions: {
          blue: blueMotion,
          red: redMotion,
        },
        start_pos: row.start_pos || row.StartPos || null,
        end_pos: row.end_pos || row.EndPos || null,
        grid_mode: gridMode,
        is_blank: false,
        metadata: {
          source: "csv",
          gridMode,
          originalRow: row,
        },
      });
    } catch (error) {
      console.warn("⚠️ Failed to create pictograph from CSV row:", error);
      return null;
    }
  }

  /**
   * Parse number from string, handling "fl" and other special values
   */
  private parseNumber(value: string): number | string {
    if (!value) return 0;
    if (value === "fl") return "fl";
    const num = parseFloat(value);
    return isNaN(num) ? 0 : num;
  }

  /**
   * Create fallback pictographs when CSV loading fails
   */
  private createFallbackPictographs(): PictographData[] {
    console.log("🔄 Creating fallback pictographs");

    // Create basic pictographs for common letters
    const letters = ["A", "B", "C", "D", "E", "F"];
    return letters.map((letter) =>
      createPictographData({
        letter,
        motions: {
          blue: {
            motion_type: MotionType.STATIC,
            prop_rot_dir: RotationDirection.NO_ROTATION,
            start_loc: Location.NORTH,
            end_loc: Location.NORTH,
            turns: 0,
            start_ori: Orientation.IN,
            end_ori: Orientation.IN,
            is_visible: true,
          },
          red: {
            motion_type: MotionType.STATIC,
            prop_rot_dir: RotationDirection.NO_ROTATION,
            start_loc: Location.NORTH,
            end_loc: Location.NORTH,
            turns: 0,
            start_ori: Orientation.IN,
            end_ori: Orientation.IN,
            is_visible: true,
          },
        },
        metadata: { source: "fallback" },
      })
    );
  }

  /**
   * Filter options by letter types - exact port from legacy _filter_options_by_letter_type()
   */
  filterOptionsByLetterTypes(
    options: PictographData[],
    letterTypes: string[]
  ): PictographData[] {
    if (!letterTypes || letterTypes.length === 0) {
      return options;
    }

    // Exact legacy letter type mapping from LetterType enum
    const letterTypeMap: { [key: string]: string[] } = {
      "Dual-Shift": [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
      ],
      Shift: ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"],
      "Cross-Shift": ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"],
      Dash: ["Φ", "Ψ", "Λ"],
      "Dual-Dash": ["Φ-", "Ψ-", "Λ-"],
      Static: ["α", "β", "Γ"],
    };

    // Get all selected letters - exact logic from legacy
    const selectedLetters: string[] = [];
    for (const letterType of letterTypes) {
      const letters = letterTypeMap[letterType];
      if (letters) {
        selectedLetters.push(...letters);
      }
    }

    console.log(`🔍 Filtering by letter types: ${letterTypes.join(", ")}`);
    console.log(`📝 Selected letters: ${selectedLetters.join(", ")}`);

    // Filter options - exact logic from legacy
    const filteredOptions = options.filter((option) =>
      selectedLetters.includes(option.letter || "")
    );

    console.log(
      `✅ After letter type filter: ${filteredOptions.length} options`
    );

    // Return filtered options, or all if none match (legacy behavior)
    return filteredOptions.length > 0 ? filteredOptions : options;
  }

  /**
   * Filter options by rotation - exact port from legacy filter_options_by_rotation()
   */
  filterOptionsByRotation(
    options: PictographData[],
    blueRotDir: string,
    redRotDir: string
  ): PictographData[] {
    console.log(
      `🔄 Filtering by rotation: blue=${blueRotDir}, red=${redRotDir}`
    );

    const filtered = options.filter((option) => {
      // Check motions structure (new domain model)
      const blueRot = option.motions?.blue?.prop_rot_dir || "no_rot";
      const redRot = option.motions?.red?.prop_rot_dir || "no_rot";

      // Legacy constants: CLOCKWISE = "cw", COUNTER_CLOCKWISE = "ccw", NO_ROT = "no_rot"
      const blueMatches = blueRot === blueRotDir || blueRot === "no_rot";
      const redMatches = redRot === redRotDir || redRot === "no_rot";

      return blueMatches && redMatches;
    });

    console.log(`✅ After rotation filter: ${filtered.length} options`);

    // Return filtered options, or all if none match (legacy behavior)
    return filtered.length > 0 ? filtered : options;
  }

  /**
   * Get options summary for debugging
   */
  getOptionsSummary(options: PictographData[]): {
    total: number;
    byLetterType: Record<string, number>;
    byMotionType: Record<string, number>;
  } {
    const summary = {
      total: options.length,
      byLetterType: {} as Record<string, number>,
      byMotionType: {} as Record<string, number>,
    };

    options.forEach((option) => {
      // Count by letter type
      const letterType = this.getLetterType(option.letter || "");
      summary.byLetterType[letterType] =
        (summary.byLetterType[letterType] || 0) + 1;

      // Count by motion type
      const blueMotion = option.motions?.blue?.motion_type || "unknown";
      const redMotion = option.motions?.red?.motion_type || "unknown";
      summary.byMotionType[blueMotion] =
        (summary.byMotionType[blueMotion] || 0) + 1;
      summary.byMotionType[redMotion] =
        (summary.byMotionType[redMotion] || 0) + 1;
    });

    return summary;
  }

  /**
   * Get letter type for a letter - exact mapping from legacy
   */
  private getLetterType(letter: string): string {
    const type1Letters = [
      "A",
      "B",
      "C",
      "D",
      "E",
      "F",
      "G",
      "H",
      "I",
      "J",
      "K",
      "L",
      "M",
      "N",
      "O",
      "P",
      "Q",
      "R",
      "S",
      "T",
      "U",
      "V",
    ];
    const type2Letters = ["W", "X", "Y", "Z", "Σ", "Δ", "θ", "Ω"];
    const type3Letters = ["W-", "X-", "Y-", "Z-", "Σ-", "Δ-", "θ-", "Ω-"];
    const type4Letters = ["Φ", "Ψ", "Λ"];
    const type5Letters = ["Φ-", "Ψ-", "Λ-"];
    const type6Letters = ["α", "β", "Γ"];

    if (type1Letters.includes(letter)) return "Dual-Shift";
    if (type2Letters.includes(letter)) return "Shift";
    if (type3Letters.includes(letter)) return "Cross-Shift";
    if (type4Letters.includes(letter)) return "Dash";
    if (type5Letters.includes(letter)) return "Dual-Dash";
    if (type6Letters.includes(letter)) return "Static";

    return "Unknown";
  }

  /**
   * Clear cache (for testing or reloading)
   */
  clearCache(): void {
    this.pictographCache = null;
    this.loadingPromise = null;
  }

  /**
   * Map string motion types to enum values
   */
  private mapMotionType(motionType: string): MotionType {
    switch (motionType.toLowerCase()) {
      case "pro":
        return MotionType.PRO;
      case "anti":
        return MotionType.ANTI;
      case "float":
        return MotionType.FLOAT;
      case "dash":
        return MotionType.DASH;
      case "static":
        return MotionType.STATIC;
      default:
        return MotionType.STATIC;
    }
  }

  /**
   * Map string rotation directions to enum values
   */
  private mapRotationDirection(rotDir: string): RotationDirection {
    switch (rotDir.toLowerCase()) {
      case "cw":
      case "clockwise":
        return RotationDirection.CLOCKWISE;
      case "ccw":
      case "counter_clockwise":
      case "counterclockwise":
        return RotationDirection.COUNTER_CLOCKWISE;
      case "no_rot":
      case "no_rotation":
        return RotationDirection.NO_ROTATION;
      default:
        return RotationDirection.NO_ROTATION;
    }
  }

  /**
   * Map string locations to enum values
   */
  private mapLocation(location: string): Location {
    switch (location.toLowerCase()) {
      case "n":
        return Location.NORTH;
      case "e":
        return Location.EAST;
      case "s":
        return Location.SOUTH;
      case "w":
        return Location.WEST;
      case "ne":
        return Location.NORTHEAST;
      case "se":
        return Location.SOUTHEAST;
      case "sw":
        return Location.SOUTHWEST;
      case "nw":
        return Location.NORTHWEST;
      default:
        return Location.NORTH;
    }
  }

  /**
   * Map string orientations to enum values
   */
  private mapOrientation(orientation: string): Orientation {
    switch (orientation.toLowerCase()) {
      case "in":
        return Orientation.IN;
      case "out":
        return Orientation.OUT;
      case "clock":
        return Orientation.CLOCK;
      case "counter":
        return Orientation.COUNTER;
      default:
        return Orientation.IN;
    }
  }

  /**
   * Convert CSV row to PictographData - public method for other services
   */
  convertCsvRowToPictographData(
    row: Record<string, string>,
    _index: number
  ): PictographData | null {
    // Use the existing createPictographFromCSVRow method
    return this.createPictographFromCSVRow(row, "diamond");
  }
}
