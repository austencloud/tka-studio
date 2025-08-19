/**
 * CSV Movement Parser Service - Converts CSV rows to MovementData objects
 *
 * Parses the BoxPictographDataframe.csv data and converts it to typed MovementData.
 * Uses the correct position mapping based on hand location combinations.
 */

import type { MovementData, HandMovement } from '$lib/domain/MovementData';
import { createMovementData, createHandMovement } from '$lib/domain/MovementData';
import { PositionMappingService } from './PositionMappingService';

interface CSVRow {
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

export class CSVMovementParserService {
  private readonly positionMapper: PositionMappingService;

  constructor() {
    this.positionMapper = new PositionMappingService();
  }

  /**
   * Convert a CSV row to MovementData object
   */
  parseCSVRowToMovement(row: CSVRow): MovementData {
    // Parse positions
    const startPosition = this.positionMapper.stringToGridPosition(row.startPosition);
    const endPosition = this.positionMapper.stringToGridPosition(row.endPosition);
    
    // Parse timing and direction
    const timing = this.positionMapper.stringToTiming(row.timing);
    const direction = this.positionMapper.stringToDirection(row.direction);
    
    // Parse blue hand movement
    const blueHand = createHandMovement({
      motionType: this.positionMapper.stringToMotionType(row.blueMotionType),
      rotationDirection: this.positionMapper.stringToRotationDirection(row.blueRotationDirection),
      startLocation: this.positionMapper.stringToLocation(row.blueStartLocation),
      endLocation: this.positionMapper.stringToLocation(row.blueEndLocation),
    });
    
    // Parse red hand movement
    const redHand = createHandMovement({
      motionType: this.positionMapper.stringToMotionType(row.redMotionType),
      rotationDirection: this.positionMapper.stringToRotationDirection(row.redRotationDirection),
      startLocation: this.positionMapper.stringToLocation(row.redStartLocation),
      endLocation: this.positionMapper.stringToLocation(row.redEndLocation),
    });

    return createMovementData({
      letter: row.letter,
      startPosition,
      endPosition,
      timing,
      direction,
      blueHand,
      redHand,
    });
  }

  /**
   * Parse multiple CSV rows for a letter
   */
  parseLetterMovements(letterRows: CSVRow[]): MovementData[] {
    return letterRows.map(row => this.parseCSVRowToMovement(row));
  }

  /**
   * Validate that a CSV row has the expected structure
   */
  validateCSVRow(row: any): row is CSVRow {
    const requiredFields = [
      'letter', 'startPosition', 'endPosition', 'timing', 'direction',
      'blueMotionType', 'blueRotationDirection', 'blueStartLocation', 'blueEndLocation',
      'redMotionType', 'redRotationDirection', 'redStartLocation', 'redEndLocation'
    ];
    
    return requiredFields.every(field => row && row[field] !== undefined);
  }
}
