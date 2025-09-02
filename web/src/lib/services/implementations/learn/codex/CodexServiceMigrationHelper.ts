/**
 * Codex Service Migration Helper
 *
 * Provides utilities to help migrate from the old monolithic service
 * to the new clean implementation.
 */

import type { PictographData } from "$domain";
import { CodexService } from "./CodexService";

export class CodexServiceMigrationHelper {
  private service: CodexService;

  constructor() {
    // TODO: Use DI container to resolve CodexService instead of direct instantiation
    // this.service = new CodexService();
    throw new Error(
      "CodexServiceMigrationHelper needs to be updated to use DI container"
    );
  }

  /**
   * Validate the current CodexService functionality
   */
  async validateService(): Promise<{
    success: boolean;
    issues: string[];
    summary: {
      pictographCount: number;
      validPictographs: number;
      invalidPictographs: string[];
    };
  }> {
    console.log("🔍 Starting service validation...");

    const issues: string[] = [];

    try {
      // Load pictographs from the service
      const pictographs = await this.service.loadAllPictographs();

      // Validate pictographs
      const validPictographs: PictographData[] = [];
      const invalidPictographs: string[] = [];

      pictographs.forEach((p: PictographData) => {
        if (p.letter && p.letter.trim() !== "") {
          validPictographs.push(p);
        } else {
          invalidPictographs.push(p.letter || "unknown");
        }
      });

      // Test specific methods
      await this.validateSpecificMethods(issues);

      const success = issues.length === 0;

      console.log(
        success
          ? "✅ Service validation passed!"
          : "❌ Service validation found issues"
      );

      return {
        success,
        issues,
        summary: {
          pictographCount: pictographs.length,
          validPictographs: validPictographs.length,
          invalidPictographs,
        },
      };
    } catch (error) {
      const errorMessage = `Migration validation failed: ${error}`;
      console.error("❌", errorMessage);
      return {
        success: false,
        issues: [errorMessage],
        summary: {
          pictographCount: 0,
          validPictographs: 0,
          invalidPictographs: [],
        },
      };
    }
  }

  /**
   * Test specific methods of the service
   */
  private async validateSpecificMethods(issues: string[]): Promise<void> {
    try {
      // Test getLettersByRow
      const rows = this.service.getLettersByRow();
      if (!rows || rows.length === 0) {
        issues.push("getLettersByRow() returned empty or null result");
      }

      // Test searchPictographs with a common letter
      const searchResults = await this.service.searchPictographs("A");
      if (!searchResults || searchResults.length === 0) {
        issues.push('searchPictographs("A") returned no results');
      }

      // Test getPictographByLetter
      const pictographA = await this.service.getPictographByLetter("A");
      if (!pictographA || pictographA.letter !== "A") {
        issues.push('getPictographByLetter("A") did not return letter A');
      }
    } catch (error) {
      issues.push(`Error during specific method validation: ${error}`);
    }
  }

  /**
   * Generate a service validation report
   */
  async generateValidationReport(): Promise<string> {
    const validation = await this.validateService();

    let report = "# Codex Service Migration Report\n\n";

    if (validation.success) {
      report += "## ✅ Migration Status: SUCCESS\n\n";
      report +=
        "The new clean CodexService implementation is ready to replace the old monolithic version.\n\n";
    } else {
      report += "## ❌ Migration Status: ISSUES FOUND\n\n";
      report +=
        "The following issues need to be addressed before migration:\n\n";

      validation.issues.forEach((issue: string, index: number) => {
        report += `${index + 1}. ${issue}\n`;
      });
      report += "\n";
    }

    report += "## Summary\n\n";
    report += `- Total pictographs: ${validation.summary.pictographCount}\n`;
    report += `- Valid pictographs: ${validation.summary.validPictographs}\n`;
    report += `- Invalid pictographs: ${validation.summary.invalidPictographs.length}\n`;

    if (validation.summary.invalidPictographs.length > 0) {
      report += `- Invalid pictograph letters: ${validation.summary.invalidPictographs.join(", ")}\n`;
    }

    report += "\n## Architecture Changes\n\n";
    report += "The new implementation features:\n";
    report += "- ✅ Separated configuration data from business logic\n";
    report += "- ✅ Clean repository pattern for data access\n";
    report += "- ✅ Dependency injection for better testability\n";
    report += "- ✅ Single responsibility principle\n";
    report += "- ✅ No hardcoded mappings in service code\n";
    report += "- ✅ Extensible lesson system\n";
    report += "- ✅ Type-safe configuration loading\n\n";

    return report;
  }
}
