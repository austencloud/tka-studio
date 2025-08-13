/**
 * Simple PNG Metadata Extractor
 * Reads TKA sequence metadata directly from PNG files
 */

export class PngMetadataExtractor {
  /**
   * Extract metadata from a PNG file
   * @param filePath - Path to the PNG file (relative to static directory)
   * @returns Promise<any> - The extracted metadata JSON
   */
  static async extractMetadata(filePath: string): Promise<any> {
    try {
      // Fetch the PNG file
      const response = await fetch(filePath);
      if (!response.ok) {
        throw new Error(
          `Failed to fetch PNG file: ${response.status} ${response.statusText}`
        );
      }

      const arrayBuffer = await response.arrayBuffer();
      const uint8Array = new Uint8Array(arrayBuffer);

      // Find the tEXt chunk containing our metadata (use "metadata" keyword)
      const metadata = this.findTextChunk(uint8Array, "metadata");

      if (!metadata) {
        throw new Error("No metadata found in PNG file");
      }

      // Parse the JSON metadata and extract the sequence array
      const parsed = JSON.parse(metadata);
      return parsed.sequence || parsed;
    } catch (error) {
      console.error("Error extracting PNG metadata:", error);
      throw error;
    }
  }

  /**
   * Find a specific tEXt chunk in PNG data
   * @param data - PNG file data as Uint8Array
   * @param keyword - The keyword to search for (use "metadata" for TKA sequences)
   * @returns string | null - The text data or null if not found
   */
  private static findTextChunk(
    data: Uint8Array,
    keyword: string
  ): string | null {
    let offset = 8; // Skip PNG signature

    while (offset < data.length) {
      // Read chunk length (4 bytes, big-endian)
      const length =
        (data[offset] << 24) |
        (data[offset + 1] << 16) |
        (data[offset + 2] << 8) |
        data[offset + 3];
      offset += 4;

      // Read chunk type (4 bytes)
      const type = String.fromCharCode(
        data[offset],
        data[offset + 1],
        data[offset + 2],
        data[offset + 3]
      );
      offset += 4;

      // If this is a tEXt chunk, check if it contains our keyword
      if (type === "tEXt") {
        const chunkData = data.slice(offset, offset + length);
        const text = new TextDecoder("latin1").decode(chunkData);

        // Find the null separator between keyword and text
        const nullIndex = text.indexOf("\0");
        if (nullIndex !== -1) {
          const chunkKeyword = text.substring(0, nullIndex);
          if (chunkKeyword === keyword) {
            return text.substring(nullIndex + 1);
          }
        }
      }

      // Skip chunk data and CRC (4 bytes)
      offset += length + 4;
    }

    return null;
  }

  /**
   * Extract metadata for a specific sequence by name
   * @param sequenceName - Name of the sequence (e.g., "DKIIEJII")
   * @returns Promise<any> - The extracted metadata JSON
   */
  static async extractSequenceMetadata(sequenceName: string): Promise<any> {
    const filePath = `/dictionary/${sequenceName}/${sequenceName}_ver1.png`;
    return this.extractMetadata(filePath);
  }

  /**
   * Quick debug method to log metadata for a sequence
   * @param sequenceName - Name of the sequence
   */
  static async debugSequenceMetadata(sequenceName: string): Promise<void> {
    try {
      console.log(
        `🔍 [PNG METADATA] Extracting metadata for ${sequenceName}...`
      );
      const metadata = await this.extractSequenceMetadata(sequenceName);

      console.log(`📋 [PNG METADATA] Raw metadata for ${sequenceName}:`);
      console.log(JSON.stringify(metadata, null, 2));

      // Extract motion types for each beat
      console.log(`🎯 [PNG METADATA] Motion types for ${sequenceName}:`);
      metadata.forEach((step: any) => {
        if (step.beat && step.beat > 0) {
          const blueMotion = step.blue_attributes?.motion_type || "unknown";
          const redMotion = step.red_attributes?.motion_type || "unknown";
          console.log(
            `  Beat ${step.beat} (${step.letter}): blue=${blueMotion}, red=${redMotion}`
          );
        }
      });
    } catch (error) {
      console.error(
        `❌ [PNG METADATA] Failed to extract metadata for ${sequenceName}:`,
        error
      );
    }
  }
}

// Global utility function for easy access in console (browser only)
if (typeof window !== "undefined") {
  (window as any).extractPngMetadata =
    PngMetadataExtractor.debugSequenceMetadata;
}
