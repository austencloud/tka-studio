/**
 * Position Mapping Service Interface
 *
 * Service for mapping between hand location combinations and grid positions.
 * A position represents the combination of (blue_hand_location, red_hand_location).
 */

import { Location, GridPosition } from "$lib/domain/enums";

export interface IPositionMappingService {
  /**
   * Get the hand location pair for a given position
   */
  getLocationPair(position: GridPosition): [Location, Location];

  /**
   * Get the position for a given hand location pair
   */
  getPositionFromLocations(
    blueLocation: Location,
    redLocation: Location
  ): GridPosition;
}
