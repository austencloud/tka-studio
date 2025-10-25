/**
 * CSV Pictograph Parser Service - Converts CSV rows to PictographData objects
 *
 * Parses the BoxPictographDataframe.csv data and converts it to typed PictographData.
 * Uses the correct position mapping based on hand location combinations.
 */

import type { CSVRow, ICSVPictographParser, IEnumMapper, IOrientationCalculationService } from "$shared";
import { GridPosition, Letter, MotionColor, createMotionData, createPictographData, type PictographData } from "$shared";
import { TYPES } from "$shared/inversify/types";
import { Orientation } from "$shared/pictograph/shared/domain/enums/pictograph-enums";
import { inject, injectable } from "inversify";

@injectable()
export class CSVPictographParser implements ICSVPictographParser {
  constructor(
    @inject(TYPES.IGridPositionDeriver)
    private readonly positionMapper: any,
    @inject(TYPES.IEnumMapper)
    private readonly enumMapper: IEnumMapper,
    @inject(TYPES.IOrientationCalculationService)
    private readonly orientationService: IOrientationCalculationService
  ) {}

  /**
   * Convert a CSV row to PictographData object
   */
  parseCSVRowToPictograph(row: CSVRow): PictographData {
    // Convert string letter to Letter enum (e.g., "A" -> Letter.A)
    const letter = row.letter as Letter;

    // Create temporary blue motion for orientation calculation
    const tempBlueMotion = createMotionData({
      motionType: this.enumMapper.mapMotionType(row.blueMotionType),
      rotationDirection: this.enumMapper.mapRotationDirection(
        row.blueRotationDirection
      ),
      startLocation: this.enumMapper.mapLocation(row.blueStartLocation),
      endLocation: this.enumMapper.mapLocation(row.blueEndLocation),
      startOrientation: Orientation.IN, // Default start orientation
      turns: 0, // Default turns for CSV data
      color: MotionColor.BLUE,
    });

    // Calculate blue end orientation dynamically
    const blueEndOrientation = this.orientationService.calculateEndOrientation(
      tempBlueMotion,
      MotionColor.BLUE
    );

    // Create final blue motion with calculated end orientation
    const blueMotion = createMotionData({
      motionType: this.enumMapper.mapMotionType(row.blueMotionType),
      rotationDirection: this.enumMapper.mapRotationDirection(
        row.blueRotationDirection
      ),
      startLocation: this.enumMapper.mapLocation(row.blueStartLocation),
      endLocation: this.enumMapper.mapLocation(row.blueEndLocation),
      startOrientation: Orientation.IN,
      endOrientation: blueEndOrientation, // Include calculated orientation
      turns: 0,
      color: MotionColor.BLUE,
    });

    // Create temporary red motion for orientation calculation
    const tempRedMotion = createMotionData({
      motionType: this.enumMapper.mapMotionType(row.redMotionType),
      rotationDirection: this.enumMapper.mapRotationDirection(
        row.redRotationDirection
      ),
      startLocation: this.enumMapper.mapLocation(row.redStartLocation),
      endLocation: this.enumMapper.mapLocation(row.redEndLocation),
      startOrientation: Orientation.IN, // Default start orientation
      turns: 0, // Default turns for CSV data
      color: MotionColor.RED,
    });

    // Calculate red end orientation dynamically
    const redEndOrientation = this.orientationService.calculateEndOrientation(
      tempRedMotion,
      MotionColor.RED
    );

    // Create final red motion with calculated end orientation
    const redMotion = createMotionData({
      motionType: this.enumMapper.mapMotionType(row.redMotionType),
      rotationDirection: this.enumMapper.mapRotationDirection(
        row.redRotationDirection
      ),
      startLocation: this.enumMapper.mapLocation(row.redStartLocation),
      endLocation: this.enumMapper.mapLocation(row.redEndLocation),
      startOrientation: Orientation.IN,
      endOrientation: redEndOrientation, // Include calculated orientation
      turns: 0,
      color: MotionColor.RED,
    });

    // CSV parsing completed successfully

    return createPictographData({
      letter,
      startPosition: this.mapStringToGridPosition(row.startPosition),
      endPosition: this.mapStringToGridPosition(row.endPosition),
      motions: {
        [MotionColor.BLUE]: blueMotion,
        [MotionColor.RED]: redMotion,
      },
    });
  }

  /**
   * Convert string position to GridPosition enum
   */
  private mapStringToGridPosition(position: string): GridPosition | null {
    const upperPosition = position.toUpperCase();

    // Convert to enum format (e.g., "alpha1" -> "ALPHA1")
    const enumKey = upperPosition.replace(
      /(\d)/,
      (match) => match
    ) as keyof typeof GridPosition;

    // Check if it's a valid GridPosition
    if (enumKey in GridPosition) {
      return GridPosition[enumKey];
    }

    return null;
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
