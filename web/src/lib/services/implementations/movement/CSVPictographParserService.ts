/**
 * CSV Pictograph Parser Service - Converts CSV rows to PictographData objects
 *
 * Parses the BoxPictographDataframe.csv data and converts it to typed PictographData.
 * Uses the correct position mapping based on hand location combinations.
 */

import { Letter } from "$lib/domain/Letter";
import { createMotionData } from "$lib/domain/MotionData";
import type { PictographData } from "$lib/domain/PictographData";
import { createPictographData } from "$lib/domain/PictographData";
import { MotionColor } from "$lib/domain/enums";
import type { IEnumMappingService } from "../data/EnumMappingService";
import type { IPositionMapper } from "../../interfaces/positioning-interfaces";
import { injectable, inject } from "inversify";
import { TYPES } from "../../inversify/types";

export interface CSVRow {
  letter: string;
  startPosition: string;
  endPosition: string;
  timing: string;
  direction: string;
  blueMotionType: string;
  blueRotationDirection: string;
  blueStartLocation: string;
  blueEndLocation: string;
  redMotionType: string;
  redRotationDirection: string;
  redStartLocation: string;
  redEndLocation: string;
}

export interface ICSVPictographParserService {
  parseCSVRowToPictograph(row: CSVRow): PictographData;
  parseLetterPictographs(letterRows: CSVRow[]): PictographData[];
  validateCSVRow(row: unknown): row is CSVRow;
}

@injectable()
export class CSVPictographParserService implements ICSVPictographParserService {
  constructor(
    @inject(TYPES.IPositionMapper)
    private readonly positionMapper: IPositionMapper,
    @inject(TYPES.IEnumMappingService)
    private readonly enumMapper: IEnumMappingService
  ) {}

  /**
   * Convert a CSV row to PictographData object
   */
  parseCSVRowToPictograph(row: CSVRow): PictographData {
    // Parse letter
    const letter = row.letter as Letter;

    // Parse blue hand motion
    const blueMotion = createMotionData({
      motionType: this.enumMapper.mapMotionType(row.blueMotionType),
      rotationDirection: this.enumMapper.mapRotationDirection(
        row.blueRotationDirection
      ),
      startLocation: this.enumMapper.mapLocation(row.blueStartLocation),
      endLocation: this.enumMapper.mapLocation(row.blueEndLocation),
      color: MotionColor.BLUE,
    });

    // Parse red hand motion
    const redMotion = createMotionData({
      motionType: this.enumMapper.mapMotionType(row.redMotionType),
      rotationDirection: this.enumMapper.mapRotationDirection(
        row.redRotationDirection
      ),
      startLocation: this.enumMapper.mapLocation(row.redStartLocation),
      endLocation: this.enumMapper.mapLocation(row.redEndLocation),
      color: MotionColor.RED,
    });

    return createPictographData({
      letter,
      startPosition: row.startPosition,
      endPosition: row.endPosition,
      motions: {
        [MotionColor.BLUE]: blueMotion,
        [MotionColor.RED]: redMotion,
      },
    });
  }

  /**
   * Parse multiple CSV rows for a letter
   */
  parseLetterPictographs(letterRows: CSVRow[]): PictographData[] {
    return letterRows.map((row) => this.parseCSVRowToPictograph(row));
  }

  /**
   * Validate that a CSV row has the expected structure
   */
  validateCSVRow(row: unknown): row is CSVRow {
    const requiredFields = [
      "letter",
      "startPosition",
      "endPosition",
      "timing",
      "direction",
      "blueMotionType",
      "blueRotationDirection",
      "blueStartLocation",
      "blueEndLocation",
      "redMotionType",
      "redRotationDirection",
      "redStartLocation",
      "redEndLocation",
    ];

    return requiredFields.every(
      (field) =>
        row &&
        typeof row === "object" &&
        field in row &&
        (row as Record<string, unknown>)[field] !== undefined
    );
  }
}
